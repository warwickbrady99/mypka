# WS-005 - Process TutAIR Captures Into GCSE Learning Resources

- **Status:** Draft active
- **Type:** Workstream
- **Owners:** **Mack** owns intake mechanics. **Silas** owns source-note shape and myPKA structure. **Pax** owns specification verification when official sources are needed. **Felix** owns the later dashboard. **Larry** orchestrates and enforces SSOT.
- **References:** [[GL-001-file-naming-conventions]], [[GL-002-frontmatter-conventions]], [[WS-004-process-tubeair-captures]], [[exam-board-map]], [[revision-framework]]

## Purpose

TutAIR turns GCSE learning material into clear, small, reviewable resources.

The goal is:

```text
YouTube URL or pasted text -> raw TutAIR capture -> ADHD-friendly learning note -> linked GCSE revision resource -> later web dashboard
```

TutAIR is like TubeAIR in spirit, but its job is GCSE learning rather than general YouTube knowledge capture.

## Non-Negotiable Rule

TutAIR must not guess exam-board mapping as fact.

It may record a possible exam board when the source or context suggests one, but it must clearly label it as unconfirmed unless there is evidence from an official specification, teacher, school document, exam timetable, or confirmed course source.

## Roles

- **Mack** gets the source into the right inbox path.
- **Silas** keeps the markdown structure clean and prepares processed learning notes.
- **Pax** verifies exam-board specifications and official links when needed.
- **Penn** may add school reflections or revision progress to the Journal when the capture changes the user's study plan.
- **Felix** builds the later web dashboard when the markdown layer is ready.
- **Larry** routes the work and checks that facts live in the right source-of-truth file.

## Inputs

TutAIR accepts:

- a YouTube educational URL
- pasted learning text
- copied transcript text
- textbook or revision-guide extracts
- lesson notes

Raw capture notes use:

```yaml
type: tutair_learning_capture
handoff_status: captured_pending_processing
```

## Output Layers

### Layer 1 - Raw Capture

Location:

```text
Team Inbox/TutAIR/YYYY/MM/
```

Rules:

- Keep the source text available.
- Preserve the source URL when there is one.
- Record subject, topic, possible exam board, capture date, and confidence level.
- Mark exam-board status as `unconfirmed` unless evidence is known.

### Layer 2 - ADHD-Friendly Learning Note

Location for MVP processed notes:

```text
Team Inbox/TutAIR/YYYY/MM/processed/
```

The template and tools live in `Deliverables/2026-07-09-tutair-mvp/`. Later, processed notes may move into `PKM/Documents/` or a dedicated GCSE resource area once the team confirms the best long-term structure.

Body sections:

- `## Tiny Summary`
- `## Key Facts`
- `## What This Means`
- `## Exam-Style Questions`
- `## Flashcards`
- `## Next Revision Task`
- `## Exam Board Mapping`

### Layer 3 - GCSE Mapping

Mapping to exam boards and specifications is evidence-led.

Use [[exam-board-map]] as the source of truth for confirmed subject, board, qualification, tier, and source details. If a source is not confirmed, write `unconfirmed` and name what evidence is missing.

### Layer 4 - Web Dashboard

The dashboard is not part of this MVP.

When built later, it should browse resources by:

- subject
- topic
- exam board
- confirmation status
- confidence level
- next revision task

Markdown remains canonical. A database or dashboard index may be generated later, but it is not the source of truth.

## MVP Processing Procedure

1. **Capture the source.**
   Save the YouTube URL or pasted text into `Team Inbox/TutAIR/YYYY/MM/`.

2. **Add metadata.**
   Include subject, topic, possible exam board, source URL, captured date, confidence level, and exam-board confirmation status.

3. **Create the learning note.**
   Run `tutair_process.py` on one capture, or use the processed learning note template manually. Save the result under `Team Inbox/TutAIR/YYYY/MM/processed/`.

4. **Separate facts from guesses.**
   Facts from the source can be summarized. Exam-board mapping stays unconfirmed unless evidence is known.

5. **Suggest the next revision task.**
   End with one small task that can be completed in 5 to 15 minutes.

6. **Defer dashboard work.**
   Do not build web UI until the capture and note shapes are useful.

## Current Implementation

The MVP implementation lives in `Deliverables/2026-07-09-tutair-mvp/`.

- `tutair_intake.py` creates capture Markdown from a YouTube URL or UTF-8 text file.
- `tutair_process.py` creates one ADHD-friendly processed note from one capture Markdown file.
- YouTube intake currently records the URL and video ID only. Transcript fetching is intentionally out of scope for this MVP.
- Processing is deterministic and Markdown-first. It does not call an AI model.

## Definition Of Done For MVP

- TutAIR inbox README exists.
- TutAIR processing workstream exists.
- Capture note template exists.
- Processed learning note template exists.
- Beginner instructions exist.
- V1 intake command exists.
- V2 processor command exists.
- Focused tests exist for intake and processing.
- No TubeAIR behavior has changed.
- No web dashboard has been built.
- Exam-board claims are clearly marked as confirmed or unconfirmed.
