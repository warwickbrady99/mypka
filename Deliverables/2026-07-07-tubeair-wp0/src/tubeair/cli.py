"""Command line interface for TubeAIR."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from tubeair.intake import DEFAULT_INTAKE_ROOT
from tubeair.processor import process_clipboard_capture, process_youtube_capture, process_youtube_url
from tubeair.transcript import TranscriptError, list_transcript_tracks
from tubeair.youtube import YouTubeUrlError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tubeair",
        description="Extract a YouTube transcript and save it as timestamped Markdown.",
    )
    parser.add_argument("url", help="One YouTube URL.")
    parser.add_argument(
        "--out-dir",
        default=None,
        type=Path,
        help="Legacy folder for generated Markdown files. Uses the WP0-WP3 local output path.",
    )
    parser.add_argument(
        "--intake-dir",
        default=DEFAULT_INTAKE_ROOT,
        type=Path,
        help=f"Fusion247/MyPKA TubeAIR intake root. Default: {DEFAULT_INTAKE_ROOT}",
    )
    parser.add_argument(
        "--language",
        default="en",
        help="Preferred transcript language code. Default: en",
    )
    parser.add_argument(
        "--list-tracks",
        action="store_true",
        help="List exposed transcript/caption tracks instead of saving Markdown.",
    )
    parser.add_argument(
        "--prefer-manual",
        action="store_true",
        default=True,
        help="Prefer manual captions over generated captions in the preferred language. Default: on",
    )
    parser.add_argument(
        "--allow-translation",
        action="store_true",
        help="Allow translated captions when the preferred language is not exposed.",
    )
    parser.add_argument(
        "--capture-mode",
        choices=["api", "clipboard"],
        default="api",
        help="Capture mode. Default: api",
    )
    parser.add_argument(
        "--clipboard-file",
        type=Path,
        help="Text file containing a manually copied transcript. Use with --capture-mode clipboard.",
    )
    parser.add_argument(
        "--ai-summary",
        action="store_true",
        help="Add optional OpenAI enrichment to the intake note.",
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Legacy alias for saving without AI enrichment.",
    )

    args = parser.parse_args(argv)

    try:
        if args.list_tracks:
            video_id = _video_id(args.url)
            tracks = list_transcript_tracks(video_id)
            if not tracks:
                print("No exposed transcript tracks found.")
                return 1
            for track in tracks:
                kind = "generated" if track.is_generated else "manual"
                translatable = "translatable" if track.is_translatable else "not-translatable"
                print(f"{track.language_code}\t{track.language}\t{kind}\t{translatable}")
            return 0

        if args.out_dir is not None and args.capture_mode == "api" and not args.ai_summary:
            result = process_youtube_url(args.url, args.out_dir, args.language, enrich=False)
        elif args.capture_mode == "clipboard":
            if args.clipboard_file is None:
                print("TubeAIR error: --capture-mode clipboard requires --clipboard-file.", file=sys.stderr)
                return 1
            transcript_text = args.clipboard_file.read_text(encoding="utf-8")
            result = process_clipboard_capture(
                args.url,
                transcript_text,
                intake_dir=args.intake_dir,
                language=args.language,
                language_code=args.language,
                enrich=args.ai_summary and not args.no_ai,
            )
        else:
            result = process_youtube_capture(
                args.url,
                intake_dir=args.intake_dir,
                language=args.language,
                prefer_manual=args.prefer_manual,
                allow_translation=args.allow_translation,
                enrich=args.ai_summary and not args.no_ai,
            )
    except (YouTubeUrlError, TranscriptError) as exc:
        print(f"TubeAIR error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"TubeAIR error: could not read clipboard import file: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"TubeAIR error: {exc}", file=sys.stderr)
        return 1

    print(f"Saved transcript: {result.output_path}")
    if result.enrichment is not None:
        print(f"AI summary: {result.enrichment.tldr}")
    elif result.enrichment_error:
        print(f"AI enrichment skipped: {result.enrichment_error}")
    return 0


def _video_id(url: str) -> str:
    from tubeair.youtube import extract_video_id

    return extract_video_id(url)


if __name__ == "__main__":
    raise SystemExit(main())
