"""Shared, standard-library OAP validation. No model or network calls on import.

Metadata is JSON inside one named Markdown fence. Markdown remains readable;
only actual metadata is rejected for unresolved future facts. Files are bounded.
Authority cannot be authenticated by a Markdown label, hash or environment role.
"""
from __future__ import annotations

import base64
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import select
import stat
import subprocess
import tempfile
import time

ID_RE = re.compile(r"[0-9]{3}-[a-z]{1,2}\Z")
SHA_RE = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?\Z")
HASH_RE = re.compile(r"[0-9a-f]{64}\Z")
MAX_FILE = 2_000_000
CRIT_SECTIONS = (
    "Dilemma", "Decision taken", "Reasoning", "Alternatives considered",
    "Strongest argument that this decision is wrong", "Assumptions",
    "Failure mode and blast radius", "Mitigations and evidence",
    "Reversibility and rollback", "Safe autonomous continuation", "Exact human gate",
    "Exact question for the human adjudicator", "Strategic attestation",
    "Human disposition", "Resolution",
)
CRIT_FIELDS = ("Status", "Introduced by", "Category", "Severity", "Decision confidence",
               "Required human gate", "Affected components")
ORDER_SECTIONS = ("Identity", "Provenance", "Current verified state", "Governance",
                  "Goal and dependencies", "Scope", "Non-goals", "Files and boundaries",
                  "Requirements", "Acceptance criteria", "Verification", "Local setup and constraints",
                  "Documentation", "Git and report publication", "Decision classification",
                  "Deferred human adjudication")
DISPOSITIONS = {"ACCEPTED", "REJECTED", "CHANGE REQUIRED", "DEFERRED"}
RESULTS = {"COMPLETE", "PARTIAL", "BLOCKED", "FAILED"}
CHECKS = {"PASSED", "FAILED", "SKIPPED", "NOT RUN", "BLOCKED", "PENDING", "MISSING"}
READ_SET = ["AGENTS.md", "oap/coding-instructions/AGENTS.md", "ARCHITECTURE-for-agents.md",
            "OAP-COMMUNICATION-coding-agent.md", "SECURITY.md", "TESTING.md"]
GOV_SOURCE = ["PLAN.md", "ARCHITECTURE.md", "oap/strategic-instructions/AGENTS.md",
              "oap/strategic-instructions/OAP-COMMUNICATION-strategic.md",
              "oap/governance/WORKSPACE-LAYOUT.json"]
SUFFIX_ORDER = tuple(chr(c) for c in range(97, 123)) + tuple(
    a + b for a in (chr(c) for c in range(97, 123))
    for b in (chr(c) for c in range(97, 123))
)
TRANSCRIPT_FILENAME_RE = re.compile(
    r"(?P<id>[0-9]{3}-[a-z]{1,2})-[a-z0-9]+(?:-[a-z0-9]+)*\.md\Z"
)


class OAPError(Exception):
    def __init__(self, code, detail=""):
        self.code = code
        super().__init__(code + (": " + detail if detail else ""))


def require(value, code, detail=""):
    if not value:
        raise OAPError(code, detail)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(path, *, kind=None, private=False, missing=False):
    """Reject every symlink component; root-owned system ancestors are allowed.

    The final object must be current-user owned. No chmod or creation here.
    """
    p = Path(os.path.abspath(path))
    for item in reversed((p, *p.parents)):
        try:
            s = item.lstat()
        except FileNotFoundError:
            continue
        require(not stat.S_ISLNK(s.st_mode), "UNSAFE_SYMLINK")
        require(s.st_uid in (0, os.getuid()), "WRONG_ANCESTOR_OWNER")
        # /tmp is permitted only as sticky system ancestor of owned fixtures.
        require(not s.st_mode & stat.S_IWOTH or bool(s.st_mode & stat.S_ISVTX), "UNSAFE_ANCESTOR_MODE")
        if item != p:
            require(stat.S_ISDIR(s.st_mode), "WRONG_ANCESTOR_TYPE")
    if not p.exists():
        require(missing, "MISSING_PATH")
        return p
    s = p.lstat()
    require(s.st_uid == os.getuid(), "WRONG_OWNER")
    if kind:
        check = {"file": stat.S_ISREG, "dir": stat.S_ISDIR, "fifo": stat.S_ISFIFO}[kind]
        require(check(s.st_mode), "WRONG_TYPE", kind)
    if private:
        expected = 0o700 if stat.S_ISDIR(s.st_mode) else 0o600
        require(stat.S_IMODE(s.st_mode) == expected, "PRIVATE_MODE")
    return p


def topology(bootstrap, repo, strategy):
    roots = [safe_path(p, kind="dir", missing=True) for p in (bootstrap, repo, strategy)]
    for i, x in enumerate(roots):
        for y in roots[i + 1:]:
            require(x != y and x not in y.parents and y not in x.parents, "NESTED_ROOTS")
    return roots


def read(path, limit=MAX_FILE):
    p = safe_path(path, kind="file")
    require(p.stat().st_size <= limit, "OVERSIZED_FILE")
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as f:
        data = f.read(limit + 1)
    require(len(data) <= limit, "OVERSIZED_FILE")
    return data


def jsread(path):
    try:
        return json.loads(read(path), object_pairs_hook=unique_pairs)
    except (ValueError, UnicodeError) as e:
        raise OAPError("INVALID_JSON") from e


def unique_pairs(pairs):
    result = {}
    for k, v in pairs:
        require(k not in result, "DUPLICATE_JSON_KEY")
        result[k] = v
    return result


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def workspace_layout(repo=None):
    repo = Path(repo) if repo is not None else Path(__file__).resolve().parents[2]
    path = repo / 'oap/governance/WORKSPACE-LAYOUT.json'
    safe_path(path, missing=True)
    if not path.exists():
        return None
    value = jsread(path)
    require(value.get('schema_version') == 1 and value.get('strategic_storage') == 'owner-selected-sync', 'LAYOUT_SCHEMA')
    require(meaningful(value.get('authority')), 'LAYOUT_AUTHORITY_REFERENCE')
    s, f = Path(value.get('strategic_home', '')), Path(value.get('fifo_home', ''))
    require(s.is_absolute() and f.is_absolute() and len(s.parts) >= 4 and len(f.parts) >= 4, 'LAYOUT_ABSOLUTE_PATHS')
    require(s != Path.home() and f != Path.home(), 'LAYOUT_BROAD_ROOT')
    require(s != f and s not in f.parents and f not in s.parents, 'LAYOUT_FIFO_OVERLAP')
    require(f != repo and f not in repo.parents and repo not in f.parents, 'LAYOUT_FIFO_OVERLAP')
    return value


def strategic_path(path, *, repo=None, kind=None, missing=False):
    """Only the owner's exact sync subtree has different POSIX mode semantics.

    All native/other paths still use strict private modes. No symlink, type,
    ownership or broad-directory check is bypassed. Launch also checks accepted
    governance, so candidate-authored layout hashes cannot authorize activation.
    """
    p = safe_path(path, kind=kind, missing=missing)
    layout = workspace_layout(repo)
    root = Path(layout['strategic_home']) if layout else None
    synced = root is not None and (p == root or root in p.parents)
    return safe_path(p, kind=kind, missing=missing, private=not synced)


