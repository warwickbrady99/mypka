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
VIEWER_UI_VERSION = "approved-dashboard-2026-07-09"
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
    subject_nav = render_subject_nav(notes, active_note)
    topic_nav = render_topic_nav(notes, active_note)
    content = render_note_content(active_note) if active_note else render_empty_state()
    topic_label = html.escape(active_note.topic if active_note else "Choose a topic")
    subject_label = html.escape(active_note.subject if active_note else "TutAIR")
    note_payload = render_note_payload(active_note)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TutAIR Revision Viewer</title>
  <meta name="tutair-ui-version" content="{VIEWER_UI_VERSION}">
  <style>{CSS}</style>
</head>
<body>
  <div class="app-shell">
    <aside class="side-rail" aria-label="TutAIR navigation">
      <a class="brand" href="/" aria-label="TutAIR home">
        <span class="brand-mark">TA</span>
        <span>
          <strong>Tut<span>AIR</span></strong>
          <small>Focus. Understand. Remember.</small>
        </span>
      </a>
      <section class="rail-section">
        <h2>Subjects</h2>
        {subject_nav}
        <button class="rail-button placeholder" type="button" disabled>+ Add Subject</button>
      </section>
      <section class="rail-section plan">
        <h2>Today's Plan</h2>
        <label><input type="checkbox" checked disabled> 1 topic review</label>
        <label><input type="checkbox" checked disabled> 5 flashcards</label>
        <label><input type="checkbox" disabled> 1 quiz</label>
      </section>
      <section class="tip-card">
        <h2>Tip of the day</h2>
        <p>Try explaining this topic out loud like you're teaching a friend.</p>
      </section>
      <button class="break-button" type="button" disabled>Take a Break</button>
    </aside>
    <main class="workspace">
      <header class="hero">
        <div>
          <h1>GCSE Revision Viewer</h1>
          <p>You've got this! Small steps, big progress.</p>
        </div>
        <div class="hero-actions" aria-label="Display controls">
          <button type="button" data-action="focus">Focus Mode</button>
          <button type="button" data-action="coming-soon" data-feature="Colour Theme">Colour Theme</button>
          <button class="sun" type="button" disabled aria-label="Brightness"></button>
          <div class="streak" aria-label="Study streak">
            <strong>Keep Going!</strong>
            <span>3-day streak</span>
          </div>
        </div>
      </header>
      <nav class="crumb-bar" aria-label="Current topic">
        <div class="crumbs">
          <span>{subject_label}</span>
          <span aria-hidden="true">/</span>
          <span>Cell biology</span>
          <span aria-hidden="true">/</span>
          <strong>{topic_label}</strong>
        </div>
        <div class="toolbar">
          <button class="save" type="button" data-action="save-topic">Save Topic</button>
          <button class="export" type="button" data-action="coming-soon" data-feature="Export">Export</button>
          <button class="review" type="button" data-action="mark-reviewed">Mark as Reviewed</button>
        </div>
      </nav>
      <div class="study-grid">
        <aside class="topic-panel" aria-label="Topics">
          <h2>Topics</h2>
          {topic_nav}
          <div class="help-card">
            <strong>Need Help?</strong>
            <p>Stuck on a topic? Ask your study buddy for help.</p>
            <button type="button" disabled>Ask TutAIR</button>
          </div>
        </aside>
        <section class="content" aria-label="Revision note">
          {content}
        </section>
        <aside class="action-panel" aria-label="Study tools">
          {render_action_panel(active_note)}
        </aside>
      </div>
      <footer class="encouragement" aria-label="Encouragement">
        <span>You're learning!</span>
        <span>One step at a time</span>
        <span>Progress over perfection</span>
        <span>Celebrate tiny wins</span>
        <button type="button" disabled>I'm proud of you!</button>
      </footer>
    </main>
  </div>
  <div class="toast" role="status" aria-live="polite" hidden></div>
  <script id="note-data" type="application/json">{note_payload}</script>
  <script>{JS}</script>
