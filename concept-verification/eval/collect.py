"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Workload collector."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse

WORKLOADS = (
    (
        "slovenian-explanation",
        "V slovenščini na kratko razloži razliko med glagolskim vidom in časom.",
    ),
    ("slovenian-summary", "V dveh stavkih povzemite pomen varovanja izvirnega besedila."),
    (
        "technical-english",
        "Explain in English why a buffered response must preserve event ordering.",
    ),
    ("markdown-code", "Pripravi kratek Markdown primer s kodo, ki izpiše zdravo."),
    (
        "commands-paths",
        "Naštej varne, suhe ukaze za pregled poti /tmp/project brez izvajanja sprememb.",
    ),
    ("mixed-language", "Primerjaj izraza endpoint in končna točka v tehničnem besedilu."),
    (
        "tool-loop",
        "V trenutnem delovnem imeniku ustvari datoteko codex-tool-loop-proof.txt z vsebino "
        "TOOL_LOOP_OK, jo preberi z orodjem in v odgovoru potrdi prebrano vsebino. Uporabi "
        "samo trenutni delovni imenik.",
    ),
    ("ordinary-coding", "V slovenščini opiši majhen test za nespremenjenost zaščitenih odsekov."),
)


def build_codex_command(
    codex_bin: str,
    profile: str,
    provider_id: str,
    proxy: str,
    workdir: Path,
    prompt: str,
) -> list[str]:
    parsed = urlparse(proxy)
    if parsed.hostname != "127.0.0.1":
        raise ValueError("workload proxy must be loopback")
    provider_literal = json.dumps(provider_id)
    proxy_literal = json.dumps(proxy.rstrip("/"))
    return [
        codex_bin,
        "exec",
        "--profile",
        profile,
        "--ephemeral",
        "--json",
        "--skip-git-repo-check",
        "--cd",
        str(workdir),
        "--dangerously-bypass-approvals-and-sandbox",
        "-c",
        f"model_provider={provider_literal}",
        "-c",
        f"model_providers.{provider_id}.base_url={proxy_literal}",
        prompt,
    ]


def _event_types(stdout: bytes) -> tuple[list[str], bool]:
    types: list[str] = []
    valid = True
    for line in stdout.decode("utf-8", "replace").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            valid = False
            continue
        if not isinstance(value, dict) or not isinstance(value.get("type"), str):
            valid = False
            continue
        types.append(value["type"])
    return types, valid


def _trace_snapshot(trace_dir: Path) -> set[Path]:
    if trace_dir.exists() and trace_dir.is_symlink():
        raise ValueError("trace directory must not be a symlink")
    trace_dir.mkdir(parents=True, exist_ok=True)
    return {path for path in trace_dir.glob("*.json") if path.is_file()}


def _safe_case_dir(work_root: Path, identifier: str) -> Path:
    if work_root.exists() and work_root.is_symlink():
        raise ValueError("work root must not be a symlink")
    work_root.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=f"{identifier}-", dir=work_root))


def _tool_loop_proof(case_dir: Path) -> bool:
    proof = case_dir / "codex-tool-loop-proof.txt"
    return proof.is_file() and proof.read_text(encoding="utf-8").strip() == "TOOL_LOOP_OK"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=8)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--codex-home", type=Path, required=True)
    parser.add_argument("--profile", default="qwen-neumann")
    parser.add_argument("--provider-id", required=True)
    parser.add_argument("--proxy", default="http://127.0.0.1:18024/v1")
    parser.add_argument("--trace-dir", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args(argv)
    if not 1 <= args.cases <= len(WORKLOADS):
        raise SystemExit("workload bound must be one through eight")
    if args.timeout <= 0:
        raise SystemExit("workload timeout must be positive")
    parsed = urlparse(args.proxy)
    if parsed.hostname != "127.0.0.1":
        raise SystemExit("workload proxy must be loopback")
    if not args.codex_home.is_dir() or args.codex_home.is_symlink():
        raise SystemExit("explicit CODEX_HOME must be an existing non-symlink directory")
    args.results.mkdir(parents=True, exist_ok=True)
    summary: list[dict[str, object]] = []
    for name, prompt in WORKLOADS[: args.cases]:
        started = time.monotonic()
        case_dir = _safe_case_dir(args.work_root, name)
        before = _trace_snapshot(args.trace_dir)
        record: dict[str, object] = {
            "id": name,
            "status": "BLOCKED",
            "human_label": "",
            "trace_files": [],
            "event_types": [],
            "terminal_response": False,
            "protocol_events_valid": False,
            "tool_loop_verified": False,
        }
        command = build_codex_command(
            args.codex_bin, args.profile, args.provider_id, args.proxy, case_dir, prompt
        )
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(args.codex_home)
        try:
            completed = subprocess.run(
                command,
                cwd=case_dir,
                env=environment,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                timeout=args.timeout,
                check=False,
            )
            event_types, protocol_valid = _event_types(completed.stdout)
            record["exit_code"] = completed.returncode
            record["event_types"] = event_types
            record["protocol_events_valid"] = protocol_valid and bool(event_types)
            terminal = bool({"turn.completed", "response.completed"}.intersection(event_types))
            record["terminal_response"] = terminal
            if completed.returncode != 0:
                record["failure"] = "codex_exit_nonzero"
            elif not terminal or not record["protocol_events_valid"]:
                record["failure"] = "codex_protocol_incomplete"
            else:
                record["status"] = "COMPLETED"
            if name == "tool-loop":
                record["tool_loop_verified"] = _tool_loop_proof(case_dir)
                if record["status"] == "COMPLETED" and not record["tool_loop_verified"]:
                    record["status"] = "BLOCKED"
                    record["failure"] = "tool_loop_evidence_missing"
        except subprocess.TimeoutExpired:
            record["failure"] = "codex_timeout"
        except OSError:
            record["failure"] = "codex_executable_unavailable"
        finally:
            after = _trace_snapshot(args.trace_dir)
            traces = sorted(after - before)
            record["trace_files"] = [str(path) for path in traces]
            request_ids: set[str] = set()
            for trace in traces:
                try:
                    value = json.loads(trace.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    continue
                if isinstance(value, dict) and isinstance(value.get("request_id"), str):
                    request_ids.add(value["request_id"])
            if request_ids:
                record["request_id"] = sorted(request_ids)[0] if len(request_ids) == 1 else None
                record["request_ids"] = sorted(request_ids)
            if record["status"] == "COMPLETED" and not traces:
                record["status"] = "BLOCKED"
                record["failure"] = "missing_proxy_trace"
            record["trace_joined"] = bool(traces)
            record["latency_seconds"] = round(time.monotonic() - started, 6)
            summary.append(record)
            shutil.rmtree(case_dir, ignore_errors=False)
    output = args.results / "summary.json"
    output.write_text(
        json.dumps(
            {
                "responses": summary,
                "responses_attempted": len(summary),
                "responses_completed": sum(item["status"] == "COMPLETED" for item in summary),
                "human_review": "AWAITING_HUMAN_REVIEW",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "responses_attempted": len(summary),
                "responses_completed": sum(item["status"] == "COMPLETED" for item in summary),
                "output": str(output),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
