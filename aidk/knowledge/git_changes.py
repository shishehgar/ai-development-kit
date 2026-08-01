"""Git change detection for incremental knowledge indexing."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path


class GitChangeDetectionError(RuntimeError):
    """Raised when repository changes cannot be detected."""


@dataclass(slots=True)
class GitChanges:
    """Files changed relative to the current Git HEAD."""

    added: list[Path] = field(
        default_factory=list
    )
    modified: list[Path] = field(
        default_factory=list
    )
    deleted: list[Path] = field(
        default_factory=list
    )
    renamed: list[
        tuple[Path, Path]
    ] = field(default_factory=list)

    @property
    def changed_files(self) -> list[Path]:
        """Return existing files requiring analysis."""

        return [
            *self.added,
            *self.modified,
            *[
                target
                for _, target in self.renamed
            ],
        ]

    @property
    def change_count(self) -> int:
        """Return the total number of detected changes."""

        return (
            len(self.added)
            + len(self.modified)
            + len(self.deleted)
            + len(self.renamed)
        )

    @property
    def requires_full_refresh(self) -> bool:
        """
        Return whether dependency-safe full indexing is required.

        Modified, deleted and renamed files can invalidate incoming
        graph relations from unchanged files.
        """

        return bool(
            self.modified
            or self.deleted
            or self.renamed
        )


class GitChangeDetector:
    """Detect tracked and untracked repository changes."""

    def __init__(
        self,
        root: str | Path,
    ) -> None:
        self.root = Path(root).resolve()

        if not self.root.is_dir():
            raise ValueError(
                f"Repository root does not exist: {self.root}"
            )

    def detect(self) -> GitChanges:
        """Return changes relative to the repository HEAD."""

        self._verify_repository()

        changes = GitChanges()

        tracked_output = self._run_git(
            "diff",
            "--name-status",
            "-z",
            "HEAD",
            "--",
        )

        self._parse_tracked_changes(
            tracked_output,
            changes,
        )

        untracked_output = self._run_git(
            "ls-files",
            "--others",
            "--exclude-standard",
            "-z",
        )

        for relative_path in self._split_null(
            untracked_output
        ):
            path = self._absolute_path(
                relative_path
            )

            if path not in changes.added:
                changes.added.append(path)

        self._sort_changes(changes)

        return changes

    def _verify_repository(self) -> None:
        result = subprocess.run(
            [
                "git",
                "rev-parse",
                "--is-inside-work-tree",
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

        if (
            result.returncode != 0
            or result.stdout.strip() != "true"
        ):
            raise GitChangeDetectionError(
                f"Not a Git repository: {self.root}"
            )

    def _run_git(
        self,
        *arguments: str,
    ) -> str:
        result = subprocess.run(
            [
                "git",
                *arguments,
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            message = (
                result.stderr.strip()
                or result.stdout.strip()
                or "Unknown Git error."
            )

            raise GitChangeDetectionError(
                message
            )

        return result.stdout

    def _parse_tracked_changes(
        self,
        output: str,
        changes: GitChanges,
    ) -> None:
        tokens = self._split_null(output)
        index = 0

        while index < len(tokens):
            status = tokens[index]
            index += 1

            if index >= len(tokens):
                break

            source_name = tokens[index]
            index += 1

            status_code = status[:1]

            if status_code in {"R", "C"}:
                if index >= len(tokens):
                    break

                target_name = tokens[index]
                index += 1

                source_path = self._absolute_path(
                    source_name
                )
                target_path = self._absolute_path(
                    target_name
                )

                changes.renamed.append(
                    (
                        source_path,
                        target_path,
                    )
                )

            elif status_code == "A":
                changes.added.append(
                    self._absolute_path(
                        source_name
                    )
                )

            elif status_code == "D":
                changes.deleted.append(
                    self._absolute_path(
                        source_name
                    )
                )

            else:
                changes.modified.append(
                    self._absolute_path(
                        source_name
                    )
                )

    def _absolute_path(
        self,
        relative_path: str,
    ) -> Path:
        return (
            self.root
            / relative_path
        ).resolve()

    @staticmethod
    def _split_null(
        value: str,
    ) -> list[str]:
        return [
            token
            for token in value.split("\0")
            if token
        ]

    @staticmethod
    def _sort_changes(
        changes: GitChanges,
    ) -> None:
        changes.added.sort(
            key=str
        )
        changes.modified.sort(
            key=str
        )
        changes.deleted.sort(
            key=str
        )
        changes.renamed.sort(
            key=lambda item: (
                str(item[0]),
                str(item[1]),
            )
        )
