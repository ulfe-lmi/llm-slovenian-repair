"""008-c end-to-end invariants 1-7 (order requirement 9).

Runs the real frozen research pipeline (``pipeline.prepare`` /
``pipeline.replay`` with the frozen detector, English-eligibility policy,
post-review gate and patching) over committed development documents and
proves, with a scripted reviewer placed at the HTTP boundary (a fake
reviewer response document parsed by the real ``review.parse_proposal``;
zero network, zero model calls, per S-EVIDENCE-01):

  1. candidate detector input cannot include protected source ranges;
  2. local n-gram/context windows do not bridge across protected spans
     (dual of detector._between_is_open: an open token pair has no
     protected interval strictly between it, so no bigram/trigram key
     spanning a protected span may appear in any candidate evidence);
  3. reviewer targets cannot originate inside protected spans;
  4. accepted repair patches cannot overlap protected spans;
  5. every protected original substring remains byte/code-point identical
     after the complete repair path;
  6. prose immediately adjacent to protected content remains repairable
     (a seeded error word inserted at the end of a prose region directly
     preceding a protected region is a candidate, is repaired by the
     scripted reviewer through both frozen gates, and the edit survives);
  7. zero eligible prose yields zero linguistic-review work (conditional
     over all dev documents plus a synthetic all-protected document).

The self-corpus n-gram index (unigram/bigram/trigram/middle counts) is
derived deterministically from the dev documents themselves; the
English-eligibility lookup is a fixed deterministic attestation table
(a pipeline input seam, not the object under test). The invariants are
mode-agnostic: they hold under the parser-first path and under the
fail-closed legacy fallback alike.

Committed output (data-free): results/increment3/e2e-invariants.json -
counts, ids, booleans, and the synthetic seeding words only; no document
text, no private paths.

Usage:
  python3 -B end_to_end_invariants.py [--helper <path>]
      [--dev-corpus <dir>] [--out <dir>] [--replay-count N]
      [--seed-count N] [--corpus-docs N] [--no-full-zero-check]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))  # repository root

from research.curated import pipeline  # noqa: E402
from research.curated import prose_boundary as PB  # noqa: E402
from research.curated.corpus import Corpus  # noqa: E402
from research.curated.detector import tokenize  # noqa: E402
from research.curated.protected import Interval, is_protected  # noqa: E402
from research.curated.review import parse_proposal  # noqa: E402

ROOT = HERE.parent
DEFAULT_CORPUS = ROOT / "corpus"
DEFAULT_OUT = ROOT / "results" / "increment3"

# The detector word pattern (kept identical to detector.WORD_RE).
WORD_RE = re.compile(r"[^\W\d_]+(?:['’\-][^\W\d_]+)*", re.UNICODE)

# Seeding words (project-authored synthetic material, safe to commit).
ERROR_WORD = "xyzzyplugh"

# Fixed deterministic English attestation seam (zipf >= 3.0 attested).
_ENGLISH_ATTESTED = frozenset(
    """
    the of and to in is you that it he was for on are as with his they at be
    this have from or one by word not if but what all were we when your can
    said there use an each which she do how their i will up other about out
    many then them these so some her would make like him into time has look
    two more write go see number no way could people my than first water
    been call who oil its now find long down day did get come made may part
    """.split()
)


def english_lookup(word: str) -> float:
    """Deterministic attestation seam: 5.0 attested, 0.0 not attested."""
    return 5.0 if word in _ENGLISH_ATTESTED else 0.0


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, obj: dict) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(obj, ensure_ascii=False, indent=1) + "\n"
    path.write_text(payload, encoding="utf-8")
    return sha256_bytes(payload.encode("utf-8"))


def load_dev_documents(corpus: Path) -> list[tuple[str, str, dict]]:
    """(doc_id, text, label) for every committed dev document, sorted."""
    out: list[tuple[str, str, dict]] = []
    for path in sorted((corpus / "documents-dev").glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        label = json.loads((corpus / "labels-dev" / path.name).read_text(encoding="utf-8"))
        out.append((doc["doc_id"], doc["document"], label))
    out.sort(key=lambda item: item[0])
    return out


# ---------------------------------------------------------------------------
# self-corpus n-gram index (deterministic; same schema as the frozen index)
# ---------------------------------------------------------------------------
def build_self_corpus(texts: Sequence[str], path: Path) -> tuple[dict, Counter]:
    uni: Counter = Counter()
    bi: Counter = Counter()
    tri: Counter = Counter()
    mid: Counter = Counter()
    for text in texts:
        keys = [m.group(0).casefold() for m in WORD_RE.finditer(text)]
        for k in keys:
            uni[k] += 1
        for a, b in zip(keys, keys[1:]):
            bi[f"{a} {b}"] += 1
        for a, b, c in zip(keys, keys[1:], keys[2:]):
            tri[f"{a} {b} {c}"] += 1
            mid[(a, c, b)] += 1
    if path.exists() or path.is_symlink():
        path.unlink()
    connection = sqlite3.connect(path)
    try:
        connection.executescript(
            "CREATE TABLE unigram(word TEXT PRIMARY KEY, count INTEGER NOT NULL);"
            "CREATE TABLE bigram(phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);"
            "CREATE TABLE trigram(phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);"
            "CREATE TABLE middle(left_word TEXT, right_word TEXT, middle_word TEXT, count INTEGER, "
            "PRIMARY KEY(left_word,right_word,middle_word));"
        )
        connection.executemany("INSERT INTO unigram VALUES (?, ?)", sorted(uni.items()))
        connection.executemany("INSERT INTO bigram VALUES (?, ?)", sorted(bi.items()))
        connection.executemany("INSERT INTO trigram VALUES (?, ?)", sorted(tri.items()))
        connection.executemany(
            "INSERT INTO middle VALUES (?, ?, ?, ?)",
            [(left, right, middle, count) for (left, right, middle), count in sorted(mid.items())],
        )
        connection.commit()
    finally:
        connection.close()
    identity = {
        "documents": len(texts),
        "unigrams": len(uni),
        "bigrams": len(bi),
        "trigrams": len(tri),
        "middle_rows": len(mid),
    }
    return identity, uni


def choose_replacement(uni: Counter) -> str:
    """Deterministic replacement word: most frequent plain alphabetic
    unigram key of length 4-12 with count >= 200 (tie: lexicographic)."""
    pool = [
        (k, c)
        for k, c in uni.items()
        if 4 <= len(k) <= 12
        and c >= 200
        and k[0].isalpha()
        and k[-1].isalpha()
        and all(ch.isalpha() for ch in k)
    ]
    if not pool:
        raise SystemExit("no deterministic replacement candidate in the self-corpus")
    pool.sort(key=lambda kv: (-kv[1], kv[0]))
    return pool[0][0]


# ---------------------------------------------------------------------------
# scripted reviewer at the HTTP boundary (S-EVIDENCE-01)
# ---------------------------------------------------------------------------
def http_response_document(text: str) -> dict:
    """The exact reviewer HTTP response shape the transport boundary parses."""
    return {
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": text}],
            }
        ]
    }


def scripted_proposal(target_text: str, replacement: str | None):
    """A scripted reviewer decision delivered as a raw HTTP response
    document and validated by the real ``review.parse_proposal`` (fake at
    the HTTP boundary; zero network, zero model calls)."""
    if replacement is not None:
        payload = {"keep": False, "replacement": replacement, "needs_wider_edit": False}
    else:
        payload = {"keep": True, "replacement": None, "needs_wider_edit": False}
    return parse_proposal(http_response_document(json.dumps(payload, ensure_ascii=False)))


# ---------------------------------------------------------------------------
# seeding: an error word in prose adjacent to a protected region
# ---------------------------------------------------------------------------
def seed_adjacent_error(text: str, label: dict) -> tuple[str, int, int] | None:
    """Insert ERROR_WORD at the end of the first PROSE region that directly
    precedes a PROTECTED region. Returns (new_text, err_start_cp, err_end_cp).

    The separator keeps the word at the end of a prose line and never
    fuses it with the protected opener, so the parse around the insertion
    is unchanged apart from the extra word."""
    regions = sorted(label["regions"], key=lambda r: r["start_cp"])
    for prev, nxt in zip(regions, regions[1:]):
        if (
            prev["role"] == "PROSE"
            and nxt["role"] == "PROTECTED"
            and prev["end_cp"] == nxt["start_cp"]
            and nxt["end_cp"] > nxt["start_cp"]
        ):
            ins = prev["end_cp"]
            if ERROR_WORD in text:
                return None
            sep = "" if text[ins] in "\n \t" else "\n"
            new_text = text[:ins] + " " + ERROR_WORD + sep + text[ins:]
            err_start = ins + 1
            return new_text, err_start, err_start + len(ERROR_WORD)
    return None


def _bridged(left: int, right: int, ivs: list[Interval]) -> bool:
    """Dual of detector._between_is_open: True iff a protected interval
    lies strictly between the two token endpoints."""
    return any(left <= item.start < right and item.end > left for item in ivs)


# ---------------------------------------------------------------------------
# invariant runner
# ---------------------------------------------------------------------------
def run_invariants(
    dev_root: Path,
    helper: Path | None,
    *,
    replay_count: int = 40,
    seed_count: int = 5,
    corpus_docs: int | None = None,
    full_zero_check: bool = True,
    scratch: Path,
) -> dict:
    scratch.mkdir(parents=True, exist_ok=True)
    docs = load_dev_documents(dev_root)
    corpus_texts = [text for _id, text, _label in (docs[:corpus_docs] if corpus_docs else docs)]
    index_path = scratch / "self-corpus.sqlite"
    corpus_identity, uni = build_self_corpus(corpus_texts, index_path)
    replacement = choose_replacement(uni)

    flags = {
        "1_detector_input_outside_protected": True,
        "2_ngram_windows_no_bridge": True,
        "3_review_targets_outside_protected": True,
        "4_accepted_edits_outside_protected": True,
        "5_protected_substrings_identical_after_path": True,
        "6_adjacent_prose_repairable": True,
        "7_zero_eligible_zero_review_work": True,
    }
    mode: str | None = None

    def _ivs(text: str) -> tuple[list[Interval], str]:
        result = PB.protection_with_status(text, helper_path=helper)
        return [Interval(s, e, r) for s, e, r in result.intervals], result.mode

    def _check_doc(text: str) -> int:
        nonlocal mode
        ivs, doc_mode = _ivs(text)
        if mode is None:
            mode = doc_mode
        elif mode != doc_mode:
            raise SystemExit(f"protection mode not uniform across documents: {mode} != {doc_mode}")
        # I1: independent token census (words overlapping a protected
        # interval are absent from the detector input; all other words
        # are present).
        raw_words = list(WORD_RE.finditer(text))
        tokens = tokenize(text, ivs)
        token_set = {(t.start, t.end) for t in tokens}
        for m in raw_words:
            overlaps = any(m.start() < iv.end and m.end() > iv.start for iv in ivs)
            present = (m.start(), m.end()) in token_set
            if overlaps == present:
                flags["1_detector_input_outside_protected"] = False
        prepared = pipeline.prepare(text, corpus, english_lookup)
        candidates = prepared["candidates"]
        english = prepared["english"]
        # I3: candidates (detector output) and, in particular, the
        # review targets (eligible after the English policy) originate
        # outside protected spans.
        for cand in candidates:
            if is_protected(int(cand["start"]), int(cand["end"]), ivs):
                flags["3_review_targets_outside_protected"] = False
        for cand, policy in zip(candidates, english):
            if policy["review_suppressed"]:
                continue
            if is_protected(int(cand["start"]), int(cand["end"]), ivs):
                flags["3_review_targets_outside_protected"] = False
        # I2: no n-gram context window bridges a protected span.
        cand_by_pos = {(int(c["start"]), int(c["end"])): c for c in candidates}
        for idx, tok in enumerate(tokens):
            cand = cand_by_pos.get((tok.start, tok.end))
            if cand is None:
                continue
            ev = cand["evidence"]
            if idx > 0:
                left = tokens[idx - 1]
                if _bridged(left.end, tok.start, ivs):
                    if ev.get("left_bigram", {}).get("key") == f"{left.key} {tok.key}":
                        flags["2_ngram_windows_no_bridge"] = False
                    if idx + 1 < len(tokens) and ev.get("trigram", {}).get("key") == (
                        f"{left.key} {tok.key} {tokens[idx + 1].key}"
                    ):
                        flags["2_ngram_windows_no_bridge"] = False
            if idx + 1 < len(tokens):
                right = tokens[idx + 1]
                if _bridged(tok.end, right.start, ivs):
                    if ev.get("right_bigram", {}).get("key") == f"{tok.key} {right.key}":
                        flags["2_ngram_windows_no_bridge"] = False
                    if idx > 0 and ev.get("trigram", {}).get("key") == (
                        f"{tokens[idx - 1].key} {tok.key} {right.key}"
                    ):
                        flags["2_ngram_windows_no_bridge"] = False
        # scripted reviewer: every non-suppressed candidate gets a raw
        # HTTP response document (keep) parsed by the real parser.
        proposals = {
            str(int(c["start"])): scripted_proposal(str(c["text"]), None)
            for c, policy in zip(candidates, english)
            if not policy["review_suppressed"]
        }
        result = pipeline.replay(text, corpus, english_lookup, proposals)
        # I4: accepted edits never overlap protected spans.
        for start, end, _rep in result["edits"]:
            if is_protected(start, end, ivs):
                flags["4_accepted_edits_outside_protected"] = False
        # I5: every protected original substring is identical after the
        # complete repair path (independent shift re-derivation).
        ordered = sorted(result["edits"])
        for iv in ivs:
            if iv.end > len(text):
                continue
            shift = sum(len(rep) - (ee - es) for es, ee, rep in ordered if ee <= iv.start)
            if result["output"][iv.start + shift:iv.start + shift + (iv.end - iv.start)] != text[iv.start:iv.end]:
                flags["5_protected_substrings_identical_after_path"] = False
        # I7 (conditional): zero eligible prose -> zero review work.
        if prepared["eligible_words"] == 0 and (candidates or result["review_calls"] != 0):
            flags["7_zero_eligible_zero_review_work"] = False
        return 1 if prepared["eligible_words"] == 0 else 0

    with Corpus(index_path) as corpus:
        zero_eligible_docs = 0
        selected = []
        replayed_ids: list[str] = []
        for doc_id, text, label in docs:
            ivs, _m = _ivs(text)
            if not any(iv.end > iv.start for iv in ivs):
                continue
            if not tokenize(text, ivs):
                continue
            selected.append((doc_id, text, label))
            if len(replayed_ids) < replay_count:
                zero_eligible_docs += _check_doc(text)
                replayed_ids.append(doc_id)

        if full_zero_check:
            replayed_set = set(replayed_ids)
            for doc_id, text, label in docs:
                if doc_id in replayed_set:
                    continue
                ivs, _m = _ivs(text)
                if not tokenize(text, ivs):
                    continue
                prepared = pipeline.prepare(text, corpus, english_lookup)
                if prepared["eligible_words"] == 0:
                    zero_eligible_docs += 1
                    if prepared["candidates"]:
                        flags["7_zero_eligible_zero_review_work"] = False

        # I6: seeded error word adjacent to protected content.
        seeded = []
        for doc_id, text, label in docs:
            if len(seeded) >= seed_count:
                break
            seeded_doc = seed_adjacent_error(text, label)
            if seeded_doc is None:
                continue
            new_text, err_start, err_end = seeded_doc
            ivs, _m = _ivs(new_text)
            # strict adjacency: a protected interval starts exactly where
            # the error word ends (mode-agnostic definition).
            if not any(iv.start == err_end for iv in ivs):
                continue
            prepared = pipeline.prepare(new_text, corpus, english_lookup)
            err_cands = [c for c in prepared["candidates"] if c["text"] == ERROR_WORD]
            if not err_cands:
                flags["6_adjacent_prose_repairable"] = False
                continue
            proposals = {}
            for cand, policy in zip(prepared["candidates"], prepared["english"]):
                if policy["review_suppressed"]:
                    continue
                is_err = cand["text"] == ERROR_WORD
                proposals[str(int(cand["start"]))] = scripted_proposal(
                    str(cand["text"]), replacement if is_err else None
                )
            result = pipeline.replay(new_text, corpus, english_lookup, proposals)
            edited_error = any(
                s <= err_start and e >= err_end for s, e, _rep in result["edits"]
            )
            error_removed = ERROR_WORD not in result["output"]
            # I4/I5 on the seeded document as well.
            ordered = sorted(result["edits"])
            for s, e, _rep in result["edits"]:
                if is_protected(s, e, ivs):
                    flags["4_accepted_edits_outside_protected"] = False
            for iv in ivs:
                if iv.end > len(new_text):
                    continue
                shift = sum(len(rep) - (ee - es) for es, ee, rep in ordered if ee <= iv.start)
                if result["output"][iv.start + shift:iv.start + shift + (iv.end - iv.start)] != new_text[iv.start:iv.end]:
                    flags["5_protected_substrings_identical_after_path"] = False
            if not (edited_error and error_removed and result["edits"]):
                flags["6_adjacent_prose_repairable"] = False
            seeded.append({
                "doc_id": doc_id,
                "error_word": ERROR_WORD,
                "replacement": replacement,
                "edit_applied": bool(edited_error and error_removed),
            })
        if not seeded:
            raise SystemExit("no seedable prose/protected adjacency in the dev corpus")

        # I7 (zero branch exercised for real): synthetic all-protected
        # document (fence only; zero prose tokens in both modes).
        synthetic = "```\nabc123 def_gh\n```\n"
        prepared_s = pipeline.prepare(synthetic, corpus, english_lookup)
        synthetic_ok = (
            prepared_s["eligible_words"] == 0
            and prepared_s["candidates"] == []
            and prepared_s["english"] == []
        )
        if not synthetic_ok:
            flags["7_zero_eligible_zero_review_work"] = False

    if mode is None:
        raise SystemExit("no dev document with protected content and prose")
    report = {
        "schema": "008c-e2e-invariants/1",
        "order": "008-c",
        "label": "dev-corpus tuning evidence, NOT acceptance",
        "protection_mode": mode,
        "helper_sha256": sha256_bytes(Path(helper).read_bytes()) if helper else None,
        "self_corpus": corpus_identity,
        "reviewer": "scripted reviewer at the HTTP boundary: raw response "
                    "documents parsed by review.parse_proposal; zero "
                    "network, zero model calls (S-EVIDENCE-01)",
        "documents": {
            "dev_total": len(docs),
            "with_protected_and_prose": len(selected),
            "replayed": len(replayed_ids),
            "zero_eligible_documents": zero_eligible_docs,
            "full_zero_check": full_zero_check,
        },
        "invariants": flags,
        "seeded": seeded,
        "synthetic_zero_eligible": {
            "eligible_words": prepared_s["eligible_words"],
            "candidates": len(prepared_s["candidates"]),
            "ok": synthetic_ok,
        },
        "all_pass": all(flags.values()) and bool(seeded),
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--helper", type=Path, default=None,
                        help="pinned helper (default: auto-discovery; absence "
                             "exercises the fail-closed fallback mode)")
    parser.add_argument("--dev-corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--replay-count", type=int, default=40)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--corpus-docs", type=int, default=None,
                        help="dev documents feeding the self-corpus "
                             "(default: all)")
    parser.add_argument("--no-full-zero-check", action="store_true",
                        help="skip the zero-eligible condition over all dev "
                             "documents")
    args = parser.parse_args()

    helper = Path(args.helper).resolve() if args.helper else PB.find_helper()
    if helper is not None:
        os.environ[PB.HELPER_ENV_VAR] = str(helper)
    else:
        os.environ.pop(PB.HELPER_ENV_VAR, None)

    import tempfile

    with tempfile.TemporaryDirectory(prefix="008c-e2e-") as td:
        report = run_invariants(
            Path(args.dev_corpus).resolve(),
            helper,
            replay_count=args.replay_count,
            seed_count=args.seed_count,
            corpus_docs=args.corpus_docs,
            full_zero_check=not args.no_full_zero_check,
            scratch=Path(td),
        )
    out = Path(args.out).resolve()
    sha = write_json(out / "e2e-invariants.json", report)
    print(json.dumps({
        "file": str(out / "e2e-invariants.json"),
        "sha256": sha,
        "protection_mode": report["protection_mode"],
        "invariants": report["invariants"],
        "all_pass": report["all_pass"],
    }, indent=1))
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
