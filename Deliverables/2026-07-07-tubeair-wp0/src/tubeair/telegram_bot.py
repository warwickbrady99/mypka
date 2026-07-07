"""Telegram bot entry point for TubeAIR."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

from tubeair.bot import process_message
from tubeair.intake import DEFAULT_INTAKE_ROOT


TOKEN_ENV_VAR = "TELEGRAM_BOT_TOKEN"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tubeair-telegram",
        description="Run the TubeAIR Telegram bot.",
    )
    parser.add_argument(
        "--intake-dir",
        default=DEFAULT_INTAKE_ROOT,
        type=Path,
        help=f"Fusion247/MyPKA TubeAIR intake root. Default: {DEFAULT_INTAKE_ROOT}",
    )
    parser.add_argument(
        "--text-out-dir",
        default="out/text",
        type=Path,
        help="Folder for pasted text summaries. Default: out/text",
    )
    parser.add_argument(
        "--language",
        default="en",
        help="Preferred transcript language code. Default: en",
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Save transcripts without AI enrichment.",
    )

    args = parser.parse_args(argv)
    token = os.environ.get(TOKEN_ENV_VAR)
    if not token:
        print(f"TubeAIR error: set {TOKEN_ENV_VAR} before starting the bot.", file=sys.stderr)
        return 1

    try:
        from telegram import Update
        from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
    except ImportError as exc:
        print(
            "TubeAIR error: Telegram support is not installed. Run: python -m pip install -e .",
            file=sys.stderr,
        )
        return 1

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if update.message is not None:
            await update.message.reply_text("Send me a YouTube URL and I will save its transcript as Markdown.")

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context
        if update.message is None or update.message.text is None:
            return

        result = process_message(
            update.message.text,
            intake_dir=args.intake_dir,
            text_out_dir=args.text_out_dir,
            language=args.language,
            enrich=not args.no_ai,
        )
        await update.message.reply_text(result.reply)

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("TubeAIR Telegram bot is running. Send a YouTube URL or long pasted text. Press Ctrl+C to stop.")
    app.run_polling()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
