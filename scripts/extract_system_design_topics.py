"""
Extracts the genuine topic-explanation section of README.md (from "Performance
vs scalability" through "Security") into one JSON entry per top-level "## "
heading. Everything before (nav/meta) and after (Appendix reference lists) is
out of scope — see LEARNING_LOG.md for why.
"""

import json
from pathlib import Path

REPO_DIR = Path("data/raw/system-design-primer")
OUT_PATH = Path("data/corpus/system_design_topics.json")
SOURCE = "donnemartin/system-design-primer"

START_HEADING = "## Performance vs scalability"
END_HEADING = "## Appendix"


def extract_readme_topics(readme_path: Path) -> list[dict]:
    lines = readme_path.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(START_HEADING))
    end = next(i for i, line in enumerate(lines) if line.startswith(END_HEADING))
    section_lines = lines[start:end]

    entries = []
    title = None
    body_lines: list[str] = []

    def flush():
        if title is not None:
            entries.append(
                {
                    "question_or_topic": title,
                    "content": "\n".join(body_lines).strip(),
                    "topic_area": "System Design",
                    "source": SOURCE,
                    "difficulty": None,
                }
            )

    for line in section_lines:
        if line.startswith("## "):
            flush()
            title = line[3:].strip()
            body_lines = []
        else:
            body_lines.append(line)
    flush()

    return entries


if __name__ == "__main__":
    entries = extract_readme_topics(REPO_DIR / "README.md")
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False))
    print(f"Wrote {len(entries)} entries to {OUT_PATH}")
