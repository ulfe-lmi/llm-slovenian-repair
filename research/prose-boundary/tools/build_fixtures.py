"""008-a: build the frozen fixture suite (fixtures.json).

Reads tools/fixture_defs.py (frozen expected structural safety semantics,
declared before any parser run) and emits research/prose-boundary/fixtures/
fixtures.json with EXACT byte offsets into each fixture's UTF-8 input bytes.

Strictness (fail closed):
  * every anchor must exist; without a *_anchor_last flag it must be unique;
  * every region must satisfy 0 <= start <= end <= len(text);
  * every region boundary is a code-point boundary by construction (regions
    are resolved in code points and then converted to bytes);
  * region order and names are preserved verbatim from the definitions.

This builder is deterministic: the same definitions always produce the same
fixtures.json bytes (sorted keys off, stable order, LF newlines).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixture_defs import FIXTURES, LONG_PARAGRAPH_FIXTURE, LONG_PARAGRAPH_SENTENCES  # noqa: E402

REQUIRED_CLASSES = set(range(1, 39))

# Explicit code-point overrides for regions whose anchors would be ambiguous.
CP_OVERRIDES = {
    ("F20", "bullet-1"): (8, 10),
    ("F20", "bullet-2"): (23, 25),
    ("F21", "quote-mark-1"): (7, 9),
    ("F21", "quote-mark-2"): (30, 32),
    ("F06", "fence"): (19, 44),
    ("F44", "label"): (6, 12),
    ("F44", "ref-syntax"): (12, 18),
    ("F50", "fence"): (9, 23),
    ("F42", "item-1"): (11, 14),
    ("F42", "item-1-1"): (19, 26),
    ("F42", "item-1-2"): (31, 38),
    ("F42", "item-2"): (41, 44),
}


def cp_to_byte(text: str, cp: int) -> int:
    return len(text[:cp].encode("utf-8"))


def resolve(text: str, region: dict, fid: str, rname: str) -> tuple[int, int]:
    key = (fid, rname)
    if key in CP_OVERRIDES:
        start, end = CP_OVERRIDES[key]
        if not (0 <= start <= end <= len(text)):
            raise SystemExit(f"{fid}/{rname}: override out of bounds: {start}..{end}")
        return start, end
    if "start_cp" in region:
        start = region["start_cp"]
    else:
        anchor = region["start_anchor"]
        count = text.count(anchor)
        if count == 0:
            raise SystemExit(f"{fid}/{rname}: start anchor missing: {anchor!r}")
        if count > 1 and not region.get("start_anchor_last"):
            raise SystemExit(f"{fid}/{rname}: start anchor not unique: {anchor!r}")
        start = text.rfind(anchor) if region.get("start_anchor_last") else text.find(anchor)
    if "end_cp" in region:
        end = region["end_cp"]
    else:
        anchor = region["end_anchor"]
        count = text.count(anchor)
        if count == 0:
            raise SystemExit(f"{fid}/{rname}: end anchor missing: {anchor!r}")
        if count > 1 and not region.get("end_anchor_last"):
            raise SystemExit(f"{fid}/{rname}: end anchor not unique: {anchor!r}")
        last = region.get("end_anchor_last")
        end = (text.rfind(anchor) + len(anchor)) if last else (text.find(anchor) + len(anchor))
    if not (0 <= start <= end <= len(text)):
        raise SystemExit(f"{fid}/{rname}: region out of bounds: {start}..{end}")
    return start, end


def build_long_paragraph_text() -> str:
    rounds = 6
    parts: list[str] = []
    for r in range(rounds):
        for s in LONG_PARAGRAPH_SENTENCES:
            parts.append(s)
    return " ".join(parts) + "\n"


def main() -> None:
    fixtures = []
    for spec in [*FIXTURES, LONG_PARAGRAPH_FIXTURE]:
        if spec["text"] is None:
            text = build_long_paragraph_text()
        else:
            text = spec["text"]
        data = text.encode("utf-8")
        regions = []
        for region in spec["regions"]:
            if spec["id"] == "F46":
                start_cp, end_cp = 0, len(text) - 1  # exclude trailing newline
            else:
                start_cp, end_cp = resolve(text, region, spec["id"], region["name"])
            roles = {
                "P0": region.get("role_by_profile", {}).get("P0", region["role"]),
                "P1": region.get("role_by_profile", {}).get("P1", region["role"]),
                "P2": region.get("role_by_profile", {}).get("P2", region["role"]),
            }
            regions.append(
                {
                    "name": region["name"],
                    "role_by_profile": roles,
                    "start_byte": cp_to_byte(text, start_cp),
                    "end_byte": cp_to_byte(text, end_cp),
                    "note": region.get("note", ""),
                }
            )
        fixtures.append(
            {
                "id": spec["id"],
                "class": spec["cls"],
                "class_name": spec["cls_name"],
                "input": text,
                "input_bytes": len(data),
                "input_sha256": hashlib.sha256(data).hexdigest(),
                "note": spec.get("note", ""),
                "regions": regions,
            }
        )

    classes = {f["class"] for f in fixtures}
    missing = sorted(REQUIRED_CLASSES - classes)
    if missing:
        raise SystemExit(f"missing required classes: {missing}")

    out = {
        "schema": "008a-fixtures/1",
        "frozen_before_first_parser_run": True,
        "frozen_note": (
            "Expected structural safety semantics are frozen in this file BEFORE any "
            "parser output is inspected (order 008-a requirement 3). No "
            "parser-specific expectations may be added afterwards without a recorded "
            "strategy-approved rationale."
        ),
        "coordinate_convention": {
            "unit": "byte offset into the exact UTF-8 input bytes of 'input'",
            "range": "[start_byte, end_byte)",
            "invariants": [
                "0 <= start_byte <= end_byte <= input_bytes",
                "boundaries lie on UTF-8 code-point boundaries",
                "input[start_byte:end_byte] is the intended original source slice",
                "byte<->code-point mapping is deterministic and exactly reversible",
            ],
        },
        "region_roles": {
            "PROSE_CANDIDATE": "must be exposed as candidate prose under the frozen structural policy",
            "PROTECTED": "must never be exposed as candidate prose",
            "NEUTRAL": "no assertion; conservative behaviour is recorded as a tradeoff",
        },
        "profiles": {
            "P0": "CommonMark core (Options::empty())",
            "P1": "P0 + ENABLE_TABLES + ENABLE_STRIKETHROUGH + ENABLE_TASKLISTS + ENABLE_MATH",
            "P2": "P1 + ENABLE_YAML_STYLE_METADATA_BLOCKS",
        },
        "fixtures": fixtures,
    }
    target = Path(__file__).resolve().parent.parent / "fixtures" / "fixtures.json"
    target.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    total_bytes = sum(f["input_bytes"] for f in fixtures)
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    print(f"fixtures: {len(fixtures)}, classes: {len(classes)}, total input bytes: {total_bytes}")


if __name__ == "__main__":
    main()
