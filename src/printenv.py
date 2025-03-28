#!/usr/bin/python3

import os
import sys
from optparse import OptionParser


def printenv(opts, var_names: list[str]):
    endchar = "\0" if opts.null else "\n"

    if not var_names:
        for name, value in os.environ.items():
            print(f"{name}={value}", end=endchar)
        return

    failed = False
    for name in var_names:
        if value := os.environ.get(name):
            print(f"{name}={value}", end=endchar)
        else:
            failed = True

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [OPTION] [VARIABLE]...",
        description="Print VARIABLE(s) or all environment variables, and their corresponding values.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.add_option("-0", "--null", action="store_true")

    printenv(*parser.parse_args())
