"""AIDK Doctor routes."""

from __future__ import annotations

from fastapi import APIRouter

from aidk.app import app
from studio.backend.schemas.doctor import DoctorReportResponse

router = APIRouter(
    prefix="/doctor",
    tags=["doctor"],
)


@router.get(
    "",
    response_model=DoctorReportResponse,
)
def run_doctor() -> DoctorReportResponse:
    report = app.services.doctor.run()

    return DoctorReportResponse.model_validate(
        report.to_dict()
    )
