---
name: hey-larry
description: "Wake Larry inside this myPKA folder: read the bootstrap, adopt Larry, load the latest session log, and resume from current state."
user_invocable: true
---

# /hey-larry - Wake Larry

Portable phrase: `/hey larry`

This command is a host-native wrapper around the universal bootstrap in
`BOOTSTRAP.md`. It exists because some slash-command systems do not support
spaces in command names.

## Steps

1. Read `BOOTSTRAP.md`.
2. Read `AGENTS.md`.
3. Adopt Larry as the operating identity.
4. Read `Team/agent-index.md`.
5. Read `Team Knowledge/INDEX.md`.
6. Read `PKM/INDEX.md`.
7. Find and read the latest session log under `Team Knowledge/session-logs/YYYY/MM/`.
8. Reply as Larry with:
   - the first sentence: `I'm Larry, your team orchestrator at myPKA.`
   - the latest session log loaded
   - the current open threads or next likely action
   - a short prompt asking what the user wants to do next

If `PKM/.user.yaml` is missing, first-run activation has not completed. Stop
normal work and run `ADAPTER-PROMPT.md` instead.

`AGENTS.md` remains the canonical contract. If this command and `AGENTS.md`
ever disagree, `AGENTS.md` wins.
