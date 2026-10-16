"""Tiny RAG-style pipeline that pulls in an embedding model and a public dataset.

Adds a dataset node and an embedding model to the AI-BOM.
"""
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DATASET = "squad"


def build_index(limit: int = 100):
    data = load_dataset(DATASET, split=f"train[:{limit}]")
    model = SentenceTransformer(EMBED_MODEL)
    contexts = list({row["context"] for row in data})
    embeddings = model.encode(contexts, show_progress_bar=False)
    return contexts, embeddings


if __name__ == "__main__":
    contexts, embeddings = build_index()
    print(f"Indexed {len(contexts)} passages with {EMBED_MODEL}; dim={embeddings.shape[1]}")
