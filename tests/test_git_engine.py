"""
Git Engine Tests
"""

from pathlib import Path

from aidk.git.engine import GitEngine
from aidk.git.models import GitInfo


def test_git_engine_detects_repository():

    project = Path.cwd()

    engine = GitEngine()

    info = engine.inspect(project)

    assert isinstance(info, GitInfo)

    assert info.exists is True


def test_git_engine_reads_branch():

    project = Path.cwd()

    engine = GitEngine()

    info = engine.inspect(project)

    assert info.branch != ""


def test_git_engine_reads_commit():

    project = Path.cwd()

    engine = GitEngine()

    info = engine.inspect(project)

    assert info.last_commit_hash != ""
