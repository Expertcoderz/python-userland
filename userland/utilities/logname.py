#!/usr/bin/python3

import os

from .. import lib

parser = lib.create_parser(
    usage=("%prog",),
    description="Print the current user's login name.",
)


@lib.command(parser)
def python_userland_logname(_, args):
    if args:
        parser.error(f"extra operand '{args[0]}'")

    print(os.getlogin())

    return 0
