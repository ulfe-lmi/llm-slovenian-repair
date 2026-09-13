from __future__ import annotations

import unittest

from research.levenshtein_one import (
    DELETION,
    INSERTION,
    SUBSTITUTION,
    build_deletion_signature_index,
    cardinality,
    distance_one_candidates,
    operation_for_one_edit,
    standard_levenshtein_distance,
    vocabulary_code_points,
)


class LevenshteinOneTests(unittest.TestCase):
    def test_distance_is_code_point_standard_and_identity_is_zero(self) -> None:
        self.assertEqual(standard_levenshtein_distance("abc", "abc"), 0)
        self.assertEqual(standard_levenshtein_distance("abc", "axc"), 1)
        self.assertEqual(standard_levenshtein_distance("abc", "abxc"), 1)
        self.assertEqual(standard_levenshtein_distance("abxc", "abc"), 1)
        self.assertEqual(standard_levenshtein_distance("č", "č"), 2)

    def test_operations_and_distance_two_exclusions(self) -> None:
        self.assertEqual(operation_for_one_edit("abc", "axc"), SUBSTITUTION)
        self.assertEqual(operation_for_one_edit("abc", "abxc"), INSERTION)
        self.assertEqual(operation_for_one_edit("abxc", "abc"), DELETION)
        for left, right in (("abc", "abc"), ("abc", "axd"), ("abc", "acb")):
            self.assertIsNone(operation_for_one_edit(left, right))
            self.assertGreaterEqual(standard_levenshtein_distance(left, right), 0)
        self.assertEqual(standard_levenshtein_distance("abc", "axd"), 2)
        self.assertEqual(standard_levenshtein_distance("abc", "acb"), 2)
        self.assertEqual(standard_levenshtein_distance("abc", "abxc"), 1)

    def test_complete_union_is_deduplicated_and_operation_labeled(self) -> None:
        vocabulary = ["abc", "axc", "abxc", "ac", "acb", "axd", "abc"]
        index = build_deletion_signature_index(vocabulary)
        candidates = distance_one_candidates(
            "abc", vocabulary, deletion_index=index, alphabet=vocabulary_code_points(vocabulary)
        )
        self.assertEqual(
            candidates,
            [
                {"text": "abxc", "operation": INSERTION},
                {"text": "ac", "operation": DELETION},
                {"text": "axc", "operation": SUBSTITUTION},
            ],
        )
        self.assertEqual(cardinality(candidates), "C>1")

    def test_unique_cross_operation_candidate_and_transposition_are_distinct(self) -> None:
        self.assertEqual(
            distance_one_candidates("abc", {"abxc"}),
            [{"text": "abxc", "operation": INSERTION}],
        )
        self.assertEqual(distance_one_candidates("abc", {"acb"}), [])

    def test_no_normalization_or_whitespace_candidates(self) -> None:
        self.assertEqual(distance_one_candidates("žaba", {"žaba", "z aba"}), [])
        self.assertEqual(distance_one_candidates("", {"a"}), [])


if __name__ == "__main__":
    unittest.main()
