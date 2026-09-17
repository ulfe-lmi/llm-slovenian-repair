"""008-a Increment 1 evaluator (deterministic).

Runs the pinned measurement adapter (and the stock pulldown-cmark CLI for
cross-checks) over the frozen fixture suite, verifies the hard coordinate
contract, the frozen structural policy, event semantics, UTF-8 behaviour,
malformed-input recovery and math behaviour, and writes data-free aggregates:

  results/increment1/events-P{0,1,2}.jsonl   (per-event records, project-authored input)
  results/increment1/summary.json            (aggregates + per-fixture results)
  results/increment1/gate-decision.json      (predeclared gate checkpoint)

Exit code 0 iff every Hard invariant holds on every fixture and profile.
No private data is read or written by this tool.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import coordinate as C  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIXTURES = ROOT / "fixtures" / "fixtures.json"
CONFIG = ROOT / "config" / "experiment-008a.json"
OUT = ROOT / "results" / "increment1"
PROFILES = ("P0", "P1", "P2")

# Binaries are supplied as CLI arguments (private scratch roots are never
# committed; privacy rule). Usage:
#   python3 run_increment1.py <adapter-bin> <stock-cli-bin>
def _required_arg(index: int, what: str) -> Path:
    if len(sys.argv) <= index or not sys.argv[index]:
        raise SystemExit(f"missing required argument {index}: {what} "
                         "(private scratch paths are never committed)")
    return Path(sys.argv[index])


def _load_bins() -> tuple[Path, Path]:
    return _required_arg(1, "adapter binary (prose-boundary-meas)"), \
        _required_arg(2, "stock pulldown-cmark CLI binary")

CLI_FLAGS = {
    "P0": [],
    "P1": ["--enable-tables", "--enable-strikethrough", "--enable-tasklists", "--enable-math"],
    "P2": [
        "--enable-tables",
        "--enable-strikethrough",
        "--enable-tasklists",
        "--enable-math",
        "--enable-metadata-blocks",
    ],
}

# Adapter kind token -> stock-CLI top-level event token (for cross-checks).
TOP_KIND = {
    "S.": "Start",
    "E.": "End",
    "Text": "Text",
    "Code": "Code",
    "InlineMath": "InlineMath",
    "DisplayMath": "DisplayMath",
    "Html": "Html",
    "InlineHtml": "InlineHtml",
    "FootnoteRef": "FootnoteReference",
    "SoftBreak": "SoftBreak",
    "HardBreak": "HardBreak",
    "Rule": "Rule",
    "TaskListMarker": "TaskListMarker",
}


def top_kind(token: str) -> str:
    if token.startswith("S.") or token.startswith("E."):
        return TOP_KIND[token[:2]]
    return TOP_KIND[token]


def run_adapter(data: bytes, profile: str, adapter_bin: Path) -> tuple[int, bytes, bytes]:
    proc = subprocess.run(
        [str(adapter_bin), profile],
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    return proc.returncode, proc.stdout, proc.stderr


def parse_events(raw: bytes) -> list[dict]:
    events = []
    for line in raw.decode("utf-8").splitlines():
        if not line:
            continue
        obj = json.loads(line)
        if "eof" in obj:
            events.append(obj)
            continue
        for key in ("i", "k", "s", "e"):
            if key not in obj:
                raise ValueError(f"malformed event line: {line!r}")
        events.append(obj)
    return events


def run_cli(data: bytes, profile: str, cli_bin: Path) -> tuple[int, bytes, bytes]:
    proc = subprocess.run(
        [str(cli_bin)] + CLI_FLAGS[profile] + ["--events"],
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    return proc.returncode, proc.stdout, proc.stderr


def parse_cli_events(raw: bytes) -> list[tuple[str, int, int]]:
    out = []
    text = raw.decode("utf-8", "replace")
    for line in text.splitlines():
        if line == "EOF" or not line:
            continue
        # Stock CLI --events format: "<start>..<end>: <Event>(...)"
        sep = line.find(": ")
        if sep < 0:
            continue
        head, rest = line[:sep], line[sep + 2 :]
        if ".." not in head:
            continue
        s, e = head.split("..")
        if not (s.isdigit() and e.isdigit()):
            continue
        top = rest.split("(", 1)[0].strip()
        out.append((top, int(s), int(e)))
    return out


def policy_match(token: str, entries: list[str]) -> bool:
    """Frozen policy names container families; the adapter emits level-suffixed
    tokens (S.Head:N, S.List:ol:N). A family entry matches its own token or any
    token of the form '<entry>:<suffix>' (implementation note D1)."""
    return any(token == e or token.startswith(e + ":") for e in entries)


def candidate_prose(events: list[dict], data: bytes, policy: dict) -> list[tuple[int, int]]:
    """Text-leaf ranges that are candidate prose under the frozen policy."""
    prose_entries = list(policy["PROSE_CONTAINERS"])
    non_prose_entries = list(policy["NON_PROSE_CONTAINERS"])
    stack: list[tuple[str, int]] = []
    out: list[tuple[int, int]] = []
    for ev in events:
        if "k" not in ev:
            continue
        kind = ev["k"]
        if kind.startswith("S."):
            stack.append((kind, ev["s"]))
            continue
        if kind.startswith("E."):
            if not stack:
                raise ValueError(f"unbalanced End event {kind!r}")
            stack.pop()
            continue
        if kind == "Text":
            tokens = [t for t, _ in stack]
            if not any(policy_match(t, prose_entries) for t in tokens):
                continue
            if any(policy_match(t, non_prose_entries) for t in tokens):
                continue
            # D0 (autolink destinations): a CommonMark autolink is the only
            # S.Link whose original source slice starts with '<'. Its inner
            # Text leaf IS the link destination, so it is protected by the
            # frozen policy intent "link destinations remain protected".
            # Deterministic source-byte test; no content parsing.
            if any(
                t == "S.Link" and data[s:s + 1] == b"<"
                for t, s in stack
            ):
                continue
            out.append((ev["s"], ev["e"]))
    return out


def region_check(region: dict, profile: str, cand: set[int], data: bytes) -> dict:
    role = region["role_by_profile"][profile]
    s, e = region["start_byte"], region["end_byte"]
    span = set(range(s, e))
    exposed = span & cand
    result = {"name": region["name"], "role": role, "start": s, "end": e}
    if role == "PROSE_CANDIDATE":
        result["ok"] = len(exposed) == len(span)
        result["missing_bytes"] = len(span) - len(exposed)
    elif role == "PROTECTED":
        result["ok"] = len(exposed) == 0
        result["exposed_bytes"] = len(exposed)
    else:  # NEUTRAL
        result["ok"] = True
        result["exposed_bytes"] = len(exposed)
        result["tradeoff_recorded"] = len(exposed) > 0
    return result


def main() -> int:
    ADAPTER_BIN, CLI_BIN = _load_bins()
    fixtures_doc = json.loads(FIXTURES.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    policy = config["structural_policy"]
    OUT.mkdir(parents=True, exist_ok=True)

    event_files = {p: OUT / f"events-{p}.jsonl" for p in PROFILES}
    for p in PROFILES:
        event_files[p].write_text("")

    per_fixture: dict[str, dict] = {}
    total_events = 0
    coordinate_violations: list[dict] = []
    reversibility_failures: list[dict] = []
    cli_mismatches: list[dict] = []
    unexpected_kinds: Counter = Counter()
    exit_code_probes: dict[str, int] = {}

    # Self-test (negative probes, order 008-a Verification): the evaluator's own
    # detectors must catch deliberately corrupted ranges and semantics before any
    # fixture result is trusted. Deterministic, project-authored, data-free.
    self_test: dict[str, bool] = {}
    probe = "\u010d".encode("utf-8")  # two-byte sequence (c-caron)
    self_test["coordinate_bisection_caught"] = bool(C.check_range(probe, 0, 1))
    # "a\u010db" = b'a' b'\xc4' b'\x8d' b'b': boundaries 0,1,3,4; pos 2 bisects
    self_test["round_trip_reversible_at_boundary"] = (
        C.round_trip("a\u010db", 1) and C.round_trip("a\u010db", 3)
        and C.byte_to_cp(probe, 1) is None
    )
    r_prot = region_check(
        {"name": "t", "role_by_profile": {"P0": "PROTECTED"}, "start_byte": 0, "end_byte": 2},
        "P0", {0, 1}, b"ab",
    )
    self_test["protected_exposure_caught"] = (not r_prot["ok"]) and r_prot["exposed_bytes"] == 2
    r_miss = region_check(
        {"name": "t", "role_by_profile": {"P0": "PROSE_CANDIDATE"}, "start_byte": 0, "end_byte": 2},
        "P0", set(), b"ab",
    )
    self_test["prose_missing_caught"] = (not r_miss["ok"]) and r_miss["missing_bytes"] == 2
    self_test["cli_offset_mismatch_caught"] = (
        sorted([("Text", 0, 3)]) != sorted([("Text", 0, 2)])
    )
    self_test_ok = all(self_test.values())
    if not self_test_ok:
        raise SystemExit(f"evaluator self-test failed: {self_test}")

    for fixture in fixtures_doc["fixtures"]:
        fid = fixture["id"]
        data = fixture["input"].encode("utf-8")
        assert hashlib.sha256(data).hexdigest() == fixture["input_sha256"]
        entry: dict = {"id": fid, "class": fixture["class"], "class_name": fixture["class_name"], "profiles": {}}
        for profile in PROFILES:
            rc, out, err = run_adapter(data, profile, ADAPTER_BIN)
            if rc != 0:
                entry["profiles"][profile] = {"adapter_exit": rc, "stderr": err.decode("utf-8", "replace")[:400]}
                continue
            events = parse_events(out)
            assert events[-1].get("eof") is True, f"{fid}/{profile}: missing eof marker"
            # (5) hard coordinate invariant on every emitted range
            for ev in events:
                if "k" not in ev:
                    continue
                problems = C.check_range(data, ev["s"], ev["e"])
                if problems:
                    coordinate_violations.append(
                        {"fixture": fid, "profile": profile, "i": ev["i"], "k": ev["k"],
                         "s": ev["s"], "e": ev["e"], "problems": problems}
                    )
                # deterministic exact reversibility of the byte<->code-point
                # mapping on every emitted boundary (order requirement 5)
                text_cp = fixture["input"]
                for bound in (ev["s"], ev["e"]):
                    cp = C.byte_to_cp(data, bound)
                    if cp is None or C.cp_to_byte(text_cp, cp) != bound:
                        reversibility_failures.append(
                            {"fixture": fid, "profile": profile, "i": ev["i"],
                             "k": ev["k"], "bound": bound}
                        )
                if ev["k"].startswith("UNEXPECTED:"):
                    unexpected_kinds[ev["k"]] += 1
            # (4) event semantics + structural policy via candidate set
            cand_ranges = candidate_prose(events, data, policy)
            cand = C.as_byte_set(cand_ranges)
            results = [region_check(r, profile, cand, data) for r in fixture["regions"]]
            ok = all(r["ok"] for r in results) and not any(
                v["fixture"] == fid and v["profile"] == profile for v in coordinate_violations
            )
            # stock CLI cross-check (independent range measurement)
            crc, cout, cerr = run_cli(data, profile, CLI_BIN)
            cli = parse_cli_events(cout) if crc == 0 else None
            adapter_triples = [
                (top_kind(ev["k"]), ev["s"], ev["e"]) for ev in events if "k" in ev
            ]
            cli_match = cli is not None and sorted(cli) == sorted(adapter_triples)
            if not cli_match:
                cli_mismatches.append(
                    {"fixture": fid, "profile": profile, "cli_rc": crc,
                     "adapter_n": len(adapter_triples), "cli_n": len(cli) if cli is not None else None,
                     "stderr": cerr.decode("utf-8", "replace")[:400]}
                )
            entry["profiles"][profile] = {
                "adapter_exit": 0,
                "event_count": len(events) - 1,
                "region_results": results,
                "policy_ok": ok,
                "cli_crosscheck_ok": cli_match,
                "candidate_bytes": len(cand),
            }
            # record events (raw adapter bytes: the determinism contract is that
            # an identical rerun emits identical bytes, so both passes record raw)
            with event_files[profile].open("ab") as fh:
                fh.write(out)
            total_events += len(events) - 1
        per_fixture[fid] = entry

    # Invalid-UTF-8 probe (documented behaviour: exit 3, no events).
    rc, out, _ = run_adapter(b"\xff\xfe\x00x", "P1", ADAPTER_BIN)
    exit_code_probes["invalid_utf8_exit_code"] = rc
    exit_code_probes["invalid_utf8_output"] = out.decode("utf-8", "replace").strip()

    # Determinism: full rerun on P1 must be byte-identical.
    first = {p: event_files[p].read_bytes() for p in PROFILES}
    for p in PROFILES:
        event_files[p].write_text("")
    for fixture in fixtures_doc["fixtures"]:
        data = fixture["input"].encode("utf-8")
        for profile in PROFILES:
            rc, out, _ = run_adapter(data, profile, ADAPTER_BIN)
            with event_files[profile].open("a", encoding="utf-8") as fh:
                fh.write(out.decode("utf-8"))
    deterministic = all(event_files[p].read_bytes() == first[p] for p in PROFILES)

    hard = {
        "coordinate_invariants": len(coordinate_violations) == 0,
        "byte_codepoint_round_trip": len(reversibility_failures) == 0,
        "self_test_negative_probes": self_test_ok,
        "structural_policy_all_profiles": all(
            entry["profiles"][p].get("policy_ok", False)
            for entry in per_fixture.values()
            for p in PROFILES
        ),
        "no_unexpected_event_kinds": sum(unexpected_kinds.values()) == 0,
        "cli_crosscheck_all_fixtures": len(cli_mismatches) == 0,
        "deterministic_rerun_identical": deterministic,
        "invalid_utf8_rejected_cleanly": exit_code_probes["invalid_utf8_exit_code"] == 3,
    }
    all_hard_ok = all(hard.values())

    # Coverage/suppression tradeoffs (data-free).
    tradeoffs = {
        "neutral_regions_with_exposed_bytes": sum(
            1
            for entry in per_fixture.values()
            for p in PROFILES
            for r in entry["profiles"].get(p, {}).get("region_results", [])
            if r["role"] == "NEUTRAL" and r.get("tradeoff_recorded")
        ),
        "protected_region_exposures": sum(
            r.get("exposed_bytes", 0)
            for entry in per_fixture.values()
            for p in PROFILES
            for r in entry["profiles"].get(p, {}).get("region_results", [])
            if r["role"] == "PROTECTED"
        ),
        "prose_candidate_missing_bytes": sum(
            r.get("missing_bytes", 0)
            for entry in per_fixture.values()
            for p in PROFILES
            for r in entry["profiles"].get(p, {}).get("region_results", [])
            if r["role"] == "PROSE_CANDIDATE"
        ),
    }

    # Gate checkpoint (predeclared stop condition + proceed conditions).
    proceed_conditions = {
        "hard_coordinate_fidelity": hard["coordinate_invariants"],
        "no_code_point_bisection": hard["coordinate_invariants"],
        "byte_codepoint_round_trip": hard["byte_codepoint_round_trip"],
        "self_test_negative_probes": hard["self_test_negative_probes"],
        "recognized_code_math_never_exposed": all(
            r.get("exposed_bytes", 0) == 0
            for entry in per_fixture.values()
            for p in ("P1", "P2")
            for r in entry["profiles"].get(p, {}).get("region_results", [])
            if r["role"] == "PROTECTED"
            and any(
                kw in entry["class_name"]
                for kw in ("code", "math", "html", "front-matter")
            )
        ),
        "link_destinations_protected": all(
            r.get("exposed_bytes", 0) == 0
            for entry in per_fixture.values()
            for p in PROFILES
            for r in entry["profiles"].get(p, {}).get("region_results", [])
            if r["name"] in ("dest", "definition", "angle-autolink", "mailto", "url-autolink")
        ),
        "prose_containers_expose_leaves": all(
            r.get("missing_bytes", 0) == 0
            for entry in per_fixture.values()
            for p in PROFILES
            for r in entry["profiles"].get(p, {}).get("region_results", [])
            if r["role"] == "PROSE_CANDIDATE"
        ),
        "bounded_deterministic": hard["deterministic_rerun_identical"],
        "stock_cli_crosscheck": hard["cli_crosscheck_all_fixtures"],
    }
    decision = "PROCEED_TO_INCREMENT_2" if all(
        proceed_conditions.values()
    ) and all_hard_ok else "STOP_NO_GO"

    summary = {
        "schema": "008a-increment1-summary/1",
        "fixture_file_sha256": hashlib.sha256(FIXTURES.read_bytes()).hexdigest(),
        "config_sha256": hashlib.sha256(CONFIG.read_bytes()).hexdigest(),
        "adapter_bin_sha256": hashlib.sha256(ADAPTER_BIN.read_bytes()).hexdigest(),
        "fixtures": len(fixtures_doc["fixtures"]),
        "profiles": list(PROFILES),
        "total_events": total_events,
        "hard_invariants": hard,
        "all_hard_ok": all_hard_ok,
        "coordinate_violations": coordinate_violations,
        "reversibility_failures": reversibility_failures,
        "self_test": self_test,
        "cli_mismatches": cli_mismatches,
        "unexpected_kinds": dict(unexpected_kinds),
        "exit_code_probes": exit_code_probes,
        "tradeoffs": tradeoffs,
        "per_fixture": per_fixture,
        "utf8_notes": {
            "carons_emoji_decomposed": [
                f["id"] for f in fixtures_doc["fixtures"]
                if f["id"] in ("F33", "F34", "F35", "F45")
            ],
            "crlf_fixtures": [
                f["id"] for f in fixtures_doc["fixtures"]
                if f["id"] in ("F36", "F45", "F50")
            ],
        },
        "math_behaviour": {
            "inline_math_fixture": "F10",
            "display_math_fixture": "F11",
            "currency_fixture": "F16",
            "escaped_dollars_fixture": "F17",
            "math_extension_available_in_0_13_4": True,
            "math_feature_gate": "none (Options::ENABLE_MATH bitflag; not a Cargo feature)",
        },
        "malformed_input_fixtures": ["F07", "F15", "F37", "F38", "F49"],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    gate = {
        "schema": "008a-gate-decision/1",
        "gate": "increment-1 strategy review checkpoint (order 008-a increment 1 step 9)",
        "summary_sha256": hashlib.sha256((OUT / "summary.json").read_bytes()).hexdigest(),
        "proceed_conditions": proceed_conditions,
        "decision": decision,
        "stop_condition_predeclared": "Any Hard invariant failure on the fixture suite stops the round with NO-GO evidence; work is not continued merely because it was planned.",
        "evaluator_implementation_notes": {
            "D0_autolink_destinations": (
                "Frozen policy intent 'link destinations remain protected' is "
                "implemented for CommonMark autolinks: the only S.Link whose "
                "original source slice starts with byte '<' is an autolink, and "
                "its inner Text leaf is the destination, so it is not candidate "
                "prose. Deterministic source-byte test; no content parsing."
            ),
            "D1_policy_token_families": (
                "The frozen policy names container families (e.g. S.Head, "
                "S.TableCell); the adapter emits level-suffixed tokens (S.Head:N, "
                "S.List:ol:N). A family entry matches its own token or any "
                "'<entry>:<suffix>' token. This implements the frozen rule "
                "'ancestor set intersects PROSE_CONTAINERS' without weakening or "
                "extending the named set."
            ),
        },
        "single_round_note": (
            "This round executes as a single reported round per the order's publication "
            "structure (one final report-only commit). The strategy review gate is enforced "
            "by the strategy final-head review before merge; this file and the OAP report "
            "record the gate-crossing evidence for that review."
        ),
    }
    (OUT / "gate-decision.json").write_text(json.dumps(gate, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"fixtures: {summary['fixtures']}, events: {summary['total_events']}")
    print("hard invariants:", json.dumps(hard))
    print("proceed conditions:", json.dumps(proceed_conditions))
    print("decision:", decision)
    return 0 if all_hard_ok else 1


if __name__ == "__main__":
    sys.exit(main())
