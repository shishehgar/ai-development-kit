"""
Python Check
"""

from __future__ import annotations

import platform


class PythonCheck:

    name = "Python"

    def run(self):

        return {
            "ok": True,
            "message": platform.python_version(),
        }
