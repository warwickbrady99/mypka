---
id: tsk-2026-07-09-001
title: "Confirm TutAIR GCSE course map"
assignee: pax
priority: 2
status: open
blocked_reason: null
blocked_by: null
created: 2026-07-09T10:41:02Z
updated: 2026-07-09T11:15:00Z
due: null
created_by: larry
source: tutair-roadmap-approval-2026-07-09
parent: null
linked_sops:
  - SOP-create-task
linked_workstreams:
  - WS-005-process-tutair-captures
linked_guidelines:
  - GL-001-file-naming-conventions
  - GL-004-task-resource-linking
linked_my_life: []
linked_session_logs: []
linked_journal_entries: []
linked_deliverables:
  - 2026-07-09-tutair-product-roadmap
  - 2026-07-09-tutair-mvp/course-map
tags:
  - tutair
  - gcse
  - product-plan
  - milestone-1
---

# Confirm TutAIR GCSE course map

## What this is
Milestone 1 of the approved TutAIR product plan. Confirm the student's real GCSE subjects, boards, qualification routes, tiers, paper structures, official sources, and remaining unknowns so TutAIR can stop treating course mapping as draft context.

## Context one click away
- Procedure: [[SOP-create-task]]
- Workstream: [[WS-005-process-tutair-captures]]
- Guideline: [[GL-001-file-naming-conventions]]
- Guideline: [[GL-004-task-resource-linking]]
- Working artifacts:
  - [[2026-07-09-tutair-product-roadmap]]
  - [[course-map]]

## Success criteria
- `docs/exam-board-map.md` clearly distinguishes confirmed, school-page draft, teacher-confirmation-needed, and unknown details for every subject.
- Each subject has a next evidence action: teacher, school document, exam timetable, official specification, or revision-guide confirmation.
- TutAIR has a clear rule for whether a processed resource may use board-specific language.
- Changes are tested where relevant, documented, and committed before Milestone 2 starts.

## Updates
- 2026-07-09 11:41 (larry) - created after the user approved the TutAIR roadmap as the product plan.
- 2026-07-09 12:15 (larry) - added the Milestone 1 course-map MVP: separate schema, beginner instructions, JSON course map, validation script, and tests for an AQA GCSE Combined Science: Trilogy Biology Paper 1 / Cell biology slice.
- 2026-07-09 12:20 (larry) - checks passed: `test_course_map.py` ran 5 tests, existing TutAIR intake/process/viewer tests ran 16 tests, and `validate_course_map.py` reported the course map valid.

## Outcome
_(filled when status flips to done - see SOP-close-task)_
