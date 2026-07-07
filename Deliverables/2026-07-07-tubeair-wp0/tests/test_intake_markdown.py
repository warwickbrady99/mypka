import unittest
from datetime import datetime, timezone
from pathlib import Path
import shutil

from tubeair.intake import dated_intake_dir
from tubeair.markdown import build_intake_frontmatter, save_capture_markdown
from tubeair.models import CaptureMode, TranscriptCapture, TranscriptLine, TranscriptSource, TranscriptTrack


class TestIntakeMarkdown(unittest.TestCase):
    def test_dated_intake_dir_uses_year_month(self):
        path = dated_intake_dir(Path("Team Inbox") / "TubeAIR", datetime(2026, 7, 7))

        self.assertEqual(path, Path("Team Inbox") / "TubeAIR" / "2026" / "07")

    def test_frontmatter_contains_handoff_contract(self):
        capture = build_capture()

        frontmatter = build_intake_frontmatter(capture, datetime(2026, 7, 7, tzinfo=timezone.utc))

        self.assertIn("type: tubeair_youtube_transcript", frontmatter)
        self.assertIn('source_url: "https://youtu.be/dQw4w9WgXcQ"', frontmatter)
        self.assertIn("capture_mode: api", frontmatter)
        self.assertIn("handoff_status: captured_pending_categorisation", frontmatter)
        self.assertIn("categorisair_status: pending", frontmatter)

    def test_save_capture_markdown_writes_frontmatter_and_transcript(self):
        out_dir = Path("tmp-test-intake") / "Team Inbox" / "TubeAIR" / "2026" / "07"
        try:
            output_path = save_capture_markdown(build_capture(), out_dir)
            text = output_path.read_text(encoding="utf-8")

            self.assertTrue(output_path.exists())
            self.assertIn("---", text)
            self.assertIn("- [00:00:00] Intake works.", text)
        finally:
            if Path("tmp-test-intake").exists():
                shutil.rmtree("tmp-test-intake")


def build_capture():
    return TranscriptCapture(
        video_url="https://youtu.be/dQw4w9WgXcQ",
        video_id="dQw4w9WgXcQ",
        lines=[TranscriptLine(start=0.0, duration=1.0, text="Intake works.")],
        track=TranscriptTrack(language="English", language_code="en", is_generated=False),
        capture_mode=CaptureMode.API,
        transcript_source=TranscriptSource.YOUTUBE_CAPTIONS,
    )


if __name__ == "__main__":
    unittest.main()
