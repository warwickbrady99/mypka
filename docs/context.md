# Project Context

## What This Project Is

This folder is a myPKA workspace: an Obsidian-compatible markdown knowledge system built around the ICOR methodology and a 12-specialist AI team. In this workspace, Larry is the default orchestrator identity. Larry routes work to specialists such as Penn for journal capture, Pax for research, Silas for structure and imports, and others as needed.

The immediate personal project is to use myPKA to help a 15-year-old student learn AI/ICOR during work experience week and build a practical GCSE revision, tutoring, and study framework.

Current subjects:

- Maths
- English
- Science
- Computer Science
- Business Enterprise
- Construction
- History

The student attends Neston High School. Exam-board details have not yet been confirmed, so future work should avoid assuming boards or specifications until the student, parent, teacher, timetable, or school document confirms them.

## Overall Architecture

The workspace is plain markdown. The folder itself is the source of truth.

- `AGENTS.md` is the root operating contract. It defines Larry, specialist routing, session logging, import triggers, expansion triggers, frontmatter rules, and wiki rules.
- `Team/` contains specialist contracts. Each specialist has an `AGENTS.md`.
- `Team Knowledge/` contains the team's operating system: SOPs, Workstreams, Guidelines, task tracking, templates, and session logs.
- `PKM/` contains the user's personal knowledge. It is split into Journal, My Life, CRM, Documents, and Images.
- `Deliverables/` is the working area for research briefs, project outputs, and multi-file artifacts.
- `Team Inbox/` is the drop zone for raw inputs such as screenshots, notes, links, and voice memos.
- `Expansions/` contains bundled expansion packs and the local myPKA Cockpit.
- `docs/` contains lightweight handoff documentation for future Codex chats.

## Main Folders

- `PKM/Journal/` - daily capture. New information usually lands here first.
- `PKM/My Life/Key Elements/` - stable life areas, such as education, health, relationships, or career.
- `PKM/My Life/Goals/` - active outcomes. Each Goal anchors to one Key Element and is carried by one Project or Habit.
- `PKM/My Life/Projects/` - bounded efforts with a finish line, such as preparing for a mock exam.
- `PKM/My Life/Habits/` - repeatable routines, such as daily revision.
- `PKM/My Life/Topics/` - subject or interest areas, such as GCSE Maths or Computer Science.
- `PKM/CRM/` - people and organizations.
- `PKM/Documents/` - document stubs and important records.
- `Team Knowledge/tasks/` - cross-session task continuity.
- `Team Knowledge/session-logs/` - formal session logs written at session close.
- `docs/session-log.md` - lightweight human-readable chat handoff log.

## Key Design Decisions

- Keep canonical knowledge in markdown files, not in a database.
- Use `[[wikilinks]]` for cross-references.
- Avoid duplicated facts. Put each fact in one source-of-truth file and link to it elsewhere.
- Use YAML frontmatter templates for entity notes in the eight controlled PKM entity folders.
- Do not guess exam boards. Verify before building subject-specific revision resources.
- Use the Journal as the easiest first capture point for school notes, worries, revision progress, and questions.
- Keep this documentation layer lightweight so future Codex chats can get oriented quickly.

## Current Progress

- The user has explained that they are 15, on work experience week, and learning AI/ICOR with help from their dad.
- Larry recommended starting with a school/exam-focused setup rather than trying to learn all of ICOR abstractly.
- The student listed their current subjects.
- The student and parent want to collect exam schemes/specifications and revision guides from the relevant exam boards to create a personalised study framework and learning resources.
- Publicly available information was not enough to safely confirm exam boards for the student's exact courses.
- This lightweight context system was added so future Codex chats can continue quickly.
- TutAIR MVP now exists as a Markdown-first GCSE learning intake and processing lane in `Deliverables/2026-07-09-tutair-mvp/`, with captures landing under `Team Inbox/TutAIR/YYYY/MM/` and processed notes under `Team Inbox/TutAIR/YYYY/MM/processed/`.
- TutAIR V1 captures either a YouTube URL or UTF-8 pasted text file. YouTube V1 records URL/video ID only; transcript fetching is intentionally not built yet.
- TutAIR V2 processes one capture Markdown file into an ADHD-friendly learning note with tiny summary, key facts, what this means, exam-style questions, flashcards, next revision task, and exam-board mapping status.

