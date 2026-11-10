"""EXPERIMENTAL / CONCEPT VERIFICATION / NOT PRODUCTION CODE.
Runtime detection (order 029-b).

Source-scale acceptance coverage for the corrected source-compatible
selector: the fixed-anchor WORD alarm and the grouped 2-4 unit PHRASE
target produced BEFORE review, the shared lexical / maximal-original /
grapheme gate before any target assignment, the safe non-positive
maximum, the over-4 / over-128 whole-run abstention, the ordinary
TAB/LF/CR prose-boundary controls, legacy-scoring equivalence and the
exact owned query schedule, all over real owned SQLite.  The real
RepairEngine and the actual ConceptProxy HTTP round trips (JSON word
and genuinely held-main delayed-SSE phrase) prove the useful outcomes
end to end; only the external main/review loopback-0 upstreams and the
scripted reviewer are synthetic.  Software proof only - never native
Qwen or quality evidence.
"""

from __future__ import annotations

import http.client
import json
import sqlite3
import sys
import tempfile
import threading
import unittest
from collections.abc import Callable
from http.server import HTTPServer
from pathlib import Path
from typing import cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import proxy  # noqa: E402
from batch_review import BatchProposal, BatchTarget  # noqa: E402
from detector import Candidate  # noqa: E402
from detector import detect as _raw_detect  # noqa: E402
from protected import Interval  # noqa: E402
from proxy import RepairEngine, Reviewer  # noqa: E402
from qwen_client import ResponsesReviewer  # noqa: E402
from runtime_corpus import RuntimeCorpus  # noqa: E402
from runtime_detection import (  # noqa: E402
    PHRASE_ALARM_SCORE,
    PHRASE_MAX_CODEPOINTS,
    WORD_ALARM_SCORE,
    detect,
)
from tests.test_responses_contract import (  # noqa: E402
    _json_completed,
    _MainUpstream,
    _review_payload,
)
from tests.test_review_batch import (  # noqa: E402
    _contract_body,
    _FakeUpstream,
    _prop,
    _real_spec,
    _ScriptedBatchReviewer,
    _tc_baseline,
)

from corpus import Corpus  # noqa: E402

# Source-scale synthetic evidence (order 029-b, R5): known units at
# 100000, original contexts at 3000, fixed-anchor alternatives at 6000.
KNOWN = 100000
CONTEXT = 3000
SUPPORT = 6000
WORD_TEXT = "to alpha je"
PHRASE_TEXT = "to alpha beta je"
HEALTHY_TEXT = "to je tako"
_MAIN_KEY = "main-key-029b-synthetic"
_REVIEW_KEY = "review-key-029b-synthetic"

_WORD_UNIGRAMS: tuple[tuple[str, int], ...] = (
    ("to", KNOWN),
    ("je", KNOWN),
    ("alpha", KNOWN),
    ("omega", KNOWN),
)
_WORD_BIGRAMS: tuple[tuple[str, int], ...] = (
    ("to alpha", CONTEXT),
    ("alpha je", CONTEXT),
    ("to omega", SUPPORT),
    ("omega je", SUPPORT),
)
_WORD_TRIGRAMS: tuple[tuple[str, int], ...] = (
    ("to alpha je", CONTEXT),
    ("to omega je", SUPPORT),
)
_WORD_MIDDLES: tuple[tuple[str, str, str, int], ...] = (
    ("to", "je", "alpha", CONTEXT),
    ("to", "je", "omega", SUPPORT),
)
_PHRASE_UNIGRAMS: tuple[tuple[str, int], ...] = (
    ("to", KNOWN),
    ("je", KNOWN),
    ("alpha", KNOWN),
    ("beta", KNOWN),
    ("omega", KNOWN),
    ("theta", KNOWN),
)
_PHRASE_BIGRAMS: tuple[tuple[str, int], ...] = (
    ("to alpha", CONTEXT),
    ("alpha beta", CONTEXT),
    ("beta je", CONTEXT),
    ("to omega", SUPPORT),
    ("omega theta", SUPPORT),
    ("theta je", SUPPORT),
)
_PHRASE_TRIGRAMS: tuple[tuple[str, int], ...] = (
    ("to alpha beta", CONTEXT),
    ("alpha beta je", CONTEXT),
    ("to omega beta", SUPPORT),
    ("alpha theta je", SUPPORT),
)
_PHRASE_MIDDLES: tuple[tuple[str, str, str, int], ...] = (
    ("to", "beta", "alpha", CONTEXT),
    ("to", "beta", "omega", SUPPORT),
    ("alpha", "je", "beta", CONTEXT),
    ("alpha", "je", "theta", SUPPORT),
)
_TAKO: tuple[tuple[str, int], ...] = (("tako", KNOWN),)
_TAKO = (("tako", KNOWN),)


def _db(
    root: Path,
    name: str,
    *,
    unigrams: tuple[tuple[str, int], ...] = (),
    bigrams: tuple[tuple[str, int], ...] = (),
    trigrams: tuple[tuple[str, int], ...] = (),
    middles: tuple[tuple[str, str, str, int], ...] = (),
) -> Path:
    """One owned tiny read-only evidence index (the standard five tables)."""
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
    for word, count in unigrams:
        connection.execute("INSERT INTO unigram VALUES (?,?)", (word, count))
    for phrase, count in bigrams:
        connection.execute("INSERT INTO bigram VALUES (?,?)", (phrase, count))
    for phrase, count in trigrams:
        connection.execute("INSERT INTO trigram VALUES (?,?)", (phrase, count))
    for left, right, middle, count in middles:
        connection.execute(
            "INSERT INTO middle VALUES (?,?,?,?)", (left, right, middle, count)
        )
    connection.commit()
    connection.close()
    return db


def _word_db(root: Path, name: str = "word.sqlite") -> Path:
    return _db(
        root,
        name,
        unigrams=_WORD_UNIGRAMS,
        bigrams=_WORD_BIGRAMS,
        trigrams=_WORD_TRIGRAMS,
        middles=_WORD_MIDDLES,
    )


def _phrase_db(root: Path, name: str = "phrase.sqlite") -> Path:
    return _db(
        root,
        name,
        unigrams=_PHRASE_UNIGRAMS,
        bigrams=_PHRASE_BIGRAMS,
        trigrams=_PHRASE_TRIGRAMS,
        middles=_PHRASE_MIDDLES,
    )


def _unknown_db(root: Path, name: str = "unknown.sqlite") -> Path:
    """The word rows without the alpha unigram: a known-context unknown."""
    return _db(
        root,
        name,
        unigrams=tuple(
            item for item in _WORD_UNIGRAMS if item[0] != "alpha"
        ),
        bigrams=_WORD_BIGRAMS[:2],
        trigrams=_WORD_TRIGRAMS[:1],
        middles=_WORD_MIDDLES,
    )


