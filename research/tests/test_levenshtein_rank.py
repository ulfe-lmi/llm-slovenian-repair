"""Focused offline tests for the 007-m CPU ranking seam and driver census.

All tests are data-free: synthetic frozen shapes plus dict-backed index fakes
with the exact query contract of the frozen read-only SQLite index.  The
existing 007-j driver test fakes are reused for the dispatch-interface
continuity proof.  No test encodes a desired live linguistic answer.
"""

from __future__ import annotations

import contextlib
import copy
import hashlib
import importlib.util
import inspect
import json
import os
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from research import contextual_validator as protocol
from research import levenshtein_rank as rank
from research.tools import run_levenshtein_one as prior_j
from research.tools import run_levenshtein_rank as driver


def _load_sibling_test_module(name: str):
    path = Path(__file__).resolve().parent / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"oap007m_{name}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_sibling = _load_sibling_test_module("test_levenshtein_one_driver")
frozen_population_item = _sibling.candidate


class FakeIndex:
    """Dict-backed queries honouring the frozen IndexQueries contract."""

    def __init__(
        self,
        unigrams: dict[str, int],
        bigrams: dict[str, int],
        trigrams: dict[str, int],
    ) -> None:
        self.unigrams = dict(unigrams)
        self.bigrams = dict(bigrams)
        self.trigrams = dict(trigrams)
        self.queries: list[tuple[str, str]] = []

    def unigram(self, word: str) -> tuple[str, int | None]:
        key = word.casefold()
        self.queries.append(("unigram", key))
        count = self.unigrams.get(key)
        return (rank.EXACT, count) if count is not None else (rank.UNAVAILABLE, None)

    def ngram(self, phrase: str, length: int) -> tuple[str, int | None]:
        key = " ".join(part.casefold() for part in phrase.split())
        self.queries.append((f"{length}gram", key))
        table = self.trigrams if length == 3 else self.bigrams
        count = table.get(key)
        return (rank.EXACT, count) if count is not None else (rank.CENSORED, None)


LOOKUP = "bela"
EVIDENCE = {
    "left_bigram": {"key": "kova bela", "state": "CENSORED", "count": None},
    "right_bigram": {"key": "bela lepa", "state": "EXACT", "count": 41},
    "trigram": {"key": "kova bela lepa", "state": "CENSORED", "count": None},
    "unigram": {"key": "bela", "state": "UNAVAILABLE", "count": None},
}
# dola: (1,30,2,135,400); belo: (0,0,1,90,50); belal: (0,0,0,0,5);
# dolq: (1,30,2,135,400) identical to dola for the tie tests.
INDEX = FakeIndex(
    unigrams={"dola": 400, "belo": 50, "belal": 5, "dolq": 400},
    bigrams={"kova dola": 120, "dola lepa": 15, "kova belo": 90, "kova dolq": 120, "dolq lepa": 15},
    trigrams={"kova dola lepa": 30, "kova dolq lepa": 30},
)
CANDIDATES = [
    {"text": "dola", "operation": "SUBSTITUTION"},
    {"text": "belo", "operation": "SUBSTITUTION"},
    {"text": "belal", "operation": "INSERTION"},
]
SENTENCE = "kova bela lepa"
START, END = 5, 9
VOCABULARY = {"kova", "bela", "lepa", "dola", "belo", "belal", "dolq"}
STRADDLE_VOCABULARY = VOCABULARY | {"xan", "yan"}


def census_item(
    case_index: int,
    phase: str,
    reference: str,
    candidates: list[dict[str, str]],
) -> dict[str, object]:
    return {
        "phase": phase,
        "case_index": case_index,
        "case_id": f"case-{case_index}",
        "target_ordinal": 0,
        "target_start": START,
        "target_end": END,
        "candidate": {
            "start": START,
            "end": END,
            "text": LOOKUP,
            "score": 1.0,
            "evidence": EVIDENCE,
        },
        "transition": "C=0 -> C>1",
        "cardinality": "C>1",
        "sentence": SENTENCE,
        "reference": reference,
        "candidates": candidates,
    }


SLICE_BASELINE = {
    "spelling-all": (10, 40),
    "spelling-initial-uv": (2, 8),
    "spelling-without-initial-uv": (8, 32),
    "preservation-all": (0, 0),
}
UV_INDICES = {22}


def synthetic_population() -> list[dict[str, object]]:
    return [
        census_item(11, "dassle-spelling", "kova dola lepa", CANDIDATES),
        census_item(22, "dassle-spelling", "kova belo lepa", CANDIDATES),
        census_item(
            33,
            "dassle-spelling",
            "kova dola lepa",
            [
                {"text": "dola", "operation": "SUBSTITUTION"},
                {"text": "dolq", "operation": "INSERTION"},
            ],
        ),
        census_item(
            44,
            "dassle-spelling-preservation",
            "kova zola lepa",
            [
                {"text": "belo", "operation": "SUBSTITUTION"},
                {"text": "belal", "operation": "INSERTION"},
            ],
        ),
    ]


class DeterministicScoreRankTests(unittest.TestCase):
    def test_score_tuple_is_predeclared_and_lexicographic(self) -> None:
        context = rank.extract_context(EVIDENCE, LOOKUP)
        self.assertEqual((context.left_word, context.right_word), ("kova", "lepa"))
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        first = rank.rank_candidates(CANDIDATES, context, index.unigram, index.ngram)
        self.assertEqual([score.text for score in first.rank_order], ["dola", "belo", "belal"])
        expected = {
            "dola": (1, 30, 2, 135, 400),
            "belo": (0, 0, 1, 90, 50),
            "belal": (0, 0, 0, 0, 5),
        }
        for score in first.scores:
            self.assertEqual(score.score, expected[score.text])
        self.assertFalse(first.tied)
        self.assertEqual(first.top.text, "dola")

    def test_rank_is_deterministic_and_input_order_independent(self) -> None:
        context = rank.extract_context(EVIDENCE, LOOKUP)
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        first = rank.rank_candidates(CANDIDATES, context, index.unigram, index.ngram)
        other = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        second = rank.rank_candidates(
            list(reversed(CANDIDATES)), context, other.unigram, other.ngram
        )
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual([score.text for score in first.scores], ["belal", "belo", "dola"])
        self.assertEqual(
            {text: (iv.rank_min, iv.rank_max) for text, iv in first.rank_intervals.items()},
            {"dola": (1, 1), "belo": (2, 2), "belal": (3, 3)},
        )

    def test_trigram_flag_and_count_dominate_bigram_and_unigram(self) -> None:
        context = rank.extract_context(EVIDENCE, LOOKUP)
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        ranking = rank.rank_candidates(CANDIDATES, context, index.unigram, index.ngram)
        # dola beats belo on the trigram flag despite belo's lower unigram;
        # the flag dominates the side count, which dominates the unigram.
        dola, belo = ranking.top, ranking.rank_order[1]
        self.assertEqual(dola.text, "dola")
        self.assertGreater(dola.score, belo.score)
        self.assertLessEqual(belo.score[2], 1)


class TieAbstentionTests(unittest.TestCase):
    def test_exact_top_tie_selects_nothing(self) -> None:
        context = rank.extract_context(EVIDENCE, LOOKUP)
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        tied_set = [
            {"text": "dola", "operation": "SUBSTITUTION"},
            {"text": "dolq", "operation": "INSERTION"},
        ]
        ranking = rank.rank_candidates(tied_set, context, index.unigram, index.ngram)
        self.assertTrue(ranking.tied)
        self.assertIsNone(ranking.top)
        self.assertEqual([score.text for score in ranking.rank_order], ["dola", "dolq"])
        payload = {"selected": True, "candidate_form": "dola"}
        unique = rank.rank_candidates(CANDIDATES, context, index.unigram, index.ngram)
        selected = rank.select_for_dispatch([(unique, dict(payload)), (ranking, dict(payload))])
        self.assertEqual(selected, [dict(payload)])
        self.assertEqual(rank.select_for_dispatch([(ranking, dict(payload))]), [])

    def test_operation_and_text_order_do_not_tiebreak(self) -> None:
        context = rank.extract_context(EVIDENCE, LOOKUP)
        swapped = [
            {"text": "dola", "operation": "INSERTION"},
            {"text": "dolq", "operation": "SUBSTITUTION"},
        ]
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        first = rank.rank_candidates(
            [
                {"text": "dola", "operation": "SUBSTITUTION"},
                {"text": "dolq", "operation": "INSERTION"},
            ],
            context,
            index.unigram,
            index.ngram,
        )
        second = rank.rank_candidates(swapped, context, index.unigram, index.ngram)
        for result in (first, second):
            self.assertTrue(result.tied)
            self.assertIsNone(result.top)
            self.assertEqual([score.text for score in result.rank_order], ["dola", "dolq"])
            self.assertEqual(
                [score.score for score in result.rank_order],
                [(1, 30, 2, 135, 400), (1, 30, 2, 135, 400)],
            )
        self.assertEqual(
            [score.text for score in first.rank_order],
            [score.text for score in second.rank_order],
        )


