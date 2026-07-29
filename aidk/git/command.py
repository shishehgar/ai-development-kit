"""
Git Command
"""

from pathlib import Path

from aidk.git.engine import GitEngine
from aidk.git.printer import GitPrinter


class GitCommand:

    def run(self):

        info = GitEngine().inspect(Path.cwd())

        GitPrinter.show(info)

        return 0
