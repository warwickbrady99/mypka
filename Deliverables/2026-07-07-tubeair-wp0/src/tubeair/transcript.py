"""Transcript fetching for YouTube videos."""

from __future__ import annotations

from tubeair.models import (
    CaptureMode,
    TranscriptCapture,
    TranscriptLine,
    TranscriptSource,
    TranscriptTrack,
)


class TranscriptError(RuntimeError):
    """Raised when TubeAIR cannot fetch a transcript for a video."""


def fetch_transcript(video_id: str, languages: list[str] | None = None) -> list[TranscriptLine]:
    """Fetch transcript lines for a YouTube video id."""

    capture = capture_best_transcript(
        video_url=f"https://www.youtube.com/watch?v={video_id}",
        video_id=video_id,
        preferred_language=(languages or ["en"])[0],
    )
    return capture.lines


def list_transcript_tracks(video_id: str) -> list[TranscriptTrack]:
    """Return all exposed YouTube transcript tracks for a video."""

    try:
        from youtube_transcript_api import TranscriptsDisabled, VideoUnavailable, YouTubeTranscriptApi
    except ImportError as exc:
        raise TranscriptError(
            "YouTube transcript support is not installed. Run: python -m pip install -e ."
        ) from exc

    try:
        transcript_list = YouTubeTranscriptApi().list(video_id)
    except (TranscriptsDisabled, VideoUnavailable) as exc:
        raise TranscriptError(f"No transcript is available for video id {video_id}.") from exc
    except Exception as exc:
        raise TranscriptError(f"Could not list transcripts for video id {video_id}: {exc}") from exc

    return [_track_from_api(item) for item in transcript_list]


def capture_best_transcript(
    video_url: str,
    video_id: str,
    preferred_language: str = "en",
    prefer_manual: bool = True,
    allow_translation: bool = False,
) -> TranscriptCapture:
    """Capture the best available transcript using TubeAIR's WP4 selection order."""

    try:
        from youtube_transcript_api import (
            NoTranscriptFound,
            TranscriptsDisabled,
            VideoUnavailable,
            YouTubeTranscriptApi,
            YouTubeTranscriptApiException,
        )
    except ImportError as exc:
        raise TranscriptError(
            "YouTube transcript support is not installed. Run: python -m pip install -e ."
        ) from exc

    try:
        transcript_list = YouTubeTranscriptApi().list(video_id)
        selected, translated = select_transcript_from_api(
            transcript_list,
            preferred_language=preferred_language,
            prefer_manual=prefer_manual,
            allow_translation=allow_translation,
        )
        raw_lines = selected.fetch()
    except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable) as exc:
        raise TranscriptError(f"No transcript is available for video id {video_id}.") from exc
    except YouTubeTranscriptApiException as exc:
        raise TranscriptError(f"Could not fetch transcript for video id {video_id}: {exc}") from exc

    track = _track_from_api(selected)
    source = TranscriptSource.YOUTUBE_TRANSLATED_CAPTIONS if translated else TranscriptSource.YOUTUBE_CAPTIONS
    return TranscriptCapture(
        video_url=video_url,
        video_id=video_id,
        lines=_lines_from_api(raw_lines),
        track=track,
        capture_mode=CaptureMode.API,
        transcript_source=source,
        translated=translated,
        timestamps_present=True,
    )


def select_transcript_from_api(
    transcript_list,
    preferred_language: str = "en",
    prefer_manual: bool = True,
    allow_translation: bool = False,
):
    """Select one transcript object from a youtube-transcript-api TranscriptList."""

    tracks = list(transcript_list)
    manual_preferred = [
        track for track in tracks if track.language_code == preferred_language and not track.is_generated
    ]
    generated_preferred = [
        track for track in tracks if track.language_code == preferred_language and track.is_generated
    ]

    if prefer_manual:
        ordered = manual_preferred + generated_preferred
    else:
        ordered = generated_preferred + manual_preferred

    if ordered:
        return ordered[0], False

    if allow_translation:
        for track in tracks:
            if getattr(track, "is_translatable", False):
                return track.translate(preferred_language), True

    if tracks:
        originals = sorted(tracks, key=lambda track: (track.is_generated, track.language_code))
        return originals[0], False

    raise TranscriptError("No exposed transcript tracks were found.")


def _track_from_api(track) -> TranscriptTrack:
    return TranscriptTrack(
        language=str(getattr(track, "language", "")).strip() or "Unknown",
        language_code=str(getattr(track, "language_code", "")).strip() or "und",
        is_generated=bool(getattr(track, "is_generated", False)),
        is_translatable=bool(getattr(track, "is_translatable", False)),
    )


def _lines_from_api(raw_lines) -> list[TranscriptLine]:
    return [
        TranscriptLine(
            start=float(line.start),
            duration=float(line.duration),
            text=str(line.text).replace("\n", " ").strip(),
        )
        for line in raw_lines
    ]
