"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

Actual-boundary tests for zero-count local support (order 027-a,
requirement 1) and composed-result validation of individually accepted
edits (order 027-a, requirements 3-8).

Native real boundaries under test: real read-only SQLite (synthetic
owned databases), the real detector/acceptance/engine/proxy code, the
installed qualified Pandoc and, for the round-trip class, the real
ResponsesReviewer over owned loopback-0 HTTP.  Only the reviewer object
(direct-engine classes), the main/review HTTP endpoints and - in the two
disclosed multiword cases - the detector's candidate list are synthetic
upstream of those boundaries; the corpus, its queries, acceptance, the
composed-validation pass, the engine/proxy paths and the native SQLite
adapter are never faked.  No live model, corpus, network or quality
claim (order 027-a, requirement 9).
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import sqlite3
import sys
import tempfile
import unittest
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Protocol, cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import composed_validation  # noqa: E402
import config  # noqa: E402
import proxy  # noqa: E402
from batch_review import (  # noqa: E402
    BatchProposal,
    BatchResult,
    BatchTarget,
    BatchUsage,
)
from composed_validation import (  # noqa: E402
    COMPOSED_MAPPING_UNPROVABLE,
    COMPOSED_REJECTED,
    ComposedMappingError,
    ComposedRecord,
    validate_composed,
)
from detector import Candidate  # noqa: E402
from detector import detect as _real_detect  # noqa: E402
from protected import Interval  # noqa: E402
from qwen_client import Proposal  # noqa: E402
from repair import Acceptance  # noqa: E402
from repair import accept as _real_accept  # noqa: E402
from runtime_corpus import REASON_BUDGET_EXCEEDED, RuntimeCorpus  # noqa: E402
from tests.test_responses_contract import (  # noqa: E402
    _Harness,
    _json_completed,
    _MainUpstream,
    _review_payload,
)
from tests.test_review_batch import (  # noqa: E402
    _contract_body,
    _FakeUpstream,
    _prop,
    _real_spec,
    _tc_baseline,
)

from corpus import Corpus, Evidence  # noqa: E402

COMPOSED_TEXT = "to wone je"


def _index_state(root: Path, db: Path) -> tuple[str, list[str]]:
    """DB byte hash plus any journal/wal/shm sidecar names next to it."""
    names = sorted(
        p.name for p in root.iterdir() if p.name.startswith(db.name + "-")
    )
    return hashlib.sha256(db.read_bytes()).hexdigest(), names


def _sub_mapping(detail: Mapping[str, object], key: str) -> dict[str, object]:
    value = detail[key]
    if not isinstance(value, dict):
        raise AssertionError(f"detail {key!r} is not a mapping")
    return cast("dict[str, object]", value)


def _composed_db(
    root: Path,
    unigrams: Mapping[str, int],
    bigrams: Mapping[str, int],
    name: str = "composed.sqlite",
) -> Path:
    """One synthetic read-only evidence index (5 tables, tiny lexicon)."""
    db = root / name
    connection = sqlite3.connect(db)
    connection.executescript(
        """
        CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE unigram (word TEXT PRIMARY KEY, count INTEGER NOT NULL);
        CREATE TABLE bigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
        CREATE TABLE trigram (phrase TEXT PRIMARY KEY, count INTEGER NOT NULL);
        CREATE TABLE middle (left_word TEXT, right_word TEXT, middle_word TEXT, count INTEGER,
            PRIMARY KEY(left_word,right_word,middle_word));
        """
    )
    for word, count in unigrams.items():
        connection.execute("INSERT INTO unigram VALUES (?,?)", (word, count))
    for phrase, count in bigrams.items():
        table = "bigram" if len(phrase.split()) == 2 else "trigram"
        connection.execute(f"INSERT INTO {table} VALUES (?,?)", (phrase, count))
    connection.commit()
    connection.close()
    return db


class _BatchReviewer(Protocol):
    """The structural reviewer surface the engine calls (proxy.Reviewer)."""

    calls: int

    def review_batch(
        self, sentence: str, targets: tuple[BatchTarget, ...]
    ) -> BatchResult: ...


class _SpecReviewer:
    """Synthetic reviewer standing in for the review worker.

    It counts actual review_batch calls, records each (sentence, targets)
    pair and answers per target text: a kept target stays, every other
    target receives its mapped replacement (or none).  The engine,
    corpus, acceptance and composed-validation code around it are real.
    """

    def __init__(
        self,
        replacements: Mapping[str, str],
        *,
        keep: frozenset[str] = frozenset(),
        usage: bool = True,
    ) -> None:
        self.replacements = dict(replacements)
        self.keep = keep
        self.usage_on = usage
        self.calls = 0
        self.sent: list[tuple[str, tuple[BatchTarget, ...]]] = []

    def review_batch(
        self, sentence: str, targets: tuple[BatchTarget, ...]
    ) -> BatchResult:
        self.calls += 1
        self.sent.append((sentence, targets))
        proposals: dict[str, BatchProposal] = {}
        for target in targets:
            if target.target in self.keep:
                proposals[target.id] = BatchProposal(
                    target.id, True, None, False
                )
            else:
                proposals[target.id] = BatchProposal(
                    target.id, False, self.replacements.get(target.target), False
                )
        return BatchResult(
            proposals, BatchUsage(10, 20, 30) if self.usage_on else None
        )


class _CloseTrackingCorpus(RuntimeCorpus):
    """Call-through adapter recording actual close calls (ownership)."""

    def __init__(self, path: str | Path) -> None:
        super().__init__(path)
        self.close_calls = 0

    def close(self) -> None:
        self.close_calls += 1
        super().close()


