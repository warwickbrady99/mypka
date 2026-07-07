---
agent_id: larry
session_id: codex-2026-07-07-agent-bootstrap
timestamp: 2026-07-07T22:34:30+01:00
type: close-session
linked_sops: []
linked_workstreams: []
linked_guidelines: []
---

# Agent Bootstrap

## Context

The user asked for a bootstrap so any supported coding agent, including Codex, Claude Code, and future tools, can enter the project, discover agent definitions, adopt Larry, and continue from the latest session log.

## What we did

- Larry created `BOOTSTRAP.md` as the host-neutral session entrypoint.
- Larry created `AGENTS.md.codex` as the Codex-specific pointer.
- Larry updated `CLAUDE.md` to point normal session resume at `BOOTSTRAP.md`.
- Larry updated the README quick-start for future coding-agent sessions.

## Decisions made

- **Question:** Where should the universal bootstrap live?
  **Decision:** Put it at the repository root as `BOOTSTRAP.md` so every host and future tool can discover it without knowing host-specific conventions.
- **Question:** Should the bootstrap duplicate `AGENTS.md`?
  **Decision:** No. `AGENTS.md` remains the source of truth. The bootstrap only defines the session-entry sequence and points to canonical files.

## Insights

- The existing `ADAPTER-PROMPT.md` is first-run activation heavy. A separate runtime bootstrap is cleaner for everyday resume sessions.
- The latest session log is now explicitly part of startup state, not just historical record.

## Realignments

- _(none this session)_

## Open threads

- [ ] Future host support can add short pointer files such as `GEMINI.md` or `.cursor/rules/main.md` that reference `BOOTSTRAP.md` without duplicating the root contract.

## Next steps

- In future coding-agent sessions, start by reading `BOOTSTRAP.md`, then `AGENTS.md`, then the latest session log.

## Cross-links

- `[[2026-07-07-21-55_larry_tubeair-wp4-architecture-correction]]`
