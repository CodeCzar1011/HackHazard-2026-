from __future__ import annotations

import hashlib
import math
from functools import lru_cache
from typing import Any

from app.core.config import settings
from app.core.logger import get_logger


logger = get_logger(__name__)


@lru_cache(maxsize=1)
def _load_model() -> Any:
    """
    Load and cache the SentenceTransformer model.

    This is a synchronous operation invoked from an async wrapper to avoid
    blocking the event loop at import time.
    """

    logger.info(
        "Loading embedding model",
        extra={"model_name": settings.EMBEDDING_MODEL_NAME},
    )
    try:
        from sentence_transformers import SentenceTransformer
    except ModuleNotFoundError as exc:  # pragma: no cover - dependency validated in production
        raise RuntimeError("sentence-transformers is required when hash embedding fallback is disabled.")
    except Exception as exc:  # pragma: no cover - defensive for broken ML runtimes
        raise RuntimeError("Failed to import sentence-transformers.") from exc
    model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
    return model


def _hash_embedding(text: str) -> list[float]:
    """Deterministic embedding fallback for offline tests and demos."""

    dims = settings.HASH_EMBEDDING_DIMENSIONS
    vector = [0.0] * dims
    tokens = text.lower().split()
    for token in tokens or [text.lower()]:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        for index, byte in enumerate(digest):
            slot = (index * 31 + byte) % dims
            vector[slot] += 1.0 if byte % 2 == 0 else -1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


async def load_embedding_model() -> Any:
    """
    Async wrapper around the cached model loader.

    Using a separate coroutine allows us to later move the blocking work
    into a thread pool executor if needed without changing call sites.
    """

    # For now this simply returns the cached model; in production you may use
    # `anyio.to_thread.run_sync(_load_model)` if model load becomes too heavy.
    return _load_model()


async def encode_texts(texts: list[str]) -> list[list[float]]:
    """
    Encode a list of texts into dense embeddings.

    Returns a list of float vectors suitable for use with ChromaDB.
    """

    if settings.USE_HASH_EMBEDDINGS_FALLBACK and not settings.LOAD_EMBEDDING_MODEL_ON_STARTUP:
        return [_hash_embedding(text) for text in texts]
    try:
        model = await load_embedding_model()
        embeddings = model.encode(
            texts,
            batch_size=settings.EMBEDDING_BATCH_SIZE,
            show_progress_bar=False,
            convert_to_numpy=False,
        )
        return [list(map(float, emb)) for emb in embeddings]  # type: ignore[arg-type]
    except Exception:
        if not settings.USE_HASH_EMBEDDINGS_FALLBACK:
            raise
        logger.warning("Falling back to deterministic hash embeddings")
        return [_hash_embedding(text) for text in texts]
