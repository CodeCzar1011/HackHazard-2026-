from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.security import require_dashboard_api_key
from app.dependencies import DatabaseSession
from app.schemas.request_schema import ChatRequest
from app.schemas.response_schema import ChatResponse
from app.services.llm_service import LLMService


router = APIRouter(prefix="/chat", tags=["proxy"])


@router.post("", response_model=ChatResponse, dependencies=[Depends(require_dashboard_api_key)])
async def secure_chat(request: ChatRequest, session: DatabaseSession) -> ChatResponse:
    return await LLMService(session).chat(request)

