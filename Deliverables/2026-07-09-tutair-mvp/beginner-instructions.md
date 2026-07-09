# TutAIR Beginner Instructions

TutAIR helps turn learning content into GCSE revision notes.

Use it when you find a useful educational YouTube video, copied transcript, textbook extract, lesson note, or pasted explanation.

## Step 1 - Save The Source

Create a new note under:

```text
Team Inbox/TutAIR/YYYY/MM/
```

Use `capture-note-template.md` as the shape.

You can also use the V1 command:

```powershell
python .\tutair_intake.py --text-file ".\my-learning-text.txt" --subject "Science" --topic "Cell division"
```

For YouTube, the current command records the URL. It does not fetch the transcript yet:

```powershell
python .\tutair_intake.py --url "https://www.youtube.com/watch?v=abcdefghijk" --subject "Science" --topic "Cell division"
```

Name it with the date and a short topic slug, for example:

```text
2026-07-09-gcse-biology-cell-division.md
```

## Step 2 - Fill In The Basics

Add what you know:

- subject
- topic
- source URL, if there is one
- date captured
- confidence level
- pasted source text or transcript

If you are not sure about the exam board, write:

```yaml
possible_exam_board: unknown
exam_board_status: unconfirmed
exam_board_evidence: none
```

## Step 3 - Make A Learning Note

Use `processed-learning-note-template.md`, or run the V2 processor on one capture:

```powershell
python .\tutair_process.py "C:\Users\Buggly\OneDrive\Desktop\MyPKA\Team Inbox\TutAIR\2026\07\your-capture.md"
```

The processed note is saved in:

```text
Team Inbox/TutAIR/YYYY/MM/processed/
```

Keep it small:

- tiny summary
- key facts
- what this means
- exam-style questions
- flashcards
- next revision task

## Step 4 - Be Careful With Exam Boards

Do not guess.

It is fine to write:

```text
This might be AQA, but it is not confirmed yet.
```

It is not fine to write:

```text
This is definitely AQA.
```

unless there is evidence from a teacher, official specification, school document, exam timetable, or confirmed course source.

## Step 5 - Pick The Next Tiny Task

End every learning note with one small task, such as:

- answer 3 flashcards
- explain the topic in 3 sentences
- do 5 practice questions
- watch the next 5 minutes of the video
- check the exam-board specification

The goal is to make revision easier to start.

## Current Limits

- TutAIR is Markdown-first.
- TutAIR does not build the web dashboard yet.
- TutAIR does not change TubeAIR.
- TutAIR does not fetch YouTube transcripts yet.
- TutAIR does not confirm exam boards without evidence.
