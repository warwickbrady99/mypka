import unittest
from pathlib import Path
from unittest.mock import patch

from tubeair.cli import main
from tubeair.models import TranscriptLine


class TestCli(unittest.TestCase):
    def test_cli_imports_and_saves_markdown(self):
        with patch(
            "tubeair.processor.fetch_transcript",
            return_value=[TranscriptLine(start=0.0, duration=1.0, text="CLI works.")],
        ):
            output_dir = Path("tmp-test-cli") / "out" / "youtube"
            try:
                exit_code = main(
                    [
                        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                        "--out-dir",
                        str(output_dir),
                        "--no-ai",
                    ]
                )

                self.assertEqual(exit_code, 0)
                output_path = output_dir / "dQw4w9WgXcQ.md"
                self.assertTrue(output_path.exists())
                self.assertIn("- [00:00:00] CLI works.", output_path.read_text(encoding="utf-8"))
            finally:
                output_path = output_dir / "dQw4w9WgXcQ.md"
                if output_path.exists():
                    output_path.unlink()
                if output_dir.exists():
                    output_dir.rmdir()
                out_dir = Path("tmp-test-cli") / "out"
                if out_dir.exists():
                    out_dir.rmdir()
                root_dir = Path("tmp-test-cli")
                if root_dir.exists():
                    root_dir.rmdir()


if __name__ == "__main__":
    unittest.main()
