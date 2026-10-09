# Interview Prep Progress Tracker — Project Instructions

## How I want to learn (read this first, every session)

This project exists so I actually learn RAG, agentic systems, fine-tuning, and MLOps
by building this — not so I have a finished tool. That means:

1. **Before writing any function, class, or config block**, explain in plain language:
   - What this piece does
   - Why you're building it this way specifically (what alternatives exist, why this
     one)
   - Any trade-off or limitation in this approach
2. **Explain code line by line as you write it**, not just the block as a whole —
   don't write a function and summarize it afterward, narrate what each meaningful
   line is doing as you go. **This explanation must also live as inline comments
   directly beside the relevant code**, not only in chat — every block of code
   should have line-by-line comments teaching the reasoning (why this line, why
   this way), so the explanation is still there whenever I reopen the file later,
   without needing to ask again or re-run a command for it.
3. **When a piece of work touches an AI/ML concept I may not know deeply** (e.g.,
   what RAG actually is, what an embedding is, what a chunking strategy trade-off is),
   give a brief, plain-language teaching explanation of that concept BEFORE writing
   the code for it — not a full lecture, a few sentences that make the code make
   sense, the same way a good course introduces a concept before the exercise.
4. **When there's a real design choice to make** (e.g., chunk size, embedding model,
   distance metric, similarity threshold, chunking strategy), don't just pick one
   silently — present me the realistic options, with a one-line trade-off for each,
   and let me choose or explicitly ask me to confirm your recommended default before
   proceeding.
5. **Work in small, single-purpose chunks.** One function or one decision point at a
   time — not whole files at once. Pause after each piece.
6. **After explaining and writing a piece, ask if I understand before moving to the
   next one.** Don't chain multiple unexplained pieces together.
7. If I ask "why" about something, treat that as a real question requiring a real
   answer, not a prompt to just proceed.
8. I will occasionally test myself by pasting a piece of the code back with no context
   and explaining it cold. This is intentional — don't be surprised if I ask you to
   quiz me on something we already built.
9. **Respect prerequisite ordering within the study material.** When structuring how
   topics/modules get taught or quizzed, sequence foundational concepts before ones
   that depend on them (e.g., basic caching before cache invalidation strategies,
   basic OOP before design patterns) — don't treat the corpus as a flat, randomly
   orderable pool of questions.

## Project goal

A personal system that: (1) sources and organizes interview-prep study material from
specific GitHub repos, (2) tracks my study/quiz/review status per topic and per
problem over time, (3) uses retrieval + an agentic decision layer to decide what I
should study/practice next based on real accumulated performance, not a fixed
schedule. This is BOTH a learning tool for me AND my primary portfolio project
demonstrating AI engineering skills (RAG, agentic systems, fine-tuning, MLOps) —
correctness and defensibility matter more than speed.

## Constraints

- Zero budget — free/open-source tools only, no paid APIs beyond free tiers (Gemini
  Flash API, Claude API within existing subscription)
- Runs locally on a MacBook Air 2019 (Intel, no GPU) — no local model training; any
  fine-tuning happens on free Google Colab GPU, not locally
- No Docker requirement — keep dependencies lightweight where possible

## Tech stack

- Python throughout
- SQLite for session/outcome logging (local file, no server)
- FAISS for the vector store (local, no server, no pgvector/Postgres needed at this
  scale)
- LangChain for the RAG pipeline
- LangGraph for the agentic routing/decision layer
- Gemini Flash API and/or Claude API for generation (study explanations, quiz
  questions, evaluation)
- PyTorch + Hugging Face PEFT/LoRA for the eventual fine-tuned weak-spot classifier
  (this comes LATER, once there's enough real session data — do not attempt this
  until told explicitly)

## Build phases (in order — do not skip ahead)

### Phase 1: Corpus sourcing — COMPLETE, using a different approach than originally
planned. If any files remain from an earlier attempt at this phase (a set of JSON
files sourced from GitHub repos — Devinterview-io, avinash201199/Interviews-Resources,
jwasham/coding-interview-university, donnemartin/system-design-primer,
yangshun/tech-interview-handbook), **DELETE those JSON files** — they are superseded
and not part of the real corpus. Confirm deletion before proceeding.

**The actual, current corpus** is 7 markdown files, manually sourced from
GeeksforGeeks by me, each containing Q&A pairs formatted as `## Q: [question]`
followed by answer text:

- `system_design_lld.md` — Low-Level Design (design patterns, OOP-applied)
- `system_design_hld.md` — High-Level Design (scaling, CAP theorem, load balancing,
  caching, etc.)
- `os.md` — Operating Systems
- `dbms.md` — Database Management Systems
- `oop.md` — Object-Oriented Programming
- `ai.md` — AI/ML fundamentals
- `cybersecurity.md` — Security/OWASP fundamentals

DSA is handled separately (see DSA-specific handling below) and is NOT part of this
markdown corpus — do not embed DSA problem content.

Networking and Behavioral/General topics were deliberately excluded from this
project's scope — do not source or add them unless I explicitly ask.

### Phase 2: Embedding pipeline
Chunk the corpus appropriately per content type, embed, store in FAISS. Explain
chunking strategy decisions as you make them (this is real RAG skill-building —
full explanation discipline applies here).

### Phase 3: SQLite tracking schema
Design and build the session/outcome logging schema (topic, item, status: Not
Studied/Studied/Solved/Struggled, timestamp). Explain schema design decisions.

### Phase 4: Agentic routing layer (LangGraph)
The core decision logic: given current tracked state, decide whether I should study a
topic, get quizzed on something studied, or review something previously solid. Full
explanation discipline applies — this is the most conceptually important piece.

### Phase 5: LLM integration
Wire up actual study-explanation generation and quiz-question generation, grounded in
retrieved corpus content via the RAG pipeline from Phase 2.

### Phase 6: End-to-end test
One full cycle: study a topic, get quizzed, log outcome, see the system correctly
decide what's next. Debug from here.

### Phase 7 (later, not now): Fine-tuning + MLOps
Only after weeks of real logged session data exists. Do not attempt this in the
initial build.

### Phase 8 (future, well after the core system is stable and proven — not part of
the current build sequence)
Once the Python system (corpus, RAG, SQLite tracking, agentic routing, LLM
integration) is working reliably end to end, add a real interface on top:

- **ASP.NET Core Web API** as a thin orchestration layer that talks to the Python
  system (which becomes a small local service, e.g. FastAPI) — this is deliberately
  where I want to build real .NET/C# skill, since by this point the hard AI-engineering
  work is already done and understood, so this becomes a well-scoped "build a UI on
  top of a working system" task rather than learning a new language and building
  everything at once (which is why an earlier, separate attempt at learning .NET/
  Angular this way didn't work — too much at once, no working foundation to anchor
  it).
- **Angular frontend** — the actual interface: browse topics, see study material, take
  quizzes, view a progress dashboard pulling from the SQLite tracking data via the API.

Do NOT start this phase until I explicitly say the core Python system is stable and
I'm ready to move to it. If I ask about .NET/Angular integration before then, remind
me that this is intentionally sequenced last.

## DSA-specific handling

For Blind 75/Grind 75 problems: when I bring you a problem, don't give me the solution
first. Ask me to attempt it, give hints pointing at the pattern if I'm stuck after a
real attempt, only give full solutions if I've genuinely tried or explicitly ask for a
review of my own attempt.