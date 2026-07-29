"""
Git Risk Models
"""

from dataclasses import dataclass, field


@dataclass
class GitRisk:

    project: str

    level: str

    reasons: list[str] = field(
        default_factory=list
    )
