"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Review sheet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records = json.loads((args.input / "summary.json").read_text(encoding="utf-8"))
    rows = []
    for item in sorted(records.get("responses", []), key=lambda value: str(value.get("id", ""))):
        identifier = str(item.get("id", ""))
        rows.append(
            {
                "blind_id": hashlib.sha256(identifier.encode()).hexdigest()[:12],
                "original": "",
                "repaired": "",
                "target_evidence": "",
                "review_proposal": "",
                "acceptance": "",
                "human_label": "",
            }
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in rows) + ("\n" if rows else ""),
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
