---
id: tsk-2026-07-09-002
title: "Build TutAIR source-content pipeline"
assignee: mack
priority: 2
status: open
blocked_reason: null
blocked_by: null
created: 2026-07-09T12:45:00Z
updated: 2026-07-09T12:45:00Z
due: null
created_by: larry
source: tutair-roadmap-milestone-2
parent: null
linked_sops:
  - SOP-create-task
linked_workstreams:
  - WS-005-process-tutair-captures
  - WS-004-process-tubeair-captures
linked_guidelines:
  - GL-001-file-naming-conventions
linked_my_life: []
linked_session_logs: []
linked_journal_entries: []
linked_deliverables:
  - 2026-07-09-tutair-product-roadmap
  - 2026-07-09-tutair-mvp
tags:
  - tutair
  - gcse
  - product-plan
  - milestone-2
---

# Build TutAIR source-content pipeline

## What this is
Milestone 2 of the approved TutAIR product plan. Build the foundation that lets TutAIR process real educational content instead of URL-only captures.

## Context one click away
- Workstream: [[WS-005-process-tutair-captures]]
- Reuse reference: [[WS-004-process-tubeair-captures]]
- Working artifacts:
  - [[2026-07-09-tutair-product-roadmap]]
  - [[2026-07-09-tutair-mvp]]

## Success criteria
- TutAIR clearly separates raw source content, capture metadata/extracted content, and processed learning resources.
- Pasted transcript or lesson text is stored as raw source content separately from processed resources.
- URL-only captures are marked `needs_source_content` and blocked from processing.
- The pipeline can later link captures and resources to course-map learning objective IDs.
- TubeAIR transcript capture is reused by architecture, not duplicated.
- Focused tests and documentation cover the readiness gate.
- AI tutoring, dashboards, and new revision features remain out of scope.

## Updates
- 2026-07-09 12:45 (larry) - created as the active Milestone 2 task after Milestone 1 completion was confirmed.

## Outcome
_(filled when status flips to done - see SOP-close-task)_