def fifo_home(repo, strategy):
    layout = workspace_layout(repo)
    if layout and Path(strategy) == Path(layout['strategic_home']):
        return safe_path(layout['fifo_home'], kind='dir', private=True, missing=True)
    return safe_path(strategy, kind='dir', private=True, missing=True)


def make_private_dirs(path):
    """Create only missing directories; never chmod an existing parent tree."""
    path = safe_path(path, kind='dir', private=True, missing=True)
    missing = []
    p = path
    while not p.exists():
        missing.append(p)
        p = p.parent
    for p in reversed(missing):
        p.mkdir(mode=0o700)
        safe_path(p, kind='dir', private=True)


def atomic(path, data, *, mode=0o644, immutable=False):
    p = safe_path(path, missing=True)
    safe_path(p.parent, kind="dir")
    if p.exists():
        old = read(p)
        if old == data:
            return "identical"
        require(not immutable, "IMMUTABLE_CONFLICT")
    fd, tmp = tempfile.mkstemp(prefix=".oap-write-", dir=p.parent)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        if immutable:
            try:
                os.link(tmp, p, follow_symlinks=False)
            except FileExistsError:
                require(read(p) == data, "IMMUTABLE_CONFLICT")
            except OSError as exc:
                import errno
                require(exc.errno in (errno.EPERM, errno.EOPNOTSUPP, errno.ENOSYS), 'IMMUTABLE_LINK_FAILED')
                # Sync mounts may reject hard links and RENAME_NOREPLACE. Serialize
                # cooperating local writers, recheck the exact final target under
                # that lock, then atomically rename a completely flushed temporary
                # file. This is not a distributed lock across multiple machines.
                guard = p.parent / ('.oap-immutable-' + digest(p.name.encode())[:20] + '.lock')
                with lock(guard):
                    safe_path(p, missing=True)
                    if p.exists():
                        require(read(p) == data, 'IMMUTABLE_CONFLICT')
                    else:
                        os.replace(tmp, p)
        else:
            os.replace(tmp, p)
        d = os.open(p.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(d)
        finally:
            os.close(d)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return "written"


@contextlib.contextmanager
def lock(path):
    p = safe_path(path, missing=True)
    fd = os.open(p, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    try:
        require(os.fstat(fd).st_uid == os.getuid() and stat.S_ISREG(os.fstat(fd).st_mode), "UNSAFE_LOCK")
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as e:
            raise OAPError("LOCKED") from e
        yield
    finally:
        os.close(fd)


def git(repo, *args, check=True):
    env = os.environ.copy()
    env['GIT_OPTIONAL_LOCKS'] = '0'
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, timeout=30, env=env)
    if check:
        require(p.returncode == 0, "GIT_FAILURE", args[0])
    return p.stdout if check else p


def git_blob(repo, ref, path):
    require(bool(SHA_RE.fullmatch(ref)), "TRUSTED_REF_REQUIRED")
    require(not path.startswith("/") and ".." not in Path(path).parts, "UNSAFE_RELATIVE_PATH")
    return git(repo, "show", f"{ref}:{path}")


def section_map(text, prefix="## "):
    """Only headings outside fences count as register/order structure."""
    out, current, lines, fence = {}, None, [], None
    for line in text.splitlines(keepends=True):
        opening = re.match(r"^(`{3,}|~{3,})([^\n]*)\n?$", line)
        if fence:
            if re.fullmatch(re.escape(fence[0]) + "{" + str(fence[1]) + r",}\s*", line):
                fence = None
            if current is not None:
                lines.append(line)
            continue
        if opening:
            fence = (opening[1][0], len(opening[1]))
        if not fence and line.startswith(prefix) and not line.startswith(prefix[0] * (len(prefix) - 1) + "#"):
            if current is not None:
                require(current not in out, "DUPLICATE_SECTION", current[:80])
                out[current] = "".join(lines)
            current, lines = line[len(prefix):].strip(), []
        elif current is not None:
            lines.append(line)
    require(fence is None, "UNCLOSED_FENCE")
    if current is not None:
        require(current not in out, "DUPLICATE_SECTION")
        out[current] = "".join(lines)
    return out


def fenced(data, tag):
    pattern = rb"(?m)^(`{3,}|~{3,})" + re.escape(tag.encode()) + rb"\n"
    found = list(re.finditer(pattern, data))
    require(len(found) == 1, "PAYLOAD_FENCE_COUNT", tag)
    f = found[0]
    end = re.search(rb"(?m)^" + re.escape(f[1]) + rb"\r?$", data[f.end():])
    require(end is not None, "UNCLOSED_PAYLOAD")
    return data[f.end():f.end() + end.start()]


def metadata(data, tag):
    try:
        m = json.loads(fenced(data, tag), object_pairs_hook=unique_pairs)
    except (ValueError, UnicodeError) as e:
        raise OAPError("INVALID_METADATA") from e
    require(isinstance(m, dict), "INVALID_METADATA")
    return m


def meaningful(v):
    return isinstance(v, str) and bool(v.strip()) and not re.search(r"\b(?:VERIFY|TBD|TODO|UNRESOLVED)\b|<[^>]+>", v)


def validate_id(value):
    require(isinstance(value, str) and bool(ID_RE.fullmatch(value)), "INVALID_ID")
    return value


def suffix_next(s):
    require(bool(re.fullmatch("[a-z]{1,2}", s)), "INVALID_SUFFIX")
    seq = [chr(c) for c in range(97, 123)]
    seq += [a + b for a in seq[:] for b in seq[:]]
    n = seq.index(s) + 1
    require(n < len(seq), "SUFFIX_EXHAUSTED")
    return seq[n]


def matching(repo, kind, ident):
    paths = list((Path(repo) / "oap" / kind).glob(ident + "-*.md"))
    require(len(paths) <= 1, "AMBIGUOUS_ID")
    return paths[0] if paths else None


def active_id(repo):
    p = Path(repo) / "oap/active"
    safe_path(p, missing=True)
    if not p.exists():
        return None
    data = read(p, 32)
    require(bool(re.fullmatch(rb"[0-9]{3}-[a-z]{1,2}\n", data)), "INVALID_ACTIVE")
    return data[:-1].decode("ascii")


def fields(block, bold=False):
    pat = r"(?m)^- \*\*([^*\n]+):\*\* (.*)$" if bold else r"(?m)^- ([^:\n]+): ?(.*)$"
    return unique_pairs(re.findall(pat, block))


def critical_payload(data, ident, action="APPEND", objective=None, pr=None):
    text = data.decode("utf-8")
    require(data.endswith(b"\n"), "PAYLOAD_FINAL_LF")
    require(not re.search(r'(?m)^#{1,6} HUMAN ADJUDICATION\b', text) and "HUMAN_ACCEPTED" not in text, "AGENT_HUMAN_DISPOSITION")
    top = section_map(text)
    require(len(top) == 1, "CRITICAL_PAYLOAD_STRUCTURE")
    title, body = next(iter(top.items()))
    if action == "UPDATE":
        require(title.startswith("MITIGATION UPDATE — " + ident + " — "), "MITIGATION_ID")
        f = fields(body)
        for k in ("Evidence", "Mitigation", "Remaining gate", "Objective"):
            require(meaningful(f.get(k)), "MITIGATION_FIELD", k)
        require(f.get("Status") in ("MITIGATED", "SUPERSEDED_PENDING"), "MITIGATION_STATUS")
        return
    require(title.startswith(ident + " — ") and len(title) > len(ident) + 4, "CRITICAL_ID")
    f = fields(body, bold=True)
    for key in CRIT_FIELDS:
        require(meaningful(f.get(key)), "CRITICAL_FIELD", key)
    require(f["Status"] == "OPEN — HUMAN ADJUDICATION REQUIRED", "CRITICAL_STATUS")
    require(f["Category"] in {"security", "authorization", "data integrity", "privacy", "operations", "architecture", "dependency", "other"}, "CRITICAL_CATEGORY")
    require(f["Severity"] in {"low", "medium", "high", "critical"}, "CRITICAL_SEVERITY")
    require(f["Decision confidence"] in {"low", "medium", "high"}, "CRITICAL_CONFIDENCE")
    intro = re.fullmatch(r"PR #([1-9][0-9]*) / OAP objective ([0-9]{3}-[a-z]{1,2})", f["Introduced by"])
    require(intro is not None, "CRITICAL_PR_IDENTITY")
    if objective is not None:
        require(intro[2] == objective and int(intro[1]) == pr, "CRITICAL_PR_IDENTITY")
    sections = section_map(body, "### ")
    require(set(sections) == set(CRIT_SECTIONS), "CRITICAL_SECTIONS")
    for key in CRIT_SECTIONS:
        require(meaningful(sections[key].strip()), "CRITICAL_SECTION_EMPTY", key)
    require(sections["Strategic attestation"].strip() == "ALL FIVE CRITICAL-ENTRY CONDITIONS SATISFIED", "CRITICAL_ATTESTATION")
    require(sections["Human disposition"].strip() == "PENDING — append separately; do not edit this entry.", "AGENT_HUMAN_DISPOSITION")
    require(sections["Resolution"].strip() == "PENDING — cleared only by the latest appended human ACCEPTED disposition.", "AGENT_HUMAN_DISPOSITION")


def critical_state(data, *, verified_humans=()):
    top = section_map(data.decode("utf-8"))
    entries, humans, duplicates, updates = {}, {}, [], []
    for title, body in top.items():
        match = re.match(r"^(CRIT-[0-9]{4}) — ", title)
        if match:
            ident = match[1]
            if ident in entries:
                duplicates.append(ident)
            require(ident not in entries, "DUPLICATE_CRITICAL_ID")
            # Preserve canonical schema validation even after legitimate growth.
            critical_payload(("## " + title + "\n" + body).encode(), ident)
            entries[ident] = fields(body, bold=True)["Required human gate"]
        elif title.startswith("HUMAN ADJUDICATION"):
            m = re.fullmatch(r"HUMAN ADJUDICATION — (CRIT-[0-9]{4}) — ([0-9]{4}-[0-9]{2}-[0-9]{2})", title)
            require(m is not None and m[1] in entries, "HUMAN_RECORD_ID")
            try:
                dt.date.fromisoformat(m[2])
            except ValueError as e:
                raise OAPError("HUMAN_RECORD_DATE") from e
            f = fields(body)
            require(f.get("Decision") in DISPOSITIONS, "HUMAN_DISPOSITION_VALUE")
            require(meaningful(f.get("Authority")), "HUMAN_AUTHORITY_MISSING")
            require("Conditions or required follow-up" in f and "Evidence/reference" in f, "HUMAN_RECORD_FIELDS")
            record_hash = digest(("## " + title + "\n" + body).encode())
            humans[m[1]] = {"decision": f["Decision"], "provenance_verified": record_hash in verified_humans}
        elif title.startswith("MITIGATION UPDATE"):
            m = re.match(r"MITIGATION UPDATE — (CRIT-[0-9]{4}) — ", title)
            require(m and m[1] in entries, "MITIGATION_ID")
            critical_payload(("## " + title + "\n" + body).encode(), m[1], "UPDATE")
            updates.append(m[1])
    accepted = [i for i, h in humans.items() if h["decision"] == "ACCEPTED" and h["provenance_verified"]]
    return {"ids": list(entries), "duplicates": duplicates, "latest_human": humans,
            "accepted": accepted, "open": [i for i in entries if i not in accepted],
            "gates": entries, "mitigation_updates": updates,
            "provenance_note": "Markdown names do not authenticate humans; only externally verified records can clear a gate."}


def gate(state, applicable, *, external=False, human_authorized=False):
    require(all(i in state["ids"] for i in applicable), "UNKNOWN_CRITICAL_GATE")
    require(not set(applicable).intersection(state["open"]), "OPEN_HUMAN_GATE")
    require(not external or human_authorized, "SEPARATE_HUMAN_AUTHORITY_REQUIRED")


def governance(repo, mode="bootstrap", accepted_ref=None, allowed_changes=(), strategy=None):
    repo = safe_path(repo, kind="dir")
    m = jsread(repo / "oap/governance/MANIFEST.json")
    require(m.get("schema_version") == 1 and m.get("coding_read_set") == READ_SET, "GOVERNANCE_READ_SET")
    source_lock = jsread(repo / "oap/bootstrap-sources.lock.json")
    for item in source_lock["sources"]:
        b = read(repo / item["installed"])
        require(len(b) == item["bytes"] and digest(b) == item["sha256"], "IMMUTABLE_SOURCE_DRIFT", item["source"])
    for rel, expected in m["identities"].items():
        require(digest(read(repo / rel)) == expected["sha256"], "GOVERNANCE_DRIFT", rel)
        require(len(read(repo / rel)) == expected["bytes"], "GOVERNANCE_SIZE", rel)
    require(set(GOV_SOURCE + READ_SET).issubset(m["identities"]), "GOVERNANCE_IDENTITY_COVERAGE")
    require(m.get("tokenizer") == "UNMEASURED" or meaningful(m.get("tokenizer")), "TOKENIZER_PROVENANCE")
    budgets = {READ_SET[0]: 2048, READ_SET[1]: 12000, READ_SET[2]: 20000, READ_SET[3]: 10000}
    for rel, bound in budgets.items():
        require(len(read(repo / rel)) <= bound, "CONTEXT_BUDGET", rel)
    total = sum(len(read(repo / p)) for p in READ_SET)
    require(total <= 50000 and total == m["coding_bytes"], "CONTEXT_BUDGET_TOTAL")
    compact = b"\n".join(read(repo / p) for p in READ_SET).decode()
    for i in range(1, 15):
        require(f"LR-{i:03}" in compact and f"LR-{i:03}" in m["coverage"], "MISSING_LR_COVERAGE")
    for clause, source in m["coverage"].items():
        require(source["file"] in m["identities"], "COVERAGE_REFERENCE")
        require(clause in read(repo / source["file"]).decode(), "MISSING_COMPACT_CLAUSE", clause)
        require(source.get("source") and source.get("comparison"), "COVERAGE_MEANING_MISSING")
    distillation = read(repo / 'oap/governance/DISTILLATION-MAP.md').decode()
    for source in GOV_SOURCE:
        require(m['identities'][source]['sha256'] in distillation, 'DISTILLATION_SOURCE_STALE', source)
    require(m['identities']['ARCHITECTURE.md']['sha256'] in read(repo/'ARCHITECTURE-for-agents.md').decode(), 'COMPACT_SOURCE_STALE')
    live = read(repo / "CRITICAL.md")
    seed = read(repo / "docs/bootstrap/CRITICAL.md")
    require(live.startswith(seed), "CRITICAL_SEED_PREFIX")
    if mode == "bootstrap":
        for p in ("PLAN.md", "ARCHITECTURE.md", "CRITICAL.md"):
            require(read(repo / p) == read(repo / "docs/bootstrap" / p), "BOOTSTRAP_SOURCE_DRIFT", p)
    else:
        require(accepted_ref is not None, "TRUSTED_REF_REQUIRED")
        accepted = json.loads(git_blob(repo, accepted_ref, "oap/governance/MANIFEST.json"))
        require(live.startswith(git_blob(repo, accepted_ref, "CRITICAL.md")), "CRITICAL_HISTORY_REWRITE")
        require(read(repo / "PLAN.md") == git_blob(repo, accepted_ref, "PLAN.md"), "PROTECTED_PLAN_CHANGE")
        changes = []
        for p in set(accepted["identities"]) | set(m["identities"]):
            if read(repo / p) != git_blob(repo, accepted_ref, p):
                changes.append(p)
        if read(repo/'oap/governance/MANIFEST.json') != git_blob(repo, accepted_ref, 'oap/governance/MANIFEST.json'):
            changes.append('oap/governance/MANIFEST.json')
        require(mode == "candidate-review" or not changes, "UNACCEPTED_GOVERNANCE")
        require(set(changes).issubset(allowed_changes), "UNORDERED_GOVERNANCE_CHANGE")
        # Accepted source integrity is checked against Git, not candidate expected values.
        require(read(repo / "oap/bootstrap-sources.lock.json") == git_blob(repo, accepted_ref, "oap/bootstrap-sources.lock.json"), "SOURCE_LOCK_REWRITE")
    if strategy is not None:
        st = strategic_path(strategy, repo=repo, kind="dir")
        for p in ("AGENTS.md", "OAP-COMMUNICATION-strategic.md", "strategic_model_init_material.md"):
            rel = "oap/strategic-instructions/" + p
            expected = git_blob(repo, accepted_ref, rel) if mode == "candidate-review" else read(repo / rel)
            require(read(st / p) == expected, "STRATEGIC_COPY_DRIFT", p)
        for p in ("PLAN.md", "ARCHITECTURE.md", "CRITICAL.md"):
            require(not (st / p).exists(), "PRIVATE_CANONICAL_MIRROR")
    critical_state(live)
    return {"structure": "valid", "coding_bytes": total, "tokens": "UNMEASURED",
            "mode": mode, "semantic_proof": False, "human_authorization_proof": False}


def validate_order(data, repo, ident=None, filename=None, *, source_ref=None):
    m = metadata(data, "oap-metadata")
    validate_id(m.get("id"))
    if ident:
        require(m["id"] == ident, "ORDER_ID_MISMATCH")
    if filename:
        require(re.fullmatch(re.escape(m["id"]) + r"-[a-z0-9]+(?:-[a-z0-9]+)*\.md", filename), "ORDER_FILENAME")
    require(m.get("status") == "FINAL", "ORDER_NOT_FINAL")
    for k in ("title", "repository", "default_branch", "branch", "phase", "local_work", "prior_review"):
        require(meaningful(m.get(k)), "ORDER_UNRESOLVED_FIELD", k)
    require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", m["repository"]), "REPOSITORY_ID")
    require(m.get("objective") == m["id"][:3], "OBJECTIVE_MISMATCH")
    require(SHA_RE.fullmatch(str(m.get("base_sha", ""))), "ORDER_BASE_SHA")
    is_a = m["id"].endswith("-a")
    require(m.get("pr_mode") == ("CREATE_NEW_PR" if is_a else "AMEND_EXISTING_PR"), "PR_MODE")
    require(m.get("pr") is None if is_a else type(m.get("pr")) is int and m["pr"] > 0, "PR_IDENTITY")
    require(m["branch"] != m["default_branch"] and not m["branch"].startswith("-"), "BRANCH_BOUNDARY")
    require(isinstance(m.get("provenance"), list) and m["provenance"], "MISSING_PROVENANCE")
    for p in m["provenance"]:
        require(p.get("kind") in "HAEIC" and len(p["kind"]) == 1 and meaningful(p.get("reference")), "INVALID_PROVENANCE")
    require(m.get("decision_class") in ("D0", "D1", "D2"), "DECISION_CLASS")
    if m["decision_class"] == "D2":
        require(m.get("safe_preparation") is True and m.get("real_boundary_blocked") is True, "D2_BOUNDARY_BLOCKED")
    require(isinstance(m.get("dependencies"), list) and all(re.fullmatch(r"[0-9]{3}", str(x)) for x in m["dependencies"]), "DEPENDENCIES")
    require(isinstance(m.get("lr"), list) and m["lr"] and set(m["lr"]).issubset({f"LR-{i:03}" for i in range(1, 15)}), "ORDER_LR")
    require(isinstance(m.get("relevant_gates"), list), "RELEVANT_GATES")
    require(isinstance(m.get("required_checks"), list) and m["required_checks"] and all(meaningful(c) for c in m["required_checks"]), "REQUIRED_CHECKS")
    # An immutable historical order names the governance at its original base.
    # Candidate implementation may update current law in that ordered round.
    current = json.loads(git_blob(repo, source_ref or m.get('governance_ref', m['base_sha']), 'oap/governance/MANIFEST.json'))
    require(m.get("governance") == {p: x["sha256"] for p, x in current["identities"].items()}, "ORDER_GOVERNANCE_IDENTITY")
    sections = section_map(data.decode())
    for k in ORDER_SECTIONS:
        require(k in sections, "ORDER_SECTION", k)
        require(k == "Deferred human adjudication" or sections[k].strip(), "ORDER_SECTION", k)
    require(meaningful(sections['Current verified state'].strip()), "ORDER_CURRENT_STATE_UNRESOLVED")
    # Metadata and control sections must be resolved; arbitrary quoted fixture text is data.
    dha = re.findall(r"(?m)^- Decision: (.+)$", sections["Deferred human adjudication"])
    require(len(dha) == 1, "DHA_DECLARATION")
    require(dha[0] == "NONE" or re.fullmatch(r"APPEND CRIT-[0-9]{4}", dha[0]), "DHA_DECLARATION")
    m["dha"] = dha[0]
    update = re.findall(r"(?m)^- Mitigation update: (.+)$", sections["Deferred human adjudication"])
    require(len(update) <= 1, "MITIGATION_DECLARATION")
    if update:
        require(dha[0] == "NONE" and re.fullmatch(r"UPDATE CRIT-[0-9]{4}", update[0]), "MITIGATION_DECLARATION")
    action = dha[0] if dha[0] != "NONE" else (update[0] if update else None)
    require(m["decision_class"] != "D1" or action is not None or m["relevant_gates"], "UNREGISTERED_D1")
    if action:
        op, crit = action.split()
        payload = fenced(data, "critical-entry" if op == "APPEND" else "critical-update")
        require(m.get("critical_payload_bytes") == len(payload) and m.get("critical_payload_sha256") == digest(payload), "CRITICAL_PAYLOAD_HASH")
        require(type(m.get("critical_prior_bytes")) is int and m["critical_prior_bytes"] >= 0 and HASH_RE.fullmatch(str(m.get("critical_prior_sha256", ""))), "CRITICAL_PRIOR_REFERENCE")
        critical_payload(payload, crit, op, m["id"] if op == "APPEND" else None, m["pr"])
        m["critical_action"], m["critical_id"], m["payload"] = op, crit, payload
    else:
        require(b"critical-entry\n" not in data and b"critical-update\n" not in data, "UNAUTHORIZED_CRITICAL_PAYLOAD")
    return m


class GitHub:
    """Read-only gh boundary. Tests inject an explicit fake executable."""
    def __init__(self, repository, executable="gh"):
        require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository), "REPOSITORY_ID")
        self.repository, self.executable = repository, executable

    def api(self, suffix):
        p = subprocess.run([self.executable, "api", f"repos/{self.repository}/{suffix}"], capture_output=True, timeout=30)
        require(p.returncode == 0, "REMOTE_UNVERIFIED")
        try:
            return json.loads(p.stdout)
        except ValueError as e:
            raise OAPError("REMOTE_INVALID_JSON") from e

    def pr(self, number):
        value = self.api(f"pulls/{number}")
        require(value.get("number") == number and value.get("base", {}).get("repo", {}).get("full_name") == self.repository, "REMOTE_PR_IDENTITY")
        return value

    def branch_prs(self, branch):
        from urllib.parse import quote
        return self.api("pulls?state=all&head=" + quote(self.repository.split("/")[0] + ":" + branch, safe=""))


