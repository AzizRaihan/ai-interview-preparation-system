"""
Phase 2 step 3: run the full pipeline -- parse all markdown files, classify
each topic's questions into difficulty tiers, and save the combined result to
one JSON file ready for the next step (chunking + embedding). Saves progress
after every sub-batch (not just at the end) and skips already-tagged entries
on re-runs, so a mid-run failure (e.g. Groq's daily token cap) never loses
work and a retry only pays for what's actually left.
"""

import json
import os
import time
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from parse_qa_markdown import CORPUS_DIR, parse_corpus
from tag_difficulty import classify_topic_batch

load_dotenv()

OUTPUT_PATH = Path("data/corpus/tagged_entries.json")

# Groq's openai/gpt-oss-120b caps at 8,000 tokens per minute per request (confirmed
# live via a 413 error on DBMS's 58-question batch, which needed 8,459). 15
# questions/sub-batch stays safely under that even for AI/ML, the heaviest topic
# at ~263 tokens/question. PACING_SECONDS spaces sub-batch calls out since the
# cap is per-minute, not just per-request -- firing several safely-sized batches
# back-to-back could still cumulatively exceed it within the same rolling window.
SUB_BATCH_SIZE = 15
PACING_SECONDS = 20


def load_already_tagged() -> dict[tuple[str, int], dict]:
    if not OUTPUT_PATH.exists():
        return {}
    existing = json.loads(OUTPUT_PATH.read_text())
    return {(e["topic_area"], e["question_number"]): e for e in existing}


def save_tagged_entries(tagged_by_key: dict[tuple[str, int], dict]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(list(tagged_by_key.values()), indent=2, ensure_ascii=False))


def build_tagged_corpus() -> list[dict]:
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    entries = parse_corpus(CORPUS_DIR)
    tagged_by_key = load_already_tagged()

    by_topic = defaultdict(list)
    for entry in entries:
        key = (entry["topic_area"], entry["question_number"])
        if key not in tagged_by_key:
            by_topic[entry["topic_area"]].append(entry)

    for topic_area, topic_entries in by_topic.items():
        print(f"Classifying {topic_area} ({len(topic_entries)} new questions)...")
        for i in range(0, len(topic_entries), SUB_BATCH_SIZE):
            chunk = topic_entries[i : i + SUB_BATCH_SIZE]
            results = classify_topic_batch(client, topic_area, chunk)
            for entry in chunk:
                tag = results[entry["question_number"]]
                entry["difficulty_tier"] = tag["tier"]
                entry["difficulty_reasoning"] = tag["reasoning"]
                tagged_by_key[(entry["topic_area"], entry["question_number"])] = entry
            save_tagged_entries(tagged_by_key)
            print(f"  saved progress: {len(tagged_by_key)} total tagged entries")
            time.sleep(PACING_SECONDS)

    return list(tagged_by_key.values())


if __name__ == "__main__":
    tagged_entries = build_tagged_corpus()
    print(f"Done: {len(tagged_entries)} tagged entries in {OUTPUT_PATH}")
