#!/usr/bin/python3

import os
import sys
from optparse import OptionParser


def tty(opts):
    try:
        ttyname = os.ttyname(sys.stdin.fileno())
    except OSError:
        if not opts.silent:
            print("not a tty")  # to stdout, not stderr
        sys.exit(1)
    else:
        if not opts.silent:
            print(ttyname)


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [OPTION]",
        description="Print the path to the terminal connected to standard input.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.add_option(
        "-s",
        "--silent",
        "--quiet",
        action="store_true",
        help="print nothing; only return an exit status",
    )

    opts, args = parser.parse_args()

    if args:
        parser.error(f"extra operand '{args[0]}'")

    tty(opts)
