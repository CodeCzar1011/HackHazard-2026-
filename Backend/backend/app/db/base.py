from __future__ import annotations

from typing import Any

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    def to_dict(self) -> dict[str, Any]:
        """Utility to convert model to plain dict."""

        return {c.key: getattr(self, c.key) for c in self.__table__.columns}  # type: ignore[attr-defined]

