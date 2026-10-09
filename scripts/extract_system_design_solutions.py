"""
Extracts the 8 solved-question READMEs under solutions/system_design/ into JSON
entries. Each file becomes one whole entry (title = H1, content = everything
after it) — no sub-chunking here, that's a Phase 2 decision.
"""

import json
from pathlib import Path

REPO_DIR = Path("data/raw/system-design-primer")
OUT_PATH = Path("data/corpus/system_design_solutions.json")
SOURCE = "donnemartin/system-design-primer"


def extract_solution_entries(repo_dir: Path) -> list[dict]:
    entries = []
    for readme in sorted(repo_dir.glob("solutions/system_design/*/README.md")):
        text = readme.read_text(encoding="utf-8")
        title_line, _, body = text.partition("\n")
        title = title_line.lstrip("#").strip()
        entries.append(
            {
                "question_or_topic": title,
                "content": body.strip(),
                "topic_area": "System Design",
                "source": SOURCE,
                "difficulty": None,
            }
        )
    return entries


if __name__ == "__main__":
    entries = extract_solution_entries(REPO_DIR)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False))
    print(f"Wrote {len(entries)} entries to {OUT_PATH}")
