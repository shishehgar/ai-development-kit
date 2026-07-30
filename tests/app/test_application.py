"""Tests for the AIDK application object."""

from __future__ import annotations

from pathlib import Path

from aidk.app.application import Application
from aidk.app.config import ApplicationConfig
from aidk.app.context import build_context


def build_test_config(
    root: Path,
) -> ApplicationConfig:
    return ApplicationConfig(
        workspace=root,
        projects_root=root,
        api_host="127.0.0.1",
        api_port=8000,
        debug=True,
        environment="test",
        cache_ttl_seconds=30,
    )


def test_application_exposes_context(
    tmp_path: Path,
) -> None:
    config = build_test_config(
        tmp_path
    )

    application = Application(
        build_context(config)
    )

    assert application.config is config
    assert application.services is (
        application.context.services
    )
    assert application.cache is (
        application.context.cache
    )
    assert application.events is (
        application.context.events
    )


def test_application_start_and_stop(
    tmp_path: Path,
) -> None:
    application = Application(
        build_context(
            build_test_config(
                tmp_path
            )
        )
    )

    assert application.started is False
    assert application.start() is True
    assert application.started is True
    assert application.stop() is True
    assert application.started is False


def test_application_reload(
    tmp_path: Path,
) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"

    first_root.mkdir()
    second_root.mkdir()

    application = Application(
        build_context(
            build_test_config(
                first_root
            )
        )
    )

    old_context = application.context

    application.reload(
        build_test_config(
            second_root
        )
    )

    assert (
        application.context
        is not old_context
    )

    assert application.config.workspace == (
        second_root.resolve()
    )
