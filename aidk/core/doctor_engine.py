"""
Professional Doctor Engine
"""

from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path


class DoctorEngine:

    def __init__(self):

        self.total = 0
        self.success = 0

    # --------------------------------------------------

    def header(self):

        print()
        print("=" * 70)
        print("AI Development Kit Doctor")
        print("=" * 70)

    # --------------------------------------------------

    def get_version(self, executable):

        try:

            result = subprocess.run(
                [executable, "--version"],
                capture_output=True,
                text=True,
                timeout=3,
            )

            text = result.stdout.strip()

            if not text:
                text = result.stderr.strip()

            return text.splitlines()[0]

        except Exception:

            return None

    # --------------------------------------------------

    def check_program(self, title, executable):

        self.total += 1

        path = shutil.which(executable)

        if not path:

            print(f"[FAIL] {title:<20}")

            return

        self.success += 1

        version = self.get_version(executable)

        if version:

            print(f"[ OK ] {title:<20} {version}")

        else:

            print(f"[ OK ] {title:<20} Installed")

    # --------------------------------------------------

    def check_workspace(self):

        self.total += 1

        workspace = Path("/home/ubuntu/my_services")

        if workspace.exists():

            self.success += 1

            print(f"[ OK ] Workspace            {workspace}")

        else:

            print("[FAIL] Workspace")

    # --------------------------------------------------

    def check_python(self):

        print()

        print("Python")

        print("-" * 70)

        print(platform.python_version())

    # --------------------------------------------------

    def footer(self):

        print()

        print("-" * 70)

        score = int(self.success / self.total * 100)

        print(f"Health Score : {score}%")

        print(f"Passed       : {self.success}")

        print(f"Failed       : {self.total-self.success}")

        print("-" * 70)

    # --------------------------------------------------

    def run(self):

        self.header()

        self.check_python()

        print()

        print("Installed Tools")

        print("-" * 70)

        self.check_program("Git", "git")
        self.check_program("Python", "python3")
        self.check_program("Docker", "docker")
        self.check_program("Node", "node")
        self.check_program("npm", "npm")
        self.check_program("GitHub CLI", "gh")
        self.check_program("AWS CLI", "aws")
        self.check_program("Ollama", "ollama")

        self.check_workspace()

        self.footer()
