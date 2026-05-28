from __future__ import annotations

import logging
import sys
from typing import Any, Dict

try:
    from python_json_logger import jsonlogger
except ModuleNotFoundError:  # pragma: no cover - local minimal environments
    jsonlogger = None  # type: ignore[assignment]

from .config import settings


class StructuredJsonFormatter(jsonlogger.JsonFormatter if jsonlogger else logging.Formatter):
    """Structured JSON log formatter with sane defaults for observability."""

    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        if jsonlogger is None:
            return
        super().add_fields(log_record, record, message_dict)
        log_record.setdefault("level", record.levelname)
        log_record.setdefault("logger", record.name)


def configure_logging() -> None:
    """
    Configure root logger with JSON or standard formatting based on settings.

    This is idempotent and can safely be called multiple times.
    """

    root = logging.getLogger()
    if root.handlers:
        return

    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    if settings.LOG_JSON:
        formatter = StructuredJsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )
    else:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        )

    handler.setFormatter(formatter)

    root.setLevel(level)
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a module‑scoped logger."""

    configure_logging()
    return logging.getLogger(name)

