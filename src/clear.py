#!/usr/bin/python3

import sys
from optparse import OptionParser

# clear(1), roughly modelled off the ncurses implementation.


def clear(opts):
    print("\x1b[2J\x1b[H", end="")
    if not opts.x:
        print("\x1b[3J", end="")


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [OPTION]...",
        description="Clear the terminal screen.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.add_option("-T", metavar="TERM", help="(unimplemented)")

    parser.add_option(
        "-x", action="store_true", help="do not try to clear the scrollback buffer"
    )

    opts, args = parser.parse_args()

    if args:
        sys.exit(1)

    clear(opts)
