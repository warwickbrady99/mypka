# TutAIR Product Roadmap - 6 to 12 Months

## Plan Status

- **Status:** Approved product plan
- **Approved on:** 2026-07-09
- **Operating rule:** Build one milestone at a time. Do not move to the next milestone until the current one is complete, tested, documented, and committed.

## Scope

TutAIR is currently a local Markdown-first GCSE learning prototype with:

- capture intake from YouTube URL or pasted text
- deterministic processing into ADHD-friendly learning notes
- a local read-only web viewer
- focused tests
- beginner documentation
- Git history

The product vision is to become a polished AI-powered GCSE revision platform, especially for students who benefit from clear, structured, ADHD-friendly learning.

## Strategic Thesis

TutAIR should not start by becoming a generic AI chatbot. Its advantage should be:

1. verified GCSE course mapping
2. small, structured learning units
3. ADHD-friendly revision flow
4. safe AI support that teaches rather than answers for the student
5. parent / student trust through privacy, transparency, and evidence

The next 6 to 12 months should therefore move in this order:

```text
source quality -> curriculum map -> learning engine -> student dashboard -> AI tutor -> accounts/privacy -> pilot -> polished product
```

## Architecture Read

### What Is Strong Now

- Markdown remains canonical, which keeps the system inspectable and easy to version.
- The capture and processed-note split is clean.
- The processor already protects against unverified exam-board claims.
- The viewer proves the product shape without committing too early to a heavy stack.
- Tests exist early, which is a good sign for evolving the system safely.

### What Is Fragile Now

- URL-only YouTube captures do not yet contain enough learning content.
- Processed notes are generated with deterministic sentence picking, not genuine tutoring intelligence.
- Exam-board mapping is still mostly unconfirmed.
- The viewer has no search, progress state, student workflow, authentication, or persistence beyond files.
- There is not yet a durable product data model for subjects, topics, sources, resources, questions, attempts, confidence, and revision history.
- No privacy/safeguarding layer exists yet for a child-facing online product.

### Product Principle

Keep Markdown as the authoring and audit layer for now, but introduce derived indexes and app data only when a feature truly needs them.

## Milestone 1 - Canonical GCSE Course Map

**Window:** Month 1

### Objective

Confirm the student's real subjects, boards, qualification routes, tiers, topic lists, paper structures, and official sources.

### Why It Matters

TutAIR cannot be trusted as a GCSE platform if it guesses the course. For GCSE revision, the board, tier, route, and specification change what content matters and how questions should be framed.

### Expected Outcome

- `docs/exam-board-map.md` becomes genuinely source-backed rather than draft-backed.
- Each subject has status, source, route, tier where relevant, paper structure, and open questions.
- TutAIR can label resources as `confirmed`, `unconfirmed`, or `general GCSE`.

### Dependencies

- Teacher confirmation, exam timetable, candidate statement, school portal, or official specification links.
- Pax verification pass for official sources.
- Silas review of fields needed for course/topic metadata.

### Comes Before

- AI-generated GCSE-specific questions.
- Subject dashboards.
- Spaced revision plans.

### Comes After

- Current local MVP.

## Milestone 2 - Source-Content Pipeline

**Window:** Month 1 to 2

### Objective

Make every capture contain actual learnable source content before processing.

### Why It Matters

A URL is not a lesson. TutAIR needs transcript text, pasted notes, textbook extracts, lesson notes, or verified source snippets before it can produce useful revision resources.

### Expected Outcome

- YouTube captures support pasted transcript text or a safe transcript extraction route.
- URL-only captures are marked `needs_source_content` and are blocked from weak processing.
- Batch processing can handle pending captures once quality gates pass.
- Capture files record source type, source content status, and processing readiness.

### Dependencies

- Mack for transcript/source ingestion mechanics.
- Vex review if using external APIs, cookies, browser automation, or third-party transcript services.
- Existing WS-005 capture/process workflow.

### Comes Before

- AI enrichment.
- Question generation.
- Searchable resource library.

### Comes After

- Canonical course map can run in parallel, but this should complete before scaling content creation.

