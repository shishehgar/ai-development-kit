"""
Workspace detectors package.
"""

from pathlib import Path
from abc import ABC, abstractmethod


class Detector(ABC):
    """Base detector."""

    @abstractmethod
    def detect(self, project: Path):
        """Detect project information."""
        raise NotImplementedError
