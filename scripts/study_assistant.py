"""
Phase 5: turns a Phase 4 decision into something real -- a generated study
explanation, or a quiz you actually answer and get evaluated on. Uses Gemini
for retrieval (it has to match whatever embedded the FAISS index in Phase 2)
and Groq for the actual generation (already integrated, proven reliable).
"""

from __future__ import annotations

import json
import time

import faiss
import numpy as np
from google import genai
from google.genai import errors, types

from tracking_db import log_attempt

INDEX_PATH = "data/corpus/faiss_index.bin"
METADATA_PATH = "data/corpus/embedding_metadata.json"
EMBEDDING_MODEL = "gemini-embedding-001"


def retrieve_context(gemini_client, index, metadata: list[dict], item: dict, k: int = 3) -> list[dict]:
    # Build the same "question + answer" text shape used when the corpus was
    # originally embedded (Phase 2's decision), so the query and the stored
    # vectors are directly comparable.
    query_text = f"{item['question']}\n\n{item['answer']}"

    # task_type="RETRIEVAL_QUERY" here, not "RETRIEVAL_DOCUMENT" -- this is
    # the query side of the asymmetric pairing decided back in Phase 2.
    # Mismatching the two task types would quietly degrade match quality.
    #
    # Same 429-retry pattern as build_embeddings.py: Gemini's embedding API
    # is rate-limited, and a momentary "too busy right now" shouldn't crash
    # a live study session the way it would a one-off batch job. Retry up to
    # 5 times, waiting 35s between attempts; any OTHER error (bad key, bad
    # request) is re-raised immediately since retrying can't fix those.
    for attempt in range(5):
        try:
            response = gemini_client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=query_text,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
            )
            break
        except errors.ClientError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(35)
    query_vector = np.array([response.embeddings[0].values], dtype="float32")

    # Normalize the same way the stored vectors were normalized in Phase 2 --
    # the index does inner-product search, which only equals cosine
    # similarity when both sides are unit length.
    query_vector = query_vector / np.linalg.norm(query_vector)

    # Search for more than k, since the item's own entry will almost always
    # come back as the single closest match to its own text -- we need room
    # to drop that self-match and still have k real candidates left over.
    scores, positions = index.search(query_vector, k + 1)

    results = []
    for position in positions[0]:
        candidate = metadata[position]
        # Skip the item explaining itself -- matched by topic_area AND
        # question_number together, since question numbers repeat across
        # different topics (e.g. every topic has its own "Q1").
        if (
            candidate["topic_area"] == item["topic_area"]
            and candidate["question_number"] == item["question_number"]
        ):
            continue
        results.append(candidate)
        if len(results) == k:
            break

    return results


GENERATION_MODEL = "openai/gpt-oss-120b"  # same Groq model already used for tagging

EXPLANATION_PROMPT = """You are helping someone prepare for a software engineering \
interview. Explain the following question clearly, in your own words -- don't just \
repeat the reference answer verbatim, teach it.

Topic: {topic_area}
Question: {question}

Reference answer (base your explanation on this, don't contradict it):
{answer}

Related material, for context (only mention a connection if it's genuinely \
relevant -- most of the time it won't be, and that's fine, don't force one):
{related_block}

Write a clear, well-organized explanation of the main question."""