## Milestone 3 - Durable TutAIR Data Model

**Window:** Month 2

### Objective

Define the long-term shape for TutAIR resources before the app grows around temporary inbox paths.

### Why It Matters

The current MVP stores processed notes under `Team Inbox/TutAIR/.../processed/`, which is right for a prototype but not right for a product knowledge base. The team needs a clean model for source, resource, topic, question, flashcard, attempt, confidence, and revision task.

### Expected Outcome

- Decision on permanent resource location: dedicated TutAIR resource area, PKM document layer, or separate product folder.
- YAML/frontmatter schema for learning resources.
- Derived index format for the viewer.
- Migration path from current processed notes.

### Dependencies

- Silas architecture pass.
- Larry SSOT review.
- Confirm whether TutAIR remains inside myPKA for personal use or becomes a separate product repo.

### Comes Before

- Full dashboard.
- Analytics.
- User accounts.

### Comes After

- Source-content pipeline is defined enough to know what fields matter.

## Milestone 4 - Student Revision Dashboard V1

**Window:** Month 2 to 3

### Objective

Turn the local viewer into a usable study surface: browse, search, filter, revise, and track simple progress.

### Why It Matters

The current viewer displays notes. A product must guide the student toward the next useful action, especially when focus and overwhelm are part of the problem.

### Expected Outcome

- Subject/topic navigation.
- Search and filters by subject, topic, board status, confidence, source type.
- "Study this now" flow.
- Mark-as-reviewed and confidence rating.
- Clear visual hierarchy, low clutter, mobile-friendly layout.
- Local-first persistence for progress.

### Dependencies

- Felix for UI build.
- Iris for design-system direction if the visual language expands.
- Vera for accessibility and responsive QA.
- Durable data model.

### Comes Before

- AI tutor UI.
- Parent view.
- Hosted product.

### Comes After

- Canonical resources and data model.

## Milestone 5 - Learning Engine V1

**Window:** Month 3 to 4

### Objective

Add a proper revision engine: flashcards, exam-style questions, confidence scoring, mistakes, and next-task scheduling.

### Why It Matters

A revision product wins by changing what the student does next. ADHD-friendly learning needs short tasks, visible completion, low-friction review, and an easy way back after losing momentum.

### Expected Outcome

- Structured question and flashcard model.
- Review queue by subject/topic/confidence.
- Mistake log.
- Next revision task generation.
- Simple spaced repetition rules.
- Weekly plan generated from confirmed subjects and weak areas.

### Dependencies

- Dashboard V1 progress controls.
- Course map.
- Data model for attempts/reviews.

### Comes Before

- Personalised AI tutoring.
- Parent/teacher reporting.

### Comes After

- Student dashboard proves the interaction loop.

## Milestone 6 - AI Tutor Guardrails And Prompt System

**Window:** Month 4 to 5

### Objective

Introduce AI support in a controlled way: explanations, quizzes, hints, feedback, and scaffolding without doing the student's work for them.

### Why It Matters

The product vision says AI-powered, but for a GCSE student the AI must be safe, accurate, age-appropriate, and learning-first. The tutor should help the student think, not shortcut thinking.

### Expected Outcome

- Prompt library for explain, quiz, hint, check answer, simplify, and plan revision.
- Grounding rules: use confirmed course map and source content.
- Refusal/redirect rules for cheating, unsafe content, or unsupported claims.
- "Show your working" and "try first" tutoring patterns.
- Human-readable AI transparency notes.

### Dependencies

- Pax for evidence-based tutoring/revision principles.
- Vex for privacy, logging, and child data controls.
- Course/source grounding.
- A decision on AI provider and data handling.

### Comes Before

- Hosted AI product.
- Multi-user accounts.

### Comes After

- Learning engine provides structured context for the AI.

## Milestone 7 - Safety, Privacy, And Child-Ready Product Gate

**Window:** Month 5 to 6

### Objective

Design the product so it is safe for under-18 users before it is hosted or shared beyond local use.

### Why It Matters

TutAIR is likely to be accessed by children. A polished product needs privacy-by-default, data minimisation, transparent controls, and safeguarding thinking before launch.

