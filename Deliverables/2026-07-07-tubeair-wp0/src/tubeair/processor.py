"""End-to-end TubeAIR video processing."""

from __future__ import annotations

from pathlib import Path

from tubeair.ai import AiConfigurationError, AiProviderError, create_ai_provider_from_env
from tubeair.clipboard_capture import capture_from_clipboard_text
from tubeair.intake import dated_intake_dir
from tubeair.markdown import save_capture_markdown, save_markdown, save_text_summary_markdown
from tubeair.models import AiEnrichment, ProcessingResult, TextSummaryResult
from tubeair.transcript import capture_best_transcript, fetch_transcript
from tubeair.youtube import extract_video_id


def process_youtube_url(
    url: str,
    out_dir: Path = Path("out/youtube"),
    language: str = "en",
    enrich: bool = True,
) -> ProcessingResult:
    """Fetch a transcript, optionally enrich it, and save one Markdown file."""

    video_id = extract_video_id(url)
    lines = fetch_transcript(video_id, languages=[language])
    enrichment: AiEnrichment | None = None
    enrichment_error: str | None = None

    if enrich:
        try:
            enrichment = create_ai_provider_from_env().enrich(url, video_id, lines)
        except (AiConfigurationError, AiProviderError) as exc:
            enrichment_error = str(exc)

    output_path = save_markdown(
        url,
        video_id,
        lines,
        out_dir,
        enrichment=enrichment,
        enrichment_error=enrichment_error,
    )

    return ProcessingResult(
        video_id=video_id,
        output_path=str(output_path),
        enrichment=enrichment,
        enrichment_error=enrichment_error,
    )


def process_youtube_capture(
    url: str,
    intake_dir: Path | None = None,
    language: str = "en",
    prefer_manual: bool = True,
    allow_translation: bool = False,
    enrich: bool = False,
) -> ProcessingResult:
    """Capture a YouTube transcript into the Fusion247/MyPKA intake path."""

    video_id = extract_video_id(url)
    capture = capture_best_transcript(
        video_url=url,
        video_id=video_id,
        preferred_language=language,
        prefer_manual=prefer_manual,
        allow_translation=allow_translation,
    )
    return _save_capture(capture, intake_dir=intake_dir, enrich=enrich)


def process_clipboard_capture(
    url: str,
    transcript_text: str,
    intake_dir: Path | None = None,
    language: str = "Unknown",
    language_code: str = "und",
    enrich: bool = False,
) -> ProcessingResult:
    """Save a manually pasted transcript into the Fusion247/MyPKA intake path."""

    video_id = extract_video_id(url)
    capture = capture_from_clipboard_text(
        video_url=url,
        video_id=video_id,
        transcript_text=transcript_text,
        language=language,
        language_code=language_code,
    )
    return _save_capture(capture, intake_dir=intake_dir, enrich=enrich)


def _save_capture(capture, intake_dir: Path | None = None, enrich: bool = False) -> ProcessingResult:
    enrichment: AiEnrichment | None = None
    enrichment_error: str | None = None

    if enrich:
        try:
            enrichment = create_ai_provider_from_env().enrich(capture.video_url, capture.video_id, capture.lines)
        except (AiConfigurationError, AiProviderError) as exc:
            enrichment_error = str(exc)

    output_path = save_capture_markdown(
        capture,
        dated_intake_dir(intake_dir),
        enrichment=enrichment,
        enrichment_error=enrichment_error,
    )

    return ProcessingResult(
        video_id=capture.video_id,
        output_path=str(output_path),
        enrichment=enrichment,
        enrichment_error=enrichment_error,
        capture=capture,
    )


def process_plain_text(
    text: str,
    out_dir: Path = Path("out/text"),
    enrich: bool = True,
) -> TextSummaryResult:
    """Summarize pasted text and save one Markdown file."""

    summary: AiEnrichment | None = None
    summary_error: str | None = None

    if enrich:
        try:
            summary = create_ai_provider_from_env().summarize_text(text)
        except AiConfigurationError as exc:
            summary_error = (
                f"{exc} Add OPENAI_API_KEY, then try again. The pasted text was saved without an AI summary."
            )
        except AiProviderError as exc:
            summary_error = (
                f"{exc} Check your API quota/billing or try again later. The pasted text was saved without an AI summary."
            )

    output_path = save_text_summary_markdown(
        text,
        out_dir,
        summary=summary,
        summary_error=summary_error,
    )

    return TextSummaryResult(
        output_path=str(output_path),
        summary=summary,
        summary_error=summary_error,
    )