def _http_db(root: Path, name: str = "http.sqlite") -> Path:
    """Word control plus phrase control plus the known healthy unit."""
    unigrams = {
        word: count
        for word, count in (*_WORD_UNIGRAMS, *_PHRASE_UNIGRAMS, *_TAKO)
    }
    bigrams = {
        phrase: count
        for phrase, count in (*_WORD_BIGRAMS, *_PHRASE_BIGRAMS)
    }
    trigrams = {
        phrase: count
        for phrase, count in (*_WORD_TRIGRAMS, *_PHRASE_TRIGRAMS)
    }
    middles = {
        (left, right, middle): count
        for left, right, middle, count in (*_WORD_MIDDLES, *_PHRASE_MIDDLES)
    }
    return _db(
        root,
        name,
        unigrams=tuple(unigrams.items()),
        bigrams=tuple(bigrams.items()),
        trigrams=tuple(trigrams.items()),
        middles=tuple(
            (left, right, middle, count)
            for (left, right, middle), count in middles.items()
        ),
    )


def _shape(candidates: object) -> list[tuple[int, int, str, float]]:
    return [
        (candidate.start, candidate.end, candidate.text, candidate.score)
        for candidate in cast("list[Candidate]", candidates)
    ]


class SelectorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _word_db(self.root)
        self.corpus = Corpus(self.db)
        self.phrase_db = _phrase_db(self.root)

    def tearDown(self) -> None:
        self.corpus.close()
        self.temp.cleanup()

class WordAlarmSelectorTests(SelectorTestCase):
    def test_word_control_fixed_anchor_alarm(self) -> None:
        result = detect(WORD_TEXT, self.corpus)
        self.assertEqual(_shape(result), [(3, 8, "alpha", WORD_ALARM_SCORE)])
        evidence = result[0].evidence
        trigram = cast(dict[str, object], evidence["trigram"])
        self.assertEqual(trigram["state"], "EXACT")
        self.assertEqual(trigram["count"], CONTEXT)

    def test_unigram_only_mode_gains_no_context_alarm(self) -> None:
        self.assertEqual(detect(WORD_TEXT, self.corpus, mode="unigram-only"), [])

    def test_same_word_maximum_four_useful(self) -> None:
        for maximum in (1, 2, 3, 4, 8):
            result = detect(WORD_TEXT, self.corpus, maximum=maximum)
            self.assertEqual(_shape(result), [(3, 8, "alpha", WORD_ALARM_SCORE)])

    def test_tab_gaps_are_horizontal(self) -> None:
        for text in ("to\talpha je", "to alpha\tje", "to alpha \t je"):
            self.assertEqual(_shape(detect(text, self.corpus)),
                             [(3, 8, "alpha", WORD_ALARM_SCORE)])

    def test_newline_barriers_never_alarm(self) -> None:
        for text in ("to alpha\nje", "to alpha\r\nje"):
            self.assertEqual(detect(text, self.corpus), [])

    def test_below_two_x_contrast_no_alarm(self) -> None:
        db = _db(
            self.root,
            "below2x.sqlite",
            unigrams=_WORD_UNIGRAMS,
            bigrams=_WORD_BIGRAMS,
            trigrams=_WORD_TRIGRAMS,
            middles=(("to", "je", "omega", SUPPORT - 1),),
        )
        corpus = Corpus(db)
        try:
            self.assertEqual(detect(WORD_TEXT, corpus), [])
        finally:
            corpus.close()

    def test_exact_two_x_boundary_alarms(self) -> None:
        result = detect(WORD_TEXT, self.corpus)  # SUPPORT == 2 * CONTEXT
        self.assertEqual(_shape(result), [(3, 8, "alpha", WORD_ALARM_SCORE)])

    def test_high_alternative_exclusions_never_support(self) -> None:
        # Genuine R6 negatives: the alternative count is HIGH (6000 >=
        # 2*3000 centered trigram), so each case is blocked ONLY by the
        # identity, the casefold-identity or the lexical exclusion - no
        # distinct valid supporting alternative exists in any index.
        for middle in ("alpha", "ALPHA", "zork_7"):
            with self.subTest(middle=middle):
                db = _db(
                    self.root,
                    f"alt-{middle}.sqlite",
                    unigrams=_WORD_UNIGRAMS,
                    bigrams=_WORD_BIGRAMS,
                    trigrams=_WORD_TRIGRAMS,
                    middles=(("to", "je", middle, SUPPORT),),
                )
                corpus = Corpus(db)
                try:
                    self.assertEqual(detect(WORD_TEXT, corpus), [])
                finally:
                    corpus.close()

    def test_zero_centered_trigram_uses_floor_of_one(self) -> None:
        rows = {
            "unigrams": _WORD_UNIGRAMS,
            "bigrams": _WORD_BIGRAMS,
            "trigrams": (("to alpha je", 0),),
        }
        corpus = Corpus(
            _db(self.root, "floor.sqlite", middles=(("to", "je", "omega", 2),), **rows)
        )
        try:
            self.assertEqual(
                _shape(detect(WORD_TEXT, corpus)),
                [(3, 8, "alpha", WORD_ALARM_SCORE)],
            )
        finally:
            corpus.close()
        corpus = Corpus(
            _db(self.root, "floor-below.sqlite", middles=(("to", "je", "omega", 1),), **rows)
        )
        try:
            self.assertEqual(detect(WORD_TEXT, corpus), [])
        finally:
            corpus.close()

    def test_unknown_original_huge_alternatives_legacy_only(self) -> None:
        db = _db(
            self.root,
            "huge-alt.sqlite",
            unigrams=(("to", KNOWN), ("je", KNOWN)),
            bigrams=_WORD_BIGRAMS[:2],
            trigrams=_WORD_TRIGRAMS[:1],
            middles=(("to", "je", "omega", 999999),),
        )
        corpus = Corpus(db)
        try:
            self.assertEqual(
                _shape(detect(WORD_TEXT, corpus, mode="unigram-only")),
                [(3, 8, "alpha", 1.0)],
            )
            self.assertEqual(_shape(detect(WORD_TEXT, corpus)), [(3, 8, "alpha", 0.7)])
        finally:
            corpus.close()

    def test_censored_centered_trigram_no_signal(self) -> None:
        db = _db(
            self.root,
            "censored.sqlite",
            unigrams=_WORD_UNIGRAMS,
            bigrams=_WORD_BIGRAMS[:2],
            trigrams=(),
            middles=(("to", "je", "omega", 999999),),
        )
        corpus = Corpus(db)
        try:
            self.assertEqual(detect(WORD_TEXT, corpus), [])
        finally:
            corpus.close()

    def test_known_zero_bigram_no_signal(self) -> None:
        db = _db(
            self.root,
            "zerobigram.sqlite",
            unigrams=_WORD_UNIGRAMS,
            bigrams=(("to alpha", 0), ("alpha je", CONTEXT)),
            trigrams=_WORD_TRIGRAMS[:1],
            middles=(("to", "je", "omega", SUPPORT),),
        )
        corpus = Corpus(db)
        try:
            self.assertEqual(detect(WORD_TEXT, corpus), [])
        finally:
            corpus.close()

    def test_anchor_below_threshold_no_alarm(self) -> None:
        db = _db(
            self.root,
            "anchor3.sqlite",
            unigrams=(("to", KNOWN), ("je", 3), ("alpha", KNOWN), ("omega", KNOWN)),
            bigrams=_WORD_BIGRAMS[:2],
            trigrams=_WORD_TRIGRAMS[:1],
            middles=(("to", "je", "omega", SUPPORT),),
        )
        corpus = Corpus(db)
        try:
            result = detect(WORD_TEXT, corpus)
            self.assertNotIn((3, 8, "alpha", WORD_ALARM_SCORE), _shape(result))
        finally:
            corpus.close()

    def test_original_count_equal_threshold_no_alarm(self) -> None:
        db = _db(
            self.root,
            "eqthreshold.sqlite",
            unigrams=(("to", KNOWN), ("je", KNOWN), ("alpha", 3), ("omega", KNOWN)),
            bigrams=_WORD_BIGRAMS[:2],
            trigrams=(("to alpha je", 3),),
            middles=(("to", "je", "omega", 6),),
        )
        corpus = Corpus(db)
        try:
            result = detect(WORD_TEXT, corpus)
            self.assertNotIn((3, 8, "alpha", WORD_ALARM_SCORE), _shape(result))
            self.assertIn((3, 8, "alpha", 0.2), _shape(result))
        finally:
            corpus.close()

    def test_nondefault_threshold_honored(self) -> None:
        result = detect(WORD_TEXT, self.corpus, threshold=KNOWN)
        self.assertTrue(all(item[3] <= 0.5 for item in _shape(result)))

    def test_uppercase_original_no_alarm(self) -> None:
        self.assertEqual(detect("to Alpha je", self.corpus), [])

    def test_uppercase_anchor_no_alarm(self) -> None:
        self.assertEqual(detect("To alpha je", self.corpus), [])

    def test_punctuation_barrier_no_alarm(self) -> None:
        self.assertEqual(detect("to alpha, je", self.corpus), [])

    def test_protected_middle_token_no_alarm(self) -> None:
        corpus = Corpus(self.phrase_db)
        try:
            self.assertEqual(
                detect(PHRASE_TEXT, corpus, [Interval(9, 13, "test")]), []
            )
        finally:
            corpus.close()

    def test_digit_unit_no_alarm(self) -> None:
        self.assertEqual(detect("to alpha2 je", self.corpus), [])

