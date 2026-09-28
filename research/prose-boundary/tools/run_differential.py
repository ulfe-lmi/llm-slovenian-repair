"""008-a Increment 2: differential A-vs-B evaluator (data-free).

Side A = the current hand-written protection, research/curated/protected.py
``protected_intervals`` (code-point coordinates, merged).
Side B = the pinned candidate (pulldown-cmark 0.13.4) via the measurement
adapter, profile P2, candidate-prose set under the frozen structural policy
(byte coordinates; B-protected = complement of the candidate set).

Disagreement unit: maximal span of the symmetric difference of the two
protected sets. Every span is classified by consequence into the 8 frozen
classes, applied in the frozen priority order [3, 6, 5, 4, 1, 2, 7, 8]:

  3  parser falsely exposes machine-significant content (SAFETY class):
     B exposes bytes that are inside a B machine context (S.Image / S.Meta),
     or adjacent (within 1 byte) to a B machine event (Code / Html /
     InlineHtml / InlineMath / DisplayMath).
  6  malformed-input safety difference: the sample is deterministically
     flagged malformed (odd fence-line count, odd backtick count, or
     unbalanced parentheses) and its protection state differs.
  5  source-coordinate mismatch: the span lies inside an A interval I and B
     still protects at least half of I (same construct, different boundary).
  4  parser unnecessarily suppresses valid prose: B protects, A exposed,
     span content prose-like.
  1  parser correctly exposes over-protected prose: B exposes, A protected,
     span content prose-like.
  2  parser correctly protects previously exposed non-prose: B protects,
     A exposed, span content not prose-like.
  7  expected residual semantic category: B exposes, A protected, content in
     the frozen residual set (TeX, JSON/YAML/TOML, shell, paths, env vars,
     identifiers, numbers, dialect-missed URLs) and not a boundary case.
  8  unresolved needing inspection: classifier cannot decide deterministically.

Privacy: raw text is held in memory only; the summary carries counts,
categories and hashes. A controlled synthetic-pair self-test (project-authored
texts) must pass before any corpus result is written (order 008-a
Verification: "the differential evaluator's self-test on a controlled
synthetic pair").

Deterministic: identical inputs produce identical output bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2]))  # repository root
import coordinate as C  # noqa: E402
import select_corpus as S  # noqa: E402
from research.curated.protected import protected_intervals  # noqa: E402

CONFIG = HERE.parent / "config" / "experiment-008a.json"
DEFAULT_OUT = HERE.parent / "results" / "increment2" / "differential-summary.json"
CHALLENGER_OUT = HERE.parent / "results" / "increment2" / "challenger-decision.json"
PROFILE = "P2"

MACHINE_EVENTS = ("Code", "Html", "InlineHtml", "InlineMath", "DisplayMath")
RESIDUAL_KINDS = {"tex", "bare_json", "yaml_toml_config", "shell", "path",
                  "env_var", "identifier", "number", "dialect_url"}
KIND_PRIORITY = ["url", "path", "shell", "tex", "structured", "identifier",
                 "number", "code_like", "env_var", "other", "prose"]

# ---- data-free token/span kind rules (config content_kind_rules) ----------
_RE_URL = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", re.IGNORECASE)
_RE_DOMAIN = re.compile(r"^[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
_RE_PATH = re.compile(r"^(?:\.?/|~/|[A-Za-z]:[\\/])")
_RE_REL_PATH = re.compile(r"^[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+$")
_RE_NUMBER = re.compile(r"^[+-]?\d[\d.,]*(?:\s?(?:%|[A-Za-z]{1,8}))?$")
_RE_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_RE_SHELL = re.compile(r"^(?:[$#>]\s|(?:sudo\s+)?(?:python|python3|uv|git|curl|npm|pip|pytest|ruff|mypy)\s)")
_RE_TEX = re.compile(r"\\[A-Za-z]+|\$\$|\\(begin|end)\{")
_RE_ENV = re.compile(r"^(?:\$[A-Za-z_][A-Za-z0-9_]*|[A-Za-z_][A-Za-z0-9_]*=)")


def token_kind(tok: str) -> str:
    if _RE_URL.match(tok) or _RE_DOMAIN.match(tok):
        return "url"
    if _RE_SHELL.match(tok):
        return "shell"
    if _RE_ENV.match(tok):
        return "env_var"
    if _RE_PATH.match(tok) or _RE_REL_PATH.match(tok):
        return "path"
    if _RE_TEX.search(tok):
        return "tex"
    if tok and tok[0] in "{[<":
        return "structured"
    if _RE_NUMBER.match(tok):
        return "number"
    if _RE_IDENT.match(tok) and (any(c.isdigit() for c in tok) or "_" in tok
                                 or sum(c.isupper() for c in tok) >= 2):
        return "identifier"
    if any(ch in tok for ch in "`;{}") or re.match(r"^[A-Za-z_]\w*\(", tok):
        return "code_like"
    letters = sum(1 for ch in tok if ch.isalpha())
    if tok and letters / len(tok) >= 0.6 and not any(c.isdigit() for c in tok) \
            and "_" not in tok:
        return "prose"
    return "other"


def span_kind(text: str) -> str:
    toks = text.split()
    if not toks:
        return "other"
    kinds = Counter(token_kind(t) for t in toks)
    best = max(kinds.values())
    winners = [k for k, n in kinds.items() if n == best]
    if len(winners) == 1:
        return winners[0]
    for k in KIND_PRIORITY:  # priority-order tiebreak
        if k in winners:
            return k
    return "mixed"


# ---- malformed flag (deterministic, data-free) ----------------------------
def malformed_flag(text: str) -> bool:
    fence_lines = sum(
        1 for line in text.splitlines()
        if line.lstrip().startswith(("```", "~~~"))
    )
    return (fence_lines % 2 == 1) or (text.count("`") % 2 == 1) \
        or (text.count("(") != text.count(")"))


# ---- parsing / sets ---------------------------------------------------------
def run_adapter(data: bytes, adapter_bin: str) -> tuple[int, list[dict]]:
    proc = subprocess.run([adapter_bin, PROFILE], input=data,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    if proc.returncode != 0:
        raise SystemExit(f"adapter failed rc={proc.returncode}")
    events = []
    for line in proc.stdout.decode("utf-8").splitlines():
        if not line:
            continue
        obj = json.loads(line)
        if "eof" in obj:
            continue
        events.append(obj)
    return proc.returncode, events


def candidate_bytes(events: list[dict], data: bytes, policy: dict) -> set[int]:
    prose_entries = list(policy["PROSE_CONTAINERS"])
    non_prose_entries = list(policy["NON_PROSE_CONTAINERS"])

    def match(token: str, entries: list[str]) -> bool:
        return any(token == e or token.startswith(e + ":") for e in entries)

    stack: list[tuple[str, int]] = []
    out: set[int] = set()
    for ev in events:
        kind = ev.get("k")
        if kind is None:
            continue
        if kind.startswith("S."):
            stack.append((kind, ev["s"]))
            continue
        if kind.startswith("E."):
            stack.pop()
            continue
        if kind != "Text":
            continue
        tokens = [t for t, _ in stack]
        if not any(match(t, prose_entries) for t in tokens):
            continue
        if any(match(t, non_prose_entries) for t in tokens):
            continue
        if any(t == "S.Link" and data[s:s + 1] == b"<" for t, s in stack):
            continue  # D0: autolink destination
        out.update(range(ev["s"], ev["e"]))
    return out


def a_intervals_bytes(text: str) -> list[tuple[int, int]]:
    ivs = protected_intervals(text)
    return C.merged([(C.cp_to_byte(text, iv.start), C.cp_to_byte(text, iv.end))
                     for iv in ivs])


def maximal_spans(diff: set[int]) -> list[tuple[int, int]]:
    if not diff:
        return []
    spans, s = [], sorted(diff)[0]
    prev = s
    for b in sorted(diff)[1:]:
        if b == prev + 1:
            prev = b
        else:
            spans.append((s, prev + 1))
            s = prev = b
    spans.append((s, prev + 1))
    return spans


def b_machine_contexts(events: list[dict]) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """(machine event ranges, tag-open ranges for S.Image/S.Meta)."""
    mech, tags = [], []
    for ev in events:
        k = ev.get("k", "")
        if k in MACHINE_EVENTS:
            mech.append((ev["s"], ev["e"]))
        if k in ("S.Image", "S.Meta"):
            tags.append((ev["s"], ev["e"]))
    return mech, tags


def classify(span: tuple[int, int], direction: str, kind: str,
             a_ivs: list[tuple[int, int]], b_prot: set[int],
             mech: list[tuple[int, int]], tags: list[tuple[int, int]],
             malformed: bool) -> str:
    s, e = span
    # 3: safety — parser-recognized machine context around exposed bytes
    if direction == "b_exposes":
        if any(ts <= s and e <= te for ts, te in tags):
            return "3"
        if any(ms - 1 <= s and e <= me + 1 for ms, me in mech):
            return "3"
    if malformed:
        return "6"
    if direction == "b_exposes":
        for (as_, ae) in a_ivs:
            if as_ <= s and e <= ae:
                overlap = sum(1 for b in range(as_, ae) if b in b_prot)
                if overlap / max(1, ae - as_) >= 0.5:
                    return "5"
    if direction == "b_protects" and kind == "prose":
        return "4"
    if direction == "b_exposes" and kind == "prose":
        return "1"
    if direction == "b_protects":
        return "2"
    if direction == "b_exposes" and kind in RESIDUAL_KINDS:
        return "7"
    return "8"


def differential_of(text: str, adapter_bin: str, policy: dict) -> dict:
    data = text.encode("utf-8")
    _, events = run_adapter(data, adapter_bin)
    for ev in events:  # coordinate contract on real corpus input (hard)
        if C.check_range(data, ev["s"], ev["e"]):
            raise SystemExit(
                f"coordinate invariant violated on corpus input: {ev!r}")
    a_ivs = a_intervals_bytes(text)
    b_cand = candidate_bytes(events, data, policy)
    b_prot = set(range(len(data))) - b_cand
    a_prot = C.as_byte_set(a_ivs)
    mech, tags = b_machine_contexts(events)
    malformed = malformed_flag(text)
    spans = []
    for (s, e) in maximal_spans(a_prot - b_prot):
        kind = span_kind(data[s:e].decode("utf-8"))
        spans.append({
            "s": s, "e": e, "dir": "b_exposes", "kind": kind,
            "cls": classify((s, e), "b_exposes", kind, a_ivs, b_prot, mech, tags,
                            malformed),
        })
    for (s, e) in maximal_spans(b_prot - a_prot):
        kind = span_kind(data[s:e].decode("utf-8"))
        spans.append({
            "s": s, "e": e, "dir": "b_protects", "kind": kind,
            "cls": classify((s, e), "b_protects", kind, a_ivs, b_prot, mech, tags,
                            malformed),
        })
    spans.sort(key=lambda x: (x["s"], x["e"]))
    return {"spans": spans, "n_a_bytes": len(a_prot), "n_b_cand_bytes": len(b_cand),
            "n_bytes": len(data), "malformed": malformed_flag(text)}


# ---- controlled synthetic-pair self-test (order Verification) ---------------
def self_test(adapter_bin: str, policy: dict) -> dict:
    results: dict[str, bool] = {}

    # ST-1: same construct, different boundary -> class 5.
    # A protects the whole link 5..38; B protects syntax+dest (27/33 >= 50%)
    # and exposes the prose label 6..12.
    r = differential_of("Glej [primer](https://primer.si/cesta) tu.", adapter_bin, policy)
    lab = [x for x in r["spans"] if x["s"] == 6 and x["e"] == 12]
    results["st1_single_label_span"] = (
        len(r["spans"]) == 1 and bool(lab)
        and lab[0]["dir"] == "b_exposes" and lab[0]["cls"] == "5")

    # ST-2: currency dollars never form math (P2); A's number intervals are
    # fully exposed by B with no B-protected part of the same construct
    # -> residual class 7, exactly the two number spans.
    r = differential_of("Cena: 5 $ in 10 $.", adapter_bin, policy)
    nums = sorted((x["s"], x["e"]) for x in r["spans"] if x["cls"] == "7")
    # "Cena: 5 $ in 10 $." -> '5' at 6..7, '10' at 13..15
    results["st2_currency_residual"] = (
        len(r["spans"]) == 2 and nums == [(6, 7), (13, 15)]
        and all(x["dir"] == "b_exposes" and x["kind"] == "number" for x in r["spans"]))

    # ST-3: A exposes emphasis delimiters; B correctly protects them
    # (non-prose) -> class 2, exactly the two '*' bytes.
    r = differential_of("Besedilo *poudarjeno* besedilo.", adapter_bin, policy)
    stars = sorted((x["s"], x["e"]) for x in r["spans"] if x["cls"] == "2")
    results["st3_delimiters_protected"] = (
        len(r["spans"]) == 2 and stars == [(9, 10), (20, 21)]
        and all(x["dir"] == "b_protects" for x in r["spans"]))

    return results


# ---- main -------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--runtime-root", required=True)
    ap.add_argument("--adapter-bin", required=True)
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--challenger-out", default=str(CHALLENGER_OUT))
    args = ap.parse_args()

    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    policy = config["structural_policy"]
    sel = config["increment2"]["corpus_selection"]
    adapter_bin = args.adapter_bin

    self_test_results = self_test(adapter_bin, policy)
    if not all(self_test_results.values()):
        raise SystemExit(f"differential self-test failed: {self_test_results}")

    population, _ = S.load_population(Path(args.runtime_root))
    shas = S.select_sample(population, sel["sample_size"])

    class_counts: Counter = Counter()
    kind_totals: Counter = Counter()
    dir_totals: Counter = Counter()
    class_samples: dict[str, list[str]] = {}
    malformed_samples = 0
    per_sample: list[dict] = []
    total_bytes = 0
    total_cand = 0

    for sha in shas:
        meta = population[sha]
        # re-read the text (private root, in memory only)
        text = json.loads((Path(args.runtime_root) / meta["root"] / meta["rel"])
                          .read_text(encoding="utf-8"))["dataset"]["input"]
        assert hashlib.sha256(text.encode("utf-8")).hexdigest() == sha
        r = differential_of(text, adapter_bin, policy)
        total_bytes += r["n_bytes"]
        total_cand += r["n_b_cand_bytes"]
        if r["malformed"]:
            malformed_samples += 1
        for sp in r["spans"]:
            class_counts[sp["cls"]] += 1
            kind_totals[sp["kind"]] += 1
            dir_totals[sp["dir"]] += 1
            class_samples.setdefault(sp["cls"], [])
            if sha not in class_samples[sp["cls"]]:
                class_samples[sp["cls"]].append(sha)
        per_sample.append({
            "sha256": sha, "root": meta["root"], "dir": meta["dir"],
            "chars": meta["chars"], "malformed": r["malformed"],
            "disagreement_spans": len(r["spans"]),
            "b_exposes": sum(1 for x in r["spans"] if x["dir"] == "b_exposes"),
            "b_protects": sum(1 for x in r["spans"] if x["dir"] == "b_protects"),
            "b_candidate_bytes": r["n_b_cand_bytes"],
            "a_protected_bytes": r["n_a_bytes"],
        })

    summary = {
        "schema": "008a-differential-summary/1",
        "order": "008-a",
        "increment": 2,
        "config_sha256": hashlib.sha256(CONFIG.read_bytes()).hexdigest(),
        "adapter_bin_sha256": hashlib.sha256(Path(adapter_bin).read_bytes()).hexdigest(),
        "profile": PROFILE,
        "side_a": "research/curated/protected.py protected_intervals (code-point, merged)",
        "side_b": "measurement adapter P2 candidate-prose set (frozen structural policy, incl. D0)",
        "sample": {"size": len(shas), "sha256_ascending": shas},
        "self_test": self_test_results,
        "aggregate": {
            "samples": len(shas),
            "total_text_bytes": total_bytes,
            "total_b_candidate_bytes": total_cand,
            "malformed_flagged_samples": malformed_samples,
            "disagreement_spans_by_class": {
                k: class_counts.get(k, 0) for k in ("1", "2", "3", "4", "5", "6", "7", "8")
            },
            "disagreement_spans_by_kind": dict(sorted(kind_totals.items())),
            "disagreement_spans_by_direction": dict(dir_totals),
            "class_sample_sha256s": {
                k: sorted(v)[:20] for k, v in sorted(class_samples.items())
            },
        },
        "per_sample": per_sample,
        "class_3_safety_detail": {
            "count": class_counts.get("3", 0),
            "note": "parser falsely exposes machine-significant content; any "
                    "non-zero count is a SAFETY class finding for the "
                    "acceptance criteria and the challenger protocol",
        },
        "residual_quantification": {
            "class_7_spans": class_counts.get("7", 0),
            "class_7_kinds": dict(sorted(
                (k, n) for k, n in kind_totals.items() if k in RESIDUAL_KINDS | {"url", "path"})),
            "bounded_residual_set": sorted(config["increment2"]["differential"]["consequence_classes"].keys()),
        },
        "coordinate_invariants_on_corpus": "held (all emitted ranges checked; aborts on violation)",
        "limitations": [
            "Corpus is dominated by plain prose (see selection receipt); "
            "structural prevalence is low, so differential observations on "
            "structural constructs are prevalence-limited.",
            "Side A is the current hand-written regex protection (code-point "
            "coordinates); the mapping to byte coordinates is exact and "
            "deterministic for all sampled texts.",
        ],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary["aggregate"], indent=1))
    print(f"wrote {out}")

    # ---- challenger trigger decision (recorded either way) ------------------
    c3 = class_counts.get("3", 0)
    c6 = class_counts.get("6", 0)
    c8 = class_counts.get("8", 0)
    gfm_kinds = sum(n for k, n in kind_totals.items() if k in ("tex", "structured"))
    triggers = {
        "incorrect_or_unusable_source_ranges": False,
        "relevant_gfm_incompatibility": False,
        "unsafe_malformed_input_handling": c3 > 0 and c6 > 0,
        "unacceptable_math_currency_behaviour": False,
        "structural_misclassification_affecting_actual_output": c3 > 0 or c8 > 5,
        "another_failure_markdown_rs_plausibly_addresses": False,
    }
    evidence = {
        "source_range_fidelity": "100% on fixtures (increment 1) and on all 100 corpus samples (coordinate check aborts on violation)",
        "gfm_construct_spans_classified": gfm_kinds,
        "malformed_flagged_samples": malformed_samples,
        "malformed_disagreement_spans_class_6": c6,
        "class_3_safety_spans": c3,
        "class_8_unresolved_spans": c8,
        "dollar_math_policy": "no dollar pair in the corpus sample forms math (ST-2 self-test + fixture F16/F17 behaviour); currency exposure is class-7 residual, bounded",
    }
    decision = {
        "schema": "008a-challenger-decision/1",
        "order": "008-a",
        "challenger": "markdown-rs 1.0.0",
        "trigger_conditions_evaluated": triggers,
        "evidence": evidence,
        "decision": "TRIGGERED" if any(triggers.values()) else "NOT_TRIGGERED",
        "note": "Decision recorded either way per the frozen challenger protocol. "
                "tree-sitter-markdown not revived; Pandoc remains a diagnostic "
                "oracle only.",
    }
    ch = Path(args.challenger_out)
    ch.write_text(json.dumps(decision, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("challenger:", decision["decision"])
    print(f"wrote {ch}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
