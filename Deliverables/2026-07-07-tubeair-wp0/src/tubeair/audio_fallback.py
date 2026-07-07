"""WP5 design placeholder for audio transcription fallback.

TubeAIR WP4 intentionally does not download audio or run transcription. WP5
should add an explicit, consent-based fallback for videos with no exposed
caption tracks, using either local Whisper-style transcription or an OpenAI
transcription provider.
"""

from __future__ import annotations


def audio_fallback_not_implemented() -> None:
    """Raise the planned WP5 boundary as a clear runtime error."""

    raise NotImplementedError("Audio transcription fallback is planned for TubeAIR WP5.")
