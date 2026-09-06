"""Manifest-scoped materialization and deliberate accepted-governance refresh."""
from __future__ import annotations
import os
from pathlib import Path
import stat
import time
import tomllib
from oap_core import (OAPError, require, safe_path, topology, read, jsread, digest,
                      atomic, json_bytes, lock, git, governance, active_id,
                      matching, git_blob, strategic_path, fifo_home, make_private_dirs)

ENV_KEYS = {
    "OAP_REPO_ROOT", "OAP_STRATEGIC_HOME", "OAP_FIFO_HOME", "OAP_GITHUB_REPOSITORY", "CODEX_BIN",
    "CODING_CODEX_HOME", "STRATEGIC_CODEX_HOME", "CODING_CODEX_PROFILE", "CODING_CODEX_MODEL",
    "STRATEGIC_CODEX_PROFILE", "STRATEGIC_CODEX_MODEL", "OAP_ACK_DANGER_FULL_ACCESS",
    "OAP_ACK_START_LOOP", "OAP_SETUP_TMUX_SESSION", "OAP_RUN_TMUX_SESSION",
    "REPAIR_QWEN_BASE_URL", "REPAIR_QWEN_MODEL", "REPAIR_QWEN_API_KEY_ENV",
    "REPAIR_ALLOW_LIVE_TESTS", "REPAIR_API_HOST", "REPAIR_API_PORT", "OAP_ACCEPTED_REF",
    "OAP_MERGE_EFFECT", "OAP_CLI_QUALIFIED_VERSION", "OAP_ROLE_AUTH_READY",
}


def runtime_defaults(repo, strategy, *, layout_repo=None):
    value = {k: "" for k in ENV_KEYS}
    value.update(OAP_REPO_ROOT=str(repo), OAP_STRATEGIC_HOME=str(strategy), CODEX_BIN="codex",
                 OAP_FIFO_HOME=str(fifo_home(layout_repo or repo, strategy)),
                 CODING_CODEX_HOME=str(strategy / "codex-homes/coding"),
                 STRATEGIC_CODEX_HOME=str(strategy / "codex-homes/strategic"),
                 OAP_ACK_DANGER_FULL_ACCESS="NO", OAP_ACK_START_LOOP="NO",
                 REPAIR_ALLOW_LIVE_TESTS="NO", REPAIR_API_HOST="127.0.0.1",
                 OAP_SETUP_TMUX_SESSION="slovenian-repair-setup", OAP_RUN_TMUX_SESSION="slovenian-repair-run")
    return value


def env_bytes(value):
    import json
    return ("# Data only: KEY=JSON string. Parsed without shell execution.\n" +
            "\n".join(k + "=" + json.dumps(v, ensure_ascii=False) for k, v in sorted(value.items())) + "\n").encode()


def runtime_config(path, environ=None, *, repo=None):
    import json
    p = strategic_path(path, repo=repo, kind="file")
    result = {}
    for line in read(p).decode().splitlines():
        if not line or line.startswith("#"):
            continue
        k, sep, v = line.partition("=")
        require(sep and k in ENV_KEYS and k not in result, "CONFIG_KEY")
        try:
            value = json.loads(v)
        except ValueError as e:
            raise OAPError("CONFIG_SYNTAX") from e
        require(isinstance(value, str) and "\n" not in value and "\0" not in value, "CONFIG_VALUE")
        result[k] = value
    require(set(result) == ENV_KEYS, "CONFIG_MISSING_KEYS")
    env = os.environ if environ is None else environ
    for k, v in result.items():
        require(k not in env or env[k] == v, "CONFIG_AUTHORITY_CONFLICT", k)
    return result


