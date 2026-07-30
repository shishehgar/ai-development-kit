"""Audit API routes."""

from __future__ import annotations

from fastapi import APIRouter

from aidk.app import app
from studio.backend.schemas.audit import (
    AuditReportResponse,
)

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
)


@router.get(
    "",
    response_model=AuditReportResponse,
)
def run_audit() -> AuditReportResponse:
    report = app.services.audit.run()

    return AuditReportResponse.model_validate(
        report.to_dict()
    )
