"""Setup shells, gated launch, external FIFO waits and owned tmux sessions."""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import time
import tomllib
from oap_core import (require, OAPError, safe_path, read, jsread, atomic, json_bytes,
                      lock, digest, git, governance, protocol_state, matching, active_id,
                      fifo, verify_report, GitHub, READ_SET, strategic_path, fifo_home,
                      coding_dispatch_mode, foreground_pane, workspace_layout)
from oap_install import runtime_config


def role_context(config, role, *, operational=False, check_selected=True, dispatch=False):
    require(role in ("coding", "strategic"), "UNKNOWN_ROLE")
    require(not check_selected or os.environ.get("OAP_ROLE", role) == role, "CONFLICTING_ROLE")
    repo = safe_path(config["OAP_REPO_ROOT"], kind="dir")
    if operational and role == "coding" and coding_dispatch_mode(repo) == "foreground":
        # Owner-selected foreground runtime: the legacy entry point may not
        # spawn a coding model (including codex exec), auto-restart one, or
        # create a background pane. It fails closed instead of falling back.
        raise OAPError("FOREGROUND_DISPATCH_ONLY")
    strategy = strategic_path(config["OAP_STRATEGIC_HOME"], repo=repo, kind="dir")
    pipes = fifo_home(repo, strategy)
    require(config.get('OAP_FIFO_HOME') == str(pipes), 'FIFO_HOME_LAYOUT_CONFLICT')
    require(repo != strategy and repo not in strategy.parents and strategy not in repo.parents, "NESTED_ROOTS")
    coding_home = strategic_path(config["CODING_CODEX_HOME"], repo=repo, kind="dir")
    strategy_home = strategic_path(config["STRATEGIC_CODEX_HOME"], repo=repo, kind="dir")
    require(coding_home != strategy_home and coding_home not in strategy_home.parents and strategy_home not in coding_home.parents, "ROLE_HOME_COLLISION")
    require(strategy in coding_home.parents and strategy in strategy_home.parents, "ROLE_HOME_OUTSIDE_PRIVATE")
    current_home = os.environ.get("CODEX_HOME")
    if current_home and not dispatch:
        # The foreground dispatcher is cross-role and launches no model; its
        # own session home is not a generator-home reuse.
        require(Path(current_home).resolve() not in (coding_home, strategy_home) or os.environ.get("OAP_ROLE") == role, "GENERATOR_HOME_REUSE")
    home = coding_home if role == "coding" else strategy_home
    cwd = repo if role == "coding" else strategy
    strategic_path(home / "config.toml", repo=repo, kind="file")
    tomllib.loads(read(home / "config.toml").decode())
    prompt_path = repo / "oap/prompts" / ("coding-round.md" if role == "coding" else "strategic-start.md")
    prompt = read(prompt_path).decode()
    require(f"OAP_ROLE={role}" in prompt, "PROMPT_ROLE_MISMATCH")
    if role == "coding":
        require("control.fifo" not in prompt and "wait --fifo" not in prompt, "DOUBLE_FIFO_READ")
        reads = READ_SET[:4] + ["oap/active", "exact active order", "ordered relevant local contracts"]
    else:
        reads = ["AGENTS.md", "OAP-COMMUNICATION-strategic.md", "strategic_model_init_material.md",
                 "canonical PLAN.md", "canonical ARCHITECTURE.md", "INITIAL-ROADMAP.md", "current CRITICAL.md at startup", "current OAP/GitHub state", "relevant full doctrine"]
    env = os.environ.copy()
    # Do not inherit another role's provider/session selectors or task state.
    for key in list(env):
        if key.startswith(("CODEX_", "OAP_", "CODING_CODEX_", "STRATEGIC_CODEX_", "REPAIR_")):
            env.pop(key, None)
    env.update(config)
    env.update(CODEX_HOME=str(home), OAP_ROLE=role, OAP_INTENDED_READ_SET=json.dumps(reads))
    argv = [config["CODEX_BIN"]]
    if role == "coding":
        argv += ["exec", "--ephemeral"]
    if operational:
        require(config["OAP_ACK_DANGER_FULL_ACCESS"] == "YES" and config["OAP_ACK_START_LOOP"] == "YES", "ACTIVATION_ACK_REQUIRED")
        require(config["OAP_ROLE_AUTH_READY"] == "YES", "ROLE_AUTH_UNQUALIFIED")
        model, profile = config[role.upper() + "_CODEX_MODEL"], config[role.upper() + "_CODEX_PROFILE"]
        require(bool(model) != bool(profile), "EXPLICIT_MODEL_OR_PROFILE_REQUIRED")
        if profile:
            require(re.fullmatch(r"[A-Za-z0-9_-]+", profile), "PROFILE_NAME")
            strategic_path(home / (profile + ".config.toml"), repo=repo, kind="file")
            tomllib.loads(read(home / (profile + ".config.toml")).decode())
        require(config["OAP_GITHUB_REPOSITORY"] and config["OAP_ACCEPTED_REF"], "REMOTE_BASELINE_REQUIRED")
        require(config["OAP_MERGE_EFFECT"] == "development-only", "MERGE_D2_EFFECT")
        version = subprocess.run([config["CODEX_BIN"], "--version"], capture_output=True, text=True, timeout=10)
        require(version.returncode == 0 and bool(version.stdout.strip()), "CLI_UNAVAILABLE")
        expected_version = config["OAP_CLI_QUALIFIED_VERSION"]
        require(expected_version == "ANY" or version.stdout.strip() == expected_version, "CLI_VERSION_UNQUALIFIED")
        origin = git(repo, "remote", "get-url", "origin").decode().strip()
        expected = config["OAP_GITHUB_REPOSITORY"]
        require(origin in (f"https://github.com/{expected}.git", f"https://github.com/{expected}", f"git@github.com:{expected}.git"), "REMOTE_ORIGIN_MISMATCH")
        governance(repo, "accepted-runtime", config["OAP_ACCEPTED_REF"], strategy=strategy)
        argv += ["--profile", profile] if profile else ["--model", model]
        argv += ["--dangerously-bypass-approvals-and-sandbox", "--cd", str(cwd), prompt]
    return {"role": role, "cwd": str(cwd), "home": str(home), "argv": argv,
            "env": env, "read_set": reads, "prompt": prompt}


