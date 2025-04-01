#!/usr/bin/python3

import os

from .. import lib

parser = lib.create_parser(
    usage=("%prog",),
    description="Print the current username. Same as `id -un`.",
)


@lib.command(parser)
def python_userland_whoami(_, args):
    if args:
        parser.error(f"extra operand '{args[0]}'")

    print(os.getlogin())

    return 0