class RankIntervalTests(unittest.TestCase):
    def test_tie_aware_intervals_for_every_candidate(self) -> None:
        context = rank.extract_context(EVIDENCE, LOOKUP)
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        members = CANDIDATES + [
            {"text": "dolq", "operation": "SUBSTITUTION"},
            {"text": "zzz", "operation": "SUBSTITUTION"},
        ]
        ranking = rank.rank_candidates(members, context, index.unigram, index.ngram)
        self.assertEqual(
            {text: (iv.rank_min, iv.rank_max) for text, iv in ranking.rank_intervals.items()},
            {"dola": (1, 2), "dolq": (1, 2), "belo": (3, 3), "belal": (4, 4), "zzz": (5, 5)},
        )
        self.assertTrue(ranking.tied)
        self.assertIsNone(ranking.top)
        groups = ranking.tie_groups
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["size"], 2)
        self.assertEqual(groups[0]["rank_interval"], {"min": 1, "max": 2})
        self.assertTrue(groups[0]["top_group"])
        self.assertEqual(groups[0]["texts"], ["dola", "dolq"])

    def test_unique_scores_give_singleton_intervals(self) -> None:
        context = rank.extract_context(EVIDENCE, LOOKUP)
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        ranking = rank.rank_candidates(CANDIDATES, context, index.unigram, index.ngram)
        self.assertEqual(
            {text: (iv.rank_min, iv.rank_max) for text, iv in ranking.rank_intervals.items()},
            {"dola": (1, 1), "belo": (2, 2), "belal": (3, 3)},
        )
        self.assertEqual(ranking.tie_groups, ())
        self.assertFalse(ranking.tied)
        self.assertEqual(ranking.top.text, "dola")

    def test_intervals_invariant_under_input_order_and_operation_permutation(self) -> None:
        context = rank.extract_context(EVIDENCE, LOOKUP)
        base = [
            {"text": "dola", "operation": "SUBSTITUTION"},
            {"text": "dolq", "operation": "INSERTION"},
            {"text": "belo", "operation": "SUBSTITUTION"},
            {"text": "belal", "operation": "INSERTION"},
        ]
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        first = rank.rank_candidates(base, context, index.unigram, index.ngram)
        other = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        swapped = [
            {
                "text": base[position]["text"],
                "operation": (
                    "INSERTION" if base[position]["operation"] == "SUBSTITUTION" else "SUBSTITUTION"
                ),
            }
            for position in (3, 1, 0, 2)
        ]
        second = rank.rank_candidates(swapped, context, other.unigram, other.ngram)
        self.assertEqual(first.rank_intervals, second.rank_intervals)
        self.assertEqual(first.tie_groups, second.tie_groups)

        def stripped(result: rank.TargetRanking) -> list[dict[str, object]]:
            return [
                {key: value for key, value in entry.items() if key != "operation"}
                for entry in result.to_dict()["candidates"]
            ]

        self.assertEqual(stripped(first), stripped(second))

    def test_no_scalar_rank_is_exposed(self) -> None:
        self.assertFalse(hasattr(rank.TargetRanking, "rank_positions"))
        context = rank.extract_context(EVIDENCE, LOOKUP)
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        ranking = rank.rank_candidates(CANDIDATES, context, index.unigram, index.ngram)
        rendered = protocol.canonical_bytes(ranking.to_dict()).decode("utf-8")
        self.assertNotIn('"rank":', rendered)
        for entry in ranking.to_dict()["candidates"]:
            self.assertNotIn("rank", entry)
            self.assertIn("rank_interval", entry)


class EvidenceStateTests(unittest.TestCase):
    def test_missing_and_censored_states_are_never_zero_counts(self) -> None:
        context = rank.extract_context(EVIDENCE, LOOKUP)
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        candidates = [
            {"text": "belal", "operation": "INSERTION"},
            {"text": "zzz", "operation": "SUBSTITUTION"},
        ]
        ranking = rank.rank_candidates(candidates, context, index.unigram, index.ngram)
        records = {entry["text"]: entry for entry in ranking.to_dict()["candidates"]}
        belal = records["belal"]
        self.assertEqual(belal["trigram"], {"state": "CENSORED", "count": None})
        self.assertEqual(belal["left_bigram"], {"state": "CENSORED", "count": None})
        self.assertEqual(belal["right_bigram"], {"state": "CENSORED", "count": None})
        self.assertEqual(belal["unigram"], {"state": "EXACT", "count": 5})
        self.assertEqual(belal["score"], [0, 0, 0, 0, 5])
        zzz = records["zzz"]
        self.assertEqual(zzz["unigram"], {"state": "UNAVAILABLE", "count": None})
        self.assertEqual(zzz["trigram"], {"state": "CENSORED", "count": None})
        self.assertEqual(zzz["score"], [0, 0, 0, 0, 0])
        for record in records.values():
            for slot in ("trigram", "left_bigram", "right_bigram", "unigram"):
                value = record[slot]
                if value["state"] != "EXACT":
                    self.assertIsNone(value["count"], (record["text"], slot))

    def test_protected_context_boundary_behaviour(self) -> None:
        left_only = {
            "left_bigram": {"key": "kova bela", "state": "EXACT", "count": 9},
            "unigram": {"key": "bela", "state": "UNAVAILABLE", "count": None},
        }
        right_only = {
            "right_bigram": {"key": "bela lepa", "state": "EXACT", "count": 7},
            "unigram": {"key": "bela", "state": "UNAVAILABLE", "count": None},
        }
        neither: dict[str, object] = {
            "unigram": {"key": "bela", "state": "UNAVAILABLE", "count": None},
        }
        pair = [
            {"text": "dola", "operation": "SUBSTITUTION"},
            {"text": "belo", "operation": "SUBSTITUTION"},
        ]
        boundary_index = FakeIndex(unigrams={"dola": 400, "belo": 50}, bigrams={}, trigrams={})
        for evidence, left, right in (
            (left_only, True, False),
            (right_only, False, True),
            (neither, False, False),
        ):
            with self.subTest(evidence="left" if left else "right" if right else "none"):
                context = rank.extract_context(evidence, LOOKUP)
                self.assertEqual(context.has_left, left)
                self.assertEqual(context.has_right, right)
                ranking = rank.rank_candidates(
                    pair, context, boundary_index.unigram, boundary_index.ngram
                )
                records = {entry["text"]: entry for entry in ranking.to_dict()["candidates"]}
                for record in records.values():
                    self.assertEqual(
                        record["right_bigram"]["state"],
                        "UNAVAILABLE" if not right else "CENSORED",
                    )
                    self.assertIsNone(record["right_bigram"]["count"])
                    self.assertEqual(record["trigram"], {"state": "UNAVAILABLE", "count": None})
                    self.assertEqual(
                        record["left_bigram"]["state"],
                        "UNAVAILABLE" if not left else "CENSORED",
                    )
                    self.assertIsNone(record["left_bigram"]["count"])
                # With every n-gram side unavailable, only the unigram slot
                # can separate the candidates.
                self.assertEqual(ranking.top.text, "dola")
                self.assertEqual(records["dola"]["score"], [0, 0, 0, 0, 400])
                self.assertEqual(records["belo"]["score"], [0, 0, 0, 0, 50])

    def test_malformed_frozen_evidence_is_rejected(self) -> None:
        cases = [
            {"left_bigram": {"key": "kova zzz", "state": "EXACT", "count": 1}},
            {"right_bigram": {"key": "zzz lepa", "state": "EXACT", "count": 1}},
            {"trigram": {"key": "kova bela lepa", "state": "EXACT", "count": 1}},
            {
                "left_bigram": {"key": "kova bela", "state": "EXACT", "count": 1},
                "right_bigram": {"key": "bela lepa", "state": "EXACT", "count": 1},
            },
            {"left_bigram": {"key": "kova bela", "state": "EXACT", "count": None}},
            {"left_bigram": {"key": "kova bela", "state": "CENSORED", "count": 5}},
            {"left_bigram": {"key": "kova  bela", "state": "CENSORED", "count": None}},
            {"left_bigram": {"key": "kova", "state": "CENSORED", "count": None}},
            {"left_bigram": {"key": "kova bela", "state": "ZERO", "count": None}},
        ]
        for evidence in cases:
            with self.assertRaises(rank.RankingError):
                rank.extract_context(evidence, LOOKUP)
        with self.assertRaises(rank.RankingError):
            rank.extract_context(EVIDENCE, "be la")

    def test_c0_and_c1_sets_are_rejected_by_the_ranking_seam(self) -> None:
        context = rank.extract_context(EVIDENCE, LOOKUP)
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        with self.assertRaises(rank.RankingError):
            rank.rank_candidates([], context, index.unigram, index.ngram)
        with self.assertRaises(rank.RankingError):
            rank.rank_candidates(CANDIDATES[:1], context, index.unigram, index.ngram)
        self.assertEqual(driver._cardinality(0), "C=0")
        self.assertEqual(driver._cardinality(1), "C=1")
        self.assertEqual(driver._cardinality(2), "C>1")
        self.assertEqual(
            list(inspect.signature(prior_j.build_population).parameters),
            ["records", "vocabulary", "buckets"],
        )


class NoGoldDependencyTests(unittest.TestCase):
    def test_ranking_api_is_structurally_gold_free(self) -> None:
        forbidden = {"reference", "gold", "ref", "expected", "answer"}
        for function in (
            rank.extract_context,
            rank._candidate_keys,
            rank.score_candidate,
            rank.score_tuple,
            rank.rank_candidates,
            rank.select_for_dispatch,
        ):
            names = set(inspect.signature(function).parameters)
            self.assertFalse(names & forbidden, names)
        public_names = [
            name for name in dir(rank) if not name.startswith("_") and callable(getattr(rank, name))
        ]
        for name in public_names:
            self.assertFalse("gold" in name.lower() or "reference" in name.lower(), name)

    def test_reference_cannot_change_ranking(self) -> None:
        population_a = synthetic_population()
        population_b = [dict(item) for item in population_a]
        population_b[0]["reference"] = "kova zola lepa"
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        first = driver.census_population(
            population_a, index, VOCABULARY, UV_INDICES, SLICE_BASELINE
        )
        other = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        second = driver.census_population(
            population_b, other, VOCABULARY, UV_INDICES, SLICE_BASELINE
        )
        for record_a, record_b in zip(first["records"], second["records"], strict=True):
            self.assertEqual(record_a["ranking"], record_b["ranking"])
        self.assertNotEqual(
            first["records"][0]["reference_headroom"],
            second["records"][0]["reference_headroom"],
        )


