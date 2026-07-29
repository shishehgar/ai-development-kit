"""
Tests detector.
"""

from pathlib import Path

from aidk.workspace.detectors import Detector


class TestsDetector(Detector):

    def detect(self, project: Path) -> bool:

        return (
            (project / "tests").exists()
            or (project / "test").exists()
        )
