#!/usr/bin/python3

from optparse import OptionParser
from pathlib import PurePath


def dirname(opts, paths: list[PurePath]):
    for path in paths:
        print(path.parent, end="\0" if opts.zero else "\n")


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [OPTION]... NAME...",
        description=(
            "Print each path NAME with the last component removed,"
            " or '.' if NAME is the only component."
        ),
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.add_option(
        "-z",
        "--zero",
        action="store_true",
        help="terminate outputs with NUL instead of newline",
    )

    opts, args = parser.parse_args()

    if not args:
        parser.error("missing operand")

    dirname(opts, map(PurePath, args))
