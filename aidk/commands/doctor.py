"""
Doctor Command
"""

from aidk.core.doctor_engine import DoctorEngine


class Doctor:

    def run(self):

        DoctorEngine().run()

        return 0
