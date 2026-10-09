"""
Extracts the Grind 75 problem list into JSON. Source is
data/raw/grind75/scrape.txt, a hand-saved transcript of techinterviewhandbook.org/grind75
grouped by topic (there's no static markdown or public API for this data --
it's a client-rendered Next.js app -- so this was captured via the live page
rather than cloned like the other sources). Per CLAUDE.md scope: title,
difficulty, pattern/category only, no full problem statements.
"""

import json
import re
from pathlib import Path

RAW_PATH = Path("data/raw/grind75/scrape.txt")
OUT_PATH = Path("data/corpus/dsa.json")
SOURCE = "techinterviewhandbook.org/grind75"

ROW_RE = re.compile(r"^\d+\s+(.+?)\s+(Easy|Medium|Hard)$")


def extract_grind75_entries(raw_path: Path) -> list[dict]:
    entries = []
    topic = None
    for line in raw_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        match = ROW_RE.match(line)
        if match:
            title, difficulty = match.groups()
            entries.append(
                {
                    "question_or_topic": title,
                    "content": f"Pattern/category: {topic}",
                    "topic_area": "DSA",
                    "source": SOURCE,
                    "difficulty": difficulty,
                }
            )
        else:
            topic = line
    return entries


if __name__ == "__main__":
    entries = extract_grind75_entries(RAW_PATH)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False))
    print(f"Wrote {len(entries)} entries to {OUT_PATH}")
