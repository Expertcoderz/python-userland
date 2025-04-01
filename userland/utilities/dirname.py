#!/usr/bin/python3

from pathlib import PurePath

from .. import lib

parser = lib.create_parser(
    usage=("%prog [OPTION]... NAME...",),
    description=(
        "Print each path NAME with the last component removed,"
        " or '.' if NAME is the only component."
    ),
)
parser.add_option("--help", action="help", help="show usage information and exit")

parser.add_option(
    "-z",
    "--zero",
    action="store_true",
    help="terminate outputs with NUL instead of newline",
)


@lib.command(parser)
def python_userland_dirname(opts, args):
    if not args:
        parser.error("missing operand")

    for path in map(PurePath, args):
        print(path.parent, end="\0" if opts.zero else "\n")

    return 0