class _KeySpyCorpus(RuntimeCorpus):
    """Call-through adapter recording every exact ngram key actually
    queried (disclosed observation; every query still executes)."""

    def __init__(self, path: str | Path) -> None:
        super().__init__(path)
        self.ngram_keys: list[tuple[str, int]] = []

    def ngram(self, phrase: str, length: int) -> Evidence:
        self.ngram_keys.append((phrase, length))
        return super().ngram(phrase, length)


def _tracked_accept_events() -> tuple[list[str], Callable[..., Acceptance]]:
    """Call-through observation of real accept decisions.

    Wraps the real repair.accept at the proxy module reference: every
    real decision is recorded as it happens and returned unchanged.  No
    acceptance, corpus or query is faked.
    """
    events: list[str] = []

    def tracked(
        text: str,
        candidate: Candidate,
        proposal: Proposal,
        corpus: Corpus,
        intervals: list[Interval],
        *,
        left: str | None = None,
        right: str | None = None,
        left_bounds: tuple[int, int] | None = None,
        right_bounds: tuple[int, int] | None = None,
    ) -> Acceptance:
        decision = _real_accept(
            text,
            candidate,
            proposal,
            corpus,
            intervals,
            left=left,
            right=right,
            left_bounds=left_bounds,
            right_bounds=right_bounds,
        )
        events.append("ACCEPTED" if decision.accepted else "REJECTED")
        return decision

    return events, tracked


def _injected_detect(
    candidates: tuple[Candidate, ...],
) -> tuple[list[tuple[str, int]], Callable[..., list[Candidate]]]:
    """Disclosed bounded detector replacement for multiword spans.

    The real detector only ever selects single-token spans, so the
    multiword-span cases cannot reach the composed pass through it.
    The wrapper still CALLS the real detector (same arguments, result
    discarded) and returns the fixed multiword candidate tuple; every
    downstream boundary - tokenize, prepare, batch, acceptance, composed
    validation, apply - is real.  ``calls`` records (mode, maximum) of
    every actual invocation.
    """
    calls: list[tuple[str, int]] = []

    def fake(
        text: str,
        corpus: Corpus,
        intervals: list[Interval] | None = None,
        *,
        mode: str = "local-context",
        threshold: int = 3,
        maximum: int = 4,
    ) -> list[Candidate]:
        calls.append((mode, maximum))
        _real_detect(
            text, corpus, intervals, mode=mode, threshold=threshold, maximum=maximum
        )
        return list(candidates)

    return calls, fake


