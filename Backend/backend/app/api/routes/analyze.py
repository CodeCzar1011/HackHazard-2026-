from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.security import require_dashboard_api_key
from app.dependencies import DatabaseSession
from app.schemas.request_schema import AnalyzeRequest
from app.schemas.response_schema import AnalyzeResponse
from app.services.threat_service import ThreatService


router = APIRouter(prefix="/analyze", tags=["analysis"])


@router.post("", response_model=AnalyzeResponse, dependencies=[Depends(require_dashboard_api_key)])
async def analyze_prompt(request: AnalyzeRequest, session: DatabaseSession) -> AnalyzeResponse:
    return await ThreatService(session).analyze(request)

