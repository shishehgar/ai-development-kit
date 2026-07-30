"""Knowledge API tests."""

from fastapi.testclient import TestClient

from studio.backend.app import app


client = TestClient(app)


def test_knowledge_health():

    response = client.get(
        "/knowledge/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": "knowledge",
    }
