from __future__ import annotations

from fastapi import APIRouter

from app.lifecycle import _check_database, _check_chroma, _check_embeddings  # type: ignore[attr-defined]


router = APIRouter()


@router.get("/readiness")
async def readiness() -> dict[str, str]:
    # Run lightweight dependency checks; if any raise, FastAPI will surface 500.
    await _check_database()
    await _check_chroma()
    await _check_embeddings()
    return {"status": "ready"}

