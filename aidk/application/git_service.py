"""Structured Git inspection service for AIDK."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from aidk.git.engine import GitEngine
from aidk.git.models import GitInfo


@dataclass(frozen=True)
class GitReport:
    """Serializable Git repository report."""

    path: str
    exists: bool
    repository_root: str
    branch: str
    default_branch: str
    clean: bool
    modified_files: int
    staged_files: int
    untracked_files: int
    remote: bool
    remote_name: str
    remote_url: str
    last_commit_hash: str
    last_commit_author: str
    last_commit_date: str
    ahead: int
    behind: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class GitService:
    """Inspect a Git repository without printing output."""

    def __init__(
        self,
        path: Path | str | None = None,
    ) -> None:
        self.path = Path(
            path or Path.cwd()
        ).expanduser().resolve()

    @staticmethod
    def _build_report(
        *,
        path: Path,
        info: GitInfo,
    ) -> GitReport:
        return GitReport(
            path=str(path),
            exists=info.exists,
            repository_root=info.repository_root,
            branch=info.branch,
            default_branch=info.default_branch,
            clean=info.clean,
            modified_files=info.modified_files,
            staged_files=info.staged_files,
            untracked_files=info.untracked_files,
            remote=info.remote,
            remote_name=info.remote_name,
            remote_url=info.remote_url,
            last_commit_hash=info.last_commit_hash,
            last_commit_author=info.last_commit_author,
            last_commit_date=info.last_commit_date,
            ahead=info.ahead,
            behind=info.behind,
        )

    def run(
        self,
        path: Path | str | None = None,
    ) -> GitReport:
        target = Path(
            path or self.path
        ).expanduser().resolve()

        info = GitEngine().inspect(
            target
        )

        return self._build_report(
            path=target,
            info=info,
        )
