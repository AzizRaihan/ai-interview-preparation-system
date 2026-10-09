# AI Interview Preparation System

A personal study tool for technical interview prep. It tracks progress across
eight subjects (OOP, DBMS, OS, AI/ML, cybersecurity, system design, and QA)
using a question bank of 503 entries sourced from GeeksforGeeks, and decides
what to study next based on how past sessions actually went rather than a
fixed order.

## How it works

Each question is tagged with a difficulty tier and a set of prerequisites
within its topic, so foundational material comes up before anything that
depends on it. A routing layer, built with LangGraph, checks what has been
logged for a topic (studied, solved, struggled) and picks the next action:
teach something new, quiz on something already studied, or review something
that was missed before. Struggled questions take priority over everything
else until they are cleared.

Explanations are grounded in the question bank itself. The system embeds all
503 entries with Gemini and stores them in a FAISS index, then retrieves
related entries before generating an explanation for a new question, so the
answer stays tied to the source material. Quiz answers are scored from 0 to
10 against the reference answer, with written feedback, and the outcome goes
into a local SQLite database that keeps a full history of every attempt.

Study sessions also get written to markdown files per topic, so past
explanations and quiz results are easy to read back later without digging
through the database.

## Topics covered

- Object-oriented programming
- Database management systems
- Operating systems
- AI and machine learning fundamentals
- Cybersecurity
- System design (high-level and low-level)
- QA and software testing

## Running it

You need a `.env` file in the project root with:

```
GEMINI_API_KEY=your-key-here
GROQ_API_KEY=your-key-here
```

Install the dependencies:

```
pip install python-dotenv faiss-cpu google-genai groq langgraph numpy
```

Then run a session:

```
python3 scripts/run_session.py
```

It asks which topic to work on, or you can pass one directly, for example
`python3 scripts/run_session.py OOP`.

## Project structure

```
data/corpus/        the question bank, FAISS index, and tagged metadata
scripts/             the pipeline: parsing, tagging, embedding, routing, and the app itself
study_logs/          full history of study sessions and quiz results, per topic
study_materials/     just the explanations, kept separately for review
```

The pipeline that builds the question bank runs in order: parsing the raw
markdown, tagging difficulty, tagging prerequisites, building the
prerequisite graph, then embedding everything into the vector index. After
that, `run_session.py` is the only script you need to run day to day.

## Built with

Python, LangGraph for the routing logic, FAISS for retrieval, Gemini for
embeddings, Groq for generating explanations and scoring quizzes, and SQLite
for tracking.
