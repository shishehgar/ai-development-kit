"""
Deployment Models
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class DeploymentReport:

    score: int = 0

    docker: bool = False

    compose: bool = False

    ci_cd: bool = False

    kubernetes: bool = False

    cloud_ready: bool = False


    strengths: list[str] = field(
        default_factory=list
    )


    warnings: list[str] = field(
        default_factory=list
    )
