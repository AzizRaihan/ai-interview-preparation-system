# Codebase Walkthrough

A file-by-file walkthrough of the Interview Prep Progress Tracker, written so you
can understand each line well enough to write it yourself. Every file is split into
small blocks. Each block shows the code, what it does in plain words, a
before-and-after using one running example, and why the line is there.

Files are covered in build order, which is also the order you need to understand
them in. Dead files (`extract_*.py`, `fetch_*.sh`, leftovers from an abandoned
approach, confirmed unused by anything else) are skipped.

**Order:**
1. `parse_qa_markdown.py` — raw markdown → structured Q&A entries
2. `tag_difficulty.py` — an LLM labels each entry's difficulty
3. `build_tagged_corpus.py` — runs #2 across all 503 entries
4. `tag_prerequisites.py` — an LLM works out which questions depend on which
5. `prereq_graph.py` — turns those dependencies into a study order
6. `build_prereq_graph.py` — runs #4 and #5 across all topics
7. `build_embeddings.py` — turns the corpus into a searchable vector index
8. `tracking_db.py` — the database that remembers what you studied
9. `routing_graph.py` — decides what to study next (LangGraph)
10. `study_assistant.py` — retrieval, explanations, and quiz scoring
11. `run_session.py` — the program you actually run

---

## File 1: `scripts/parse_qa_markdown.py`

**What it does:** reads the 8 hand-written markdown files (`oop.md`, `DBMS.md`, ...)
and turns each `## Q<number>: question` heading plus the text under it into one
Python dictionary. It returns one flat list of about 503 dictionaries, each tagged
with which topic it came from. Everything else in the project starts from this list.

**Running example** (a tiny fake `oop.md`):

```
## Q1: What is a variable?
A variable stores a value.
---
## Q2: What is a loop?
Repeats code.
```

### Block 1: imports

```python
import re
from pathlib import Path
```
**In plain words:** `re` is Python's tool for matching text patterns. `Path` lets you
treat a file location as an object instead of a plain string.

**Example:**
- `Path("data/corpus") / "oop.md"` gives the path `data/corpus/oop.md`.
- `Path("data/corpus/oop.md").read_text()` gives the whole file as one string.

**Why:** the `/` between paths works on any operating system, and `read_text()` saves
you from opening and closing the file yourself.

### Block 2: the heading pattern

```python
HEADING_RE = re.compile(r"^## Q(\d+):\s*(.+)$")
```
**In plain words:** a pattern that recognizes a heading line like `## Q3: What is a
Class?` and grabs the number and the question text out of it.

**Example**, reading the pattern piece by piece:
- `^` means the line must start right here.
- `## Q` means those exact four characters.
- `(\d+)` means one or more digits, and the parentheses "save" what matched as group 1.
- `:` means a literal colon.
- `\s*` means zero or more spaces.
- `(.+)` means one or more of any character, saved as group 2.
- `$` means the line must end here.

Trying it on the running example:
- `"## Q1: What is a variable?"` matches. `group(1)` is `"1"` (text, not a number yet), and `group(2)` is `"What is a variable?"`.
- `"A variable stores a value."` returns `None`, because it doesn't start with `## Q`.
- `"---"` returns `None`.

**Why:** it's written once at the top and reused for every line, instead of being
rebuilt on every line.

### Block 3: read the file into lines

```python
def parse_qa_file(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
```
**In plain words:** define a function that takes one file's path. Read the whole file
as one string, then cut it into a list with one item per line.

**Example:**
- After `read_text(...)`: `"## Q1: What is a variable?\nA variable stores a value.\n---\n## Q2: What is a loop?\nRepeats code.\n"`
- After `.splitlines()`: `lines = ["## Q1: What is a variable?", "A variable stores a value.", "---", "## Q2: What is a loop?", "Repeats code."]`

**Why:** the parser looks at one line at a time, so it needs a list to loop over.
`.splitlines()` also removes the invisible newline at the end of each line, so no
line keeps a stray `\n`.

### Block 4: the notepad

```python
    entries = []
    number = None
    question = None
    body_lines: list[str] = []
```
**In plain words:** four variables. `entries` is the finished pile. `number`,
`question` and `body_lines` are a notepad for the one question you're writing down
right now.

**Example, state right now:**
`entries = []`, `number = None`, `question = None`, `body_lines = []`

