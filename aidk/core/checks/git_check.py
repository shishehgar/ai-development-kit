"""
Git Check
"""

from __future__ import annotations

import shutil
import subprocess


class GitCheck:

    name = "Git"

    def run(self):

        executable = shutil.which("git")

        if executable is None:

            return {
                "ok": False,
                "message": "Git not installed",
            }

        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
        )

        return {
            "ok": True,
            "message": result.stdout.strip(),
        }
