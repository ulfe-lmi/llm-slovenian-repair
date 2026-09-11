"""Exercise the actual preserved campaign record shape using synthetic content."""
import os
from pathlib import Path
import tempfile
import unittest

from research.tools.replay import _create_fixture_index, replay_saved_record


class CampaignReplayShape(unittest.TestCase):
    def record(self, suppressed):
        candidate = {"start": 0, "end": 4, "text": "zzzx", "score": 1.0,
                     "evidence": {"unigram": {"state": "UNAVAILABLE", "count": None}}}
        english = {"casefolded_target": "zzzx", "original_target": "zzzx",
                   "english_frequency": 5.0 if suppressed else 0.0,
                   "english_classification": "ENGLISH_ATTESTED" if suppressed else "NOT_STRONGLY_ENGLISH_ATTESTED",
                   "review_suppressed": suppressed, "threshold": 3.0,
                   "slovene_unigram": {"state": "UNAVAILABLE", "count": None}}
        return {"id": "synthetic", "input": "zzzx", "output": "zzzx", "maximum": None,
                "method": "M2", "operational_failure": not suppressed,
                "no_retry_operational_failure": not suppressed, "no_retry_output": "zzzx",
                "detector": {"candidates": [candidate], "english": [english],
                             "eligible_words": 1, "protected_intervals": []},
                "decisions": [{"candidate": candidate, "english": english,
                               "policy_preserved": suppressed,
                               "first": None if suppressed else {"operational_failure": True,
                                                                  "failure": "TIMEOUT", "proposal": None},
                               "retry": None}], "edits": [], "no_retry_edits": []}

    def replay(self, record):
        scratch = Path(os.environ.get("TMPDIR", str(Path.cwd() / ".research-test-scratch")))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            index = Path(directory) / "index.sqlite"
            _create_fixture_index({"unigrams": {"abc": 100}}, index)
            return replay_saved_record(record, index)

    def test_campaign_nested_english_evidence_is_replayed(self):
        receipt = self.replay(self.record(suppressed=True))
        self.assertEqual(receipt["review_calls"], 0)
        self.assertEqual(receipt["english_values"], 1)
        self.assertEqual(receipt["model_calls"], 0)

    def test_recorded_first_call_failure_is_not_missing_proposal_or_keep(self):
        receipt = self.replay(self.record(suppressed=False))
        self.assertTrue(receipt["operational_failure"])
        self.assertEqual(receipt["model_calls"], 0)


if __name__ == "__main__":
    unittest.main()
