# WS-005 - Process TutAIR Captures Into GCSE Learning Resources

- **Status:** Draft active
- **Type:** Workstream
- **Owners:** **Mack** owns intake mechanics. **Silas** owns source-note shape and myPKA structure. **Pax** owns specification verification when official sources are needed. **Felix** owns the later dashboard. **Larry** orchestrates and enforces SSOT.
- **References:** [[GL-001-file-naming-conventions]], [[GL-002-frontmatter-conventions]], [[WS-004-process-tubeair-captures]], [[exam-board-map]], [[revision-framework]]

## Purpose

TutAIR turns GCSE learning material into clear, small, reviewable resources.

The goal is:

```text
YouTube URL or pasted text -> raw source content -> TutAIR capture metadata -> ADHD-friendly learning note -> linked GCSE revision resource -> later web dashboard
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
source_content_status: ready
processing_readiness: ready_for_processing
```

## Output Layers

### Layer 1 - Raw Source

Location:

```text
Team Inbox/TutAIR/YYYY/MM/source-content/
```

Rules:

- Keep the actual transcript, lesson text, textbook extract, or copied note available.
- Do not overwrite raw source text when processed resources change.
- Preserve source URL in the capture metadata when there is one.
- Reuse TubeAIR's YouTube transcript capture path when possible. TubeAIR lands YouTube transcripts under `Team Inbox/TubeAIR/YYYY/MM/`; TutAIR should link or import that transcript text into the TutAIR source-content layer instead of duplicating the Telegram/transcript listener.

### Layer 2 - Capture Metadata

Location:

```text
Team Inbox/TutAIR/YYYY/MM/
```

Rules:

- Store handoff metadata, not the only copy of the source.
- Preserve the source URL when there is one.
- Record subject, topic, possible exam board, capture date, and confidence level.
- Record `source_content_status`, `source_content_path`, and `processing_readiness`.
- Mark exam-board status as `unconfirmed` unless evidence is known.
- Mark URL-only captures as `needs_source_content` and block processing.

### Layer 3 - ADHD-Friendly Learning Note

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

### Layer 4 - GCSE Mapping

Mapping to exam boards and specifications is evidence-led.

Use [[exam-board-map]] as the source of truth for confirmed subject, board, qualification, tier, and source details. If a source is not confirmed, write `unconfirmed` and name what evidence is missing.

### Layer 5 - Web Dashboard

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

1. **Capture or attach raw source content.**
   Save transcript, lesson text, textbook extract, or copied notes under `Team Inbox/TutAIR/YYYY/MM/source-content/` when available. For a YouTube URL, use TubeAIR's transcript capture route when available rather than rebuilding it inside TutAIR.

2. **Add metadata.**
   Create a TutAIR capture under `Team Inbox/TutAIR/YYYY/MM/`. Include subject, topic, possible exam board, source URL, captured date, confidence level, source-content status, source-content path, processing readiness, and exam-board confirmation status.

3. **Check readiness.**
   Process only captures with `source_content_status: ready` and `processing_readiness: ready_for_processing`. Leave URL-only captures blocked as `needs_source_content`.

4. **Create the learning note.**
   Run `tutair_process.py` on one ready capture, or use the processed learning note template manually. Save the result under `Team Inbox/TutAIR/YYYY/MM/processed/`.

5. **Separate facts from guesses.**
   Facts from the source can be summarized. Exam-board mapping stays unconfirmed unless evidence is known.

6. **Suggest the next revision task.**
   End with one small task that can be completed in 5 to 15 minutes.

7. **Defer dashboard work.**
   Do not build web UI until the capture and note shapes are useful.

## Current Implementation

The MVP implementation lives in `Deliverables/2026-07-09-tutair-mvp/`.

- `tutair_intake.py` creates capture Markdown from a YouTube URL or UTF-8 text file.
- Text-file intake now writes raw source text under `Team Inbox/TutAIR/YYYY/MM/source-content/` and links the capture to it.
- URL-only intake now marks captures as `needs_source_content` and blocks processing until content is attached.
- `tutair_process.py` creates one ADHD-friendly processed note from one capture Markdown file.
- `tutair_process.py` reads ready source content from `source_content_path` and refuses URL-only captures.
- YouTube transcript fetching remains owned by TubeAIR for now; TutAIR should consume the resulting transcript content.
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
- URL-only captures are blocked from weak processing.
- Raw source content is stored separately from processed learning resources.
- No TubeAIR behavior has changed.
- No web dashboard has been built.
- Exam-board claims are clearly marked as confirmed or unconfirmed.
