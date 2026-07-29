"""
Git detector.
"""

from pathlib import Path

from aidk.workspace.detectors import Detector


class GitDetector(Detector):

    def detect(self, project: Path) -> bool:

        return (project / ".git").exists()