def private_files(repo, strategy):
    files = {}
    for name in ("AGENTS.md", "OAP-COMMUNICATION-strategic.md", "strategic_model_init_material.md", "INITIAL-ROADMAP.md"):
        files[name] = (read(repo / "oap/strategic-instructions" / name), "governance")
    for p in (repo / "oap/strategic-instructions/initial-orders").glob("*.md"):
        files["drafts/" + p.name] = (read(p), "private")
    for p in (repo / "oap/audit/requests").glob("*.md"):
        files["audit/requests/" + p.name] = (read(p), "private")
    refs = "# Canonical source references\n\nThese are references, not independently editable mirrors.\n\n"
    for name in ("PLAN.md", "ARCHITECTURE.md", "CRITICAL.md"):
        refs += f"- {name}: `{repo / name}`; bootstrap SHA-256 `{digest(read(repo / name))}`.\n"
    refs += "\nCurrent accepted reference: unresolved until authorized baseline publication.\nCRITICAL grows by exact authorized EOF appends; its bootstrap digest is a seed identity.\n"
    files["SOURCE-REFERENCES.md"] = (refs.encode(), "governance")
    files["RUNTIME.md"] = (b"# Strategic runtime\n\nInactive bootstrap. runtime.env is the only runtime authority, parsed as allowlisted JSON-string assignments without execution. Never source it in a shell. OAP_FIFO_HOME contains the real control.fifo and response.fifo; it is resolved from the owner-approved WORKSPACE-LAYOUT.json when strategy uses the selected sync folder. Native FIFO directory/files retain 0700/0600. All regular strategic files, configuration, logs, drafts and separate role homes remain in STRATEGIC_HOME. The selected sync mount has its own permission semantics; no POSIX private-mode guarantee is asserted there. Other paths retain strict checks. Models, profiles, authentication and activation require deliberate setup. A role label is routing, not authentication. No activation or live Qwen test is implied by relocation.\n", "governance")
    files["runtime.env"] = (env_bytes(runtime_defaults(repo, strategy)), "private")
    files["workorders/EXECUTION_TIMINGS.md"] = (b"# Execution timings\n\nNo operational execution has occurred. Append ID, observed start/end UTC, implementation/report SHA and evidence reference after actual work. Separate coding time, CI/data waiting, model inference and human annotation; no invented duration.\n", "private")
    files["workorders/STRATEGIC-HANDOFF.md"] = (b"# Strategic handoff\n\nBOOTSTRAP ONLY. Product PLANNED; tests NOT RUN. No active order, PR, remote baseline, ICA or human acceptance. After owner review/publication, reconcile real sources, remote main, local work, CI, role profiles and disabled gates before finalizing 000-a. Do not repeat scaffold generation or execute the queue from this handoff. Preserve same unresolved order/branch/PR after any process replacement.\n", "private")
    for role in ("coding", "strategic"):
        # Empty valid TOML avoids guessing provider/model/context keys.
        files[f"codex-homes/{role}/config.toml"] = (("# Separate " + role + " home. Model/profile intentionally unresolved.\n# Runtime launch selects an explicit model or profile; no credentials copied.\n").encode(), "private")
    return files


def inspect_repository(repo):
    if not repo.exists():
        return {"git": "absent", "dirty": [], "origin": "absent"}
    safe_path(repo, kind="dir")
    p = git(repo, "rev-parse", "--show-toplevel", check=False)
    if p.returncode:
        require(not (repo / ".git").exists(), "INVALID_GIT_STATE")
        return {"git": "not initialized", "dirty": [], "origin": "absent"}
    require(Path(p.stdout.decode().strip()).resolve() == repo, "NESTED_GIT_REPOSITORY")
    dirty = git(repo, "status", "--porcelain=v1", "-z").decode().split("\0")
    origin = git(repo, "remote", "get-url", "origin", check=False)
    return {"git": "worktree" if (repo / ".git").is_file() else "repository",
            "dirty": [x for x in dirty if x], "origin": "configured (value redacted)" if origin.returncode == 0 else "absent"}


