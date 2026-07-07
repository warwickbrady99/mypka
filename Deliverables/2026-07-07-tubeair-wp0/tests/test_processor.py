import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from tubeair.models import AiEnrichment, TranscriptLine
from tubeair.processor import process_youtube_url


class TestProcessor(unittest.TestCase):
    def test_process_youtube_url_saves_ai_enrichment(self):
        output_dir = Path("tmp-test-processor") / "out" / "youtube"
        enrichment = AiEnrichment(
            executive_summary="Summary.",
            key_takeaways=["One", "Two", "Three", "Four", "Five"],
            action_items=["Act"],
            entities=["OpenAI"],
            tags=["ai"],
            tldr="Short version.",
        )
        provider = Mock()
        provider.enrich.return_value = enrichment

        with patch(
            "tubeair.processor.fetch_transcript",
            return_value=[TranscriptLine(start=0.0, duration=1.0, text="Processor works.")],
        ), patch("tubeair.processor.create_ai_provider_from_env", return_value=provider):
            try:
                result = process_youtube_url(
                    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    out_dir=output_dir,
                )

                output_path = Path(result.output_path)
                self.assertEqual(result.enrichment, enrichment)
                self.assertIn("## AI Research Assistant", output_path.read_text(encoding="utf-8"))
            finally:
                output_path = output_dir / "dQw4w9WgXcQ.md"
                if output_path.exists():
                    output_path.unlink()
                if output_dir.exists():
                    output_dir.rmdir()
                out_dir = Path("tmp-test-processor") / "out"
                if out_dir.exists():
                    out_dir.rmdir()
                root_dir = Path("tmp-test-processor")
                if root_dir.exists():
                    root_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