class CensusTests(unittest.TestCase):
    def _census(self) -> dict[str, object]:
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        return driver.census_population(
            synthetic_population(), index, VOCABULARY, UV_INDICES, SLICE_BASELINE
        )

    def test_complete_c_gt_1_census_aggregates(self) -> None:
        census = self._census()
        spelling = census["slices"]["spelling-all"]
        self.assertEqual(spelling["target_count"], 3)
        self.assertEqual(spelling["total_candidate_pairs"], 8)
        self.assertEqual(
            spelling["set_size"],
            {"min": 2, "median": 3.0, "p90": 3, "p95": 3, "p99": 3, "max": 3},
        )
        self.assertEqual(spelling["operation_composition"], {"INSERTION": 3, "SUBSTITUTION": 5})
        self.assertEqual((spelling["unique_top"], spelling["tied_top"]), (2, 1))
        self.assertEqual((spelling["reference_present"], spelling["reference_absent"]), (3, 0))
        self.assertEqual(
            spelling["reference_rank"],
            {
                "rank_min": {"min": 1, "median": 1, "p95": 2, "max": 2},
                "rank_max": {"min": 1, "median": 2, "p95": 2, "max": 2},
            },
        )
        self.assertEqual(
            spelling["top_k_coverage"]["1"],
            {
                "certain": {"count": 1, "rate_among_present": 1 / 3},
                "possible": {"count": 2, "rate_among_present": 2 / 3},
                "straddling": 1,
            },
        )
        self.assertEqual(spelling["top_k_coverage"]["2"]["certain"]["count"], 3)
        self.assertEqual(spelling["top_k_coverage"]["2"]["possible"]["count"], 3)
        self.assertEqual(spelling["top_k_coverage"]["2"]["straddling"], 0)
        self.assertEqual(spelling["top_k_coverage"]["10"]["certain"]["count"], 3)
        self.assertEqual(spelling["lower_tie_groups"], 0)
        self.assertEqual(spelling["reference_group_tied"], 1)
        self.assertEqual(spelling["oracle_gold_units"], 3)
        self.assertEqual(spelling["dispatchable_unique_tops"], 2)
        self.assertEqual(spelling["baseline"]["frozen_recall"], 0.2)
        self.assertAlmostEqual(spelling["baseline"]["ceiling"], (10 + 3) / 50)

        uv = census["slices"]["spelling-initial-uv"]
        self.assertEqual(uv["target_count"], 1)
        self.assertEqual(
            uv["reference_rank"],
            {
                "rank_min": {"min": 2, "median": 2, "p95": 2, "max": 2},
                "rank_max": {"min": 2, "median": 2, "p95": 2, "max": 2},
            },
        )
        self.assertEqual(uv["top_k_coverage"]["1"]["certain"]["count"], 0)
        self.assertEqual(uv["top_k_coverage"]["1"]["possible"]["count"], 0)
        self.assertEqual(uv["top_k_coverage"]["2"]["certain"]["count"], 1)
        self.assertEqual(uv["top_k_coverage"]["2"]["straddling"], 0)
        self.assertAlmostEqual(uv["baseline"]["ceiling"], (2 + 1) / 10)

        without = census["slices"]["spelling-without-initial-uv"]
        self.assertEqual(without["target_count"], 2)
        self.assertEqual((without["unique_top"], without["tied_top"]), (1, 1))
        self.assertEqual(
            without["reference_rank"],
            {
                "rank_min": {"min": 1, "median": 1, "p95": 1, "max": 1},
                "rank_max": {"min": 1, "median": 1.5, "p95": 2, "max": 2},
            },
        )
        self.assertEqual(without["top_k_coverage"]["1"]["certain"]["count"], 1)
        self.assertEqual(without["top_k_coverage"]["1"]["possible"]["count"], 2)
        self.assertEqual(without["top_k_coverage"]["1"]["straddling"], 1)
        self.assertAlmostEqual(without["baseline"]["ceiling"], (8 + 2) / 40)

        preservation = census["slices"]["preservation-all"]
        self.assertEqual(preservation["target_count"], 1)
        self.assertEqual(preservation["reference_absent"], 1)
        self.assertEqual(preservation["top_k_coverage"]["1"]["possible"]["count"], 0)
        self.assertEqual(preservation["lower_tie_groups"], 0)
        self.assertIsNone(preservation["baseline"]["ceiling"])
        self.assertIsNone(preservation["baseline"]["frozen_recall"])

        totals = census["totals"]
        self.assertEqual(totals["target_count"], 4)
        self.assertEqual(totals["total_candidate_pairs"], 10)
        self.assertEqual((totals["unique_top"], totals["tied_top"]), (3, 1))
        self.assertEqual((totals["reference_present"], totals["reference_absent"]), (3, 1))
        self.assertEqual(totals["oracle_gold_units"], 3)
        self.assertEqual(totals["dispatchable_unique_tops"], 3)
        self.assertEqual(totals["top_k_coverage"]["1"]["certain"]["count"], 1)
        self.assertEqual(totals["top_k_coverage"]["1"]["possible"]["count"], 2)
        self.assertEqual(totals["top_k_coverage"]["2"]["certain"]["count"], 3)
        self.assertEqual(totals["lower_tie_groups"], 0)
        self.assertEqual(totals["reference_group_tied"], 1)

    def test_tied_target_abstains_but_headroom_is_still_measured(self) -> None:
        census = self._census()
        tied = census["records"][2]
        self.assertTrue(tied["ranking"]["tied"])
        self.assertIsNone(tied["ranking"]["top"])
        self.assertIsNone(tied["dispatch"])
        self.assertTrue(tied["reference_headroom"]["present"])
        self.assertEqual(tied["reference_headroom"]["rank_interval"], {"min": 1, "max": 2})
        self.assertEqual(
            tied["reference_headroom"]["top_k"]["1"], {"certain": False, "possible": True}
        )
        self.assertEqual(
            tied["reference_headroom"]["top_k"]["2"], {"certain": True, "possible": True}
        )
        self.assertEqual(tied["reference_headroom"]["oracle_gold_units"], 1)
        self.assertEqual(
            tied["ranking"]["tie_groups"],
            [
                {
                    "size": 2,
                    "rank_interval": {"min": 1, "max": 2},
                    "top_group": True,
                    "texts": ["dola", "dolq"],
                }
            ],
        )

    def test_dispatch_manifest_is_at_most_one_candidate_per_target(self) -> None:
        census = self._census()
        dispatch = census["dispatch"]
        self.assertEqual(len(dispatch), 3)
        for payload in dispatch:
            self.assertTrue(payload["selected"])
            self.assertEqual(
                [key for key in payload if key == "candidate_form"], ["candidate_form"]
            )
            self.assertEqual(
                payload["prompt_sha256"],
                protocol.sha256_bytes(
                    protocol.prompt_text(
                        payload["sentence"],
                        payload["candidate"]["text"],
                        payload["candidate_form"],
                    ).encode("utf-8")
                ),
            )
        first = dispatch[0]
        body = protocol.request_body(
            first["sentence"], first["candidate"]["text"], first["candidate_form"]
        )
        self.assertEqual(len(body["input"]), 1)
        self.assertEqual(len(body["input"][0]["content"]), 1)
        self.assertEqual(
            body["input"][0]["content"][0]["text"],
            protocol.prompt_text(
                first["sentence"], first["candidate"]["text"], first["candidate_form"]
            ),
        )
        # No unselected candidate text may reach the dispatch payload.
        rendered = protocol.canonical_bytes(first).decode("utf-8")
        for absent in ("belo", "belal", "dolq", "zola"):
            self.assertNotIn(absent, rendered)

    def test_dispatch_payload_keeps_the_frozen_007j_field_contract(self) -> None:
        census = self._census()
        payload = census["dispatch"][0]
        frozen_item = frozen_population_item(0, target=LOOKUP, replacement="dola")
        self.assertIsInstance(frozen_item, dict)
        frozen_keys = {
            "phase",
            "case_index",
            "case_id",
            "target_ordinal",
            "target_start",
            "target_end",
            "candidate",
            "candidate_form",
            "operation",
            "mechanical_edit",
            "sentence",
        }
        self.assertTrue(frozen_keys.issubset(set(payload)))
        self.assertNotIn("reference", payload)


class StraddlingTieCensusTests(unittest.TestCase):
    """A tie group straddling k=2 must keep certain and possible separate."""

    MEMBERS = [
        {"text": "dola", "operation": "SUBSTITUTION"},
        {"text": "xan", "operation": "INSERTION"},
        {"text": "yan", "operation": "INSERTION"},
        {"text": "belal", "operation": "SUBSTITUTION"},
    ]

    def _index(self) -> FakeIndex:
        return FakeIndex(
            unigrams={"dola": 400, "xan": 50, "yan": 50, "belal": 5},
            bigrams={"kova xan": 90, "kova yan": 90},
            trigrams={"kova dola lepa": 30},
        )

    def _census(self, members: list[dict[str, str]]) -> dict[str, object]:
        population = [census_item(55, "dassle-spelling", "kova xan lepa", members)]
        return driver.census_population(
            population, self._index(), STRADDLE_VOCABULARY, UV_INDICES, SLICE_BASELINE
        )

    def test_straddling_group_reports_both_bounds(self) -> None:
        census = self._census([dict(entry) for entry in self.MEMBERS])
        record = census["records"][0]
        headroom = record["reference_headroom"]
        self.assertTrue(headroom["present"])
        self.assertEqual(headroom["rank_interval"], {"min": 2, "max": 3})
        self.assertEqual(headroom["top_k"]["1"], {"certain": False, "possible": False})
        self.assertEqual(headroom["top_k"]["2"], {"certain": False, "possible": True})
        self.assertEqual(headroom["top_k"]["3"], {"certain": True, "possible": True})
        self.assertEqual(headroom["top_k"]["10"], {"certain": True, "possible": True})
        self.assertEqual(headroom["oracle_gold_units"], 1)
        self.assertEqual(headroom["reference_candidates"], 1)
        spelling = census["slices"]["spelling-all"]
        self.assertEqual(
            spelling["reference_rank"],
            {
                "rank_min": {"min": 2, "median": 2, "p95": 2, "max": 2},
                "rank_max": {"min": 3, "median": 3, "p95": 3, "max": 3},
            },
        )
        self.assertEqual(spelling["top_k_coverage"]["1"]["certain"]["count"], 0)
        self.assertEqual(spelling["top_k_coverage"]["1"]["possible"]["count"], 0)
        self.assertEqual(spelling["top_k_coverage"]["2"]["certain"]["count"], 0)
        self.assertEqual(spelling["top_k_coverage"]["2"]["possible"]["count"], 1)
        self.assertEqual(spelling["top_k_coverage"]["2"]["straddling"], 1)
        self.assertEqual(spelling["top_k_coverage"]["3"]["certain"]["count"], 1)
        self.assertEqual(spelling["top_k_coverage"]["3"]["straddling"], 0)
        self.assertEqual(spelling["lower_tie_groups"], 1)
        self.assertEqual(spelling["reference_group_tied"], 1)
        self.assertEqual((spelling["unique_top"], spelling["tied_top"]), (1, 0))
        self.assertEqual(spelling["dispatchable_unique_tops"], 1)

    def test_permutation_cannot_change_intervals_or_top_k_counts(self) -> None:
        members = [dict(entry) for entry in self.MEMBERS]
        census_a = self._census(members)
        reordered = []
        for position in (3, 1, 0, 2):
            entry = dict(members[position])
            entry["operation"] = (
                "INSERTION" if entry["operation"] == "SUBSTITUTION" else "SUBSTITUTION"
            )
            reordered.append(entry)
        census_b = self._census(reordered)
        entries_a = {
            entry["text"]: entry for entry in census_a["records"][0]["ranking"]["candidates"]
        }
        entries_b = {
            entry["text"]: entry for entry in census_b["records"][0]["ranking"]["candidates"]
        }
        for text in entries_a:
            self.assertEqual(entries_a[text]["score"], entries_b[text]["score"])
            self.assertEqual(entries_a[text]["rank_interval"], entries_b[text]["rank_interval"])
        self.assertEqual(
            census_a["records"][0]["reference_headroom"],
            census_b["records"][0]["reference_headroom"],
        )
        coverage_a = census_a["slices"]["spelling-all"]["top_k_coverage"]
        coverage_b = census_b["slices"]["spelling-all"]["top_k_coverage"]
        for k in rank.TOP_K:
            for name in ("certain", "possible"):
                self.assertEqual(
                    coverage_a[str(k)][name]["count"], coverage_b[str(k)][name]["count"]
                )