</body>
</html>"""


def render_note_payload(note: LearningNote | None) -> str:
    if not note:
        return "{}"
    payload = {
        "id": note.id,
        "title": note.title,
        "subject": note.subject,
        "topic": note.topic,
        "exam_board_status": note.exam_board_status,
        "possible_exam_board": note.possible_exam_board,
        "sections": note.sections,
        "flashcards": parse_flashcards(note.sections.get("Flashcards", "")),
        "questions": parse_questions(note.sections.get("Exam-Style Questions", "")),
    }
    return json.dumps(payload).replace("</", "<\\/")


def parse_flashcards(markdown: str) -> list[dict[str, str]]:
    cards: list[dict[str, str]] = []
    current_question = ""
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("Q:"):
            current_question = stripped.removeprefix("Q:").strip()
        elif stripped.startswith("A:") and current_question:
            cards.append({"question": current_question, "answer": stripped.removeprefix("A:").strip()})
            current_question = ""
    return cards


def parse_questions(markdown: str) -> list[dict[str, str]]:
    questions: list[dict[str, str]] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if match:
            question = match.group(1).strip()
            questions.append({"question": question, "answer": "Use the note above to answer in your own words."})
    return questions


def render_subject_nav(notes: list[LearningNote], active_note: LearningNote | None) -> str:
    if not notes:
        return '<p class="rail-empty">No subjects yet</p>'

    parts: list[str] = []
    for subject in group_notes(notes):
        first_note = group_notes(notes)[subject][0]
        active = " active" if active_note and subject == active_note.subject else ""
        icon = subject_icon(subject)
        parts.append(
            f'<a class="subject-link{active}" href="/note/{html.escape(first_note.id)}">'
            f'<span class="subject-icon">{icon}</span>'
            f'<span>{html.escape(subject)}</span>'
            "</a>"
        )
    for subject in ["Maths", "English", "History", "Geography"]:
        if subject not in group_notes(notes):
            parts.append(
                f'<button class="subject-link ghost" type="button" disabled>'
                f'<span class="subject-icon">{subject_icon(subject)}</span>'
                f'<span>{html.escape(subject)}</span>'
                "</button>"
            )
    return "\n".join(parts)


def render_topic_nav(notes: list[LearningNote], active_note: LearningNote | None) -> str:
    if not notes:
        return '<p class="muted">No processed TutAIR notes found yet.</p>'

    active_subject = active_note.subject if active_note else notes[0].subject
    visible_notes = group_notes(notes).get(active_subject, notes)
    parts: list[str] = ['<div class="topic-list">']
    for index, note in enumerate(visible_notes):
        active = " active" if active_note and note.id == active_note.id else ""
        icon = ["◎", "◉", "✣", "◆", "⌕"][index % 5]
        parts.append(
            f'<a class="topic-link{active}" data-note-id="{html.escape(note.id)}" href="/note/{html.escape(note.id)}">'
            f'<span class="topic-icon">{icon}</span>'
            f'<span><strong>{html.escape(note.topic)}</strong>'
            f'<small>{html.escape(note.exam_board_status)}</small></span>'
            f'<b aria-hidden="true">›</b>'
            "</a>"
        )
    placeholders = ["Cell structure", "Specialised cells", "Plant cells", "Microscopy"]
    for index, topic in enumerate(placeholders):
        if topic.lower() not in {note.topic.lower() for note in visible_notes}:
            icon = ["◉", "✣", "◆", "⌕"][index % 4]
            parts.append(
                f'<button class="topic-link ghost" type="button" disabled>'
                f'<span class="topic-icon">{icon}</span>'
                f'<span><strong>{html.escape(topic)}</strong><small>unconfirmed</small></span>'
                "</button>"
            )
    parts.append("</div>")
    return "\n".join(parts)


def subject_icon(subject: str) -> str:
    icons = {
        "science": "S",
        "maths": "M",
        "english": "E",
        "history": "H",
        "geography": "G",
        "computer science": "CS",
        "business enterprise": "B",
        "construction": "C",
    }
    return icons.get(subject.lower(), subject[:1].upper())


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
      <span>Status: {html.escape(note.exam_board_status)}</span>
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
    section_class = slugify_section(title)
    return f"""
<section class="revision-section {section_class}">
  <button class="collapse-dot" type="button" disabled aria-label="{html.escape(title)} is expanded"></button>
  <h3>{section_icon(title)} {html.escape(title)}</h3>
  {rendered}
</section>
"""


def slugify_section(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def section_icon(title: str) -> str:
    icons = {
        "Tiny Summary": "TS",
        "Key Facts": "KF",
        "What This Means": "WM",
        "Exam-Style Questions": "Q",
        "Flashcards": "FC",
        "Next Revision Task": "NR",
        "Exam Board Mapping": "EB",
    }
    return f'<span class="section-icon">{icons.get(title, "N")}</span>'


def render_action_panel(note: LearningNote | None) -> str:
    status = html.escape(note.exam_board_status if note else "none")
    return f"""
<section class="side-card quick-actions">
  <h2>Quick Actions</h2>
  <button class="flashcards" type="button" data-action="flashcards">Flashcards</button>
  <button class="quiz" type="button" data-action="quiz">Quiz Me</button>
  <button class="mindmap" type="button" data-action="coming-soon" data-feature="Mind Map">Mind Map</button>
  <button class="notes" type="button" data-action="notes">Notes</button>
  <button class="read" type="button" data-action="read-aloud">Read Aloud</button>
</section>
<section class="side-card timer">
  <h2>Focus Timer</h2>
  <div><strong>25:00</strong><button type="button" disabled aria-label="Start focus timer">▶</button></div>
  <p>Focus time <a href="#" aria-disabled="true">Skip Break</a></p>
</section>
<section class="side-card progress">
  <h2>Progress</h2>
  <div class="progress-row">
    <span>This Topic</span>
    <strong>0%</strong>
  </div>
  <label>Overall Progress <span>12%</span></label>
  <div class="bar"><span></span></div>
  <p class="muted">Mapping status: {status}</p>
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
    print(f"UI version: {VIEWER_UI_VERSION}")
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


