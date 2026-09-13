"""Historical parser invariants, using synthetic non-linguistic replies only."""
import unittest

from research.curated.historical_transport import _parse_word
from research.curated.validation import parse_validator
from research.curated.retry import parse_contextual


def envelope(text):
    return {"output": [{"type": "message", "role": "assistant", "content": [
        {"type": "output_text", "text": text}
    ]}]}


class HistoricalParserFidelity(unittest.TestCase):
    def test_contextual_retry_retains_its_original_json_contract(self):
        proposal = parse_contextual(envelope('{"keep":false,"replacement":"xyz","needs_wider_edit":false}'))
        self.assertEqual(proposal.replacement, "xyz")
        with self.assertRaises(ValueError):
            parse_contextual(envelope("xyz"))

    def test_validator_rejects_duplicate_keys_like_original_parser(self):
        self.assertEqual(parse_validator(envelope('{"decision":"ACCEPT"}')), "ACCEPT")
        with self.assertRaises(ValueError):
            parse_validator(envelope('{"decision":"REJECT","decision":"ACCEPT"}'))

    def test_original_word_parser_retains_combining_marks(self):
        word = "abc\u0301"
        self.assertEqual(_parse_word(envelope(word)).replacement, word)
        with self.assertRaises(ValueError):
            _parse_word(envelope(word + " "))


if __name__ == "__main__":
    unittest.main()