def materialize(source_repo, repo, strategy, bootstrap, *, dry_run=False, refresh=False):
    source_repo = safe_path(source_repo, kind="dir")
    _, repo, strategy = topology(bootstrap, repo, strategy)
    before = inspect_repository(repo)
    src_manifest = jsread(source_repo / "oap/GENERATED-FILES.json")
    repo_files = {}
    for rel, item in src_manifest["files"].items():
        require(not Path(rel).is_absolute() and ".." not in Path(rel).parts, "UNSAFE_MANIFEST_PATH")
        data = read(source_repo / rel)
        require(digest(data) == item["sha256"], "SOURCE_GENERATION_DRIFT", rel)
        repo_files[rel] = (data, item["class"])
    repo_files["oap/GENERATED-FILES.json"] = (read(source_repo / "oap/GENERATED-FILES.json"), "generated")
    repo_files["oap/BOOTSTRAP-MANIFEST.sha256"] = (read(source_repo / "oap/BOOTSTRAP-MANIFEST.sha256"), "generated")
    # All preflight calculations use source bytes; targets need not exist yet.
    private = private_files(source_repo, strategy)
    private["runtime.env"] = (env_bytes(runtime_defaults(repo, strategy, layout_repo=source_repo)), "private")
    pipes = fifo_home(source_repo, strategy)
    require(pipes == strategy or (pipes != bootstrap and Path(bootstrap) not in pipes.parents and pipes not in Path(bootstrap).parents), 'FIFO_BOOTSTRAP_OVERLAP')
    private["SOURCE-REFERENCES.md"] = (private["SOURCE-REFERENCES.md"][0].replace(str(source_repo).encode(), str(repo).encode()), "governance")
    plans, conflicts = [], []
    for root, desired in ((repo, repo_files), (strategy, private)):
        old_path = root / ("oap/INSTALLATION.json" if root == repo else ".bootstrap-manifest.json")
        prior = jsread(old_path)["files"] if old_path.exists() else {}
        for rel, (data, category) in desired.items():
            target = safe_path(root / rel, missing=True)
            if not target.exists():
                require(not (root == repo and rel == 'CRITICAL.md' and old_path.exists()), 'MISSING_LIVE_REGISTER_NO_RESEED')
                action = "created"
            elif read(target) == data:
                action = "identical"
            elif category == "private":
                action = "preserved-private"
            elif refresh and category == "generated" and rel in prior and digest(read(target)) == prior[rel]["sha256"]:
                action = "backed-up"
            else:
                action = "conflict"
                conflicts.append(rel)
            plans.append((root, rel, data, category, action))
    dirs = ["drafts", "critical-drafts", "workorders", "audit", "audit/requests", "audit/results", "logs", "bootstrap-backups", "codex-homes", "codex-homes/coding", "codex-homes/strategic"]
    for rel in ["", *dirs]:
        p = strategy / rel
        if p.exists():
            strategic_path(p, repo=source_repo, kind="dir")
    for name in ("control.fifo", "response.fifo"):
        p = safe_path(pipes / name, missing=True)
        if p.exists():
            safe_path(p, kind="fifo", private=True)
    require(not conflicts, "INSTALL_CONFLICT", ", ".join(conflicts[:8]))
    summary = {"counts": {a: sum(p[4] == a for p in plans) for a in ("created", "identical", "preserved-private", "backed-up")},
               "dry_run": dry_run, "repository_before": before, "files": [{"tree": "repo" if p[0] == repo else "strategy", "path": p[1], "action": p[4]} for p in plans]}
    if dry_run:
        return summary
    # Never lock or create anything during dry run. Real publication uses owned parent locks.
    repo.mkdir(parents=True, exist_ok=True)
    strategy.mkdir(parents=True, mode=0o700, exist_ok=True)
    strategic_path(strategy, repo=source_repo, kind="dir")
    make_private_dirs(pipes)
    with lock(strategy / ".bootstrap.lock"):
        for rel in dirs:
            (strategy / rel).mkdir(parents=True, mode=0o700, exist_ok=True)
        for root, rel, data, category, action in plans:
            if action in ("identical", "preserved-private"):
                continue
            target = root / rel
            target.parent.mkdir(parents=True, mode=0o700 if root == strategy else 0o755, exist_ok=True)
            # Recheck preflight observations under lock; unexpected arrivals are conflicts.
            if action == "created":
                require(not target.exists() or read(target) == data, "INSTALL_RACE")
            if action == "backed-up":
                old = read(target)
                backup = strategy / "bootstrap-backups" / (digest(old) + "-" + target.name)
                atomic(backup, old, mode=0o600, immutable=True)
            mode = 0o600 if root == strategy else (0o755 if rel.startswith("oap/bin/") and rel.endswith((".sh", ".py")) else 0o644)
            atomic(target, data, mode=mode)
        for name in ("control.fifo", "response.fifo"):
            p = pipes / name
            if not p.exists():
                os.mkfifo(p, 0o600)
        for root, desired in ((repo, repo_files), (strategy, private)):
            manifest = {"schema_version": 1, "files": {rel: {"sha256": digest(read(root / rel)), "class": cat} for rel, (_, cat) in desired.items()}}
            atomic(root / ("oap/INSTALLATION.json" if root == repo else ".bootstrap-manifest.json"), json_bytes(manifest), mode=0o644 if root == repo else 0o600)
        if before["git"] in ("absent", "not initialized"):
            git(repo, "init", "-b", "main")
    return summary