class ZeroSupportTests(unittest.TestCase):
    """T1: an explicit EXACT(0) row is a known zero, not positive support."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_exact_zero_row_is_not_positive_support(self) -> None:
        db = _composed_db(
            self.root,
            {"to": 100, "je": 100, "wone": 2, "rone": 50},
            {"to rone": 0},
        )
        before = _index_state(self.root, db)
        reviewer = _SpecReviewer({"wone": "rone"})
        captured: list[_CloseTrackingCorpus] = []

        def tracked(path: str | Path) -> _CloseTrackingCorpus:
            corpus = _CloseTrackingCorpus(path)
            captured.append(corpus)
            return corpus

        engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
        with mock.patch.object(proxy, "RuntimeCorpus", tracked):
            engine.begin_request()
            repaired = engine.repair(COMPOSED_TEXT)
        self.assertEqual(repaired, COMPOSED_TEXT)
        self.assertEqual(reviewer.calls, 1)
        [detail] = engine.take_details()
        acceptance = detail["acceptance"]
        if not isinstance(acceptance, list) or len(acceptance) != 1:
            self.fail("expected one acceptance record")
        item = acceptance[0]
        if not isinstance(item, dict):
            self.fail("acceptance is not a mapping")
        self.assertEqual(
            item,
            {
                "accepted": False,
                "reason": "local-evidence-not-stronger",
                "replacement": None,
            },
        )
        self.assertEqual(detail["replacements"], [])
        review = _sub_mapping(detail, "review_batch")
        self.assertEqual(review["calls"], 1)
        # Schema 5 + detection 9 (3 tokens) + one acceptance 4.  No
        # composed phase: nothing was accepted.
        [corpus] = captured
        self.assertEqual(corpus._budget.statements, 18)
        self.assertEqual(corpus.close_calls, 1)
        self.assertEqual(_index_state(self.root, db), before)

    def test_adapter_retains_valid_zero_as_exact_evidence(self) -> None:
        db = _composed_db(
            self.root,
            {"to": 100, "je": 100, "wone": 2, "rone": 50},
            {"to rone": 0},
        )
        corpus = RuntimeCorpus(db)
        self.assertEqual(
            corpus.ngram("to rone", 2), Evidence("EXACT", 0, "to rone")
        )
        corpus.close()

    def test_censored_absence_stays_unknown_and_rejects(self) -> None:
        db = _composed_db(
            self.root,
            {"to": 100, "je": 100, "wone": 2, "rone": 50},
            {},
        )
        corpus = RuntimeCorpus(db)
        self.assertEqual(
            corpus.ngram("to rone", 2), Evidence("CENSORED", None, "to rone")
        )
        corpus.close()
        reviewer = _SpecReviewer({"wone": "rone"})
        captured: list[_CloseTrackingCorpus] = []

        def tracked(path: str | Path) -> _CloseTrackingCorpus:
            corpus = _CloseTrackingCorpus(path)
            captured.append(corpus)
            return corpus

        engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
        with mock.patch.object(proxy, "RuntimeCorpus", tracked):
            engine.begin_request()
            repaired = engine.repair(COMPOSED_TEXT)
        self.assertEqual(repaired, COMPOSED_TEXT)
        self.assertEqual(reviewer.calls, 1)
        [detail] = engine.take_details()
        acceptance = detail["acceptance"]
        if not isinstance(acceptance, list) or len(acceptance) != 1:
            self.fail("expected one acceptance record")
        item = acceptance[0]
        if not isinstance(item, dict):
            self.fail("acceptance is not a mapping")
        self.assertEqual(item["reason"], "local-evidence-not-stronger")
        [corpus] = captured
        self.assertEqual(corpus._budget.statements, 18)

    def test_positive_control_survives_composed_pass(self) -> None:
        db = _composed_db(
            self.root,
            {"to": 100, "je": 100, "wone": 2, "rone": 50},
            {"to rone": 20},
        )
        before = _index_state(self.root, db)
        reviewer = _SpecReviewer({"wone": "rone"})
        captured: list[_CloseTrackingCorpus] = []

        def tracked(path: str | Path) -> _CloseTrackingCorpus:
            corpus = _CloseTrackingCorpus(path)
            captured.append(corpus)
            return corpus

        engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
        with mock.patch.object(proxy, "RuntimeCorpus", tracked):
            engine.begin_request()
            repaired = engine.repair(COMPOSED_TEXT)
        self.assertEqual(repaired, "to rone je")
        self.assertEqual(reviewer.calls, 1)
        [detail] = engine.take_details()
        self.assertNotIn("evidence_failure", detail)
        acceptance = detail["acceptance"]
        if not isinstance(acceptance, list) or len(acceptance) != 1:
            self.fail("expected one acceptance record")
        item = acceptance[0]
        if not isinstance(item, dict):
            self.fail("acceptance is not a mapping")
        self.assertEqual(
            item,
            {
                "accepted": True,
                "reason": "accepted-independent-evidence",
                "replacement": "rone",
            },
        )
        self.assertEqual(detail["replacements"], ["rone"])
        # Schema 5 + detection 9 + acceptance 4 + composed re-validation
        # of the single surviving record 4 (unigram + 2 bigrams +
        # trigram): the composed pass actually re-ran the real queries.
        [corpus] = captured
        self.assertEqual(corpus._budget.statements, 22)
        self.assertEqual(corpus.close_calls, 1)
        self.assertEqual(_index_state(self.root, db), before)


class ComposedEngineTests(unittest.TestCase):
    """T2: individually accepted edits composed, then re-validated."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _db(self, unigrams: Mapping[str, int], bigrams: Mapping[str, int]) -> Path:
        return _composed_db(self.root, unigrams, bigrams)

    def _repair(
        self,
        db: Path,
        reviewer: _SpecReviewer,
        text: str,
    ) -> tuple[str, list[dict[str, object]], list[str]]:
        events, tracked = _tracked_accept_events()
        engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
        with mock.patch.object(proxy, "accept", tracked):
            engine.begin_request()
            repaired = engine.repair(text)
        return repaired, engine.take_details(), events

    def _assert_all(self, detail: Mapping[str, object], reason: str) -> None:
        acceptance = detail["acceptance"]
        if not isinstance(acceptance, list) or not acceptance:
            self.fail("expected acceptance records")
        for item in acceptance:
            if not isinstance(item, dict):
                self.fail("acceptance item is not a mapping")
            self.assertEqual(
                item, {"accepted": False, "reason": reason, "replacement": None}
            )

    def test_one_sided_group_rejects_whole(self) -> None:
        # The 026 defect shape: each edit is individually accepted, but
        # the composed result supports neither member - no winner is
        # chosen and the whole group is rebuilt from the original.
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "wtwo": 2, "one": 50, "two": 50},
            {"to one": 20, "wone two": 20},
        )
        reviewer = _SpecReviewer({"wone": "one", "wtwo": "two"})
        repaired, details, events = self._repair(db, reviewer, "to wone wtwo je")
        self.assertEqual(repaired, "to wone wtwo je")
        # Direct real-accept premise: BOTH proposals passed the actual
        # individual acceptance on the original before composed review.
        self.assertEqual(events, ["ACCEPTED", "ACCEPTED"])
        self.assertEqual(reviewer.calls, 1)
        [detail] = details
        self.assertEqual(detail["replacements"], [])
        self._assert_all(detail, COMPOSED_REJECTED)
        self.assertNotIn("evidence_failure", detail)

    def test_supported_new_neighbor_pair_survives(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "wtwo": 2, "one": 50, "two": 50},
            {"one wtwo": 20, "wone two": 20, "one two": 20},
        )
        reviewer = _SpecReviewer({"wone": "one", "wtwo": "two"})
        repaired, details, events = self._repair(db, reviewer, "to wone wtwo je")
        self.assertEqual(repaired, "to one two je")
        self.assertEqual(events, ["ACCEPTED", "ACCEPTED"])
        self.assertEqual(reviewer.calls, 1)
        [detail] = details
        self.assertEqual(detail["replacements"], ["one", "two"])
        acceptance = detail["acceptance"]
        if not isinstance(acceptance, list) or len(acceptance) != 2:
            self.fail("expected two acceptance records")
        for item in acceptance:
            if not isinstance(item, dict):
                self.fail("acceptance item is not a mapping")
            self.assertTrue(item["accepted"])

    def test_direct_support_control_survives(self) -> None:
        # Each member keeps its own direct local support in the composed
        # result as well: compatible individually supported edits stay.
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "wtwo": 2, "one": 50, "two": 50},
            {"to one": 20, "two je": 20},
        )
        reviewer = _SpecReviewer({"wone": "one", "wtwo": "two"})
        repaired, details, events = self._repair(db, reviewer, "to wone wtwo je")
        self.assertEqual(repaired, "to one two je")
        self.assertEqual(events, ["ACCEPTED", "ACCEPTED"])
        [detail] = details
        self.assertEqual(detail["replacements"], ["one", "two"])

    def test_prefix_neighbor_is_not_an_unchanged_token(self) -> None:
        # B's individual support used the original token "wone"; after A
        # replaces it with "woneplus", the changed neighbor re-enters the
        # evidence under its ACTUAL full token key - the old "wone two"
        # row (a prefix of the new token) must not count.
        db = self._db(
            {
                "to": 100,
                "je": 100,
                "wone": 2,
                "wtwo": 2,
                "woneplus": 50,
                "two": 50,
            },
            {"to woneplus": 20, "wone two": 20},
        )
        reviewer = _SpecReviewer({"wone": "woneplus", "wtwo": "two"})
        repaired, details, events = self._repair(db, reviewer, "to wone wtwo je")
        self.assertEqual(repaired, "to wone wtwo je")
        self.assertEqual(events, ["ACCEPTED", "ACCEPTED"])
        self.assertEqual(reviewer.calls, 1)
        [detail] = details
        self.assertEqual(detail["replacements"], [])
        self._assert_all(detail, COMPOSED_REJECTED)

    def test_far_compatible_pair_survives(self) -> None:
        # Non-interacting edits in different localities: each re-validates
        # against the other's composition and both survive.
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "wtwo": 2, "one": 50, "two": 50},
            {"to one": 20, "je two": 20},
        )
        reviewer = _SpecReviewer({"wone": "one", "wtwo": "two"})
        repaired, details, events = self._repair(
            db, reviewer, "to wone je wtwo je"
        )
        self.assertEqual(repaired, "to one je two je")
        self.assertEqual(events, ["ACCEPTED", "ACCEPTED"])
        [detail] = details
        self.assertEqual(detail["replacements"], ["one", "two"])

    def test_mixed_length_edits_use_original_coordinates(self) -> None:
        # Contraction (4 -> 2) and same-length edits compose on exact
        # original coordinates; the rebased member's slice must match.
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "wtwo": 2, "ro": 50, "two": 50},
            {"to ro": 20, "two je": 20},
        )
        reviewer = _SpecReviewer({"wone": "ro", "wtwo": "two"})
        repaired, details, events = self._repair(db, reviewer, "to wone wtwo je")
        self.assertEqual(repaired, "to ro two je")
        self.assertEqual(events, ["ACCEPTED", "ACCEPTED"])
        [detail] = details
        self.assertEqual(detail["replacements"], ["ro", "two"])

    def test_repeated_occurrences_get_two_ids_one_call(self) -> None:
        # The two occurrences are two targets of ONE batch call; the
        # interacting pair is validated as one group and rejected whole.
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "one": 50},
            {"to one": 20, "wone one": 20},
        )
        reviewer = _SpecReviewer({"wone": "one"})
        repaired, details, events = self._repair(db, reviewer, "to wone wone je")
        self.assertEqual(repaired, "to wone wone je")
        self.assertEqual(events, ["ACCEPTED", "ACCEPTED"])
        self.assertEqual(reviewer.calls, 1)
        sentence, targets = reviewer.sent[0]
        self.assertEqual(sentence, "to wone wone je")
        self.assertEqual([t.id for t in targets], ["t0", "t1"])
        self.assertEqual(targets[0].target, "wone")
        self.assertEqual(targets[1].target, "wone")
        [detail] = details
        self.assertEqual(detail["replacements"], [])
        self._assert_all(detail, COMPOSED_REJECTED)

    def test_multiword_adjacent_group_rejects_whole(self) -> None:
        # Two adjacent multiword spans: each span's EXTERNAL right
        # neighbor is the other span's first token, so the pair interacts
        # and the composed result supports neither member.  The injected
        # multiword candidates are disclosed in _injected_detect; the
        # decisions' recorded neighbors prove whole-span external
        # preparation (internal tokens are never external neighbors).
        db = self._db(
            {
                "to": 100,
                "je": 100,
                "wone": 2,
                "wtwo": 2,
                "wthree": 2,
                "wfour": 2,
                "one": 50,
                "two": 50,
            },
            {"to one": 20, "wtwo two": 20},
        )
        a = Candidate(3, 12, "wone wtwo", 0.5, {})
        b = Candidate(13, 25, "wthree wfour", 0.5, {})
        detect_calls, fake_detect = _injected_detect((a, b))
        events, tracked_accept = _tracked_accept_events()
        reviewer = _SpecReviewer({"wone wtwo": "one", "wthree wfour": "two"})
        engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
        with (
            mock.patch.object(proxy, "detect", fake_detect),
            mock.patch.object(proxy, "accept", tracked_accept),
        ):
            engine.begin_request()
            repaired = engine.repair("to wone wtwo wthree wfour je")
        details = engine.take_details()
        self.assertEqual(repaired, "to wone wtwo wthree wfour je")
        self.assertEqual(events, ["ACCEPTED", "ACCEPTED"])
        self.assertEqual(reviewer.calls, 1)
        self.assertEqual(detect_calls, [("local-context", 4)])
        [detail] = details
        self.assertEqual(detail["replacements"], [])
        self._assert_all(detail, COMPOSED_REJECTED)
        decisions = detail["reviewer_decisions"]
        if not isinstance(decisions, list) or len(decisions) != 2:
            self.fail("expected two reviewer decisions")
        first = cast(dict[str, object], decisions[0])
        second = cast(dict[str, object], decisions[1])
        first_neighbors = first["neighbors"]
        if not isinstance(first_neighbors, dict):
            self.fail("neighbors is not a mapping")
        second_neighbors = second["neighbors"]
        if not isinstance(second_neighbors, dict):
            self.fail("neighbors is not a mapping")
        self.assertEqual(first_neighbors, {"left": "to", "right": "wthree"})
        self.assertEqual(second_neighbors, {"left": "wtwo", "right": "je"})


