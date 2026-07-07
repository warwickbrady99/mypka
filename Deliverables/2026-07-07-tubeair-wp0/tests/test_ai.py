import unittest
from unittest.mock import patch

from tubeair.ai import AiConfigurationError, create_ai_provider_from_env, parse_enrichment, transcript_as_text
from tubeair.models import TranscriptLine


class TestAiProviderBoundary(unittest.TestCase):
    def test_create_provider_requires_openai_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(AiConfigurationError):
                create_ai_provider_from_env()

    def test_parse_enrichment_normalizes_provider_json(self):
        enrichment = parse_enrichment(
            {
                "executive_summary": "Summary.",
                "key_takeaways": ["One", "Two", "Three", "Four", "Five", "Six"],
                "action_items": ["Act"],
                "entities": ["OpenAI"],
                "tags": ["AI Research", "YouTube"],
                "tldr": "Short version.",
            }
        )

        self.assertEqual(enrichment.key_takeaways, ["One", "Two", "Three", "Four", "Five"])
        self.assertEqual(enrichment.tags, ["ai-research", "youtube"])

    def test_transcript_as_text_keeps_timestamps(self):
        text = transcript_as_text([TranscriptLine(start=12.5, duration=1.0, text="Hello.")])

        self.assertEqual(text, "[12s] Hello.")


if __name__ == "__main__":
    unittest.main()