def transition(repo, new, remote):
    old_id = active_id(repo)
    if old_id == new["id"]:
        require(matching(repo, "reports", old_id) is None, "COMPLETED_REPLAY")
        return
    if old_id is None:
        require(new["id"] == "000-a", "INITIAL_ORDER_ID")
        require(not list((Path(repo) / "oap/orders").glob("*.md")) or matching(repo, "orders", new["id"]) is not None, "ORPHAN_HISTORY")
        require(remote.api('branches/'+new['default_branch'])['commit']['sha'] == new['base_sha'], 'STALE_DEFAULT_HEAD')
        return
    old_path = matching(repo, "orders", old_id)
    require(old_path is not None, "ACTIVE_ORDER_MISSING")
    old = validate_order(read(old_path), repo, old_id, old_path.name)
    require(matching(repo, "reports", old_id) is not None, "PRIOR_REPORT_MISSING")
    verify_report(repo, old_id, remote=remote)
    previous_report = metadata(read(matching(repo, "reports", old_id)), "oap-report")
    pr = remote.pr(previous_report["pr"])
    if new["objective"] == old["objective"]:
        require(new["id"].split("-")[1] == suffix_next(old_id.split("-")[1]), "ROUND_SEQUENCE")
        require(new["branch"] == old["branch"] and new["pr"] == previous_report["pr"] and pr["state"] == "open", "SAME_PR_REQUIRED")
    else:
        require(int(new["objective"]) == int(old["objective"]) + 1 and new["id"].endswith("-a"), "OBJECTIVE_SEQUENCE")
        abandoned = new.get("prior_disposition") == "ABANDONED" and meaningful(new.get("abandonment_rationale")) and meaningful(new.get("dependency_reassessment")) and pr["state"] == "closed"
        require(pr.get("merged") is True or abandoned, "PRIOR_NOT_MERGED_OR_DISPOSED")
        default = remote.api("branches/" + new["default_branch"])
        require(default["commit"]["sha"] == new["base_sha"], "STALE_DEFAULT_HEAD")


