#!/usr/bin/python3

import os

from .. import core

UNAME_ATTRS = frozenset("mnrsv")


parser = core.create_parser(
    usage=("%prog [OPTION]...",),
    description="Print system information.",
)

parser.add_option(
    "-a",
    "--all",
    action="store_true",
    help="print all",
)
parser.add_option(
    "-s",
    "--kernel-name",
    action="store_true",
    help="print kernel name (default)",
)
parser.add_option(
    "-n",
    "--nodename",
    action="store_true",
    help="print hostname",
)
parser.add_option(
    "-r",
    "--kernel-release",
    action="store_true",
    help="print kernel release",
)
parser.add_option(
    "-v",
    "--kernel-version",
    action="store_true",
    help="print kernel version",
)
parser.add_option(
    "-m",
    "--machine",
    action="store_true",
    help="print machine hardware type",
)
parser.add_option(
    "-p",
    "--processor",
    action="store_true",
    help="print processor type (unimplemented)",
)
parser.add_option(
    "-i",
    "--hardware-platform",
    action="store_true",
    help="print hardware platform (unimplemented)",
)
parser.add_option(
    "-o",
    "--operating-system",
    action="store_true",
    help="print operating system (unimplemented)",
)


@core.command(parser)
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