def setup_shell(config, role, *, print_only=False):
    c = role_context(config, role)
    if print_only:
        return {k: c[k] for k in ("role", "cwd", "home")} | {"argv": ["bash", "--noprofile", "--norc", "-i"], "model_started": False}
    os.chdir(c["cwd"])
    # A shell with no automatic CLI command necessarily survives a manually exited CLI.
    os.execvpe("bash", ["bash", "--noprofile", "--norc", "-i"], c["env"])


def run_model(context):
    return subprocess.run(context['argv'], cwd=context['cwd'], env=context['env'])


def launch(config, role, *, print_only=False, resume_id=None, once=False, timeout=None, gh_bin="gh"):
    c = role_context(config, role, operational=True)
    if print_only:
        return {k: c[k] for k in ("role", "cwd", "home", "argv", "read_set")}
    repo, strategy = Path(config["OAP_REPO_ROOT"]), Path(config["OAP_STRATEGIC_HOME"])
    remote = GitHub(config["OAP_GITHUB_REPOSITORY"], gh_bin)
    with lock(strategy / ("." + role + ".lock")):
        if role == "strategic":
            result = run_model(c)
            require(result.returncode == 0, "STRATEGIC_EXIT_RECOVERY")
            return {"result": "exited", "restarted": False}
        while True:
            # OS waits, no model call. The model sees a ready order after this one read.
            fifo(Path(config['OAP_FIFO_HOME']) / "control.fifo", "wait", timeout=timeout)
            state = protocol_state(repo, strategy=strategy, remote=remote)
            if state["state"] in ("INACTIVE", "REVIEW_READY"):
                if once:
                    return {"result": "suppressed", "state": state["state"], "model_calls": 0}
                continue
            require(state["state"] != "PUBLICATION_RECONCILIATION_REQUIRED", "REPORT_RECOVERY_REQUIRED")
            if state["state"] == "RECOVERY_REQUIRED":
                require(resume_id == state["id"], "EXPLICIT_SAME_ORDER_RECOVERY_REQUIRED")
            peers = remote.branch_prs(state["branch"])
            require(len(peers) <= 1, "DUPLICATE_PR")
            if state["pr"] is not None:
                require(len(peers) == 1 and peers[0]["number"] == state["pr"], "RECOVERY_PR_MISMATCH")
            atomic(strategy / "workorders/consumed.json", json_bytes({"id": state["id"], "branch": state["branch"], "pr": peers[0]["number"] if peers else None,
                    "phase": "consumed", "recovery": resume_id == state["id"]}), mode=0o600)
            result = run_model(c)
            if result.returncode:
                atomic(strategy / "workorders/incident.json", json_bytes({"id": state["id"], "classification": "CODING_EXIT_RECOVERY", "exit_code": result.returncode}), mode=0o600)
                raise OAPError("CODING_EXIT_RECOVERY")
            verified = verify_report(repo, state["id"], remote=remote)
            atomic(strategy / "workorders/publication.json", json_bytes(verified), mode=0o600)
            if once:
                return {"result": "round verified", "model_calls": 1, "id": state["id"]}
            resume_id = None


