"""
Process execution utilities.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class ProcessRunner:
    """Execute external commands safely."""

    @staticmethod
    def run(command: list[str], cwd: Path | None = None) -> tuple[bool, str]:

        try:

            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            if result.returncode == 0:
                return True, result.stdout.strip()

            return False, result.stderr.strip()

        except Exception as exc:
            return False, str(exc)
