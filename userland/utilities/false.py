import os
import sys

from .. import core


@core.command()
def python_userland_false(_, args):
    if args and args[0] == "--help":
        print(
            f"""\
Usage: {os.path.basename(sys.argv[0])} [IGNORED]...

Return an exit status of 1.

Options:
  --help  show usage information and exit"""
        )

    # Exit with status 1, even if --help was passed.
    # (coreutils/POSIX compat)
    return 1
