"""Git CLI adapter."""

from __future__ import annotations

from pathlib import Path

from aidk.application.container import services
from aidk.git.models import GitInfo
from aidk.git.printer import GitPrinter


class GitCommand:
    """Inspect the current Git repository."""

    @staticmethod
    def _to_git_info(report) -> GitInfo:
        return GitInfo(
            exists=report.exists,
            repository_root=report.repository_root,
            branch=report.branch,
            default_branch=report.default_branch,
            clean=report.clean,
            modified_files=report.modified_files,
            staged_files=report.staged_files,
            untracked_files=report.untracked_files,
            remote=report.remote,
            remote_name=report.remote_name,
            remote_url=report.remote_url,
            last_commit_hash=report.last_commit_hash,
            last_commit_author=report.last_commit_author,
            last_commit_date=report.last_commit_date,
            ahead=report.ahead,
            behind=report.behind,
        )

    def run(self) -> int:
        report = services.git.run(
            Path.cwd()
        )

        GitPrinter.show(
            self._to_git_info(report)
        )

        return 0
