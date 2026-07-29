"""
Git Report Models
"""

from dataclasses import dataclass, field


@dataclass
class GitRiskItem:

    project: str

    level: str

    reasons: list[str] = field(
        default_factory=list
    )


@dataclass
class GitReport:

    total_projects: int = 0

    clean_repositories: int = 0

    dirty_repositories: int = 0

    branches: dict = field(
        default_factory=dict
    )

    remote_count: int = 0

    no_remote_count: int = 0

    risks: list[GitRiskItem] = field(
        default_factory=list
    )
