import os
import subprocess
from pathlib import Path

import pytest

from aidk.git.engine import GitEngine, GitInfo


def run_git(repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    """Run Git with isolated configuration."""
    return subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        text=True,
        capture_output=True,
        env=os.environ.copy(),
    )


@pytest.fixture()
def git_repository(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Path:
    """Create an isolated Git repository with one commit."""

    repository = tmp_path / "repository"
    repository.mkdir()

    # Prevent incompatible global/system Git settings from affecting tests.
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", os.devnull)
    monkeypatch.setenv("HOME", str(tmp_path))

    run_git(repository, "init")
    run_git(repository, "symbolic-ref", "HEAD", "refs/heads/main")

    run_git(repository, "config", "user.name", "AIDK Test")
    run_git(repository, "config", "user.email", "aidk@example.invalid")

    readme = repository / "README.md"
    readme.write_text(
        "# AIDK test repository\n",
        encoding="utf-8",
    )

    run_git(repository, "add", "README.md")
    run_git(repository, "commit", "-m", "Initial test commit")

    return repository


def test_git_engine_detects_repository(git_repository: Path) -> None:
    engine = GitEngine()

    info = engine.inspect(git_repository)

    assert isinstance(info, GitInfo)
    assert info.exists is True


def test_git_engine_reads_branch(git_repository: Path) -> None:
    engine = GitEngine()

    info = engine.inspect(git_repository)

    assert info.exists is True
    assert info.branch == "main"


def test_git_engine_reads_commit(git_repository: Path) -> None:
    engine = GitEngine()

    info = engine.inspect(git_repository)

    expected_hash = run_git(
        git_repository,
        "rev-parse",
        "HEAD",
    ).stdout.strip()

    assert info.exists is True
    assert info.last_commit_hash != ""
    assert expected_hash.startswith(info.last_commit_hash) or (
        info.last_commit_hash.startswith(expected_hash)
    )
