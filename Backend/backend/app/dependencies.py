from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_dashboard_api_key
from app.db.session import get_db_session

DatabaseSession = Annotated[AsyncSession, Depends(get_db_session)]
Authenticated = Depends(require_dashboard_api_key)

