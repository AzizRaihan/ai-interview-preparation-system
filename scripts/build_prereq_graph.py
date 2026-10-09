"""
Phase 3 extension: runs prerequisite tagging + validation for one topic at a
time, saving to tagged_entries.json immediately after each topic succeeds --
same don't-lose-progress discipline as difficulty tagging.
"""

import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from prereq_graph import topological_sort, validate_and_clean
from tag_prerequisites import tag_prerequisites

load_dotenv()

TAGGED_ENTRIES_PATH = Path("data/corpus/tagged_entries.json")

# Same safe sub-batch size difficulty tagging already proved works under Groq's
# 8,000-tokens-per-request cap. A chunk can only ever see its own questions, so
# each chunk's output is validated against ONLY that chunk's numbers (not the
# whole topic's) -- a reference to a question outside the visible chunk gets
# dropped as invalid even though it might be a real number elsewhere in the
# topic, since the model never actually saw that question's content.
SUB_BATCH_SIZE = 15
PACING_SECONDS = 20


def process_topic(client: Groq, topic_area: str) -> None:
    all_entries = json.loads(TAGGED_ENTRIES_PATH.read_text())
    topic_entries = [e for e in all_entries if e["topic_area"] == topic_area]

    print(f"Tagging prerequisites for {topic_area} ({len(topic_entries)} questions)...")

    combined_graph: dict[int, list[int]] = {}
    all_warnings: list[str] = []
    chunked = len(topic_entries) > SUB_BATCH_SIZE

    for i in range(0, len(topic_entries), SUB_BATCH_SIZE):
        chunk = topic_entries[i : i + SUB_BATCH_SIZE]
        raw = tag_prerequisites(client, topic_area, chunk)
        print(f"  chunk {i // SUB_BATCH_SIZE + 1}: {len(raw)}/{len(chunk)} entries got tags back")

        chunk_graph, chunk_warnings = validate_and_clean(chunk, raw)
        combined_graph.update(chunk_graph)
        all_warnings.extend(chunk_warnings)
        if chunked:
            time.sleep(PACING_SECONDS)

    print(f"  {len(all_warnings)} warning(s):")
    for w in all_warnings:
        print("   -", w)
    if chunked:
        print(
            "  NOTE: this topic was processed in chunks -- a true dependency spanning "
            "across two different chunks would not be detected, since each chunk only "
            "ever saw its own questions."
        )

    tier_by_number = {e["question_number"]: e["difficulty_tier"] for e in topic_entries}
    order, stuck = topological_sort(combined_graph, tier_by_number)
    print(f"  valid order for {len(order)}/{len(combined_graph)} questions")
    print(f"  stuck (cycle): {stuck if stuck else 'none'}")

    for entry in topic_entries:
        entry["prerequisites"] = combined_graph[entry["question_number"]]

    TAGGED_ENTRIES_PATH.write_text(json.dumps(all_entries, indent=2, ensure_ascii=False))
    print(f"  saved {topic_area}'s prerequisites to {TAGGED_ENTRIES_PATH}")

    by_number = {e["question_number"]: e for e in topic_entries}
    print()
    print("  Study order:")
    for qnum in order:
        prereqs = combined_graph[qnum]
        prereq_str = f" (needs: {prereqs})" if prereqs else ""
        print(f"    Q{qnum}{prereq_str}: {by_number[qnum]['question']}")


if __name__ == "__main__":
    import sys

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    process_topic(client, sys.argv[1])