class PhraseGroupingSelectorTests(SelectorTestCase):
    def test_two_unit_phrase_single_exact_slice(self) -> None:
        corpus = Corpus(self.phrase_db)
        try:
            result = detect(PHRASE_TEXT, corpus)
            self.assertEqual(
                _shape(result), [(3, 13, "alpha beta", PHRASE_ALARM_SCORE)]
            )
            evidence = result[0].evidence
            self.assertEqual(evidence["context_phrase"], True)
        finally:
            corpus.close()

    def test_tab_phrase_single_exact_slice(self) -> None:
        corpus = Corpus(self.phrase_db)
        try:
            result = detect("to alpha\tbeta je", corpus)
            self.assertEqual(
                _shape(result), [(3, 13, "alpha\tbeta", PHRASE_ALARM_SCORE)]
            )
        finally:
            corpus.close()

    def test_three_unit_phrase_single_exact_slice(self) -> None:
        db = _db(
            self.root,
            "three.sqlite",
            unigrams=(
                ("to", KNOWN), ("je", KNOWN), ("alpha", KNOWN),
                ("beta", KNOWN), ("gamma", KNOWN), ("omega", KNOWN),
            ),
            bigrams=(
                ("to alpha", CONTEXT), ("alpha beta", CONTEXT),
                ("beta gamma", CONTEXT), ("gamma je", CONTEXT),
            ),
            trigrams=(
                ("to alpha beta", CONTEXT), ("alpha beta gamma", CONTEXT),
                ("beta gamma je", CONTEXT),
            ),
            middles=(
                ("to", "beta", "omega", SUPPORT),
                ("alpha", "gamma", "omega", SUPPORT),
                ("beta", "je", "omega", SUPPORT),
            ),
        )
        corpus = Corpus(db)
        try:
            result = detect("to alpha beta gamma je", corpus)
            self.assertEqual(
                _shape(result),
                [(3, 19, "alpha beta gamma", PHRASE_ALARM_SCORE)],
            )
        finally:
            corpus.close()


        corpus = Corpus(self.phrase_db)
        try:
            self.assertEqual(detect("to alpha\nbeta je", corpus), [])
            self.assertEqual(detect("to alpha\r\nbeta je", corpus), [])
        finally:
            corpus.close()

    def test_same_four_unit_run_useful(self) -> None:
        db = _db(
            self.root,
            "four.sqlite",
            unigrams=(
                ("to", KNOWN), ("je", KNOWN), ("alpha", KNOWN),
                ("beta", KNOWN), ("gamma", KNOWN), ("delta", KNOWN),
            ),
            bigrams=(
                ("to alpha", CONTEXT), ("alpha beta", CONTEXT),
                ("beta gamma", CONTEXT), ("gamma delta", CONTEXT),
                ("delta je", CONTEXT),
            ),
            trigrams=(
                ("to alpha beta", CONTEXT), ("alpha beta gamma", CONTEXT),
                ("beta gamma delta", CONTEXT), ("gamma delta je", CONTEXT),
            ),
            middles=(
                ("to", "beta", "omega", SUPPORT),
                ("alpha", "gamma", "omega", SUPPORT),
                ("beta", "delta", "omega", SUPPORT),
                ("gamma", "je", "omega", SUPPORT),
            ),
        )
        corpus = Corpus(db)
        try:
            result = detect("to alpha beta gamma delta je", corpus)
            self.assertEqual(
                _shape(result),
                [(3, 25, "alpha beta gamma delta", PHRASE_ALARM_SCORE)],
            )
        finally:
            corpus.close()

    def test_five_alarm_run_yields_no_targets(self) -> None:
        db = _db(
            self.root,
            "five.sqlite",
            unigrams=(
                ("to", KNOWN), ("je", KNOWN), ("alpha", KNOWN),
                ("beta", KNOWN), ("gamma", KNOWN), ("delta", KNOWN),
                ("epsilon", KNOWN),
            ),
            bigrams=(
                ("to alpha", CONTEXT), ("alpha beta", CONTEXT),
                ("beta gamma", CONTEXT), ("gamma delta", CONTEXT),
                ("delta epsilon", CONTEXT), ("epsilon je", CONTEXT),
            ),
            trigrams=(
                ("to alpha beta", CONTEXT), ("alpha beta gamma", CONTEXT),
                ("beta gamma delta", CONTEXT), ("gamma delta epsilon", CONTEXT),
                ("delta epsilon je", CONTEXT),
            ),
            middles=(
                ("to", "beta", "omega", SUPPORT),
                ("alpha", "gamma", "omega", SUPPORT),
                ("beta", "delta", "omega", SUPPORT),
                ("gamma", "epsilon", "omega", SUPPORT),
                ("delta", "je", "omega", SUPPORT),
            ),
        )
        corpus = Corpus(db)
        text = "to alpha beta gamma delta epsilon je"
        try:
            self.assertEqual(detect(text, corpus), [])
            self.assertEqual(detect(text, corpus, maximum=8), [])
        finally:
            corpus.close()

    def test_over_128_two_unit_run_yields_no_targets(self) -> None:
        first, second = "a" * 70, "b" * 70
        db = _db(
            self.root,
            "over128.sqlite",
            unigrams=(
                ("to", KNOWN), ("je", KNOWN), (first, KNOWN), (second, KNOWN),
                ("omega", KNOWN), ("theta", KNOWN),
            ),
            bigrams=(
                ("to " + first, CONTEXT), (first + " " + second, CONTEXT),
                (second + " je", CONTEXT),
            ),
            trigrams=(
                ("to " + first + " " + second, CONTEXT),
                (first + " " + second + " je", CONTEXT),
            ),
            middles=(("to", second, "omega", SUPPORT), (first, "je", "theta", SUPPORT)),
        )
        corpus = Corpus(db)
        try:
            self.assertEqual(detect("to " + first + " " + second + " je", corpus), [])
        finally:
            corpus.close()

    def test_one_unit_over_128_no_target(self) -> None:
        long_word = "a" * (PHRASE_MAX_CODEPOINTS + 1)
        db = _db(
            self.root,
            "longword.sqlite",
            unigrams=(
                ("to", KNOWN), ("je", KNOWN), (long_word, KNOWN), ("omega", KNOWN),
            ),
            bigrams=(("to " + long_word, CONTEXT), (long_word + " je", CONTEXT)),
            trigrams=(("to " + long_word + " je", CONTEXT),),
            middles=(("to", "je", "omega", SUPPORT),),
        )
        corpus = Corpus(db)
        try:
            self.assertEqual(detect("to " + long_word + " je", corpus), [])
        finally:
            corpus.close()

    def test_one_unit_at_128_stays_a_word(self) -> None:
        word = "a" * PHRASE_MAX_CODEPOINTS
        db = _db(
            self.root,
            "word128.sqlite",
            unigrams=(
                ("to", KNOWN), ("je", KNOWN), (word, KNOWN), ("omega", KNOWN),
            ),
            bigrams=(("to " + word, CONTEXT), (word + " je", CONTEXT)),
            trigrams=(("to " + word + " je", CONTEXT),),
            middles=(("to", "je", "omega", SUPPORT),),
        )
        corpus = Corpus(db)
        try:
            result = detect("to " + word + " je", corpus)
            self.assertEqual(_shape(result), [(3, 131, word, WORD_ALARM_SCORE)])
        finally:
            corpus.close()

    def test_intervening_non_alarm_breaks_run(self) -> None:
        db = _db(
            self.root,
            "breakrun.sqlite",
            unigrams=(
                ("to", KNOWN), ("je", KNOWN), ("alpha", KNOWN),
                ("beta", KNOWN), ("rare", KNOWN),
            ),
            bigrams=(
                ("to alpha", CONTEXT), ("alpha rare", CONTEXT),
                ("rare beta", CONTEXT), ("beta je", CONTEXT),
            ),
            trigrams=(("to alpha rare", CONTEXT), ("rare beta je", CONTEXT)),
            middles=(
                ("to", "rare", "omega", SUPPORT),
                ("rare", "je", "theta", SUPPORT),
            ),
        )
        corpus = Corpus(db)
        try:
            result = detect("to alpha rare beta je", corpus)
            self.assertEqual(
                _shape(result),
                [
                    (3, 8, "alpha", WORD_ALARM_SCORE),
                    (14, 18, "beta", WORD_ALARM_SCORE),
                ],
            )
        finally:
            corpus.close()

    def test_repetition_gets_separate_targets(self) -> None:
        result = detect("to alpha je to alpha je", self.corpus)
        self.assertEqual(
            _shape(result),
            [
                (3, 8, "alpha", WORD_ALARM_SCORE),
                (15, 20, "alpha", WORD_ALARM_SCORE),
            ],
        )

    def test_cap_default_four_and_hard_cap_eight(self) -> None:
        unigrams: tuple[tuple[str, int], ...] = (
            ("to", KNOWN),
            ("je", KNOWN),
            ("omega", KNOWN),
        )
        bigrams: list[tuple[str, int]] = []
        trigrams: list[tuple[str, int]] = []
        words = [
            f"w{chr(ord('a') + index % 26)}{chr(ord('a') + index // 26)}"
            for index in range(10)
        ]
        for word in words:
            unigrams = unigrams + ((word, KNOWN),)
            bigrams.extend(
                [(f"to {word}", CONTEXT), (f"{word} je", CONTEXT)]
            )
            trigrams.append((f"to {word} je", CONTEXT))
        db = _db(
            self.root,
            "cap.sqlite",
            unigrams=unigrams,
            bigrams=tuple(bigrams),
            trigrams=tuple(trigrams),
            middles=(("to", "je", "omega", SUPPORT),),
        )
        corpus = Corpus(db)
        text = " ".join(f"to {word} je" for word in words)
        try:
            self.assertEqual(len(detect(text, corpus)), 4)
            elevated = detect(text, corpus, maximum=10)
            self.assertEqual(len(elevated), 8)
            starts = [item[0] for item in _shape(elevated)]
            self.assertEqual(starts, sorted(starts))
        finally:
            corpus.close()

    def test_deterministic_source_ordered(self) -> None:
        corpus = Corpus(self.phrase_db)
        try:
            first = detect(PHRASE_TEXT, corpus)
            second = detect(PHRASE_TEXT, corpus)
            self.assertEqual(
                [candidate.as_dict() for candidate in first],
                [candidate.as_dict() for candidate in second],
            )
        finally:
            corpus.close()

    def test_legacy_unknown_never_merged_into_phrase(self) -> None:
        corpus = Corpus(self.phrase_db)
        try:
            result = detect("zork " + PHRASE_TEXT, corpus)
            self.assertEqual(
                _shape(result),
                [
                    (0, 4, "zork", 1.0),
                    (8, 18, "alpha beta", PHRASE_ALARM_SCORE),
                ],
            )
        finally:
            corpus.close()


