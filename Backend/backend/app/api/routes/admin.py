from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.core.security import require_dashboard_api_key
from app.background_tasks.mutation_tasks import generate_and_index_mutations
from app.vectorstore.chroma.indexing import seed_threat_vectors


router = APIRouter(prefix="/admin", tags=["admin"])


class MutationIndexRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000)
    category: str = "adversarial_mutation"


@router.post("/seed-vectors", dependencies=[Depends(require_dashboard_api_key)])
async def seed_vectors() -> dict[str, int]:
    return {"threat_vectors": await seed_threat_vectors()}


@router.post("/index-mutations", dependencies=[Depends(require_dashboard_api_key)])
async def index_mutations(request: MutationIndexRequest) -> dict[str, int]:
    return {"mutations_indexed": await generate_and_index_mutations(request.prompt, request.category)}