def publish(repo, source, ident, *, strategy=None, accepted_ref=None, dry_run=False, remote=None, fault=None):
    repo = Path(repo)
    require(os.environ.get("OAP_ROLE") == "strategic", "ROLE_REQUIRED")
    data = read(source)
    m = validate_order(data, repo, ident, Path(source).name)
    governance(repo, "accepted-runtime", accepted_ref, strategy=strategy)
    current = jsread(repo / 'oap/governance/MANIFEST.json')
    require(m['governance'] == {p:x['sha256'] for p,x in current['identities'].items()}, 'STALE_ORDER_GOVERNANCE')
    require(remote is not None and remote.repository == m["repository"], "REMOTE_REQUIRED")
    target = repo / "oap/orders" / Path(source).name
    require(matching(repo, "reports", ident) is None, "COMPLETED_REPLAY")
    if dry_run:
        transition(repo, m, remote)
        if target.exists():
            require(read(target) == data, "IMMUTABLE_CONFLICT")
        return {"result": "valid dry run", "writes": 0}
    with lock(repo / "oap/.publish.lock"):
        transition(repo, m, remote)
        peers = remote.branch_prs(m["branch"])
        require(len(peers) <= 1, "DUPLICATE_PR")
        if m["pr_mode"] == "AMEND_EXISTING_PR":
            require(len(peers) == 1 and peers[0]["number"] == m["pr"], "SAME_PR_REQUIRED")
        elif peers:
            # Only identical recovery of a previously published a may adopt a PR.
            require(target.exists() and read(target) == data, "UNEXPECTED_EXISTING_PR")
        require(matching(repo, "orders", ident) in (None, target), "ORDER_FILENAME_CONFLICT")
        atomic(target, data, immutable=True)
        if fault:
            fault("order-written")
        atomic(repo / "oap/active", (ident + "\n").encode())
    return {"result": "published", "signal_sent": False, "id": ident}


