#!/usr/bin/python3

import os

from .. import lib

UNAME_ATTRS = frozenset("mnrsv")


parser = lib.create_parser(
    usage=("%prog [OPTION]...",),
    description="Print system information.",
)

parser.add_option("-a", action="store_true", help="print all")
parser.add_option("-m", action="store_true", help="machine hardware type")
parser.add_option("-n", action="store_true", help="hostname")
parser.add_option("-r", action="store_true", help="kernel release")
parser.add_option("-s", action="store_true", help="kernel name (default)")
parser.add_option("-v", action="store_true", help="kernel version")
parser.add_option("-p", action="store_true", help="processor type")
parser.add_option("-i", action="store_true", help="hardware platform (unimplemented)")
parser.add_option("-o", action="store_true", help="operating system (unimplemented)")


@lib.command(parser)
def python_userland_uname(opts, args):
    if args:
        parser.error(f"extra operand '{args[0]}'")

    extras: list[str] = []

    if opts.a:
        for attr in UNAME_ATTRS:
            setattr(opts, attr, True)
    else:
        if opts.p:
            extras.append("unknown")

        if opts.i:
            extras.append("unknown")

        if opts.o:
            extras.append("unknown")

    if not extras and not any({getattr(opts, attr) for attr in UNAME_ATTRS}):
        opts.s = True

    uname = os.uname()

    print(
        " ".join(
            [
                getattr(uname, attribute)
                for attribute in [
                    "sysname",
                    "nodename",
                    "release",
                    "version",
                    "machine",
                ]
                if getattr(opts, attribute[0])
            ]
            + extras
        )
    )

    return 0
