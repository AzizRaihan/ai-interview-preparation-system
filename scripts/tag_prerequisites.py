"""
Phase 3 extension: identify prerequisite relationships between questions within
each topic, producing a directed dependency graph. Same per-topic batching as
difficulty tagging -- the model needs to see every question's number in one
context to reference real dependencies instead of inventing nonexistent ones.
"""

import json
import time

from groq import InternalServerError

MODEL = "openai/gpt-oss-120b"

PREREQ_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "dependencies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question_number": {"type": "integer"},
                    "reasoning": {"type": "string"},
                    "prerequisites": {"type": "array", "items": {"type": "integer"}},
                },
                "required": ["question_number", "reasoning", "prerequisites"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["dependencies"],
    "additionalProperties": False,
}

PREREQ_PROMPT_TEMPLATE = """You are mapping prerequisite relationships between software \
engineering interview-prep questions in the same topic. For EACH question below, \
identify which OTHER question numbers from this same list (if any) it assumes the \
reader already understands.

A question X is a prerequisite of question Y only if Y's answer specifically builds \
on, uses, or assumes a concept that X's answer defines or explains -- not just that \
they're on a similar subject.

Only reference question_number values that appear in the list below. If a question \
has no real prerequisites among this list, return an empty list for it.

Example (from a different topic, for calibration only):

Topic: DBMS
question_number: 1
Question: What is a database?
Answer: A database is an organized collection of data.

question_number: 2
Question: What is the difference between DBMS and RDBMS?
Answer: DBMS stores data as files. RDBMS stores data in tables.

question_number: 3
Question: What is a foreign key?
Answer: A foreign key is a field in one table that references the primary key of \
another table, enforcing a relationship between them.

Expected output:
- question_number 1: reasoning "A bare definition, nothing else here is assumed.", \
prerequisites []
- question_number 2: reasoning "Assumes you already know what a DBMS is (question \
1) before comparing it to RDBMS.", prerequisites [1]
- question_number 3: reasoning "Assumes you understand tables, introduced when \
question 2 contrasts DBMS/RDBMS.", prerequisites [2]

Now map every question below. This topic is: {topic_area}

{questions_block}

Return one entry per question_number listed above, using its exact question_number."""


def tag_prerequisites(client, topic_area: str, entries: list[dict]) -> dict:
    questions_block = "\n\n".join(
        f"question_number: {e['question_number']}\nQuestion: {e['question']}\nAnswer: {e['answer']}"
        for e in entries
    )
    prompt = PREREQ_PROMPT_TEMPLATE.format(topic_area=topic_area, questions_block=questions_block)

    response = None
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=8192,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "dependencies",
                        "schema": PREREQ_RESPONSE_SCHEMA,
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
    for item in result["dependencies"]:
        by_number[item["question_number"]] = {
            "reasoning": item["reasoning"],
            "prerequisites": item["prerequisites"],
        }
    return by_number
