"""AI enrichment providers for TubeAIR."""

from __future__ import annotations

from abc import ABC, abstractmethod
import json
import os
from typing import Any
from urllib import error, request

from tubeair.models import AiEnrichment, TranscriptLine


OPENAI_API_KEY_ENV_VAR = "OPENAI_API_KEY"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"


class AiConfigurationError(RuntimeError):
    """Raised when no usable AI provider is configured."""


class AiProviderError(RuntimeError):
    """Raised when an AI provider cannot complete enrichment."""


class AiProvider(ABC):
    """Interface for transcript enrichment providers."""

    @abstractmethod
    def enrich(self, video_url: str, video_id: str, lines: list[TranscriptLine]) -> AiEnrichment:
        """Return structured enrichment for a transcript."""

    @abstractmethod
    def summarize_text(self, text: str) -> AiEnrichment:
        """Return structured enrichment for pasted plain text."""


class OpenAiProvider(AiProvider):
    """OpenAI Chat Completions provider.

    The provider uses only environment-sourced credentials and avoids a hard SDK
    dependency so TubeAIR remains easy to install for beginners.
    """

    def __init__(self, api_key: str, model: str = DEFAULT_OPENAI_MODEL) -> None:
        self.api_key = api_key
        self.model = model

    def enrich(self, video_url: str, video_id: str, lines: list[TranscriptLine]) -> AiEnrichment:
        transcript_text = transcript_as_text(lines)
        payload = {
            "model": self.model,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are TubeAIR, a careful research assistant. Return valid JSON only. "
                        "Do not invent facts that are not supported by the transcript."
                    ),
                },
                {
                    "role": "user",
                    "content": build_enrichment_prompt(video_url, video_id, transcript_text),
                },
            ],
        }

        response_body = self._post_json("https://api.openai.com/v1/chat/completions", payload)
        try:
            content = response_body["choices"][0]["message"]["content"]
            data = json.loads(content)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise AiProviderError("OpenAI returned an unexpected enrichment response.") from exc

        return parse_enrichment(data)

    def summarize_text(self, text: str) -> AiEnrichment:
        payload = {
            "model": self.model,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are TubeAIR, a careful research intake assistant. Return valid JSON only. "
                        "Do not invent facts that are not supported by the supplied text."
                    ),
                },
                {
                    "role": "user",
                    "content": build_text_summary_prompt(plain_text_for_ai(text)),
                },
            ],
        }

        response_body = self._post_json("https://api.openai.com/v1/chat/completions", payload)
        try:
            content = response_body["choices"][0]["message"]["content"]
            data = json.loads(content)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise AiProviderError("OpenAI returned an unexpected text summary response.") from exc

        return parse_enrichment(data)

    def _post_json(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        http_request = request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

        try:
            with request.urlopen(http_request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise AiProviderError(f"OpenAI enrichment failed with HTTP {exc.code}: {detail}") from exc
        except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise AiProviderError(f"OpenAI enrichment failed: {exc}") from exc


def create_ai_provider_from_env() -> AiProvider:
    """Create the configured AI provider from environment variables."""

    api_key = os.environ.get(OPENAI_API_KEY_ENV_VAR)
    if not api_key:
        raise AiConfigurationError(f"Set {OPENAI_API_KEY_ENV_VAR} to enable AI enrichment.")

    model = os.environ.get("TUBEAIR_OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
    return OpenAiProvider(api_key=api_key, model=model)


def build_enrichment_prompt(video_url: str, video_id: str, transcript_text: str) -> str:
    """Build the provider-neutral enrichment request."""

    return (
        f"Video URL: {video_url}\n"
        f"Video ID: {video_id}\n\n"
        "Analyze the transcript and return a JSON object with exactly these keys:\n"
        "- executive_summary: string, 5-10 sentences\n"
        "- key_takeaways: array of 5 strings\n"
        "- action_items: array of practical action strings\n"
        "- entities: array of important names, companies, and places\n"
        "- tags: array of short lowercase tags\n"
        "- tldr: one sentence\n\n"
        "Transcript:\n"
        f"{transcript_text}"
    )


def build_text_summary_prompt(text: str) -> str:
    """Build the provider-neutral plain-text summary request."""

    return (
        "Summarize the following pasted text and return a JSON object with exactly these keys:\n"
        "- executive_summary: string, 5-10 sentences\n"
        "- key_takeaways: array of 5 strings\n"
        "- action_items: array of practical action strings\n"
        "- entities: array of people, companies, organizations, and places mentioned\n"
        "- tags: array of short lowercase tags\n"
        "- tldr: one sentence\n\n"
        "Text:\n"
        f"{text}"
    )


def transcript_as_text(lines: list[TranscriptLine], max_chars: int = 60000) -> str:
    """Flatten transcript lines while keeping timestamps for context."""

    text = "\n".join(f"[{int(line.start)}s] {line.text}" for line in lines)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n[Transcript truncated for AI processing.]"


def plain_text_for_ai(text: str, max_chars: int = 60000) -> str:
    """Trim long pasted text to the provider request budget."""

    cleaned = text.strip()
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[:max_chars] + "\n[Text truncated for AI processing.]"


def parse_enrichment(data: dict[str, Any]) -> AiEnrichment:
    """Normalize provider JSON into TubeAIR's enrichment model."""

    return AiEnrichment(
        executive_summary=str(data.get("executive_summary", "")).strip(),
        key_takeaways=_string_list(data.get("key_takeaways"))[:5],
        action_items=_string_list(data.get("action_items")),
        entities=_string_list(data.get("entities")),
        tags=[tag.lower().strip().replace(" ", "-") for tag in _string_list(data.get("tags"))],
        tldr=str(data.get("tldr", "")).strip(),
    )


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]
