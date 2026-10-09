"""
Phase 4: the agentic routing layer. Decides what to do next (study/quiz/
review, and which specific item) within a topic the caller chooses -- not a
fixed schedule, and not forced to cycle through every topic in sequence
either. The user picks the department (OOP, AI/ML, QA, ...) they want to work
in; the graph just decides what to do next inside that one topic.
"""

# Python 3.9 has no native `X | None` union syntax (that's 3.10+). This makes
# every type hint in this file lazy (just text, never evaluated at runtime),
# so `dict | None` below doesn't crash on import.
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, TypedDict

from langgraph.graph import END, StateGraph

# Reuse Phase 3's "what's this item's most recent logged status" lookup
# directly, instead of re-querying the tracker ourselves.
from tracking_db import get_current_status

TAGGED_ENTRIES_PATH = Path("data/corpus/tagged_entries.json")

# No longer an auto-cycled sequence -- just the list of valid department
# names, kept in the same order as parse_qa_markdown.py's SOURCE_FILES so
# "topic order" still means the same thing everywhere in the project (useful
# later for showing a menu of departments to choose from).
TOPIC_ORDER = [
    "OOP",
    "DBMS",
    "OS",
    "AI/ML",
    "Cybersecurity",
    "System Design (HLD)",
    "System Design (LLD)",
    "QA / Software Testing",
]


# The one shared object that flows through the graph -- each node reads it,
# does something, and returns an updated version of it.
class RoutingState(TypedDict):
    topic_area: str  # the department the caller chose to focus on right now
    entries: list[dict]  # this topic's questions, enriched by gather_state below
    # Optional[dict], not `dict | None` -- LangGraph resolves this hint for
    # real via get_type_hints() at graph-build time, not just at import time,
    # so the __future__ lazy-annotations trick doesn't protect it on Python
    # 3.9. Optional[] works natively, no lazy evaluation needed at all.
    decision: Optional[dict]  # the final {"action", "item"}, or None if nothing pending


def gather_state(state: RoutingState, conn) -> RoutingState:
    # The topic to check is now given directly by the caller, not computed
    # from a fixed position in a list.
    topic_area = state["topic_area"]

    # Load the whole 503-entry corpus, then filter to just this topic --
    # same load-then-filter pattern used throughout Phase 2/3.
    all_entries = json.loads(TAGGED_ENTRIES_PATH.read_text())
    topic_entries = [e for e in all_entries if e["topic_area"] == topic_area]

    # For every question in this topic, ask the tracker what its most recent
    # logged status is. Returns "Studied"/"Solved"/"Struggled", or None --
    # None means "Not Studied," since that status is never actually stored as
    # a row (see tracking_db.py / LEARNING_LOG.md for why).
    status_by_number = {}
    for entry in topic_entries:
        status_by_number[entry["question_number"]] = get_current_status(
            conn, topic_area, entry["question_number"]
        )

    # Build a NEW list of entries (not mutating the originals), each one
    # enriched with its status and whether it's "ready" to be studied.
    enriched = []
    for entry in topic_entries:
        prereq_numbers = entry["prerequisites"]
        # Ready only if EVERY prerequisite is already Studied or Solved.
        # all() on an empty list is True by default in Python -- which is
        # exactly correct here: an item with zero prerequisites is
        # automatically ready, nothing to wait on.
        ready = all(
            status_by_number[p] in ("Studied", "Solved") for p in prereq_numbers
        )
        enriched.append(
            {
                **entry,  # copy every existing field (question, answer, tier, ...)
                "status": status_by_number[entry["question_number"]],
                "ready": ready,
            }
        )

    # Return a new state (not mutating the original), with entries replaced
    # by the freshly-gathered data.
    return {**state, "entries": enriched}


def get_topic_progress(conn, topic_area: str) -> dict:
    # Same load-corpus-then-filter-to-topic pattern as gather_state -- this
    # function is a sibling of it, just tallying counts instead of feeding
    # into a routing decision.
    all_entries = json.loads(TAGGED_ENTRIES_PATH.read_text())
    topic_entries = [e for e in all_entries if e["topic_area"] == topic_area]

    # Start every possible status at zero, including "Not Studied" -- which,
    # same as everywhere else in this project, means "no log row exists,"
    # represented here by the string key "Not Studied" even though it's
    # never actually stored that way in the tracker itself.
    counts = {"Not Studied": 0, "Studied": 0, "Solved": 0, "Struggled": 0}

    for entry in topic_entries:
        status = get_current_status(conn, topic_area, entry["question_number"])
        # get_current_status returns None for "no row yet" -- translate that
        # back into the human-readable "Not Studied" label for this summary,
        # since a progress view is for a person to read, not for the router
        # to branch on.
        counts[status or "Not Studied"] += 1

    return {
        "topic_area": topic_area,
        "total": len(topic_entries),
        "counts": counts,
    }