def refresh_governance(repo, strategy, accepted_ref, *, dry_run=False, remote=None):
    repo = Path(repo)
    strategy = strategic_path(strategy, repo=repo, kind="dir")
    governance(repo, "accepted-runtime", accepted_ref)
    # Locks are never inspected by mere file existence: persistent lock files are normal.
    ident = active_id(repo)
    require(ident is None or matching(repo, "reports", ident) is not None, "REFRESH_NOT_QUIESCENT")
    require(git(repo, "rev-parse", "HEAD").decode().strip() == accepted_ref, "REFRESH_NOT_ACCEPTED_HEAD")
    if ident:
        from oap_core import verify_report, metadata
        require(remote is not None, 'REFRESH_REMOTE_RECONCILIATION_REQUIRED')
        report_meta = metadata(read(matching(repo, 'reports', ident)), 'oap-report')
        pr = remote.pr(report_meta['pr'])
        require(pr.get('merged') is True, 'REFRESH_NOT_MERGED')
        verify_report(repo, ident, commit=pr['head']['sha'], remote=remote)
        order_meta = metadata(read(matching(repo, 'orders', ident)), 'oap-metadata')
        require(remote.api('branches/'+order_meta['default_branch'])['commit']['sha'] == accepted_ref, 'REFRESH_STALE_DEFAULT')
    names = ("AGENTS.md", "OAP-COMMUNICATION-strategic.md", "strategic_model_init_material.md")
    changed = [p for p in names if read(strategy / p) != git_blob(repo, accepted_ref, "oap/strategic-instructions/" + p)]
    if dry_run:
        return {"dry_run": True, "changed": changed, "writes": 0}
    with lock(strategy / ".coding.lock"), lock(strategy / ".strategic.lock"), lock(strategy / ".bootstrap.lock"):
        for name in changed:
            old = read(strategy / name)
            atomic(strategy / "bootstrap-backups" / (digest(old) + "-" + name), old, mode=0o600, immutable=True)
            atomic(strategy / name, git_blob(repo, accepted_ref, "oap/strategic-instructions/" + name), mode=0o600)
        refs = "# Canonical accepted source references\n\nAccepted Git revision: `" + accepted_ref + "`.\n\n"
        for name in ("PLAN.md", "ARCHITECTURE.md", "CRITICAL.md"):
            refs += f"- {name}: `{repo / name}`; accepted SHA-256 `{digest(git_blob(repo, accepted_ref, name))}`.\n"
        atomic(strategy / "SOURCE-REFERENCES.md", refs.encode(), mode=0o600)
    return {"result": "refreshed", "changed": changed, "reread_required": True}
