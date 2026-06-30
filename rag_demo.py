from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


KNOWLEDGE_DIR = Path("knowledge_base")
CHUNK_SIZE_WORDS = 90
CHUNK_OVERLAP_WORDS = 20
TOP_K = 3


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "using",
    "with",
}


@dataclass(frozen=True)
class Chunk:
    source: str
    text: str
    vector: Counter[str]


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return [word for word in words if word not in STOP_WORDS and len(word) > 1]


def vectorize(text: str) -> Counter[str]:
    return Counter(tokenize(text))


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    shared_words = set(left) & set(right)
    dot_product = sum(left[word] * right[word] for word in shared_words)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))

    if left_norm == 0 or right_norm == 0:
        return 0.0

    return dot_product / (left_norm * right_norm)


def split_into_chunks(text: str, source: str) -> list[Chunk]:
    words = text.split()
    chunks: list[Chunk] = []
    start = 0

    while start < len(words):
        end = start + CHUNK_SIZE_WORDS
        chunk_text = " ".join(words[start:end]).strip()

        if chunk_text:
            chunks.append(Chunk(source=source, text=chunk_text, vector=vectorize(chunk_text)))

        if end >= len(words):
            break

        start = max(end - CHUNK_OVERLAP_WORDS, start + 1)

    return chunks


def load_knowledge_base() -> list[Chunk]:
    chunks: list[Chunk] = []

    for path in sorted(KNOWLEDGE_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        chunks.extend(split_into_chunks(text, path.name))

    return chunks


def retrieve(question: str, chunks: list[Chunk], top_k: int = TOP_K) -> list[tuple[float, Chunk]]:
    question_vector = vectorize(question)
    scored_chunks = [
        (cosine_similarity(question_vector, chunk.vector), chunk)
        for chunk in chunks
    ]
    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    return [item for item in scored_chunks[:top_k] if item[0] > 0]


def generate_answer(question: str, retrieved_chunks: list[tuple[float, Chunk]]) -> str:
    if not retrieved_chunks:
        return (
            "I could not find enough relevant information in the knowledge base. "
            "In a production RAG system, I would ask a clarifying question or say I do not know."
        )

    context_lines = []
    source_lines = []

    for index, (score, chunk) in enumerate(retrieved_chunks, start=1):
        context_lines.append(f"{index}. {chunk.text}")
        source_lines.append(f"- {chunk.source} (similarity: {score:.2f})")

    return (
        "Answer grounded in retrieved context:\n\n"
        f"Question: {question}\n\n"
        "Relevant information:\n"
        + "\n".join(context_lines)
        + "\n\nSources:\n"
        + "\n".join(source_lines)
    )


def main() -> None:
    chunks = load_knowledge_base()

    if not chunks:
        raise SystemExit("No knowledge files found. Add .txt files inside knowledge_base/.")

    print("Company Knowledge Base RAG Demo")
    print(f"Loaded {len(chunks)} chunks from {KNOWLEDGE_DIR}/")
    print("Ask a question, or type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit", "q"}:
            print("Goodbye.")
            break

        if not question:
            continue

        retrieved_chunks = retrieve(question, chunks)
        answer = generate_answer(question, retrieved_chunks)
        print(f"\n{answer}\n")


if __name__ == "__main__":
    main()
