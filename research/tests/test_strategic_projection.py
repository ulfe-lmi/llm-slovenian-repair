"""Keep numeric evidence without accidentally copying text-bearing fields."""
from __future__ import annotations

import json
import unittest

from research.tools.build_public_registry import _safe_projection


class StrategicProjection(unittest.TestCase):
    def test_numeric_suppression_count_is_not_dropped_with_private_records(self) -> None:
        original = {
            "english_suppressions": [{"original_target": "SYNTHETIC_PRIVATE_CANARY"}],
            "methods": {
                "M2": {
                    "end_to_end": {"english_suppressions": 3, "tp": 2, "fp": 1}
                }
            },
        }
        projected = _safe_projection(original)
        self.assertEqual(
            projected["methods"]["M2"]["end_to_end"].get("english_suppressions"),
            3,
        )
        self.assertNotIn("SYNTHETIC_PRIVATE_CANARY", json.dumps(projected))

    def test_text_token_arrays_are_not_numeric_evidence(self) -> None:
        projected = _safe_projection(
            {
                "replacement_tokens": ["SYNTHETIC_PRIVATE_CANARY"],
                "call_latencies": [1.25, 2.5],
            }
        )
        self.assertNotIn("SYNTHETIC_PRIVATE_CANARY", json.dumps(projected))
        self.assertEqual(projected["call_latencies"], [1.25, 2.5])


if __name__ == "__main__":
    unittest.main()
