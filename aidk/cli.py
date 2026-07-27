"""
Main CLI
"""

from __future__ import annotations

import argparse

from aidk.version import get_version


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
        "init",
        help="Initialize project",
    )

    sub.add_parser(
        "build",
        help="Build project",
    )

    return parser


def main():

    parser = build_parser()

    args = parser.parse_args()

    if args.command == "version":

        print(get_version())

        return

    if args.command == "doctor":

        print("Doctor: OK")

        return

    if args.command == "init":

        print("Init: TODO")

        return

    if args.command == "build":

        print("Build: TODO")

        return

    parser.print_help()


if __name__ == "__main__":
    main()
