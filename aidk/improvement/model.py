"""
Improvement Models
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class ImprovementItem:

    priority: int = 0

    problem: str = ""

    action: str = ""


@dataclass(slots=True)
class ImprovementPlan:

    project: str = ""

    current_score: int = 0

    items: list[ImprovementItem] = field(
        default_factory=list
    )
