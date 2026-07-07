---
agent_id: larry
session_id: codex-2026-07-07-hey-larry-bootstrap-command
timestamp: 2026-07-07T22:37:38+01:00
type: close-session
linked_sops: []
linked_workstreams: []
linked_guidelines: []
---

# Hey Larry Bootstrap Command

## Context

The user asked to name the bootstrap command `/hey larry` so any supported AI host can wake up, know where it is, adopt Larry, and resume from the latest session log.

## What we did

- Larry added `/hey larry` as the portable wake phrase in `BOOTSTRAP.md`.
- Larry updated `AGENTS.md.codex` so Codex treats `/hey larry` as the resume trigger.
- Larry updated `CLAUDE.md` with the same wake phrase.
- Larry added `.claude/commands/hey-larry.md` as the Claude-compatible slash command wrapper because host command filenames may not support spaces.
- Larry updated `README.md` so future sessions see `/hey larry` as the short startup prompt.

## Decisions made

- **Question:** Should the canonical user phrase be `/hey larry` even if some hosts cannot bind slash commands with spaces?
  **Decision:** Yes. `/hey larry` is the portable natural-language wake phrase. Hosts that need a command filename use `/hey-larry` as a wrapper for the same behavior.

## Insights

- A human wake phrase is better than a technical command name for cross-host continuity. It helps the user remember the action and helps the agent remember the identity overlay.

## Realignments

- _(none this session)_

## Open threads

- [ ] Future host pointer files, such as `GEMINI.md` or Cursor rules, should reference `/hey larry` when those hosts are added.

## Next steps

- In any new coding-agent session, the user can say `/hey larry` to trigger the bootstrap flow.

## Cross-links

- `[[2026-07-07-22-34_larry_agent-bootstrap]]`
