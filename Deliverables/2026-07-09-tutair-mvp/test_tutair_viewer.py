import shutil
import tempfile
import unittest
from datetime import date
from pathlib import Path

from tutair_intake import TutairCapture, save_capture, save_source_content, with_source_content_fields
from tutair_process import process_capture
from tutair_viewer import find_processed_notes, parse_processed_note, render_home


class TestTutairViewer(unittest.TestCase):
    def test_find_processed_notes_reads_processed_folder(self):
        temp_dir = Path(tempfile.mkdtemp(prefix="tutair-viewer-"))
        try:
            capture_path = make_processed_note(temp_dir)
            notes = find_processed_notes(temp_dir)

            self.assertEqual(len(notes), 1)
            self.assertEqual(notes[0].subject, "Science")
            self.assertEqual(notes[0].topic, "Cell division")
            self.assertIn("Tiny Summary", notes[0].sections)
            self.assertIn("processed", str(capture_path.parent))
        finally:
            shutil.rmtree(temp_dir)

    def test_parse_processed_note_extracts_sections(self):
        temp_dir = Path(tempfile.mkdtemp(prefix="tutair-viewer-"))
        try:
            processed_path = make_processed_note(temp_dir)
            note = parse_processed_note(processed_path, temp_dir)

            self.assertEqual(note.exam_board_status, "unconfirmed")
            self.assertIn("Mitosis makes new body cells.", note.sections["Tiny Summary"])
            self.assertIn("What This Means", note.sections)
        finally:
            shutil.rmtree(temp_dir)

    def test_render_home_has_empty_state(self):
        html = render_home([])

        self.assertIn("No processed notes yet", html)
        self.assertIn("Team Inbox/TutAIR/YYYY/MM/processed/", html)

    def test_render_home_lists_note_subject_and_topic(self):
        temp_dir = Path(tempfile.mkdtemp(prefix="tutair-viewer-"))
        try:
            make_processed_note(temp_dir)
            html = render_home(find_processed_notes(temp_dir))

            self.assertIn("Science", html)
            self.assertIn("Cell division", html)
            self.assertIn("Exam-Style Questions", html)
            self.assertIn("Flashcards", html)
        finally:
            shutil.rmtree(temp_dir)


def make_processed_note(root: Path) -> Path:
    capture = TutairCapture(
        source_type="pasted_text",
        subject="Science",
        topic="Cell division",
        source_url="",
        learning_content=(
            "Mitosis makes new body cells. "
            "The parent cell divides to make two identical daughter cells. "
            "This helps organisms grow and repair tissue."
        ),
        captured_on=date(2026, 7, 9),
    )
    source_path = save_source_content(capture, root)
    capture_path = save_capture(with_source_content_fields(capture, source_path), root)
    return process_capture(capture_path)


if __name__ == "__main__":
    unittest.main()