JS = r"""
(function () {
  const dataEl = document.getElementById("note-data");
  const note = dataEl ? JSON.parse(dataEl.textContent || "{}") : {};
  const app = document.querySelector(".app-shell");
  const content = document.querySelector(".content");
  const toast = document.querySelector(".toast");
  const storagePrefix = "tutair.viewer.";
  let flashIndex = 0;
  let flashShowingAnswer = false;
  let activeUtterance = null;

  function getSet(key) {
    try {
      return new Set(JSON.parse(localStorage.getItem(storagePrefix + key) || "[]"));
    } catch {
      return new Set();
    }
  }

  function saveSet(key, values) {
    localStorage.setItem(storagePrefix + key, JSON.stringify(Array.from(values)));
  }

  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.hidden = false;
    window.clearTimeout(showToast.timer);
    showToast.timer = window.setTimeout(() => {
      toast.hidden = true;
    }, 2600);
  }

  function setMode(mode) {
    if (!content) return;
    document.body.dataset.mode = mode;
    if (mode === "notes") {
      content.querySelectorAll(".practice-view").forEach((el) => el.remove());
      const noteEl = content.querySelector(".note");
      if (noteEl) noteEl.hidden = false;
      return;
    }
    const noteEl = content.querySelector(".note");
    if (noteEl) noteEl.hidden = true;
    content.querySelectorAll(".practice-view").forEach((el) => el.remove());
  }

  function escapeText(value) {
    const span = document.createElement("span");
    span.textContent = value || "";
    return span.innerHTML;
  }

  function renderFlashcards() {
    const cards = note.flashcards || [];
    if (!cards.length) {
      showToast("Coming Soon: this note has no flashcards yet.");
      return;
    }
    setMode("flashcards");
    flashIndex = Math.min(flashIndex, cards.length - 1);
    flashShowingAnswer = false;
    const view = document.createElement("article");
    view.className = "practice-view flashcard-practice";
    view.setAttribute("aria-live", "polite");
    view.innerHTML = flashcardMarkup(cards);
    content.appendChild(view);
  }

  function flashcardMarkup(cards) {
    const card = cards[flashIndex];
    const visibleText = flashShowingAnswer ? card.answer : card.question;
    return `
      <p class="eyebrow">${escapeText(note.subject || "TutAIR")}</p>
      <h2>Flashcards</h2>
      <div class="practice-card" tabindex="0">
        <span>Card ${flashIndex + 1} of ${cards.length}</span>
        <strong>${escapeText(flashShowingAnswer ? "Answer" : "Question")}</strong>
        <p>${escapeText(visibleText)}</p>
      </div>
      <div class="practice-controls">
        <button type="button" data-practice="prev">Previous</button>
        <button type="button" data-practice="flip">${flashShowingAnswer ? "Show Question" : "Flip Card"}</button>
        <button type="button" data-practice="next">Next</button>
        <button type="button" data-action="notes">Back to Notes</button>
      </div>`;
  }

  function rerenderFlashcards() {
    const view = content.querySelector(".flashcard-practice");
    if (view) view.innerHTML = flashcardMarkup(note.flashcards || []);
  }

  function renderQuiz() {
    const questions = note.questions || [];
    if (!questions.length) {
      showToast("Coming Soon: this note has no quiz questions yet.");
      return;
    }
    setMode("quiz");
    const view = document.createElement("article");
    view.className = "practice-view quiz-practice";
    view.innerHTML = `
      <p class="eyebrow">${escapeText(note.subject || "TutAIR")}</p>
      <h2>Quiz Me</h2>
      <form class="quiz-form">
        ${questions.map((item, index) => `
          <section class="quiz-item">
            <label for="quiz-${index}"><strong>${index + 1}. ${escapeText(item.question)}</strong></label>
            <textarea id="quiz-${index}" rows="3" placeholder="Try your answer first"></textarea>
            <button type="button" data-reveal="${index}">Reveal</button>
            <p class="quiz-answer" id="answer-${index}" hidden>${escapeText(item.answer)}</p>
          </section>
        `).join("")}
      </form>
      <div class="practice-controls">
        <button type="button" data-action="notes">Back to Notes</button>
      </div>`;
    content.appendChild(view);
  }

  function readAloud() {
    if (!("speechSynthesis" in window)) {
      showToast("Coming Soon: read aloud is not available in this browser.");
      return;
    }
    setMode("read");
    const text = Array.from(document.querySelectorAll(".note .revision-section"))
      .map((section) => section.innerText.trim())
      .filter(Boolean)
      .join("\n\n");
    if (!text) {
      showToast("Nothing to read yet.");
      return;
    }
    const view = document.createElement("article");
    view.className = "practice-view read-practice";
    view.innerHTML = `
      <p class="eyebrow">${escapeText(note.subject || "TutAIR")}</p>
      <h2>Read Aloud</h2>
      <p>The browser will read the current revision note aloud.</p>
      <div class="practice-controls">
        <button type="button" data-speech="play">Play</button>
        <button type="button" data-speech="pause">Pause</button>
        <button type="button" data-speech="stop">Stop</button>
        <button type="button" data-action="notes">Back to Notes</button>
      </div>`;
    content.appendChild(view);
    activeUtterance = new SpeechSynthesisUtterance(text);
    activeUtterance.rate = 0.92;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(activeUtterance);
  }

  function stopSpeech() {
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    activeUtterance = null;
  }

  function toggleFocus() {
    const enabled = document.body.classList.toggle("focus-mode");
    const button = document.querySelector('[data-action="focus"]');
    if (button) button.textContent = enabled ? "Exit Focus" : "Focus Mode";
    showToast(enabled ? "Focus Mode on" : "Focus Mode off");
  }

  function toggleReviewed() {
    if (!note.id) return;
    const reviewed = getSet("reviewed");
    if (reviewed.has(note.id)) {
      reviewed.delete(note.id);
    } else {
      reviewed.add(note.id);
    }
    saveSet("reviewed", reviewed);
    applyLocalState();
  }

  function toggleFavourite() {
    if (!note.id) return;
    const favourites = getSet("favourites");
    if (favourites.has(note.id)) {
      favourites.delete(note.id);
      showToast("Removed from favourites");
    } else {
      favourites.add(note.id);
      showToast("Saved to favourites");
    }
    saveSet("favourites", favourites);
    applyLocalState();
  }

  function applyLocalState() {
    if (!note.id) return;
    const reviewed = getSet("reviewed");
    const favourites = getSet("favourites");
    document.body.classList.toggle("is-reviewed", reviewed.has(note.id));
    document.body.classList.toggle("is-favourite", favourites.has(note.id));
    document.querySelectorAll(`[data-note-id="${CSS.escape(note.id)}"]`).forEach((el) => {
      el.classList.toggle("reviewed", reviewed.has(note.id));
      el.classList.toggle("favourite", favourites.has(note.id));
    });
    const reviewButton = document.querySelector('[data-action="mark-reviewed"]');
    if (reviewButton) reviewButton.textContent = reviewed.has(note.id) ? "Reviewed" : "Mark as Reviewed";
    const saveButton = document.querySelector('[data-action="save-topic"]');
    if (saveButton) saveButton.textContent = favourites.has(note.id) ? "Saved Topic" : "Save Topic";
    const status = document.querySelector(".status");
    if (status && reviewed.has(note.id) && !status.querySelector(".reviewed-pill")) {
      status.insertAdjacentHTML("beforeend", '<small class="reviewed-pill">reviewed locally</small>');
    }
    renderFavourites(favourites);
  }

  function renderFavourites(favourites) {
    const rail = document.querySelector(".side-rail");
    if (!rail) return;
    let box = rail.querySelector(".favourites-section");
    if (!box) {
      box = document.createElement("section");
      box.className = "rail-section favourites-section";
      const subjects = rail.querySelector(".rail-section");
      if (subjects) subjects.insertAdjacentElement("afterend", box);
    }
    if (!favourites.size) {
      box.innerHTML = '<h2>Favourites</h2><p class="rail-empty">No saved topics yet</p>';
      return;
    }
    const isCurrent = note.id && favourites.has(note.id);
    box.innerHTML = `
      <h2>Favourites</h2>
      ${isCurrent ? `<a class="subject-link active" href="/note/${encodeURIComponent(note.id)}"><span class="subject-icon">*</span><span>${escapeText(note.topic || "Saved topic")}</span></a>` : '<p class="rail-empty">Saved topics appear when opened</p>'}
    `;
  }

  document.addEventListener("click", (event) => {
    const target = event.target.closest("button, a");
    if (!target) return;
    const action = target.dataset.action;
    if (action === "flashcards") renderFlashcards();
    if (action === "quiz") renderQuiz();
    if (action === "notes") {
      stopSpeech();
      setMode("notes");
    }
    if (action === "read-aloud") readAloud();
    if (action === "focus") toggleFocus();
    if (action === "mark-reviewed") toggleReviewed();
    if (action === "save-topic") toggleFavourite();
    if (action === "coming-soon") showToast(`Coming Soon: ${target.dataset.feature || "This feature"}`);

    const practice = target.dataset.practice;
    if (practice === "prev") {
      flashIndex = Math.max(0, flashIndex - 1);
      flashShowingAnswer = false;
      rerenderFlashcards();
    }
    if (practice === "next") {
      flashIndex = Math.min((note.flashcards || []).length - 1, flashIndex + 1);
      flashShowingAnswer = false;
      rerenderFlashcards();
    }
    if (practice === "flip") {
      flashShowingAnswer = !flashShowingAnswer;
      rerenderFlashcards();
    }

    const reveal = target.dataset.reveal;
    if (reveal !== undefined) {
      const answer = document.getElementById(`answer-${reveal}`);
      if (answer) answer.hidden = false;
    }

    const speech = target.dataset.speech;
    if (speech === "play") {
      if (window.speechSynthesis.paused) window.speechSynthesis.resume();
      else readAloud();
    }
    if (speech === "pause" && "speechSynthesis" in window) window.speechSynthesis.pause();
    if (speech === "stop") stopSpeech();
  });

  document.addEventListener("input", (event) => {
    if (event.target.closest(".quiz-item")) {
      const answer = event.target.closest(".quiz-item").querySelector(".quiz-answer");
      if (answer && event.target.value.trim().length > 0) answer.hidden = false;
    }
  });

  applyLocalState();
})();
"""


