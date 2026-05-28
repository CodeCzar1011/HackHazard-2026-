from __future__ import annotations

from app.vectorstore.chroma.collections import get_threats_collection
from app.vectorstore.datasets.seed_vectors import SEED_THREATS
from app.vectorstore.embeddings.embedding_service import EmbeddingService


async def seed_threat_vectors() -> int:
    """Seed Chroma with curated baseline threat signatures."""

    collection = get_threats_collection()
    existing = collection.count()
    if existing:
        return existing
    embedder = EmbeddingService()
    texts = [item["text"] for item in SEED_THREATS]
    embeddings = await embedder.embed_many(texts)
    collection.add(
        ids=[item["id"] for item in SEED_THREATS],
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"category": item["category"]} for item in SEED_THREATS],
    )
    return collection.count()

