"""
Maturity Models
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MaturityReport:

    score: int = 0

    level: str = "Initial"