# Same tier-to-number mapping used in prereq_graph.py's topological sort.
# Duplicated here (not imported) since it's a tiny constant and importing it
# would create an unnecessary cross-file dependency between two things that
# otherwise don't need to know about each other.
TIER_RANK = {"foundational": 0, "intermediate": 1, "advanced": 2}


def _pick_best(candidates: list[dict]) -> dict:
    # min() with a key function returns whichever item produces the smallest
    # value when passed through that function. The key here is a
    # (tier_rank, question_number) pair -- the exact same two-level tiebreak
    # already verified for the topological sort: foundational before
    # intermediate before advanced, then lowest question number as the final
    # tiebreaker when tiers match too.
    return min(candidates, key=lambda e: (TIER_RANK[e["difficulty_tier"]], e["question_number"]))


def decide(state: RoutingState) -> RoutingState:
    entries = state["entries"]

    # Bucket 1: anything currently struggled with, anywhere in this topic.
    # If this list is non-empty we return immediately -- the other three
    # buckets' code never even runs. That early return is what actually
    # enforces the priority order; it's not just a comment, it's the
    # mechanism.
    struggled = [e for e in entries if e["status"] == "Struggled"]
    if struggled:
        chosen = _pick_best(struggled)
        return {**state, "decision": {"action": "review_struggled", "item": chosen}}

    # Bucket 2: only reached once bucket 1 is empty. Studied-but-not-yet-
    # Solved items get quizzed next, to verify whether the "Studied" status
    # should graduate to "Solved" or reveal it should actually be
    # "Struggled."
    studied = [e for e in entries if e["status"] == "Studied"]
    if studied:
        chosen = _pick_best(studied)
        return {**state, "decision": {"action": "quiz", "item": chosen}}

    # Bucket 3: only reached once nothing existing needs fixing or
    # verifying. `status is None` is the precise "Not Studied" condition
    # (no log row exists yet); `ready` means every prerequisite is already
    # Studied/Solved, so this never introduces something before its own
    # foundation.
    ready_new = [e for e in entries if e["status"] is None and e["ready"]]
    if ready_new:
        chosen = _pick_best(ready_new)
        return {**state, "decision": {"action": "study_new", "item": chosen}}

    # Bucket 4: lowest urgency, only reached when nothing else qualifies --
    # spaced-repetition-style maintenance of things already mastered.
    solved = [e for e in entries if e["status"] == "Solved"]
    if solved:
        chosen = _pick_best(solved)
        return {**state, "decision": {"action": "review_solved", "item": chosen}}

    # All four buckets were empty: genuinely nothing pending in this topic
    # right now. This is a real, reportable outcome on its own -- the graph
    # does NOT jump to a different topic on its own anymore. Picking a
    # different department is the caller's choice, not the router's.
    return {**state, "decision": None}


def build_graph(conn):
    # gather_state needs an open tracker connection, but a live database
    # connection doesn't belong inside RoutingState (that's meant to hold
    # plain data, not external resources) -- so this closure binds `conn`
    # once, and the resulting gather_node still has the one-argument shape
    # every LangGraph node needs (just `state` in, `state` out).
    def gather_node(state: RoutingState) -> RoutingState:
        return gather_state(state, conn)

    graph = StateGraph(RoutingState)
    graph.add_node("gather", gather_node)
    graph.add_node("decide", decide)

    graph.set_entry_point("gather")
    # Both edges are now plain, unconditional edges -- gather always leads to
    # decide, and decide always ends the graph, whether or not it actually
    # found something. There's no loop anymore, since there's no "try the
    # next topic automatically" behavior left to loop for.
    graph.add_edge("gather", "decide")
    graph.add_edge("decide", END)

    # compile() turns the graph definition into something actually runnable.
    return graph.compile()
