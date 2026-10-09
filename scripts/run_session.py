"""
Phase 6: one clean, runnable script tying Phases 3-5 together -- get a
decision, present it, take a quiz answer if there is one, log the outcome,
and show that the router's next decision actually reflects it. No new logic
here, just real orchestration of everything already built.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import sys
from pathlib import Path

import faiss
from dotenv import load_dotenv
from google import genai
from groq import Groq

import routing_graph
from study_assistant import INDEX_PATH, METADATA_PATH, present_decision, submit_quiz_answer
from tracking_db import init_db

load_dotenv()  # reads GEMINI_API_KEY and GROQ_API_KEY from .env into the environment

# One growing markdown file per topic (study_logs/OOP.md, study_logs/DBMS.md,
# ...) -- separate from the tracker (which only stores status, not content),
# this is the actual readable history of what was taught and how each quiz
# answer went, for real sessions from here on.
STUDY_LOG_DIR = Path("study_logs")


def _append_to_study_log(topic_area: str, action: str, item: dict, body: str) -> None:
    # mkdir with exist_ok=True: create the folder the first time this runs,
    # do nothing (no error) on every call after that.
    STUDY_LOG_DIR.mkdir(exist_ok=True)

    # A literal "/" in the topic name (e.g. "AI/ML") would make Python treat
    # it as a subdirectory separator and try to create a folder called "AI"
    # -- swap it for a dash first so the topic name stays one flat filename.
    filename = topic_area.replace("/", "-") + ".md"
    path = STUDY_LOG_DIR / filename

    # One human-readable heading per entry: when it happened, what the
    # router decided, and which real question this was about.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    heading = f"## {timestamp} -- {action} -- Q{item['question_number']}: {item['question']}\n\n"

    # "a" = append mode -- opens the file (creating it if this is the very
    # first entry for this topic) and writes onto the end, never overwriting
    # what's already there.
    with open(path, "a") as f:
        f.write(heading)
        f.write(body.strip())
        f.write("\n\n---\n\n")  # a divider so entries stay visually separated


# A second, cleaner folder: ONLY the first-time teaching explanations
# (study_new), one file per topic, meant for re-reading later. study_logs/
# above stays the full history (quizzes, scores, reviews) -- this one is the
# "study notes" you can open and just read.
STUDY_MATERIALS_DIR = Path("study_materials")


def _topic_slug(topic_area: str) -> str:
    # Turns any topic name into a filename-safe piece: every run of characters
    # that isn't a letter or digit becomes one dash, and dashes at the ends are
    # trimmed. "QA / Software Testing" -> "QA-Software-Testing",
    # "AI/ML" -> "AI-ML", "System Design (HLD)" -> "System-Design-HLD".
    return re.sub(r"[^A-Za-z0-9]+", "-", topic_area).strip("-")


def _append_study_material(topic_area: str, item: dict, explanation: str) -> None:
    # Create the folder on first use; do nothing if it already exists.
    STUDY_MATERIALS_DIR.mkdir(exist_ok=True)
    path = STUDY_MATERIALS_DIR / f"study_{_topic_slug(topic_area)}.md"

    # The date goes under the heading in italics. The heading is level 1 ("# ")
    # on purpose: the AI's explanation has its own "##"/"###" headings, and a
    # level-1 entry heading keeps those nested under the right question
    # instead of looking like separate entries.
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    heading = f"# Q{item['question_number']}: {item['question']}\n\n*Studied {date}*\n\n"

    # "a" = append: creates the file on the first entry, then adds to the end.
    with open(path, "a") as f:
        f.write(heading)
        f.write(explanation.strip())
        f.write("\n\n---\n\n")


def build_resources():
    # One client per API we actually call: Gemini for retrieval embeddings,
    # Groq for everything generated (explanations, quiz evaluation).
    gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

    # faiss.read_index loads the vector index built in Phase 2 back into
    # memory; json.loads on the metadata file gives us the parallel list
    # that turns a FAISS position number back into a real question/answer.
    index = faiss.read_index(INDEX_PATH)
    metadata = json.loads(open(METADATA_PATH).read())

    # init_db() opens (or creates) the Phase 3 tracker -- the running record
    # of every study/quiz attempt so far.
    conn = init_db()

    # build_graph(conn) compiles the Phase 4 routing graph, wiring the
    # tracker connection into its gather_state node via the closure we wrote
    # back in Phase 4.
    graph = routing_graph.build_graph(conn)

    return gemini_client, groq_client, index, metadata, conn, graph


def run_cycle(topic_area: str, resources) -> None:
    gemini_client, groq_client, index, metadata, conn, graph = resources

    # Same call pattern verified back in Phase 4 -- an empty entries list and
    # decision=None are just placeholders; gather_state fills entries in,
    # decide fills decision in.
    result = graph.invoke({"topic_area": topic_area, "entries": [], "decision": None})
    decision = result["decision"]

    # decision is None exactly when every bucket was empty for this topic --
    # a real, valid outcome (per Phase 4's design), not an error.
    if decision is None:
        print(f"Nothing pending in {topic_area} right now.")
        return

    item = decision["item"]
    print(f"[{topic_area}] {decision['action']} -> Q{item['question_number']}: {item['question']}")
    print()

    presented = present_decision(gemini_client, groq_client, index, metadata, conn, decision)

    if presented["type"] == "explanation":
        # study_new / review_solved: nothing more to do, just show it --
        # and log the explanation itself as this entry's body.
        print(presented["text"])
        _append_to_study_log(topic_area, decision["action"], item, presented["text"])
        # Only the FIRST time something is taught goes into the study-notes
        # file. review_solved also produces an explanation, but that's a
        # repeat, not new material, so it stays out of the notes.
        if decision["action"] == "study_new":
            _append_study_material(topic_area, item, presented["text"])
        return

    # presented["type"] == "question": quiz / review_struggled. Show the
    # real question, then actually wait for a typed answer -- this is the
    # one place in this script that's genuinely interactive.
    print(presented["text"])
    user_answer = input("\nYour answer: ")

    outcome = submit_quiz_answer(groq_client, conn, decision, user_answer)
    print(f"\nScore: {outcome['score']}/10 -> {outcome['status']}")
    print(outcome["feedback"])

    # Body for a quiz-type entry: your actual answer, the score/outcome,
    # then the feedback -- everything needed to see later exactly what was
    # asked, what you said, and how it was judged.
    quiz_body = (
        f"**Your answer:** {user_answer}\n\n"
        f"**Score:** {outcome['score']}/10 -> {outcome['status']}\n\n"
        f"{outcome['feedback']}"
    )
    _append_to_study_log(topic_area, decision["action"], item, quiz_body)


def _resolve_topic(text: str) -> str | None:
    # Turns whatever was typed ("qa", "OOP", "system design (hld)") into one
    # exact official topic name, or None if it can't tell which one you meant.
    # Needed because gather_state compares names with ==, so "QA" would match
    # zero questions and the app would just say "nothing pending".
    text = text.strip().lower()
    if not text:
        return None

    # First choice: a case-insensitive exact match, e.g. "oop" -> "OOP".
    for name in routing_graph.TOPIC_ORDER:
        if name.lower() == text:
            return name

    # Second choice: the typed text appears inside exactly ONE topic name,
    # e.g. "qa" -> "QA / Software Testing". If it appears in several (like
    # "system" -> both System Design topics), guessing would be wrong, so
    # return None and let the caller ask again.
    partial = [n for n in routing_graph.TOPIC_ORDER if text in n.lower()]
    return partial[0] if len(partial) == 1 else None


def _prompt_for_topic() -> str:
    # Shown both at startup and whenever you choose to switch topics --
    # TOPIC_ORDER is the single source of truth for valid names (same list
    # routing_graph.py itself uses), so this menu can't drift out of sync
    # with what gather_state actually accepts.
    while True:
        print("\nTopics:")
        for name in routing_graph.TOPIC_ORDER:
            print(f"  {name}")
        topic = _resolve_topic(input("Which topic? "))
        if topic is not None:
            return topic
        # Unknown or ambiguous input: say so and ask again, instead of
        # carrying a bad name forward.
        print("Not a recognized topic (or it matches more than one) -- try again.")


if __name__ == "__main__":
    # Topic comes from the command line if given (same pattern as
    # build_prereq_graph.py), otherwise ask interactively -- real sessions
    # won't always start knowing the exact topic string by heart.
    # A topic typed on the command line goes through the same matching; if
    # it isn't recognized, fall back to the menu rather than run with a bad name.
    topic = _resolve_topic(sys.argv[1]) if len(sys.argv) > 1 else None
    if topic is None:
        topic = _prompt_for_topic()

    # Build every shared resource once, up front -- not once per cycle,
    # since opening the tracker or reloading the FAISS index twice would be
    # wasteful for no benefit.
    resources = build_resources()

    # A real session is "however many decisions I feel like doing right
    # now," not a fixed count -- so this loops until you explicitly quit,
    # rather than the old hardcoded "run it exactly twice" test scaffold.
    while True:
        print(f"\n=== {topic} ===")
        run_cycle(topic, resources)

        # Enter alone just means "yes, keep going in this same topic" --
        # the common case should be the free action, not typing a word.
        choice = input(
            "\nContinue in this topic? [Enter = yes, s = switch topic, q = quit]: "
        ).strip().lower()

        if choice == "q":
            break
        elif choice == "s":
            topic = _prompt_for_topic()
        # any other input (including a blank Enter) just loops again on
        # the same topic -- no separate "yes" branch needed for that.
