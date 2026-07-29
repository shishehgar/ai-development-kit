"""
License detector.
"""

from pathlib import Path

from aidk.workspace.detectors import Detector


class LicenseDetector(Detector):

    def detect(self, project: Path) -> bool:

        return any(
            (project / name).exists()
            for name in (
                "LICENSE",
                "LICENSE.md",
                "LICENSE.txt",
            )
        )
