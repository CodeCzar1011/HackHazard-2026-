from __future__ import annotations

from functools import lru_cache

from app.core.config import settings


class InMemoryChromaClient:
    """Small Chroma-compatible fallback used when chromadb is not installed locally."""

    def __init__(self) -> None:
        self.collections: dict[str, InMemoryCollection] = {}

    def get_or_create_collection(self, name: str):
        self.collections.setdefault(name, InMemoryCollection(name))
        return self.collections[name]

    def heartbeat(self) -> int:
        return 1


class InMemoryCollection:
    def __init__(self, name: str) -> None:
        self.name = name
        self._items: dict[str, dict[str, object]] = {}

    def count(self) -> int:
        return len(self._items)

    def add(self, ids, documents, embeddings, metadatas=None) -> None:
        for index, item_id in enumerate(ids):
            self._items[item_id] = {
                "document": documents[index],
                "embedding": embeddings[index],
                "metadata": (metadatas or [{}])[index],
            }

    def query(self, query_embeddings, n_results: int = 5):
        from app.utils.similarity_utils import cosine_similarity

        query_embedding = query_embeddings[0]
        ranked = sorted(
            self._items.items(),
            key=lambda item: cosine_similarity(query_embedding, item[1]["embedding"]),
            reverse=True,
        )[:n_results]
        return {
            "ids": [[item_id for item_id, _ in ranked]],
            "documents": [[str(item["document"]) for _, item in ranked]],
            "distances": [[1.0 - cosine_similarity(query_embedding, item["embedding"]) for _, item in ranked]],
            "metadatas": [[item["metadata"] for _, item in ranked]],
        }


@lru_cache(maxsize=1)
def get_chroma_client():
    """
    Return a configured ChromaDB client.

    Uses persistent storage so that threat signatures and mutations survive
    restarts in a local or containerized environment.
    """

    try:
        import chromadb
        from chromadb.config import Settings as ChromaSettings

        return chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    except ModuleNotFoundError:
        if settings.is_production or not settings.ALLOW_IN_MEMORY_VECTOR_FALLBACK:
            raise
        return InMemoryChromaClient()

