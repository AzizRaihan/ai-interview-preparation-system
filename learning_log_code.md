# Code Log

A running record of code walkthroughs for the interview-prep tracker project —
what each piece does, why it's built this way, and a full line-by-line
explanation, matching CLAUDE.md's explain-before-code discipline.

This is separate from `LEARNING_LOG.md`, which tracks decisions, concepts, and
results rather than code specifically. Entries here are written before the code
is written, then walked through again line by line once it exists.

---

## 2026-09-12 — `scripts/routing_graph.py`: state + `gather_state`

**What it does:** defines the shared state that flows through the Phase 4
routing graph, and the first node — `gather_state` — which builds one topic's
worth of questions, each tagged with its current tracked status and whether
it's "ready" (every prerequisite already Studied/Solved).

**Why built this way:** LangGraph passes one shared state object through every
node, so before writing any decision logic, we needed to settle exactly what
that state holds. Kept "gathering the data" and "deciding what to do with it"
as two separate pieces on purpose, rather than one tangled function.

**Trade-off:** queries the tracker once per question in the topic (up to 103
separate lookups for OS) instead of one bulk query. Simpler code; costs
nothing noticeable at this project's scale on a local SQLite file.

**Line by line:**
- `from __future__ import annotations` — same Python 3.9 fix as `tracking_db.py`,
  needed because of the `dict | None` type hint below.
- `TOPIC_ORDER` — the fixed topic sequence just confirmed, matching
  `parse_qa_markdown.py`'s `SOURCE_FILES` order.
- `RoutingState` (a TypedDict) — the three things that flow through the graph:
  which topic we're checking (`topic_index`), that topic's enriched questions
  (`entries`), and the eventual decision (`decision`, starts `None`).
- `gather_state(state, conn)` — a plain function taking the current state (plus
  an open tracker connection) and returning an updated state; this is exactly
  what a LangGraph node is.
- `topic_area = TOPIC_ORDER[state["topic_index"]]` — looks up which topic is
  currently being checked.
- Loads the full corpus, filters to this topic's entries.
- For each entry, asks the tracker for its most recent status
  (`"Studied"`/`"Solved"`/`"Struggled"`/`None` for not-yet-studied).
- `ready = all(status_by_number[p] in ("Studied", "Solved") for p in prereq_numbers)`
  — true only if every prerequisite is already done. `all()` on an empty list
  is `True` by default, which correctly makes a no-prerequisite item
  automatically ready.
- Builds a *new* dict per entry and a *new* state dict overall, rather than
  mutating in place — since this node re-runs every time the graph loops to a
  new topic, mutating in place risked stale data carrying over between runs.

**Understood?** yes

---

## 2026-09-12 — `scripts/routing_graph.py`: the `decide` node

**What it does:** scans one topic's gathered entries through the four
priority buckets in order (Struggled → Studied/quiz → ready-new-study →
Solved/review), stops at the first bucket with any candidate, and picks the
specific item using the same tier-then-number tiebreak as the topological
sort.

**Why built this way:** a plain scan through the list four times (stopping
early the moment one bucket has a hit) rather than pre-sorting everything up
front — costs nothing measurable at 29-103 entries per topic, and keeps the
priority order obvious just from reading the code top to bottom.

**Trade-off:** only looks at the single most recent status per item, not how
many times it's been struggled with or how long ago — consistent with Phase
3's "current status = most recent log row" design, but a real simplification
worth naming.

**Line by line:**
- `TIER_RANK` — duplicated from `prereq_graph.py` rather than imported, since
  it's a tiny constant and importing would create an unnecessary cross-file
  dependency.
- `_pick_best` — uses `min()` with a `(tier_rank, question_number)` key, the
  same two-level tiebreak already verified for the topological sort.
- Each bucket follows the identical shape: filter entries by status, and if
  the list is non-empty, pick the best candidate and return immediately —
  this early-return is what actually enforces the priority order, since a
  later bucket's code never runs if an earlier one already returned.
- `ready_new` bucket checks `status is None and ready` — the precise "Not
  Studied AND prerequisites satisfied" condition, since "Not Studied" is
  never a stored value, just the absence of any log row (`status is None`).
- The decision returned is `{"action": ..., "item": chosen}` — the full
  entry dict is included, not just its number, so whatever uses the decision
  has everything it needs without a second lookup.
- Falling through all four buckets returns `decision: None`, signaling
  "nothing left in this topic, move to the next one."

**Understood?** yes

---

## 2026-09-12 — `scripts/routing_graph.py`: wiring the actual LangGraph graph

**What it does:** connects `gather_state` and `decide` into a real, runnable
LangGraph graph, with a loop: nothing found in this topic but topics remain?
advance to the next one and try again. Something found, or truly nothing left
anywhere? Stop.

