"""
Knowledge Models
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class Knowledge:

    readme: bool = False

    license: bool = False

    contributing: bool = False

    changelog: bool = False

    code_of_conduct: bool = False

    architecture: bool = False

    docs: bool = False

    wiki: bool = False

    api_docs: bool = False

    score: int = 0

    missing: list[str] = field(default_factory=list)