## Active Build: F247 AsdAIr Microsite

- The FastAPI MVP lives at `Deliverables/2026-07-08-f247-asdair-microsite/`.
- The FastAPI MVP includes the Mum shopping page, Warwick admin dashboard, SQLite persistence, Markdown/JSON/Claude Chrome handoff exports, optional email notification support, tests, manual QA notes, phone shortcut notes, and VPS deployment documentation.
- On 2026-07-08, the hosting direction changed: V1 should move the public Mum-facing surface to a Vercel-hosted Next.js app, while keeping Warwick processing and Local Brain / `inbox-asdair` local.
- The Next.js V1 sibling app lives at `Deliverables/2026-07-08-f247-asdair-microsite-nextjs/`.
- The Next.js app currently ports only the Mum-facing shopping page: private token route, static catalogue, grouped items, quantity controls, `Use usual shop`, notes field, and local confirmation preview.
- The Next.js app intentionally has no database, no admin dashboard, no cloud file exports, and no Asda login, payment, API, checkout, or order placement.
- The next implementation step is structured email submission from the Next.js app so Dad/Warwick receives the request by email.

## Outstanding Tasks

- For TutAIR V3, add a better source-content path for YouTube captures, either by reusing TubeAIR transcript capture safely or by supporting pasted transcripts more directly.
- For TutAIR V3, decide where durable processed GCSE resources should live after inbox processing: remain in `Team Inbox/TutAIR/.../processed/`, move to `PKM/Documents/`, or create a dedicated GCSE resource area.
- For TutAIR V3, add batch processing for pending TutAIR captures once the single-file workflow feels right.
- For TutAIR V3, improve the deterministic processor so URL-only captures do not produce weak learning notes without actual transcript or pasted content.
- Add structured email submission to the Next.js AsdAIr app.
- Decide which email provider to use for Vercel deployment, such as Resend, Postmark, SendGrid, or SMTP-compatible service.
- Replace the Next.js local confirmation preview with a real submit/sent/error flow after email is wired.
- Run browser QA for the Next.js Mum page locally and then on Vercel.
- Later, decide whether to add webhook or local inbox automation from the email/request into Local Brain / `inbox-asdair`.
- Confirm the exam board and qualification for each subject.
- Confirm tier where relevant, especially Maths and Science.
- Confirm current year group and upcoming mock/exam dates.
- Create PKM topic notes for each subject once the subject structure is confirmed.
- Create goals and projects for revision once the student has target outcomes or exam dates.
- Gather official specifications, assessment objectives, past-paper links, and revision-guide references for each confirmed board.
- Build a personalised revision framework: topic checklist, weak-area tracker, weekly plan, practice-question rota, and tutoring prompts.
- Decide whether TutAIR should become the dedicated `Deliverables/` folder for the GCSE study framework or remain a capture/processing subproject.

## Important Conventions And Rules

- Start new Codex chats by reading `AGENTS.md`, this file, `docs/session-log.md`, and `Team/agent-index.md`.
- Larry leads every response and delegates specialist work when needed.
- Use `[[wikilinks]]` inside the myPKA wiki.
- When creating entity notes under PKM, use the relevant template from `Team Knowledge/Templates/` and follow `Team Knowledge/Guidelines/GL-002-frontmatter-conventions.md`.
- Session-close requests such as "wrap up" or "close session" should create a formal session log under `Team Knowledge/session-logs/YYYY/MM/`.
- The lightweight `docs/session-log.md` can be updated during ordinary handoffs without replacing the formal myPKA session-log system.
- Keep school-related advice practical and age-appropriate. The system should help the student learn, revise, and understand, not bypass their own work.

## Helpful Future Docs To Add

- `docs/exam-board-map.md` - confirmed subject, exam board, qualification, tier, teacher, and source link.
- `docs/revision-framework.md` - the student's personalised revision system once exam boards are known.
- `docs/codex-startup-prompt.md` - a reusable one-page startup prompt for new chats.
- `docs/parent-guide.md` - simple explanation for the parent: how to support the student without overcomplicating the system.