class DispatchBoundaryTests(unittest.TestCase):
    def _unique_ranking(self) -> rank.TargetRanking:
        context = rank.extract_context(EVIDENCE, LOOKUP)
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        return rank.rank_candidates(CANDIDATES, context, index.unigram, index.ngram)

    def test_candidate_lists_are_refused_in_dispatch_payloads(self) -> None:
        ranking = self._unique_ranking()
        clean = {"selected": True, "candidate_form": "dola"}
        self.assertEqual(rank.select_for_dispatch([(ranking, clean)]), [dict(clean)])
        with self.assertRaises(rank.RankingError):
            rank.select_for_dispatch(
                [
                    (
                        ranking,
                        {
                            "selected": True,
                            "candidate_form": "dola",
                            "candidates": [
                                {"candidate_form": "dola"},
                                {"candidate_form": "belo"},
                            ],
                        },
                    )
                ]
            )
        with self.assertRaises(rank.RankingError):
            rank.select_for_dispatch(
                [
                    (
                        ranking,
                        {
                            "selected": True,
                            "candidate_form": "dola",
                            "audit": [
                                {"candidate_form": "dola"},
                                {"candidate_form": "belo"},
                            ],
                        },
                    )
                ]
            )
        with self.assertRaises(rank.RankingError):
            rank.select_for_dispatch([(ranking, {"selected": True, "candidate_form": "belo"})])
        with self.assertRaises(rank.RankingError):
            rank.select_for_dispatch([(ranking, {"selected": True})])


class PublicProjectionTests(unittest.TestCase):
    def test_public_artifacts_expose_no_raw_language(self) -> None:
        index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
        census = driver.census_population(
            synthetic_population(), index, VOCABULARY, UV_INDICES, SLICE_BASELINE
        )
        census["runtime"] = {
            "vocabulary_loading_seconds": 0.1,
            "vocabulary_rows": 7,
            "candidate_search_seconds": 0.2,
            "ranking_seconds": 0.3,
            "headroom_seconds": 0.4,
        }
        census["private_sha256"] = {"aggregate": "0" * 64}
        identity = {
            "implementation_head": "f" * 40,
            "branch": driver.BRANCH,
            "source_experiment": "007-j-levenshtein-one-contextual-validator",
            "configuration_sha256": "1" * 64,
            "candidate_manifest_sha256": "2" * 64,
            "results_sha256": "3" * 64,
        }
        schema = {"tables": {}, "meta": {"ngram_absence": "CENSORED"}}
        analysis = {
            "c_gt_1_counts": {"dassle-spelling": 3, "dassle-spelling-preservation": 1},
            "c0_counts": {},
            "entering_targets": {},
            "transition_matrix": {},
            "vocabulary_forms": 7,
        }
        public_configuration, public_result = driver.public_projection(
            identity, schema, analysis, census
        )
        rendered = (
            protocol.canonical_bytes(public_configuration) + protocol.canonical_bytes(public_result)
        ).decode("utf-8")
        for raw in ("kova", "bela", "lepa", "dola", "belo", "belal", "dolq", "zola"):
            self.assertNotIn(raw, rendered)
        self.assertNotIn("007m", rendered)
        self.assertEqual(public_configuration["no_model_calls"], True)


# ---------------------------------------------------------------------------
# Increment 2: focused offline tests for the live C>1 execution seam.
# Everything is synthetic and data-free; the frozen frozen-validator protocol
# (request bytes, parser, persistence, resume) is exercised through fakes.
# No test encodes a desired live linguistic answer.
# ---------------------------------------------------------------------------

SYNTHETIC_C_GT_1_COUNTS = {"dassle-spelling": 2, "dassle-spelling-preservation": 1}


def synthetic_live_items() -> tuple[dict[str, object], list[dict[str, object]]]:
    """Census the synthetic population and project the dispatchable items."""
    index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
    population = synthetic_population()
    census = driver.census_population(population, index, VOCABULARY, UV_INDICES, SLICE_BASELINE)
    items = driver.build_live_candidates(
        census["dispatch"], population, expected_total=3, expected_counts=SYNTHETIC_C_GT_1_COUNTS
    )
    return census, items


def multi_live_items(groups: int) -> list[dict[str, object]]:
    """Build ``groups`` dispatchable unique-top census items in one phase."""
    population = [
        census_item(101 + position, "dassle-spelling", "kova dola lepa", CANDIDATES)
        for position in range(groups)
    ]
    index = FakeIndex(INDEX.unigrams, INDEX.bigrams, INDEX.trigrams)
    census = driver.census_population(population, index, VOCABULARY, UV_INDICES, SLICE_BASELINE)
    return driver.build_live_candidates(
        census["dispatch"],
        population,
        expected_total=groups,
        expected_counts={"dassle-spelling": groups, "dassle-spelling-preservation": 0},
    )


class CaptureTransport:
    def __init__(self, choice: str = "KEEP_ORIGINAL") -> None:
        self.choice = choice
        self.calls = 0
        self.bodies: list[bytes] = []

    def request(
        self, endpoint: str, body: bytes, headers: dict[str, str], timeout: float
    ) -> tuple[int, dict[str, str], bytes]:
        del endpoint, headers, timeout
        self.calls += 1
        self.bodies.append(body)
        payload = json.dumps(_sibling.validator_response(self.choice)).encode("utf-8")
        return 200, {"Content-Type": "application/json"}, payload


class FailingTransport:
    def __init__(self, status: int = 500) -> None:
        self.status = status
        self.calls = 0

    def request(
        self, endpoint: str, body: bytes, headers: dict[str, str], timeout: float
    ) -> tuple[int, dict[str, str], bytes]:
        del endpoint, body, headers, timeout
        self.calls += 1
        return self.status, {"Content-Type": "application/json"}, b"not a choice"


class BarrierTransport:
    """Hold the first ``width`` calls in flight until ``width`` are concurrent."""

    def __init__(self, width: int) -> None:
        self.width = width
        self.lock = threading.Lock()
        self.in_flight = 0
        self.max_in_flight = 0
        self.calls = 0
        self.released = threading.Event()
        self.payload = json.dumps(_sibling.validator_response("KEEP_ORIGINAL")).encode("utf-8")

    def request(
        self, endpoint: str, body: bytes, headers: dict[str, str], timeout: float
    ) -> tuple[int, dict[str, str], bytes]:
        del endpoint, body, headers, timeout
        with self.lock:
            self.calls += 1
            self.in_flight += 1
            self.max_in_flight = max(self.max_in_flight, self.in_flight)
            if self.in_flight == self.width:
                self.released.set()
            hold = self.in_flight <= self.width and not self.released.is_set()
        if hold and not self.released.wait(timeout=10):
            raise AssertionError("workers never reached the frozen width in flight")
        with self.lock:
            self.in_flight -= 1
        return 200, {"Content-Type": "application/json"}, self.payload


class LiveCandidateProjectionTests(unittest.TestCase):
    def test_only_unique_dispatchable_tops_become_live_items(self) -> None:
        census, items = synthetic_live_items()
        self.assertEqual(len(items), 3)
        self.assertEqual({item["case_index"] for item in items}, {11, 22, 44})
        for item in items:
            self.assertEqual(
                set(item),
                {
                    "phase",
                    "case_index",
                    "case_id",
                    "target_ordinal",
                    "target_start",
                    "target_end",
                    "candidate",
                    "candidate_form",
                    "operation",
                    "mechanical_edit",
                    "sentence",
                },
            )
            for forbidden in ("reference", "gold", "score", "dispatch", "candidates"):
                self.assertNotIn(forbidden, item)
            self.assertEqual(item["mechanical_edit"][2], item["candidate_form"])
            self.assertEqual(item["candidate"]["text"], LOOKUP)
            self.assertEqual(item["sentence"], SENTENCE)
        ids = [protocol.candidate_path_id(item) for item in items]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids, sorted(ids))
        tied = census["records"][2]
        self.assertTrue(tied["ranking"]["tied"])
        self.assertIsNone(tied["dispatch"])

    def test_live_item_count_gate_rejects_wrong_population(self) -> None:
        census, _items = synthetic_live_items()
        population = synthetic_population()
        with self.assertRaisesRegex(driver.ExperimentError, "live C>1 candidate count mismatch"):
            driver.build_live_candidates(
                census["dispatch"],
                population,
                expected_total=4,
                expected_counts=SYNTHETIC_C_GT_1_COUNTS,
            )