class MappingBoundaryTests(unittest.TestCase):
    """T4: R6 unprovable mappings abstain the WHOLE optional pass."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_rebased_slice_mismatch_abstains(self) -> None:
        # An independently supported record S lives next to a record M
        # whose stored span text no longer equals the exact rebased
        # slice: the whole pass raises, S is not retained.
        db = _composed_db(
            self.root,
            {"to": 100, "je": 100, "wone": 100, "rone": 50, "one": 50},
            {"to one": 20, "to rone": 20},
        )
        s = ComposedRecord(1, 3, 7, "wone", "rone", "to", "je", (0, 2), (8, 10))
        m = ComposedRecord(0, 3, 7, "WONE", "one", "to", "je", (0, 2), (8, 10))
        corpus = RuntimeCorpus(db)
        try:
            with self.assertRaises(ComposedMappingError):
                validate_composed("to wone je", [m, s], corpus, [])
        finally:
            corpus.close()

    def test_rebased_missing_token_abstains(self) -> None:
        # The rebased slice matches exactly, but no actual token of the
        # validation view starts at the rebased span.
        db = _composed_db(
            self.root,
            {"to": 100, "je": 100, "wone": 100, "one": 50},
            {"to one": 20},
        )
        n = ComposedRecord(0, 2, 8, " wone ", "one", None, "je", None, (8, 10))
        corpus = RuntimeCorpus(db)
        try:
            with self.assertRaises(ComposedMappingError):
                validate_composed("to wone je", [n], corpus, [])
        finally:
            corpus.close()

    def test_rebased_out_of_range_abstains(self) -> None:
        db = _composed_db(
            self.root,
            {"to": 100, "je": 100, "wone": 100, "rone": 50},
            {"to rone": 20},
        )
        o = ComposedRecord(1, 100, 104, "wone", "rone", None, None, None, None)
        corpus = RuntimeCorpus(db)
        try:
            with self.assertRaises(ComposedMappingError):
                validate_composed("to wone je", [o], corpus, [])
        finally:
            corpus.close()

    def test_supported_record_survives_alone(self) -> None:
        db = _composed_db(
            self.root,
            {"to": 100, "je": 100, "wone": 100, "rone": 50},
            {"to rone": 20},
        )
        s = ComposedRecord(1, 3, 7, "wone", "rone", "to", "je", (0, 2), (8, 10))
        corpus = RuntimeCorpus(db)
        try:
            self.assertEqual(validate_composed("to wone je", [s], corpus, []), {0})
        finally:
            corpus.close()

    def test_ordinary_group_rejection_is_not_a_mapping_failure(self) -> None:
        # The same one-sided group that the engine rejects with
        # composed-context-rejected returns an empty survivor set HERE
        # without raising: group rejection and mapping failure are
        # distinct outcomes.
        db = _composed_db(
            self.root,
            {"to": 100, "je": 100, "wone": 100, "wtwo": 100, "one": 50, "two": 50},
            {"to one": 20, "wone two": 20},
        )
        c1 = ComposedRecord(0, 3, 7, "wone", "one", "to", "wtwo", (0, 2), (8, 12))
        c2 = ComposedRecord(1, 8, 12, "wtwo", "two", "wone", "je", (3, 7), (13, 15))
        corpus = RuntimeCorpus(db)
        try:
            self.assertEqual(
                validate_composed("to wone wtwo je", [c1, c2], corpus, []), frozenset()
            )
        finally:
            corpus.close()

    def test_protected_barrier_between_neighbor_rejects_member(self) -> None:
        # Protected content strictly between the left neighbor and the
        # span bars the adjacency through the real accept barrier check.
        db = _composed_db(
            self.root,
            {"to": 100, "je": 100, "wone": 100, "rone": 50},
            {"to rone": 20},
        )
        s = ComposedRecord(1, 3, 7, "wone", "rone", "to", "je", (0, 2), (8, 10))
        corpus = RuntimeCorpus(db)
        try:
            self.assertEqual(
                validate_composed(
                    "to wone je", [s], corpus, [Interval(2, 3, "test")]
                ),
                frozenset(),
            )
        finally:
            corpus.close()

    def test_composed_never_queries_internal_span_words(self) -> None:
        # The exact ngram keys actually queried through the engine:
        # individual acceptance then composed re-validation.  The spans'
        # internal words ("wone", "wtwo", "wthree", "wfour") never appear
        # as external-neighbor keys - only whole external tokens and the
        # replacement words form evidence keys.
        db = _composed_db(
            self.root,
            {
                "to": 100,
                "je": 100,
                "wone": 100,
                "wtwo": 100,
                "wthree": 100,
                "wfour": 100,
                "one": 50,
                "two": 50,
            },
            {"to one": 20, "wtwo two": 20},
        )
        a = Candidate(3, 12, "wone wtwo", 0.5, {})
        b = Candidate(13, 25, "wthree wfour", 0.5, {})
        detect_calls, fake_detect = _injected_detect((a, b))
        reviewer = _SpecReviewer({"wone wtwo": "one", "wthree wfour": "two"})
        captured: list[_KeySpyCorpus] = []

        def tracked(path: str | Path) -> _KeySpyCorpus:
            corpus = _KeySpyCorpus(path)
            captured.append(corpus)
            return corpus

        engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
        with (
            mock.patch.object(proxy, "detect", fake_detect),
            mock.patch.object(proxy, "RuntimeCorpus", tracked),
        ):
            engine.begin_request()
            repaired = engine.repair("to wone wtwo wthree wfour je")
        self.assertEqual(repaired, "to wone wtwo wthree wfour je")
        self.assertEqual(detect_calls, [("local-context", 4)])
        [corpus] = captured
        # The exact sequence of every ngram query actually executed:
        # the detector's per-token evidence (14), the two individual
        # acceptances (6) and the two composed re-validations (6).
        # From the first acceptance on, only whole EXTERNAL tokens and
        # the replacement words form evidence keys: the spans' internal
        # words are never queried as external-neighbor keys.
        self.assertEqual(
            corpus.ngram_keys,
            [
                ("to wone", 2),
                ("to wone", 2),
                ("wone wtwo", 2),
                ("to wone wtwo", 3),
                ("wone wtwo", 2),
                ("wtwo wthree", 2),
                ("wone wtwo wthree", 3),
                ("wtwo wthree", 2),
                ("wthree wfour", 2),
                ("wtwo wthree wfour", 3),
                ("wthree wfour", 2),
                ("wfour je", 2),
                ("wthree wfour je", 3),
                ("wfour je", 2),
                ("to one", 2),
                ("one wthree", 2),
                ("to one wthree", 3),
                ("wtwo two", 2),
                ("two je", 2),
                ("wtwo two je", 3),
                ("to one", 2),
                ("one two", 2),
                ("to one two", 3),
                ("one two", 2),
                ("two je", 2),
                ("one two je", 3),
            ],
        )


class LateComposedBudgetTests(unittest.TestCase):
    """T5: a known budget failure in the composed pass is a late abort."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        # Schema 5 + detection 14 (4 tokens) + 2 acceptances x 4 = 27;
        # composed member 0 queries 4 (28-31); member 1's first query is
        # the 32nd start, denied before execute at cap 31.
        self._cap = mock.patch.object(
            config, "RUNTIME_EVIDENCE_MAX_STATEMENTS", 31
        )
        self._cap.start()
        self.addCleanup(self._cap.stop)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _run(self, usage: bool) -> tuple[str, list[dict[str, object]], _CloseTrackingCorpus]:
        db = _composed_db(
            self.root,
            {"to": 100, "je": 100, "wone": 2, "wtwo": 2, "one": 50, "two": 50},
            {"to one": 20, "wone two": 20},
        )
        reviewer = _SpecReviewer({"wone": "one", "wtwo": "two"}, usage=usage)
        captured: list[_CloseTrackingCorpus] = []

        def tracked(path: str | Path) -> _CloseTrackingCorpus:
            corpus = _CloseTrackingCorpus(path)
            captured.append(corpus)
            return corpus

        engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
        with mock.patch.object(proxy, "RuntimeCorpus", tracked):
            engine.begin_request()
            repaired = engine.repair("to wone wtwo je")
        details = engine.take_details()
        self.assertEqual(len(captured), 1)
        self.assertEqual(reviewer.calls, 1)
        return repaired, details, captured[0]

    def test_composed_exhaustion_aborts_whole_pass(self) -> None:
        repaired, details, corpus = self._run(True)
        self.assertEqual(repaired, "to wone wtwo je")
        [detail] = details
        self.assertEqual(detail["replacements"], [])
        review = _sub_mapping(detail, "review_batch")
        self.assertEqual(review["calls"], 1)
        self.assertEqual(
            review["usage"],
            {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
        )
        failure = _sub_mapping(detail, "evidence_failure")
        self.assertEqual(
            failure, {"reason": REASON_BUDGET_EXCEEDED, "stage": "late"}
        )
        decisions = detail["reviewer_decisions"]
        if not isinstance(decisions, list) or len(decisions) != 2:
            self.fail("expected two reviewer decisions")
        for item in decisions:
            if not isinstance(item, dict):
                self.fail("decision is not a mapping")
            acceptance = _sub_mapping(item, "acceptance")
            self.assertEqual(
                acceptance,
                {
                    "accepted": False,
                    "reason": "evidence-abort",
                    "replacement": None,
                },
            )
            self.assertEqual(item["failure"], REASON_BUDGET_EXCEEDED)
        self.assertEqual(corpus._budget.statements, 31)
        self.assertTrue(corpus._budget.exhausted)
        self.assertEqual(corpus.close_calls, 1)

    def test_composed_exhaustion_unknown_usage_stays_unknown(self) -> None:
        repaired, details, corpus = self._run(False)
        self.assertEqual(repaired, "to wone wtwo je")
        [detail] = details
        review = _sub_mapping(detail, "review_batch")
        self.assertEqual(review["usage"], "unknown")
        failure = _sub_mapping(detail, "evidence_failure")
        self.assertEqual(
            failure, {"reason": REASON_BUDGET_EXCEEDED, "stage": "late"}
        )
        self.assertEqual(corpus._budget.statements, 31)
        self.assertTrue(corpus._budget.exhausted)

    def test_fresh_request_recovers_after_exhaustion(self) -> None:
        self._run(True)
        # A fresh request with the default finite policy and healthy text
        # (no detector candidates) completes fully: no failure is
        # recorded and no review call is made.
        healthy_db = _composed_db(self.root, {"to": 100, "je": 100}, {}, name="healthy.sqlite")
        reviewer = _SpecReviewer({})
        captured: list[_CloseTrackingCorpus] = []

        def tracked(path: str | Path) -> _CloseTrackingCorpus:
            corpus = _CloseTrackingCorpus(path)
            captured.append(corpus)
            return corpus

        engine = proxy.RepairEngine(healthy_db, reviewer, pandoc=_real_spec())
        with mock.patch.object(proxy, "RuntimeCorpus", tracked):
            engine.begin_request()
            repaired = engine.repair("to je je")
        self.assertEqual(repaired, "to je je")
        self.assertEqual(reviewer.calls, 0)
        [detail] = engine.take_details()
        self.assertNotIn("evidence_failure", detail)
        [corpus] = captured
        self.assertFalse(corpus._budget.exhausted)
        self.assertEqual(corpus.close_calls, 1)


class EngineMappingAbortTests(unittest.TestCase):
    """T5/R6: an unprovable mapping aborts the whole optional pass."""

    MAPPING_TEXT = "to wone je in wtwo end"

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _composed_db(
            self.root,
            {
                "to": 100,
                "je": 100,
                "in": 100,
                "end": 100,
                "wone": 2,
                "wtwo": 2,
                "one": 50,
                "two": 50,
            },
            {"to one": 20, "in two": 20},
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _run_mapping_abort(
        self, usage: bool
    ) -> tuple[
        str,
        list[dict[str, object]],
        _SpecReviewer,
        proxy.RepairEngine,
        list[_CloseTrackingCorpus],
    ]:
        # Both edits are independently and otherwise supported (real
        # individual acceptances succeed).  The fault is injected ONLY at
        # the actual owned ComposedRecord construction: the second real
        # construction returns a record whose original-slice field is
        # deliberately stale, and the REAL validator detects it and
        # raises ComposedMappingError - no fake validator, accept or
        # corpus lookup.
        reviewer = _SpecReviewer({"wone": "one", "wtwo": "two"}, usage=usage)
        constructor = composed_validation.ComposedRecord
        created: list[ComposedRecord] = []
        events, tracked_accept = _tracked_accept_events()

        def stale_record(
            decision_index: int,
            start: int,
            end: int,
            text: str,
            replacement: str,
            left: str | None,
            right: str | None,
            left_bounds: tuple[int, int] | None,
            right_bounds: tuple[int, int] | None,
        ) -> ComposedRecord:
            record = constructor(
                decision_index,
                start,
                end,
                text,
                replacement,
                left,
                right,
                left_bounds,
                right_bounds,
            )
            created.append(record)
            if len(created) == 2:
                return dataclasses.replace(record, text="deliberately-stale")
            return record

        captured: list[_CloseTrackingCorpus] = []

        def tracked(path: str | Path) -> _CloseTrackingCorpus:
            corpus = _CloseTrackingCorpus(path)
            captured.append(corpus)
            return corpus

        engine = proxy.RepairEngine(self.db, reviewer, pandoc=_real_spec())
        before = _index_state(self.root, self.db)
        with (
            mock.patch.object(composed_validation, "ComposedRecord", stale_record),
            mock.patch.object(proxy, "accept", tracked_accept),
            mock.patch.object(proxy, "RuntimeCorpus", tracked),
        ):
            engine.begin_request()
            repaired = engine.repair(self.MAPPING_TEXT)
        details = engine.take_details()
        self.assertEqual(before, _index_state(self.root, self.db))
        return repaired, details, reviewer, engine, captured

    def test_mapping_abort_known_usage_whole_pass_abstains(self) -> None:
        self._assert_mapping_abort(usage=True)

    def test_mapping_abort_unknown_usage_whole_pass_abstains(self) -> None:
        self._assert_mapping_abort(usage=False)

    def _assert_mapping_abort(self, *, usage: bool) -> None:
        repaired, details, reviewer, engine, captured = self._run_mapping_abort(usage)
        del engine
        # The whole optional pass abstained to the completed original;
        # no edit - not even the independently supported first one -
        # survives.
        self.assertEqual(repaired, self.MAPPING_TEXT)
        [detail] = details
        self.assertEqual(detail["replacements"], [])
        review = _sub_mapping(detail, "review_batch")
        self.assertEqual(review["calls"], 1)
        if usage:
            self.assertEqual(
                review["usage"],
                {"input_tokens": 10, "output_tokens": 20, "total_tokens": 30},
            )
        else:
            self.assertEqual(review["usage"], "unknown")
        failure = _sub_mapping(detail, "evidence_failure")
        self.assertEqual(
            failure,
            {"reason": COMPOSED_MAPPING_UNPROVABLE, "stage": "late"},
        )
        acceptance = detail["acceptance"]
        if not isinstance(acceptance, list) or len(acceptance) != 2:
            self.fail("expected two final acceptance records")
        for item in acceptance:
            if not isinstance(item, dict):
                self.fail("acceptance is not a mapping")
            self.assertEqual(
                item,
                {
                    "accepted": False,
                    "reason": COMPOSED_MAPPING_UNPROVABLE,
                    "replacement": None,
                },
            )
        decisions = detail["reviewer_decisions"]
        if not isinstance(decisions, list) or len(decisions) != 2:
            self.fail("expected two reviewer decisions")
        for item in decisions:
            if not isinstance(item, dict):
                self.fail("decision is not a mapping")
            self.assertEqual(item["failure"], COMPOSED_MAPPING_UNPROVABLE)
        # The owned real SQLite connection was actually closed once.
        [corpus] = captured
        self.assertEqual(corpus.close_calls, 1)
        connection = corpus.connection
        with self.assertRaises(sqlite3.ProgrammingError):
            connection.execute("SELECT 1")

    def test_same_engine_recovers_after_mapping_fault_removed(self) -> None:
        repaired, _details, reviewer, engine, _captured = self._run_mapping_abort(True)
        self.assertEqual(repaired, self.MAPPING_TEXT)
        self.assertEqual(reviewer.calls, 1)
        # The SAME engine instance, fault removed: both individually
        # supported, non-interacting edits are accepted and applied.
        engine.begin_request()
        recovered = engine.repair(self.MAPPING_TEXT)
        self.assertEqual(recovered, "to one je in two end")
        self.assertEqual(reviewer.calls, 2)
        [recovery] = engine.take_details()
        self.assertNotIn("evidence_failure", recovery)
        self.assertEqual(recovery["replacements"], ["one", "two"])
        acceptance = recovery["acceptance"]
        if not isinstance(acceptance, list) or len(acceptance) != 2:
            self.fail("expected two recovery acceptance records")
        for item in acceptance:
            if not isinstance(item, dict):
                self.fail("acceptance is not a mapping")
            self.assertTrue(item["accepted"])


class HttpRoundTripTests(unittest.TestCase):
    """T6: real proxy HTTP -> real engine -> real ResponsesReviewer."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _composed_db(
            self.root,
            {
                "to": 100,
                "in": 100,
                "je": 100,
                "wone": 2,
                "wtwo": 2,
                "one": 50,
                "two": 50,
                "rone": 50,
                "rtwo": 50,
            },
            {
                "one wtwo": 20,
                "wone two": 20,
                "to rone": 20,
                "in rtwo": 20,
            },
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _harness(self) -> _Harness:
        harness = _Harness()
        self.addCleanup(harness.close)
        harness.engine.index = self.db
        return harness

    def test_json_all_conflict_returns_raw_envelope(self) -> None:
        harness = self._harness()
        answer = "wone wtwo je"
        _MainUpstream.source = _json_completed(answer)
        _FakeUpstream.payload = _review_payload(
            [_prop("t0", False, "one"), _prop("t1", False, "two")]
        )
        status, payload = harness.post(_contract_body(False, input_text=answer))
        self.assertEqual(status, 200)
        # No accepted edit: the captured main body is returned exactly.
        self.assertEqual(payload, _MainUpstream.source)
        self.assertEqual(len(_FakeUpstream.recorded), 1)

    def test_json_compatible_pair_renders_repaired_text(self) -> None:
        harness = self._harness()
        answer = "to wone in wtwo je"
        _MainUpstream.source = _json_completed(answer)
        _FakeUpstream.payload = _review_payload(
            [_prop("t0", False, "rone"), _prop("t1", False, "rtwo")]
        )
        status, payload = harness.post(_contract_body(False, input_text=answer))
        self.assertEqual(status, 200)
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        body = json.loads(payload)
        if not isinstance(body, dict):
            self.fail("payload is not an object")
        output = body.get("output")
        if not isinstance(output, list) or not output or not isinstance(output[0], dict):
            self.fail("payload has no output")
        content = output[0].get("content")
        if not isinstance(content, list) or not content or not isinstance(content[0], dict):
            self.fail("payload has no content")
        self.assertEqual(content[0].get("text"), "to rone in rtwo je")

    def test_sse_all_conflict_stream_is_byte_identical(self) -> None:
        harness = self._harness()
        answer = "wone wtwo je"
        _MainUpstream.content_type = "text/event-stream"
        _MainUpstream.source = _tc_baseline(answer)
        _FakeUpstream.payload = _review_payload(
            [_prop("t0", False, "one"), _prop("t1", False, "two")]
        )
        status, payload = harness.post(_contract_body(True, input_text=answer))
        self.assertEqual(status, 200)
        self.assertEqual(payload, _MainUpstream.source)
        self.assertEqual(len(_FakeUpstream.recorded), 1)

    def test_sse_compatible_pair_renders_repaired_answer(self) -> None:
        harness = self._harness()
        answer = "to wone in wtwo je"
        _MainUpstream.content_type = "text/event-stream"
        _MainUpstream.source = _tc_baseline(answer)
        _FakeUpstream.payload = _review_payload(
            [_prop("t0", False, "rone"), _prop("t1", False, "rtwo")]
        )
        status, payload = harness.post(_contract_body(True, input_text=answer))
        self.assertEqual(status, 200)
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        events = [
            line[5:]
            for line in payload.split(b"\n")
            if line.startswith(b"data: ")
        ]
        self.assertTrue(events)
        completed = json.loads(events[-1])
        if not isinstance(completed, dict):
            self.fail("completed event is not an object")
        self.assertEqual(completed.get("type"), "response.completed")
        response = completed.get("response")
        if not isinstance(response, dict):
            self.fail("completed event has no response")
        output = response.get("output")
        if not isinstance(output, list) or not output or not isinstance(output[0], dict):
            self.fail("completed response has no output")
        content = output[0].get("content")
        if not isinstance(content, list) or not content or not isinstance(content[0], dict):
            self.fail("completed response has no content")
        self.assertEqual(content[0].get("text"), "to rone in rtwo je")

    def test_same_proxy_next_request_healthy_zero_review(self) -> None:
        harness = self._harness()
        answer = "wone wtwo je"
        _MainUpstream.source = _json_completed(answer)
        _FakeUpstream.payload = _review_payload(
            [_prop("t0", False, "one"), _prop("t1", False, "two")]
        )
        status, payload = harness.post(_contract_body(False, input_text=answer))
        self.assertEqual(status, 200)
        self.assertEqual(payload, _MainUpstream.source)
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        # The SAME proxy instance then serves a healthy answer: zero
        # detector candidates, zero review calls, raw envelope returned.
        healthy = "to je je"
        _MainUpstream.source = _json_completed(healthy)
        status, payload = harness.post(_contract_body(False, input_text=healthy))
        self.assertEqual(status, 200)
        self.assertEqual(payload, _MainUpstream.source)
        self.assertEqual(len(_FakeUpstream.recorded), 1)


if __name__ == "__main__":
    unittest.main()
