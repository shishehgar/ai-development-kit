"""
Workspace Project Model
"""

from dataclasses import dataclass, field
from pathlib import Path

from aidk.git.models import GitInfo


@dataclass
class Project:

    name: str

    path: Path

    language: str = "Unknown"

    git: bool = False

    git_info: GitInfo = field(
        default_factory=GitInfo
    )

    docker: bool = False

    continue_config: bool = False

    readme: bool = False

    license: bool = False

    tests: bool = False


    # Existing score
    score: int = 0


    # Intelligence fields

    intelligence_score: int = 0

    grade: str = "D"


    strengths: list[str] = field(
        default_factory=list
    )


    weaknesses: list[str] = field(
        default_factory=list
    )


    recommendations: list[str] = field(
        default_factory=list
    )
