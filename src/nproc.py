#!/usr/bin/python3

import os
from optparse import OptionParser


def nproc(opts):
    n_cpus = os.cpu_count() if opts.all else os.process_cpu_count()

    print(max(n_cpus - opts.ignore, 1))


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [OPTION]...",
        description="Print the number of processing units available to the process.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.add_option(
        "--all",
        action="store_true",
        help="print the total number of installed processors",
    )

    parser.add_option(
        "--ignore",
        type="int",
        default=0,
        metavar="N",
        help="exclude up to N processors if possible",
    )

    opts, args = parser.parse_args()

    if args:
        parser.error(f"extra operand '{args[0]}'")

    nproc(opts)
