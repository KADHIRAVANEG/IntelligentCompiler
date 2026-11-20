import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app, get_nim_client, _lint_python, SAFE_ENV, IPRateLimiter, resolve_candidate_models


@pytest.fixture
def client():
    return TestClient(app)


def test_serve_ui(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "html" in response.headers.get("content-type", "").lower()


def test_serve_ui_head(client):
    response = client.head("/")
    assert response.status_code == 200


def test_lint_empty_code(client):
    response = client.post("/lint", json={"lang": "python", "code": ""})
    assert response.status_code == 200
    assert response.json() == {"diagnostics": []}


def test_lint_unsupported_language(client):
    response = client.post("/lint", json={"lang": "unknown_lang", "code": "some code"})
    assert response.status_code == 200
    assert response.json() == {"diagnostics": []}


def test_lint_python_syntax_error(client):
    broken_code = "def foo(\n    print('missing paren')"
    response = client.post("/lint", json={"lang": "python", "code": broken_code})
    assert response.status_code == 200
    diagnostics = response.json().get("diagnostics", [])
    assert len(diagnostics) > 0
    assert any(d["severity"] == "error" for d in diagnostics)


def test_lint_python_valid_code(client):
    valid_code = "def add(a, b):\n    return a + b\n\nresult = add(1, 2)\nprint(result)\n"
    response = client.post("/lint", json={"lang": "python", "code": valid_code})
    assert response.status_code == 200
    diagnostics = response.json().get("diagnostics", [])
    assert not any(d["severity"] == "error" for d in diagnostics)


def test_analyze_without_api_key(client, monkeypatch):
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)
    response = client.post("/analyze", json={
        "code": "print('hello')",
        "lang": "python",
        "output": "hello\n"
    })
    assert response.status_code == 200
    data = response.json()
    assert "AI Error: NVIDIA_API_KEY" in data["suggestion"]


def test_safe_env_excludes_secrets():
    """Verify that SAFE_ENV excludes sensitive keys like NVIDIA_API_KEY."""
    assert "NVIDIA_API_KEY" not in SAFE_ENV
    assert "SECRET" not in SAFE_ENV
    assert "PATH" in SAFE_ENV


def test_rate_limiter_logic():
    """Verify rate limiter blocks after reaching threshold."""
    limiter = IPRateLimiter(max_requests=3, window_seconds=10)
    ip = "192.168.1.100"
    assert limiter.is_allowed(ip) is True
    assert limiter.is_allowed(ip) is True
    assert limiter.is_allowed(ip) is True
    assert limiter.is_allowed(ip) is False  # Exceeded


def test_resolve_candidate_models():
    """Verify resolve_candidate_models returns list with preferred and active models."""
    models = resolve_candidate_models(client=None, preferred_model="custom/my-model")
    assert models[0] == "custom/my-model"
    assert "google/gemma-3-12b-it" in models
    assert "nvidia/nemotron-3.5-lightning-30b-a3b" in models
    # Check no duplicates
    assert len(models) == len(set(models))

