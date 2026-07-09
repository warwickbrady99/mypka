"""Local read-only web viewer for processed TutAIR Markdown notes."""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


DEFAULT_TUTAIR_ROOT = Path(r"C:\Users\Buggly\OneDrive\Desktop\MyPKA\Team Inbox\TutAIR")
SECTIONS = [
    "Tiny Summary",
    "Key Facts",
    "What This Means",
    "Exam-Style Questions",
    "Flashcards",
    "Next Revision Task",
    "Exam Board Mapping",
]


@dataclass(frozen=True)
class LearningNote:
    id: str
    path: Path
    title: str
    subject: str
    topic: str
    exam_board_status: str
    possible_exam_board: str
    sections: dict[str, str]


def find_processed_notes(root: Path = DEFAULT_TUTAIR_ROOT) -> list[LearningNote]:
    notes: list[LearningNote] = []
    if not root.exists():
        return notes

    for path in sorted(root.glob("**/processed/*.md")):
        notes.append(parse_processed_note(path, root))
    return sorted(notes, key=lambda note: (note.subject.lower(), note.topic.lower(), note.title.lower()))


def parse_processed_note(path: Path, root: Path = DEFAULT_TUTAIR_ROOT) -> LearningNote:
    text = path.read_text(encoding="utf-8")
    metadata = parse_frontmatter(text)
    title = extract_title(text) or f"{metadata.get('subject', 'GCSE')} - {metadata.get('topic', path.stem)}"
    subject = metadata.get("subject", "Unknown")
    topic = metadata.get("topic", path.stem)
    sections = {section: extract_section(text, section) for section in SECTIONS}
    return LearningNote(
        id=note_id(path, root),
        path=path,
        title=title,
        subject=subject,
        topic=topic,
        exam_board_status=metadata.get("exam_board_status", "unconfirmed"),
        possible_exam_board=metadata.get("possible_exam_board", "unknown"),
        sections=sections,
    )


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}

    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line or line.startswith(" ") or line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata


def extract_title(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^## .+$", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def note_id(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def group_notes(notes: list[LearningNote]) -> dict[str, list[LearningNote]]:
    grouped: dict[str, list[LearningNote]] = {}
    for note in notes:
        grouped.setdefault(note.subject, []).append(note)
    return grouped


def render_home(notes: list[LearningNote]) -> str:
    active_note = notes[0] if notes else None
    return render_page(notes, active_note)


def render_note(notes: list[LearningNote], requested_id: str) -> str:
    active_note = next((note for note in notes if note.id == requested_id), None)
    return render_page(notes, active_note)


def render_page(notes: list[LearningNote], active_note: LearningNote | None) -> str:
    nav = render_nav(notes, active_note)
    content = render_note_content(active_note) if active_note else render_empty_state()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TutAIR Revision Viewer</title>
  <style>{CSS}</style>
</head>
<body>
  <header class="topbar">
    <div>
      <p class="eyebrow">TutAIR</p>
      <h1>GCSE revision viewer</h1>
    </div>
    <span class="count">{len(notes)} notes</span>
  </header>
  <main class="layout">
    <aside class="sidebar" aria-label="Processed TutAIR notes">
      {nav}
    </aside>
    <section class="content">
      {content}
    </section>
  </main>
</body>
</html>"""


def render_nav(notes: list[LearningNote], active_note: LearningNote | None) -> str:
    if not notes:
        return '<p class="muted">No processed TutAIR notes found yet.</p>'

    parts: list[str] = []
    for subject, subject_notes in group_notes(notes).items():
        parts.append(f"<h2>{html.escape(subject)}</h2>")
        parts.append('<div class="note-list">')
        for note in subject_notes:
            active = " active" if active_note and note.id == active_note.id else ""
            url = f"/note/{html.escape(note.id)}"
            parts.append(
                f'<a class="note-link{active}" href="{url}">'
                f'<span>{html.escape(note.topic)}</span>'
                f'<small>{html.escape(note.exam_board_status)}</small>'
                "</a>"
            )
        parts.append("</div>")
    return "\n".join(parts)


def render_note_content(note: LearningNote) -> str:
    sections = "\n".join(render_section(name, note.sections.get(name, "")) for name in SECTIONS)
    return f"""
<article class="note">
  <div class="note-heading">
    <div>
      <p class="eyebrow">{html.escape(note.subject)}</p>
      <h2>{html.escape(note.topic)}</h2>
    </div>
    <div class="status">
      <span>{html.escape(note.exam_board_status)}</span>
      <small>{html.escape(note.possible_exam_board)}</small>
    </div>
  </div>
  {sections}
  <details class="source">
    <summary>Source file</summary>
    <code>{html.escape(str(note.path))}</code>
  </details>
</article>
"""


def render_section(title: str, body: str) -> str:
    rendered = render_markdown_block(body) if body else '<p class="muted">Not filled yet.</p>'
    return f"""
<section class="revision-section">
  <h3>{html.escape(title)}</h3>
  {rendered}
</section>
"""


def render_markdown_block(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    list_items: list[str] = []

    def flush_list() -> None:
        if list_items:
            output.append("<ul>" + "".join(list_items) + "</ul>")
            list_items.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_list()
            continue
        if stripped.startswith("- "):
            list_items.append(f"<li>{html.escape(stripped[2:])}</li>")
            continue
        if re.match(r"^\d+\.\s+", stripped):
            list_items.append(f"<li>{html.escape(re.sub(r'^\\d+\\.\\s+', '', stripped))}</li>")
            continue
        flush_list()
        if stripped.startswith("Q:") or stripped.startswith("A:"):
            output.append(f"<p class=\"flashline\">{html.escape(stripped)}</p>")
        else:
            output.append(f"<p>{html.escape(stripped)}</p>")

    flush_list()
    return "\n".join(output)


def render_empty_state() -> str:
    return """
<article class="empty">
  <h2>No processed notes yet</h2>
  <p>Create a TutAIR capture, then run the V2 processor. Processed notes appear here automatically.</p>
  <code>Team Inbox/TutAIR/YYYY/MM/processed/</code>
</article>
"""


class TutairRequestHandler(BaseHTTPRequestHandler):
    tutair_root = DEFAULT_TUTAIR_ROOT

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        notes = find_processed_notes(self.tutair_root)
        if parsed.path == "/":
            self.respond_html(render_home(notes))
            return
        if parsed.path.startswith("/note/"):
            requested_id = unquote(parsed.path.removeprefix("/note/"))
            self.respond_html(render_note(notes, requested_id))
            return
        if parsed.path == "/api/notes":
            payload = [
                {
                    "id": note.id,
                    "title": note.title,
                    "subject": note.subject,
                    "topic": note.topic,
                    "exam_board_status": note.exam_board_status,
                    "possible_exam_board": note.possible_exam_board,
                }
                for note in notes
            ]
            self.respond_json(payload)
            return
        self.send_error(404)

    def respond_html(self, body: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def respond_json(self, payload: object) -> None:
        encoded = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: object) -> None:
        return


def run_server(host: str, port: int, root: Path) -> None:
    handler = type("ConfiguredTutairRequestHandler", (TutairRequestHandler,), {"tutair_root": root})
    server = ThreadingHTTPServer((host, port), handler)
    print(f"TutAIR viewer running at http://{host}:{port}")
    print(f"Reading processed notes from: {root}")
    server.serve_forever()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the local TutAIR revision viewer.")
    parser.add_argument("--root", type=Path, default=DEFAULT_TUTAIR_ROOT)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    run_server(args.host, args.port, args.root)
    return 0


CSS = """
:root {
  color-scheme: light;
  --bg: #f7f8fa;
  --panel: #ffffff;
  --ink: #18202a;
  --muted: #667085;
  --line: #d8dee8;
  --accent: #176b87;
  --accent-ink: #ffffff;
  --soft: #e9f5f8;
  --focus: #9b5de5;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--ink);
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.5;
}

.topbar {
  align-items: center;
  background: var(--panel);
  border-bottom: 1px solid var(--line);
  display: flex;
  justify-content: space-between;
  min-height: 84px;
  padding: 18px 24px;
}

.eyebrow {
  color: var(--accent);
  font-size: 0.78rem;
  font-weight: 700;
  margin: 0 0 4px;
  text-transform: uppercase;
}

h1, h2, h3, p { margin-top: 0; }

h1 { font-size: 1.6rem; margin-bottom: 0; }
h2 { font-size: 1.25rem; margin-bottom: 12px; }
h3 { font-size: 1rem; margin-bottom: 8px; }

.count {
  background: var(--soft);
  border: 1px solid var(--line);
  border-radius: 999px;
  color: var(--accent);
  font-weight: 700;
  padding: 6px 12px;
}

.layout {
  display: grid;
  grid-template-columns: minmax(220px, 300px) 1fr;
  min-height: calc(100vh - 84px);
}

.sidebar {
  background: var(--panel);
  border-right: 1px solid var(--line);
  padding: 18px;
}

.note-list {
  display: grid;
  gap: 8px;
  margin-bottom: 20px;
}

.note-link {
  border: 1px solid var(--line);
  border-radius: 8px;
  color: var(--ink);
  display: grid;
  gap: 2px;
  padding: 10px;
  text-decoration: none;
}

.note-link:focus-visible {
  outline: 3px solid var(--focus);
  outline-offset: 2px;
}

.note-link.active,
.note-link:hover {
  background: var(--soft);
  border-color: var(--accent);
}

.note-link small,
.muted {
  color: var(--muted);
}

.content {
  padding: 24px;
}

.note,
.empty {
  margin: 0 auto;
  max-width: 980px;
}

.note-heading {
  align-items: start;
  display: flex;
  gap: 16px;
  justify-content: space-between;
  margin-bottom: 16px;
}

.status {
  background: var(--ink);
  border-radius: 8px;
  color: var(--accent-ink);
  display: grid;
  min-width: 150px;
  padding: 10px 12px;
  text-align: right;
}

.status small {
  opacity: 0.75;
}

.revision-section,
.source,
.empty {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  margin-bottom: 12px;
  padding: 16px;
}

.revision-section ul {
  margin-bottom: 0;
  padding-left: 20px;
}

.flashline {
  margin-bottom: 6px;
}

code {
  background: #eef1f5;
  border-radius: 6px;
  display: inline-block;
  max-width: 100%;
  overflow-wrap: anywhere;
  padding: 4px 6px;
}

@media (max-width: 760px) {
  .topbar {
    align-items: flex-start;
    display: grid;
    gap: 10px;
  }

  .layout {
    display: block;
  }

  .sidebar {
    border-bottom: 1px solid var(--line);
    border-right: 0;
  }

  .content {
    padding: 16px;
  }

  .note-heading {
    display: grid;
  }

  .status {
    text-align: left;
  }
}
"""


if __name__ == "__main__":
    raise SystemExit(main())