def append_critical(repo, source, ident, *, accepted_ref, dry_run=False, fault=None):
    repo = Path(repo)
    require(os.environ.get("OAP_ROLE") == "coding", "ROLE_REQUIRED")
    aid = active_id(repo)
    require(aid is not None, "INACTIVE")
    opath = matching(repo, "orders", aid)
    require(opath is not None, "ACTIVE_ORDER_MISSING")
    order = validate_order(read(opath), repo, aid, opath.name)
    require(order.get("critical_id") == ident, "APPEND_NOT_AUTHORIZED")
    payload = read(source)
    require(payload == order["payload"], "APPEND_BYTES_MISMATCH")
    require(matching(repo, "reports", aid) is None, "REPORT_ALREADY_EXISTS")
    prior = git_blob(repo, accepted_ref, "CRITICAL.md")
    require(len(prior) == order["critical_prior_bytes"] and digest(prior) == order["critical_prior_sha256"], "UNTRUSTED_CRITICAL_BASE")
    require(prior.startswith(read(repo / "docs/bootstrap/CRITICAL.md")), "CRITICAL_SEED_PREFIX")
    state = critical_state(prior)
    if order["critical_action"] == "APPEND":
        require(ident not in state["ids"], "DUPLICATE_CRITICAL_ID")
    else:
        require(ident in state["ids"], "MITIGATION_ID")
    target = repo / "CRITICAL.md"
    def run():
        current = read(target)
        if current == prior + payload:
            return {"result": "already applied", "id": ident}
        require(current == prior, "CRITICAL_STALE_OR_REWRITTEN")
        critical_state(prior + payload)
        if dry_run:
            return {"result": "valid dry run", "writes": 0}
        if fault:
            fault("before-append")
        atomic(target, prior + payload)
        if fault:
            fault("after-append")
        return {"result": "appended", "id": ident}
    if dry_run:
        return run()
    with lock(repo / "oap/.critical.lock"):
        return run()


