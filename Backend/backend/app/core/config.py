from __future__ import annotations

from functools import lru_cache
import secrets
from typing import Literal, Optional

from pydantic import AnyHttpUrl, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.

    This is the single source of truth for all environment‑dependent settings.
    Use `get_settings()` to access a cached instance across the codebase.
    """

    # -------------------------------------------------------------------------
    # Core application
    # -------------------------------------------------------------------------
    APP_NAME: str = "GuardAIian"
    APP_ENV: Literal["local", "dev", "staging", "prod"] = Field(
        default="local", description="Deployment environment"
    )
    DEBUG: bool = False

    API_V1_PREFIX: str = "/api/v1"

    # CORS / security
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] | list[str] = Field(
        default_factory=list,
        description="Allowed CORS origins. Can be a JSON array or comma‑separated list.",
    )
    MAX_REQUEST_BODY_BYTES: int = 1_000_000

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------
    # Example: sqlite+aiosqlite:///./guardaiian.db
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./guardaiian.db",
        description="SQLAlchemy async database URL.",
    )

    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    AUTO_CREATE_TABLES: bool = True

    # -------------------------------------------------------------------------
    # ChromaDB / Vector store
    # -------------------------------------------------------------------------
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    CHROMA_COLLECTION_THREATS: str = "guardaiian_threat_signatures"
    CHROMA_COLLECTION_MUTATIONS: str = "guardaiian_mutations"
    ALLOW_IN_MEMORY_VECTOR_FALLBACK: bool = True

    # -------------------------------------------------------------------------
    # Embeddings / NLP
    # -------------------------------------------------------------------------
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_BATCH_SIZE: int = 32

    # -------------------------------------------------------------------------
    # LLM Providers
    # -------------------------------------------------------------------------
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-5-haiku-latest"

    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"

    LOCAL_LLM_ENDPOINT: Optional[str] = None

    # -------------------------------------------------------------------------
    # Security / Auth
    # -------------------------------------------------------------------------
    API_KEY_HEADER_NAME: str = "x-guardaiian-api-key"
    DASHBOARD_API_KEY: Optional[str] = None
    JWT_SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(48))
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRES_DAYS: int = 7
    DASHBOARD_ADMIN_EMAIL: str = "admin@guardaiian.local"
    DASHBOARD_ADMIN_PASSWORD: str = "change-me"
    DASHBOARD_ADMIN_NAME: str = "GuardAIian Admin"

    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 600
    REQUIRE_API_KEY: bool = False
    RATE_LIMIT_FAIL_CLOSED: bool = True
    REDIS_URL: Optional[str] = None

    # -------------------------------------------------------------------------
    # Detection / Risk scoring
    # -------------------------------------------------------------------------
    SEMANTIC_SIMILARITY_THRESHOLD: float = 0.78
    CONTEXT_RISK_WEIGHT: float = 0.25
    SEMANTIC_RISK_WEIGHT: float = 0.35
    MUTATION_RISK_WEIGHT: float = 0.2
    REGEX_POLICY_WEIGHT: float = 0.1
    SESSION_HISTORY_WEIGHT: float = 0.1

    GLOBAL_BLOCK_THRESHOLD: float = 0.8
    GLOBAL_WARN_THRESHOLD: float = 0.6
    HIGH_RISK_CONTEXT_WINDOW: int = 8

    # Demo/runtime controls
    LOAD_EMBEDDING_MODEL_ON_STARTUP: bool = False
    USE_HASH_EMBEDDINGS_FALLBACK: bool = True
    SEED_VECTORSTORE_ON_STARTUP: bool = True
    HASH_EMBEDDING_DIMENSIONS: int = 384

    # LLM proxy
    DEFAULT_LLM_PROVIDER: Literal["local", "openai", "anthropic", "gemini"] = "local"
    LLM_REQUEST_TIMEOUT_SECONDS: float = 30.0
    LLM_RETRY_ATTEMPTS: int = 2

    # -------------------------------------------------------------------------
    # WebSocket / Realtime
    # -------------------------------------------------------------------------
    WEBSOCKET_BROADCAST_QUEUE_SIZE: int = 1000

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = True

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "prod"

    @property
    def auth_required(self) -> bool:
        return self.REQUIRE_API_KEY or self.is_production

    @model_validator(mode="after")
    def validate_environment(self) -> "Settings":
        if self.MAX_REQUEST_BODY_BYTES < 1024:
            raise ValueError("MAX_REQUEST_BODY_BYTES must be at least 1024 bytes.")
        if self.RATE_LIMIT_REQUESTS_PER_MINUTE < 1:
            raise ValueError("RATE_LIMIT_REQUESTS_PER_MINUTE must be greater than 0.")
        if self.DB_POOL_SIZE < 1:
            raise ValueError("DB_POOL_SIZE must be greater than 0.")
        if self.DB_MAX_OVERFLOW < 0:
            raise ValueError("DB_MAX_OVERFLOW cannot be negative.")
        if self.LLM_RETRY_ATTEMPTS < 1:
            raise ValueError("LLM_RETRY_ATTEMPTS must be at least 1.")
        if self.is_production:
            self._validate_production()
        return self

    def _validate_production(self) -> None:
        errors: list[str] = []
        if self.DEBUG:
            errors.append("DEBUG must be false in production.")
        if self.DATABASE_URL.startswith("sqlite"):
            errors.append("DATABASE_URL must use PostgreSQL or another production database in production.")
        if self.AUTO_CREATE_TABLES:
            errors.append("AUTO_CREATE_TABLES must be false in production; run migrations before startup.")
        if not self.DASHBOARD_API_KEY:
            errors.append("DASHBOARD_API_KEY is required in production.")
        if not self.BACKEND_CORS_ORIGINS:
            errors.append("BACKEND_CORS_ORIGINS must be explicitly configured in production.")
        if any(str(origin) == "*" for origin in self.BACKEND_CORS_ORIGINS):
            errors.append("Wildcard CORS origins are not allowed in production.")
        if self.USE_HASH_EMBEDDINGS_FALLBACK:
            errors.append("USE_HASH_EMBEDDINGS_FALLBACK must be false in production.")
        if not self.LOAD_EMBEDDING_MODEL_ON_STARTUP:
            errors.append("LOAD_EMBEDDING_MODEL_ON_STARTUP must be true in production.")
        if self.ALLOW_IN_MEMORY_VECTOR_FALLBACK:
            errors.append("ALLOW_IN_MEMORY_VECTOR_FALLBACK must be false in production.")
        if not self.REDIS_URL:
            errors.append("REDIS_URL is required for distributed rate limiting in production.")
        if self.DEFAULT_LLM_PROVIDER != "local" and not self.provider_api_key(self.DEFAULT_LLM_PROVIDER):
            errors.append(f"API key is required for DEFAULT_LLM_PROVIDER={self.DEFAULT_LLM_PROVIDER}.")
        if errors:
            raise ValueError("Production configuration is invalid: " + " ".join(errors))

    def provider_api_key(self, provider: str) -> Optional[str]:
        return {
            "openai": self.OPENAI_API_KEY,
            "anthropic": self.ANTHROPIC_API_KEY,
            "gemini": self.GEMINI_API_KEY,
            "local": self.LOCAL_LLM_ENDPOINT,
        }.get(provider)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return a cached settings instance.

    Using `lru_cache` ensures we only parse environment variables once per
    process while still allowing easy import across modules.
    """

    return Settings()  # type: ignore[call-arg]


class SettingsProxy:
    """Resolve settings lazily so tests and app factories can refresh env config."""

    def __getattr__(self, name: str):
        return getattr(get_settings(), name)


def reload_settings() -> Settings:
    get_settings.cache_clear()
    return get_settings()


settings = SettingsProxy()

