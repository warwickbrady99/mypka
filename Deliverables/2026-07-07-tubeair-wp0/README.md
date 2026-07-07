# TubeAIR WP4

TubeAIR is a Fusion247/MyPKA capture-and-handoff tool.

It can:

1. Discover available YouTube transcript/caption tracks.
2. Capture the best available transcript into the Fusion247/MyPKA intake path.
3. Preserve transcript metadata in YAML frontmatter for downstream MyPKA/CategorisAIr routing.
4. Import manually copied transcripts from a clipboard/text file fallback.
5. Optionally add OpenAI enrichment when requested.

OpenAI summarisation is optional. The core workflow is capture first, then hand off to MyPKA/CategorisAIr.

WP0-WP3 behavior is still available:

1. Turn a YouTube URL into a local Markdown transcript and optional AI research note.
2. Turn a long pasted Telegram message into a Markdown summary.

Short messages show help instructions so the bot does not waste AI credits on casual chat.

## Current State

WP4 is implemented and tested.

- WP0/WP1/WP2 YouTube behaviour is still intact.
- Telegram now accepts either a YouTube URL or a long pasted text message.
- Long pasted text is routed to a dedicated plain-text processor.
- AI output uses the existing provider interface and the shared summary structure, but YouTube intake does not use AI unless `--ai-summary` is passed.
- The new capture-first CLI writes YouTube transcript intake notes to `Team Inbox/TubeAIR/YYYY/MM/`.
- Legacy local transcript output is still available with `--out-dir`.
- The current long-text threshold is 500 characters or 100 words.
- The test suite currently has 29 passing tests.

## Fusion247/MyPKA Intake Destination

By default, WP4 writes YouTube capture notes here:

```text
C:\Users\Buggly\OneDrive\Desktop\MyPKA\Team Inbox\TubeAIR\YYYY\MM\
```

Each intake note includes YAML frontmatter with:

- source URL
- video ID
- language and language code
- manual vs generated caption flag
- translated flag
- capture mode
- transcript source
- timestamp availability
- captured datetime
- `handoff_status: captured_pending_categorisation`
- `categorisair_status: pending`

## What TubeAIR Saves

Fusion247/MyPKA YouTube intake notes are saved here by default:

```text
Team Inbox/TubeAIR/YYYY/MM/
```

Legacy local YouTube notes can still be saved here with `--out-dir`:

```text
out/youtube/
```

Pasted text summaries are saved here:

```text
out/text/
```

Long text summaries include:

- TL;DR
- Executive Summary
- Key Points
- Action Items
- People / Companies / Places mentioned
- Suggested tags
- A source text excerpt

## Reinstall

From this folder:

```powershell
cd "C:\Users\Buggly\OneDrive\Desktop\MyPKA\Deliverables\2026-07-07-tubeair-wp0"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e . --upgrade
```

If PowerShell blocks activation, run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Configure AI

TubeAIR reads API keys from environment variables only. Do not paste keys into code.

Set your OpenAI key in the same PowerShell window where you run TubeAIR:

```powershell
$env:OPENAI_API_KEY="paste-your-openai-key-here"
```

Optional model override:

```powershell
$env:TUBEAIR_OPENAI_MODEL="gpt-4o-mini"
```

If `OPENAI_API_KEY` is missing, or if the API quota is unavailable, TubeAIR saves the Markdown file and includes a clear message explaining that AI summary/enrichment was unavailable.

## Run The CLI

Capture a YouTube transcript into the Fusion247/MyPKA intake folder:

```powershell
tubeair "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

Add optional OpenAI enrichment:

```powershell
tubeair "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --ai-summary
```

List available transcript/caption tracks:

```powershell
tubeair "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --list-tracks
```

Choose another preferred transcript language:

```powershell
tubeair "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --language de
```

Allow translated captions if the preferred language is not exposed:

```powershell
tubeair "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --language en --allow-translation
```

Force manual/clipboard import from a copied transcript text file:

```powershell
tubeair "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --capture-mode clipboard --clipboard-file ".\copied-transcript.txt"
```

Write to a custom Fusion247/MyPKA intake root:

```powershell
tubeair "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --intake-dir "C:\Users\Buggly\OneDrive\Desktop\MyPKA\Team Inbox\TubeAIR"
```

Legacy WP0-WP3 local transcript-only mode:

```powershell
tubeair "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --out-dir "out/youtube" --no-ai
```

Choose another transcript language:

```powershell
tubeair "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --language en
```

## Run The Telegram Bot

First, create a Telegram bot with BotFather and copy the bot token.

In the same PowerShell window where your virtual environment is active:

```powershell
$env:TELEGRAM_BOT_TOKEN="paste-your-telegram-token-here"
$env:OPENAI_API_KEY="paste-your-openai-key-here"
tubeair-telegram
```

Then send either:

```text
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

or paste a long email, note, article, meeting recap, or research extract directly into Telegram.

Transcript-only and no-AI text capture mode:

```powershell
tubeair-telegram --no-ai
```

Choose custom output folders:

```powershell
tubeair-telegram --out-dir "out/youtube" --text-out-dir "out/text"
```

## Test

Run the unit tests:

```powershell
python -m unittest discover -s tests
```

If you have not reinstalled yet, you can run tests from source like this:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests
```

The tests cover:

- YouTube links still route to the YouTube processor.
- Long pasted text routes to the text summariser.
- Short text returns help instructions.
- Text summaries generate Markdown files under `out/text/`.
- Transcript selection prefers manual captions, then generated captions, then translated or original-language fallback.
- Fusion247/MyPKA intake Markdown includes YAML handoff frontmatter.
- Clipboard/manual transcript imports produce capture metadata.

## Outstanding Tasks

There are no known blockers for WP3.

Recommended future improvements:

- WP5: add an explicit audio download plus local/OpenAI Whisper-style transcription fallback for videos with no exposed captions.
- Add CLI support for summarising a local `.txt` or `.md` file.
- Add more intake processors, such as PDFs, web pages, forwarded emails, or Telegram documents.
- Add an optional setting for the long-text threshold if real Telegram usage shows the current value is too high or too low.
- Add a richer error parser for OpenAI quota and billing responses so user-facing messages can be even clearer.

## Notes

Some YouTube videos do not expose transcripts, and some transcripts are blocked by language, region, or video settings. In those cases TubeAIR sends a friendly error instead of creating a transcript file.

AI output is based on the supplied transcript or pasted text. TubeAIR asks the model not to invent facts beyond the source, but important notes should still be reviewed before being treated as final research.