def validate_report(data, order, order_data, order_path):
    r = metadata(data, "oap-report")
    require(r.get("id") == order["id"] and r.get("result") in RESULTS, "REPORT_ID_RESULT")
    require(r.get("order_path") == order_path and r.get("order_sha256") == digest(order_data), "REPORT_ORDER_IDENTITY")
    require(r.get("governance") == order["governance"], "REPORT_GOVERNANCE")
    require(r.get("publication_commit") == "SELF", "REPORT_SELF")
    require(SHA_RE.fullmatch(str(r.get("implementation_head", ""))), "REPORT_IMPLEMENTATION_SHA")
    require(r.get("publication_verified") is False, "FUTURE_PUBLICATION_CLAIM")
    require(r.get("pr_mode") == order["pr_mode"] and type(r.get("pr")) is int and r["pr"] > 0, "REPORT_PR")
    require(r.get("pr_url") == f"https://github.com/{order['repository']}/pull/{r['pr']}", "REPORT_PR_URL")
    require(r.get("pr_state") == "open" and r.get("branch") == order["branch"] and r.get("base_sha") == order["base_sha"], "REPORT_BRANCH_BASE")
    require(SHA_RE.fullmatch(str(r.get("starting_remote_sha", ""))), "REPORT_START_SHA")
    require(r.get("no_merge") is True, "REPORT_MERGE_AUTHORITY")
    for k in ("implementation", "documentation", "criteria", "negative_paths", "boundary_fidelity", "setup", "privacy", "limits", "human_gates", "scope"):
        require(meaningful(r.get(k)), "REPORT_FIELD", k)
    require(isinstance(r.get("checks"), list) and r["checks"], "REPORT_CHECKS")
    for c in r["checks"]:
        require(meaningful(c.get("command")) and c.get("result") in CHECKS and SHA_RE.fullmatch(str(c.get("sha", ""))), "REPORT_CHECK")
        require(c.get("publication_head_claim") is not True, "FUTURE_CI_CLAIM")
    require(re.fullmatch(r"NONE|APPENDED CRIT-[0-9]{4}|MITIGATION UPDATED CRIT-[0-9]{4}|CANDIDATE REPORTED", str(r.get("critical_action"))), "REPORT_CRITICAL_ACTION")
    if "critical_action" in order:
        want = ("APPENDED " if order["critical_action"] == "APPEND" else "MITIGATION UPDATED ") + order["critical_id"]
        require(r["critical_action"] == want, "REPORT_CRITICAL_ACTION")
    try:
        observed = dt.datetime.fromisoformat(r["pr_observed_at"])
        written = dt.datetime.fromisoformat(r["report_written_at"])
        require(observed.tzinfo and written.tzinfo and observed <= written, "REPORT_CHRONOLOGY")
    except (KeyError, ValueError, TypeError) as e:
        raise OAPError("REPORT_CHRONOLOGY") from e
    return r


def _revision(repo, revision):
    require(isinstance(revision, str) and (revision == "HEAD" or SHA_RE.fullmatch(revision)),
            "INVALID_REVISION")
    resolved = git(repo, "rev-parse", "--verify", "--end-of-options", revision + "^{commit}").decode().strip()
    require(SHA_RE.fullmatch(resolved), "INVALID_REVISION")
    return resolved


def _index_entries(repo, prefixes):
    raw = git(repo, "ls-files", "--stage", "-z", "--", *prefixes)
    entries = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        header, path = record.split(b"\t", 1)
        mode, object_id, stage = header.split()
        require(mode in (b"100644", b"100755"), "TRANSCRIPT_UNSAFE_TYPE")
        require(stage == b"0", "INDEX_UNMERGED")
        require(re.fullmatch(rb"[0-9a-f]{40}", object_id), "INDEX_ENTRY_INVALID")
        name = path.decode("utf-8")
        require(name not in entries, "AMBIGUOUS_ID")
        entries[name] = git(repo, "cat-file", "blob", object_id.decode())
    return entries


def _transcript_entries(repo, *, index, revision):
    if index:
        entries = _index_entries(repo, ("oap/orders", "oap/reports"))
        active_entries = _index_entries(repo, ("oap/active",))
        return entries, active_entries.get("oap/active")
    records = git(repo, "ls-tree", "-r", "-z", revision, "--",
                  "oap/orders", "oap/reports").split(b"\0")
    entries = {}
    for record in records:
        if not record:
            continue
        header, raw_path = record.split(b"\t", 1)
        mode, object_type, object_id = header.split()
        require(mode in (b"100644", b"100755") and object_type == b"blob", "TRANSCRIPT_UNSAFE_TYPE")
        require(re.fullmatch(rb"[0-9a-f]{40}", object_id), "TRANSCRIPT_OBJECT_INVALID")
        path = raw_path.decode("utf-8")
        entries[path] = git(repo, "cat-file", "blob", object_id.decode())
    active = _revision_entry(repo, revision, "oap/active")
    return entries, active


def _revision_entry(repo, revision, path):
    result = git(repo, "ls-tree", "-z", revision, "--", path, check=False)
    require(result.returncode == 0, "GIT_FAILURE", "ls-tree")
    records = [record for record in result.stdout.split(b"\0") if record]
    require(len(records) <= 1, "AMBIGUOUS_ID")
    if not records:
        return None
    header, raw_path = records[0].split(b"\t", 1)
    mode, object_type, object_id = header.split()
    require(raw_path.decode("utf-8") == path, "TRANSCRIPT_PATH")
    require(mode in (b"100644", b"100755") and object_type == b"blob", "TRANSCRIPT_UNSAFE_TYPE")
    require(re.fullmatch(rb"[0-9a-f]{40}", object_id), "TRANSCRIPT_OBJECT_INVALID")
    return git(repo, "cat-file", "blob", object_id.decode())


def _worktree_active(repo):
    path = Path(repo) / "oap/active"
    safe_path(path, missing=True)
    return read(path, 32) if path.exists() else None


def _parse_transcript_files(entries, kind):
    prefix = "oap/" + kind + "/"
    result = {}
    for path, data in entries.items():
        if not path.startswith(prefix):
            continue
        name = path[len(prefix):]
        if name == ".gitkeep":
            continue
        match = TRANSCRIPT_FILENAME_RE.fullmatch(name)
        require(match is not None, kind.upper() + "_FILENAME")
        ident = validate_id(match["id"])
        require(ident not in result, "AMBIGUOUS_ID")
        result[ident] = (path, data)
    return result


