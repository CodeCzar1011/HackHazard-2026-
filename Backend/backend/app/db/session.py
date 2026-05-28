from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.db.base import Base
from app.db import models  # noqa: F401


_engine: AsyncEngine | None = None
_engine_url: str | None = None
_schema_ready = False


def get_engine() -> AsyncEngine:
    """Create the async SQLAlchemy engine lazily so imports stay lightweight."""

    global _engine, _engine_url, _schema_ready
    if _engine is None or _engine_url != settings.DATABASE_URL:
        engine_kwargs: dict[str, object] = {"pool_pre_ping": True}
        if not settings.DATABASE_URL.startswith("sqlite"):
            engine_kwargs.update(pool_size=settings.DB_POOL_SIZE, max_overflow=settings.DB_MAX_OVERFLOW)
        _engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)
        _engine_url = settings.DATABASE_URL
        _schema_ready = False
    return _engine

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an async SQLAlchemy session.
    Ensures proper cleanup after each request.
    """

    engine = get_engine()
    await _ensure_local_schema(engine)
    sessionmaker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with sessionmaker() as session:
        yield session


async def _ensure_local_schema(engine: AsyncEngine) -> None:
    global _schema_ready
    if _schema_ready or not settings.AUTO_CREATE_TABLES or settings.is_production:
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    _schema_ready = True

