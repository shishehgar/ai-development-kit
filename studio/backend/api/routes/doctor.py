"""AIDK Doctor routes."""

from __future__ import annotations

from fastapi import APIRouter

from aidk.application.doctor_service import DoctorService
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
    report = DoctorService().run()

    return DoctorReportResponse.model_validate(
        report.to_dict()
    )