def _transcript_order(ids):
    require(ids, "TRANSCRIPT_NO_ORDERS")
    grouped = {}
    for ident in ids:
        objective, suffix = ident.split("-", 1)
        grouped.setdefault(int(objective), []).append(suffix)
    objectives = sorted(grouped)
    require(objectives == list(range(objectives[0], objectives[-1] + 1)),
            "TRANSCRIPT_OBJECTIVE_GAP")
    ordered = []
    for objective in objectives:
        suffixes = grouped[objective]
        ranks = sorted(SUFFIX_ORDER.index(suffix) for suffix in suffixes)
        require(ranks == list(range(ranks[0], ranks[-1] + 1)), "TRANSCRIPT_SUFFIX_GAP")
        ordered.extend(f"{objective:03}-{SUFFIX_ORDER[rank]}" for rank in ranks)
    return ordered


def _validate_committed_report(repo, revision, report_path, report_data, order_path, order_data,
                               report, implementation_head):
    report_commit = git(repo, "log", "-1", "--format=%H", revision, "--", report_path).decode().strip()
    require(SHA_RE.fullmatch(report_commit), "REPORT_NOT_COMMITTED")
    parents = git(repo, "rev-list", "--parents", "-n", "1", report_commit).decode().split()
    require(len(parents) == 2 and parents[1] == implementation_head, "REPORT_PARENT")
    changed = git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", report_commit)
    changed_paths = changed.rstrip(b"\0").decode().split("\0") if changed else []
    require(changed_paths == [report_path], "REPORT_ONLY_PATH")
    require(git_blob(repo, report_commit, report_path) == report_data, "REPORT_CONTENT_DRIFT")
    require(git_blob(repo, revision, order_path) == order_data, "COMMITTED_ORDER_DRIFT")
    for check in report["checks"]:
        result = git(repo, "merge-base", "--is-ancestor", check["sha"], implementation_head, check=False)
        require(result.returncode == 0, "UNOBSERVED_CHECK_SHA")


def check_transcript(repo, *, index=False, revision=None, expected_id=None):
    """Validate published transcript state from the index or one committed tree.

    The selected tree is the source of transcript truth.  The worktree active
    pointer is compared byte-for-byte so a same-size atomic write cannot hide
    behind Git's status/stat cache.
    """
    repo = safe_path(repo, kind="dir")
    require(bool(index) ^ (revision is not None), "TRANSCRIPT_MODE_REQUIRED")
    if expected_id is not None:
        validate_id(expected_id)
    resolved = _revision(repo, "HEAD" if index else revision)
    entries, selected_active = _transcript_entries(repo, index=index, revision=resolved)
    worktree_active = _worktree_active(repo)
    if index:
        require(worktree_active == selected_active, "ACTIVE_INDEX_MISMATCH")
    else:
        require(worktree_active == selected_active, "ACTIVE_COMMIT_MISMATCH")
    if expected_id is not None:
        require(selected_active == (expected_id + "\n").encode(), "EXPECTED_ACTIVE_MISMATCH")

    orders = _parse_transcript_files(entries, "orders")
    reports = _parse_transcript_files(entries, "reports")
    for ident in reports:
        require(ident in orders, "REPORT_ORDER_MISSING")
    if selected_active is None:
        require(not orders and not reports, "ACTIVE_REQUIRED")
        return {"result": "valid", "mode": "index" if index else "revision",
                "revision": resolved, "active": None, "orders": [], "reports": []}
    require(bool(re.fullmatch(rb"[0-9]{3}-[a-z]{1,2}\n", selected_active)), "INVALID_ACTIVE")
    active = selected_active[:-1].decode("ascii")
    if not orders:
        require(not reports, "ACTIVE_ORDER_MISSING")
        raise OAPError("ACTIVE_ORDER_MISSING")
    ordered = _transcript_order(list(orders))
    latest = ordered[-1]
    require(active in orders, "ACTIVE_ORDER_MISSING")
    require(active == latest, "TRANSCRIPT_LATEST_MISMATCH")

    validated_orders = {}
    for ident in ordered:
        path, data = orders[ident]
        validated_orders[ident] = validate_order(data, repo, ident, Path(path).name,
                                                  source_ref=resolved)
    for ident, (path, data) in reports.items():
        order_path, order_data = orders[ident]
        require(path.rsplit("/", 1)[-1] == order_path.rsplit("/", 1)[-1], "REPORT_FILENAME")
        report = validate_report(data, validated_orders[ident], order_data, order_path)
        if not index:
            _validate_committed_report(repo, resolved, path, data, order_path, order_data,
                                       report, report["implementation_head"])
        else:
            _validate_committed_report(repo, resolved, path, data, order_path, order_data,
                                       report, report["implementation_head"])
    for ident in ordered:
        if ident not in reports:
            require(ident == active, "TRANSCRIPT_NONCURRENT_UNFINISHED")
    return {"result": "valid", "mode": "index" if index else "revision",
            "revision": resolved, "active": active, "latest": latest,
            "orders": ordered, "reports": [ident for ident in ordered if ident in reports]}


