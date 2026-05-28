from __future__ import annotations

from app.vectorstore.chroma.retrieval import query_threat_vectors
from app.vectorstore.embeddings.embedding_service import EmbeddingService


class SemanticMatcher:
    """Semantic threat matcher backed by embeddings and ChromaDB."""

    def __init__(self, embedder: EmbeddingService | None = None) -> None:
        self.embedder = embedder or EmbeddingService()

    async def match(self, prompt: str) -> tuple[float, str, list[dict[str, object]]]:
        embedding = await self.embedder.embed_one(prompt)
        matches = await query_threat_vectors(embedding)
        if not matches:
            return 0.0, "benign", []
        best = matches[0]
        return float(best["similarity"]), str(best["category"]), matches