class LiveRequestPurityTests(unittest.TestCase):
    def test_only_the_cpu_winner_is_requested_with_no_list_gold_or_score(self) -> None:
        _census, items = synthetic_live_items()
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            transport = CaptureTransport()
            statuses = driver.execute_fresh_007m(
                root, items, "https://synthetic.invalid", "MISSING", transport=transport
            )
            self.assertEqual(sum(value["completed"] for value in statuses.values()), 3)
            self.assertEqual(len(statuses), 8)
            self.assertEqual(transport.calls, 3)
            request_root = root / "requests"
            actual_dirs = sorted(path.name for path in request_root.iterdir())
            expected_dirs = sorted(protocol.candidate_path_id(item) for item in items)
            self.assertEqual(actual_dirs, expected_dirs)
            recorded = set(transport.bodies)
            for item in items:
                body = protocol.request_body(
                    item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
                )
                expected_bytes = protocol.canonical_bytes(body)
                self.assertIn(expected_bytes, recorded)
                persisted = (
                    request_root / protocol.candidate_path_id(item) / "request.json"
                ).read_bytes()
                self.assertEqual(persisted, expected_bytes)
                rendered = expected_bytes.decode("utf-8")
                prompt = protocol.prompt_text(
                    item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
                )
                self.assertEqual(body["input"][0]["content"][0]["text"], prompt)
                self.assertEqual(set(body), set(prior_j.EXPECTED_REQUEST_FIELDS))
                self.assertNotIn("gold", rendered)
                self.assertNotIn("reference", rendered)
                self.assertNotIn("score", rendered)
            case_11 = next(item for item in items if item["case_index"] == 11)
            winner_11 = protocol.request_body(
                case_11["sentence"], case_11["candidate"]["text"], case_11["mechanical_edit"][2]
            )
            rendered_11 = protocol.canonical_bytes(winner_11).decode("utf-8")
            for runner_up in ("belo", "belal"):
                self.assertNotIn(runner_up, rendered_11)
            case_44 = next(item for item in items if item["case_index"] == 44)
            winner_44 = protocol.request_body(
                case_44["sentence"], case_44["candidate"]["text"], case_44["mechanical_edit"][2]
            )
            rendered_44 = protocol.canonical_bytes(winner_44).decode("utf-8")
            self.assertNotIn("belal", rendered_44)


class LiveReuseGateTests(unittest.TestCase):
    def test_c_gt_1_reuse_is_disabled_by_the_frozen_drift_decision(self) -> None:
        self.assertEqual(
            driver.c_gt_1_reuse_reason(driver.EXPECTED_007M_PROFILE_SHA256),
            driver.C_GT_1_REUSE_DISABLED,
        )
        with self.assertRaisesRegex(driver.ExperimentError, "profile-drift"):
            driver.c_gt_1_reuse_reason(prior_j.EXPECTED_PROFILE)

    def test_frozen_identity_gate_still_governs_observations(self) -> None:
        item, old_item, request_bytes, configuration, deployment = _sibling.reuse_fixture()
        observation = {
            "request_sha256": driver.sha256_bytes(request_bytes),
            "response_sha256": "raw-response-hash",
        }
        self.assertIsNone(
            prior_j.reuse_identity_reason(
                item,
                old_item,
                request_bytes,
                request_bytes,
                observation,
                "raw-response-hash",
                configuration,
                deployment,
            )
        )
        drifted = {**deployment, "profile_sha256": driver.EXPECTED_007M_PROFILE_SHA256}
        self.assertEqual(
            prior_j.reuse_identity_reason(
                item,
                old_item,
                request_bytes,
                request_bytes,
                observation,
                "raw-response-hash",
                configuration,
                drifted,
            ),
            "deployment-identity-mismatch",
        )

    def test_live_deployment_freezes_the_strategy_accepted_profile(self) -> None:
        source_configuration = {
            "deployment": {
                "endpoint": "http://synthetic.invalid/v1",
                "credential_env": "OAP_007_J_QWEN_BEARER",
                "profile_path": "/private/profile.toml",
            }
        }
        with tempfile.TemporaryDirectory() as raw_root:
            profile = Path(raw_root) / "profile.toml"
            profile.write_bytes(b"synthetic profile bytes")
            actual_sha = driver.sha256_file(profile)
            with patch.object(driver, "EXPECTED_007M_PROFILE_SHA256", actual_sha):
                deployment = driver.live_deployment(
                    source_configuration, profile, "OAP_007_J_QWEN_BEARER"
                )
            self.assertEqual(deployment["profile_sha256"], actual_sha)
            self.assertEqual(deployment["frozen_007j_profile_sha256"], prior_j.EXPECTED_PROFILE)
            self.assertTrue(deployment["profile_drift"])
            self.assertEqual(deployment["model"], protocol.MODEL)
            self.assertEqual(deployment["protocol"], "Responses non-streaming")
            self.assertEqual(deployment["credential_env"], "OAP_007_J_QWEN_BEARER")
            with self.assertRaisesRegex(driver.ExperimentError, "fresh-call identity"):
                driver.live_deployment(source_configuration, profile, None)
            with (
                patch.object(driver, "EXPECTED_007M_PROFILE_SHA256", actual_sha),
                self.assertRaisesRegex(driver.ExperimentError, "not the frozen 007-j identity"),
            ):
                driver.live_deployment(source_configuration, profile, "OTHER_CREDENTIAL")
            with (
                patch.object(driver, "EXPECTED_007M_PROFILE_SHA256", actual_sha),
                self.assertRaisesRegex(driver.ExperimentError, "007-j deployment identity"),
            ):
                driver.live_deployment({}, profile, None)


class C1RejectionSemanticsTests(unittest.TestCase):
    """Rejected C>1 targets keep the original while unrelated edits survive."""

    SOURCE = "a b c d"

    def _case(self) -> dict[str, object]:
        saved = {
            "id": "case-1",
            "index": 1,
            "input": self.SOURCE,
            "input_sha256": hashlib.sha256(self.SOURCE.encode()).hexdigest(),
            "detector": {"candidates": [], "english": []},
            "decisions": [
                {
                    "candidate": {"start": 0, "end": 1, "text": "a"},
                    "first": None,
                    "retry": None,
                    "final_gate": {"accepted": True},
                    "final_case": {"adjusted_replacement": "A"},
                },
                {
                    "candidate": {"start": 2, "end": 3, "text": "b"},
                    "first": None,
                    "retry": None,
                    "final_gate": {"accepted": False},
                    "final_case": None,
                },
            ],
            "calls": [],
            "output": self.SOURCE,
            "edits": [],
            "operational_failure": False,
        }
        return {
            "phase": "dassle-spelling",
            "index": 1,
            "id": "case-1",
            "dataset": {"reference": None},
            "baseline": saved,
            "new": copy.deepcopy(saved),
        }

    def _item(self) -> dict[str, object]:
        return {
            "phase": "dassle-spelling",
            "case_index": 1,
            "case_id": "case-1",
            "target_ordinal": 0,
            "target_start": 2,
            "target_end": 3,
            "candidate": {"start": 2, "end": 3, "text": "b"},
            "candidate_form": "B",
            "operation": "SUBSTITUTION",
            "mechanical_edit": [2, 3, "B"],
            "sentence": self.SOURCE,
        }

    def _record(self, observation: dict[str, object]) -> dict[str, object]:
        item = self._item()
        return driver.validator_driver.make_case_result(
            "dassle-spelling",
            self._case(),
            [item],
            {protocol.candidate_path_id(item): observation},
            "configuration",
        )

    def test_keep_uncertain_and_failure_keep_original_and_preserve_unrelated_edit(self) -> None:
        for choice in ("KEEP_ORIGINAL", "UNCERTAIN"):
            record = self._record(
                {"decision": choice, "operational_failure": False, "dispatch": "ATTEMPTED"}
            )
            with self.subTest(choice=choice):
                self.assertEqual(record["validated_only"]["output"], "A b c d")
                self.assertEqual(record["validated_only"]["edits"], [[0, 1, "A"]])
                self.assertEqual(record["validated_fallback"]["output"], "A b c d")
                target = record["validator_targets"][0]
                self.assertEqual(target["decision"], choice)
                self.assertFalse(target["applied_only"])
        record = self._record(
            {"decision": None, "operational_failure": True, "dispatch": "ATTEMPTED"}
        )
        self.assertEqual(record["validated_only"]["output"], "A b c d")
        self.assertEqual(record["validated_only"]["edits"], [[0, 1, "A"]])
        self.assertIsNone(record["validator_targets"][0]["decision"])

    def test_use_applies_only_the_supplied_candidate(self) -> None:
        record = self._record(
            {"decision": "USE_CANDIDATE", "operational_failure": False, "dispatch": "ATTEMPTED"}
        )
        self.assertEqual(record["validated_only"]["output"], "A B c d")
        self.assertEqual(record["validated_only"]["edits"], [[0, 1, "A"], [2, 3, "B"]])
        self.assertEqual(record["validated_fallback"]["output"], "A B c d")
        target = record["validator_targets"][0]
        self.assertEqual(target["decision"], "USE_CANDIDATE")
        self.assertTrue(target["applied_only"])
        self.assertEqual(target["mechanical_edit"], [2, 3, "B"])


