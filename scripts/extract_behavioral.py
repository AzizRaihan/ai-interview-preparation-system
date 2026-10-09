"""
Extracts the 4 behavioral-interview*.md content pages from
yangshun/tech-interview-handbook into one JSON entry per "## " section
(same whole-unit approach as the other Phase 1 extractors). Strips each
file's YAML frontmatter block first.
"""

import json
from pathlib import Path

CONTENT_DIR = Path("data/raw/tech-interview-handbook/apps/website/contents")
FILES = [
    "behavioral-interview.md",
    "behavioral-interview-questions.md",
    "behavioral-interview-rubrics.md",
    "behavioral-interview-senior-candidates.md",
]
OUT_PATH = Path("data/corpus/behavioral.json")
SOURCE = "yangshun/tech-interview-handbook"


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :]
    return text


def extract_sections(text: str) -> list[tuple[str, str]]:
    lines = strip_frontmatter(text).splitlines()
    sections = []
    title = None
    body_lines: list[str] = []

    def flush():
        if title is not None:
            sections.append((title, "\n".join(body_lines).strip()))

    for line in lines:
        if line.startswith("## "):
            flush()
            title = line[3:].strip()
            body_lines = []
        elif title is not None:
            body_lines.append(line)
    flush()
    return sections


if __name__ == "__main__":
    entries = []
    for filename in FILES:
        text = (CONTENT_DIR / filename).read_text(encoding="utf-8")
        for title, content in extract_sections(text):
            entries.append(
                {
                    "question_or_topic": title,
                    "content": content,
                    "topic_area": "Behavioral",
                    "source": SOURCE,
                    "difficulty": None,
                }
            )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False))
    print(f"Wrote {len(entries)} entries to {OUT_PATH}")
