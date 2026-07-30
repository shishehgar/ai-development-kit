"""Audit API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class AuditReportResponse(BaseModel):
    root: str
    total_projects: int
    average_score: float
    grade_distribution: dict[str, int]
    missing_readme: int
    missing_tests: int
    missing_ai_config: int
    missing_license: int
    missing_docker: int
    critical_projects: list[str]
    recommendations: list[str]