class LiveExecutionResumeTests(unittest.TestCase):
    def test_eight_stable_workers_with_one_in_flight_each(self) -> None:
        items = multi_live_items(12)
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            transport = BarrierTransport(width=8)
            statuses = driver.execute_fresh_007m(
                root, items, "https://synthetic.invalid", "MISSING", transport=transport
            )
            self.assertEqual(transport.calls, 12)
            self.assertEqual(transport.max_in_flight, 8)
            self.assertEqual(len(statuses), 8)
            assigned = {key: value["assigned"] for key, value in statuses.items()}
            self.assertEqual(assigned, {0: 2, 1: 2, 2: 2, 3: 2, 4: 1, 5: 1, 6: 1, 7: 1})
            self.assertEqual(sum(value["completed"] for value in statuses.values()), 12)
            partition = protocol.partitions(items)
            for worker in range(8):
                self.assertEqual(
                    [protocol.candidate_path_id(item) for item in partition[worker]],
                    sorted(protocol.candidate_path_id(item) for item in partition[worker]),
                )

    def test_completed_observations_resume_without_resampling(self) -> None:
        items = multi_live_items(9)
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            first = _sibling.FakeTransport()
            driver.execute_fresh_007m(
                root, items, "https://synthetic.invalid", "MISSING", transport=first
            )
            self.assertEqual(first.calls, 9)
            digests = {}
            for item in items:
                directory = root / "requests" / protocol.candidate_path_id(item)
                digests[protocol.candidate_path_id(item)] = driver.sha256_file(
                    directory / "observation.json"
                )
            second = _sibling.FakeTransport()
            statuses = driver.execute_fresh_007m(
                root,
                list(reversed(items)),
                "https://synthetic.invalid",
                "MISSING",
                transport=second,
            )
            self.assertEqual(second.calls, 0)
            self.assertEqual(sum(value["completed"] for value in statuses.values()), 9)
            for item in items:
                directory = root / "requests" / protocol.candidate_path_id(item)
                self.assertEqual(
                    driver.sha256_file(directory / "observation.json"),
                    digests[protocol.candidate_path_id(item)],
                )

    def test_uncertain_delivery_is_never_retried(self) -> None:
        item = multi_live_items(1)[0]
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            directory = root / "requests" / protocol.candidate_path_id(item)
            directory.parent.mkdir(mode=0o700)
            os.chmod(directory.parent, 0o700)
            directory.mkdir(mode=0o700)
            os.chmod(directory, 0o700)
            body = protocol.request_body(
                item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
            )
            protocol.immutable_write(directory / "request.json", protocol.canonical_bytes(body))
            transport = _sibling.FakeTransport()
            statuses = driver.execute_fresh_007m(
                root, [item], "https://synthetic.invalid", "MISSING", transport=transport
            )
            self.assertEqual(transport.calls, 0)
            self.assertEqual(statuses[0]["failures"], 1)
            observation = json.loads((directory / "observation.json").read_text())
            self.assertEqual(observation["dispatch"], "UNKNOWN")
            self.assertEqual(observation["failure"], "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE")
            observations, counts = driver.verify_c_gt_1_observations(root, [item])
            self.assertEqual(counts, {"dispatched": 0, "uncertain": 1, "operational_failures": 1})
            self.assertIn(protocol.candidate_path_id(item), observations)
            retry = _sibling.FakeTransport()
            driver.execute_fresh_007m(
                root, [item], "https://synthetic.invalid", "MISSING", transport=retry
            )
            self.assertEqual(retry.calls, 0)

    def test_operational_failure_stays_distinct_from_keep(self) -> None:
        item = multi_live_items(1)[0]
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            transport = FailingTransport(status=500)
            statuses = driver.execute_fresh_007m(
                root, [item], "https://synthetic.invalid", "MISSING", transport=transport
            )
            self.assertEqual(transport.calls, 1)
            self.assertEqual(statuses[0]["failures"], 1)
            self.assertEqual(statuses[0]["dispatched_http"], 1)
            directory = root / "requests" / protocol.candidate_path_id(item)
            observation = json.loads((directory / "observation.json").read_text())
            self.assertTrue(observation["operational_failure"])
            self.assertEqual(observation["failure"], "HTTP_STATUS")
            self.assertIsNone(observation["decision"])
            self.assertIsNone(protocol.observation_decision(observation))
            observations, counts = driver.verify_c_gt_1_observations(root, [item])
            self.assertEqual(counts["dispatched"], 1)
            self.assertEqual(counts["uncertain"], 0)
            self.assertEqual(counts["operational_failures"], 1)
            self.assertEqual(observations[protocol.candidate_path_id(item)], observation)

    def test_completed_verification_rejects_byte_drift(self) -> None:
        item = multi_live_items(1)[0]
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            transport = _sibling.FakeTransport(choice="KEEP_ORIGINAL")
            driver.execute_fresh_007m(
                root, [item], "https://synthetic.invalid", "MISSING", transport=transport
            )
            directory = root / "requests" / protocol.candidate_path_id(item)
            raw_path = directory / "raw-response.json"
            original_raw = raw_path.read_bytes()
            raw_path.write_bytes(original_raw + b" ")
            os.chmod(raw_path, 0o600)
            with self.assertRaisesRegex(driver.ExperimentError, "observation identity"):
                driver.verify_c_gt_1_observations(root, [item])
            raw_path.write_bytes(original_raw)
            os.chmod(raw_path, 0o600)
            request_path = directory / "request.json"
            original_request = request_path.read_bytes()
            request_path.write_bytes(original_request + b" ")
            os.chmod(request_path, 0o600)
            with self.assertRaisesRegex(driver.ExperimentError, "observation identity"):
                driver.verify_c_gt_1_observations(root, [item])
            request_path.write_bytes(original_request)
            os.chmod(request_path, 0o600)
            _observations, counts = driver.verify_c_gt_1_observations(root, [item])
            self.assertEqual(counts["dispatched"], 1)


class LiveConfigurationFreezeTests(unittest.TestCase):
    def test_configuration_freezes_identity_budget_and_disabled_reuse(self) -> None:
        _census, items = synthetic_live_items()
        identity = {
            "implementation_head": "f" * 40,
            "branch": driver.BRANCH,
            "head_blobs": {"research/levenshtein_rank.py": {"sha256": "0" * 64}},
        }
        source = {
            "source_root": "/native/007j-root",
            "source_experiment": "007-j-levenshtein-one-contextual-validator",
            "configuration_sha256": "1" * 64,
            "candidate_manifest_sha256": "2" * 64,
            "results_sha256": "3" * 64,
        }
        deployment = {
            "class": "A100-FP8",
            "model": protocol.MODEL,
            "endpoint": "http://synthetic.invalid/v1",
            "profile_path": "/private/profile.toml",
            "profile_sha256": driver.EXPECTED_007M_PROFILE_SHA256,
            "frozen_007j_profile_sha256": prior_j.EXPECTED_PROFILE,
            "profile_drift": True,
            "credential_env": "OAP_007_J_QWEN_BEARER",
            "protocol": "Responses non-streaming",
        }
        analysis = {"entering_targets": {}, "transition_matrix": {}, "c0_counts": {}}
        configuration = driver.build_live_configuration(
            identity,
            source,
            dict(driver.EXPECTED_007J_REQUEST_TREE),
            dict(driver.EXPECTED_CENSUS_SHA),
            {"prior_007i_identity": {"configuration_sha256": prior_j.EXPECTED_PRIOR_CONFIG}},
            deployment,
            analysis,
            items,
            [{"candidate_id": "c1"}],
            Path("/native/scratch"),
        )
        self.assertEqual(configuration["status"], "FROZEN_BEFORE_LIVE_EXECUTION")
        self.assertEqual(configuration["implementation_head"], "f" * 40)
        self.assertEqual(configuration["census_root"]["name"], driver.EXPECTED_CENSUS_ROOT)
        self.assertEqual(
            configuration["census_root"]["superseded_diagnostic_root"],
            driver.SUPERSEDED_CENSUS_ROOT,
        )
        self.assertEqual(configuration["reuse"]["c_gt_1_reused"], 0)
        self.assertEqual(configuration["reuse"]["c_gt_1_fresh"], 3)
        self.assertEqual(
            configuration["reuse"]["c_gt_1_disabled_reason"], driver.C_GT_1_REUSE_DISABLED
        )
        self.assertEqual(configuration["reuse"]["c1_copied_observations"], 1)
        self.assertEqual(configuration["scheduling"]["workers"], protocol.WORKERS)
        self.assertEqual(configuration["scheduling"]["scheduled_new_calls"], 3)
        self.assertEqual(configuration["scheduling"]["maximum_in_flight"], protocol.WORKERS)
        self.assertEqual(configuration["limits"]["new_call_budget"], 3)
        self.assertFalse(configuration["limits"]["resampling"])
        self.assertEqual(configuration["limits"]["timeout_seconds"], protocol.TIMEOUT_SECONDS)
        self.assertEqual(configuration["prompt"]["sha256"], protocol.FROZEN_PROMPT_SHA256)
        self.assertEqual(configuration["request"]["fields"], prior_j.EXPECTED_REQUEST_FIELDS)
        self.assertEqual(configuration["parser"], prior_j.EXPECTED_PARSER)
        self.assertTrue(configuration["deployment"]["profile_drift"])
        self.assertTrue(configuration["no_resampling"])
        self.assertEqual(
            configuration["population"]["scheduled_total"],
            driver.EXPECTED_007J_C1_TOTAL + driver.EXPECTED_C_GT_1_TOTAL,
        )
        self.assertIn("no runner-up", configuration["method"]["c_gt_1"])
        self.assertEqual(
            configuration["source_007j_identity"]["request_tree"],
            driver.EXPECTED_007J_REQUEST_TREE,
        )

    def test_census_root_verification_binds_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            parent = Path(raw_root)
            census = parent / driver.EXPECTED_CENSUS_ROOT
            census.mkdir(mode=0o700)
            os.chmod(census, 0o700)
            payload = b"\n"
            actual = driver.sha256_bytes(payload)
            (census / "RUN-STATUS.json").write_bytes(payload)
            os.chmod(census / "RUN-STATUS.json", 0o600)
            with (
                patch.object(driver, "EXPECTED_CENSUS_SHA", {"RUN-STATUS.json": actual}),
                patch.object(driver, "EXPECTED_CENSUS_ROOT", driver.EXPECTED_CENSUS_ROOT),
            ):
                self.assertEqual(driver.verify_census_root(census), {"RUN-STATUS.json": actual})
                (census / "RUN-STATUS.json").write_bytes(b"tampered")
                os.chmod(census / "RUN-STATUS.json", 0o600)
                with self.assertRaisesRegex(
                    driver.validator_driver.ExperimentError, "hash mismatch"
                ):
                    driver.verify_census_root(census)
            outside = parent / "other-root"
            outside.mkdir(mode=0o700)
            (outside / "RUN-STATUS.json").write_bytes(payload)
            os.chmod(outside / "RUN-STATUS.json", 0o600)
            with (
                patch.object(driver, "EXPECTED_CENSUS_SHA", {"RUN-STATUS.json": actual}),
                self.assertRaisesRegex(driver.ExperimentError, "accepted 007-m census root"),
            ):
                driver.verify_census_root(outside)



