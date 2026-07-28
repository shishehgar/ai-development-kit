"""
Doctor Command
"""

from __future__ import annotations

import platform
import shutil
import subprocess
from dataclasses import dataclass


@dataclass
class CheckResult:

    name: str
    ok: bool
    version: str = ""


class Doctor:

    @staticmethod
    def command_exists(command: str) -> bool:

        return shutil.which(command) is not None

    @staticmethod
    def command_version(command: list[str]) -> str:

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=5,
            )

            output = (
                result.stdout.strip()
                or result.stderr.strip()
            )

            return output.splitlines()[0]

        except Exception:

            return ""

    def check_python(self):

        return CheckResult(
            "Python",
            True,
            platform.python_version(),
        )

    def check_git(self):

        ok = self.command_exists("git")

        return CheckResult(
            "Git",
            ok,
            self.command_version(
                ["git", "--version"]
            ) if ok else "",
        )

    def check_docker(self):

        ok = self.command_exists("docker")

        return CheckResult(
            "Docker",
            ok,
            self.command_version(
                ["docker", "--version"]
            ) if ok else "",
        )

    def check_node(self):

        ok = self.command_exists("node")

        return CheckResult(
            "Node.js",
            ok,
            self.command_version(
                ["node", "-v"]
            ) if ok else "",
        )

    def check_npm(self):

        ok = self.command_exists("npm")

        return CheckResult(
            "npm",
            ok,
            self.command_version(
                ["npm", "-v"]
            ) if ok else "",
        )

    def run(self):

        checks = [

            self.check_python(),

            self.check_git(),

            self.check_docker(),

            self.check_node(),

            self.check_npm(),

        ]

        print()

        print("=" * 60)

        print("AI DEVELOPMENT KIT DOCTOR")

        print("=" * 60)

        print()

        for item in checks:

            status = "✓" if item.ok else "✗"

            print(
                f"{status:2} "
                f"{item.name:<15}"
                f"{item.version}"
            )

        print()
