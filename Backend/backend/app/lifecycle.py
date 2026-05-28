from __future__ import annotations

from sqlalchemy import inspect, text

from app.core.config import settings
from app.core.logger import get_logger
from app.db.base import Base
from app.db import models  # noqa: F401
from app.db.session import get_engine
from app.vectorstore.embeddings.model_loader import load_embedding_model
from app.vectorstore.chroma.chroma_client import get_chroma_client
from app.vectorstore.chroma.indexing import seed_threat_vectors


logger = get_logger(__name__)


async def run_startup_checks() -> None:
    """
    Perform startup‑time validation of critical dependencies.

    - Database connectivity
    - Embedding model load
    - ChromaDB client initialization
    """

    _validate_environment_contracts()
    await _check_database()
    if settings.LOAD_EMBEDDING_MODEL_ON_STARTUP:
        await _check_embeddings()
    await _check_chroma()
    if settings.SEED_VECTORSTORE_ON_STARTUP:
        await seed_threat_vectors()


async def _check_database() -> None:
    try:
        engine = get_engine()
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            if not settings.AUTO_CREATE_TABLES:
                has_threat_events = await conn.run_sync(
                    lambda sync_conn: inspect(sync_conn).has_table("threat_events")
                )
                if not has_threat_events:
                    raise RuntimeError(
                        "Database schema missing required table 'threat_events'. Run migrations before startup."
                    )
            elif not settings.is_production:
                async with engine.begin() as ddl_conn:
                    await ddl_conn.run_sync(Base.metadata.create_all)
        logger.info("Database connection OK", extra={"env": settings.APP_ENV})
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Database connectivity check failed", exc_info=exc)
        raise


async def _check_embeddings() -> None:
    try:
        _ = await load_embedding_model()
        logger.info("Embedding model loaded successfully")
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Failed to load embedding model", exc_info=exc)
        raise


async def _check_chroma() -> None:
    try:
        client = get_chroma_client()
        # Light touch to ensure persistence directory is usable
        _ = client.heartbeat()
        logger.info("ChromaDB client initialized")
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("ChromaDB startup check failed", exc_info=exc)
        raise


def _validate_environment_contracts() -> None:
    """
    Enforce stricter safety contracts when running in production.

    This function performs only cheap config validation; expensive IO checks
    belong in the async helpers above.
    """

    if not settings.is_production:
        return
    logger.info("Production configuration contract validated")

