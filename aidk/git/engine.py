"""
Git Engine
"""

from pathlib import Path

from aidk.core.process import ProcessRunner
from aidk.git.models import GitInfo


class GitEngine:

    def inspect(self, project: Path) -> GitInfo:

        info = GitInfo()

        ok, _ = ProcessRunner.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=project,
        )

        if not ok:
            return info

        info.exists = True

        ok, output = ProcessRunner.run(
            ["git", "branch", "--show-current"],
            cwd=project,
        )

        if ok:
            info.branch = output

        ok, output = ProcessRunner.run(
            ["git", "status", "--porcelain"],
            cwd=project,
        )

        if ok:

            info.clean = len(output.strip()) == 0

            if not info.clean:

                for line in output.splitlines():

                    if line.startswith("??"):
                        info.untracked_files += 1

                    else:

                        if line[0] != " ":
                            info.staged_files += 1

                        if line[1] != " ":
                            info.modified_files += 1

        ok, output = ProcessRunner.run(
            ["git", "remote"],
            cwd=project,
        )

        if ok and output:

            info.remote = True

            info.remote_name = output.splitlines()[0]

            ok2, url = ProcessRunner.run(
                [
                    "git",
                    "remote",
                    "get-url",
                    info.remote_name,
                ],
                cwd=project,
            )

            if ok2:
                info.remote_url = url

        ok, output = ProcessRunner.run(
            [
                "git",
                "log",
                "-1",
                "--pretty=format:%h|%an|%ad",
                "--date=iso",
            ],
            cwd=project,
        )

        if ok and output:

            parts = output.split("|")

            if len(parts) == 3:

                info.last_commit_hash = parts[0]

                info.last_commit_author = parts[1]

                info.last_commit_date = parts[2]

        return info
