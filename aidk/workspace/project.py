"""
Workspace Project Model
"""

from dataclasses import dataclass, field
from pathlib import Path
from aidk.security.models import SecurityReport
from aidk.git.models import GitInfo
from aidk.knowledge.models import Knowledge
from aidk.deployment.models import DeploymentReport
from aidk.maturity.model import MaturityReport


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

    documentation_score: int = 0

    strengths: list[str] = field(
        default_factory=list
    )


    weaknesses: list[str] = field(
        default_factory=list
    )


    recommendations: list[str] = field(
        default_factory=list
    )


    knowledge: Knowledge = field(
        default_factory=Knowledge
    )


    security: SecurityReport = field(
        default_factory=SecurityReport
    )


    deployment: DeploymentReport = field(
        default_factory=DeploymentReport
    )


    maturity: MaturityReport = field(
        default_factory=MaturityReport
    )
