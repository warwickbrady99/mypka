import unittest

from tubeair.clipboard_capture import capture_from_clipboard_text, parse_clipboard_transcript
from tubeair.models import CaptureMode, TranscriptSource


class TestClipboardCapture(unittest.TestCase):
    def test_parses_timestamped_clipboard_lines(self):
        lines = parse_clipboard_transcript("00:01 First line\n01:02:03 Later line")

        self.assertEqual(lines[0].start, 1.0)
        self.assertEqual(lines[0].text, "First line")
        self.assertEqual(lines[1].start, 3723.0)

    def test_plain_clipboard_lines_are_accepted(self):
        lines = parse_clipboard_transcript("First line\nSecond line")

        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0].start, 0.0)

    def test_capture_marks_clipboard_source(self):
        capture = capture_from_clipboard_text(
            "https://youtu.be/dQw4w9WgXcQ",
            "dQw4w9WgXcQ",
            "00:01 Manual line",
            language="English",
            language_code="en",
        )

        self.assertEqual(capture.capture_mode, CaptureMode.CLIPBOARD)
        self.assertEqual(capture.transcript_source, TranscriptSource.CLIPBOARD_MANUAL_IMPORT)
        self.assertTrue(capture.timestamps_present)


if __name__ == "__main__":
    unittest.main()
