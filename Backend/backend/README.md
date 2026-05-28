# GuardAIian Backend

GuardAIian is an AI proxy and vector firewall for LLM applications. It analyzes prompts before they reach an LLM provider, combines semantic vector matching, contextual session risk, adversarial mutation heuristics, policy classifiers, and adaptive scoring, then returns `allow`, `warn`, or `block`.

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

For containerized local dependencies from the repository root:

```bash
copy .env.example .env
docker compose up --build
```

## Main APIs

- `GET /api/v1/health`
- `GET /api/v1/ready`
- `POST /api/v1/analyze`
- `POST /api/v1/chat`
- `GET /api/v1/threat-feed`
- `GET /api/v1/analytics/metrics`
- `GET /api/v1/dashboard/summary`
- `WS /api/v1/ws/alerts`

The backend uses ChromaDB when installed and can fall back to an in-memory vector store for lightweight local tests. Production disables unsafe fallbacks through startup configuration validation.

## Production Readiness

Set `APP_ENV=prod` only with production-safe values:

- `DATABASE_URL` must point to a production database, not SQLite.
- `AUTO_CREATE_TABLES=false`; run Alembic migrations before startup.
- `REQUIRE_API_KEY=true` behavior is enforced automatically in production, and `DASHBOARD_API_KEY` must be set.
- `REDIS_URL` is required for distributed rate limiting.
- `BACKEND_CORS_ORIGINS` must be explicit and cannot be `*`.
- `USE_HASH_EMBEDDINGS_FALLBACK=false` and `LOAD_EMBEDDING_MODEL_ON_STARTUP=true`.
- `ALLOW_IN_MEMORY_VECTOR_FALLBACK=false`.

Run migrations from the `backend` directory:

```bash
python -m alembic upgrade head
```

Run verification:

```bash
python -m pytest -q
```
