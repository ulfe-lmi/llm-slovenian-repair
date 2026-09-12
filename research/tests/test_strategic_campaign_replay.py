"""Exercise the actual preserved campaign record shape using synthetic content."""
import os
from pathlib import Path
import tempfile
import unittest

from research.tools.replay import ReplayEvidenceError, _create_fixture_index, replay_saved_record
from research.curated.historical_methods import no_retry


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

    def replay(self, record, **kwargs):
        scratch = Path(os.environ.get("TMPDIR", str(Path.cwd() / ".research-test-scratch")))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            index = Path(directory) / "index.sqlite"
            _create_fixture_index({"unigrams": {"abc": 100}}, index)
            return replay_saved_record(record, index, **kwargs)

    def test_campaign_nested_english_evidence_is_replayed(self):
        receipt = self.replay(self.record(suppressed=True))
        self.assertEqual(receipt["review_calls"], 0)
        self.assertEqual(receipt["english_values"], 1)
        self.assertEqual(receipt["model_calls"], 0)

    def test_verified_global_null_maximum_is_explicit_replay_configuration(self):
        record = self.record(suppressed=True)
        del record["maximum"]
        receipt = self.replay(record, configured_maximum=None)
        self.assertIsNone(receipt["detector_maximum"])
        with self.assertRaises(ReplayEvidenceError):
            self.replay(record)

    def test_recorded_first_call_failure_is_not_missing_proposal_or_keep(self):
        receipt = self.replay(self.record(suppressed=False))
        self.assertTrue(receipt["operational_failure"])
        self.assertEqual(receipt["model_calls"], 0)

    def test_retry_only_failure_preserves_full_original_but_not_m3_failure(self):
        record = self.record(suppressed=False)
        original = "qqqx zzzx"
        decisions = []
        english_rows = []
        first_calls = []
        for start, target, replacement, accepted in ((0, "qqqx", "abc", True),
                                                      (5, "zzzx", "xxxx", False)):
            candidate = {"start": start, "end": start + 4, "text": target, "score": 1.0,
                         "evidence": {"unigram": {"state": "UNAVAILABLE", "count": None}}}
            english = {**record["detector"]["english"][0], "casefolded_target": target,
                       "original_target": target}
            proposal = {"keep": False, "replacement": replacement, "needs_wider_edit": False}
            first = {"kind": "reviewer", "operational_failure": False, "proposal": proposal}
            first_calls.append(first)
            english_rows.append(english)
            decisions.append({"candidate": candidate, "english": english, "policy_preserved": False,
                              "first": first, "first_adjusted": proposal,
                              "first_gate": {"accepted": accepted,
                                             "reason": "unigram-exact" if accepted else "replacement-unigram-uncertain"},
                              "retry": None})
        failed_retry = {"kind": "expression-retry", "operational_failure": True,
                        "proposal": None, "failure": "TIMEOUT"}
        decisions[1]["retry"] = failed_retry
        record.update(input=original, output=original, decisions=decisions,
                      calls=first_calls + [failed_retry], no_retry_output="abc zzzx",
                      no_retry_operational_failure=False)
        record["detector"].update(candidates=[d["candidate"] for d in decisions],
                                  english=english_rows, eligible_words=2)
        receipt = self.replay(record)
        self.assertTrue(receipt["operational_failure"])
        self.assertEqual(receipt["model_calls"], 0)
        ablation = no_retry(original, record)
        self.assertFalse(ablation["operational_failure"])
        self.assertEqual(ablation["output"], "abc zzzx")


if __name__ == "__main__":
    unittest.main()
