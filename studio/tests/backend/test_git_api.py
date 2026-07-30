"""Tests for the Git API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from studio.backend.app import app


client = TestClient(app)


def test_git_endpoint() -> None:
    response = client.get(
        "/api/v1/git"
    )

    assert response.status_code == 200

    body = response.json()

    assert "path" in body
    assert "exists" in body
    assert "branch" in body
    assert "clean" in body
    assert "remote" in body
    assert "last_commit_hash" in body
