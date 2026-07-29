"""
Main CLI
"""

from __future__ import annotations

import argparse

from aidk.version import get_version
from aidk.commands.doctor import Doctor
from aidk.commands.workspace import Workspace
from aidk.commands.audit import Audit
from aidk.git.command import GitCommand
from aidk.audit.command import AuditCommand
from aidk.commands.git_report import GitReport


def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog="aidk",
        description="AI Development Kit",
    )

    sub = parser.add_subparsers(
        dest="command"
    )

    sub.add_parser(
        "version",
        help="Show version",
    )

    sub.add_parser(
        "doctor",
        help="Check installation",
    )

    sub.add_parser(
        "workspace",
        help="Analyze workspace",
    )

    sub.add_parser(
        "git",
        help="Inspect git repository",
    )

    sub.add_parser(
        "git-report",
        help="Generate git workspace report",
    )

    sub.add_parser(
        "init",
        help="Initialize project",
    )

    sub.add_parser(
        "build",
        help="Build project",
    )

    sub.add_parser(
        "audit",
        help="Engineering audit report",
    )

    sub.add_parser(
        "audit",
        help="Engineering audit",
    )

    return parser


def main():

    parser = build_parser()

    args = parser.parse_args()


    if args.command == "version":

        print(get_version())

        return 0


    if args.command == "doctor":

        Doctor().run()

        return 0


    if args.command == "workspace":

        Workspace().run()

        return 0


    if args.command == "git":

        return GitCommand().run()


    if args.command == "git-report":

        GitReport().run()

        return 0

    if args.command == "audit":

        return AuditCommand().run()


    if args.command == "init":

        print("Init: TODO")

        return 0


    if args.command == "build":

        print("Build: TODO")

        return 0


    parser.print_help()

    return 0


if __name__ == "__main__":
    main()
