"""
Git Printer
"""

from aidk.git.models import GitInfo


class GitPrinter:

    @staticmethod
    def show(info: GitInfo):

        print()

        print("=" * 60)

        print("Git Information")

        print("=" * 60)

        print(f"Repository : {info.exists}")

        print(f"Branch     : {info.branch}")

        print(f"Clean      : {info.clean}")

        print(f"Modified   : {info.modified_files}")

        print(f"Staged     : {info.staged_files}")

        print(f"Untracked  : {info.untracked_files}")

        print(f"Remote     : {info.remote}")

        print(f"Remote URL : {info.remote_url}")

        print(f"Commit     : {info.last_commit_hash}")

        print(f"Author     : {info.last_commit_author}")

        print(f"Date       : {info.last_commit_date}")