def generate_explanation(groq_client, item: dict, related: list[dict]) -> str:
    # Build the related-context block once here rather than inside the
    # template string -- if `related` is empty (no genuinely close matches
    # were found), this still produces valid, readable text instead of an
    # awkward blank section.
    if related:
        related_block = "\n\n".join(
            f"[{r['topic_area']}] {r['question']}\n{r['answer']}" for r in related
        )
    else:
        related_block = "(none found)"

    prompt = EXPLANATION_PROMPT.format(
        topic_area=item["topic_area"],
        question=item["question"],
        answer=item["answer"],
        related_block=related_block,
    )

    # Plain text completion -- no response_schema here, unlike the tagging
    # steps. Those needed structured JSON because code had to parse the
    # result; this is a natural-language explanation meant for a person to
    # read directly, so there's nothing to enforce a schema on.
    response = groq_client.chat.completions.create(
        model=GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


QUIZ_EVAL_SCHEMA = {
    "type": "object",
    "properties": {
        # feedback still listed BEFORE score -- same reasoning-before-
        # judgment trick as before, just paired with a number now instead
        # of a category label.
        "feedback": {"type": "string"},
        "score": {"type": "integer"},
    },
    "required": ["feedback", "score"],
    "additionalProperties": False,
}

# The Solved/Struggled line lives HERE, in plain code we control -- not left
# for the LLM to also decide alongside its scoring. Whatever score the model
# gives, this threshold is what actually determines the tracked outcome.
PASSING_SCORE = 7

QUIZ_EVAL_PROMPT = """You are evaluating someone's answer to a software engineering \
interview question, to help them prepare. Score their answer from 0 to 10:

- 9-10: fully covers the key points, even if phrased differently.
- 6-8: gets the core idea right but misses a meaningful supporting point.
- 3-5: partially on topic, but misses or garbles the core mechanism.
- 0-2: misses the core idea entirely, or describes something fundamentally \
different -- even if the answer sounds confident or uses related vocabulary.

Example (for calibration only, not the real question below):

Question: What is a database index?
Reference answer: A database index is a data structure that improves the speed of \
data retrieval, similar to a book's index, at the cost of extra storage and slower \
writes.
Answer A: "An index speeds up how fast you can find rows in a table, but it takes \
extra disk space and can slow down inserts and updates."
Score A: 9 -- captures the core trade-off (faster reads, cost to storage/writes), \
just phrased differently.
Answer B: "An index is a numbered list of all the rows in a table."
Score B: 1 -- this describes something like a row ID or primary key column, not \
what an index actually does (speeding up retrieval) or its trade-off. Sounding \
plausible and using related terms ("numbered," "rows," "table") doesn't earn a \
higher score if the core mechanism is wrong.

Now evaluate the real answer below.

Question: {question}

Reference answer (the known-correct answer to judge against):
{reference_answer}

Their answer:
{user_answer}

Write specific, encouraging feedback -- what they got right, what's missing or \
wrong -- then give a score from 0 to 10, per the rubric above."""


def evaluate_quiz_answer(groq_client, item: dict, user_answer: str) -> dict:
    prompt = QUIZ_EVAL_PROMPT.format(
        question=item["question"],
        reference_answer=item["answer"],
        user_answer=user_answer,
    )

    response = groq_client.chat.completions.create(
        model=GENERATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "quiz_evaluation",
                "schema": QUIZ_EVAL_SCHEMA,
                "strict": True,
            },
        },
    )
    result = json.loads(response.choices[0].message.content)
    # Translate the numeric score into the tracker's vocabulary right here,
    # so every caller gets a ready-to-log status, not just a raw number they
    # each have to threshold themselves.
    result["status"] = "Solved" if result["score"] >= PASSING_SCORE else "Struggled"
    return result


def present_decision(gemini_client, groq_client, index, metadata, conn, decision: dict) -> dict:
    action = decision["action"]
    item = decision["item"]

    if action in ("study_new", "review_solved"):
        related = retrieve_context(gemini_client, index, metadata, item)
        explanation = generate_explanation(groq_client, item, related)

        # Generating and showing the explanation IS the study event itself --
        # only log it for study_new, though. review_solved is just
        # maintenance viewing of something already mastered; it shouldn't
        # re-log a fresh "Studied" row over an existing "Solved" one.
        if action == "study_new":
            log_attempt(conn, item["topic_area"], item["question_number"], "Studied")

        return {"type": "explanation", "action": action, "item": item, "text": explanation}

    # quiz / review_struggled: nothing to generate yet -- the real question
    # already exists in the corpus, so just hand it back as-is.
    return {"type": "question", "action": action, "item": item, "text": item["question"]}


def submit_quiz_answer(groq_client, conn, decision: dict, user_answer: str) -> dict:
    item = decision["item"]
    result = evaluate_quiz_answer(groq_client, item, user_answer)


    log_attempt(conn, item["topic_area"], item["question_number"], result["status"])

    return result
