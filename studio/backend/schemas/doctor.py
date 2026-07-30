"""Doctor API schemas."""

from __future__ import annotations

from pydantic import BaseModel


class DoctorCheckResponse(BaseModel):
    key: str
    title: str
    status: str
    installed: bool
    required: bool
    executable: str | None = None
    path: str | None = None
    version: str | None = None
    message: str | None = None


class DoctorReportResponse(BaseModel):
    status: str
    health_score: int
    passed: int
    failed: int
    warnings: int
    python_version: str
    platform: str
    workspace: str
    checks: list[DoctorCheckResponse]
