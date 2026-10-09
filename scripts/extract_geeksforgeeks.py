"""
Extracts Q&A/topic entries from the 5 GeeksforGeeks interview-prep pages fetched
by fetch_geeksforgeeks_pages.sh. All 5 share one template: a single
<div class="text"> article body containing "N. Question" <h3> headings with
rich HTML answers (lists, bold labels, comparisons) in between.

Heading classification:
  - "N. Question" (leading digit) -> real entry, number stripped from title.
  - A handful of known footer/junk headings (verified empty or link-only when
    inspected -- "Related Article", "Resources:", etc.) -> dropped entirely.
  - Anything else (e.g. "Types of VPN", a sub-heading inside a VPN question's
    answer; "Additional Tips for HR Interview", genuine standalone advice) ->
    kept as its own entry using the heading text as-is. The schema's
    `question_or_topic` field is meant to hold either, so this isn't a hack.
"""

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

RAW_DIR = Path("data/raw/geeksforgeeks")
OUT_DIR = Path("data/corpus")
SOURCE = "geeksforgeeks.org"

NUM_RE = re.compile(r"^\d+\.\s*")

JUNK_HEADINGS = {
    "Related Article",
    "Related Posts:",
    "Resources:",
    "Relevant Resources",
    "General HR Interview Questions",
}

PAGES = [
    {"name": "oop", "topic_area": "OOP"},
    {"name": "dbms", "topic_area": "DBMS"},
    {"name": "os", "topic_area": "OS"},
    {"name": "networking", "topic_area": "Networking"},
    {"name": "behavioral", "topic_area": "Behavioral"},
]


def table_to_text(table) -> str:
    rows = []
    for row in table.find_all("tr"):
        cells = [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
        rows.append(" | ".join(cells))
    return "\n".join(rows)


def html_to_text(elements) -> str:
    parts = []
    for el in elements:
        if el.name == "figure":
            continue
        if el.name == "table":
            table_text = table_to_text(el)
            if table_text:
                parts.append(table_text)
            continue

        for figure in el.find_all("figure"):
            figure.decompose()
        for table in el.find_all("table"):
            table.replace_with(table_to_text(table))

        text = el.get_text(separator=" ", strip=True)
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def extract_page(html_path: Path, topic_area: str) -> list[dict]:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "lxml")
    container = soup.find("div", class_="text")
    headings = container.find_all("h3")

    entries = []
    for i, heading in enumerate(headings):
        title = heading.get_text(strip=True)
        if title in JUNK_HEADINGS:
            continue
        title = NUM_RE.sub("", title)

        body_elements = []
        for sibling in heading.find_next_siblings():
            if sibling in headings:
                break
            body_elements.append(sibling)
        content = html_to_text(body_elements)
        if not content:
            continue

        entries.append(
            {
                "question_or_topic": title,
                "content": content,
                "topic_area": topic_area,
                "source": SOURCE,
                "difficulty": None,
            }
        )
    return entries


if __name__ == "__main__":
    for page in PAGES:
        html_path = RAW_DIR / f"{page['name']}.html"
        entries = extract_page(html_path, page["topic_area"])
        out_path = OUT_DIR / f"gfg_{page['name']}.json"
        out_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False))
        print(f"{page['name']}: wrote {len(entries)} entries to {out_path}")
