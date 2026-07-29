"""
Doctor Command
"""

from __future__ import annotations

from aidk.core.doctor_engine import DoctorEngine


class Doctor:

    def run(self) -> int:

        DoctorEngine().run()

        return 0