### Expected Outcome

- Data inventory: what is stored, why, where, and for how long.
- Parent/student consent model.
- Child-friendly privacy explanations.
- No unnecessary profiling or dark patterns.
- AI safety logging without over-collecting personal data.
- Security checklist for any hosted app.

### Dependencies

- Vex security/privacy audit.
- AI provider decision.
- Account model decision.
- Hosting model decision.

### Comes Before

- Online hosted beta.
- Any real student accounts beyond the original household.

### Comes After

- AI tutor design is clear enough to audit.

## Milestone 8 - Product Repo And Hosted Beta Architecture

**Window:** Month 6 to 8

### Objective

Move from local scripts/viewer to a maintainable product architecture with development, staging, deployment, and a clean data boundary.

### Why It Matters

The local prototype proves the idea. A polished product needs reliable setup, deployment, backups, environment secrets, auth, observability, and repeatable releases.

### Expected Outcome

- Separate TutAIR product repo or clearly isolated app folder.
- Web app stack decision.
- Auth and role model: student, parent, admin.
- API/data layer for resources and progress.
- Import pipeline from Markdown canonical resources.
- CI tests and pre-ship checks.
- Staging deployment before public beta.

### Dependencies

- Milestones 3, 6, and 7.
- Mack for deployment/integration mechanics.
- Vex for security gate.
- Felix/Vera for production UI and QA.

### Comes Before

- External pilot.
- Payment/subscription decisions.

### Comes After

- Local product loop has evidence of value.

## Milestone 9 - Pilot With Real Study Sessions

**Window:** Month 8 to 10

### Objective

Test TutAIR with real revision sessions and measure whether it helps students revise more clearly, consistently, and independently.

### Why It Matters

The best product roadmap is evidence-led. A GCSE platform must prove it can reduce overwhelm, improve recall, and help students choose the next right task.

### Expected Outcome

- Pilot protocol: session length, subject mix, baseline, feedback questions.
- Metrics: task completion, confidence change, recall, return rate, confusion points.
- Qualitative notes from student/parent.
- Prioritised product fixes.
- Decision on whether to expand beyond one household.

### Dependencies

- Hosted or stable local beta.
- Privacy/safety gate.
- Enough verified subject content for meaningful sessions.

### Comes Before

- Wider release.
- Commercial positioning.

### Comes After

- Hosted beta architecture.

## Milestone 10 - Polished Product V1

**Window:** Month 10 to 12

### Objective

Turn TutAIR into a coherent V1 product with a clear promise, reliable workflow, and enough polish to show to families, tutors, or schools.

### Why It Matters

V1 should feel like a real learning companion, not a folder of clever scripts. The bar is trust, clarity, and repeat use.

### Expected Outcome

- Onboarding flow.
- Student dashboard.
- Subject library.
- Revision queue.
- AI tutor with guardrails.
- Parent-friendly progress view.
- Exportable revision packs.
- Accessibility pass.
- Security/privacy pass.
- Product documentation.

### Dependencies

- Pilot evidence.
- QA and security gates.
- Stable hosting.
- Content pipeline.

### Comes Before

- School partnerships.
- Payments.
- Multi-student classroom features.

### Comes After

- Real usage validates the core loop.

## Recommended Build Order

1. Canonical GCSE course map.
2. Source-content pipeline.
3. Durable TutAIR data model.
4. Student dashboard V1.
5. Learning engine V1.
6. AI tutor guardrails and prompt system.
7. Safety/privacy gate.
8. Hosted beta architecture.
9. Real study pilot.
10. Polished product V1.

## What Not To Build Yet

- A general AI chatbot.
- Payments or subscriptions.
- School admin dashboards.
- Multi-school analytics.
- Social features.
- Gamification beyond small completion cues.
- Automatic exam-board claims without evidence.
- A heavy database before the resource model is stable.

## Next Decision

Agree Milestone 1 and Milestone 2 as the immediate product foundation:

1. confirm course map evidence
2. improve source-content intake so every processed note has real learning material

Once those are stable, build the data model and dashboard around proven content rather than assumptions.
