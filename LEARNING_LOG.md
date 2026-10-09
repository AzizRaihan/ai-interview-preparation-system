# Learning Log

A running record of what we built, in order, and why — kept per the teaching rules in
CLAUDE.md (explain before coding, small chunks, no skipping ahead). Append an entry
after each piece of work; don't edit past entries except to fix mistakes.

## How to add an entry

Copy this template to the bottom of the log:

```
## YYYY-MM-DD — <short title>

**Phase:** <build phase from CLAUDE.md, e.g. Phase 1: Corpus sourcing>

**What we did:**
- ...

**Why this way (alternatives considered):**
- ...

**Trade-offs / limitations:**
- ...

**Understood?** <yes / not yet — revisit>
```

---

## 2026-08-29 — Fetch script for system-design-primer

**Phase:** Phase 1: Corpus sourcing

**What we did:**
- Wrote `scripts/fetch_system_design_repo.sh`, which shallow + partial clones
  `donnemartin/system-design-primer` and sparse-checks-out only `README.md` and
  `solutions/system_design/*/README.md` into `data/raw/system-design-primer/`.
- Explicitly excluded `solutions/object_oriented_design/*` — inspected it and found
  those are Jupyter notebooks/code, not prose, and OOP content is already sourced from
  a dedicated repo per CLAUDE.md's Phase 1 plan.

**Why this way (alternatives considered):**
- `git clone --depth 1 --filter=blob:none --sparse` instead of a plain clone: avoids
  downloading `images/` and full history entirely, rather than downloading then
  deleting it.
- Considered fetching via GitHub REST API / raw.githubusercontent.com per-file instead
  of cloning — rejected because it hits unauthenticated rate limits (60 req/hr) across
  9+ files and is more code for the same result.
- Sparse-checkout needed `--no-cone` mode with explicit leading-slash patterns —
  default "cone mode" only accepts whole directories, not file globs like
  `*/README.md`.

**Trade-offs / limitations:**
- Depends on git 2.19+ for `--filter` support (fine on current macOS).
- Re-running the script does a fresh clone each time (`rm -rf` first) rather than
  incrementally updating — fine for a one-time corpus build, would need a `git pull`
  variant if we wanted to refresh this regularly later.

**Understood?** yes

---

## 2026-08-29 — Extractor for the 8 solved-question READMEs

**Phase:** Phase 1: Corpus sourcing

**What we did:**
- Wrote `scripts/extract_system_design_solutions.py`. Confirmed all 8
  `solutions/system_design/*/README.md` files open with exactly one `# Title` line,
  then split each file into `title` (the H1) + `content` (everything after, as one
  whole block — subheadings like "Step 1", "Step 2" stay inside `content`).
- Ran it: 8/8 entries extracted cleanly into `data/corpus/system_design_solutions.json`,
  14–20K chars of content each, `topic_area="System Design"`, `difficulty=null`
  (not available for these).

**Why this way (alternatives considered):**
- Plain string `partition("\n")` split instead of a markdown-parsing library
  (`markdown-it-py` etc.) — justified because the format is verified uniform (single
  ATX `# ` heading, no setext `===` headers) across all 8 files; a full parser would be
  unjustified complexity for content this consistent.
- Kept each file as one whole entry rather than chunking by `## Step N` — chunking
  strategy is a Phase 2 decision (embeddings), not a Phase 1 (raw extraction) one.

**Trade-offs / limitations:**
- Fragile to upstream format drift: if a file's H1 style changes, the split silently
  mis-parses instead of erroring loudly. Acceptable for a source we've already
  hand-inspected and that changes rarely.

**Understood?** yes

---

## 2026-08-30 — Extractor for README.md topic sections

**Phase:** Phase 1: Corpus sourcing

**What we did:**
- Mapped every `#`/`##`/`###` heading in the main `README.md` (85 headings) to find
  the boundary between navigation/meta content and genuine topic prose.
- Decided scope with you: only the 15 `##` sections from "Performance vs scalability"
  through "Security" are real topic explanations worth extracting. Everything before
  (Motivation, Contributing, Index, Study guide, an index-only list of the solved
  questions already extracted separately) and everything after (`## Appendix` onward —
  powers-of-two table, latency numbers, bare link lists to external blogs) is
  navigation or reference material, not prose to quiz on.
