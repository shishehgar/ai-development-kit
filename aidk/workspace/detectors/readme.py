"""
Readme detector.
"""

from pathlib import Path

from aidk.workspace.detectors import Detector


class ReadmeDetector(Detector):

    def detect(self, project: Path) -> bool:

        return any(
            (project / name).exists()
            for name in (
                "README.md",
                "README.rst",
                "README.txt",
            )
        )
