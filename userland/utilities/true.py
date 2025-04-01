import os
import sys

from .. import core


@core.command()
def python_userland_true(_, args):
    if args and args[0] == "--help":
        print(
            f"""\
Usage: {os.path.basename(sys.argv[0])} [IGNORED]...

Return an exit status of 0.

Options:
  --help  show usage information and exit"""
        )
