---
description: Teach the next file of the codebase block by block with a running example, append it to codebase.md, then quiz me before moving on
---

This command drives the file-by-file codebase walkthrough kept in `codebase.md`
(project root). Do exactly one file per invocation, then stop and wait.

**Who this is for:** someone who can solve LeetCode-style problems but has always
had AI write real software, and wants to understand code well enough to write it
alone. They cannot yet "connect the dots" between a line of code and how it changes
the output. Line-by-line explanation with concrete values is the TOP PRIORITY of
this whole command; everything else is secondary and must stay short.

**Step 1 -- figure out where we are.** Read `codebase.md`. It has an ordered list of
files and one lesson section per file taught so far, each ending in an
`**Understood?**` line.
- If $ARGUMENTS names a specific file, teach that one.
- Otherwise, if the most recent lesson still says `_(pending)_` and I have NOT yet
  answered its quiz in this conversation, don't move on -- re-ask that quiz
  (briefly) and wait.
- If I HAVE just answered a quiz: grade it honestly (what was right, what was
  missing or wrong, the correct version), update that lesson's `**Understood?**`
  line in `codebase.md` to `yes` / `partly: <what to revisit>`, and only then
  continue to the next file in the list.
- Otherwise teach the next file in the list that has no lesson yet.

**Step 2 -- read the real source file in full** before writing anything. Never
teach from memory; the file may have changed.

**Step 3 -- teach it in this exact format**, appended to the end of `codebase.md`
(never rewrite earlier lessons unless I ask) AND given in chat:

1. `## File N: scripts/<name>.py` heading.
2. **What it does** -- 2 to 3 plain sentences: its job, where it sits in the
   pipeline, and what it receives and returns.
3. **Running example** -- ONE tiny concrete input (a few lines of data, 2-3 items)
   invented for this file, shown in a code block. This same example is carried
   through every block below so the reader watches the same data change.
4. **Block by block** (the main part, the bulk of the lesson). Split the file into
   small blocks of roughly 1-6 lines, in file order. Every block uses exactly this
   layout:
   - `### Block N: <short plain-words title>`
   - the code, in a fenced snippet (exact lines from the real file)
   - **In plain words:** one or two simple sentences, everyday language.
   - **Example:** the running example going THROUGH this block -- show the actual
     values of the variables/arguments before and after (`x = ...` then `x = ...`),
     the real return value, or what a call produces. For lines inside a loop or an
     `if`, show at least one iteration or branch that fires, and one that doesn't.
     Use small built-in demonstrations for unfamiliar operations (e.g.
     `"\n".join(["a","b"])` gives `"a\nb"`). For API calls, show the shape of the
     request and of the response instead of the network.
   - **Why:** why this line exists / why this way and not the obvious alternative.
     Add "If you deleted this line: ..." when the consequence is instructive.
   Do not skip lines that are boring; every meaningful line appears in some block.
   Read regexes, format strings, comprehensions and call arguments piece by piece.
5. **Final output** -- the finished result for the running example after all blocks.
6. **The big ideas (short)** -- at most 2 or 3 short paragraphs naming the general
   CS / software-engineering concepts this file is an instance of (state machine,
   closure, retry with backoff, structured output, append-only log...), each in
   plain language: what it is, and where it showed up in the blocks above. Keep it
   brief; the blocks already taught the substance. Teach any AI/ML concept the file
   relies on (embedding, rate limit, structured output) in a couple of plain
   sentences, placed just before the first block that uses it.
7. **Watch out for later** -- 1 to 3 bullets: real subtleties, stale comments, or
   forward links to the files where a detail returns.
8. `**Understood?** _(pending)_`

Style rules: plain language over jargon (define any term the first time it
appears); short sentences; concrete values over abstractions; never assume a
production idiom is obvious; never say "simply" or "just". If a line's effect can be
shown as `before -> after`, show it that way.

**Step 4 -- quiz.** After appending, ask exactly 3 short questions in chat, tied to
the running example: (1) "what is the value of X after block N?" style prediction,
(2) "why is line/block Y there, or what breaks without it?", (3) one edge case or
how this file connects to a later one. Do not include answers. Then STOP -- do not
start the next file until I answer and run `/codebase` again.

Do not modify any source code in `scripts/` while teaching; this command only reads
code and writes `codebase.md`.
