import unittest
from pathlib import Path

from tubeair.markdown import build_markdown, format_timestamp, save_markdown
from tubeair.models import AiEnrichment, TranscriptLine


class TestMarkdownGeneration(unittest.TestCase):
    def test_format_timestamp(self):
        self.assertEqual(format_timestamp(0), "00:00:00")
        self.assertEqual(format_timestamp(65.9), "00:01:05")
        self.assertEqual(format_timestamp(3661), "01:01:01")

    def test_build_markdown_keeps_timestamps(self):
        lines = [
            TranscriptLine(start=0.0, duration=2.0, text="Hello there."),
            TranscriptLine(start=65.2, duration=3.0, text="This is TubeAIR."),
        ]

        markdown = build_markdown("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ", lines)

        self.assertIn("# YouTube Transcript - dQw4w9WgXcQ", markdown)
        self.assertIn("- Source: https://youtu.be/dQw4w9WgXcQ", markdown)
        self.assertIn("- [00:00:00] Hello there.", markdown)
        self.assertIn("- [00:01:05] This is TubeAIR.", markdown)

    def test_build_markdown_appends_ai_section(self):
        enrichment = AiEnrichment(
            executive_summary="This is a concise executive summary.",
            key_takeaways=["One", "Two", "Three", "Four", "Five"],
            action_items=["Do the next thing."],
            entities=["TubeAIR"],
            tags=["research assistant", "youtube"],
            tldr="TubeAIR turns transcripts into research notes.",
        )

        markdown = build_markdown("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ", [], enrichment=enrichment)

        self.assertIn("## AI Research Assistant", markdown)
        self.assertIn("TubeAIR turns transcripts into research notes.", markdown)
        self.assertIn("- Do the next thing.", markdown)
        self.assertIn("#research-assistant #youtube", markdown)

    def test_save_markdown_writes_to_out_dir(self):
        output_path = save_markdown(
            "https://youtu.be/dQw4w9WgXcQ",
            "dQw4w9WgXcQ",
            [TranscriptLine(start=0.0, duration=1.0, text="Saved.")],
            Path("tmp-test-out") / "out" / "youtube",
        )

        try:
            self.assertEqual(output_path, Path("tmp-test-out") / "out" / "youtube" / "dQw4w9WgXcQ.md")
            self.assertIn("- [00:00:00] Saved.", output_path.read_text(encoding="utf-8"))
        finally:
            if output_path.exists():
                output_path.unlink()
            youtube_dir = Path("tmp-test-out") / "out" / "youtube"
            out_dir = Path("tmp-test-out") / "out"
            root_dir = Path("tmp-test-out")
            if youtube_dir.exists():
                youtube_dir.rmdir()
            if out_dir.exists():
                out_dir.rmdir()
            if root_dir.exists():
                root_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
