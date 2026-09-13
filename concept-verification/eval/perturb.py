"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE. Case validator."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval.common import dataset_identity, load_cases  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", type=Path, default=Path(__file__).parent / "cases/dev.jsonl")
    parser.add_argument(
        "--heldout", type=Path, default=Path(__file__).parent / "cases/heldout.jsonl"
    )
    args = parser.parse_args()
    dev, heldout = load_cases(args.dev), load_cases(args.heldout)
    if len(dev) < 16 or len(heldout) < 32:
        raise SystemExit("controlled split is smaller than the ordered minimum")
    import json

    print(
        json.dumps(
            {"dev": dataset_identity(args.dev), "heldout": dataset_identity(args.heldout)},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
