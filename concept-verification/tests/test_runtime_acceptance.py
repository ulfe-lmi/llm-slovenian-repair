"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.

Order 028-a, requirement 8: bounded regression coverage for the new
runtime lexical acceptance policy (runtime_acceptance.accept).

Native real boundaries under test: real read-only SQLite (tiny
synthetic owned databases), the lexical-shape gate, R4/R5 routing and
the anchored context comparisons, the read-only RuntimeCorpus and its
finite evidence budget, the composed-result validation callable, the
real RepairEngine with the actual detector, and - in the round-trip
class - the real ResponsesReviewer and qualified Pandoc over owned
loopback-0 HTTP.  Only the reviewer object, the main/review HTTP
endpoints and - in the disclosed phrase-consumer cases - the
detector's candidate list are synthetic; the corpus, its queries,
acceptance and the engine/proxy paths are never faked.  No
missing-to-zero default, no quality claim (order 028-a, R8).
"""

from __future__ import annotations

import json
import sys
import tempfile
import time
import unittest
from collections.abc import Mapping
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config  # noqa: E402
import proxy  # noqa: E402
from composed_validation import (  # noqa: E402
    ComposedMappingError,
    ComposedRecord,
    validate_composed,
)
from detector import Candidate  # noqa: E402
from protected import Interval  # noqa: E402
from qwen_client import Proposal  # noqa: E402
from repair import Acceptance  # noqa: E402
from runtime_acceptance import (  # noqa: E402
    ACCEPTED_POSSIBLE_TYPO,
    ORIGINAL_SPAN_NOT_LEXICAL,
    REPLACEMENT_NOT_LEXICAL,
    _one_codepoint_edit,
    accept,
    is_lexical_unit,
)
from runtime_corpus import (  # noqa: E402
    REASON_BUDGET_EXCEEDED,
    RuntimeCorpus,
    RuntimeCorpusError,
)
from tests.test_composed_validation import (  # noqa: E402
    _CloseTrackingCorpus,
    _composed_db,
    _index_state,
    _injected_detect,
    _KeySpyCorpus,
    _SpecReviewer,
)
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


class _QueryCountCorpus(RuntimeCorpus):
    """Call-through adapter counting every actual corpus query
    (disclosed observation; every query still executes)."""

    def __init__(self, path: str | Path) -> None:
        super().__init__(path)
        self.unigram_calls: list[str] = []
        self.ngram_calls: list[tuple[str, int]] = []

    def unigram(self, word: str) -> Evidence:
        self.unigram_calls.append(word)
        return super().unigram(word)

    def ngram(self, phrase: str, length: int) -> Evidence:
        self.ngram_calls.append((phrase, length))
        return super().ngram(phrase, length)


class _MarkingKeySpyCorpus(_KeySpyCorpus):
    """Key-spy corpus that also marks the end of the detector query
    phase so acceptance-phase keys can be examined separately."""

    def __init__(self, path: str | Path) -> None:
        super().__init__(path)
        self.marks: list[int] = []


def _answer_text(payload: bytes) -> str:
    """The output_text of a JSON completed response payload."""
    body = json.loads(payload)
    if not isinstance(body, dict):
        raise AssertionError("payload is not an object")
    output = body.get("output")
    if not isinstance(output, list) or not output or not isinstance(output[0], dict):
        raise AssertionError("payload has no output")
    content = output[0].get("content")
    if not isinstance(content, list) or not content or not isinstance(content[0], dict):
        raise AssertionError("payload has no content")
    text = content[0].get("text")
    if not isinstance(text, str):
        raise AssertionError("payload has no output_text")
    return text


def _sse_completed_text(payload: bytes) -> str:
    """The output_text of the LAST SSE data event (completion)."""
    events = [
        line[5:] for line in payload.split(b"\n") if line.startswith(b"data: ")
    ]
    if not events:
        raise AssertionError("payload has no SSE data events")
    completed = json.loads(events[-1])
    if not isinstance(completed, dict) or completed.get("type") != "response.completed":
        raise AssertionError("last SSE event is not response.completed")
    response = completed.get("response")
    if not isinstance(response, dict):
        raise AssertionError("completed event has no response")
    output = response.get("output")
    if not isinstance(output, list) or not output or not isinstance(output[0], dict):
        raise AssertionError("completed response has no output")
    content = output[0].get("content")
    if not isinstance(content, list) or not content or not isinstance(content[0], dict):
        raise AssertionError("completed response has no content")
    text = content[0].get("text")
    if not isinstance(text, str):
        raise AssertionError("completed response has no output_text")
    return text


class _AcceptCaseBase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _db(
        self,
        unigrams: Mapping[str, int],
        bigrams: Mapping[str, int],
    ) -> Path:
        return _composed_db(self.root, unigrams, bigrams)

    def _decide(
        self,
        db: Path,
        text: str,
        start: int,
        end: int,
        replacement: str,
        *,
        intervals: tuple[Interval, ...] = (),
        left: str | None = None,
        right: str | None = None,
        left_bounds: tuple[int, int] | None = None,
        right_bounds: tuple[int, int] | None = None,
        keep: bool = False,
        wider: bool = False,
        candidate_text: str | None = None,
    ) -> tuple[Acceptance, _QueryCountCorpus]:
        corpus = _QueryCountCorpus(db)
        self.addCleanup(corpus.close)
        verdict = accept(
            text,
            Candidate(start, end, candidate_text or text[start:end], 0.5, {}),
            Proposal(keep, replacement, wider),
            corpus,
            list(intervals),
            left=left,
            right=right,
            left_bounds=left_bounds,
            right_bounds=right_bounds,
        )
        return verdict, corpus


class LexicalUnitTests(unittest.TestCase):
    """R2: the raw-byte lexical-unit gate on actual token shapes."""

    def test_letter_units_with_tokenizer_joiners_accept(self) -> None:
        for unit in ("črka", "rjavo-zlati", "d'acqua", "it's", "ONE", "a"):
            self.assertTrue(is_lexical_unit(unit), unit)

    def test_numeric_shapes_digits_and_fragments_reject(self) -> None:
        for unit in (
            "2",
            "ⅲ",
            "½",
            "one²",
            "1",
            "abc1",
            "a_b",
            "a/b",
            "ka[",
            "x—y",
            "foo—bar",
            "",
        ):
            self.assertFalse(is_lexical_unit(unit), unit)


class OneCodepointEditTests(unittest.TestCase):
    """R5: exactly-one code-point insertion/deletion/substitution."""

    def test_zero_or_multi_edit_reject(self) -> None:
        self.assertFalse(_one_codepoint_edit("kat", "kat"))
        self.assertFalse(_one_codepoint_edit("kat", "kaij"))
        self.assertFalse(_one_codepoint_edit("ka", "katr"))
        self.assertFalse(_one_codepoint_edit("kat", "k"))
        self.assertFalse(_one_codepoint_edit("kat", "kjr"))

    def test_single_edit_accepts(self) -> None:
        self.assertTrue(_one_codepoint_edit("kat", "kai"))
        self.assertTrue(_one_codepoint_edit("kat", "katr"))
        self.assertTrue(_one_codepoint_edit("katr", "kat"))
        self.assertTrue(_one_codepoint_edit("čes", "čeks"))


class DirectAcceptTests(_AcceptCaseBase):
    """R2-R5: the real accept boundary with explicit owned evidence
    rows; the call-through corpus proves query order/absence."""

    # Known original unigram 100: the DIRECT fixtures are synthetic and
    # do not depend on real CPU rarity.  100 keeps every same-n context
    # count (10/20/40) within the original unit count and makes the R4
    # positive (20 candidate vs 10 original context) fail the old
    # wrong-unigram-denominator threshold (2 x 100).
    WONE_DB = {"to": 100, "je": 100, "wone": 100, "rone": 50}

    def test_r5_count_one_accepts_censored_original(self) -> None:
        db = self._db({"to": 100, "je": 100, "zaa": 42}, {"zaa je": 1})
        # count ONE is positive support on the narrow R5 route: a
        # factor-two floor policy would reject this exact fixture.
        verdict, corpus = self._decide(
            db,
            "to aaa je",
            3,
            6,
            "zaa",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(7, 9),
        )
        self.assertTrue(verdict.accepted)
        self.assertEqual(verdict.reason, ACCEPTED_POSSIBLE_TYPO)
        self.assertEqual(verdict.replacement, "zaa")
        # censored original context is queried, stays unknown and does
        # not oppose the count-one positive adjacent context.
        self.assertIn(("aaa je", 2), corpus.ngram_calls)

    def test_r4_factor_two_accepts(self) -> None:
        db = self._db(self.WONE_DB, {"to rone": 20, "to wone": 10})
        verdict, _corpus = self._decide(
            db,
            "to wone je",
            3,
            7,
            "rone",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(8, 10),
        )
        self.assertTrue(verdict.accepted)
        self.assertEqual(verdict.reason, "accepted-independent-evidence")
        self.assertEqual(verdict.replacement, "rone")

    def test_equal_context_rejects(self) -> None:
        db = self._db(self.WONE_DB, {"to rone": 20, "to wone": 20})
        verdict, _corpus = self._decide(
            db,
            "to wone je",
            3,
            7,
            "rone",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(8, 10),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "local-evidence-not-stronger")

    def test_below_factor_two_rejects(self) -> None:
        db = self._db(self.WONE_DB, {"to rone": 21, "to wone": 20})
        verdict, _corpus = self._decide(
            db,
            "to wone je",
            3,
            7,
            "rone",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(8, 10),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "local-evidence-not-stronger")

    def test_unknown_original_context_rejects(self) -> None:
        db = self._db(self.WONE_DB, {"to rone": 20})
        verdict, _corpus = self._decide(
            db,
            "to wone je",
            3,
            7,
            "rone",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(8, 10),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "local-evidence-not-stronger")

    def test_weaker_context_opposes(self) -> None:
        db = self._db(self.WONE_DB, {"to rone": 20, "to wone": 40})
        verdict, corpus = self._decide(
            db,
            "to wone je",
            3,
            7,
            "rone",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(8, 10),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "local-evidence-not-stronger")
        self.assertEqual(corpus.ngram_calls, [("to rone", 2), ("to wone", 2)])

    def test_known_zero_replacement_opposes_immediately(self) -> None:
        db = self._db(self.WONE_DB, {"to rone": 0})
        verdict, corpus = self._decide(
            db,
            "to wone je",
            3,
            7,
            "rone",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(8, 10),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "local-evidence-not-stronger")
        self.assertEqual(corpus.ngram_calls, [("to rone", 2)])
        self.assertEqual(corpus.unigram_calls, ["rone", "wone"])

    def test_nonlexical_replacement_rejects_before_queries(self) -> None:
        db = self._db({"to": 100, "je": 100, "wone": 2, "one²": 100}, {})
        verdict, corpus = self._decide(
            db,
            "to wone je",
            3,
            7,
            "one²",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(8, 10),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, REPLACEMENT_NOT_LEXICAL)
        self.assertEqual(corpus.unigram_calls, [])
        self.assertEqual(corpus.ngram_calls, [])

    def test_numeric_shape_replacement_rejects_before_queries(self) -> None:
        db = self._db({"to": 100, "je": 100, "wone": 2, "ⅲ": 100}, {})
        verdict, corpus = self._decide(
            db,
            "to wone je",
            3,
            7,
            "ⅲ",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(8, 10),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, REPLACEMENT_NOT_LEXICAL)
        self.assertEqual(corpus.unigram_calls, [])
        self.assertEqual(corpus.ngram_calls, [])

    def test_nonlexical_original_span_rejects_before_queries(self) -> None:
        db = self._db({"to": 100, "je": 100, "kat": 100}, {})
        verdict, corpus = self._decide(
            db,
            "to ⅲ je",
            3,
            4,
            "kat",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(5, 7),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, ORIGINAL_SPAN_NOT_LEXICAL)
        self.assertEqual(corpus.unigram_calls, [])
        self.assertEqual(corpus.ngram_calls, [])

    def test_distant_unknown_original_rejects(self) -> None:
        db = self._db({"to": 100, "je": 100, "zeta": 50}, {"to zeta": 20})
        verdict, _corpus = self._decide(
            db,
            "to kat je",
            3,
            6,
            "zeta",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(7, 9),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "local-evidence-not-stronger")

    def test_anchorless_same_count_phrase_rejects(self) -> None:
        db = self._db(
            {"alpha": 100, "beta": 100, "omega": 100, "gamma": 100},
            {"omega gamma": 20, "alpha beta": 1},
        )
        verdict, _corpus = self._decide(db, "alpha beta", 0, 10, "omega gamma")
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "local-evidence-not-stronger")

    def test_unchanged_anchor_same_count_phrase_accepts(self) -> None:
        db = self._db(
            {"alpha": 100, "beta": 100, "omega": 100, "gamma": 100},
            {"omega beta": 20, "alpha beta": 1},
        )
        verdict, _corpus = self._decide(db, "alpha beta", 0, 10, "omega beta")
        self.assertTrue(verdict.accepted)
        self.assertEqual(verdict.reason, "accepted-independent-evidence")

    def test_phrase_missing_eligible_boundary_rejects(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "alpha": 100, "beta": 100, "omega": 100, "gamma": 100},
            {"to omega": 20, "to alpha": 10, "omega gamma": 20, "alpha beta": 1},
        )
        verdict, _corpus = self._decide(
            db,
            "to alpha beta je",
            3,
            13,
            "omega gamma",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(14, 16),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "local-evidence-not-stronger")

    def test_phrase_both_supported_accepts(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "alpha": 100, "beta": 100, "omega": 100, "gamma": 100},
            {
                "to omega": 20,
                "to alpha": 10,
                "omega gamma": 20,
                "alpha beta": 1,
                "gamma je": 20,
                "beta je": 10,
            },
        )
        verdict, _corpus = self._decide(
            db,
            "to alpha beta je",
            3,
            13,
            "omega gamma",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(14, 16),
        )
        self.assertTrue(verdict.accepted)
        self.assertEqual(verdict.reason, "accepted-independent-evidence")

    def test_changed_count_both_anchors_accept(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "alpha": 100, "beta": 100, "omega": 100},
            {"to omega": 20, "to alpha": 10, "omega je": 20, "beta je": 10},
        )
        verdict, _corpus = self._decide(
            db,
            "to alpha beta je",
            3,
            13,
            "omega",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(14, 16),
        )
        self.assertTrue(verdict.accepted)
        self.assertEqual(verdict.reason, "accepted-independent-evidence")

    def test_changed_count_missing_anchor_rejects(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "alpha": 100, "beta": 100, "omega": 100},
            {"to omega": 20, "to alpha": 10},
        )
        verdict, _corpus = self._decide(
            db,
            "to alpha beta je",
            3,
            13,
            "omega",
            left="to",
            left_bounds=(0, 2),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "local-evidence-not-stronger")

    def test_changed_count_never_queries_spanning_trigram(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "alpha": 100, "beta": 100, "omega": 100},
            {
                "to omega": 20,
                "to alpha": 10,
                "omega je": 20,
                "beta je": 10,
                "to omega je": 100,
            },
        )
        verdict, corpus = self._decide(
            db,
            "to alpha beta je",
            3,
            13,
            "omega",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(14, 16),
        )
        self.assertTrue(verdict.accepted)
        self.assertNotIn(("to omega je", 3), corpus.ngram_calls)

    def test_partial_word_target_is_stale(self) -> None:
        db = self._db({"to": 100, "je": 100, "kat": 100}, {})
        verdict, _corpus = self._decide(
            db, "to alphabeta je", 3, 8, "kat", left="to", left_bounds=(0, 2)
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "stale-candidate-bounds")

    def test_skipped_neighbor_is_stale(self) -> None:
        db = self._db({"to": 100, "je": 100, "alpha": 100, "omega": 100}, {})
        verdict, _corpus = self._decide(
            db, "to je alpha", 6, 11, "omega", left="to", left_bounds=(0, 2)
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "stale-neighbor-bounds")

    def test_wrong_occurrence_neighbor_is_stale(self) -> None:
        db = self._db({"to": 100, "je": 100, "alpha": 100, "omega": 100}, {})
        verdict, _corpus = self._decide(
            db,
            "to alpha je to alpha je",
            15,
            20,
            "omega",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(21, 23),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "stale-neighbor-bounds")

    def test_neighbor_inside_target_is_stale(self) -> None:
        db = self._db({"to": 100, "je": 100, "alpha": 100, "omega": 100}, {})
        verdict, _corpus = self._decide(
            db,
            "to alpha je",
            3,
            8,
            "omega",
            left="alpha",
            left_bounds=(3, 8),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "stale-neighbor-bounds")

    def test_stale_candidate_text_is_stale(self) -> None:
        db = self._db({"to": 100, "je": 100, "wone": 2, "rone": 50}, {})
        verdict, _corpus = self._decide(
            db,
            "to wone je",
            3,
            7,
            "rone",
            left="to",
            left_bounds=(0, 2),
            candidate_text="WONE",
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "stale-candidate-bounds")

    def test_protected_span_rejects(self) -> None:
        db = self._db({"to": 100, "je": 100, "kat": 100}, {})
        verdict, corpus = self._decide(
            db,
            "to alpha beta je",
            3,
            13,
            "kat",
            intervals=(Interval(8, 9, "p"),),
            left="to",
            left_bounds=(0, 2),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "protected")
        self.assertEqual(corpus.unigram_calls, [])
        self.assertEqual(corpus.ngram_calls, [])

    def test_barrier_between_neighbor_rejects(self) -> None:
        db = self._db({"to": 100, "je": 100, "alpha": 100, "kat": 100}, {})
        verdict, corpus = self._decide(
            db,
            "to, alpha je",
            4,
            9,
            "kat",
            intervals=(Interval(3, 4, "p"),),
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(10, 12),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "barrier-between-neighbor")
        self.assertEqual(corpus.unigram_calls, [])
        self.assertEqual(corpus.ngram_calls, [])

    def test_reviewer_kept_rejects_before_queries(self) -> None:
        db = self._db(self.WONE_DB, {"to rone": 20, "to wone": 10})
        verdict, corpus = self._decide(
            db,
            "to wone je",
            3,
            7,
            "rone",
            keep=True,
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(8, 10),
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "reviewer-kept")
        self.assertEqual(corpus.unigram_calls, [])
        self.assertEqual(corpus.ngram_calls, [])

    def test_wider_edit_rejects(self) -> None:
        db = self._db(self.WONE_DB, {})
        verdict, corpus = self._decide(
            db, "to wone je", 3, 7, "rone", wider=True
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "wider-or-identity")
        self.assertEqual(corpus.unigram_calls, [])

    def test_identity_replacement_rejects(self) -> None:
        db = self._db({"to": 100, "je": 100, "wone": 2}, {})
        verdict, corpus = self._decide(
            db, "to wone je", 3, 7, "wone", left="to", left_bounds=(0, 2)
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "wider-or-identity")
        self.assertEqual(corpus.unigram_calls, [])

    def test_control_or_newline_rejects(self) -> None:
        db = self._db({"to": 100, "je": 100, "wone": 2}, {})
        verdict, _corpus = self._decide(db, "to wone je", 3, 7, "ka\nto")
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "control-or-newline")

    def test_grapheme_sensitive_replacement_rejects(self) -> None:
        db = self._db({"to": 100, "je": 100, "wone": 2}, {})
        verdict, _corpus = self._decide(db, "to wone je", 3, 7, "ka\u0308")
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "grapheme-sensitive-replacement")

    def test_markup_rejects(self) -> None:
        db = self._db({"to": 100, "je": 100, "wone": 2}, {})
        verdict, _corpus = self._decide(db, "to wone je", 3, 7, "ka[to]")
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "markup")

    def test_replacement_size_rejects(self) -> None:
        db = self._db({"to": 100, "je": 100, "wone": 2}, {})
        verdict, _corpus = self._decide(
            db, "to wone je", 3, 7, "wone wtwo wthree wfour wfive"
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "replacement-size")

    def test_replacement_unigram_known_zero_rejects(self) -> None:
        db = self._db({"to": 100, "je": 100, "wone": 2, "rone": 0}, {})
        verdict, corpus = self._decide(
            db, "to wone je", 3, 7, "rone", left="to", left_bounds=(0, 2)
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "replacement-unigram-uncertain")
        self.assertEqual(corpus.unigram_calls, ["rone"])

    def test_replacement_unigram_unavailable_rejects(self) -> None:
        db = self._db({"to": 100, "je": 100, "wone": 2}, {})
        verdict, corpus = self._decide(
            db, "to wone je", 3, 7, "rone", left="to", left_bounds=(0, 2)
        )
        self.assertFalse(verdict.accepted)
        self.assertEqual(verdict.reason, "replacement-unigram-uncertain")
        self.assertEqual(corpus.unigram_calls, ["rone"])

    def test_casefold_lookup_preserves_proposed_bytes(self) -> None:
        db = self._db({"to": 100, "je": 100, "wone": 2, "one": 50}, {"to one": 20, "to wone": 10})
        verdict, _corpus = self._decide(
            db,
            "To wone je",
            3,
            7,
            "ONE",
            left="to",
            right="je",
            left_bounds=(0, 2),
            right_bounds=(8, 10),
        )
        self.assertTrue(verdict.accepted)
        self.assertEqual(verdict.replacement, "ONE")

    def test_repeated_identical_spans_both_accept(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "one": 50},
            {"to one": 20, "wone one": 20, "to wone": 10, "wone wone": 10},
        )
        first, _ = self._decide(
            db,
            "to wone wone je",
            3,
            7,
            "one",
            left="to",
            right="wone",
            left_bounds=(0, 2),
            right_bounds=(8, 12),
        )
        second, _ = self._decide(
            db,
            "to wone wone je",
            8,
            12,
            "one",
            left="wone",
            right="je",
            left_bounds=(3, 7),
            right_bounds=(13, 15),
        )
        self.assertTrue(first.accepted)
        self.assertTrue(second.accepted)


class BudgetTests(_AcceptCaseBase):
    """R3: a finite budget failure propagates untouched (late abort)."""

    def _run_capped(self, cap: int) -> RuntimeCorpus:
        patcher = mock.patch.object(config, "RUNTIME_EVIDENCE_MAX_STATEMENTS", cap)
        patcher.start()
        self.addCleanup(patcher.stop)
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "rone": 50},
            {"to rone": 20, "to wone": 10},
        )
        corpus = RuntimeCorpus(db)
        self.addCleanup(corpus.close)
        with self.assertRaises(RuntimeCorpusError) as ctx:
            accept(
                "to wone je",
                Candidate(3, 7, "wone", 0.5, {}),
                Proposal(False, "rone", False),
                corpus,
                [],
                left="to",
                right="je",
                left_bounds=(0, 2),
                right_bounds=(8, 10),
            )
        exc = ctx.exception
        self.assertIsInstance(exc, RuntimeCorpusError)
        self.assertEqual(exc.reason, REASON_BUDGET_EXCEEDED)
        self.assertTrue(corpus._budget.exhausted)
        return corpus

    def test_unigram_phase_exhaustion(self) -> None:
        corpus = self._run_capped(6)
        # schema 5 + the replacement unigram reach the cap; the
        # original-side unigram start is denied before execute.
        self.assertEqual(corpus._budget.statements, 6)

    def test_context_pair_phase_exhaustion(self) -> None:
        corpus = self._run_capped(8)
        # schema 5 + both unigrams + the first pair's replacement side
        # reach the cap; the original side of the same pair is denied.
        self.assertEqual(corpus._budget.statements, 8)


class MappingTests(_AcceptCaseBase):
    """R6: unprovable composed mappings abort the whole pass."""

    def test_stale_rebased_slice_aborts_whole_pass(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "wone": 100, "rone": 50, "one": 50},
            {"to rone": 20, "to one": 20},
        )
        s = ComposedRecord(1, 3, 7, "wone", "rone", "to", "je", (0, 2), (8, 10))
        m = ComposedRecord(0, 3, 7, "WONE", "one", "to", "je", (0, 2), (8, 10))
        corpus = RuntimeCorpus(db)
        self.addCleanup(corpus.close)
        with self.assertRaises(ComposedMappingError):
            validate_composed("to wone je", [m, s], corpus, [])

    def test_compatible_multiple_edits_both_survive(self) -> None:
        db = self._db(
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
            {"to one": 20, "in two": 20, "to wone": 10, "in wtwo": 10},
        )
        c1 = ComposedRecord(0, 3, 7, "wone", "one", "to", "je", (0, 2), (8, 10))
        c2 = ComposedRecord(1, 14, 18, "wtwo", "two", "in", "end", (11, 13), (19, 22))
        corpus = RuntimeCorpus(db)
        self.addCleanup(corpus.close)
        self.assertEqual(
            validate_composed("to wone je in wtwo end", [c1, c2], corpus, []),
            {0, 1},
        )


class EngineWordTests(_AcceptCaseBase):
    """R8: real detector + real engine + qualified Pandoc word-level
    acceptance (no candidate injection)."""

    def _run(
        self,
        unigrams: Mapping[str, int],
        bigrams: Mapping[str, int],
        replacements: Mapping[str, str],
        text: str,
    ) -> tuple[str, list[dict[str, object]], _SpecReviewer, _CloseTrackingCorpus]:
        db = self._db(unigrams, bigrams)
        before = _index_state(self.root, db)
        reviewer = _SpecReviewer(dict(replacements))
        captured: list[_CloseTrackingCorpus] = []

        def tracked(path: str | Path) -> _CloseTrackingCorpus:
            corpus = _CloseTrackingCorpus(path)
            captured.append(corpus)
            return corpus

        engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
        with mock.patch.object(proxy, "RuntimeCorpus", tracked):
            engine.begin_request()
            repaired = engine.repair(text)
        details = engine.take_details()
        self.assertEqual(before, _index_state(self.root, db))
        self.assertEqual(len(captured), 1)
        return repaired, details, reviewer, captured[0]

    def test_supported_word_repair_end_to_end(self) -> None:
        repaired, details, reviewer, corpus = self._run(
            {"to": 100, "je": 100, "wone": 2, "one": 50},
            {"to one": 20, "to wone": 10},
            {"wone": "one"},
            "to wone je",
        )
        self.assertEqual(repaired, "to one je")
        self.assertEqual(reviewer.calls, 1)
        [detail] = details
        self.assertEqual(detail["replacements"], ["one"])
        acceptance = detail["acceptance"]
        if not isinstance(acceptance, list) or len(acceptance) != 1:
            self.fail("expected one acceptance record")
        item = acceptance[0]
        if not isinstance(item, dict):
            self.fail("acceptance record is not a mapping")
        self.assertEqual(
            item,
            {
                "accepted": True,
                "reason": "accepted-independent-evidence",
                "replacement": "one",
            },
        )
        self.assertEqual(corpus.close_calls, 1)

    def test_unsupported_word_returns_raw_original(self) -> None:
        repaired, details, reviewer, _corpus = self._run(
            {"to": 100, "je": 100, "wone": 2, "one": 50},
            {"to wone": 10},
            {"wone": "one"},
            "to wone je",
        )
        self.assertEqual(repaired, "to wone je")
        self.assertEqual(reviewer.calls, 1)
        [detail] = details
        self.assertEqual(detail["replacements"], [])
        acceptance = detail["acceptance"]
        if not isinstance(acceptance, list) or len(acceptance) != 1:
            self.fail("expected one acceptance record")
        item = acceptance[0]
        if not isinstance(item, dict):
            self.fail("acceptance record is not a mapping")
        self.assertEqual(
            item,
            {
                "accepted": False,
                "reason": "local-evidence-not-stronger",
                "replacement": None,
            },
        )

    def test_possible_typo_word_end_to_end(self) -> None:
        repaired, details, reviewer, _corpus = self._run(
            {"to": 100, "je": 100, "zaa": 42},
            {"zaa je": 5},
            {"aaa": "zaa"},
            "to aaa je",
        )
        self.assertEqual(repaired, "to zaa je")
        self.assertEqual(reviewer.calls, 1)
        [detail] = details
        self.assertEqual(detail["replacements"], ["zaa"])
        acceptance = detail["acceptance"]
        if not isinstance(acceptance, list) or len(acceptance) != 1:
            self.fail("expected one acceptance record")
        item = acceptance[0]
        if not isinstance(item, dict):
            self.fail("acceptance record is not a mapping")
        self.assertEqual(
            item,
            {
                "accepted": True,
                "reason": ACCEPTED_POSSIBLE_TYPO,
                "replacement": "zaa",
            },
        )

    def test_repeated_occurrences_one_review_both_applied(self) -> None:
        repaired, details, reviewer, _corpus = self._run(
            {"to": 100, "je": 100, "wone": 2, "one": 50},
            {
                "to one": 20,
                "wone one": 20,
                "to wone": 10,
                "wone wone": 10,
                "one one": 20,
                "one je": 20,
                "wone je": 10,
            },
            {"wone": "one"},
            "to wone wone je",
        )
        self.assertEqual(repaired, "to one one je")
        self.assertEqual(reviewer.calls, 1)
        sentence, targets = reviewer.sent[0]
        self.assertEqual(sentence, "to wone wone je")
        self.assertEqual([t.id for t in targets], ["t0", "t1"])
        [detail] = details
        self.assertEqual(detail["replacements"], ["one", "one"])
        acceptance = detail["acceptance"]
        if not isinstance(acceptance, list) or len(acceptance) != 2:
            self.fail("expected two acceptance records")
        for item in acceptance:
            if not isinstance(item, dict):
                self.fail("acceptance record is not a mapping")
            self.assertTrue(item["accepted"])


class PhraseConsumerTests(_AcceptCaseBase):
    """R8: multiword phrase consumer controls.

    Disclosed: the real detector only ever selects single-token spans,
    so the multiword candidates come from the _injected_detect wrapper
    (which still CALLS the real detector); every downstream boundary -
    tokenize, prepare, batch, acceptance, composed validation, apply -
    is real.  This proves the phrase CONSUMER boundary, not the
    existence of a phrase producer.
    """

    def _run(
        self,
        unigrams: Mapping[str, int],
        bigrams: Mapping[str, int],
        candidate: Candidate,
        replacement: str,
        text: str,
    ) -> tuple[str, _SpecReviewer, list[tuple[str, int]]]:
        db = self._db(unigrams, bigrams)
        reviewer = _SpecReviewer({candidate.text: replacement})
        detect_calls, base_fake = _injected_detect((candidate,))
        captured: list[_MarkingKeySpyCorpus] = []

        def fake(
            raw_text: str,
            raw_corpus: Corpus,
            raw_intervals: list[Interval] | None = None,
            *,
            mode: str = "local-context",
            threshold: int = 3,
            maximum: int = 4,
        ) -> list[Candidate]:
            result = base_fake(
                raw_text,
                raw_corpus,
                raw_intervals,
                mode=mode,
                threshold=threshold,
                maximum=maximum,
            )
            captured[0].marks.append(len(captured[0].ngram_keys))
            return result

        def tracked(path: str | Path) -> _MarkingKeySpyCorpus:
            corpus = _MarkingKeySpyCorpus(path)
            captured.append(corpus)
            return corpus

        engine = proxy.RepairEngine(db, reviewer, pandoc=_real_spec())
        with (
            mock.patch.object(proxy, "detect", fake),
            mock.patch.object(proxy, "RuntimeCorpus", tracked),
        ):
            engine.begin_request()
            repaired = engine.repair(text)
        self.assertEqual(detect_calls, [("local-context", 4)])
        self.assertEqual(len(captured), 1)
        [corpus] = captured
        [mark] = corpus.marks
        return repaired, reviewer, corpus.ngram_keys[mark:]

    def test_unchanged_anchor_phrase_survives(self) -> None:
        candidate = Candidate(3, 13, "alpha beta", 0.5, {})
        repaired, reviewer, accept_keys = self._run(
            {
                "to": 100,
                "je": 100,
                "alpha": 100,
                "beta": 100,
                "omega": 100,
                "gamma": 100,
            },
            {
                "to omega": 20,
                "to alpha": 10,
                "omega beta": 20,
                "alpha beta": 1,
                "beta je": 5,
            },
            candidate,
            "omega beta",
            "to alpha beta je",
        )
        self.assertEqual(repaired, "to omega beta je")
        self.assertEqual(reviewer.calls, 1)
        for probe in (
            ("omega beta", 2),
            ("alpha beta", 2),
            ("to omega", 2),
            ("to alpha", 2),
            ("beta je", 2),
        ):
            self.assertIn(probe, accept_keys)
        for key, length in accept_keys:
            self.assertEqual(length, 2, f"spanning ngram {key!r} queried")

    def test_changed_count_phrase_survives(self) -> None:
        candidate = Candidate(3, 13, "alpha beta", 0.5, {})
        repaired, reviewer, accept_keys = self._run(
            {
                "to": 100,
                "je": 100,
                "alpha": 100,
                "beta": 100,
                "omega": 100,
            },
            {"to omega": 20, "to alpha": 10, "omega je": 20, "beta je": 10},
            candidate,
            "omega",
            "to alpha beta je",
        )
        self.assertEqual(repaired, "to omega je")
        self.assertEqual(reviewer.calls, 1)
        for probe in (
            ("to omega", 2),
            ("to alpha", 2),
            ("omega je", 2),
            ("beta je", 2),
        ):
            self.assertIn(probe, accept_keys)
        for key, length in accept_keys:
            self.assertEqual(length, 2, f"spanning ngram {key!r} queried")

    def test_censored_internal_phrase_abstains(self) -> None:
        candidate = Candidate(3, 13, "alpha beta", 0.5, {})
        repaired, reviewer, accept_keys = self._run(
            {
                "to": 100,
                "je": 100,
                "alpha": 100,
                "beta": 100,
                "omega": 100,
                "gamma": 100,
            },
            {"to omega": 20, "to alpha": 10},
            candidate,
            "omega gamma",
            "to alpha beta je",
        )
        self.assertEqual(repaired, "to alpha beta je")
        self.assertEqual(reviewer.calls, 1)
        # the internal replacement adjacency is checked FIRST and its
        # censored absence is not positive support.
        self.assertEqual(accept_keys[0], ("omega gamma", 2))
        for key, length in accept_keys:
            self.assertEqual(length, 2, f"spanning ngram {key!r} queried")


class _DelayedSseMainUpstream(BaseHTTPRequestHandler):
    """Owned fake MAIN endpoint for the delayed-stream round trip.

    Streams the real SSE prefix (delta / part-done / item-done frames),
    flushes it, then delays before the held completion tail.  The exact
    declared Content-Length keeps the real proxy reading across the
    delay; only the main endpoint is synthetic, the proxy, bounded
    capture, engine, corpus, Pandoc, reviewer and parser stay real."""

    protocol_version = "HTTP/1.1"
    source: bytes = b""
    delay: float = 0.3
    recorded: list[dict[str, object]] = []
    review_count_before_tail: int = -1
    split_index: int = -1
    prefix_sent_at: float = -1.0
    tail_sent_at: float = -1.0

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        self.__class__.recorded.append(
            {"path": self.path, "headers": dict(self.headers.items()), "body": body}
        )
        marker = b'{"type":"response.completed"'
        index = self.source.rfind(marker)
        if index < 0:
            prefix, tail = self.source, b""
        else:
            prefix, tail = self.source[:index], self.source[index:]
        self.__class__.split_index = index
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Content-Length", str(len(prefix) + len(tail)))
        self.end_headers()
        self.wfile.write(prefix)
        self.wfile.flush()
        self.__class__.prefix_sent_at = time.monotonic()
        time.sleep(self.delay)
        self.__class__.review_count_before_tail = len(_FakeUpstream.recorded)
        self.wfile.write(tail)
        self.wfile.flush()
        self.__class__.tail_sent_at = time.monotonic()

    def log_message(self, *_args: object) -> None:
        return


class HttpRoundTripTests(unittest.TestCase):
    """R8: real proxy HTTP -> real engine -> real ResponsesReviewer ->
    real read-only corpus and qualified Pandoc; only the main/review
    HTTP endpoints are synthetic."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _db(
        self,
        unigrams: Mapping[str, int],
        bigrams: Mapping[str, int],
    ) -> Path:
        return _composed_db(self.root, unigrams, bigrams)

    def _harness(self, db: Path) -> _Harness:
        harness = _Harness()
        self.addCleanup(harness.close)
        harness.engine.index = db
        return harness

    def test_json_useful_edit_renders_repaired_text(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "one": 50},
            {"to one": 20, "to wone": 10},
        )
        harness = self._harness(db)
        answer = "to wone je"
        _MainUpstream.source = _json_completed(answer)
        _FakeUpstream.payload = _review_payload([_prop("t0", False, "one")])
        status, payload = harness.post(_contract_body(False, input_text=answer))
        self.assertEqual(status, 200)
        self.assertEqual(_answer_text(payload), "to one je")
        self.assertEqual(len(_FakeUpstream.recorded), 1)

    def test_json_unsupported_edit_returns_exact_raw_bytes(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "one": 50},
            {"to wone": 10},
        )
        harness = self._harness(db)
        answer = "to wone je"
        _MainUpstream.source = _json_completed(answer)
        _FakeUpstream.payload = _review_payload([_prop("t0", False, "one")])
        status, payload = harness.post(_contract_body(False, input_text=answer))
        self.assertEqual(status, 200)
        self.assertEqual(payload, _MainUpstream.source)
        self.assertEqual(len(_FakeUpstream.recorded), 1)

    def test_sse_slow_reviewer_useful_edit_renders_completed_text(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "one": 50},
            {"to one": 20, "to wone": 10},
        )
        harness = self._harness(db)
        answer = "to wone je"
        _MainUpstream.content_type = "text/event-stream"
        _MainUpstream.source = _tc_baseline(answer)
        _FakeUpstream.payload = _review_payload([_prop("t0", False, "one")])
        _FakeUpstream.delay = 0.2
        self.addCleanup(lambda: setattr(_FakeUpstream, "delay", 0.0))
        status, payload = harness.post(_contract_body(True, input_text=answer))
        self.assertEqual(status, 200)
        self.assertEqual(_sse_completed_text(payload), "to one je")
        self.assertEqual(len(_FakeUpstream.recorded), 1)

    def test_delayed_main_sse_useful_edit_renders_completed_text(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "one": 50},
            {"to one": 20, "to wone": 10},
        )
        harness = self._harness(db)
        original_handler = harness.main_server.RequestHandlerClass
        self.addCleanup(
            setattr,
            harness.main_server,
            "RequestHandlerClass",
            original_handler,
        )
        harness.main_server.RequestHandlerClass = _DelayedSseMainUpstream
        answer = "to wone je"
        _DelayedSseMainUpstream.source = _tc_baseline(answer)
        _DelayedSseMainUpstream.delay = 0.3
        _DelayedSseMainUpstream.recorded = []
        _DelayedSseMainUpstream.review_count_before_tail = -1
        _DelayedSseMainUpstream.split_index = -1
        _DelayedSseMainUpstream.prefix_sent_at = -1.0
        _DelayedSseMainUpstream.tail_sent_at = -1.0
        self.addCleanup(lambda: setattr(_DelayedSseMainUpstream, "delay", 0.0))
        _FakeUpstream.payload = _review_payload([_prop("t0", False, "one")])
        status, payload = harness.post(_contract_body(True, input_text=answer))
        self.assertEqual(status, 200)
        self.assertEqual(len(_DelayedSseMainUpstream.recorded), 1)
        # The real main stream was split at the completion event: the
        # delta / part-done / item-done frames were sent and flushed
        # first, the completed event was held across the delay, and the
        # proxy read the full declared Content-Length across it.
        self.assertGreater(_DelayedSseMainUpstream.split_index, 0)
        self.assertLess(
            _DelayedSseMainUpstream.split_index, len(_DelayedSseMainUpstream.source)
        )
        # The held tail was actually delayed after the flushed prefix.
        self.assertGreaterEqual(
            _DelayedSseMainUpstream.tail_sent_at
            - _DelayedSseMainUpstream.prefix_sent_at,
            _DelayedSseMainUpstream.delay,
        )
        # Exactly one real review call, and only AFTER the main response
        # had completed: zero review observations before the tail.
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        self.assertEqual(_DelayedSseMainUpstream.review_count_before_tail, 0)
        # Useful final repair: every answer copy updated, no partial
        # original left in the returned stream.
        self.assertEqual(_sse_completed_text(payload), "to one je")
        self.assertIn(b"to one je", payload)
        self.assertNotIn(b"to wone je", payload)

    def test_same_proxy_next_healthy_request_zero_review(self) -> None:
        db = self._db(
            {"to": 100, "je": 100, "wone": 2, "one": 50},
            {"to one": 20, "to wone": 10},
        )
        harness = self._harness(db)
        answer = "to wone je"
        _MainUpstream.source = _json_completed(answer)
        _FakeUpstream.payload = _review_payload([_prop("t0", False, "one")])
        status, payload = harness.post(_contract_body(False, input_text=answer))
        self.assertEqual(status, 200)
        self.assertEqual(_answer_text(payload), "to one je")
        # The SAME proxy then serves a healthy answer: zero detector
        # candidates, zero new review calls, raw envelope returned.
        healthy = "to je je"
        _MainUpstream.source = _json_completed(healthy)
        status, payload = harness.post(_contract_body(False, input_text=healthy))
        self.assertEqual(status, 200)
        self.assertEqual(payload, _MainUpstream.source)
        self.assertEqual(len(_FakeUpstream.recorded), 1)


if __name__ == "__main__":
    unittest.main()
