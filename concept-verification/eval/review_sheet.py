"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Review sheet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

PAIR_LABELS = (
    "ORIGINAL BETTER",
    "REPAIRED BETTER",
    "EQUIVALENT",
    "BOTH BAD / UNDECIDABLE",
)


def _load_trace(path: Path, trace_root: Path) -> dict[str, Any]:
    resolved = path.resolve()
    try:
        resolved.relative_to(trace_root.resolve())
    except ValueError as exc:
        raise SystemExit("trace is outside the configured trace directory") from exc
    if path.is_symlink() or not path.is_file():
        raise SystemExit("trace is not a regular file")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit("trace is not an object")
    original, repaired = value.get("original"), value.get("repaired")
    if (
        not isinstance(original, str)
        or not original
        or not isinstance(repaired, str)
        or not repaired
    ):
        raise SystemExit("completed trace has empty assistant text")
    protocol = value.get("protocol")
    if not isinstance(protocol, dict) or protocol.get("response_completed") is not True:
        raise SystemExit("trace is missing response.completed")
    return value


def _target_rows(trace: dict[str, Any]) -> list[dict[str, Any]]:
    decisions = trace.get("reviewer_decisions")
    if not isinstance(decisions, list):
        raise SystemExit("trace is missing target decisions")
    rows: list[dict[str, Any]] = []
    for decision in decisions:
        if not isinstance(decision, dict) or not isinstance(decision.get("candidate"), dict):
            raise SystemExit("trace target decision is malformed")
        candidate = decision["candidate"]
        acceptance = decision.get("acceptance")
        proposal = decision.get("proposal")
        rows.append(
            {
                "target": candidate.get("text"),
                "start": candidate.get("start"),
                "end": candidate.get("end"),
                "evidence": decision.get("evidence", candidate.get("evidence")),
                "proposal": proposal,
                "accepted": acceptance.get("accepted") if isinstance(acceptance, dict) else False,
                "replacement": acceptance.get("replacement")
                if isinstance(acceptance, dict)
                else None,
                "edit_label": "",
            }
        )
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--traces", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    records = json.loads((args.input / "summary.json").read_text(encoding="utf-8"))
    if not isinstance(records, dict) or not isinstance(records.get("responses"), list):
        raise SystemExit("workload summary is malformed")
    rows: list[dict[str, Any]] = []
    for item in sorted(records["responses"], key=lambda value: str(value.get("id", ""))):
        if not isinstance(item, dict) or item.get("status") != "COMPLETED":
            continue
        trace_values = item.get("trace_files")
        if not isinstance(trace_values, list) or not trace_values:
            raise SystemExit("completed workload row has no joined trace")
        for trace_value in trace_values:
            if not isinstance(trace_value, str):
                raise SystemExit("completed workload trace path is invalid")
            trace = _load_trace(Path(trace_value), args.traces)
            if item.get("request_id") is not None and trace.get("request_id") != item.get(
                "request_id"
            ):
                raise SystemExit("trace does not join its workload request")
            request_id = str(trace.get("request_id", ""))
            if not request_id:
                raise SystemExit("trace has no request ID")
            blind_id = hashlib.sha256(request_id.encode("utf-8")).hexdigest()[:12]
            swap = (
                int(hashlib.sha256(("007-b:" + request_id).encode("utf-8")).hexdigest()[-1], 16) % 2
            )
            original = str(trace["original"])
            repaired = str(trace["repaired"])
            left_text, right_text = (repaired, original) if swap else (original, repaired)
            rows.append(
                {
                    "blind_id": blind_id,
                    "request_id": request_id,
                    "case_id": item.get("id"),
                    "original": original,
                    "repaired": repaired,
                    "left": {"label": "A", "text": left_text},
                    "right": {"label": "B", "text": right_text},
                    "pair_label": "",
                    "allowed_pair_labels": list(PAIR_LABELS),
                    "targets": _target_rows(trace),
                }
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
        + ("\n" if rows else ""),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"rows": len(rows), "human_labels": "BLANK", "output": str(args.output)}, sort_keys=True
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
