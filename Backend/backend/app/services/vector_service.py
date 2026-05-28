from __future__ import annotations

import uuid

from app.detection.adversarial.mutation_engine import MutationEngine
from app.vectorstore.chroma.collections import get_mutations_collection
from app.vectorstore.embeddings.embedding_service import EmbeddingService


class VectorService:
    """Coordinates vector indexing for curated and generated threat signatures."""

    def __init__(
        self,
        embedder: EmbeddingService | None = None,
        mutation_engine: MutationEngine | None = None,
    ) -> None:
        self.embedder = embedder or EmbeddingService()
        self.mutation_engine = mutation_engine or MutationEngine()

    async def index_mutations(self, prompt: str, category: str = "adversarial_mutation") -> int:
        variants = self.mutation_engine.generate(prompt)
        if not variants:
            return 0
        embeddings = await self.embedder.embed_many(variants)
        collection = get_mutations_collection()
        collection.add(
            ids=[f"mutation-{uuid.uuid4()}" for _ in variants],
            documents=variants,
            embeddings=embeddings,
            metadatas=[{"category": category, "source": "mutation_engine"} for _ in variants],
        )
        return len(variants)

