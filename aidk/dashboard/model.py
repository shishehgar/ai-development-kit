"""
Workspace Dashboard Models
"""

from dataclasses import dataclass, field



@dataclass(slots=True)
class WorkspaceDashboard:

    projects: int = 0

    average_score: int = 0

    levels: dict = field(
        default_factory=dict
    )

    ranking: list = field(
        default_factory=list
    )

    critical_projects: list = field(
        default_factory=list
    )