def foreground_dispatch(config, *, pane_pid, timeout=None, resume_id=None, gh_bin="gh"):
    """Adopt the owner-selected foreground coding pane; starts zero models.

    The dispatcher runs outside the coding model (explicit OAP_ROLE=strategic)
    and, under the coding role lock, verifies: the accepted runtime baseline
    (repository, origin, governance at the literal trusted ref), the
    explicitly selected pane PID's tmux identity plus its exact Codex
    descendant, and the durable protocol state including consumed.json. It
    then consumes exactly one OK control frame, re-verifies the pane
    liveness/argv/cwd and the order state after the OS wait, and writes the
    durable consumed record before returning the paste-ready handoff. A
    duplicate completed signal cannot dispatch implementation; an unfinished
    consumed order requires an explicit same-ID resume.
    """
    require(os.environ.get("OAP_ROLE") == "strategic", "ROLE_REQUIRED")
    repo = safe_path(config["OAP_REPO_ROOT"], kind="dir")
    layout = workspace_layout(repo)
    require(layout is not None and layout.get("coding_dispatch") == "foreground", "FOREGROUND_NOT_SELECTED")
    # Cross-role topology, FIFO identity, role homes and prompt role checks;
    # no model/auth qualification for a dispatcher that launches no model.
    role_context(config, "coding", check_selected=False, dispatch=True)
    require(config.get("OAP_GITHUB_REPOSITORY") and config.get("OAP_ACCEPTED_REF"), "REMOTE_BASELINE_REQUIRED")
    origin = git(repo, "remote", "get-url", "origin").decode().strip()
    expected = config["OAP_GITHUB_REPOSITORY"]
    require(origin in (f"https://github.com/{expected}.git", f"https://github.com/{expected}", f"git@github.com:{expected}.git"), "REMOTE_ORIGIN_MISMATCH")
    strategy = strategic_path(config["OAP_STRATEGIC_HOME"], repo=repo, kind="dir")
    governance(repo, "accepted-runtime", config["OAP_ACCEPTED_REF"], strategy=strategy)
    remote = GitHub(config["OAP_GITHUB_REPOSITORY"], gh_bin)
    # The versioned layout record stores the exact relaunch argv, codex
    # binary first (validated by workspace_layout); the pane matcher
    # compares the binary plus post-binary arguments.
    launch = list(layout["foreground_launch"])
    require(launch and launch[0] == "codex", "LAYOUT_FOREGROUND_LAUNCH_SHAPE")
    launch_args = launch[1:]
    with lock(strategy / ".coding.lock"):
        pane = foreground_pane(repo, pane_pid, launch_args)
        state = protocol_state(repo, strategy=strategy, remote=remote)
        if state["state"] == "INACTIVE":
            raise OAPError("NO_ACTIVE_ROUND")
        if state["state"] in ("PUBLICATION_RECONCILIATION_REQUIRED", "REVIEW_READY"):
            raise OAPError("COMPLETED_REPLAY")
        if state["state"] == "RECOVERY_REQUIRED":
            require(resume_id == state["id"], "EXPLICIT_SAME_ORDER_RECOVERY_REQUIRED")
        order_path = matching(repo, "orders", state["id"])
        require(order_path is not None, "ACTIVE_ORDER_MISSING")
        order_before = read(order_path)
        order_hash = digest(order_before)
        peers = remote.branch_prs(state["branch"])
        require(len(peers) <= 1, "DUPLICATE_PR")
        # state=all peers include closed/merged history: an owner's mid-round
        # merge is observed history requiring strategic reconciliation
        # (e.g. explicit merged-tail recognition in the next round), never a
        # blind dispatch or resumed coding. Only an exactly open, unmerged
        # peer may proceed; missing/unknown state fails closed. Reject
        # before consuming control.
        for peer in peers:
            require(peer.get("state") == "open" and peer.get("merged") is not True,
                    "MERGED_PEER_REQUIRES_RECONCILIATION")
        # On same-ID resume the durable consumed record is the PR identity
        # binding when the order itself names no PR (CREATE_NEW_PR rounds).
        consumed_pr = None
        if state["state"] == "RECOVERY_REQUIRED":
            consumed_pr = jsread(strategy / "workorders/consumed.json").get("pr")
        if state["pr"] is not None:
            require(len(peers) == 1 and peers[0]["number"] == state["pr"], "RECOVERY_PR_MISMATCH")
        elif consumed_pr is not None:
            require(len(peers) == 1 and peers[0]["number"] == consumed_pr, "RECOVERY_PR_MISMATCH")
        frame = fifo(fifo_home(repo, strategy) / "control.fifo", "wait", timeout=timeout)
        require(frame == {"frame": "OK", "bytes": 2}, "FIFO_INVALID_FRAME")
        # The OS wait is not a trust boundary: re-verify the selected pane
        # (liveness, argv, cwd), the durable order state, the exact active
        # order bytes, and the remote PR peers before handoff.
        pane = foreground_pane(repo, pane_pid, launch_args)
        state_after = protocol_state(repo, strategy=strategy, remote=remote)
        require(state_after["id"] == state["id"] and state_after["state"] == state["state"], "STATE_CHANGED_DURING_DISPATCH")
        require(read(order_path) == order_before and digest(read(order_path)) == order_hash,
                "ORDER_CHANGED_DURING_DISPATCH")
        require(remote.branch_prs(state["branch"]) == peers, "PR_CHANGED_DURING_DISPATCH")
        consumed = {"id": state["id"], "branch": state["branch"],
                    "pr": peers[0]["number"] if peers else None,
                    "phase": "consumed", "recovery": resume_id == state["id"],
                    "dispatch": "foreground", "pane_pid": pane}
        atomic(strategy / "workorders/consumed.json", json_bytes(consumed), mode=0o600)
        handoff = (
            "OAP_ROLE=coding. Foreground handoff: this already-running pane is the sole coding agent; "
            "export OAP_ROLE=coding in every helper command environment. Do not wait for control again: "
            "the exact OK frame was consumed once outside this model.\n"
            f"Exact active order: {state['id']}. Read the repository router and oap/coding-instructions/AGENTS.md, "
            "then its ordered compact read set and the exact active order.\n"
            "No subagents, background codex exec, alternate providers, launchers or auto-restarts.\n"
            "Implement only that bounded round, open/keep its one PR, publish its verified report and "
            "remain at the foreground prompt."
        )
        return {"result": "handoff ready", "pane_pid": pane, "id": state["id"],
                "state": state["state"], "recovery": state["state"] == "RECOVERY_REQUIRED",
                "control_frame": frame, "handoff": handoff,
                "consumed_record": "workorders/consumed.json",
                "models_started": 0, "signals_sent": 0}


