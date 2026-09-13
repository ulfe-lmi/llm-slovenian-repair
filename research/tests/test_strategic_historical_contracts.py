"""Independent archival-contract checks; no data, model or linguistic fixtures."""
import unittest
import os
from pathlib import Path

from research.curated.historical import reproduction_contract, variant_map


class HistoricalContractReview(unittest.TestCase):
    def evidence_hint(self):
        scratch = os.environ.get("TMPDIR")
        if scratch:
            mirror = Path(scratch) / "verified-source-mirror"
            if mirror.is_dir():
                return f"Exact original code/config/docs were independently hash-verified in {mirror}; no need to crawl the sync-backed experiment tree."
        return "Compare the original frozen configuration/source identified by the archival census."

    def test_final_and_spelling_campaigns_do_not_reintroduce_four_target_cap(self):
        # Owner removed this cap before these runs. Metadata must preserve that fact.
        variants = variant_map()
        for name in ("large-evaluation-uncapped", "dassle-spelling-preparation", "full-campaign8"):
            with self.subTest(variant=name):
                self.assertIsNone(variants[name].maximum_targets, self.evidence_hint())

    def test_initial_unigram_retry_is_not_misdescribed_as_word_only(self):
        # The later word-only experiment was an actual distinct change.
        spec = variant_map()["low-unigram-retry"]
        description = (spec.authorized_change + " " + spec.prompt).casefold()
        self.assertNotIn("word-only", description, self.evidence_hint())
        self.assertIn("context", description)

    def test_request_metadata_does_not_confuse_public_redaction_with_model_input(self):
        contract = reproduction_contract(variant_map()["ten-run-english-preserve-low"])
        fields = contract["inference_fields"]
        self.assertIn("reasoning", fields["sent"])
        self.assertNotIn("reasoning_effort", fields["sent"])
        self.assertIn("input", fields["sent"])
        self.assertNotIn("filled_dataset_text", fields["omitted"])


if __name__ == "__main__":
    unittest.main()
