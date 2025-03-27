#!/usr/bin/python3

import sys
from optparse import OptionParser


def nologin():
    print("This account is currently not available.")
    sys.exit(1)


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [IGNORED]...",
        description="Politely refuse a login.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.parse_args()

    nologin()
