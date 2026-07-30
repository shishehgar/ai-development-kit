"""Safe project path validation."""

from __future__ import annotations

from pathlib import Path

from studio.backend.core.config import settings
from studio.backend.schemas.projects import ProjectPathResult


class ProjectPathService:
    """Validate project paths before any AIDK operation is executed."""

    def validate(self, raw_path: str) -> ProjectPathResult:
        candidate = Path(raw_path).expanduser()

        try:
            resolved = candidate.resolve(strict=False)
        except OSError as exc:
            return ProjectPathResult(
                path=str(candidate),
                exists=False,
                is_directory=False,
                is_git_repository=False,
                allowed=False,
                message=f"امکان پردازش مسیر وجود ندارد: {exc}",
            )

        exists = resolved.exists()
        is_directory = resolved.is_dir()
        is_git = is_directory and (resolved / ".git").exists()

        try:
            resolved.relative_to(settings.workspace_root)
            inside_workspace = True
        except ValueError:
            inside_workspace = False

        allowed = exists and is_directory and inside_workspace

        if not exists:
            message = "مسیر موردنظر وجود ندارد."
        elif not is_directory:
            message = "مسیر انتخاب‌شده یک پوشه نیست."
        elif not inside_workspace:
            message = (
                "مسیر خارج از Workspace مجاز AIDK Studio قرار دارد."
            )
        else:
            message = "مسیر پروژه معتبر است."

        return ProjectPathResult(
            path=str(resolved),
            exists=exists,
            is_directory=is_directory,
            is_git_repository=is_git,
            allowed=allowed,
            message=message,
        )
