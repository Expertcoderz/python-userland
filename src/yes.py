#!/usr/bin/python3

import sys
from optparse import OptionParser


def yes(_, strings: list[str]):
    try:
        string = " ".join(strings or ["y"])
        while True:
            print(string)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [STRING]...",
        description="Repeatedly output a line with STRING(s) (or 'y' by default).",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    yes(*parser.parse_args())
