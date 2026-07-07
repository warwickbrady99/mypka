"""Manual transcript import for clipboard/browser-captured text."""

from __future__ import annotations

import re

from tubeair.models import (
    CaptureMode,
    TranscriptCapture,
    TranscriptLine,
    TranscriptSource,
    TranscriptTrack,
)


TIMESTAMP_PATTERN = re.compile(r"^\s*(?:(\d{1,2}):)?(\d{1,2}):(\d{2})\s+(.+?)\s*$")


def capture_from_clipboard_text(
    video_url: str,
    video_id: str,
    transcript_text: str,
    language: str = "Unknown",
    language_code: str = "und",
) -> TranscriptCapture:
    """Convert pasted transcript text into a TubeAIR capture."""

    lines = parse_clipboard_transcript(transcript_text)
    return TranscriptCapture(
        video_url=video_url,
        video_id=video_id,
        lines=lines,
        track=TranscriptTrack(
            language=language,
            language_code=language_code,
            is_generated=False,
            is_translatable=False,
        ),
        capture_mode=CaptureMode.CLIPBOARD,
        transcript_source=TranscriptSource.CLIPBOARD_MANUAL_IMPORT,
        translated=False,
        timestamps_present=any(line.start > 0 or line.duration > 0 for line in lines),
    )


def parse_clipboard_transcript(transcript_text: str) -> list[TranscriptLine]:
    """Parse timestamped or plain pasted transcript text."""

    lines: list[TranscriptLine] = []
    for raw_line in transcript_text.splitlines():
        cleaned = raw_line.strip()
        if not cleaned:
            continue

        match = TIMESTAMP_PATTERN.match(cleaned)
        if match:
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2))
            seconds = int(match.group(3))
            text = match.group(4).strip()
            start = float(hours * 3600 + minutes * 60 + seconds)
            lines.append(TranscriptLine(start=start, duration=0.0, text=text))
        else:
            lines.append(TranscriptLine(start=0.0, duration=0.0, text=cleaned))

    if not lines:
        raise ValueError("Clipboard transcript text is empty.")
    return lines
