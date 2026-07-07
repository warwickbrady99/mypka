"""YouTube URL parsing helpers."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse


class YouTubeUrlError(ValueError):
    """Raised when a URL does not contain a usable YouTube video id."""


def extract_video_id(url: str) -> str:
    """Return the video id from a common YouTube URL shape."""

    parsed = urlparse(url.strip())
    host = parsed.netloc.lower()
    path = parsed.path.strip("/")

    if host.startswith("www."):
        host = host[4:]

    if host in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        if path == "watch":
            video_ids = parse_qs(parsed.query).get("v", [])
            if video_ids and _looks_like_video_id(video_ids[0]):
                return video_ids[0]

        if path.startswith("shorts/") or path.startswith("embed/"):
            video_id = path.split("/", 1)[1].split("/", 1)[0]
            if _looks_like_video_id(video_id):
                return video_id

    if host == "youtu.be":
        video_id = path.split("/", 1)[0]
        if _looks_like_video_id(video_id):
            return video_id

    raise YouTubeUrlError(f"Could not find a YouTube video id in: {url}")


def _looks_like_video_id(value: str) -> bool:
    return len(value) == 11 and all(char.isalnum() or char in {"_", "-"} for char in value)

