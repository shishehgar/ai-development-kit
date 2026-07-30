from pathlib import Path

from aidk.db.engine import DatabaseEngine


def test_database_migration_version(
    tmp_path: Path,
) -> None:
    engine = DatabaseEngine(
        tmp_path / "workspace.db"
    )

    engine.initialize()

    assert engine.migration_version() == 2


def test_database_migration_history(
    tmp_path: Path,
) -> None:
    engine = DatabaseEngine(
        tmp_path / "workspace.db"
    )

    engine.initialize()

    history = engine.migration_history()

    assert len(history) == 2
    assert history[0]["version"] == 1
    assert history[0]["name"] == "initial_schema"
    assert history[1]["version"] == 2
    assert history[1]["name"] == "dependencies"


def test_database_initialize_is_idempotent(
    tmp_path: Path,
) -> None:
    engine = DatabaseEngine(
        tmp_path / "workspace.db"
    )

    engine.initialize()
    engine.initialize()

    history = engine.migration_history()

    assert len(history) == 2
