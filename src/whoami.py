#!/usr/bin/python3

import os
from optparse import OptionParser


def whoami():
    print(os.getlogin())


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog",
        description="Print the current username. Same as `id -un`.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    opts, args = parser.parse_args()

    if args:
        parser.error(f"extra operand '{args[0]}'")

    whoami()
