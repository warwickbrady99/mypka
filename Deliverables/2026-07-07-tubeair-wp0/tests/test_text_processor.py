import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

from tubeair.models import AiEnrichment
from tubeair.processor import process_plain_text


class FakeAiProvider:
    def summarize_text(self, text: str) -> AiEnrichment:
        return AiEnrichment(
            executive_summary="This is the executive summary.",
            key_takeaways=["First point", "Second point"],
            action_items=["Follow up"],
            entities=["OpenAI", "London"],
            tags=["research", "notes"],
            tldr="This is the short version.",
        )


class TestTextProcessor(unittest.TestCase):
    def test_markdown_file_generation_for_text_summaries(self):
        out_dir = Path("tmp-test-text") / "out" / "text"
        try:
            with patch("tubeair.processor.create_ai_provider_from_env", return_value=FakeAiProvider()):
                result = process_plain_text("Important source text " * 40, out_dir=out_dir)

            output_path = Path(result.output_path)
            content = output_path.read_text(encoding="utf-8")

            self.assertTrue(output_path.exists())
            self.assertEqual(output_path.parent, out_dir)
            self.assertIn("# Text Summary", content)
            self.assertIn("### TL;DR", content)
            self.assertIn("This is the short version.", content)
            self.assertIn("### Executive Summary", content)
            self.assertIn("### Key Takeaways", content)
            self.assertIn("### Action Items", content)
            self.assertIn("### Important Names, Companies and Places", content)
            self.assertIn("### Tags", content)
            self.assertIn("## Source Text Excerpt", content)
        finally:
            root = Path("tmp-test-text")
            if root.exists():
                shutil.rmtree(root)


if __name__ == "__main__":
    unittest.main()