**Why:** `None` means "no question on the notepad yet." Later code checks for it.

### Block 5: the "save the notepad" helper

```python
    def flush():
        if question is not None:
            entries.append(
                {
                    "question_number": number,
                    "question": question,
                    "answer": "\n".join(body_lines).strip(),
                }
            )
```
**In plain words:** if a question is on the notepad, package it as a dictionary and
add it to the finished pile.

**Example, called while the notepad holds Q1:**
- Notepad: `number = 1`, `question = "What is a variable?"`, `body_lines = ["A variable stores a value."]`
- `"\n".join(["A variable stores a value."])` gives `"A variable stores a value."`. With two lines, `"\n".join(["a", "b"])` gives `"a\nb"`.
- `.strip()` removes blank space from both ends of the answer.
- Result: `entries = [{"question_number": 1, "question": "What is a variable?", "answer": "A variable stores a value."}]`

**Example, called while the notepad is empty** (`question = None`): the `if` is false,
so nothing is saved.

**Why:** the same "save" is needed in two places, when a new question starts and at
the very end, so it's written once as a function. `flush` takes no arguments because
it's defined inside `parse_qa_file`, so it can see `number`, `question`, `body_lines`
and `entries` directly.

### Block 6: look at each line

```python
    for line in lines:
        match = HEADING_RE.match(line)
```
**In plain words:** go through the lines one at a time and ask "is this a heading?"

**Example:**
- Line 1 `"## Q1: What is a variable?"` gives a match object.
- Line 2 `"A variable stores a value."` gives `match = None`.
- Line 3 `"---"` gives `match = None`.

**Why:** the match result is how the loop tells a new question apart from an answer line.

### Block 7: a heading starts a new question

```python
        if match:
            flush()
            number = int(match.group(1))
            question = match.group(2).strip()
            body_lines = []
```
**In plain words:** save the old question, then start a fresh notepad for the new one.

**Example at line 1** (`"## Q1: ..."`):
- `flush()` does nothing, because `question` is still `None`.
- Notepad becomes `number = 1`, `question = "What is a variable?"`, `body_lines = []`.

**Example at line 4** (`"## Q2: ..."`):
- `flush()` saves Q1, so `entries` now has 1 item.
- Notepad resets to `number = 2`, `question = "What is a loop?"`, `body_lines = []`.

**Why:** `flush()` comes first so the old question is saved before its variables are
overwritten. `int(...)` turns the text `"1"` into the number `1`. `body_lines = []`
creates a brand-new empty list, so nothing from the old answer can leak into the
new one.

### Block 8: anything else belongs to the answer

```python
        elif question is not None and line.strip() != "---":
            body_lines.append(line)
```
**In plain words:** if it isn't a heading, we're inside a question, and it isn't the
`---` divider, add it to the answer.

**Example:**
- Line 2 `"A variable stores a value."` is added, so `body_lines = ["A variable stores a value."]`.
- Line 3 `"---"` fails the last check and is skipped, so `body_lines` doesn't change.
- Line 5 `"Repeats code."` is added, so `body_lines = ["Repeats code."]`.

**Why:** `question is not None` ignores any stray text before the first heading. The
`---` check keeps the divider out of the answers.

### Block 9: save the last question

```python
    flush()
    return entries
```
**In plain words:** after the loop, the notepad still holds Q2, because only a new
heading triggers a save and none comes after Q2. This last `flush()` saves it.

**Example:** `entries` goes from 1 item (Q1) to 2 items (Q1, Q2).

**Why:** the loop has no way to know it just read the final question, so the last
one has to be saved by hand. If you deleted this line, Q2 would be lost silently,
with no error.

### Block 10: which file is which topic

```python
CORPUS_DIR = Path("data/corpus")

SOURCE_FILES = [
    ("oop.md", "OOP"),
    ("DBMS.md", "DBMS"),
    ("OS.md", "OS"),
    ("AI.md", "AI/ML"),
    ("cybersecurity.md", "Cybersecurity"),
    ("system_design_HLD.md", "System Design (HLD)"),
    ("system_design_ULD.md", "System Design (LLD)"),
    ("QA.md", "QA / Software Testing"),
]
```
**In plain words:** the folder the files live in, and a list pairing each filename with
the topic name it stands for.

