from __future__ import annotations

from app.vectorstore.chroma.collections import get_mutations_collection, get_threats_collection


async def query_threat_vectors(embedding: list[float], limit: int = 5) -> list[dict[str, object]]:
    """Query curated and mutation collections and normalize Chroma distances."""

    matches: list[dict[str, object]] = []
    for source, collection in (
        ("threats", get_threats_collection()),
        ("mutations", get_mutations_collection()),
    ):
        if collection.count() == 0:
            continue
        result = collection.query(query_embeddings=[embedding], n_results=limit)
        ids = result.get("ids", [[]])[0]
        docs = result.get("documents", [[]])[0]
        distances = result.get("distances", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        for item_id, doc, distance, metadata in zip(ids, docs, distances, metadatas):
            similarity = max(0.0, min(1.0, 1.0 - float(distance)))
            matches.append(
                {
                    "id": item_id,
                    "text": doc,
                    "similarity": similarity,
                    "category": (metadata or {}).get("category", "unknown"),
                    "source": source,
                }
            )
    return sorted(matches, key=lambda item: float(item["similarity"]), reverse=True)[:limit]

