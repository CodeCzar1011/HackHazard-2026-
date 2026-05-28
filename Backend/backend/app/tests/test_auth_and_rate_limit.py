from __future__ import annotations

import os

from fastapi.testclient import TestClient

from app.main import create_app


def create_test_client(require_api_key: bool = False) -> TestClient:
    os.environ["APP_ENV"] = "local"
    os.environ["REQUIRE_API_KEY"] = "true" if require_api_key else "false"
    os.environ.pop("DASHBOARD_API_KEY", None)
    app = create_app()
    return TestClient(app)


def test_health_unauthenticated_allowed():
    client = create_test_client(require_api_key=False)
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200


def test_analyze_requires_api_key_when_enabled():
    os.environ["DASHBOARD_API_KEY"] = "secret"
    client = create_test_client(require_api_key=True)
    resp = client.post("/api/v1/analyze", json={"prompt": "hi", "session_id": "s", "provider": "local"})
    assert resp.status_code == 401

    resp_ok = client.post(
        "/api/v1/analyze",
        headers={"x-guardaiian-api-key": "secret"},
        json={"prompt": "hi", "session_id": "s", "provider": "local"},
    )
    assert resp_ok.status_code == 200

