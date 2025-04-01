#!/usr/bin/python3

import os
import sys

from .. import lib

parser = lib.create_parser(
    usage=("%prog [FILE]...",),
    description="Sync the filesystem or write each FILE's blocks to disk.",
)

@lib.command(parser)
def python_userland_sync(_, args):
    if args:
        failed = False

        for name in args:
            try:
                with open(name, "rb+") as io:
                    os.fsync(io)
            except OSError as e:
                failed = True
                print(e, file=sys.stderr)

        return int(failed)

    os.sync()
    return 0
