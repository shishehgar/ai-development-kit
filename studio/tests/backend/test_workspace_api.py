from fastapi.testclient import TestClient

from studio.backend.app import app

client = TestClient(app)


def test_workspace_endpoint():

    response = client.get(
        "/api/v1/workspace"
    )

    assert response.status_code == 200

    body = response.json()

    assert "root" in body

    assert "project_count" in body

    assert "projects" in body
