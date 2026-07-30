"""Tests for application configuration."""

from __future__ import annotations

from pathlib import Path

from aidk.app.config import ApplicationConfig


def test_config_reads_environment(
    monkeypatch,
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    projects = tmp_path / "projects"

    workspace.mkdir()
    projects.mkdir()

    monkeypatch.setenv(
        "AIDK_WORKSPACE",
        str(workspace),
    )
    monkeypatch.setenv(
        "AIDK_STUDIO_WORKSPACE",
        str(projects),
    )
    monkeypatch.setenv(
        "AIDK_API_HOST",
        "0.0.0.0",
    )
    monkeypatch.setenv(
        "AIDK_API_PORT",
        "8765",
    )
    monkeypatch.setenv(
        "AIDK_DEBUG",
        "true",
    )
    monkeypatch.setenv(
        "AIDK_CACHE_TTL_SECONDS",
        "120",
    )

    config = (
        ApplicationConfig.from_environment()
    )

    assert config.workspace == (
        workspace.resolve()
    )
    assert config.projects_root == (
        projects.resolve()
    )
    assert config.api_host == "0.0.0.0"
    assert config.api_port == 8765
    assert config.debug is True
    assert config.cache_ttl_seconds == 120
