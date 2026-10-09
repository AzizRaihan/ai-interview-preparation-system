"""
Phase 2 step 1: parse each hand-sourced markdown Q&A file into structured
entries (one dict per "## Q<N>: question" heading + its answer text).
"""

import re
from pathlib import Path

HEADING_RE = re.compile(r"^## Q(\d+):\s*(.+)$")


def parse_qa_file(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()

    entries = []
    number = None
    question = None
    body_lines: list[str] = []

    def flush():
        if question is not None:
            entries.append(
                {
                    "question_number": number,
                    "question": question,
                    "answer": "\n".join(body_lines).strip(),
                }
            )

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            flush()
            number = int(match.group(1))
            question = match.group(2).strip()
            body_lines = []
        elif question is not None and line.strip() != "---":
            body_lines.append(line)
    flush()

    return entries


CORPUS_DIR = Path("data/corpus")

SOURCE_FILES = [
    ("oop.md", "OOP"),
    ("DBMS.md", "DBMS"),
    ("OS.md", "OS"),
    ("AI.md", "AI/ML"),
    ("cybersecurity.md", "Cybersecurity"),
    ("system_design_HLD.md", "System Design (HLD)"),
    ("system_design_ULD.md", "System Design (LLD)"),
    ("QA.md", "QA / Software Testing"),
]


def parse_corpus(corpus_dir: Path) -> list[dict]:
    all_entries = []
    for filename, topic_area in SOURCE_FILES:
        entries = parse_qa_file(corpus_dir / filename)
        for entry in entries:
            entry["topic_area"] = topic_area
            entry["source_file"] = filename
            entry["content_type"] = "qa_pair"
            all_entries.append(entry)
    return all_entries
