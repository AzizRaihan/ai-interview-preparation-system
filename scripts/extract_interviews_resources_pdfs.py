"""
Extracts numbered "N) Question" Q&A pairs from the DBMS/OS/Networking PDFs in
avinash201199/Interviews-Resources. All three are scraped-webpage-to-PDF exports
sharing the same quirks:
  - stray share-count sidebar lines (e.g. "54.6M") injected mid-text
  - in-answer numbered sub-lists (e.g. "1) Mutual Exclusion...") that falsely
    match the same "N) " heading pattern as real questions
A heading is only accepted if its number is strictly greater than the last
accepted one -- this rejects sub-list restarts (which don't exceed the current
count) while still allowing the Networking file's genuine numbering gap
(28 -> 30, no 29 in the source).
"""

import json
import re
from pathlib import Path

import fitz

HEADING_RE = re.compile(r"^(\d+)\)\s*(.+)$")
JUNK_RE = re.compile(r"^\d+(\.\d+)?[MK]\s*$")
SOURCE_REPO = "avinash201199/Interviews-Resources"

SOURCES = [
    {
        "pdf": Path("data/raw/interviews-resources/DBMS-Interview-Questions/DBMS Interview Questions.pdf"),
        "topic_area": "DBMS",
        "out": Path("data/corpus/dbms.json"),
    },
    {
        "pdf": Path(
            "data/raw/interviews-resources/OS-Interview-Questions/Operating System Interview Question.pdf"
        ),
        "topic_area": "OS",
        "out": Path("data/corpus/os.json"),
    },
    {
        "pdf": Path(
            "data/raw/interviews-resources/Networking-Interview-Questions/Networking Interview Questions.pdf"
        ),
        "topic_area": "Networking",
        "out": Path("data/corpus/networking.json"),
    },
]


def extract_qa_entries(pdf_path: Path, topic_area: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    text = "".join(page.get_text() for page in doc)
    lines = [line for line in text.split("\n") if not JUNK_RE.match(line.strip())]

    entries = []
    title = None
    body_lines: list[str] = []
    last_num = 0

    def flush():
        if title is not None:
            entries.append(
                {
                    "question_or_topic": title,
                    "content": "\n".join(body_lines).strip(),
                    "topic_area": topic_area,
                    "source": SOURCE_REPO,
                    "difficulty": None,
                }
            )

    for line in lines:
        match = HEADING_RE.match(line.strip())
        if match and int(match.group(1)) > last_num:
            flush()
            last_num = int(match.group(1))
            title = match.group(2).strip()
            body_lines = []
        elif title is not None:
            body_lines.append(line)
    flush()

    return entries


if __name__ == "__main__":
    for cfg in SOURCES:
        entries = extract_qa_entries(cfg["pdf"], cfg["topic_area"])
        cfg["out"].parent.mkdir(parents=True, exist_ok=True)
        cfg["out"].write_text(json.dumps(entries, indent=2, ensure_ascii=False))
        print(f"{cfg['topic_area']}: wrote {len(entries)} entries to {cfg['out']}")
