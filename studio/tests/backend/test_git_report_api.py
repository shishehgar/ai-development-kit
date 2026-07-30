"""Tests for the workspace Git report API."""

from fastapi.testclient import TestClient

from studio.backend.app import app


client = TestClient(app)


def test_git_report_endpoint() -> None:
    response = client.get(
        "/api/v1/git-report"
    )

    assert response.status_code == 200

    body = response.json()

    assert "root" in body
    assert "total_projects" in body
    assert "clean_repositories" in body
    assert "dirty_repositories" in body
    assert "branches" in body
    assert "remote_count" in body
    assert "no_remote_count" in body
    assert "risks" in body
