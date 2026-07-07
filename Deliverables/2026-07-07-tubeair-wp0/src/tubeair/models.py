"""Shared TubeAIR data models."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CaptureMode(str, Enum):
    API = "api"
    CLIPBOARD = "clipboard"
    AUDIO = "audio"


class TranscriptSource(str, Enum):
    YOUTUBE_CAPTIONS = "youtube_captions"
    YOUTUBE_TRANSLATED_CAPTIONS = "youtube_translated_captions"
    CLIPBOARD_MANUAL_IMPORT = "clipboard_manual_import"
    AUDIO_TRANSCRIPTION = "audio_transcription"


@dataclass(frozen=True)
class TranscriptLine:
    start: float
    duration: float
    text: str


@dataclass(frozen=True)
class TranscriptTrack:
    language: str
    language_code: str
    is_generated: bool
    is_translatable: bool = False
    translation_language_code: str | None = None


@dataclass(frozen=True)
class TranscriptCapture:
    video_url: str
    video_id: str
    lines: list[TranscriptLine]
    track: TranscriptTrack
    capture_mode: CaptureMode
    transcript_source: TranscriptSource
    translated: bool = False
    timestamps_present: bool = True


@dataclass(frozen=True)
class AiEnrichment:
    executive_summary: str
    key_takeaways: list[str]
    action_items: list[str]
    entities: list[str]
    tags: list[str]
    tldr: str


@dataclass(frozen=True)
class ProcessingResult:
    video_id: str
    output_path: str
    enrichment: AiEnrichment | None = None
    enrichment_error: str | None = None
    capture: TranscriptCapture | None = None


@dataclass(frozen=True)
class TextSummaryResult:
    output_path: str
    summary: AiEnrichment | None = None
    summary_error: str | None = None
