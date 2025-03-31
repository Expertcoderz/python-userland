#!/usr/bin/python3

import os
import sys
from optparse import OptionParser


# reset(1), roughly modelled off the ncurses implementation.


def reset(opts, term: str | None = os.environ.get("TERM")):
    if opts.q:
        if not term:
            print("unknown terminal type ", file=sys.stderr)
            try:
                while True:
                    if term := input("Terminal type? "):
                        break
            except KeyboardInterrupt:
                print()
                sys.exit(130)

        print(term)
        return

    print("\x1bc", end="")

    if opts.r:
        print(f"Terminal type is {term}.")

    if opts.s:
        print(f"TERM={term};")


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [OPTION]... [IGNORED]...",
        description="Initialize or reset the terminal state.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.add_option("-I", action="store_true", help="(unimplemented)")
    parser.add_option("-c", action="store_true", help="(unimplemented)")
    parser.add_option("-Q", action="store_true", help="(unimplemented)")

    parser.add_option(
        "-q",
        action="store_true",
        help="print the terminal type; do not initialize the terminal",
    )
    parser.add_option(
        "-r", action="store_true", help="print the terminal type to standard error"
    )
    parser.add_option(
        "-s",
        action="store_true",
        help="print the sequence of shell commands to initialize the TERM environment variable",
    )

    parser.add_option("-w", action="store_true", help="(unimplemented)")

    parser.add_option("-e", metavar="CHAR", help="(unimplemented)")
    parser.add_option("-i", metavar="CHAR", help="(unimplemented)")
    parser.add_option("-k", metavar="CHAR", help="(unimplemented)")

    parser.add_option("-m", metavar="MAPPING", help="(unimplemented)")

    opts, args = parser.parse_args()

    if args and args[0] == "-":
        opts.q = True
        del args[0]

    if args:
        reset(opts, args[0])
    else:
        reset(opts)
