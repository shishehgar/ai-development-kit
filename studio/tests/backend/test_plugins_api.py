"""Tests for the plugin API."""

from fastapi.testclient import TestClient

from studio.backend.app import app


client = TestClient(app)


def test_plugins_endpoint() -> None:
    response = client.get(
        "/api/v1/plugins"
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["loaded"] >= 0
    assert payload["discovered"] >= 0
    assert isinstance(
        payload["plugins"],
        list,
    )
