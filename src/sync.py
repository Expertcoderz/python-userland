#!/usr/bin/python3

import os
import sys
from optparse import OptionParser


def sync(_, filenames: list[str]):
    if filenames:
        failed = False

        for name in filenames:
            try:
                with open(name, "rb+") as io:
                    os.fsync(io)
            except OSError as e:
                failed = True
                print(e, file=sys.stderr)

        if failed:
            sys.exit(1)
    else:
        os.sync()


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [FILE]...",
        description="Sync the filesystem or write each FILE's blocks to disk.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    sync(*parser.parse_args())
