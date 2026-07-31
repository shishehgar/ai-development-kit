"""Project metadata retrieval for assistant context."""

from __future__ import annotations

import subprocess
from pathlib import Path

from aidk.ai.retrieval.models import RetrievedContext


_EXCLUDED_DIRECTORIES = frozenset(
    {
        ".git",
        ".venv",
        "__pycache__",
        "dist",
        "build",
        "node_modules",
    }
)


class ProjectMetadataRetriever:
    """Collect safe project and Git metadata."""

    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.project_root = Path(project_root).resolve()

    def retrieve(
        self,
        question: str,
    ) -> RetrievedContext:
        metadata: dict[str, object] = {
            "project_root": str(self.project_root),
            "project_name": self.project_root.name,
            "file_count": self._count_files(),
        }

        branch = self._git_output(
            "branch",
            "--show-current",
        )

        commit = self._git_output(
            "rev-parse",
            "--short",
            "HEAD",
        )

        status = self._git_output(
            "status",
            "--porcelain",
        )

        if branch:
            metadata["git_branch"] = branch

        if commit:
            metadata["git_commit"] = commit

        if status is not None:
            metadata["git_clean"] = not bool(
                status.strip()
            )

        return RetrievedContext(
            question=question.strip(),
            metadata=metadata,
        )

    def _count_files(self) -> int:
        if not self.project_root.exists():
            return 0

        count = 0

        for path in self.project_root.rglob("*"):
            if not path.is_file():
                continue

            if any(
                part in _EXCLUDED_DIRECTORIES
                for part in path.parts
            ):
                continue

            count += 1

        return count

    def _git_output(
        self,
        *arguments: str,
    ) -> str | None:
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(self.project_root),
                    *arguments,
                ],
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )
        except (
            OSError,
            subprocess.TimeoutExpired,
        ):
            return None

        if result.returncode != 0:
            return None

        return result.stdout.strip()
