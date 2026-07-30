"""Tests for the AIDK Studio API foundation."""

from __future__ import annotations

from fastapi.testclient import TestClient

from studio.backend.app import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["name"] == "AIDK Studio"
    assert response.json()["status"] == "ready"


def test_system_status() -> None:
    response = client.get("/api/v1/system/status")

    assert response.status_code == 200

    payload = response.json()

    assert payload["name"] == "AIDK Studio"
    assert payload["status"] == "ready"
    assert payload["command_count"] == 16


def test_command_catalog() -> None:
    response = client.get("/api/v1/commands")

    assert response.status_code == 200

    payload = response.json()
    command_names = {
        item["name"]
        for item in payload["commands"]
    }

    assert payload["count"] == 16
    assert "workspace" in command_names
    assert "audit" in command_names
    assert "fix" in command_names
    assert "deps-licenses" in command_names


def test_command_help() -> None:
    response = client.get("/api/v1/commands/audit")

    assert response.status_code == 200
    assert response.json()["title_fa"] == "ممیزی مهندسی"
    assert response.json()["safety"] == "read-only"


def test_unknown_command() -> None:
    response = client.get("/api/v1/commands/not-existing")

    assert response.status_code == 404
