#!/usr/bin/python3

import os
from optparse import OptionParser


def pwd(opts):
    resolved_pwd = os.getcwd()

    print(
        resolved_pwd
        if opts.resolve
        or not (
            # Only use PWD's contents if it accurately
            # points to the current working directory
            # and the -L flag is also given.
            (pwd_from_env := os.environ.get("PWD"))
            and os.path.samefile(pwd_from_env, resolved_pwd)
        )
        else pwd_from_env
    )


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [OPTION]",
        description="Print the path to the current working directory.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.add_option(
        "-L",
        "--logical",
        dest="resolve",
        action="store_false",
        help="don't resolve symlinks",
    )
    parser.add_option(
        "-P",
        "--physical",
        dest="resolve",
        action="store_true",
        default=True,
        help="resolve all encountered symlinks",
    )

    opts, args = parser.parse_args()

    if args:
        parser.error("too many arguments")

    pwd(opts)
