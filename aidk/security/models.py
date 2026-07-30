"""
Security Models
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class SecurityReport:

    score: int = 0

    secrets_found: bool = False

    env_exposed: bool = False

    security_policy: bool = False

    gitignore_present: bool = False

    warnings: list[str] = field(
        default_factory=list
    )

    strengths: list[str] = field(
        default_factory=list
    )
