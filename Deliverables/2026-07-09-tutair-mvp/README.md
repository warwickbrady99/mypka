# TutAIR MVP

TutAIR is a small GCSE revision helper for myPKA.

It starts simple:

```text
YouTube link or pasted learning text -> raw source content -> TutAIR capture -> ADHD-friendly revision note
```

This MVP does not build the web dashboard yet. It gives TutAIR a safe local intake and processing path.

Milestone 2 adds the source-content foundation: raw source text is stored separately, capture Markdown records metadata and readiness, and processed resources are generated only when source content is ready.

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
- `course-map/` - Milestone 1 GCSE course-map MVP, kept separate from learning resources.

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

For YouTube URLs, TutAIR records the URL and video ID, then marks the capture as `needs_source_content`. For useful processed notes today, paste transcript or lesson text through `--text-file`.

When you use `--text-file`, TutAIR also saves the raw source text under:

```text
Team Inbox/TutAIR/YYYY/MM/source-content/
```

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

URL-only captures are blocked from processing until transcript, lesson text, or another raw source-content file is attached. This prevents TutAIR from turning a bare URL into a weak learning resource.

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

The viewer UI follows the approved TutAIR revision dashboard mockup: dark subject navigation, topic cards, colourful revision sections, study controls, and responsive panels. The backend and Markdown reading path are unchanged.

Interactive controls now work locally in the browser:

- `Flashcards` opens a practice view using the current note's flashcards, with Previous, Next, and Flip Card controls.
- `Quiz Me` turns the current note's exam-style questions into a simple answer-and-reveal quiz.
- `Notes` returns to the full revision note.
- `Read Aloud` uses the browser's built-in SpeechSynthesis API and includes Play, Pause, and Stop controls.
- `Focus Mode` hides side panels and distractions until you switch back.
- `Mark as Reviewed` stores reviewed status in browser `localStorage`.
- `Save Topic` stores favourites in browser `localStorage` and shows a Favourites section in the sidebar.
- Controls that are not ready yet show `Coming Soon`.

All of this stays local to the browser. It does not publish anything online, call an AI service, or change the Markdown files.

## Checks

Run the focused tests from this folder:

```powershell
python -m unittest test_tutair_intake.py test_tutair_process.py test_tutair_viewer.py
```

Run the course-map MVP checks from `course-map/`:

```powershell
python -m unittest test_course_map.py
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

## Milestone 1 Course Map

The course map is TutAIR's curriculum spine. It lives separately from captures and learning resources in:

```text
Deliverables/2026-07-09-tutair-mvp/course-map/
```

The first MVP slice maps a small official-specification-backed AQA GCSE Combined Science: Trilogy Biology Paper 1 / Cell biology branch. Future captures should link to one or more stable learning objective IDs instead of copying the course-map hierarchy.

## Source Content Pipeline

TutAIR now uses three distinct layers:

```text
Raw source content -> TutAIR capture metadata -> Processed learning resource
```

### Raw source

Raw source is the actual transcript, lesson text, textbook extract, or copied note. It is evidence. For pasted text intake, it is stored as a `.txt` file in `Team Inbox/TutAIR/YYYY/MM/source-content/`.

TubeAIR already captures YouTube transcripts into `Team Inbox/TubeAIR/YYYY/MM/`. TutAIR should reuse that capability by linking or importing the resulting transcript text into the TutAIR source-content layer, rather than rebuilding the TubeAIR Telegram/transcript listener.

### Extracted content

The TutAIR capture Markdown is the extracted/handoff record. It stores subject, topic, source URL, source-content status, processing readiness, and future course-map links. It should stay light and point back to the raw source.

### Processed learning resources

Processed resources live under `Team Inbox/TutAIR/YYYY/MM/processed/` for the MVP. They are student-facing revision notes generated from ready source content. They should later link to stable course-map learning objective IDs.
