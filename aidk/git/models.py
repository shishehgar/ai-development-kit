"""
Git models
"""

from dataclasses import dataclass


@dataclass(slots=True)
class GitInfo:
    exists: bool = False

    repository_root: str = ""

    branch: str = ""

    default_branch: str = ""

    clean: bool = False

    modified_files: int = 0

    staged_files: int = 0

    untracked_files: int = 0

    remote: bool = False

    remote_name: str = ""

    remote_url: str = ""

    last_commit_hash: str = ""

    last_commit_author: str = ""

    last_commit_date: str = ""

    ahead: int = 0

    behind: int = 0