def tmux_plan(config, operational, *, config_path):
    require(shutil.which("tmux"), "TMUX_MISSING")
    repo, strategy = Path(config["OAP_REPO_ROOT"]), Path(config["OAP_STRATEGIC_HOME"])
    if operational and coding_dispatch_mode(repo) == "foreground":
        # The operational two-pane session would spawn the coding model in a
        # background pane; the foreground runtime refuses it outright.
        raise OAPError("FOREGROUND_DISPATCH_ONLY")
    roles = [role_context(config, r, operational=operational, check_selected=False) for r in ("coding", "strategic")]
    session = config["OAP_RUN_TMUX_SESSION" if operational else "OAP_SETUP_TMUX_SESSION"]
    require(re.fullmatch(r"[A-Za-z0-9_-]+", session), "TMUX_SESSION_NAME")
    project = digest((str(repo) + "\0" + str(strategy) + "\0" + str(operational)).encode())
    commands = []
    for c in roles:
        role = c["role"]
        tool = repo / "oap/bin/oap_cli.py"
        prefix = ['env', 'OAP_ROLE='+role, 'CODEX_HOME='+c['home']]
        shell = prefix + ["python3", str(tool), "setup-shell", "--config", str(config_path), "--role", role]
        if operational:
            run = prefix + ["python3", str(tool), "launch", "--config", str(config_path), "--role", role]
            # Shell syntax uses shlex.join, never JSON as shell escaping. A run is
            # followed by a live role shell once; there is no restart loop on quit.
            command = shlex.join(run) + "; exec " + shlex.join(shell)
        else:
            command = "exec " + shlex.join(shell)
        commands.append(command)
    return {"session": session, "project_marker": project, "roles": [{k: c[k] for k in ("role", "cwd", "home")} for c in roles],
            "commands": [["tmux", "new-session", "-d", "-s", session, "-c", roles[0]["cwd"], commands[0]],
                         ["tmux", "set-option", "-t", session, "@oap_project", project],
                         ["tmux", "split-window", "-h", "-t", session + ":0", "-c", roles[1]["cwd"], commands[1]],
                         ["tmux", "select-layout", "-t", session, "even-horizontal"],
                         ["tmux", "attach-session", "-t", session]]}


def tmux_launch(config, operational, config_path, *, print_only=False):
    plan = tmux_plan(config, operational, config_path=config_path)
    if print_only:
        return plan | {"writes": 0, "processes_started": 0}
    session = plan["session"]
    with lock(Path(config["OAP_STRATEGIC_HOME"]) / ".tmux.lock"):
        exists = subprocess.run(["tmux", "has-session", "-t", "=" + session], capture_output=True).returncode == 0
        if exists:
            marker = subprocess.run(["tmux", "show-options", "-v", "-t", "=" + session, "@oap_project"], capture_output=True, text=True)
            require(marker.stdout.strip() == plan["project_marker"], "UNRELATED_TMUX_SESSION")
        else:
            for cmd in plan["commands"][:-1]:
                p = subprocess.run(cmd)
                require(p.returncode == 0, "TMUX_SETUP_FAILED")
    return {"exit_code": subprocess.run(plan["commands"][-1]).returncode, "restarted": False}
