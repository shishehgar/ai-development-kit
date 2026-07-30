"""Tests for the Audit API."""

from fastapi.testclient import TestClient

from studio.backend.app import app


client = TestClient(app)


def test_audit_endpoint() -> None:
    response = client.get(
        "/api/v1/audit"
    )

    assert response.status_code == 200

    body = response.json()

    assert "root" in body
    assert "total_projects" in body
    assert "average_score" in body
    assert "grade_distribution" in body
    assert "critical_projects" in body
    assert "recommendations" in body
