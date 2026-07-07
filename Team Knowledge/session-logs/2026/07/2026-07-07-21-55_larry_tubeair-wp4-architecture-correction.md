---
agent_id: larry
session_id: codex-2026-07-07-tubeair-wp4-architecture-correction
timestamp: 2026-07-07T21:55:34+01:00
type: close-session
linked_sops: []
linked_workstreams: []
linked_guidelines: []
---

# TubeAIR WP4 Architecture Correction

## Context

The user approved the WP4 direction: TubeAIR should be a Fusion247/MyPKA capture-and-handoff tool first, not primarily an OpenAI summariser. WP4 needed to preserve WP0-WP3 while adding transcript discovery, best-track selection, metadata-rich intake Markdown, manual clipboard import, and a WP5 audio fallback boundary.

## What we did

- Added capture metadata models: `TranscriptTrack`, `TranscriptCapture`, `CaptureMode`, and `TranscriptSource`.
- Added YouTube transcript track discovery and selection order:
  - manual captions in the preferred language
  - generated captions in the preferred language
  - translated captions when allowed
  - best available original-language transcript
- Added Fusion247/MyPKA intake writing to `Team Inbox/TubeAIR/YYYY/MM/`.
- Added YAML frontmatter for downstream MyPKA/CategorisAIr routing, including `handoff_status: captured_pending_categorisation`.
- Added manual/clipboard transcript import from a text file.
- Added a WP5-only audio fallback design stub without implementing audio download or transcription.
- Updated the CLI with `--list-tracks`, `--language`, `--allow-translation`, `--intake-dir`, `--ai-summary`, `--capture-mode clipboard`, and `--clipboard-file`.
- Preserved legacy local output via `--out-dir`.
- Updated the TubeAIR README and added `Team Inbox/TubeAIR/README.md`.

## Decisions

- OpenAI enrichment is now opt-in for YouTube intake through `--ai-summary`.
- `--out-dir` remains the legacy WP0-WP3 local-output path.
- Default CLI YouTube capture now writes to the Fusion247/MyPKA TubeAIR intake root.
- Audio transcription is explicitly deferred to WP5.

## Verification

Ran the deterministic test suite from `Deliverables/2026-07-07-tubeair-wp0` with the bundled Python runtime:

```text
PYTHONPATH=src python -m unittest discover -s tests
Ran 29 tests in 0.074s
OK
```

## Open threads

- WP5 should add an explicit, consent-based audio download/transcription fallback for videos with no exposed captions.
- CategorisAIr may need a dedicated specialist or formal workstream once the first intake notes are ready for routing.

## Cross-links

- [[2026-07-07-21-48_larry_tubeair-fusion247-realignment]]
- [[Deliverables/2026-07-07-tubeair-wp0]]
- [[Team Inbox/TubeAIR/README]]
