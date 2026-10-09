"""
Extracts Q&A entries from Devinterview-io/oop-interview-questions' README.md.
Real answers only exist for questions 1-15 (the file's "52 questions" title is
aspirational marketing; the rest are paywalled on devinterview.io) — this
extracts whatever numbered "## N. <question>" sections actually exist.
"""

import json
import re
from pathlib import Path

README_PATH = Path("data/raw/oop-interview-questions/README.md")
OUT_PATH = Path("data/corpus/oop.json")
SOURCE = "Devinterview-io/oop-interview-questions"

HEADING_RE = re.compile(r"^## \d+\.\s*(.+)$")
FOOTER_MARKER = "#### Explore all"


def clean_title(raw_title: str) -> str:
    return re.sub(r"[_*]", "", raw_title).strip()


def extract_oop_entries(readme_path: Path) -> list[dict]:
    lines = readme_path.read_text(encoding="utf-8").splitlines()

    entries = []
    title = None
    body_lines: list[str] = []

    def flush():
        if title is not None:
            content = "\n".join(body_lines).strip()
            content = content.split(FOOTER_MARKER)[0].strip()
            entries.append(
                {
                    "question_or_topic": title,
                    "content": content,
                    "topic_area": "OOP",
                    "source": SOURCE,
                    "difficulty": None,
                }
            )

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            flush()
            title = clean_title(match.group(1))
            body_lines = []
        elif title is not None:
            body_lines.append(line)
    flush()

    return entries


if __name__ == "__main__":
    entries = extract_oop_entries(README_PATH)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False))
    print(f"Wrote {len(entries)} entries to {OUT_PATH}")
