"""Markdown generation for TubeAIR transcripts."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re

from tubeair.models import AiEnrichment, TextSummaryResult, TranscriptCapture, TranscriptLine


def build_markdown(
    video_url: str,
    video_id: str,
    lines: list[TranscriptLine],
    enrichment: AiEnrichment | None = None,
    enrichment_error: str | None = None,
    capture: TranscriptCapture | None = None,
) -> str:
    """Build a timestamped Markdown transcript."""

    captured_dt = datetime.now(timezone.utc)
    created_at = captured_dt.strftime("%Y-%m-%d %H:%M UTC")
    body = "\n".join(f"- [{format_timestamp(line.start)}] {line.text}" for line in lines)
    frontmatter = build_intake_frontmatter(capture, captured_dt) if capture else ""

    return (
        f"{frontmatter}"
        f"# YouTube Transcript - {video_id}\n\n"
        f"- Source: {video_url}\n"
        f"- Video ID: {video_id}\n"
        f"- Captured: {created_at}\n\n"
        f"{build_ai_section(enrichment, enrichment_error)}"
        "## Transcript\n\n"
        f"{body}\n"
    )


def save_markdown(
    video_url: str,
    video_id: str,
    lines: list[TranscriptLine],
    out_dir: Path,
    enrichment: AiEnrichment | None = None,
    enrichment_error: str | None = None,
    capture: TranscriptCapture | None = None,
) -> Path:
    """Write a transcript Markdown file and return its path."""

    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"{safe_filename(video_id)}.md"
    output_path.write_text(
        build_markdown(
            video_url,
            video_id,
            lines,
            enrichment=enrichment,
            enrichment_error=enrichment_error,
            capture=capture,
        ),
        encoding="utf-8",
    )
    return output_path


def save_capture_markdown(
    capture: TranscriptCapture,
    out_dir: Path,
    enrichment: AiEnrichment | None = None,
    enrichment_error: str | None = None,
) -> Path:
    """Write a Fusion247/MyPKA intake Markdown file for a transcript capture."""

    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"{datetime.now(timezone.utc):%Y-%m-%d}-{safe_filename(capture.video_id)}.md"
    output_path.write_text(
        build_markdown(
            capture.video_url,
            capture.video_id,
            capture.lines,
            enrichment=enrichment,
            enrichment_error=enrichment_error,
            capture=capture,
        ),
        encoding="utf-8",
    )
    return output_path


def build_text_summary_markdown(
    source_text: str,
    summary: AiEnrichment | None = None,
    summary_error: str | None = None,
) -> str:
    """Build a Markdown research note for pasted plain text."""

    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    excerpt = source_text.strip()
    if len(excerpt) > 4000:
        excerpt = excerpt[:4000] + "\n\n[Original pasted text truncated in saved note.]"

    return (
        "# Text Summary\n\n"
        f"- Captured: {created_at}\n"
        f"- Source: Pasted Telegram text\n\n"
        f"{build_ai_section(summary, summary_error)}"
        "## Source Text Excerpt\n\n"
        f"{excerpt}\n"
    )


def save_text_summary_markdown(
    source_text: str,
    out_dir: Path,
    summary: AiEnrichment | None = None,
    summary_error: str | None = None,
) -> Path:
    """Write a pasted-text summary Markdown file and return its path."""

    out_dir.mkdir(parents=True, exist_ok=True)
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")
    output_path = out_dir / f"{created_at}-text-summary.md"
    output_path.write_text(
        build_text_summary_markdown(source_text, summary=summary, summary_error=summary_error),
        encoding="utf-8",
    )
    return output_path


def build_ai_section(enrichment: AiEnrichment | None, enrichment_error: str | None = None) -> str:
    """Build the optional AI research section."""

    if enrichment is None and not enrichment_error:
        return ""

    if enrichment is None:
        return "## AI Research Assistant\n\n" f"> AI enrichment unavailable: {enrichment_error}\n\n"

    return (
        "## AI Research Assistant\n\n"
        "### TL;DR\n\n"
        f"{enrichment.tldr}\n\n"
        "### Executive Summary\n\n"
        f"{enrichment.executive_summary}\n\n"
        "### Key Takeaways\n\n"
        f"{format_bullets(enrichment.key_takeaways)}\n"
        "### Action Items\n\n"
        f"{format_bullets(enrichment.action_items)}\n"
        "### Important Names, Companies and Places\n\n"
        f"{format_bullets(enrichment.entities)}\n"
        "### Tags\n\n"
        f"{format_tags(enrichment.tags)}\n\n"
    )


def build_intake_frontmatter(capture: TranscriptCapture, captured_at: datetime) -> str:
    """Build the YAML contract consumed by Fusion247/MyPKA intake."""

    generated = "generated" if capture.track.is_generated else "manual"
    return (
        "---\n"
        "type: tubeair_youtube_transcript\n"
        f"source_url: {yaml_quote(capture.video_url)}\n"
        f"video_id: {yaml_quote(capture.video_id)}\n"
        f"language: {yaml_quote(capture.track.language)}\n"
        f"language_code: {yaml_quote(capture.track.language_code)}\n"
        f"caption_kind: {generated}\n"
        f"is_generated: {yaml_bool(capture.track.is_generated)}\n"
        f"translated: {yaml_bool(capture.translated)}\n"
        f"capture_mode: {capture.capture_mode.value}\n"
        f"transcript_source: {capture.transcript_source.value}\n"
        f"timestamps_present: {yaml_bool(capture.timestamps_present)}\n"
        f"captured_datetime: {captured_at.strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        "handoff_status: captured_pending_categorisation\n"
        "categorisair_status: pending\n"
        "assigned_agents: []\n"
        "routing_notes: []\n"
        "---\n\n"
    )


def yaml_bool(value: bool) -> str:
    return "true" if value else "false"


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def format_bullets(items: list[str]) -> str:
    """Format a Markdown bullet list with a stable empty state."""

    if not items:
        return "- None identified.\n\n"
    return "".join(f"- {item}\n" for item in items) + "\n"


def format_tags(tags: list[str]) -> str:
    """Format tags for easy Obsidian-style scanning."""

    if not tags:
        return "None identified."
    return " ".join(f"#{safe_filename(tag.lower())}" for tag in tags)


def format_timestamp(seconds: float) -> str:
    """Format seconds as HH:MM:SS for stable transcript timestamps."""

    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def safe_filename(value: str) -> str:
    """Return a filesystem-safe filename stem."""

    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-") or "youtube-transcript"