**Example:** `SOURCE_FILES[0]` is `("oop.md", "OOP")`. Writing
`filename, topic_area = SOURCE_FILES[0]` sets `filename = "oop.md"` and
`topic_area = "OOP"`.

**Why:** one list is the single source of truth for the 8 topic names. Other files
(like `routing_graph.py`) reuse the same names and order.

### Block 11: parse every file and label each entry

```python
def parse_corpus(corpus_dir: Path) -> list[dict]:
    all_entries = []
    for filename, topic_area in SOURCE_FILES:
        entries = parse_qa_file(corpus_dir / filename)
        for entry in entries:
            entry["topic_area"] = topic_area
            entry["source_file"] = filename
            entry["content_type"] = "qa_pair"
            all_entries.append(entry)
    return all_entries
```
**In plain words:** for each file, parse it, then stamp every entry with its topic,
its file, and a fixed type label, and collect everything into one list.

**Example**, pretending only two files exist and each has one question:
- Round 1: `filename = "oop.md"`, `topic_area = "OOP"`. `parse_qa_file` returns `[{"question_number": 1, "question": "What is a class?", "answer": "..."}]`. The inner loop adds `topic_area = "OOP"`, `source_file = "oop.md"` and `content_type = "qa_pair"`. `all_entries` has 1 item.
- Round 2: `filename = "dbms.md"`, `topic_area = "DBMS"`. The same steps run on one DBMS entry, whose `question_number` is also `1`. `all_entries` has 2 items.

**Why:** `parse_qa_file` only knows about one file and has no idea what "topic" means,
so the labels are added here. Both entries have `question_number = 1`, which is fine
because `topic_area` tells them apart.

### Final output for the running example

Calling `parse_qa_file` on the tiny `oop.md` gives:

```python
[{"question_number": 1, "question": "What is a variable?", "answer": "A variable stores a value."},
 {"question_number": 2, "question": "What is a loop?", "answer": "Repeats code."}]
```

### The big ideas (short)

**A state machine.** The loop is always in one of two states, "collecting a question"
or "not yet." A heading changes the state, and any other line just adds to the
current one. The "notepad" variables are that state. **A closure.** `flush` uses
variables from the function around it instead of taking them as arguments. **A
sentinel value.** `None` doubles as the flag meaning "no question yet." One
data-design idea sits behind the whole file: each Q&A pair is kept whole as one unit
(one question plus its full answer), which matters later when these become the
searchable pieces.

### Watch out for later

- `question_number` repeats across topics (every topic has a Q1), so any later code
  that looks up a question must use the topic *and* the number together. File 10
  filters on exactly that.

**Understood?** _(pending)_

---

## File 2: `scripts/tag_difficulty.py`

**What it does:** takes all the Q&A entries of one topic, sends them to an AI model
(Groq) in a single request, and gets back a label for each: `foundational`,
`intermediate` or `advanced`, plus a written reason. It returns a dictionary from
question number to that label. The router (file 9) later uses these labels to decide
which question comes first.

**Running example** (a tiny fake DBMS topic, 3 entries):

```python
entries = [
    {"question_number": 1, "question": "What is a database?",
     "answer": "An organized collection of data."},
    {"question_number": 2, "question": "What is a primary key?",
     "answer": "A column that uniquely identifies each row."},
    {"question_number": 3, "question": "How would you shard a multi-tenant database?",
     "answer": "Split data across servers by tenant..."},
]
```

### Block 1: imports and the API key

```python
import json
import os
import time

from dotenv import load_dotenv
from groq import Groq, InternalServerError

load_dotenv()
```
**In plain words:** load the tools this file needs, then read the secret API key from
a hidden `.env` file.

**Example:**
- `.env` contains the line `GROQ_API_KEY=abc123`.
- Before `load_dotenv()`, the program's environment doesn't have that key. After it, the key is available, and the Groq client reads it from there.
- `InternalServerError` is the specific error Groq raises when its server fails (an HTTP 5xx).

**Why:** the key lives in `.env`, not in the code, so it never gets copied around
with the source. Importing the specific error class lets the retry code (Block 8)
catch only that error and not everything else. (`os` is imported but never used in
this file.)

### Block 2: two constants

```python
MODEL = "openai/gpt-oss-120b"
TIERS = ["foundational", "intermediate", "advanced"]
```
**In plain words:** which AI model to use, and the only three labels allowed.

**Example:** `"advanced" in TIERS` is `True`. `"medium" in TIERS` is `False`.

