"""
Phase 2 step 4: embed all tagged entries (question+answer per chunk) using
Gemini's embedding API, then build and save a FAISS index for similarity search.
"""

import json
import os
import time
from pathlib import Path

import faiss
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

TAGGED_ENTRIES_PATH = Path("data/corpus/tagged_entries.json")
INDEX_PATH = Path("data/corpus/faiss_index.bin")
METADATA_PATH = Path("data/corpus/embedding_metadata.json")

EMBEDDING_MODEL = "gemini-embedding-001"
BATCH_SIZE = 100  # Gemini's embed_content hard caps at 100 texts per call (confirmed live)


def embed_entries(client: genai.Client, entries: list[dict]) -> np.ndarray:
    texts = [f"{e['question']}\n\n{e['answer']}" for e in entries]

    response = None
    for attempt in range(5):
        try:
            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=texts,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
            )
            break
        except errors.ClientError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(35)

    vectors = np.array([e.values for e in response.embeddings], dtype="float32")
    return vectors


def embed_all_entries(client: genai.Client, entries: list[dict]) -> np.ndarray:
    all_vectors = []
    for i in range(0, len(entries), BATCH_SIZE):
        chunk = entries[i : i + BATCH_SIZE]
        all_vectors.append(embed_entries(client, chunk))
    return np.vstack(all_vectors)


def normalize_vectors(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / norms


def build_faiss_index(vectors: np.ndarray) -> faiss.Index:
    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)
    return index


def save_index_and_metadata(index: faiss.Index, entries: list[dict]) -> None:
    faiss.write_index(index, str(INDEX_PATH))
    METADATA_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    entries = json.loads(TAGGED_ENTRIES_PATH.read_text())
    print(f"Embedding {len(entries)} entries...")

    vectors = embed_all_entries(client, entries)
    normalized = normalize_vectors(vectors)
    index = build_faiss_index(normalized)

    save_index_and_metadata(index, entries)
    print(f"Saved FAISS index ({index.ntotal} vectors) to {INDEX_PATH}")
    print(f"Saved metadata ({len(entries)} entries) to {METADATA_PATH}")
