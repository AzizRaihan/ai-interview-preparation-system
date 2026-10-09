"""
Phase 2 step 2: classify every Q&A entry within a topic in one batched call,
tagging each with a foundational/intermediate/advanced tier so we can respect
prerequisite ordering later (CLAUDE.md rule 9). Batched per topic (not per
question) so the model judges relative difficulty against real in-topic
neighbors, and so 7 topics cost 7 API calls instead of 452.

Uses Groq (openai/gpt-oss-20b) rather than Gemini for this step -- Gemini's
free tier turned out to be a hard 20 requests/day for gemini-3.6-flash
(confirmed live, not from published docs), while Groq's real rate-limit
headers showed ~1,000 requests per ~90s window on this account -- comfortably
enough for both this one-time job and ongoing future use.
"""

import json
import os
import time

from dotenv import load_dotenv
from groq import Groq, InternalServerError

load_dotenv()

MODEL = "openai/gpt-oss-120b"
TIERS = ["foundational", "intermediate", "advanced"]

BATCH_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "classifications": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question_number": {"type": "integer"},
                    "reasoning": {"type": "string"},
                    "tier": {"type": "string", "enum": TIERS},
                },
                "required": ["question_number", "reasoning", "tier"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["classifications"],
    "additionalProperties": False,
}

BATCH_PROMPT_TEMPLATE = """You are tagging software engineering interview-prep questions \
for a study app. For EACH question below, classify how foundational it is \
*relative to the other questions in this same topic*.

- foundational: a core definition or concept everything else in this topic builds on
- intermediate: assumes foundational knowledge, applies or compares concepts
- advanced: assumes intermediate knowledge, deep edge cases or nuanced trade-offs

Examples (from a different topic, for calibration only):

Topic: DBMS
Question: What is a database?
Reasoning: A bare definition with no other concept assumed -- everything else in \
DBMS builds on knowing what a database is.
Tier: foundational

Topic: DBMS
Question: What is the difference between DBMS and RDBMS?
Reasoning: Assumes the reader already knows what a DBMS is, then compares it \
against a related concept -- that's applying/comparing foundational knowledge, \
not introducing it.
Tier: intermediate

Topic: DBMS
Question: How would you design a schema to avoid deadlocks in a highly \
concurrent, distributed transaction system?
Reasoning: Combines several advanced ideas at once (schema design, deadlocks, \
distributed systems, concurrency) and asks for a design trade-off, not a \
definition.
Tier: advanced

Now classify every question below. This topic is: {topic_area}

{questions_block}

Return one classification per question_number listed above, using its exact \
question_number so results can be matched back correctly."""


def classify_topic_batch(client: Groq, topic_area: str, entries: list[dict]) -> dict[int, dict]:
    questions_block = "\n\n".join(
        f"question_number: {e['question_number']}\nQuestion: {e['question']}\nAnswer: {e['answer']}"
        for e in entries
    )
    prompt = BATCH_PROMPT_TEMPLATE.format(topic_area=topic_area, questions_block=questions_block)

    response = None
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=4096,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "classifications",
                        "schema": BATCH_RESPONSE_SCHEMA,
                        "strict": True,
                    },
                },
            )
            break
        except InternalServerError:
            if attempt == 2:
                raise
            time.sleep(5 * (attempt + 1))

    result = json.loads(response.choices[0].message.content)
    by_number = {}
    for item in result["classifications"]:
        assert item["tier"] in TIERS
        by_number[item["question_number"]] = {
            "tier": item["tier"],
            "reasoning": item["reasoning"],
        }
    return by_number
