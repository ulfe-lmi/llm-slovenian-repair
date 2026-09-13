"""Published configurations must preserve actual generic prompt bytes."""
import json
import hashlib
from pathlib import Path
import unittest

from research.curated.historical_pipeline import reviewer_prompt
from research.curated.historical_transport import EXPRESSION_RETRY_PROMPT, WORD_RETRY_PROMPT


class PromptArchiveFidelity(unittest.TestCase):
    def config(self, name):
        path = Path(__file__).resolve().parents[1] / "configs" / f"{name}.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_english_baseline_config_preserves_actual_prompt_bytes(self):
        config = self.config("ten-run-english-preserve-low")
        self.assertEqual(config["generic_prompt"], reviewer_prompt("{sentence}", "{target}"))
        self.assertEqual(config["retry_prompt"], EXPRESSION_RETRY_PROMPT)
        self.assertNotIn("filled_dataset_text", config["inference_fields"]["omitted"])

    def test_word_only_config_does_not_substitute_later_expression_prompt(self):
        config = self.config("low-word-only-retry")
        self.assertEqual(config["retry_prompt"], WORD_RETRY_PROMPT)

    def test_contextual_retry_preserves_original_instruction_identity(self):
        config = self.config("low-unigram-retry")
        # Exact generic INSTRUCTION from the preserved original retry.py; no fixture text.
        prefix = config["retry_prompt"].encode("utf-8")[:1442]
        self.assertEqual(hashlib.sha256(prefix).hexdigest(),
                         "79995ff7868cd307bf96f18916583b5ac310cc81d18b6ca70098185e79d93818")


if __name__ == "__main__":
    unittest.main()