CSS = """
:root {
  color-scheme: light;
  --nav: #121239;
  --nav-2: #191446;
  --ink: #171442;
  --muted: #6d6b8a;
  --panel: #ffffff;
  --line: #e4dcf5;
  --aqua: #18c7bd;
  --aqua-dark: #07959a;
  --purple: #a74ee8;
  --blue: #2d91e9;
  --green: #18a84f;
  --yellow: #ffcc29;
  --pink: #ed4f9b;
  --orange: #e19a00;
  --shadow: 0 14px 34px rgba(37, 29, 78, 0.12);
  --soft-shadow: 0 8px 22px rgba(24, 199, 189, 0.12);
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background:
    radial-gradient(circle at 60% 10%, rgba(167, 78, 232, 0.08), transparent 32%),
    linear-gradient(120deg, #fbfdff 0%, #fff8fc 48%, #f7fffd 100%);
  color: var(--ink);
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  line-height: 1.5;
}

button,
a {
  font: inherit;
}

button:focus-visible,
a:focus-visible {
  outline: 4px solid rgba(24, 199, 189, 0.45);
  outline-offset: 3px;
}

button:disabled {
  cursor: not-allowed;
}

.app-shell {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  min-height: 100vh;
}

.side-rail {
  background: linear-gradient(180deg, #15123f 0%, #0c1031 100%);
  color: #f7f4ff;
  display: flex;
  flex-direction: column;
  gap: 28px;
  padding: 30px 24px;
  position: sticky;
  top: 0;
  height: 100vh;
}

.brand {
  align-items: center;
  color: #ffffff;
  display: flex;
  gap: 12px;
  text-decoration: none;
}

.brand-mark,
.subject-icon,
.topic-icon,
.section-icon {
  align-items: center;
  display: inline-flex;
  justify-content: center;
}

.brand-mark {
  background: linear-gradient(135deg, #d9a6ff, #55efe6);
  border-radius: 14px;
  box-shadow: 0 10px 26px rgba(85, 239, 230, 0.22);
  color: #14123d;
  font-weight: 900;
  height: 42px;
  width: 42px;
}

.brand strong {
  display: block;
  font-size: 2.15rem;
  letter-spacing: 0;
  line-height: 1;
}

.brand strong span { color: #35e5dc; }
.brand small { color: #c6c3e3; display: block; margin-top: 7px; }

.rail-section h2,
.side-card h2,
.topic-panel h2 {
  color: var(--aqua);
  font-size: 0.95rem;
  letter-spacing: 0;
  margin: 0 0 14px;
  text-transform: uppercase;
}

.rail-section {
  display: grid;
  gap: 10px;
}

.subject-link,
.rail-button,
.break-button {
  align-items: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(98, 67, 177, 0.74);
  border-radius: 8px;
  color: #ffffff;
  display: flex;
  gap: 14px;
  min-height: 46px;
  padding: 11px 14px;
  text-decoration: none;
  width: 100%;
}

.subject-link.active {
  background: linear-gradient(135deg, #16c9bd, #178f99);
  border-color: rgba(55, 238, 226, 0.74);
  box-shadow: var(--soft-shadow);
  font-weight: 800;
}

.subject-link.ghost,
.rail-button.placeholder {
  color: #e8e3ff;
}

.subject-icon {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 7px;
  color: #61f1e8;
  font-weight: 900;
  height: 24px;
  min-width: 24px;
}

.plan label {
  align-items: center;
  color: #ffffff;
  display: flex;
  gap: 10px;
  min-height: 26px;
}

.plan input {
  accent-color: var(--aqua);
  height: 20px;
  width: 20px;
}

.tip-card {
  background: linear-gradient(145deg, rgba(24, 199, 189, 0.12), rgba(85, 58, 159, 0.34));
  border: 1px solid rgba(24, 199, 189, 0.20);
  border-radius: 8px;
  color: #ffffff;
  padding: 18px;
}

.tip-card h2 {
  color: var(--yellow);
  font-size: 1rem;
  margin: 0 0 10px;
}

.tip-card p,
.hero p,
.side-card p,
.help-card p {
  margin: 0;
}

.break-button {
  background: linear-gradient(135deg, #5d2fa4, #6b33bd);
  border: 0;
  font-weight: 800;
  justify-content: center;
  margin-top: auto;
}

.workspace {
  min-width: 0;
  padding: 24px 32px 12px;
}

.hero,
.crumb-bar,
.encouragement {
  align-items: center;
  display: flex;
  justify-content: space-between;
}

.hero {
  min-height: 84px;
}

.hero h1 {
  color: #161344;
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1;
  margin: 0 0 8px;
  text-transform: uppercase;
}

.hero p {
  color: #a24ef0;
  font-size: 1.1rem;
  font-weight: 800;
}

.hero-actions {
  align-items: center;
  display: flex;
  gap: 14px;
}

.hero-actions button,
.streak,
.toolbar button {
  border-radius: 8px;
  border: 1px solid var(--line);
  box-shadow: 0 6px 16px rgba(28, 24, 72, 0.08);
  font-weight: 800;
  min-height: 42px;
  padding: 0 18px;
}

.hero-actions button {
  background: #ffffff;
  color: var(--aqua-dark);
}

.hero-actions button:nth-child(2) {
  color: #7358d9;
}

.hero-actions .sun {
  background: #ffffff;
  border-radius: 50%;
  min-width: 42px;
  padding: 0;
}

.hero-actions .sun::before {
  color: var(--yellow);
  content: "☼";
  font-size: 1.35rem;
}

.streak {
  align-items: center;
  background: #f1fff6;
  border-color: #c9efd7;
  color: #188f39;
  display: grid;
  min-width: 174px;
  padding: 10px 18px;
}

.crumb-bar {
  background: rgba(255, 255, 255, 0.70);
  border: 1px solid #cbeeed;
  border-radius: 8px;
  box-shadow: var(--shadow);
  gap: 16px;
  margin: 14px 0 22px;
  padding: 20px;
}

.crumbs {
  align-items: center;
  background: #f8ffff;
  border: 1px solid #d9eeee;
  border-radius: 7px;
  color: #26324f;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 10px 14px;
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.toolbar .save { background: var(--yellow); border-color: #f3be00; color: #1b1840; }
.toolbar .export { background: #e9f4ff; border-color: #9ac8f6; color: #162040; }
.toolbar .review { background: #0b9342; border-color: #0b9342; color: #ffffff; }

.study-grid {
  display: grid;
  grid-template-columns: 300px minmax(440px, 1fr) 240px;
  gap: 24px;
}

.topic-panel,
.side-card {
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: 0 10px 28px rgba(27, 22, 68, 0.08);
  padding: 18px;
}

.topic-list {
  display: grid;
  gap: 14px;
}

.topic-link {
  align-items: center;
  background: #ffffff;
  border: 1px solid #e7e5ee;
  border-radius: 8px;
  color: var(--ink);
  display: grid;
  gap: 12px;
  grid-template-columns: 34px 1fr auto;
  min-height: 64px;
  padding: 12px;
  text-align: left;
  text-decoration: none;
  width: 100%;
}

.topic-link.active {
  background: linear-gradient(135deg, #0fa8a6, #17a3a6);
  border-color: #0fa8a6;
  color: #ffffff;
  font-weight: 800;
}

.topic-link.ghost {
  color: var(--ink);
}

.topic-link small {
  color: inherit;
  display: block;
  font-weight: 500;
  opacity: 0.76;
}

.topic-icon {
  background: #f5f7ff;
  border-radius: 50%;
  color: var(--purple);
  font-weight: 900;
  height: 34px;
  width: 34px;
}

.help-card {
  background: #f2ffff;
  border: 1px solid #c6eeee;
  border-radius: 8px;
  color: #26405e;
  margin-top: 56px;
  padding: 18px;
}

.help-card strong {
  color: var(--aqua-dark);
  display: block;
  font-size: 1.05rem;
  margin-bottom: 8px;
}

.help-card button {
  background: #f9ffff;
  border: 1px solid #97d7da;
  border-radius: 7px;
  color: var(--aqua-dark);
  font-weight: 800;
  margin-top: 14px;
  min-height: 42px;
  width: 100%;
}

.content {
  min-width: 0;
}

.note-heading {
  align-items: flex-start;
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}

.eyebrow {
  color: var(--aqua-dark);
  font-weight: 900;
  letter-spacing: 0;
  margin: 0 0 8px;
  text-transform: uppercase;
}

.note-heading h2 {
  color: var(--ink);
  font-size: clamp(2.1rem, 4vw, 3rem);
  line-height: 1;
  margin: 0;
}

.status {
  background: #11194a;
  border: 2px solid #08b1ab;
  border-radius: 7px;
  color: #ffffff;
  display: grid;
  min-width: 178px;
  padding: 12px;
  text-align: right;
}

.status span {
  font-weight: 900;
}

.status small {
  font-weight: 800;
  opacity: 0.9;
}

.revision-section {
  background: rgba(255, 255, 255, 0.70);
  border: 2px solid #9dd2ff;
  border-radius: 8px;
  margin-bottom: 12px;
  padding: 16px 48px 16px 18px;
  position: relative;
}

.revision-section h3 {
  align-items: center;
  color: var(--blue);
  display: flex;
  gap: 9px;
  font-size: 1.1rem;
  margin: 0 0 10px;
}

.revision-section p,
.revision-section li {
  color: #161b34;
  font-size: 0.95rem;
}

.revision-section p:last-child,
.revision-section ul:last-child {
  margin-bottom: 0;
}

.revision-section.key-facts {
  background: #f3fff6;
  border-color: #7ed497;
}

.revision-section.key-facts h3 { color: #219645; }

.revision-section.what-this-means {
  background: #fffcf1;
  border-color: #f4c647;
}

.revision-section.what-this-means h3 { color: var(--orange); }

.revision-section.exam-style-questions {
  background: #fbf5ff;
  border-color: #bc78ec;
}

.revision-section.exam-style-questions h3 { color: var(--purple); }

.revision-section.flashcards {
  background: #fff5fb;
  border-color: #ef8fc0;
}

.revision-section.flashcards h3 { color: var(--pink); }

.revision-section.next-revision-task,
.revision-section.exam-board-mapping {
  background: #f7ffff;
  border-color: #7bd8d5;
}

.revision-section.next-revision-task h3,
.revision-section.exam-board-mapping h3 {
  color: var(--aqua-dark);
}

.section-icon {
  border-radius: 50%;
  color: currentColor;
  font-size: 0.78rem;
  font-weight: 900;
  min-height: 22px;
  min-width: 22px;
}

.collapse-dot {
  background: var(--blue);
  border: 0;
  border-radius: 50%;
  height: 26px;
  position: absolute;
  right: 16px;
  top: 16px;
  width: 26px;
}

.collapse-dot::after {
  color: #ffffff;
  content: "⌄";
  font-weight: 900;
}

.key-facts .collapse-dot { background: var(--green); }
.what-this-means .collapse-dot { background: #f4b400; }
.exam-style-questions .collapse-dot { background: var(--purple); }
.flashcards .collapse-dot { background: var(--pink); }

.revision-section ul {
  margin: 0;
  padding-left: 24px;
}

.flashline {
  display: inline-block;
  margin: 0 28px 7px 0;
}

.source {
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid var(--line);
  border-radius: 8px;
  color: var(--muted);
  margin-top: 12px;
  padding: 14px;
}

.side-card {
  margin-bottom: 20px;
}

.quick-actions {
  display: grid;
  gap: 10px;
}

.quick-actions button {
  border-radius: 6px;
  font-weight: 900;
  min-height: 38px;
}

.quick-actions .flashcards { background: #fcf3ff; border: 1px solid #d997f6; color: var(--purple); }
.quick-actions .quiz { background: #fff2f6; border: 1px solid #f3a3c4; color: var(--pink); }
.quick-actions .mindmap { background: #eff8ff; border: 1px solid #a3d1f7; color: var(--blue); }
.quick-actions .notes { background: #fff9df; border: 1px solid #f0c54c; color: var(--orange); }
.quick-actions .read { background: #edfff1; border: 1px solid #a4dfa9; color: var(--green); }

.timer strong {
  color: #b163ef;
  font-size: 2.35rem;
}

.timer div {
  align-items: center;
  display: flex;
  justify-content: space-between;
}

.timer button {
  background: linear-gradient(135deg, #c64be7, #834ee9);
  border: 0;
  border-radius: 50%;
  color: #ffffff;
  height: 52px;
  width: 52px;
}

.timer a {
  color: var(--ink);
  font-size: 0.8rem;
}

.progress-row {
  align-items: center;
  display: flex;
  justify-content: space-between;
}

.progress-row strong {
  align-items: center;
  border: 7px solid #ffd5e6;
  border-top-color: #f490bd;
  border-radius: 50%;
  color: var(--pink);
  display: flex;
  height: 78px;
  justify-content: center;
  width: 78px;
}

.progress label {
  color: var(--aqua-dark);
  display: flex;
  font-size: 0.9rem;
  justify-content: space-between;
  margin-top: 14px;
}

.bar {
  background: #eef0ef;
  border-radius: 999px;
  height: 10px;
  margin-top: 6px;
  overflow: hidden;
}

.bar span {
  background: var(--aqua);
  display: block;
  height: 100%;
  width: 12%;
}

.empty {
  background: rgba(255, 255, 255, 0.78);
  border: 2px dashed #9ddbd8;
  border-radius: 8px;
  padding: 30px;
}

.muted,
.rail-empty {
  color: var(--muted);
}

code {
  background: #f1f2f8;
  border-radius: 6px;
  display: inline-block;
  max-width: 100%;
  overflow-wrap: anywhere;
  padding: 4px 6px;
}

.encouragement {
  background: rgba(247, 255, 255, 0.88);
  border: 1px solid #c7eded;
  border-radius: 8px;
  box-shadow: 0 10px 26px rgba(24, 199, 189, 0.12);
  color: #489399;
  gap: 16px;
  margin-top: 24px;
  padding: 16px 24px;
}

.encouragement span {
  white-space: nowrap;
}

.encouragement button {
  background: linear-gradient(135deg, #0fa8a6, #078f98);
  border: 0;
  border-radius: 6px;
  color: #ffffff;
  font-weight: 900;
  min-height: 36px;
  padding: 0 18px;
}

.toast {
  background: #11194a;
  border: 2px solid var(--aqua);
  border-radius: 8px;
  bottom: 22px;
  box-shadow: var(--shadow);
  color: #ffffff;
  font-weight: 800;
  left: 50%;
  max-width: min(90vw, 520px);
  padding: 12px 16px;
  position: fixed;
  transform: translateX(-50%);
  z-index: 20;
}

.practice-view {
  background: rgba(255, 255, 255, 0.82);
  border: 2px solid #9dd2ff;
  border-radius: 8px;
  box-shadow: var(--shadow);
  padding: 22px;
}

.practice-view h2 {
  color: var(--ink);
  font-size: clamp(2rem, 4vw, 2.8rem);
  line-height: 1;
  margin: 0 0 18px;
}

.practice-card {
  align-items: center;
  background: linear-gradient(145deg, #ffffff, #f8ffff);
  border: 2px solid var(--aqua);
  border-radius: 8px;
  display: grid;
  gap: 12px;
  min-height: 260px;
  padding: 26px;
  text-align: center;
}

.practice-card span {
  color: var(--muted);
  font-weight: 800;
}

.practice-card strong {
  color: var(--purple);
  font-size: 1.2rem;
  text-transform: uppercase;
}

.practice-card p {
  color: var(--ink);
  font-size: 1.35rem;
  font-weight: 800;
  margin: 0;
}

.practice-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 18px;
}

.practice-controls button,
.quiz-item button {
  background: #ffffff;
  border: 1px solid #9ac8f6;
  border-radius: 7px;
  color: var(--ink);
  font-weight: 900;
  min-height: 40px;
  padding: 0 16px;
}

.practice-controls button:nth-child(2),
.quiz-item button {
  background: var(--yellow);
  border-color: #f3be00;
}

.quiz-form {
  display: grid;
  gap: 14px;
}

.quiz-item {
  background: #fbf5ff;
  border: 1px solid #bc78ec;
  border-radius: 8px;
  display: grid;
  gap: 10px;
  padding: 16px;
}

.quiz-item label {
  color: var(--ink);
}

.quiz-item textarea {
  border: 1px solid var(--line);
  border-radius: 7px;
  color: var(--ink);
  font: inherit;
  padding: 10px;
  resize: vertical;
}

.quiz-answer {
  background: #ffffff;
  border-left: 4px solid var(--purple);
  border-radius: 6px;
  margin: 0;
  padding: 10px;
}

.topic-link.reviewed::after {
  color: #ffffff;
  content: "Reviewed";
  font-size: 0.72rem;
  font-weight: 900;
}

.topic-link.favourite .topic-icon {
  background: #fff7cf;
  color: #c48b00;
}

.is-reviewed .status {
  border-color: var(--green);
}

.reviewed-pill {
  color: #a6ffbf;
}

.is-favourite .save {
  background: #fff7cf;
}

body.focus-mode .side-rail,
body.focus-mode .topic-panel,
body.focus-mode .action-panel,
body.focus-mode .crumb-bar,
body.focus-mode .encouragement {
  display: none;
}

body.focus-mode .app-shell,
body.focus-mode .study-grid {
  display: block;
}

body.focus-mode .workspace {
  margin: 0 auto;
  max-width: 980px;
  padding: 28px;
}

body.focus-mode .content {
  font-size: 1.12rem;
}

body.focus-mode .revision-section {
  padding: 24px 58px 24px 24px;
}

@media (max-width: 1180px) {
  .app-shell {
    grid-template-columns: 230px minmax(0, 1fr);
  }

  .study-grid {
    grid-template-columns: 260px minmax(0, 1fr);
  }

  .action-panel {
    display: grid;
    gap: 18px;
    grid-column: 1 / -1;
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .side-card {
    margin-bottom: 0;
  }
}

@media (max-width: 900px) {
  .app-shell {
    display: block;
  }

  .side-rail {
    height: auto;
    position: static;
  }

  .workspace {
    padding: 18px;
  }

  .hero,
  .crumb-bar,
  .note-heading,
  .encouragement {
    align-items: stretch;
    display: grid;
  }

  .hero-actions,
  .toolbar {
    justify-content: flex-start;
  }

  .study-grid,
  .action-panel {
    display: grid;
    grid-template-columns: 1fr;
  }

  .topic-panel {
    order: 1;
  }

  .content {
    order: 2;
  }

  .action-panel {
    order: 3;
  }

  .status {
    text-align: left;
  }
}

@media (max-width: 560px) {
  .workspace,
  .side-rail {
    padding: 16px;
  }

  .hero h1 {
    font-size: 2rem;
  }

  .hero-actions,
  .toolbar {
    display: grid;
  }

  .hero-actions button,
  .toolbar button,
  .streak {
    width: 100%;
  }

  .crumbs {
    align-items: flex-start;
    display: grid;
  }

  .revision-section {
    padding-right: 42px;
  }
}
"""


if __name__ == "__main__":
    raise SystemExit(main())
