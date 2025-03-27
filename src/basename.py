#!/usr/bin/python3

import os
from optparse import OptionParser


def basename(opts, names: list[str]):
    for name in names:
        print(
            os.path.basename(name.removesuffix(opts.suffix)),
            end="\0" if opts.zero else "\n",
        )


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog NAME [SUFFIX]\n       %prog OPTION... NAME...",
        description="Print the last component of each path NAME.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.add_option(
        "-a", "--multiple", action="store_true", help="support multiple NAMES"
    )
    parser.add_option(
        "-s",
        "--suffix",
        metavar="SUFFIX",
        help="remove trailing SUFFIX; implies -a",
    )

    parser.add_option(
        "-z",
        "--zero",
        action="store_true",
        help="terminate outputs with NUL instead of newline",
    )

    opts, args = parser.parse_args()

    if not args:
        parser.error("missing operand")

    if opts.suffix:
        opts.multiple = True
    elif not opts.multiple and len(args) > 1:
        if len(args) > 2:
            parser.error(f"extra operand '{args[2]}'")

        opts.suffix = args.pop()
    else:
        opts.suffix = ""

    basename(opts, args)