class InterruptedFileSetContractTests(unittest.TestCase):
    """Interrupted file-set contract after the harness revision.

    A crash after the dispatch marker is finalized without a call as the
    request plus the stale ATTEMPTED marker plus raw/observation UNKNOWN
    (or the same set without the marker) and verifies as an uncertain
    delivery that stays distinguishable from a completed ATTEMPTED
    observation.  An unfinalized request-only set and any identity drift
    remain rejected.
    """

    def _prepared(
        self, root: Path, item: dict[str, object]
    ) -> tuple[Path, dict[str, object], bytes]:
        directory = root / "requests" / protocol.candidate_path_id(item)
        directory.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(directory.parent, 0o700)
        directory.mkdir(mode=0o700)
        os.chmod(directory, 0o700)
        body = protocol.request_body(
            item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
        )
        return directory, body, protocol.canonical_bytes(body)

    def _completed(self, root: Path, item: dict[str, object], choice: str = "KEEP_ORIGINAL"):
        directory, body, _request_bytes = self._prepared(root, item)
        transport = CaptureTransport(choice)
        observation = protocol.perform_call(directory, body, transport=transport)
        return directory, transport, observation

    @staticmethod
    def _rewrite(path: Path, value: object) -> bytes:
        data = protocol.canonical_bytes(value)
        path.write_bytes(data)
        os.chmod(path, 0o600)
        return data

    def test_crash_after_dispatch_finalizes_without_a_call_and_verifies_as_uncertain(self) -> None:
        item = multi_live_items(1)[0]
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            directory, body, request_bytes = self._prepared(root, item)
            protocol.immutable_write(directory / "request.json", request_bytes)
            protocol.immutable_json(directory / "dispatch.json", {"dispatch": "ATTEMPTED"})
            transport = CaptureTransport()
            observation = protocol.perform_call(directory, body, transport=transport)
            self.assertEqual(transport.calls, 0)
            self.assertEqual(
                json.loads((directory / "dispatch.json").read_text())["dispatch"], "ATTEMPTED"
            )
            self.assertEqual(observation["dispatch"], "UNKNOWN")
            self.assertEqual(observation["failure"], "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE")
            observations, counts = driver.verify_c_gt_1_observations(root, [item])
            self.assertEqual(counts, {"dispatched": 0, "uncertain": 1, "operational_failures": 1})
            self.assertEqual(
                observations[protocol.candidate_path_id(item)],
                json.loads((directory / "observation.json").read_text()),
            )

    def test_interrupted_state_is_distinguishable_from_completed(self) -> None:
        items = multi_live_items(2)
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            first_transport = CaptureTransport("KEEP_ORIGINAL")
            directory, body, _request_bytes = self._prepared(root, items[0])
            protocol.perform_call(directory, body, transport=first_transport)
            crash_directory, crash_body, crash_bytes = self._prepared(root, items[1])
            protocol.immutable_write(crash_directory / "request.json", crash_bytes)
            protocol.immutable_json(crash_directory / "dispatch.json", {"dispatch": "ATTEMPTED"})
            crash_transport = CaptureTransport()
            protocol.perform_call(crash_directory, crash_body, transport=crash_transport)
            self.assertEqual(first_transport.calls, 1)
            self.assertEqual(crash_transport.calls, 0)
            _observations, counts = driver.verify_c_gt_1_observations(root, items)
            self.assertEqual(counts, {"dispatched": 1, "uncertain": 1, "operational_failures": 1})

    def test_three_file_interruption_verifies_as_uncertain(self) -> None:
        item = multi_live_items(1)[0]
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            directory, body, request_bytes = self._prepared(root, item)
            protocol.immutable_write(directory / "request.json", request_bytes)
            transport = CaptureTransport()
            protocol.perform_call(directory, body, transport=transport)
            self.assertEqual(transport.calls, 0)
            self.assertEqual(
                {entry.name for entry in directory.iterdir()},
                {"request.json", "raw-response.json", "observation.json"},
            )
            _observations, counts = driver.verify_c_gt_1_observations(root, [item])
            self.assertEqual(counts, {"dispatched": 0, "uncertain": 1, "operational_failures": 1})

    def test_unfinalized_request_only_state_is_rejected(self) -> None:
        item = multi_live_items(1)[0]
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            directory, _body, request_bytes = self._prepared(root, item)
            protocol.immutable_write(directory / "request.json", request_bytes)
            protocol.immutable_json(directory / "dispatch.json", {"dispatch": "ATTEMPTED"})
            with self.assertRaisesRegex(driver.ExperimentError, "request set is invalid"):
                driver.verify_c_gt_1_observations(root, [item])

    def test_completed_observation_with_unknown_raw_is_rejected(self) -> None:
        item = multi_live_items(1)[0]
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            directory, _transport, _observation = self._completed(root, item)
            raw = json.loads((directory / "raw-response.json").read_text())
            raw.update(
                {
                    "dispatch": "UNKNOWN",
                    "dispatch_attempted": False,
                    "operational_failure": True,
                    "failure": "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE",
                    "http_seconds": None,
                    "http_status": None,
                }
            )
            raw_bytes = self._rewrite(directory / "raw-response.json", raw)
            observation = json.loads((directory / "observation.json").read_text())
            observation["response_sha256"] = driver.sha256_bytes(raw_bytes)
            self._rewrite(directory / "observation.json", observation)
            with self.assertRaisesRegex(driver.ExperimentError, "observation identity"):
                driver.verify_c_gt_1_observations(root, [item])

    def test_dispatch_marker_drift_is_rejected(self) -> None:
        item = multi_live_items(1)[0]
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            directory, _transport, _observation = self._completed(root, item)
            self._rewrite(directory / "dispatch.json", {"dispatch": "UNKNOWN"})
            with self.assertRaisesRegex(driver.ExperimentError, "observation identity"):
                driver.verify_c_gt_1_observations(root, [item])

    def test_non_interrupted_raw_failure_is_rejected(self) -> None:
        item = multi_live_items(1)[0]
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            directory, body, request_bytes = self._prepared(root, item)
            protocol.immutable_write(directory / "request.json", request_bytes)
            protocol.immutable_json(directory / "dispatch.json", {"dispatch": "ATTEMPTED"})
            protocol.perform_call(directory, body, transport=CaptureTransport())
            raw = json.loads((directory / "raw-response.json").read_text())
            raw["failure"] = "TIMEOUT"
            raw_bytes = self._rewrite(directory / "raw-response.json", raw)
            observation = json.loads((directory / "observation.json").read_text())
            observation["response_sha256"] = driver.sha256_bytes(raw_bytes)
            self._rewrite(directory / "observation.json", observation)
            with self.assertRaisesRegex(driver.ExperimentError, "observation identity"):
                driver.verify_c_gt_1_observations(root, [item])

    def test_request_byte_drift_is_rejected(self) -> None:
        item = multi_live_items(1)[0]
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            directory, _transport, _observation = self._completed(root, item)
            request_path = directory / "request.json"
            request_path.write_bytes(request_path.read_bytes() + b" ")
            os.chmod(request_path, 0o600)
            with self.assertRaisesRegex(driver.ExperimentError, "observation identity"):
                driver.verify_c_gt_1_observations(root, [item])

    def test_three_file_attempted_content_is_rejected(self) -> None:
        item = multi_live_items(1)[0]
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            directory, _transport, _observation = self._completed(root, item)
            (directory / "dispatch.json").unlink()
            with self.assertRaisesRegex(driver.ExperimentError, "interruption identity"):
                driver.verify_c_gt_1_observations(root, [item])


