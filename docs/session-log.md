# Session Log

Use this lightweight log to help future Codex chats continue quickly. Keep entries short: what changed, why, and what should happen next.

## 2026-07-06 - Project context system

- Added a quick-start context pointer to `README.md`.
- Created `docs/context.md` to explain the project, architecture, folders, design decisions, current progress, outstanding tasks, and rules.
- Created this `docs/session-log.md` for short handoff notes across Codex chats.
- Current project focus: help a 15-year-old student use myPKA/ICOR for GCSE revision and AI learning during work experience week.
- Known subjects: Maths, English, Science, Computer Science, Business Enterprise, Construction, and History.
- Important caution: exam boards and qualifications are not confirmed yet. Do not build board-specific resources until they are verified.
- Next best step: collect the exam board, qualification, tier, and exam/mock dates for each subject, then create an exam-board map.

## 2026-07-06 - GCSE study documentation layer

- Created `docs/exam-board-map.md` as the source-of-truth template for subjects, qualification types, exam boards, tiers, sources, and status.
- Created `docs/revision-framework.md` to turn confirmed course details into topic trackers, confidence scoring, weekly revision tasks, mistake reviews, and AI tutoring prompts.
- Created `docs/student-guide.md` as the beginner-friendly guide for using the system without overcomplicating it.
- Preserved the key caution: exam boards for Neston High School subjects are still unconfirmed, so all board-specific details remain placeholders until verified.

## 2026-07-06 - Draft Neston exam-board map added

- Updated `docs/exam-board-map.md` with the user's ChatGPT-researched draft from Neston High School curriculum pages.
- Marked school-page details separately from personal route, tier, code, and teacher-confirmation gaps.
- Updated `docs/revision-framework.md` with a draft course summary and starter trackers, while keeping uncertain items clearly labelled.
- Updated `docs/student-guide.md` with the next teacher-confirmation priorities.

## 2026-07-06 - Hat Business OS MVP dashboard

- Inspected the repo and found the existing `Expansions/mypka-cockpit` app: Node/Express backend, Vite/React frontend, and a read-only `mypka.db` mirror plus a separate writeable `mypka-cockpit.db`.
- Chose the smallest sensible architecture: add a `Hat Business OS` cockpit module rather than building a separate app.
- Added local Business OS tables in `mypka-cockpit.db` for suppliers, designs, products, product costs, stock, and orders.
- Added starter seed data based on the first activewear hat ideas so the dashboard has useful example records.
- Added `/api/business-os/overview` for the dashboard data and profit calculations.
- Added a React dashboard view with product cards, live ecommerce product URL fields, stock status, supplier/design summaries, order table, and profit per product.
- Added `Hat Business OS` to the cockpit sidebar as an Overview module.
- Important boundary: this is an MVP admin dashboard, not a full ecommerce backend. The live customer website remains separate for now and is linked through each product's `ecommerce_product_url`.
- Verification note: dependency install for the web app was attempted using the bundled `pnpm`, but pnpm stopped on its build-script approval gate for `esbuild`. A full build was not completed in this session.
- Next steps: approve/rebuild dependencies if needed, run the cockpit web build, open `#/hat-business-os`, then add edit forms for products/costs/stock once the dashboard shape feels right.
# Session Log - 2026-07-06 - Custom Cap Brand Setup

## What Larry Created

- Created `docs/brand/` for brand direction documents.
- Created `docs/business/` for launch, pricing, marketing, and planning documents.
- Created `docs/research/` for supplier and legal research checklists.
- Created `docs/designs/` for cap product and concept planning.
- Added `docs/brand/brand-foundation.md`.
- Added `docs/designs/custom-cap-product-plan.md`.
- Added `docs/research/research-checklist.md`.
- Added `docs/business/launch-plan.md`.
- Added `docs/business/cost-and-pricing-template.md`.
- Added `docs/business/content-and-marketing-ideas.md`.
- Added `docs/business/questions-for-me.md`.

## Key Assumptions

- The brand starts with custom caps only.
- The first launch should be small, low-risk, and feedback-led.
- The owner is 15, so parent or guardian help may be required for payments, supplier orders, accounts, selling platforms, and legal questions.
- No accounts should be created and no purchases should be made until the setup is checked with a parent or guardian.
- The brand can expand into clothing later, but only after the first cap test gives real feedback.

## Open Questions

- What vibe should the brand have?
- Which starter colours are preferred?
- Is there already a brand name idea?
- Should the first designs use text, logos, symbols, custom names, initials, or numbers?
- What sample budget is realistic?
- Is parent or guardian help available for payments and orders?