class TargetGateSelectorTests(SelectorTestCase):
    """The shared lexical / maximal-original / grapheme gate is applied
    before ANY target assignment (order 029-b, R1/R2): nonlexical raw
    tokens and fragments of larger machine source units are excluded
    before review, while ordinary prose boundaries stay eligible."""

    def setUp(self) -> None:
        super().setUp()
        self.tiny = _db(
            self.root,
            "tiny.sqlite",
            unigrams=(("to", KNOWN), ("je", KNOWN)),
        )
        self.tiny_corpus = Corpus(self.tiny)

    def tearDown(self) -> None:
        self.tiny_corpus.close()
        super().tearDown()

    def test_nonlexical_nl_unit_not_selected(self) -> None:
        text = "to \u2162 je"
        self.assertEqual(detect(text, self.tiny_corpus), [])
        # The frozen historical detector still selects it: the gate is a
        # new before-review exclusion, not a frozen-source change.
        self.assertEqual(
            _shape(_raw_detect(text, self.tiny_corpus)), [(3, 4, "\u2162", 1.0)]
        )

    def test_digit_fragment_of_machine_unit_not_selected(self) -> None:
        self.assertEqual(detect("to alpha_42 je", self.tiny_corpus), [])

    def test_digit_prefix_fragment_not_selected(self) -> None:
        self.assertEqual(detect("to 42alpha je", self.tiny_corpus), [])

    def test_fragment_does_not_consume_cap_or_obscure(self) -> None:
        result = detect("zork_7 to alpha je", self.corpus)
        self.assertEqual(_shape(result), [(10, 15, "alpha", WORD_ALARM_SCORE)])

    def test_combining_mark_fragments_not_selected(self) -> None:
        result = detect("to al\u0308pha je", self.tiny_corpus)
        self.assertTrue(all(candidate.text in ("to", "je") for candidate in result))

    def test_zero_width_space_fragment_not_selected(self) -> None:
        result = detect("to alpha\u200bje", self.tiny_corpus)
        self.assertTrue(all(candidate.text in ("to", "je") for candidate in result))

    def test_control_character_fragment_not_selected(self) -> None:
        # The named unsafe boundary marks stay excluded even though the
        # ordinary TAB/LF/CR boundaries above stay eligible (order 029-b
        # whitespace review): NUL/VT/FF, NEL/LS/PS, ZWNJ, a variation
        # selector, a regional indicator and an emoji modifier.
        for char in ("\x00", "\x0b", "\x0c", "\u0085", "\u2028",
                     "\u2029", "\u200c", "\ufe0f", "\U0001F1E6",
                     "\U0001F3FB"):
            with self.subTest(char=repr(char)):
                self.assertEqual(detect(f"to alpha{char}je", self.tiny_corpus), [])

    def test_line_terminators_keep_word_eligible(self) -> None:
        db = _unknown_db(self.root)
        corpus = Corpus(db)
        try:
            for text in ("to\talpha je", "to alpha\nje", "to alpha\r\nje", "to alpha je"):
                reference = _raw_detect(text, corpus)
                actual = detect(text, corpus)
                self.assertEqual(
                    [candidate.as_dict() for candidate in actual],
                    [candidate.as_dict() for candidate in reference],
                )
        finally:
            corpus.close()

    def test_tab_boundary_alarms_and_newline_gap_does_not(self) -> None:
        for text in ("to\talpha je", "to alpha\tje"):
            self.assertEqual(_shape(detect(text, self.corpus)),
                             [(3, 8, "alpha", WORD_ALARM_SCORE)])
        for text in ("to alpha\nje", "to alpha\r\nje"):
            self.assertEqual(detect(text, self.corpus), [])

    def test_punctuation_boundary_keeps_legacy_eligible(self) -> None:
        result = detect("to zork, je", self.tiny_corpus)
        self.assertEqual(_shape(result), [(3, 7, "zork", 1.0)])

    def test_ineligible_context_unit_never_anchors(self) -> None:
        self.assertEqual(detect("to alpha_42 je", self.corpus), [])