**Why:** `TIERS` is used twice below, in the schema (Block 3) and in the check
(Block 10), so the two can never get out of step.

### Block 3: the shape of the reply we demand

```python
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
```
**In plain words:** a rulebook describing exactly what the AI's answer must look like:
one object holding a list called `classifications`, and each item in that list has a
question number, a reason, and a tier.

**Example, a reply that follows the rules:**
`{"classifications": [{"question_number": 1, "reasoning": "Bare definition.", "tier": "foundational"}]}`

**Example, replies that break the rules** (the server won't let the model produce these):
- `"tier": "medium"` breaks it, because `medium` isn't in `TIERS`.
- A missing `reasoning` breaks it, because it's listed under `required`.
- An extra key like `"confidence": 0.9` breaks it, because `additionalProperties` is `False`.

**Why:** with the rulebook in place, the reply is always valid JSON in this exact
shape, so the code doesn't have to guess how to read it. The order of the three
properties matters: `reasoning` comes before `tier`, and the model writes fields in
that order. It has to write its justification first and pick the label second, which
gave better labels in testing.

### Block 4: the instructions template

```python
BATCH_PROMPT_TEMPLATE = """You are tagging software engineering interview-prep questions \
for a study app. ...
Now classify every question below. This topic is: {topic_area}

{questions_block}

Return one classification per question_number listed above, using its exact \
question_number so results can be matched back correctly."""
```
**In plain words:** the full instructions sent to the model, with two blanks
(`{topic_area}` and `{questions_block}`) to fill in later. It includes three worked
examples so the model learns what each label means.

**Example:**
- `"This topic is: {topic_area}".format(topic_area="DBMS")` gives `"This topic is: DBMS"`.
- The `\` at the end of a line joins it to the next line, so two source lines read as one sentence with no line break.

**Why:** the examples are from a different topic so the model learns the rubric
without copying answers into the topic being tagged. The last sentence asks the model
to repeat each question's number, which Block 10 depends on. Because `.format` treats
every `{` and `}` as a blank, this template can't contain literal curly braces.

### Block 5: the function's inputs and output

```python
def classify_topic_batch(client: Groq, topic_area: str, entries: list[dict]) -> dict[int, dict]:
```
**In plain words:** a function that takes an API client, a topic name, and that
topic's entries, and returns a dictionary from question number to a small dictionary.

**Example call:** `classify_topic_batch(client, "DBMS", entries)`.

**Why:** the client is passed in rather than created inside, so the caller controls
it (and tests can hand in a fake one).

### Block 6: build the list of questions

```python
    questions_block = "\n\n".join(
        f"question_number: {e['question_number']}\nQuestion: {e['question']}\nAnswer: {e['answer']}"
        for e in entries
    )
```
**In plain words:** turn each entry into a few lines of text, then join all of them
together with a blank line between.

**Example:** for the first entry, the f-string gives
`"question_number: 1\nQuestion: What is a database?\nAnswer: An organized collection of data."`.
After joining all three:

```
question_number: 1
Question: What is a database?
Answer: An organized collection of data.

question_number: 2
Question: What is a primary key?
Answer: A column that uniquely identifies each row.

question_number: 3
Question: How would you shard a multi-tenant database?
Answer: Split data across servers by tenant...
```

**Why:** the model judges difficulty better when it sees the answer too, and seeing
all questions together lets it judge each one against the others. The keys inside the
f-string use single quotes (`e['question']`) because reusing double quotes would end
the string early on Python 3.9.

### Block 7: fill in the template

```python
    prompt = BATCH_PROMPT_TEMPLATE.format(topic_area=topic_area, questions_block=questions_block)
```
**In plain words:** put the topic name and the question list into the two blanks.

**Example:** `{topic_area}` becomes `DBMS`, and `{questions_block}` becomes the text
from Block 6. `prompt` is now one long string: instructions, three examples, then the
3 real questions.

### Block 8: call the API, retrying if the server hiccups

```python
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
```
**In plain words:** send the prompt to the model. If the server errors, wait a bit and
try again, up to 3 times in total.

**What the request contains:**
- `model=MODEL` says which model to run.
- `messages=[{"role": "user", "content": prompt}]` is a chat with one message: our prompt.
- `max_completion_tokens=4096` caps the reply length. A reply longer than that gets cut off mid-way.
- `response_format=...` with `"strict": True` forces the reply to follow the Block 3 rulebook.

**What the response looks like** (a simplified version): an object where
`response.choices[0].message.content` is a string of JSON text.

**Example, a bad day** (the server fails twice, then works):

| `attempt` | what happens | wait |
|---|---|---|
| 0 | `InternalServerError`, and `attempt` is not 2 | `5 * (0+1)` = 5 seconds |
| 1 | `InternalServerError` again | `5 * (1+1)` = 10 seconds |
| 2 | success, so `break` ends the loop | none |

Total wait is 15 seconds and no error reaches the caller. If attempt 2 had failed
too, `attempt == 2` is true, so `raise` re-throws the error right away with no third
wait.

**Why:** server errors are often temporary, so retrying can fix them. Only
`InternalServerError` is caught. A wrong API key or a malformed request would fail
the same way every time, so those stop immediately. A "too many requests" (429)
error isn't caught here either, which File 3 has to deal with. `response = None`
first just makes sure the name exists.

### Block 9: turn the reply text into Python data

```python
    result = json.loads(response.choices[0].message.content)
```
**In plain words:** take the reply text and convert it into a real Python dictionary.

**Example:** the reply text is
`'{"classifications": [{"question_number": 2, "reasoning": "Assumes you know tables.", "tier": "intermediate"}, {"question_number": 1, "reasoning": "Bare definition.", "tier": "foundational"}, {"question_number": 3, "reasoning": "Design trade-offs.", "tier": "advanced"}]}'`.
After `json.loads`, `result["classifications"]` is a list of 3 dictionaries. Notice
the model returned them in the order 2, 1, 3, not 1, 2, 3.

### Block 10: index the results by question number

```python
    by_number = {}
    for item in result["classifications"]:
        assert item["tier"] in TIERS
        by_number[item["question_number"]] = {
            "tier": item["tier"],
            "reasoning": item["reasoning"],
        }
    return by_number
```
**In plain words:** build a dictionary where the key is the question number, so you
can look up any question's label directly, whatever order the reply came in.

**Example, walking the three items:**
- Item `{"question_number": 2, ...}`: `by_number = {2: {"tier": "intermediate", "reasoning": "Assumes you know tables."}}`
- Item `{"question_number": 1, ...}`: `by_number` now also has key `1`.
- Item `{"question_number": 3, ...}`: `by_number` now also has key `3`.

**Why:** matching by number, not by position, keeps each label with the right
question even if the model reorders, so `by_number[1]` is question 1's label. The
`assert` double-checks the tier is one of the allowed three. It should never fail,
because the rulebook already blocks bad values, and Python skips `assert` when run
with the `-O` flag, so it's only a sanity check. Only `tier` and `reasoning` are
stored, because the number is already the key.

### Final output for the running example

```python
{
  2: {"tier": "intermediate", "reasoning": "Assumes you know tables."},
  1: {"tier": "foundational", "reasoning": "Bare definition."},
  3: {"tier": "advanced",     "reasoning": "Design trade-offs."},
}
```

### The big ideas (short)

**Structured output.** Instead of asking an AI for free text and hoping to parse it,
you hand it a rulebook (a JSON Schema) and the server forces the answer to fit. This
is the AI-engineering way to make a model's output something a program can trust
(Blocks 3 and 8). **Retry with backoff.** Network calls fail for temporary reasons,
so you retry a few times with growing waits, but only for errors that can heal, and
you give up after a limit (Block 8). **Matching by key.** When data comes back from
somewhere you don't control, match it by an ID, never by position (Block 10).

### Watch out for later

- The docstring at the top of the real file is out of date. It says `gpt-oss-20b`,
  "7 topics" and "452 questions", but the code uses `gpt-oss-120b` and the corpus is
  now 8 topics and 503 questions.
- Nothing in this function checks that the model returned every question. If it
  skipped question 2, `by_number` would just lack key 2 with no error. Look for
  whether File 3 catches that.
- One prompt holding a whole topic is too big for Groq's per-minute token limit on
  large topics. That's why File 3 splits each topic into smaller batches.
- The `reasoning` text is saved into the corpus as `difficulty_reasoning`
  (`build_tagged_corpus.py:67`), but no other code reads it. Its real job was making
  the model pick better tiers while writing.

**Understood?** _(pending)_