- Wrote `scripts/extract_system_design_topics.py`: slices `README.md` between those
  two heading markers, then splits on `## ` boundaries into one entry per topic
  (subheadings like "Source(s) and further reading" stay inside that topic's
  `content`, same whole-unit approach as the solutions extractor).
- Ran it: 15/15 entries extracted, matching the heading count exactly (401–19,950
  chars each — "Database" and "Communication" are the largest since they cover several
  subtopics).

**Why this way (alternatives considered):**
- Same line-based split-on-heading approach as the solutions extractor, justified the
  same way: headings here are consistently ATX-style, confirmed by grepping the whole
  file first rather than assuming.
- Considered including the Appendix's link lists as entries too — rejected (with you)
  since they're bare links/tables, not explanatory prose, and wouldn't be useful
  grounding content for the RAG step.

**Trade-offs / limitations:**
- The start/end heading strings (`"## Performance vs scalability"`, `"## Appendix"`)
  are hardcoded — if upstream renames either section, this breaks (loudly, via the
  `next()` call raising `StopIteration`, so at least it won't silently mis-scope).

**Understood?** yes

---

## 2026-08-30 — OOP corpus (Devinterview-io/oop-interview-questions)

**Phase:** Phase 1: Corpus sourcing

**What we did:**
- Fetched the repo (single `README.md`) and extracted it into `data/corpus/oop.json`.
- Found the file's title claims "52 Important OOP Interview Questions" but only 15 are
  actually answered in-repo (`## 1.` through `## 15.`) — the rest are paywalled on
  devinterview.io. Extracted the 15 that exist rather than the advertised 52.
- Stripped a trailing promo footer ("Explore all 52 answers here...") from the last
  entry's content, and stripped markdown emphasis (`_..._`, `**...**`) from question
  titles for cleanliness.
- 15/15 entries extracted, `topic_area="OOP"`, `difficulty=null`.

**Understood?** yes (per your instruction — moving through extraction mechanics
without a pause-to-explain step for this kind of data-wrangling work)

---

## 2026-08-30 — DBMS/OS/Networking corpus (avinash201199/Interviews-Resources, PDFs)

**Phase:** Phase 1: Corpus sourcing

**What we did:**
- These sources turned out to be PDFs (`DBMS Interview Questions.pdf`, `Operating
  System Interview Question.pdf`, `Networking Interview Questions.pdf`), not markdown
  — first PDF source in the corpus. Used PyMuPDF (`fitz`), already installed, no new
  dependency needed.
- All three are scraped-webpage-to-PDF exports with the same numbered "N) Question"
  format, and the same two quirks: stray share-count sidebar lines (e.g. "54.6M")
  injected mid-text, and in-answer numbered sub-lists that falsely match the same
  heading pattern (e.g. OS Q18's answer contains "1) Mutual Exclusion... 2) Hold and
  Wait...", which would've corrupted the split into 5 fake entries).
- **Real bug caught and fixed:** a heading is only accepted as a new question if its
  number is strictly greater than the last accepted one — not "exactly +1", because
  the Networking file has a genuine gap in its real numbering (28 → 30, no 29 in the
  source) that a stricter rule would've broken on.
- Verified the fix: OS Q18 stayed one whole entry with the sub-list intact; DBMS/OS/
  Networking extracted 52/39/46 entries respectively, matching their real (not
  necessarily consecutive) numbering ranges exactly.
- Wrote one shared script (`scripts/extract_interviews_resources_pdfs.py`) rather than
  three near-identical ones, since all three sources share the exact same format and
  bug.

**Known limitation (disclosed, not fixed):** ~10-15% of titles are truncated mid-
sentence by PDF line-wrapping (e.g. "What is the difference between a DELETE command
and") — cosmetic only, since `content` still carries the full question+answer text
immediately after. Didn't build a repair heuristic for this: tried a few
(ending-punctuation checks), none were reliable — some genuine complete titles have no
trailing "?" (e.g. "Explain ACID properties"), so a repair rule risks corrupting good
titles to fix bad ones. Also left one single-line sidebar-title leftover
("OOPs Concepts in Java") inside DBMS entry 2 — same reasoning, not worth a fragile
targeted rule for one inert line in a 294K-char corpus.

**Corpus running total:** 175 entries, ~294K chars across 6 JSON files.

**Understood?** yes

---

## 2026-08-30 — Behavioral corpus (yangshun/tech-interview-handbook)

**Phase:** Phase 1: Corpus sourcing

**What we did:**
- Found `tech-interview-handbook` is now a full Docusaurus monorepo (the site's
  actual source), not a plain markdown-questions repo — content pages live under
  `apps/website/contents/`.
- Scoped to the 4 `behavioral-interview*.md` files (not just the literal
  "-questions" one CLAUDE.md named, since `behavioral-interview.md`,
  `-rubrics.md`, and `-senior-candidates.md` are all clearly in-scope behavioral
  content, not System Design — the excluded topic per CLAUDE.md).
- Stripped each file's YAML frontmatter, then split on `## ` sections, same
  whole-unit approach as prior extractors.
- 22/22 sections extracted across all 4 files, matching heading counts exactly
  (160–10,807 chars each — company-specific question lists are short, the prep
  guidance ones are longer prose).

**Corpus running total:** 197 entries, ~317K chars across 7 JSON files.

**Understood?** yes

---

## 2026-08-30 — DSA corpus (Grind 75) — last Phase 1 source

**Phase:** Phase 1: Corpus sourcing

**What we did:**
- techinterviewhandbook.org/grind75 redirects to a separately-hosted client-rendered
  Next.js app (grind75.pages.dev) with no static markdown and no public JSON/API —
  the problem list only exists once JS renders it in a real browser. Used Chrome
  browser automation to load the live page, switched its view to "Group by Topics" to
  get pattern/category per problem, and read the rendered text.
- Saved that as a raw transcript (`data/raw/grind75/scrape.txt`) for provenance, then
  wrote `scripts/extract_grind75.py` to parse it into JSON — per CLAUDE.md scope, only
  title/difficulty/pattern, no full problem statements.
- 75/75 entries extracted, difficulty split (Easy 24 / Medium 42 / Hard 9) matches the
  site's own summary counts exactly.
- This was the last of the 7 Phase 1 sources named in CLAUDE.md.

**Corpus final Phase 1 total:** 272 entries across 8 JSON files in `data/corpus/`
(system_design_solutions: 8, system_design_topics: 15, oop: 15, dbms: 52, os: 39,
networking: 46, behavioral: 22, dsa: 75).

**Understood?** yes

---

## 2026-08-30 — GeeksforGeeks replaces thin sources (OOP/DBMS/OS/Networking/Behavioral)

**Phase:** Phase 1: Corpus sourcing

**What we did:**
- On your request, pulled 5 GeeksforGeeks pages (real server-rendered HTML, no bot
  block hit) to replace/prioritize over the thinner repo-based sources:
  OOP, DBMS, OS, Networking, HR/Behavioral.
- Built a shared HTML extractor (BeautifulSoup + lxml, newly installed): splits each
  page's single `<div class="text">` article body on `<h3>` headings. Numbered
  headings ("N. Question") become entries with the number stripped; a small set of
  confirmed-empty/link-only footer headings ("Related Article", "Resources:", etc.)
  are dropped; everything else (e.g. "Types of VPN", "Additional Tips for HR
  Interview") is kept as its own standalone entry — the schema's `question_or_topic`
  field covers topics as well as questions, so this isn't a hack.
- Caught and fixed two real content-quality bugs before finalizing: diagram
  `<figcaption>` text (e.g. a literal typo "Kernal") was bleeding into answers via
  `get_text()` — fixed by dropping `<figure>` elements; and DBMS comparison tables
  were flattening into unreadable run-on text — fixed with a dedicated table-to-text
  formatter (`col1 | col2` rows) so the DBMS/RDBMS-style comparison tables stay
  legible.
- Verified zero suspiciously-short/empty entries across all 5 files after fixes.
- Renamed files so GeeksforGeeks is now the primary source per topic
  (`oop.json`, `dbms.json`, `os.json`, `networking.json`, `behavioral.json`), and
  renamed the original repo-based extractions to `*_supplementary.json` — kept, not
  deleted, since they still add some real coverage and dedup logic can merge in
  anything GfG missed.

**Yield comparison (old repo source -> new GfG primary):**
- OOP: 15 -> 29 entries
- DBMS: 52 -> 58 entries (similar count, but GfG answers are meaningfully deeper —
  the old avinash PDF source was terse javatpoint-scrape content)
- OS: 39 -> 103 entries (biggest gap — old OS source was both thin in count and
  ~1-2 sentence answers; GfG's OS page is the single largest source in the corpus)
- Networking: 46 -> 73 entries
- Behavioral: 22 -> 26 entries, plus more concretely practical (STAR method,
  concrete prep-tips list) alongside the company-specific question lists

**Corpus totals after this change:** system_design_solutions (8) + system_design_topics
(15) + dsa (75) + oop (29) + dbms (58) + os (103) + networking (73) + behavioral (26)
= **387 primary entries**, plus 174 in the 5 supplementary files, not yet merged in.

**Understood?** yes

---

## 2026-09-04 — CLAUDE.md updated; corpus approach changed; all GitHub-repo JSON deleted

**Phase:** Phase 1 → Phase 2 transition

**What happened:**
- CLAUDE.md was rewritten (new "How I want to learn" points: explain code line-by-line,
  teach AI/ML concepts before implementing, present real config choices, respect
  prerequisite ordering). Phase 1 is now marked COMPLETE with a different corpus
  approach: 7 hand-sourced GeeksforGeeks markdown files (`system_design_ULD.md`,
  `system_design_HLD.md`, `os.md`/`OS.md`, `dbms.md`/`DBMS.md`, `oop.md`, `ai.md`/
  `AI.md`, `cybersecurity.md`) replace all the GitHub-repo extraction work from the
  previous session. **Networking and Behavioral are now explicitly out of scope.**
  DSA stays separate, not embedded.
- Deleted all 13 leftover JSON files from the prior session's repo-based extraction:
  7 matched CLAUDE.md's named repos exactly (Devinterview-io, avinash201199 x3,
  donnemartin x2, yangshun); the other 6 (oop/dbms/os/networking/behavioral.json,
  all geeksforgeeks.org-sourced but pre-dating this corpus) didn't literally match
  "from GitHub repos" — asked you directly rather than guess, you confirmed deleting
  5 of them (oop/dbms/os as superseded duplicates, networking/behavioral as
  out-of-scope) and keeping `dsa.json` (Grind 75 metadata, separately handled).
- `data/corpus/` is now exactly: the 7 real markdown files + `dsa.json`.
- Caught and corrected a filename mismatch inside CLAUDE.md itself: its text says
  `system_design_lld.md`, the real file is `system_design_ULD.md` — flagged rather
  than silently normalized.

**Understood?** yes — moving into Phase 2 (embedding pipeline) next, scoped to the
7 markdown files only.

---

## 2026-09-04/05 — Phase 2 parsing and difficulty tagging (backfilled)

**Phase:** Phase 2: Embedding pipeline

**Note:** this entry and the next two were written after the fact — logging lapsed
for a while during some heavy debugging. Backfilling now.

**Parsing:**
- Each markdown file uses `## Q<N>: question` headings. The parser reads each file
  line by line and treats everything until the next heading as that question's answer.
- Chunking: one chunk per Q&A pair, confirmed with you. No further splitting.
- 452 entries from the 7 original files, later 503 once QA.md was added.

**Difficulty tagging (foundational/intermediate/advanced):**
- Decided to use an LLM to tag each question, not rules or manual tagging.
- First attempt (Gemini, one question at a time) gave inconsistent results — e.g. it
  tagged basic OOP comparison questions as "intermediate" just because they were
  phrased as comparisons, even when both sides were simple concepts.
- Fixed by: asking the model to explain its reasoning before giving a tier, adding
  a few worked examples to the prompt, and classifying a whole topic's questions
  together instead of one at a time (so it can judge difficulty relative to real
  neighbors, not in isolation).

**Understood?** yes

---

## 2026-09-05 — Switching from Gemini to Groq (backfilled)

**Phase:** Phase 2: Embedding pipeline

**What happened:**
- Gemini's real free daily limit turned out to be only 20 requests — much lower
  than the numbers I'd found online and quoted earlier. Lesson: don't trust
  published rate-limit numbers, only trust what the live API actually says.
- Switched to Groq instead, which is much more generous and still free.
- First model tried (`gpt-oss-20b`) gave noticeably worse tagging quality — it
  missed the four core pillars of OOP as "foundational." Switched to the bigger
  `gpt-oss-120b`, which matched Gemini's quality at no extra cost.
- Groq had its own limits we had to work around: a cap on tokens per request (fixed
  by splitting each topic into smaller batches), and a cap on tokens per day that
  slowly refills over 24 hours rather than resetting all at once.
- Found and fixed a real bug: the tagging script only saved results at the very end
  of a full run, so any failure partway through lost everything already done. Now it
  saves after every small batch instead.
- Used an automatic retry loop that kept trying every few minutes until the daily
  quota freed up enough. Took about 20 tries over roughly an hour.

**Result:** all 503 questions tagged, saved to `data/corpus/tagged_entries.json`.

**Understood?** yes

---

## 2026-09-05 — Embedding strategy: what it is, and our choices

**Phase:** Phase 2: Embedding pipeline

**What an embedding is:**
A list of numbers representing what a piece of text *means*. Texts with similar
meaning end up as numbers that are close together, even if they don't share any
words. That's what lets us search by meaning instead of by keyword: a study
question you type gets turned into numbers the same way, and whichever saved
questions are "closest" get pulled up as relevant.

**Choices we made:**
- What to embed per question: the question and answer together, not just one or
  the other. This is the normal default for this kind of Q&A search.
- How to measure "closeness": cosine similarity (comparing the angle between two
  sets of numbers, not their size). In practice this means normalizing every vector
  first, then using a fast "inner product" search — mathematically the same result,
  just quicker to compute.
- Already decided by our corpus's small size (503 entries): we don't need any of
  FAISS's fancier, larger-scale search modes. The simple exact-search mode is fine.

**Understood?** pending — embedding code not yet written.

---

## 2026-09-05 — What depends on embeddings, and the wider RAG landscape

**Phase:** Phase 2: Embedding pipeline

**What depends on embeddings in this project:**
- Embeddings only exist to power one thing: finding which of our 503 questions are
  relevant to whatever you're studying right now (retrieval).
- Phase 4 (deciding what to study/quiz next) needs this to find the right content.
- Phase 5 (generating explanations/quizzes) needs this so the LLM's answer is
  grounded in our actual corpus, not just made up from general knowledge.

**Other RAG strategies, and whether we need them:**
- **Semantic caching** — reuse a past answer if a new question is similar enough,
  instead of asking the LLM again. Saves API calls. Not built yet, but worth adding
  later given how tight some of today's free quotas turned out to be.
- **GraphRAG** — instead of treating each question independently, build a map of how
  concepts relate to each other and search that map. Useful for large,
  cross-referenced knowledge bases. Not needed for us — our topic + difficulty tags
  already give us a lightweight version of this.
- **Hybrid search** — combine meaning-based search with plain keyword search, so
  exact terms (like "CAP theorem") aren't missed. A reasonable future upgrade, not
  urgent now.
- **Re-ranking** — fetch a wide set of results cheaply, then re-sort the top ones
  with a heavier, more accurate model. More useful at bigger scale than 503 entries.
- **Agentic RAG** — an LLM decides what to retrieve and when, instead of always doing
  the same fixed steps. This is exactly what Phase 4 already is in our plan.

**Our choice:** basic retrieval (embed + FAISS + similarity search) for Phase 2/5,
and agentic RAG for Phase 4. Skipping the rest for now — they solve problems that
show up at a bigger scale than our project has.

**How Phase 4's agent will actually decide what to retrieve:**
Unlike a general chatbot deciding *whether* to search at all, our agent's job is
simpler: retrieval is basically always needed. The real decision is *what kind* of
retrieval to do — which topic, which difficulty level, and whether to study
something new, quiz something already studied, or review something solid — based on
your tracked progress in SQLite (Phase 3), not open-ended reasoning.

**Understood?** yes

---

## 2026-09-05 — Is our embedding choice risky? Cost and token trade-offs

**Phase:** Phase 2: Embedding pipeline

**An unverified risk, flagged rather than assumed away:**
- Today we learned Gemini's generation model had a real daily limit far stricter
  than published numbers said. We have NOT yet checked whether the embedding model
  has the same kind of surprise — we've only made two test calls, which isn't real
  evidence either way.
- Plan: embed a small batch first (one topic, ~30 questions) and watch for errors,
  before running all 503 — same caution we used for tagging.

**Do fancier embedding methods cost more?**
- Yes. A bigger embedding model is slower per call, and in practice tends to have
  a tighter free daily limit (we saw this happen twice today already).
- Add-on strategies like GraphRAG or re-ranking cost *extra*, on top of the base
  embedding cost — they don't replace it. GraphRAG needs extra calls to build the
  concept map; re-ranking needs another model call per result.

**Once the whole system is built, will each study session cost more or fewer tokens
than just using a free chatbot directly?**
- More, per interaction. A plain chatbot question uses only your question plus its
  answer — no extra steps. Our system also embeds your query (cheap) and stuffs
  1-3 retrieved questions into the prompt as grounding context, which adds several
  hundred extra tokens per answer.
- That's not a fair straight comparison though — a plain chatbot can't track your
  progress over time, can't guarantee its answer matches your specific study
  material, and can't decide what you should study next. The extra tokens buy those
  things.
- At our actual scale (a personal project, a handful of study sessions a day), that
  extra cost is tiny compared to any free tier we've looked at — more expensive
  per call, but not a real practical problem for this project.

**Also created:** `/log-teaching` — a command that logs the most recent teaching
moment from the conversation into this file, in this same easy-to-read style,
without you needing to ask each time.

**Understood?** yes

---

## 2026-09-05 — FAISS, taught plainly

**Phase:** Phase 2: Embedding pipeline

**What FAISS is:**
- A library that stores a big pile of vectors and quickly answers one question:
  "which stored vectors are closest to this new one?" It doesn't know what a
  question or topic is — it just stores numbers and does distance math on them.

**How it actually works:**
- You add your vectors one batch at a time. FAISS gives each one a plain position
  number in the order you added them (0, 1, 2, ...) — nothing meaningful like
  "question 14," just a position.
- Our index type is `IndexFlatIP` — "Flat" means no shortcuts, it truly compares
  against every stored vector (fine at our size, 503 entries). "IP" means inner
  product, the actual math used to score closeness — equivalent to cosine
  similarity once vectors are normalized, which we already decided to do.

**The important gotcha:**
- FAISS only gives back a position number and a score — never the original text.
  So we have to keep our own list, in the exact same order the vectors were added,
  to translate "position 47" back into the real question/answer/topic. If that
  list and the FAISS index ever get out of sync, every lookup silently points to
  the wrong entry with no error.

**Saving to disk is two separate files:**
- FAISS has its own save function for the index itself (not plain JSON — it's a
  specialized format).
- The metadata list (question, answer, topic, tags) is saved separately, as normal
  JSON, same as everything else so far.

**Understood?** yes

---

## 2026-09-05 — Making vector search faster at large scale

**Phase:** Phase 2: Embedding pipeline

**The question:** if FAISS compares a query against every stored vector, isn't that
slow once you have a lot of vectors?

**Yes, and there are established ways to fix it:**
- **Clustering first (IVF):** group all vectors into clusters ahead of time. At
  search time, only check the closest few clusters instead of everything. Faster,
  but approximate — the true best match could technically be in a cluster you
  didn't check.
- **Graph search (HNSW):** link each vector to a handful of nearby ones, forming a
  web. Searching means hopping toward vectors closer to your query instead of
  scanning everything. Fast and accurate, costs more memory.
- **Compression (Product Quantization):** shrink each vector to a smaller,
  approximate version so comparisons are cheaper. Often combined with clustering.
- These are just different FAISS index types — same library, swap in a different
  one.

**A simpler trick we already get for free:** filter by topic first. If you're
studying OS, you only need to search OS's ~103 entries, not all 503 — no fancy
algorithm needed, just using the topic tag we already have.

**Why we're not using any of this now:** at 503 vectors, brute-force search takes a
few milliseconds — faster than the network delay just to call the embedding API in
the first place. These techniques solve a real problem, but only at a much bigger
scale (millions of vectors) than we have.

**Understood?** yes

---

## 2026-09-05 — Embedding pipeline built and run on all 503 entries

**Phase:** Phase 2: Embedding pipeline — complete

**What we built (`scripts/build_embeddings.py`):**
- For each entry, combine question + answer into one piece of text (our earlier
  decision), and send it to Gemini's embedding model, tagged as
  `task_type="RETRIEVAL_DOCUMENT"` since it's stored content to be searched later.
- Normalize each vector to length 1, then add them all to a FAISS index.
- Save the FAISS index and a matching metadata file (same order, so positions line
  up) to disk.

**Two real limits found while running it (not guessed, discovered live):**
- The embedding API only accepts 100 texts per call, so we split our 503 entries
  into 6 batches.
- There's also a 100-requests-per-minute limit. Added a retry that waits and tries
  again if we hit it — much milder than today's earlier Groq daily-limit problem,
  since this one clears itself in under a minute.

**Result:** all 503 entries embedded, saved to a FAISS index
(`data/corpus/faiss_index.bin`) and a matching metadata file
(`data/corpus/embedding_metadata.json`). Double-checked the two files line up
correctly, and a test search returns sensible, expected results.

**Understood?** yes — Phase 2 (embedding pipeline) is done. Next up per the build
order: Phase 3, the SQLite tracking schema.

---

## 2026-09-06 — Phase 3: SQLite tracking schema, first pieces built

**Phase:** Phase 3: SQLite tracking schema

**Decisions made:**
- Keep a full history of every study/quiz attempt (an event log), not just the
  latest status. This matches the project's goal of deciding what to study next
  based on real accumulated performance, not just one snapshot.
- DSA is excluded from this tracking too, same as it's excluded from the corpus —
  so an item is identified simply by `topic_area` + `question_number`.
- No separate "session" grouping for now — a timestamp is enough, and sessions can
  always be reconstructed later if needed.
- "Current status" for an item is worked out by asking for its most recent log
  row, not kept in a separate summary table. Simpler, and only one place holds the
  truth.

**What we built (`scripts/tracking_db.py`):**
- A `study_log` table: one row per attempt, with topic, question number, status,
  and a timestamp. The database itself rejects any status that isn't "Studied",
  "Solved", or "Struggled" — a typo can't slip through.
- "Not Studied" is never actually stored as a row — it just means no rows exist yet
  for that item.
- A function to log a new attempt, and a function to look up an item's current
  status (its most recent row).

**A real bug fixed along the way:** used a newer Python type-hint style (`str |
None`) that only works on Python 3.10+, but this project runs on 3.9. Fixed with
one line at the top of the file that makes type hints lazy, so this can't happen
again in this file.

**Tested it:** logged the same item through Studied → Struggled → Solved, all
within the same second (so all three got an identical timestamp) — and the
"current status" lookup still correctly returned the true most recent one each
time, thanks to a secondary tiebreaker. A separate, untouched item stayed
unaffected, and all three log rows are still there, nothing overwritten.

**Understood?** yes

---

## 2026-09-06 — Prerequisite chains built for all 8 topics

**Phase:** Phase 3 extension: prerequisite graph

**What we built:**
- Realized the difficulty tiers (foundational/intermediate/advanced) weren't
  actually enough on their own — they group questions into rough buckets, but say
  nothing about which *specific* question depends on which other one. Decided to
  build a real dependency graph instead: each question gets a list of the exact
  other questions (in the same topic) it assumes you already understand.
- An LLM identifies these dependencies by reading a topic's questions together and
  judging, per question, what it actually builds on — not just similarity, real
  content grounding.
- Kept this cleanly separate from plain graph math: a completely different piece
  of code (no LLM involved) turns the raw dependencies into an actual study order,
  and can prove whether the graph is even valid (no circular "A needs B needs A"
  loops).
- Added two automatic safety checks after tagging: drop any reference to a
  question that doesn't exist, and drop any case where a "foundational" question
  claims to need something tagged "intermediate" or "advanced" (that direction
  never makes sense).

**A real limit hit and fixed:** big topics (DBMS, OS, etc.) were too large to send
to the model in one request. Fixed by splitting into smaller groups — but that
means a group can only ever see its own questions, so a true dependency between
two *different* groups in the same topic could be missed. To keep this honest, we
made sure each group's output is only checked against its own questions, not the
whole topic — so nothing gets accepted unless it was actually possible for the
model to have seen it.

**Result — all 8 topics done, checked one at a time before moving to the next:**
- 503/503 questions now have a dependency list.
- Every topic produced a fully valid order — no circular dependencies anywhere.
- A small number of tier-violations got caught and dropped automatically in every
  topic (expected, and proof the safety check works).
- Spot-checked real connections across topics and they hold up: RAG correctly
  needs Vector Databases, Dependency Injection correctly needs Interfaces and
  SOLID, Digital Signatures correctly need RSA, TCP/IP correctly needs the OSI
  model.
- One honest, non-blocking observation: in one topic (System Design LLD), a few
  genuinely independent, foundational questions ended up placed at the very end
  of the sequence, purely because of how ties get broken when several questions
  are equally ready to study. Worth improving later, doesn't break correctness.

**Understood?** yes

---

## 2026-09-06 — Directed graphs and topological sort, taught plainly

**Phase:** Phase 3 extension: prerequisite graph

**Why the graph has to be directed:**
- A regular (undirected) connection just says "these two are related" — no notion
  of order, like how similar two things are.
- A prerequisite is different: "B needs A" is not the same as "A needs B." The
  arrow has to point one specific way, or the whole idea of "study this before
  that" doesn't mean anything.

**How you turn a list of "X needs Y" facts into an actual study order:**
- Start by finding every question with zero prerequisites — those are ready to
  study right away.
- Pick one, add it to the list. Then check: did anything depend on it? If so,
  cross that dependency off. Anything that just lost its last remaining
  prerequisite becomes newly ready.
- Repeat until everything is placed.
- Worked through a small example: if C needs A, and D needs C, the order ends up
  A, (anything else with no dependencies), C, D — never D or C before A.

**Why this also catches broken (circular) dependencies for free:**
- If two questions end up needing each other in a loop, neither one can ever
  become "ready" — they're each waiting on the other forever.
- So if you reach the end of this process and some questions were never placed,
  that's proof a loop exists. No separate check needed — it falls out of the same
  process.

**Important split we kept throughout:** the LLM only ever decides the raw facts
("B needs A"). Turning those facts into an order, and checking whether the graph
is even valid, is plain code with no AI involved — fully reliable, unlike the
LLM's judgment calls.

**Understood?** yes

---

## 2026-09-09 — Fixed the tie-breaking rule in the study order

**Phase:** Phase 3 extension: prerequisite graph

**The problem:** when several questions were all equally ready to study (no real
prerequisites blocking any of them), the order used to just pick whichever had the
lowest original question number. That meant some genuinely foundational,
independent questions (a few basic OOP recap questions in the LLD topic) ended up
placed near the very end, just because of their number.

**The fix:** tie-break by difficulty tier first (foundational before intermediate
before advanced), and only fall back to question number if the tier is the same
too.

**Checked it worked, using data we'd already saved (no new tagging, no API calls
needed):**
- Two of the four questions that were misplaced before (Abstraction vs.
  Encapsulation, Polymorphism — both tagged foundational) moved way earlier, from
  near the end to roughly the middle of the list.
- The other two (Inheritance vs. Composition, Interface vs. Abstract Class) barely
  moved — and that's actually correct, not a leftover bug: those two are tagged
  "intermediate," so they're supposed to wait behind foundational content.
- Re-checked all 8 topics after the change: still fully valid everywhere, no
  circular dependencies introduced.

**Understood?** yes