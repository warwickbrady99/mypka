"""Reusable Telegram-message logic for TubeAIR."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from tubeair.processor import process_plain_text, process_youtube_url
from tubeair.transcript import TranscriptError
from tubeair.youtube import YouTubeUrlError


YOUTUBE_URL_PATTERN = re.compile(r"https?://(?:www\.)?(?:youtube\.com|youtu\.be|m\.youtube\.com|music\.youtube\.com)/\S+")
LONG_TEXT_MIN_CHARS = 500
LONG_TEXT_MIN_WORDS = 100
HELP_MESSAGE = (
    "Send me either:\n"
    "- one YouTube URL, and I will save its transcript as Markdown\n"
    "- a long pasted text message, and I will save a structured research summary"
)


@dataclass(frozen=True)
class BotResult:
    ok: bool
    reply: str
    output_path: Path | None = None


def process_message(
    text: str,
    out_dir: Path = Path("out/youtube"),
    text_out_dir: Path = Path("out/text"),
    language: str = "en",
    enrich: bool = True,
) -> BotResult:
    """Process a Telegram message body and return the reply TubeAIR should send."""

    url = find_youtube_url(text)
    if url is None:
        if is_long_plain_text(text):
            result = process_plain_text(text, out_dir=text_out_dir, enrich=enrich)
            return BotResult(
                ok=result.summary is not None,
                reply=build_text_reply(
                    result.output_path,
                    result.summary.tldr if result.summary else None,
                    result.summary_error,
                ),
                output_path=Path(result.output_path),
            )
        return BotResult(ok=False, reply=HELP_MESSAGE)

    try:
        result = process_youtube_url(url, out_dir=out_dir, language=language, enrich=enrich)
    except YouTubeUrlError as exc:
        return BotResult(ok=False, reply=f"I could not read that YouTube URL: {exc}")
    except TranscriptError as exc:
        return BotResult(ok=False, reply=f"I could not save a transcript: {exc}")

    return BotResult(
        ok=True,
        reply=build_reply(result.output_path, result.enrichment.tldr if result.enrichment else None, result.enrichment_error),
        output_path=Path(result.output_path),
    )


def build_reply(output_path: str, summary: str | None, enrichment_error: str | None = None) -> str:
    """Build the Telegram confirmation message."""

    if summary:
        return f"{summary}\n\nSaved Markdown: {output_path}"
    if enrichment_error:
        return f"Saved transcript: {output_path}\n\nAI enrichment skipped: {enrichment_error}"
    return f"Saved transcript: {output_path}"


def build_text_reply(output_path: str, summary: str | None, summary_error: str | None = None) -> str:
    """Build the Telegram confirmation message for pasted text."""

    if summary:
        return f"{summary}\n\nSaved text summary: {output_path}"
    if summary_error:
        return f"Saved pasted text: {output_path}\n\nAI summary unavailable: {summary_error}"
    return f"Saved text summary: {output_path}"


def find_youtube_url(text: str) -> str | None:
    """Return the first YouTube URL in a message, if there is one."""

    match = YOUTUBE_URL_PATTERN.search(text.strip())
    if match is None:
        return None
    return match.group(0).rstrip(".,;)")


def is_long_plain_text(text: str) -> bool:
    """Return True when a message is likely pasted source material."""

    stripped = text.strip()
    if len(stripped) >= LONG_TEXT_MIN_CHARS:
        return True
    return len(re.findall(r"\b\w+\b", stripped)) >= LONG_TEXT_MIN_WORDS
