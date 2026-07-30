"""
Dependency health analysis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum

from aidk.dependency.models import (
    Dependency,
    DependencyReport,
)


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class DependencyIssue:
    dependency: str
    issue_type: str
    message: str
    severity: Severity
    source: str = ""
    group: str = "runtime"


@dataclass
class DependencyHealthReport:
    project_name: str
    dependency_total: int
    score: int
    issues: list[DependencyIssue] = field(
        default_factory=list
    )

    @property
    def critical_total(self) -> int:
        return self._count(Severity.CRITICAL)

    @property
    def high_total(self) -> int:
        return self._count(Severity.HIGH)

    @property
    def medium_total(self) -> int:
        return self._count(Severity.MEDIUM)

    @property
    def low_total(self) -> int:
        return self._count(Severity.LOW)

    @property
    def healthy(self) -> bool:
        return (
            self.critical_total == 0
            and self.high_total == 0
        )

    def _count(
        self,
        severity: Severity,
    ) -> int:
        return sum(
            1
            for issue in self.issues
            if issue.severity == severity
        )


class DependencyHealthAnalyzer:

    EXACT_VERSION_PATTERN = re.compile(
        r"^={2,3}\s*[A-Za-z0-9_.+-]+$"
    )

    RANGE_PATTERN = re.compile(
        r"(>=|<=|~=|\^|~|>|<)"
    )

    LOCAL_PATTERN = re.compile(
        r"(^\.{0,2}/|^/|^file:|^path:)",
        re.IGNORECASE,
    )

    URL_PATTERN = re.compile(
        r"(https?://|git\+|git@|github\.com)",
        re.IGNORECASE,
    )

    WILDCARD_PATTERN = re.compile(
        r"(^|\D)[xX*](\D|$)"
    )

    def analyze(
        self,
        report: DependencyReport,
    ) -> DependencyHealthReport:
        issues: list[DependencyIssue] = []

        for dependency in report.dependencies:
            issues.extend(
                self._analyze_dependency(
                    dependency
                )
            )

        issues.extend(
            self._analyze_duplicates(report)
        )

        issues.extend(
            self._analyze_parse_errors(report)
        )

        issues.sort(
            key=lambda issue: (
                self._severity_rank(
                    issue.severity
                ),
                issue.dependency,
                issue.issue_type,
            )
        )

        score = self._calculate_score(
            issues
        )

        return DependencyHealthReport(
            project_name=report.project_name,
            dependency_total=report.total,
            score=score,
            issues=issues,
        )

    def _analyze_dependency(
        self,
        dependency: Dependency,
    ) -> list[DependencyIssue]:
        issues: list[DependencyIssue] = []

        version = dependency.version.strip()

        if not version:
            issues.append(
                self._issue(
                    dependency,
                    issue_type="unpinned",
                    message=(
                        "Dependency has no version "
                        "constraint."
                    ),
                    severity=Severity.HIGH,
                )
            )
            return issues

        if version in {"*", "latest"}:
            issues.append(
                self._issue(
                    dependency,
                    issue_type="floating-version",
                    message=(
                        "Dependency uses a floating "
                        "version."
                    ),
                    severity=Severity.HIGH,
                )
            )

        elif self.WILDCARD_PATTERN.search(version):
            issues.append(
                self._issue(
                    dependency,
                    issue_type="wildcard-version",
                    message=(
                        "Dependency version contains "
                        "a wildcard."
                    ),
                    severity=Severity.MEDIUM,
                )
            )

        if self.URL_PATTERN.search(version):
            severity = (
                Severity.HIGH
                if not self._contains_commit_hash(
                    version
                )
                else Severity.MEDIUM
            )

            issues.append(
                self._issue(
                    dependency,
                    issue_type="remote-source",
                    message=(
                        "Dependency is installed from "
                        "a remote URL or Git source."
                    ),
                    severity=severity,
                )
            )

        if self.LOCAL_PATTERN.search(version):
            issues.append(
                self._issue(
                    dependency,
                    issue_type="local-source",
                    message=(
                        "Dependency uses a local path "
                        "and may not be reproducible."
                    ),
                    severity=Severity.MEDIUM,
                )
            )

        if self._is_range(version):
            issues.append(
                self._issue(
                    dependency,
                    issue_type="version-range",
                    message=(
                        "Dependency allows multiple "
                        "versions."
                    ),
                    severity=Severity.LOW,
                )
            )

        if dependency.group == "runtime":
            if self._looks_like_dev_dependency(
                dependency.normalized_name
            ):
                issues.append(
                    self._issue(
                        dependency,
                        issue_type="dev-runtime-mismatch",
                        message=(
                            "Development dependency "
                            "appears in the runtime group."
                        ),
                        severity=Severity.LOW,
                    )
                )

        return issues

    def _analyze_duplicates(
        self,
        report: DependencyReport,
    ) -> list[DependencyIssue]:
        issues: list[DependencyIssue] = []

        for name, dependencies in (
            report.duplicates.items()
        ):
            versions = {
                dependency.version.strip()
                for dependency in dependencies
            }

            sources = sorted(
                {
                    dependency.source
                    for dependency in dependencies
                    if dependency.source
                }
            )

            if len(versions) > 1:
                severity = Severity.HIGH
                message = (
                    "Dependency has conflicting "
                    "version declarations."
                )
                issue_type = "version-conflict"
            else:
                severity = Severity.MEDIUM
                message = (
                    "Dependency is declared more "
                    "than once."
                )
                issue_type = "duplicate"

            issues.append(
                DependencyIssue(
                    dependency=name,
                    issue_type=issue_type,
                    message=message,
                    severity=severity,
                    source=", ".join(sources),
                    group="multiple",
                )
            )

        return issues

    @staticmethod
    def _analyze_parse_errors(
        report: DependencyReport,
    ) -> list[DependencyIssue]:
        return [
            DependencyIssue(
                dependency="project",
                issue_type="parse-error",
                message=error,
                severity=Severity.HIGH,
                source="",
                group="project",
            )
            for error in report.errors
        ]

    @staticmethod
    def _issue(
        dependency: Dependency,
        issue_type: str,
        message: str,
        severity: Severity,
    ) -> DependencyIssue:
        return DependencyIssue(
            dependency=dependency.name,
            issue_type=issue_type,
            message=message,
            severity=severity,
            source=dependency.source,
            group=dependency.group,
        )

    def _is_range(
        self,
        version: str,
    ) -> bool:
        if self.EXACT_VERSION_PATTERN.match(
            version
        ):
            return False

        return bool(
            self.RANGE_PATTERN.search(version)
        )

    @staticmethod
    def _contains_commit_hash(
        value: str,
    ) -> bool:
        return bool(
            re.search(
                r"[@#][0-9a-f]{7,40}(?:\b|$)",
                value,
                re.IGNORECASE,
            )
        )

    @staticmethod
    def _looks_like_dev_dependency(
        name: str,
    ) -> bool:
        tokens = (
            "pytest",
            "ruff",
            "flake8",
            "mypy",
            "black",
            "isort",
            "coverage",
            "tox",
            "nox",
            "eslint",
            "prettier",
            "jest",
            "vitest",
            "typescript",
        )

        return any(
            name == token
            or name.startswith(f"{token}-")
            for token in tokens
        )

    @staticmethod
    def _calculate_score(
        issues: list[DependencyIssue],
    ) -> int:
        penalties = {
            Severity.CRITICAL: 30,
            Severity.HIGH: 15,
            Severity.MEDIUM: 7,
            Severity.LOW: 2,
        }

        score = 100

        for issue in issues:
            score -= penalties[
                issue.severity
            ]

        return max(0, score)

    @staticmethod
    def _severity_rank(
        severity: Severity,
    ) -> int:
        ranks = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3,
        }

        return ranks[severity]
