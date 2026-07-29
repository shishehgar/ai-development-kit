"""
Language detector.
"""

from pathlib import Path

from aidk.workspace.detectors import Detector


class LanguageDetector(Detector):

    def detect(self, project: Path) -> str:

        if (project / "pyproject.toml").exists():
            return "Python"

        if (project / "requirements.txt").exists():
            return "Python"

        if (project / "package.json").exists():
            return "Node.js"

        if (project / "go.mod").exists():
            return "Go"

        if (project / "Cargo.toml").exists():
            return "Rust"

        if list(project.glob("*.sln")):
            return ".NET"

        return "Unknown"
