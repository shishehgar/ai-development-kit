"""Lightweight source-code retrieval for assistant requests."""

from __future__ import annotations

import re
from pathlib import Path

from aidk.ai.retrieval.models import RetrievedContext


_TOKEN_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]*")

_DEFAULT_SUFFIXES = frozenset(
    {
        ".py",
        ".ts",
        ".tsx",
        ".js",
        ".jsx",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".md",
    }
)

_EXCLUDED_DIRECTORIES = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "dist",
        "build",
        "node_modules",
    }
)


class CodeContextRetriever:
    """Find source files and lines relevant to a question."""

    def __init__(
        self,
        project_root: str | Path,
        *,
        max_files: int = 500,
        max_matches: int = 10,
        max_file_size: int = 512_000,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.max_files = max_files
        self.max_matches = max_matches
        self.max_file_size = max_file_size

    def retrieve(
        self,
        question: str,
    ) -> RetrievedContext:
        normalized = question.strip()
        tokens = self._tokens(normalized)

        if not tokens or not self.project_root.exists():
            return RetrievedContext(
                question=normalized
            )

        matches: list[dict[str, object]] = []

        for path in self._source_files():
            match = self._match_file(
                path,
                tokens,
            )

            if match is None:
                continue

            matches.append(match)

            if len(matches) >= self.max_matches:
                break

        matches.sort(
            key=lambda item: int(item["score"]),
            reverse=True,
        )

        return RetrievedContext(
            question=normalized,
            code_matches=matches,
        )

    def _source_files(self) -> list[Path]:
        files: list[Path] = []

        for path in self.project_root.rglob("*"):
            if len(files) >= self.max_files:
                break

            if not path.is_file():
                continue

            if path.suffix.lower() not in _DEFAULT_SUFFIXES:
                continue

            if any(
                part in _EXCLUDED_DIRECTORIES
                for part in path.parts
            ):
                continue

            try:
                if path.stat().st_size > self.max_file_size:
                    continue
            except OSError:
                continue

            files.append(path)

        return sorted(files)

    def _match_file(
        self,
        path: Path,
        tokens: list[str],
    ) -> dict[str, object] | None:
        try:
            content = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except OSError:
            return None

        relative_path = path.relative_to(
            self.project_root
        ).as_posix()

        lowered_content = content.casefold()
        lowered_path = relative_path.casefold()

        score = 0

        for token in tokens:
            score += lowered_content.count(token)

            if token in lowered_path:
                score += 5

        if score <= 0:
            return None

        snippets = self._matching_lines(
            content,
            tokens,
        )

        return {
            "path": relative_path,
            "score": score,
            "snippets": snippets,
        }

    @staticmethod
    def _tokens(
        question: str,
    ) -> list[str]:
        tokens = _TOKEN_PATTERN.findall(
            question.casefold()
        )

        return list(dict.fromkeys(tokens))

    @staticmethod
    def _matching_lines(
        content: str,
        tokens: list[str],
        *,
        limit: int = 5,
    ) -> list[dict[str, object]]:
        snippets: list[dict[str, object]] = []

        for line_number, line in enumerate(
            content.splitlines(),
            start=1,
        ):
            lowered_line = line.casefold()

            if not any(
                token in lowered_line
                for token in tokens
            ):
                continue

            snippets.append(
                {
                    "line": line_number,
                    "text": line.strip()[:300],
                }
            )

            if len(snippets) >= limit:
                break

        return snippets
