# TutAIR MVP

TutAIR is a small GCSE revision helper for myPKA.

It starts simple:

```text
YouTube link or pasted learning text -> TutAIR inbox -> ADHD-friendly revision note
```

This MVP does not build the web dashboard yet. It gives TutAIR a safe local intake and processing path.

## Files In This Folder

- `capture-note-template.md` - use this when saving a new learning source.
- `processed-learning-note-template.md` - use this when turning a source into a revision resource.
- `beginner-instructions.md` - plain-English steps for using TutAIR.
- `tutair_intake.py` - small V1 command that creates a TutAIR capture note.
- `test_tutair_intake.py` - checks for the V1 intake command.
- `tutair_process.py` - small V2 command that creates an ADHD-friendly processed learning note from one capture.
- `test_tutair_process.py` - checks for the V2 processor.
- `tutair_viewer.py` - small V3 local web viewer for processed TutAIR notes.
- `test_tutair_viewer.py` - checks for the V3 viewer.

## V1 Intake Command

From this folder, capture a YouTube educational URL:

```powershell
python .\tutair_intake.py --url "https://www.youtube.com/watch?v=abcdefghijk" --subject "Science" --topic "Cell division"
```

Or capture pasted learning text from a UTF-8 `.txt` file:

```powershell
python .\tutair_intake.py --text-file ".\my-learning-text.txt" --subject "History" --topic "Cold War"
```

The command saves Markdown under:

```text
Team Inbox/TutAIR/YYYY/MM/
```

For YouTube URLs, V1 records the URL and video ID. It does not fetch a transcript yet. For useful processed notes today, paste transcript or lesson text through `--text-file`.

## V2 Processor Command

Turn one TutAIR capture into an ADHD-friendly learning note:

```powershell
python .\tutair_process.py "C:\Users\Buggly\OneDrive\Desktop\MyPKA\Team Inbox\TutAIR\2026\07\2026-07-09-gcse-science-cell-division.md"
```

By default, the processed note is saved beside the capture in:

```text
Team Inbox/TutAIR/YYYY/MM/processed/
```

The processor fills:

- Tiny Summary
- Key Facts
- What This Means
- Exam-Style Questions
- Flashcards
- Next Revision Task
- Exam Board Mapping

It keeps exam-board mapping unconfirmed unless the capture has both `exam_board_status: confirmed` and real evidence in `exam_board_evidence`.

Exam-board mapping is unconfirmed by default. You can record a possible board, but that still stays unconfirmed:

```powershell
python .\tutair_intake.py --url "https://www.youtube.com/watch?v=abcdefghijk" --subject "Science" --topic "Cell division" --possible-exam-board "AQA"
```

## V3 Local Web Viewer

Run the read-only revision viewer from this folder:

```powershell
python .\tutair_viewer.py
```

Then open:

```text
http://127.0.0.1:8765
```

The viewer reads processed notes from:

```text
Team Inbox/TutAIR/YYYY/MM/processed/
```

It shows the processed TutAIR sections in a revision-friendly page:

- Tiny Summary
- Key Facts
- What This Means
- Exam-Style Questions
- Flashcards
- Next Revision Task
- Exam Board Mapping

The viewer is local and read-only. It does not edit notes, publish anything online, or change TubeAIR.

## Checks

Run the focused tests from this folder:

```powershell
python -m unittest test_tutair_intake.py test_tutair_process.py test_tutair_viewer.py
```

## Important Rule

TutAIR can write a possible exam board, but it must not treat that as fact unless there is evidence.

Good:

```yaml
possible_exam_board: AQA
exam_board_status: unconfirmed
exam_board_evidence: none
```

Only mark something as confirmed when it comes from a reliable source such as a teacher, official specification, school document, exam timetable, or confirmed course source.