## Next Suggested Task

Answer `docs/business/questions-for-me.md`, then use those answers to narrow the brand direction and choose 3 to 5 first cap concepts.

## Token-Saving Note

When the context changes significantly, start a new Codex chat and point it to these docs so future work can continue without relying on chat history.

## 2026-07-08 - F247 AsdAIr FastAPI MVP completed

- Completed the FastAPI MVP in `Deliverables/2026-07-08-f247-asdair-microsite/`.
- MVP scope: Mum shopping page, Warwick admin dashboard, SQLite, Markdown/JSON exports, Claude Chrome handoff export, optional email notifications, tests, manual QA checklist, phone shortcut guide, and VPS deployment notes.
- Safety boundary preserved: this is a shopping request and basket-preparation aid only. No Asda login, payment, checkout, API, or order placement.
- The FastAPI implementation remains the reference MVP and should not be deleted or overwritten during the Next.js migration.

## 2026-07-08 - AsdAIr hosting pivot to Next.js/Vercel

- Reviewed the completed FastAPI implementation and compared FastAPI/VPS with Next.js/Vercel for this specific project.
- Decision: V1 should use GitHub -> Vercel -> Mum-facing Next.js app -> structured email -> Warwick/local processing -> Local Brain / `inbox-asdair`.
- Keep local for V1: SQLite, admin dashboard, filesystem exports, Claude Chrome handoff files, Local Brain intake, and final Asda basket/checkout workflow.
- Move to Vercel for V1: Mum-facing private page, static catalogue, form submission endpoint, and structured email notification.
- Recommended avoiding cloud database/admin until the email workflow is trusted.

## 2026-07-08 - Next.js V1 Mum page port

- Created the sibling app `Deliverables/2026-07-08-f247-asdair-microsite-nextjs/`.
- Ported only the Mum-facing page from the FastAPI MVP: private token route, grouped shopping items, quantity buttons, `Use usual shop`, `Anything else?`, and confirmation preview.
- Ported the starter catalogue into `lib/catalogue.ts`.
- Added local app docs in the Next.js `README.md`.
- Installed dependencies with bundled `pnpm`; `pnpm` reported an ignored-build-scripts approval gate for native packages, but the app built successfully by invoking Next directly.
- Current limitation: browser-level local QA was not completed because the sandbox blocked launching a hidden dev server from the session.
- Next step: add structured email submission, then replace the local preview with a real sent/error confirmation.

## 2026-07-09 - TutAIR MVP V1/V2 completed

- Created `Team Inbox/TutAIR/README.md` as the GCSE learning intake lane.
- Created `Team Knowledge/Workstreams/WS-005-process-tutair-captures.md` and added it to the Workstreams index.
- Created `Deliverables/2026-07-09-tutair-mvp/` with capture and processed-note templates, beginner instructions, intake and processor scripts, focused tests, and local `.gitignore`.
- V1 intake creates Markdown captures from either a YouTube URL or UTF-8 pasted text file and saves them under `Team Inbox/TutAIR/YYYY/MM/`.
- V2 processor reads one TutAIR capture Markdown file and writes an ADHD-friendly processed note under `Team Inbox/TutAIR/YYYY/MM/processed/`.
- Exam-board mapping remains `unconfirmed` by default and is only treated as confirmed when status and evidence are both present.
- Cleanup removed generated Python cache, temporary test inbox files, and placeholder TutAIR test captures from the real inbox.
- Out of scope: web dashboard, TubeAIR behavior changes, automatic YouTube transcript fetching, AI enrichment, batch processing, and confirmed exam-board/spec mapping.
- Next best step: TutAIR V3 should add a safe source-content path for YouTube transcripts, then batch-process pending captures once the single-file workflow is trusted.

## 2026-07-09 - TutAIR V3 local viewer

- Added `tutair_viewer.py` as a local read-only web viewer inside `Deliverables/2026-07-09-tutair-mvp/`.
- The viewer reads processed Markdown notes from `Team Inbox/TutAIR/YYYY/MM/processed/`.
- It groups the note list by subject and displays topic, exam-board status, tiny summary, key facts, what this means, exam-style questions, flashcards, next revision task, and exam-board mapping.
- Added `test_tutair_viewer.py` and updated the TutAIR README and beginner instructions with local run steps.
- V3 intentionally does not publish online, edit Markdown, change TubeAIR, fetch YouTube transcripts, add a database, or rebuild TutAIR from scratch.
- Check run: `python -m unittest test_tutair_intake.py test_tutair_process.py test_tutair_viewer.py` passed with 16 tests.
