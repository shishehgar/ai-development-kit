"""
Continue detector.
"""

from pathlib import Path

from aidk.workspace.detectors import Detector


class ContinueDetector(Detector):

    def detect(self, project: Path) -> bool:

        return (project / ".continue").exists()
