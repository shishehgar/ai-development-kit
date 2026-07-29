"""
Audit Models
"""

from dataclasses import dataclass, field


@dataclass
class AuditReport:

    total_projects: int = 0

    average_score: float = 0

    grade_distribution: dict = field(
        default_factory=dict
    )


    missing_readme: int = 0

    missing_tests: int = 0

    missing_ai_config: int = 0

    missing_license: int = 0

    missing_docker: int = 0


    critical_projects: list = field(
        default_factory=list
    )


    recommendations: list = field(
        default_factory=list
    )
