"""
Auto Fix Models
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class FixTask:

    title: str

    path: str

    content: str


@dataclass(slots=True)
class FixPlan:

    project: str

    tasks: list[FixTask] = field(
        default_factory=list
    )
