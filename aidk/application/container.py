"""Application service container for AIDK."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from aidk.application.doctor_service import DoctorService


@dataclass(frozen=True)
class ApplicationServices:
    """Services shared by AIDK interfaces."""

    doctor: DoctorService


def build_services(
    *,
    workspace: Path | None = None,
) -> ApplicationServices:
    """Build the application service container."""

    return ApplicationServices(
        doctor=DoctorService(
            workspace=workspace,
        ),
    )


services = build_services()
