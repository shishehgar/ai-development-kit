"""Tests for the dependency registry API."""

from fastapi.testclient import TestClient

from studio.backend.app import app


client = TestClient(app)


def test_registry_endpoint() -> None:
    response = client.get(
        "/api/v1/registry"
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["total"] >= 1
    assert isinstance(
        payload["services"],
        list,
    )

    names = {
        item["service"]
        for item
        in payload["services"]
    }

    assert any(
        name.endswith(
            ".WorkspaceService"
        )
        for name in names
    )