class FailedRootAdoptionTests(unittest.TestCase):
    """Cross-root adoption of a preserved failed-instrument root (synthetic).

    The fixture mirrors the ffdf13 contract: two completed ATTEMPTED
    observations, one persisted uncertain finalization, one request-only
    interruption and one missing target.  All constants are patched to the
    synthetic identities so no real root is touched.
    """

    FAILED_NAME = "007-m-rank-ambiguous-levenshtein-candidates-recovery.synthetic"

    def _build_failed_root(
        self, parent: Path
    ) -> tuple[Path, list[dict[str, object]], dict[str, object]]:
        items = multi_live_items(5)
        failed = parent / self.FAILED_NAME
        failed.mkdir(mode=0o700)
        os.chmod(failed, 0o700)
        for position, item in enumerate(items[:4]):
            directory = failed / "requests" / protocol.candidate_path_id(item)
            directory.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            os.chmod(directory.parent, 0o700)
            directory.mkdir(mode=0o700)
            os.chmod(directory, 0o700)
            body = protocol.request_body(
                item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
            )
            if position == 0:
                protocol.perform_call(directory, body, transport=CaptureTransport("KEEP_ORIGINAL"))
            elif position == 1:
                protocol.perform_call(directory, body, transport=CaptureTransport("USE_CANDIDATE"))
            else:
                protocol.immutable_write(
                    directory / "request.json", protocol.canonical_bytes(body)
                )
                protocol.immutable_json(directory / "dispatch.json", {"dispatch": "ATTEMPTED"})
                if position == 2:
                    protocol.interrupted_observation(directory, body)
        configuration = {
            "run_id": "007-m",
            "status": "FROZEN_BEFORE_LIVE_EXECUTION",
            "implementation_head": "f" * 40,
            "deployment": {
                "endpoint": "http://synthetic.invalid/v1",
                "model": protocol.MODEL,
                "credential_env": "OAP_007_J_QWEN_BEARER",
                "profile_sha256": "0" * 64,
            },
            "prompt": {"sha256": protocol.FROZEN_PROMPT_SHA256},
            "parser": prior_j.EXPECTED_PARSER,
        }
        driver.validator_driver.immutable_json(failed / "CONFIGURATION.json", configuration)
        driver.validator_driver.immutable_json(
            failed / "RUN-STATUS.json",
            {"status": "FROZEN_BEFORE_LIVE_EXECUTION", "run_id": "007-m"},
        )
        return failed, items, configuration

    @contextlib.contextmanager
    def _patched(self, failed: Path, **overrides: object):
        values = {
            "EXPECTED_FAILED_ROOT": self.FAILED_NAME,
            "EXPECTED_FAILED_ROOT_CONFIGURATION": driver.sha256_file(
                failed / "CONFIGURATION.json"
            ),
            "EXPECTED_FAILED_ROOT_HEAD": "f" * 40,
            "EXPECTED_FAILED_ROOT_RUN_STATUS": driver.sha256_file(failed / "RUN-STATUS.json"),
            "EXPECTED_FAILED_ROOT_REQUEST_TREE": driver.validator_driver.request_tree_identity(
                failed / "requests"
            ),
            "EXPECTED_ADOPTED_COMPLETED_ATTEMPTED": 2,
            "EXPECTED_ADOPTED_COMPLETED_UNCERTAIN": 1,
            "EXPECTED_ADOPTED_REQUEST_ONLY": 1,
            "EXPECTED_ADOPTED_FRESH": 1,
            "EXPECTED_007M_PROFILE_SHA256": "0" * 64,
        }
        values.update(overrides)
        with contextlib.ExitStack() as stack:
            for name, value in values.items():
                stack.enter_context(patch.object(driver, name, value))
            yield

    def _scratch(self, parent: Path, name: str = "adoption-scratch") -> Path:
        scratch = parent / name
        scratch.mkdir(mode=0o700)
        os.chmod(scratch, 0o700)
        return scratch

    def test_verify_failed_root_census_and_tamper_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            parent = Path(raw_root)
            failed, items, _configuration = self._build_failed_root(parent)
            scratch = self._scratch(parent)
            with self._patched(failed):
                result = driver.verify_failed_root(failed, scratch, items)
                self.assertEqual(
                    result["state_census"],
                    {
                        "completed_attempted": 2,
                        "completed_uncertain_persisted": 1,
                        "request_only_interrupted": 1,
                        "missing": 1,
                    },
                )
                self.assertFalse(result["resampled"])
                self.assertEqual(len(result["states"]), 5)
                request_path = (
                    failed / "requests" / protocol.candidate_path_id(items[0]) / "request.json"
                )
                request_path.write_bytes(request_path.read_bytes() + b" ")
                os.chmod(request_path, 0o600)
                with self.assertRaisesRegex(
                    driver.ExperimentError, "request tree identity changed"
                ):
                    driver.verify_failed_root(failed, scratch, items)

    def test_failed_root_census_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            parent = Path(raw_root)
            failed, items, _configuration = self._build_failed_root(parent)
            scratch = self._scratch(parent)
            with (
                self._patched(failed, EXPECTED_ADOPTED_COMPLETED_ATTEMPTED=3),
                self.assertRaisesRegex(driver.ExperimentError, "state census drifted"),
            ):
                driver.verify_failed_root(failed, scratch, items)

    def test_failed_root_identity_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            parent = Path(raw_root)
            failed, items, _configuration = self._build_failed_root(parent)
            scratch = self._scratch(parent)
            configuration_path = failed / "CONFIGURATION.json"
            original_sha = driver.sha256_file(configuration_path)
            configuration_path.write_bytes(configuration_path.read_bytes() + b" ")
            os.chmod(configuration_path, 0o600)
            with (
                self._patched(failed, EXPECTED_FAILED_ROOT_CONFIGURATION=original_sha),
                self.assertRaisesRegex(
                    driver.validator_driver.ExperimentError, "hash mismatch"
                ),
            ):
                driver.verify_failed_root(failed, scratch, items)

    def test_adopt_copies_completed_and_carry_finalizes_interrupted(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            parent = Path(raw_root)
            failed, items, configuration = self._build_failed_root(parent)
            scratch = self._scratch(parent)
            by_id = {protocol.candidate_path_id(item): item for item in items}
            with self._patched(failed):
                states = driver.verify_failed_root(failed, scratch, items)["states"]
                self.assertEqual(
                    sorted(set(states.values())),
                    ["ATTEMPTED", "INTERRUPTED_4FILE", "MISSING", "REQUEST_ONLY"],
                )
                identity_basis = driver._reuse_identity_basis(configuration)
                reuse_records = driver.adopt_completed_c_gt_1(
                    failed, scratch, items, states, identity_basis
                )
                self.assertEqual(len(reuse_records), 3)
                self.assertEqual(
                    [record["state"] for record in reuse_records],
                    ["completed-attempted", "completed-attempted", "interrupted-uncertain"],
                )
                self.assertEqual(
                    [record["new_calls"] for record in reuse_records], [0, 0, 0]
                )
                for record in reuse_records:
                    item = by_id[record["candidate_id"]]
                    source = failed / "requests" / record["candidate_id"]
                    destination = scratch / "requests" / record["candidate_id"]
                    for name in (
                        "request.json",
                        "dispatch.json",
                        "raw-response.json",
                        "observation.json",
                    ):
                        self.assertEqual(
                            driver.sha256_file(destination / name),
                            driver.sha256_file(source / name),
                        )
                    body = protocol.request_body(
                        item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
                    )
                    state, _observation = driver._c_gt_1_directory_state(
                        destination, protocol.canonical_bytes(body)
                    )
                    expected_state = (
                        driver.C_GT_1_STATE_ATTEMPTED
                        if record["state"] == "completed-attempted"
                        else driver.C_GT_1_STATE_INTERRUPTED_4FILE
                    )
                    self.assertEqual(state, expected_state)
                decisions = [record["decision"] for record in reuse_records]
                self.assertEqual(decisions[:2], ["KEEP_ORIGINAL", "USE_CANDIDATE"])
                self.assertIsNone(decisions[2])
                carry_records = driver.carry_interrupted_c_gt_1(failed, scratch, items, states)
                self.assertEqual(len(carry_records), 1)
                record = carry_records[0]
                item = by_id[record["candidate_id"]]
                destination = scratch / "requests" / record["candidate_id"]
                body = protocol.request_body(
                    item["sentence"], item["candidate"]["text"], item["mechanical_edit"][2]
                )
                state, observation = driver._c_gt_1_directory_state(
                    destination, protocol.canonical_bytes(body)
                )
                self.assertEqual(state, driver.C_GT_1_STATE_INTERRUPTED_4FILE)
                self.assertEqual(
                    observation["failure"], "INTERRUPTED_UNCERTAIN_DELIVERY_NO_RESAMPLE"
                )
                self.assertIsNone(observation["decision"])
                self.assertEqual(
                    driver.sha256_file(destination / "request.json"),
                    record["source_request_sha256"],
                )
                self.assertEqual(
                    driver.sha256_file(destination / "dispatch.json"),
                    record["source_dispatch_sha256"],
                )
                self.assertEqual(record["new_calls"], 0)
                with self.assertRaisesRegex(driver.ExperimentError, "already exists"):
                    driver.carry_interrupted_c_gt_1(failed, scratch, items, states)

    def test_build_live_configuration_adoption_block_and_frozen_regression(self) -> None:
        identity = {
            "implementation_head": "f" * 40,
            "branch": driver.BRANCH,
            "head_blobs": {"research/levenshtein_rank.py": {"sha256": "0" * 64}},
        }
        source = {
            "source_root": "/native/007j-root",
            "source_experiment": "007-j-levenshtein-one-contextual-validator",
            "configuration_sha256": "1" * 64,
            "candidate_manifest_sha256": "2" * 64,
            "results_sha256": "3" * 64,
        }
        deployment = {
            "class": "A100-FP8",
            "model": protocol.MODEL,
            "endpoint": "http://synthetic.invalid/v1",
            "profile_path": "/private/profile.toml",
            "profile_sha256": "0" * 64,
            "frozen_007j_profile_sha256": prior_j.EXPECTED_PROFILE,
            "profile_drift": True,
            "credential_env": "OAP_007_J_QWEN_BEARER",
            "protocol": "Responses non-streaming",
        }
        analysis = {"entering_targets": {}, "transition_matrix": {}, "c0_counts": {}}
        fresh = multi_live_items(1)
        c1_records = [{"candidate_id": "c1"}]
        scratch = Path("/native/scratch")
        reuse_records = [{"candidate_id": f"adopted-{index}"} for index in range(3)]
        adoption = {
            "failed_root": self.FAILED_NAME,
            "completed_reused": 3,
            "completed_reused_attempted": 2,
            "completed_reused_uncertain": 1,
            "interrupted_carried": 1,
            "fresh": 1,
            "linkage_sha256": "1" * 64,
            "reuse_records_sha256": "2" * 64,
            "carry_records_sha256": "3" * 64,
            "adopted_candidates_sha256": "4" * 64,
            "adopted_candidate_manifest_sha256": "5" * 64,
        }
        source_configuration = {
            "prior_007i_identity": {"configuration_sha256": prior_j.EXPECTED_PRIOR_CONFIG}
        }
        configuration = driver.build_live_configuration(
            identity,
            source,
            dict(driver.EXPECTED_007J_REQUEST_TREE),
            dict(driver.EXPECTED_CENSUS_SHA),
            source_configuration,
            deployment,
            analysis,
            fresh,
            c1_records,
            scratch,
            reuse_records=reuse_records,
            adoption=adoption,
        )
        self.assertEqual(configuration["adoption"], adoption)
        self.assertEqual(configuration["population"]["c_gt_1_completed_reused"], 3)
        self.assertEqual(configuration["population"]["c_gt_1_completed_reused_attempted"], 2)
        self.assertEqual(configuration["population"]["c_gt_1_completed_reused_uncertain"], 1)
        self.assertEqual(configuration["population"]["c_gt_1_interrupted_carried"], 1)
        self.assertEqual(configuration["population"]["c_gt_1_fresh"], 1)
        self.assertEqual(configuration["reuse"]["c_gt_1_reused"], 3)
        self.assertEqual(configuration["reuse"]["c_gt_1_interrupted_carried"], 1)
        self.assertIn("c_gt_1_cross_root_reuse_basis", configuration["reuse"])
        self.assertEqual(configuration["scheduling"]["scheduled_new_calls"], 1)
        self.assertEqual(configuration["limits"]["new_call_budget"], 1)
        frozen = driver.build_live_configuration(
            identity,
            source,
            dict(driver.EXPECTED_007J_REQUEST_TREE),
            dict(driver.EXPECTED_CENSUS_SHA),
            source_configuration,
            deployment,
            analysis,
            fresh,
            c1_records,
            scratch,
        )
        self.assertNotIn("adoption", frozen)
        self.assertEqual(frozen["reuse"]["c_gt_1_reused"], 0)
        self.assertNotIn("c_gt_1_cross_root_reuse_basis", frozen["reuse"])
        self.assertNotIn("c_gt_1_fresh", frozen["population"])


if __name__ == "__main__":
    unittest.main()
