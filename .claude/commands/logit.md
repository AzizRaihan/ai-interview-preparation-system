---
description: Append the most recent teaching/explanation from this conversation to LEARNING_LOG.md
---

Find the most recent concept explanation or teaching moment in this conversation —
the part where a new RAG/AI/ML/embedding concept was explained in plain language,
per CLAUDE.md's teaching rules.

Write it up as a new dated entry in LEARNING_LOG.md, following the existing entries'
format (## date — title, then **Phase:**, then short plain bullets).

Keep it easy to read, per the established preference: short sentences, simple
bullets, no dense technical jargon or debugging-transcript detail. It should read
like a clear study note, not a technical spec.

If $ARGUMENTS is given, use it to narrow down which part of the conversation to log
(e.g. "the part about GraphRAG" or "the caching explanation"). Otherwise, log the
most recent teaching moment.

After writing the entry, confirm briefly what was logged.