**Why built this way:** a plain sequence of steps can't naturally express
"keep trying the next topic until something turns up or you run out of
topics" — that's exactly the kind of loop LangGraph is built to support, and
the reason to use it here instead of a simple linear pipeline.

**A real bug caught and fixed:** `from __future__ import annotations` (used
earlier to avoid Python 3.9's lack of `X | None` syntax) only stops *our own*
code from crashing when it reads a type hint — it does NOT protect against a
library calling `typing.get_type_hints()` to actually resolve that hint for
real. LangGraph's `StateGraph` does exactly that internally, so `decision:
dict | None` still crashed at graph-build time even with the future-import in
place. Fixed by switching to `Optional[dict]`, which works natively on
Python 3.9 with no lazy-evaluation trick needed at all.

**Trade-off:** always restarts from `gather_state` on the *current* topic
before ever advancing — meaning "review Solved" (bucket 4) is essentially
unreachable until a topic has nothing left in the first three buckets at all,
not just its higher-priority ones. This is actually correct given the
confirmed policy (finish one topic before moving on), just worth naming.

**Tested end to end**, using real data already in `data/tracking.db` from
earlier Phase 3 testing (OOP Q14 already logged as Solved, nothing else
logged yet): the graph correctly picked `study_new`, item Q3 "What is a
Class?" — the lowest-numbered foundational OOP item with no unmet
prerequisites (Q1 is intermediate; Q4/6/7/8 aren't ready since their own
prerequisites haven't been studied yet).

**Understood?** yes

---

## 2026-09-12 — Removed forced topic sequencing; the user picks the department

**What changed:** the router no longer auto-cycles through all 8 topics in a
fixed order. The caller now provides which topic to focus on directly
(`topic_area` in state, e.g. "AI/ML"), and the graph only ever decides what to
do *within* that one topic — it never jumps to a different department on its
own.

**Why:** the user wants to choose which subject to work in and progress
within it, not be forced through topics one after another.

**What this simplified:** the `advance_topic` node and the conditional
routing after `decide` are both gone. The graph is now a plain two-step
pipeline (`gather -> decide -> end`) instead of a loop, since there's no
"automatically try the next topic" behavior left to loop for.

**What stayed the same:** everything inside `gather_state` and `decide` --
the four-bucket priority policy, the tier-then-number tiebreak, and "nothing
pending" as a real, valid outcome rather than a trigger to go elsewhere.
`TOPIC_ORDER` is kept as the list of valid department names (for validating
input, or showing a menu later), just no longer used to auto-cycle.

**Tested:** ran the graph against three different chosen topics (OOP, AI/ML,
QA) using real tracked data -- each one independently returned the correct
decision for that topic alone (OOP still Q3, matching the earlier verified
run; AI/ML and QA both correctly Q1, since neither has any tracked history
yet).

**Understood?** yes

---

## 2026-09-12 — Testing the priority order for real (Struggled vs. Studied)

**What we tested:** logged OS Q10 as "Studied" and OS Q20 as "Struggled" in
the same topic at the same time, then ran the router on OS. It correctly
ignored Q10 entirely and picked Q20 -- proving bucket 1 actually outranks
bucket 2, not just that each bucket works when tested alone.

Then tested bucket 2 by itself: logged only Cybersecurity Q1 as "Studied"
(nothing struggled anywhere in that topic), and the router correctly
returned `quiz` for Q1.

Bucket 4 (review Solved) wasn't tested live -- it shares the exact same code
shape as the other three buckets, and fully exhausting a real topic just to
exercise it wasn't worth the setup for this pass.

**Understood?** yes

---

## 2026-09-12 — `scripts/routing_graph.py`: `get_topic_progress`

**What it does:** for a given department, counts how many questions currently
sit in each status (Solved, Studied, Struggled, or untouched) -- the raw data
for a future "here's where you stand in each subject" view.

**Why built this way:** a sibling of `gather_state`, reusing the exact same
"load corpus, filter to topic, ask the tracker per question" steps -- the
only difference is tallying counts instead of feeding a routing decision.

**Trade-off:** same as `gather_state` -- one tracker query per question (up
to 103 for OS), not one bulk query. Consistent choice, same reasoning: costs
nothing noticeable at this project's scale.

**Line by line:**
- `counts = {...}` starts every bucket at zero, including Struggled, so a
  topic with no struggles reports `0` explicitly rather than a missing key.
- `counts[status or "Not Studied"] += 1` -- `get_current_status` returns
  `None` for "no row yet"; swapping that for the label `"Not Studied"` here
  is purely for display. The tracker itself still never stores that value as
  an actual row.
- Returns topic name, total count, and the full breakdown together.

**Tested** against all four topics touched so far -- every count matched
exactly what we'd actually logged (OOP's one Solved item, OS's one Studied +
one Struggled, Cybersecurity's one Studied, AI/ML completely untouched).

**Understood?** yes

---

## 2026-09-12 — `scripts/study_assistant.py`: `retrieve_context`

**What it does:** given one chosen item, embeds its question+answer as a
*query* (using Gemini, since it has to match whatever built the FAISS index),
searches for the closest matches in the whole corpus, and returns a few
genuinely related entries -- filtering out the item's own entry, which
otherwise always comes back as its own closest match.

**Why built this way:** uses `task_type="RETRIEVAL_QUERY"` (not
`RETRIEVAL_DOCUMENT`), completing the asymmetric embedding pairing decided
back in Phase 2. Searches across the whole corpus rather than one topic,
since cross-topic connections were explicitly deferred to this exact phase.

**Real finding from testing, not a bug:** tried this against three real
items (an OOP definition, an LLD design-patterns question, a DBMS foreign-key
question) and every single result stayed within the *same* topic as the
query, even though nothing in the code restricts that. Likely reason: each
topic's own vocabulary is dense and self-consistent, so the closest
neighbors of most questions genuinely are other questions in the same
subject. The cross-topic connection found earlier (AI/ML's RAG needing
Vector Databases) came from the prerequisite-tagging LLM *reading and
reasoning* about content -- a different mechanism than nearest-neighbor
similarity, which measures surface closeness, not conceptual dependency.

**Understood?** yes

---

## 2026-09-12 — `scripts/study_assistant.py`: `generate_explanation`

**What it does:** takes the chosen item plus its retrieved related entries,
asks Groq to write a real explanation grounded in that material -- not a
verbatim repeat of the stored answer.

**Why built this way:** plain text output, not structured JSON like the
tagging steps -- there's nothing for code to parse here, it's meant to be
read directly. The prompt explicitly tells the model to only mention a
connection to the related material when it's genuinely relevant, matching
what we just found empirically about how rare real cross-topic links are.

**Tested** against OOP's "What is a Class?" -- the result was noticeably
richer than the raw stored answer: a blueprint analogy, working code in two
languages, and an interview-focused summary table, while naturally weaving
in the retrieved Encapsulation/Object context without forcing anything.

**Understood?** yes

---

## 2026-09-12 — `scripts/study_assistant.py`: `evaluate_quiz_answer`

**What it does:** re-asks the real corpus question, and has Groq judge a
free-text answer against the reference answer.

**First version (3-way verdict) had a real quality problem:** tested with a
clearly wrong answer (comparing a class to "a folder that stores files,"
missing the whole concept of methods/behavior) and it still got marked
"partial" instead of "incorrect" -- even after adding calibration examples,
same fix that worked for difficulty tagging. The correct/partial boundary
improved, but partial/incorrect stayed blurry.

**Fixed by switching to a 0-10 score instead of 3 categories** -- your idea,
and it worked: the same wrong answer now scores 3/10 (clearly low), a strong
answer scores 9/10, and a thin-but-basically-right answer lands right at 7/10
-- a real, defensible spread instead of everything clustering into one
middle bucket.

**Where the Solved/Struggled line lives:** a plain constant,
`PASSING_SCORE = 7`, in code we control -- not something the LLM also has to
decide alongside its scoring. The function translates the score into a
ready-to-log status itself, so every caller gets `"Solved"` or `"Struggled"`
directly rather than each having to threshold the raw number themselves.

**Understood?** yes

---

## 2026-09-12 — `scripts/study_assistant.py`: `present_decision` + `submit_quiz_answer`, and the full loop tested

**What they do:** the last wiring piece. `present_decision` turns a Phase 4
decision into either a generated explanation (study_new/review_solved,
logging "Studied" only for study_new) or the real question to ask
(quiz/review_struggled, no generation needed). `submit_quiz_answer` takes the
user's actual answer afterward, scores it, and logs the result -- split into
two functions because quiz genuinely needs two separate steps (show the
question, then later receive an answer), not one.

**Full loop tested for real, not just each piece in isolation:**
1. OS Q20 was logged "Struggled" from earlier testing. Phase 4's router
   correctly picked it (`review_struggled`).
2. Submitted a genuinely good answer -- scored 8/10, logged as "Solved."
3. Re-ran the router on OS again: it now picked `quiz` on Q10 (already
   Studied from much earlier testing) -- proving the tracker update from
   step 2 actually changed what the router sees next, not just that each
   function works alone.

**A real environment mistake along the way (not a code bug):** an earlier
`cd` into `scripts/` silently persisted across tool calls, so a later test
failed to find `faiss_index.bin` via its relative path. Fixed by running
from the project root explicitly -- same class of mistake made once before
in this project, worth remembering to check working directory before
blaming the code.

**Phase 5 is functionally complete:** retrieval, explanation generation,
quiz evaluation, and the full decision-to-tracked-outcome loop all working
and verified end to end.

**Understood?** yes

---

## 2026-09-12 — `scripts/run_session.py`: `_append_to_study_log`, real session history in markdown

**What it does:** writes one markdown entry per real event (a study
explanation, or a quiz answer + score + feedback) to `study_logs/<topic>.md`
-- one growing file per topic, appended to forever, called from `run_cycle`
right after each explanation is shown or each quiz is scored.

**Why this shape:** the tracker (`tracking.db`) only stores status --
"Solved," a timestamp -- not the actual content. This is the readable
counterpart: what was actually taught, what you actually answered, and what
feedback you actually got, kept per topic so a file doesn't grow into one
giant unsorted wall of everything.

**Trade-off handled:** a topic name with a `/` in it (`AI/ML`) would make
Python read the `/` as a folder separator and try to create a directory
named `AI` -- swapped to a dash first (`AI-ML.md`) so it's always one flat
file per topic, never an accidental nested path.

**Tested in isolation, not through a real cycle:** called the helper
directly with fake data into a scratch `/tmp` folder (not the real
`study_logs/`), confirmed the filename sanitizing and the append-with-
divider behavior both work, then deleted the scratch folder -- specifically
to avoid seeding your actual study history with fake test entries now that
real sessions have started.

**Understood?** yes

---

## 2026-09-12 — `scripts/run_session.py`: Phase 6, the whole thing wired together

**What it does:** the actual end-to-end script. No new logic at all --
just real orchestration of Phases 3-5. `build_resources()` sets up every
shared thing once (Gemini client, Groq client, the FAISS index + metadata,
the tracker connection, the compiled routing graph). `run_cycle(topic_area,
resources)` does one full turn: ask the router for a decision, present it
(explanation or a real question), and if it's a quiz, actually read a typed
answer, score it, and log the outcome.

**Why one `build_resources()` instead of rebuilding things inside the
loop:** opening the tracker or reloading the FAISS index is real work with
no benefit to repeating -- doing it once up front and passing the same
resources into every `run_cycle` call is just avoiding pointless cost, not
a new design idea.

**A mistake I caught myself and fixed:** first draft had
`__import__("os").environ[...]` instead of a normal `import os` at the top
of the file -- sloppy, no reason for it, fixed immediately.

**Tested for real, three decisions in a row on OOP, not just one:**
1. First decision: nothing studied yet in OOP -> router picked
   `study_new` on Q3 ("What is a Class?"). Generated a genuinely good
   explanation (analogy, code sample, interview-relevance table). Logged
   "Studied."
2. Second decision, same topic, same resources: router now picked `quiz`
   on that same Q3 -- proving it saw the "Studied" log row from step 1
   before deciding, not just re-running blind. Piped in a deliberately
   unsure answer -> scored 1/10 -> logged "Struggled," with feedback that
   correctly named what was missing.
3. Third decision: router picked `review_struggled` on Q3 again --
   confirming the priority ordering in `decide()` actually works, not
   just in theory: once something is Struggled, it jumps straight to the
   top of the queue ahead of every other bucket.

**This is the real milestone:** three decisions in a row where each one
changed because of what the previous one logged, using nothing but the
already-built Phase 3 (tracker) + Phase 4 (router) + Phase 5 (LLM) pieces.
Phase 6 asked for exactly this -- one full studied -> quizzed -> logged ->
re-routed cycle -- and it works.

**Understood?** yes

---

## 2026-09-19 — `scripts/run_session.py`: `_append_study_material`, per-topic study notes

**What it does:** every time the router picks `study_new`, the generated
explanation is ALSO saved to `study_materials/study_<topic>.md` (e.g.
`study_QA-Software-Testing.md`), one growing file per topic, meant for
re-reading later. Quizzes, scores and repeat reviews stay only in
`study_logs/`, which remains the full history.

**Why a second folder instead of filtering `study_logs/`:** the log mixes
explanations, your answers and feedback, so it is awkward to read as notes.
This file is only the teaching material.

**Small decisions:** `_topic_slug` turns a topic name into a safe filename
(runs of non-alphanumerics become one dash: `AI/ML` -> `AI-ML`). Entry
headings are level 1 (`#`) because the AI's explanations contain their own
`##` headings, which would otherwise look like separate entries.

**Also done:** copied the 7 existing study explanations (OOP Q5-Q10, QA Q1)
out of `study_logs/` into the new files, keeping their original dates.

**Tested** in a scratch folder (naming and file format) before use.

**Understood?** _(pending)_
