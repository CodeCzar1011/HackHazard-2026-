from __future__ import annotations

from app.vectorstore.embeddings.model_loader import encode_texts


class EmbeddingService:
    """Application service for embedding text batches."""

    async def embed_one(self, text: str) -> list[float]:
        return (await encode_texts([text]))[0]

    async def embed_many(self, texts: list[str]) -> list[list[float]]:
        return await encode_texts(texts)

