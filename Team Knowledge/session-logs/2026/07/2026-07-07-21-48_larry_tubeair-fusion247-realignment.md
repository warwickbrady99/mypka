---
agent_id: larry
session_id: codex-2026-07-07-tubeair-fusion247-realignment
timestamp: 2026-07-07T21:48:51+01:00
type: realignment
linked_sops: []
linked_workstreams: []
linked_guidelines: []
---

# TubeAIR Fusion247 Realignment

## Original direction

TubeAIR WP0-WP3 had drifted toward a standalone beginner-friendly intake bot: YouTube URL in, transcript Markdown out, optional OpenAI summary, plus Telegram handling for long pasted text.

## Correction

TubeAIR should be treated as a mini-project inside Fusion247/MyPKA. Its primary purpose is to capture the fullest available YouTube transcript and hand it into the Fusion247 intake path so myPKA, CategorisAIr, and recruited sub-agents can process it. OpenAI summarisation should remain optional enrichment, not the primary processing path.

## Why it matters

The saved Markdown needs to become an intake artifact with provenance, transcript source metadata, processing status, and downstream handoff fields. WP4 should correct architecture and intake routing before adding more summary features.

## Implications

- Transcript capture must distinguish manual captions, auto-generated captions, translated captions, language choice, timestamps, and unavailable-caption fallback.
- The current `out/youtube/` location is project-local output, not the Fusion247 intake destination.
- Mack should own capture/fallback wiring, Silas should own the intake Markdown contract, and Nolan may need to recruit or formalize CategorisAIr-specific roles after transcript capture.