def verify_report(repo, ident, *, commit=None, remote=None):
    repo = Path(repo)
    validate_id(ident)
    opath, rpath = matching(repo, "orders", ident), matching(repo, "reports", ident)
    require(opath is not None and rpath is not None, "REPORT_OR_ORDER_MISSING")
    order_data = read(opath)
    order = validate_order(order_data, repo, ident, opath.name)
    require(rpath.name == opath.name, "REPORT_FILENAME")
    data = read(rpath)
    r = validate_report(data, order, order_data, str(opath.relative_to(repo)))
    report_rel = str(rpath.relative_to(repo))
    if commit is None:
        commit = git(repo, "log", "-1", "--format=%H", "--", report_rel).decode().strip()
    require(SHA_RE.fullmatch(commit or ""), "REPORT_NOT_COMMITTED")
    parents = git(repo, "rev-list", "--parents", "-n", "1", commit).decode().split()
    require(len(parents) == 2 and parents[1] == r["implementation_head"], "REPORT_PARENT")
    changed = git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", commit).decode().strip("\0").split("\0")
    require(changed == [report_rel], "REPORT_ONLY_PATH")
    require(git_blob(repo, commit, report_rel) == data, "REPORT_CONTENT_DRIFT")
    require(git_blob(repo, commit, str(opath.relative_to(repo))) == order_data, "COMMITTED_ORDER_DRIFT")
    for c in r["checks"]:
        require(git(repo, "merge-base", "--is-ancestor", c["sha"], r["implementation_head"], check=False).returncode == 0, "UNOBSERVED_CHECK_SHA")
    if remote is not None:
        require(remote.repository == order["repository"], "REMOTE_PR_IDENTITY")
        pr = remote.pr(r["pr"])
        require(pr["head"]["sha"] == commit and pr["head"]["ref"] == r["branch"], "REMOTE_HEAD_MISMATCH")
        require(dt.datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00")) <= dt.datetime.fromisoformat(r["pr_observed_at"]), "PR_CREATED_AFTER_REPORT")
        rc = remote.api("commits/" + commit)
        require([p["sha"] for p in rc["parents"]] == [r["implementation_head"]], "REMOTE_REPORT_PARENT")
        require([f["filename"] for f in rc["files"]] == [report_rel], "REMOTE_REPORT_ONLY_PATH")
        blob = remote.api("contents/" + report_rel + "?ref=" + commit)
        require(blob.get("encoding") == "base64" and base64.b64decode(blob["content"]) == data, "REMOTE_REPORT_CONTENT")
    return {"result": "verified", "scope": "remote" if remote else "local only", "commit": commit, "id": ident}


def protocol_state(repo, *, strategy=None, remote=None):
    repo = Path(repo)
    critical = critical_state(read(repo / "CRITICAL.md"))
    ident = active_id(repo)
    if ident is None:
        return {"state": "INACTIVE", "critical": critical}
    path = matching(repo, "orders", ident)
    require(path is not None, "ACTIVE_ORDER_MISSING")
    order = validate_order(read(path), repo, ident, path.name)
    state = "READY"
    if matching(repo, "reports", ident):
        state = "PUBLICATION_RECONCILIATION_REQUIRED"
        if remote:
            verify_report(repo, ident, remote=remote)
            state = "REVIEW_READY"
    elif strategy and (Path(strategy) / "workorders/consumed.json").exists():
        if jsread(Path(strategy) / "workorders/consumed.json").get("id") == ident:
            state = "RECOVERY_REQUIRED"
    return {"state": state, "id": ident, "branch": order["branch"], "pr": order["pr"], "critical": critical}


def fifo(path, action, *, timeout=None):
    p = safe_path(path, kind="fifo", private=True)
    start = time.monotonic()
    def remaining():
        if timeout is None:
            return 0.2
        left = timeout - (time.monotonic() - start)
        require(left > 0, "FIFO_TIMEOUT")
        return min(left, 0.2)
    if action == "send":
        while True:
            try:
                fd = os.open(p, os.O_WRONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
                break
            except OSError as e:
                import errno
                if e.errno != errno.ENXIO:
                    raise
                select.select([], [], [], remaining())
        try:
            view = memoryview(b"OK")
            while view:
                _, writable, _ = select.select([], [fd], [], remaining())
                if writable:
                    view = view[os.write(fd, view):]
        finally:
            os.close(fd)
        return {"frame": "OK", "bytes": 2}
    require(action == "wait", "FIFO_ACTION")
    fd = os.open(p, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    data, connected = bytearray(), False
    try:
        while True:
            ready, _, _ = select.select([fd], [], [], remaining())
            if not ready:
                continue
            chunk = os.read(fd, 4096)
            if chunk:
                connected = True
                data.extend(chunk)
                require(len(data) <= 2 and b"OK".startswith(data), "FIFO_INVALID_FRAME")
            elif connected:
                require(bytes(data) == b"OK", "FIFO_INVALID_FRAME")
                return {"frame": "OK", "bytes": 2}
            else:
                # A writer closed without bytes: EOF is an invalid empty frame.
                raise OAPError("FIFO_EMPTY_FRAME")
    finally:
        os.close(fd)


def strategic_gate(remote, pr_number, reviewed_sha, required_checks, *, merge_effect):
    require(os.environ.get("OAP_ROLE") == "strategic", "ROLE_REQUIRED")
    require(merge_effect == "development-only", "MERGE_D2_EFFECT")
    require(required_checks, "REQUIRED_CHECKS_MISSING")
    pr = remote.pr(pr_number)
    require(pr["state"] == "open" and not pr.get("draft", False), "PR_NOT_REVIEWABLE")
    require(pr["head"]["sha"] == reviewed_sha, "REVIEW_HEAD_CHANGED")
    runs = remote.api(f"commits/{reviewed_sha}/check-runs?per_page=100")
    require(runs.get("total_count", 0) <= 100, "CHECK_PAGINATION_REQUIRED")
    by_name = {}
    for c in runs["check_runs"]:
        by_name.setdefault(c["name"], []).append(c)
    for name in required_checks:
        require(name in by_name, "REQUIRED_CHECK_MISSING")
        require(all(c.get("head_sha") == reviewed_sha and c.get("status") == "completed" and c.get("conclusion") == "success" for c in by_name[name]), "REQUIRED_CHECK_NOT_GREEN")
    return {"result": "structural development gate valid", "reviewed_sha": reviewed_sha,
            "merge_performed": False, "semantic_review_required": True, "deployment_authorized": False}


def verify_merge(remote, pr_number, default_branch):
    pr = remote.pr(pr_number)
    require(pr.get("merged") is True and pr.get("merge_commit_sha"), "MERGE_UNVERIFIED")
    head = remote.api("branches/" + default_branch)["commit"]["sha"]
    compare = remote.api("compare/" + pr["merge_commit_sha"] + "..." + head)
    require(compare.get("status") in ("identical", "ahead"), "MERGE_NOT_ON_DEFAULT")
    return {"merged": True, "default_head": head, "deployment_authorized": False}


def check_ica(repo, source, current_main):
    repo = Path(repo)
    m = metadata(read(source), "oap-ica")
    require(m.get("status") == "FINAL" and m.get("milestone") in ("DEMONSTRATOR", "MVP", "SERVICE"), "ICA_STATUS_SCOPE")
    require(SHA_RE.fullmatch(current_main or "") and m.get("main_sha") == current_main, "ICA_STALE_MAIN")
    require(m.get("architecture_sha256") == digest(git_blob(repo, current_main, "ARCHITECTURE.md")), "ICA_SOURCE_REVISION")
    require(m.get("plan_sha256") == digest(git_blob(repo, current_main, "PLAN.md")), "ICA_PLAN_REVISION")
    require(meaningful(m.get("auditor")) and meaningful(m.get("context_provenance")), "ICA_INDEPENDENCE_PROVENANCE")
    require(m.get("input_order") == ["human_scope", "full_architecture", "current_main", "strategic_claims"], "ICA_INPUT_ORDER")
    expected_bytes = git_blob(repo, current_main, 'oap/audit/requirements.json')
    require(read(repo/'oap/audit/requirements.json') == expected_bytes, 'ICA_MATRIX_SOURCE_DRIFT')
    expected = json.loads(expected_bytes)
    needed = {r["id"] for r in expected if m["milestone"] in r["milestones"]}
    require(isinstance(m.get("matrix"), list), "ICA_MATRIX")
    rows = m["matrix"]
    require(len({r.get("id") for r in rows}) == len(rows), "ICA_DUPLICATE_REQUIREMENT")
    require({r.get("id") for r in rows} == needed, "ICA_REQUIREMENT_COVERAGE")
    for row in rows:
        require(row.get("class") in {"IMPLEMENTED", "PARTIAL", "ABSENT", "UNPROVEN"}, "ICA_CLASS")
        if row["class"] == "IMPLEMENTED":
            require(row.get("tested_sha") == current_main and all(meaningful(row.get(k)) for k in ("runtime_path", "evidence", "negative_paths")), "ICA_EVIDENCE_MISSING")
        else:
            require(meaningful(row.get("gap")), "ICA_GAP_MISSING")
    require(m.get("deployment_authorized") is False and m.get("human_milestone_accepted") is False, "ICA_AUTHORITY")
    return {"schema": "valid", "gaps": [r["id"] for r in rows if r["class"] != "IMPLEMENTED"],
            "independence": "declared, requires separate verification", "semantic_acceptance": "NOT CERTIFIED"}
