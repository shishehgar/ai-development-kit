"""
Docker detector.
"""

from pathlib import Path

from aidk.workspace.detectors import Detector


class DockerDetector(Detector):

    def detect(self, project: Path) -> bool:

        return (
            (project / "Dockerfile").exists()
            or (project / "docker-compose.yml").exists()
            or (project / "compose.yml").exists()
        )
