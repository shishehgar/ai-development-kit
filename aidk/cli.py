"""
Main CLI
"""

from __future__ import annotations

import argparse

from aidk.core.load_commands import build_registry


def main():

    registry = build_registry()

    parser = argparse.ArgumentParser(
        prog="aidk",
        description="AI Development Kit",
    )

    sub = parser.add_subparsers(
        dest="command"
    )

    commands = {}

    for command in registry.all():

        p = sub.add_parser(
            command.name,
            help=command.help,
        )

        command.configure(p)

        commands[
            command.name
        ] = command

    args = parser.parse_args()

    if args.command is None:

        parser.print_help()

        return 0

    return commands[
        args.command
    ].run(args)


if __name__ == "__main__":

    raise SystemExit(main())