class LegacyEquivalenceAndScheduleTests(SelectorTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tiny = _db(
            self.root,
            "tiny.sqlite",
            unigrams=(("to", KNOWN), ("je", KNOWN)),
        )
        self.tiny_corpus = Corpus(self.tiny)

    def tearDown(self) -> None:
        self.tiny_corpus.close()
        super().tearDown()

    def _legacy_corpus(self, name: str = "legacy.sqlite") -> Corpus:
        db = _db(
            self.root,
            name,
            unigrams=(("to", 1), ("alpha", 1), ("je", 2), ("wone", 2)),
            bigrams=(("to alpha", 1),),
        )
        return Corpus(db)

    def test_legacy_scoring_equivalence_clean_fixtures(self) -> None:
        corpus = self._legacy_corpus()
        text = "to alpha je to alpha je wone"
        try:
            for mode in ("local-context", "unigram-only"):
                for maximum in (1, 2, 4):
                    reference = _raw_detect(text, corpus, None, mode=mode, maximum=maximum)
                    actual = detect(text, corpus, None, mode=mode, maximum=maximum)
                    self.assertEqual(
                        [candidate.as_dict() for candidate in actual],
                        [candidate.as_dict() for candidate in reference],
                    )
        finally:
            corpus.close()

    def test_legacy_equivalence_with_protection_intervals(self) -> None:
        corpus = self._legacy_corpus()
        text = "to alpha je to alpha je wone"
        intervals = [Interval(3, 8, "test")]
        try:
            reference = _raw_detect(text, corpus, intervals, mode="local-context")
            actual = detect(text, corpus, intervals, mode="local-context")
            self.assertEqual(
                [candidate.as_dict() for candidate in actual],
                [candidate.as_dict() for candidate in reference],
            )
        finally:
            corpus.close()

    def test_nonpositive_maximum_returns_no_targets(self) -> None:
        for maximum in (0, -3):
            self.assertEqual(detect(WORD_TEXT, self.corpus, maximum=maximum), [])

    def test_query_schedule_matches_raw_detect(self) -> None:
        cases: tuple[tuple[str, Path, int], ...] = (
            (WORD_TEXT, self.db, 3),
            (PHRASE_TEXT, self.phrase_db, 4),
        )
        five_db = _db(
            self.root,
            "five-schedule.sqlite",
            unigrams=(
                ("to", KNOWN), ("je", KNOWN), ("alpha", KNOWN),
                ("beta", KNOWN), ("gamma", KNOWN), ("delta", KNOWN),
                ("epsilon", KNOWN),
            ),
            bigrams=(
                ("to alpha", CONTEXT), ("alpha beta", CONTEXT),
                ("beta gamma", CONTEXT), ("gamma delta", CONTEXT),
                ("delta epsilon", CONTEXT), ("epsilon je", CONTEXT),
            ),
            trigrams=(
                ("to alpha beta", CONTEXT), ("alpha beta gamma", CONTEXT),
                ("beta gamma delta", CONTEXT), ("gamma delta epsilon", CONTEXT),
                ("delta epsilon je", CONTEXT),
            ),
            middles=(
                ("to", "beta", "omega", SUPPORT),
                ("alpha", "gamma", "omega", SUPPORT),
                ("beta", "delta", "omega", SUPPORT),
                ("gamma", "epsilon", "omega", SUPPORT),
                ("delta", "je", "omega", SUPPORT),
            ),
        )
        cases = cases + (("to alpha beta gamma delta epsilon je", five_db, 7),)
        for text, db, tokens in cases:
            expected = 5 + (5 * tokens - 6)
            owned = RuntimeCorpus(db)
            try:
                detect(text, owned)
                new_statements = owned._budget.statements
            finally:
                owned.close()
            raw_owned = RuntimeCorpus(db)
            try:
                _raw_detect(text, raw_owned)
                raw_statements = raw_owned._budget.statements
            finally:
                raw_owned.close()
            self.assertEqual(new_statements, expected, (text, tokens))
            self.assertEqual(raw_statements, expected, (text, tokens))

    def test_schedule_held_on_empty_selection_controls(self) -> None:
        owned = RuntimeCorpus(self.db)
        try:
            self.assertEqual(detect(WORD_TEXT, owned, maximum=0), [])
            self.assertEqual(owned._budget.statements, 14)
        finally:
            owned.close()
        owned = RuntimeCorpus(self.tiny)
        try:
            self.assertEqual(detect("to \u2162 je", owned), [])
            self.assertEqual(owned._budget.statements, 14)
        finally:
            owned.close()

    def test_index_bytes_unchanged_and_owned_close(self) -> None:
        before = self.db.read_bytes()
        directory_files = sorted(path.name for path in self.root.iterdir())
        corpus = RuntimeCorpus(self.db)
        try:
            detect(WORD_TEXT, corpus)
        finally:
            corpus.close()
        self.assertEqual(self.db.read_bytes(), before)
        self.assertEqual(
            sorted(path.name for path in self.root.iterdir()), directory_files
        )

    def test_unknown_mode_rejected(self) -> None:
        with self.assertRaises(ValueError):
            detect(WORD_TEXT, self.corpus, mode="unknown")


class _ScheduledCorpus(RuntimeCorpus):
    def __init__(self, path: str | Path) -> None:
        super().__init__(path)
        self.close_calls = 0

    def close(self) -> None:
        self.close_calls += 1
        super().close()


def _replace_with(
    replacement: str,
) -> Callable[[str, tuple[BatchTarget, ...]], dict[str, BatchProposal]]:
    def responder(
        sentence: str, targets: tuple[BatchTarget, ...]
    ) -> dict[str, BatchProposal]:
        return {
            target.id: BatchProposal(target.id, False, replacement, False)
            for target in targets
        }

    return responder


def _keep_all(
    sentence: str, targets: tuple[BatchTarget, ...]
) -> dict[str, BatchProposal]:
    return {
        target.id: BatchProposal(target.id, True, None, False) for target in targets
    }


def _wider_all(
    sentence: str, targets: tuple[BatchTarget, ...]
) -> dict[str, BatchProposal]:
    return {
        target.id: BatchProposal(target.id, True, None, True) for target in targets
    }


class EngineProofTests(unittest.TestCase):
    """Real RepairEngine with real Pandoc and real owned SQLite; only
    the scripted reviewer is synthetic (order 029-b, R5/R6)."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.word_db = _word_db(self.root)
        self.phrase_db = _phrase_db(self.root)
        self.http_db = _http_db(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _engine(self, db: Path, reviewer: Reviewer) -> RepairEngine:
        return RepairEngine(db, reviewer, pandoc=_real_spec())

    def test_word_useful_target_assigned_before_one_review(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_with("omega"))
        engine = self._engine(self.word_db, reviewer)
        engine.begin_request()
        repaired = engine.repair(WORD_TEXT)
        self.assertEqual(repaired, "to omega je")
        self.assertEqual(reviewer.calls, 1)
        sentence, targets = reviewer.sent[0]
        self.assertEqual(sentence, WORD_TEXT)
        self.assertEqual([target.target for target in targets], ["alpha"])
        self.assertEqual(targets[0].before_target, "to ")
        self.assertEqual(targets[0].after_target, " je")
        details = engine.take_details()
        self.assertEqual(len(details), 1)
        detail = details[0]
        self.assertEqual(
            detail["review_batch"],
            {
                "calls": 1,
                "targets": 1,
                "outcome": "ok",
                "reason": None,
                "usage": "unknown",
            },
        )
        acceptance = cast(list[dict[str, object]], detail["acceptance"])
        self.assertEqual(acceptance[0]["accepted"], True)
        self.assertEqual(acceptance[0]["reason"], "accepted-independent-evidence")
        self.assertEqual(detail["replacements"], ["omega"])

    def test_phrase_useful_whole_span_one_review(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_with("omega theta"))
        engine = self._engine(self.phrase_db, reviewer)
        engine.begin_request()
        repaired = engine.repair(PHRASE_TEXT)
        self.assertEqual(repaired, "to omega theta je")
        self.assertEqual(reviewer.calls, 1)
        _sentence, targets = reviewer.sent[0]
        self.assertEqual([target.target for target in targets], ["alpha beta"])
        self.assertEqual(targets[0].before_target, "to ")
        self.assertEqual(targets[0].after_target, " je")
        details = engine.take_details()
        acceptance = cast(list[dict[str, object]], details[0]["acceptance"])
        self.assertEqual(acceptance[0]["accepted"], True)
        self.assertEqual(acceptance[0]["reason"], "accepted-independent-evidence")
        self.assertEqual(details[0]["replacements"], ["omega theta"])

    def test_keep_is_noop(self) -> None:
        reviewer = _ScriptedBatchReviewer(_keep_all)
        engine = self._engine(self.word_db, reviewer)
        engine.begin_request()
        self.assertEqual(engine.repair(WORD_TEXT), WORD_TEXT)
        self.assertEqual(reviewer.calls, 1)
        acceptance = cast(
            list[dict[str, object]], engine.take_details()[0]["acceptance"]
        )
        self.assertEqual(acceptance[0]["reason"], "reviewer-kept")

    def test_wider_is_noop(self) -> None:
        reviewer = _ScriptedBatchReviewer(_wider_all)
        engine = self._engine(self.word_db, reviewer)
        engine.begin_request()
        self.assertEqual(engine.repair(WORD_TEXT), WORD_TEXT)
        acceptance = cast(
            list[dict[str, object]], engine.take_details()[0]["acceptance"]
        )
        self.assertEqual(acceptance[0]["reason"], "reviewer-kept")

    def test_invalid_replacement_rejected(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_with("zeta"))
        engine = self._engine(self.word_db, reviewer)
        engine.begin_request()
        self.assertEqual(engine.repair(WORD_TEXT), WORD_TEXT)
        acceptance = cast(
            list[dict[str, object]], engine.take_details()[0]["acceptance"]
        )
        self.assertEqual(acceptance[0]["reason"], "replacement-unigram-uncertain")

    def test_oversize_replacement_rejected(self) -> None:
        reviewer = _ScriptedBatchReviewer(
            _replace_with("omega gamma delta epsilon zeta")
        )
        engine = self._engine(self.word_db, reviewer)
        engine.begin_request()
        self.assertEqual(engine.repair(WORD_TEXT), WORD_TEXT)
        acceptance = cast(
            list[dict[str, object]], engine.take_details()[0]["acceptance"]
        )
        self.assertEqual(acceptance[0]["reason"], "replacement-size")

    def test_nonlexical_replacement_rejected(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_with("omega2"))
        engine = self._engine(self.word_db, reviewer)
        engine.begin_request()
        self.assertEqual(engine.repair(WORD_TEXT), WORD_TEXT)
        acceptance = cast(
            list[dict[str, object]], engine.take_details()[0]["acceptance"]
        )
        self.assertEqual(acceptance[0]["reason"], "replacement-not-lexical")

    def test_high_identity_alternative_zero_calls(self) -> None:
        # Genuine high self/casefold-identical/nonlexical alternative
        # (6000 >= 2*3000 centered trigram): the zero-call outcome can
        # only come from the alternative exclusions, never from count.
        for middle in ("alpha", "ALPHA", "zork_7"):
            with self.subTest(middle=middle):
                db = _db(
                    self.root,
                    f"engine-alt-{middle}.sqlite",
                    unigrams=_WORD_UNIGRAMS,
                    bigrams=_WORD_BIGRAMS,
                    trigrams=_WORD_TRIGRAMS,
                    middles=(("to", "je", middle, SUPPORT),),
                )
                reviewer = _ScriptedBatchReviewer(_replace_with("omega"))
                engine = self._engine(db, reviewer)
                engine.begin_request()
                self.assertEqual(engine.repair(WORD_TEXT), WORD_TEXT)
                self.assertEqual(reviewer.calls, 0)

    def test_safe_known_zero_calls(self) -> None:
        reviewer = _ScriptedBatchReviewer(_replace_with("tako"))
        engine = self._engine(self.http_db, reviewer)
        engine.begin_request()
        self.assertEqual(engine.repair(HEALTHY_TEXT), HEALTHY_TEXT)
        self.assertEqual(reviewer.calls, 0)
        detail = engine.take_details()[0]
        self.assertEqual(
            detail["review_batch"],
            {
                "calls": 0,
                "targets": 0,
                "outcome": "skipped",
                "reason": None,
                "usage": "unknown",
            },
        )

    def test_engine_query_schedule_and_close(self) -> None:
        captured: list[_ScheduledCorpus] = []

        def tracked(path: str | Path) -> _ScheduledCorpus:
            corpus = _ScheduledCorpus(path)
            captured.append(corpus)
            return corpus

        reviewer = _ScriptedBatchReviewer(_replace_with("tako"))
        engine = self._engine(self.http_db, reviewer)
        with mock.patch.object(proxy, "RuntimeCorpus", tracked):
            engine.begin_request()
            self.assertEqual(engine.repair(HEALTHY_TEXT), HEALTHY_TEXT)
        self.assertEqual(len(captured), 1)
        self.assertEqual(captured[0]._budget.statements, 14)
        self.assertEqual(captured[0].close_calls, 1)

        captured.clear()
        reviewer = _ScriptedBatchReviewer(_keep_all)
        engine = self._engine(self.phrase_db, reviewer)
        with mock.patch.object(proxy, "RuntimeCorpus", tracked):
            engine.begin_request()
            self.assertEqual(engine.repair(PHRASE_TEXT), PHRASE_TEXT)
        self.assertEqual(len(captured), 1)
        self.assertEqual(captured[0]._budget.statements, 19)
        self.assertEqual(captured[0].close_calls, 1)

    def test_engine_index_bytes_unchanged(self) -> None:
        before = self.phrase_db.read_bytes()
        reviewer = _ScriptedBatchReviewer(_replace_with("omega theta"))
        engine = self._engine(self.phrase_db, reviewer)
        engine.begin_request()
        engine.repair(PHRASE_TEXT)
        engine.take_details()
        self.assertEqual(self.phrase_db.read_bytes(), before)


class _ClientResult:
    """One real concurrent loopback client (order 029-b, R8 fidelity):
    runs the full POST in its own thread so the test can observe the
    response-delivery boundary against the main-completion barrier."""

    def __init__(
        self, port: int, body: bytes, headers: dict[str, str]
    ) -> None:
        self.port = port
        self.body = body
        self.headers = headers
        self.status: int | None = None
        self.payload: bytes | None = None
        self.error: Exception | None = None
        self.done = threading.Event()

    def run(self) -> None:
        try:
            client = http.client.HTTPConnection(
                "127.0.0.1", self.port, timeout=30
            )
            try:
                client.request(
                    "POST",
                    "/v1/responses",
                    body=self.body,
                    headers=self.headers,
                )
                response = client.getresponse()
                self.status = response.status
                self.payload = response.read()
            finally:
                client.close()
        except Exception as exc:
            self.error = exc
        finally:
            self.done.set()


class _BarrierSseMainUpstream(_MainUpstream):
    """Owned fake MAIN SSE endpoint with a controlled completion barrier
    (order 029-b, R8 fidelity): it streams the real SSE prefix, then
    blocks on ``release`` before the ``response.completed`` tail.  The
    barrier - not a sleep or timestamp ordering - is what proves that
    while main remains incomplete the proxy starts no review and
    delivers no response bytes to the real client."""

    release: threading.Event | None = None
    prefix_sent: threading.Event | None = None

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        self.__class__.recorded.append(
            {"path": self.path, "headers": dict(self.headers.items()), "body": body}
        )
        source = self.__class__.source
        marker = b'{"type":"response.completed"'
        index = source.rfind(marker)
        prefix, tail = (
            (source, b"") if index < 0 else (source[:index], source[index:])
        )
        self.send_response(self.status)
        self.send_header("Content-Type", self.content_type)
        self.send_header("Content-Length", str(len(source)))
        self.end_headers()
        self.wfile.write(prefix)
        self.wfile.flush()
        if self.prefix_sent is not None:
            self.prefix_sent.set()
        if self.release is not None:
            self.release.wait(30.0)
        self.wfile.write(tail)
        self.wfile.flush()

    def log_message(self, *_args: object) -> None:
        return


def _prompt_targets(record: dict[str, object]) -> list[str]:
    value = json.loads(cast(bytes, record["body"]))
    prompt = cast(str, value["input"][0]["content"][0]["text"])
    payload = json.loads(prompt.split("\n", 1)[1])
    targets = cast(list[dict[str, object]], payload.get("targets"))
    return [str(target["target"]) for target in targets]


class _BHarness:
    """One real proxy instance with owned fake main/review upstreams on
    loopback port 0 (order 029-b, R6/R8).  ``close`` is the single
    release / bounded-join / termination-assert / cleanup path and runs
    through addCleanup on every failure mode."""

    def __init__(
        self,
        usage_observer: Callable[[dict[str, object]], None] | None = None,
    ) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db = _http_db(self.root)
        self.release = threading.Event()
        self.prefix_sent = threading.Event()
        _BarrierSseMainUpstream.release = self.release
        _BarrierSseMainUpstream.prefix_sent = self.prefix_sent
        _MainUpstream.status = 200
        _MainUpstream.content_type = "application/json"
        _MainUpstream.source = b"{}"
        _MainUpstream.recorded = []
        _FakeUpstream.status = 200
        _FakeUpstream.delay = 0.0
        _FakeUpstream.payload = b"{}"
        _FakeUpstream.recorded = []
        self.servers: list[HTTPServer] = []
        self.threads: list[threading.Thread] = []
        self.clients: list[threading.Thread] = []
        self.main_server = HTTPServer(("127.0.0.1", 0), _MainUpstream)
        self.review_server = HTTPServer(("127.0.0.1", 0), _FakeUpstream)
        for server in (self.main_server, self.review_server):
            self.servers.append(server)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            self.threads.append(thread)
        reviewer = ResponsesReviewer(
            f"http://127.0.0.1:{self.review_server.server_port}/v1",
            "test-model",
            timeout=10.0,
            api_key=_REVIEW_KEY,
        )
        self.engine = proxy.RepairEngine(self.db, reviewer, pandoc=_real_spec())
        self.proxy_server = proxy.ConceptProxy(
            ("127.0.0.1", 0),
            f"http://127.0.0.1:{self.main_server.server_port}",
            self.engine,
            usage_observer=usage_observer,
        )
        self.servers.append(self.proxy_server)
        thread = threading.Thread(target=self.proxy_server.serve_forever, daemon=True)
        thread.start()
        self.threads.append(thread)

    def post(
        self, body: bytes, headers: dict[str, str] | None = None
    ) -> tuple[int, bytes]:
        all_headers = {"Content-Length": str(len(body))}
        if headers:
            all_headers.update(headers)
        client = http.client.HTTPConnection(
            "127.0.0.1", self.proxy_server.server_port, timeout=30
        )
        client.request("POST", "/v1/responses", body=body, headers=all_headers)
        response = client.getresponse()
        payload = response.read()
        client.close()
        return response.status, payload

    def post_async(
        self, body: bytes, headers: dict[str, str] | None = None
    ) -> _ClientResult:
        all_headers = {"Content-Length": str(len(body))}
        if headers:
            all_headers.update(headers)
        result = _ClientResult(self.proxy_server.server_port, body, all_headers)
        thread = threading.Thread(target=result.run, daemon=True)
        self.clients.append(thread)
        thread.start()
        return result

    def close(self) -> None:
        self.release.set()
        for client_thread in self.clients:
            client_thread.join(30)
            assert not client_thread.is_alive()
        for server in self.servers:
            server.shutdown()
        for server_thread in self.threads:
            server_thread.join(10)
            assert not server_thread.is_alive()
        for server in self.servers:
            server.server_close()
        self.temp.cleanup()


class HttpRoundTripTests(unittest.TestCase):
    """R8: real proxy HTTP -> real engine -> real ResponsesReviewer ->
    real read-only corpus and qualified Pandoc; only the main/review
    HTTP endpoints are synthetic (order 029-b integration fidelity:
    barrier-held main, real concurrent client, recorded operator usage
    observation)."""

    def test_json_word_useful_one_review(self) -> None:
        observations: list[dict[str, object]] = []
        harness = _BHarness(usage_observer=observations.append)
        self.addCleanup(harness.close)
        _MainUpstream.source = _json_completed(
            answer=WORD_TEXT,
            usage={"input_tokens": 7, "output_tokens": 3, "total_tokens": 10},
        )
        _FakeUpstream.payload = _review_payload(
            [_prop("t0", False, "omega")],
            usage={"input_tokens": 4, "output_tokens": 2, "total_tokens": 6},
        )
        status, payload = harness.post(
            _contract_body(False, input_text=WORD_TEXT),
            {"Authorization": f"Bearer {_MAIN_KEY}"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        self.assertEqual(
            _prompt_targets(_FakeUpstream.recorded[0]), ["alpha"]
        )
        body = json.loads(payload)
        self.assertEqual(body["output"][0]["content"][0]["text"], "to omega je")
        self.assertEqual(
            body["usage"],
            {"input_tokens": 7, "output_tokens": 3, "total_tokens": 10},
        )
        self.assertEqual(
            observations,
            [
                {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 4,
                        "output_tokens": 2,
                        "total_tokens": 6,
                    },
                }
            ],
        )

    def test_sse_phrase_held_main_delayed_review(self) -> None:
        observations: list[dict[str, object]] = []
        harness = _BHarness(usage_observer=observations.append)
        self.addCleanup(harness.close)
        # Real SSE prefix, then the controlled completion barrier holds
        # the response.completed tail until the test releases it.
        _BarrierSseMainUpstream.status = 200
        _BarrierSseMainUpstream.content_type = "text/event-stream"
        _BarrierSseMainUpstream.source = _tc_baseline(PHRASE_TEXT)
        harness.main_server.RequestHandlerClass = _BarrierSseMainUpstream
        # Real delayed review of one WHOLE phrase with explicit known
        # usage on the first owned fake response.
        _FakeUpstream.delay = 0.5
        _FakeUpstream.payload = _review_payload(
            [_prop("t0", False, "omega theta")],
            usage={"input_tokens": 5, "output_tokens": 2, "total_tokens": 7},
        )
        result = harness.post_async(
            _contract_body(True, input_text=PHRASE_TEXT),
            {"Authorization": f"Bearer {_MAIN_KEY}"},
        )
        # Observable boundary: the real prefix is on the wire and the
        # completion tail is still held by the barrier.
        self.assertTrue(harness.prefix_sent.wait(30.0))
        # While main remains incomplete: zero review calls and no
        # response/answer bytes delivered to the real client.
        self.assertEqual(len(_FakeUpstream.recorded), 0)
        self.assertIsNone(result.status)
        self.assertIsNone(result.payload)
        # Release the barrier (harness.close also guarantees this).
        harness.release.set()
        self.assertTrue(result.done.wait(30.0))
        self.assertIsNone(result.error)
        self.assertEqual(result.status, 200)
        payload = cast(bytes, result.payload)
        # One useful WHOLE phrase target, one real delayed review.
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        self.assertEqual(
            _prompt_targets(_FakeUpstream.recorded[0]), ["alpha beta"]
        )
        # No provisional original leak; every answer copy consistent.
        self.assertNotIn(PHRASE_TEXT.encode(), payload)
        self.assertEqual(payload.count(b"to omega theta je"), 4)
        # Operator observation: real per-request review calls with the
        # known reviewer usage of the first owned response.
        self.assertEqual(
            observations,
            [
                {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 5,
                        "output_tokens": 2,
                        "total_tokens": 7,
                    },
                }
            ],
        )
        # Same-proxy following known-safe zero-review JSON response:
        # the exact original bytes, no extra review, isolated usage.
        harness.main_server.RequestHandlerClass = _MainUpstream
        _MainUpstream.content_type = "application/json"
        _MainUpstream.source = _json_completed(
            answer=HEALTHY_TEXT,
            usage={"input_tokens": 1, "output_tokens": 1, "total_tokens": 2},
        )
        status, payload = harness.post(
            _contract_body(False, input_text=HEALTHY_TEXT),
            {"Authorization": f"Bearer {_MAIN_KEY}"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload, _MainUpstream.source)
        self.assertEqual(len(_FakeUpstream.recorded), 1)
        body = json.loads(payload)
        self.assertEqual(
            body["usage"],
            {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2},
        )
        # The second observation proves the first known usage is not
        # carried over: zero calls and explicit unknown.
        self.assertEqual(
            observations,
            [
                {
                    "review_calls": 1,
                    "reviewer_usage": {
                        "input_tokens": 5,
                        "output_tokens": 2,
                        "total_tokens": 7,
                    },
                },
                {"review_calls": 0, "reviewer_usage": "unknown"},
            ],
        )


if __name__ == "__main__":
    unittest.main()
