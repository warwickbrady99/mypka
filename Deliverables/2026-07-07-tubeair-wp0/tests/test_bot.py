import unittest
from pathlib import Path
import shutil
from unittest.mock import patch

from tubeair.bot import find_youtube_url, is_long_plain_text, process_message
from tubeair.models import AiEnrichment, TextSummaryResult, TranscriptLine
from tubeair.telegram_bot import main as telegram_main


class TestBotMessageProcessing(unittest.TestCase):
    def test_find_youtube_url(self):
        self.assertEqual(
            find_youtube_url("watch this https://www.youtube.com/watch?v=dQw4w9WgXcQ please"),
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )

    def test_process_message_short_text_gives_help_message(self):
        result = process_message("hello", out_dir=Path("tmp-test-bot") / "out" / "youtube")

        self.assertFalse(result.ok)
        self.assertIn("Send me either:", result.reply)

    def test_youtube_link_still_routes_to_youtube_processor(self):
        with patch("tubeair.bot.process_youtube_url") as process_youtube:
            process_youtube.return_value.output_path = "out/youtube/abc123.md"
            process_youtube.return_value.enrichment = None
            process_youtube.return_value.enrichment_error = None

            result = process_message("notes https://youtu.be/abc123", enrich=False)

        self.assertTrue(result.ok)
        self.assertIn("Saved transcript:", result.reply)
        process_youtube.assert_called_once()

    def test_long_text_routes_to_text_summariser(self):
        long_text = " ".join(["research"] * 120)
        summary = AiEnrichment(
            executive_summary="Summary.",
            key_takeaways=["Point"],
            action_items=["Act"],
            entities=["OpenAI"],
            tags=["research"],
            tldr="Short version.",
        )

        with patch("tubeair.bot.process_plain_text") as process_text:
            process_text.return_value = TextSummaryResult(output_path="out/text/sample.md", summary=summary)

            result = process_message(long_text, enrich=True)

        self.assertTrue(result.ok)
        self.assertIn("Short version.", result.reply)
        self.assertIn("Saved text summary:", result.reply)
        process_text.assert_called_once()

    def test_is_long_plain_text_uses_word_count(self):
        self.assertTrue(is_long_plain_text(" ".join(["word"] * 100)))
        self.assertFalse(is_long_plain_text("short note"))

    def test_process_message_saves_markdown_and_returns_reply(self):
        out_dir = Path("tmp-test-bot") / "out" / "youtube"
        with patch(
            "tubeair.processor.fetch_transcript",
            return_value=[TranscriptLine(start=0.0, duration=1.0, text="Bot works.")],
        ):
            try:
                result = process_message(
                    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    out_dir=out_dir,
                    enrich=False,
                )

                output_path = out_dir / "dQw4w9WgXcQ.md"
                self.assertTrue(result.ok)
                self.assertEqual(result.output_path, output_path)
                self.assertIn("Saved transcript:", result.reply)
                self.assertTrue(output_path.exists())
                self.assertIn("- [00:00:00] Bot works.", output_path.read_text(encoding="utf-8"))
            finally:
                output_path = out_dir / "dQw4w9WgXcQ.md"
                if output_path.exists():
                    output_path.unlink()
                if out_dir.exists():
                    out_dir.rmdir()
                parent = Path("tmp-test-bot") / "out"
                if parent.exists():
                    parent.rmdir()
                root = Path("tmp-test-bot")
                if root.exists():
                    shutil.rmtree(root)

    def test_telegram_entrypoint_requires_token(self):
        with patch.dict("os.environ", {}, clear=True):
            self.assertEqual(telegram_main([]), 1)


if __name__ == "__main__":
    unittest.main()
