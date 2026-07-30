"""
Dependency models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Dependency:
    name: str
    version: str = ""
    source: str = ""
    group: str = "runtime"
    optional: bool = False

    @property
    def normalized_name(self) -> str:
        return self.name.strip().lower().replace("_", "-")


@dataclass
class DependencyReport:
    project_name: str
    project_path: Path
    dependencies: list[Dependency] = field(
        default_factory=list
    )
    files: list[Path] = field(
        default_factory=list
    )
    duplicates: dict[str, list[Dependency]] = field(
        default_factory=dict
    )
    errors: list[str] = field(
        default_factory=list
    )

    @property
    def total(self) -> int:
        return len(self.dependencies)

    @property
    def runtime_total(self) -> int:
        return sum(
            1
            for dependency in self.dependencies
            if dependency.group == "runtime"
        )

    @property
    def development_total(self) -> int:
        return sum(
            1
            for dependency in self.dependencies
            if dependency.group == "development"
        )

    @property
    def optional_total(self) -> int:
        return sum(
            1
            for dependency in self.dependencies
            if dependency.optional
        )

    @property
    def unique_total(self) -> int:
        return len(
            {
                dependency.normalized_name
                for dependency in self.dependencies
            }
        )
