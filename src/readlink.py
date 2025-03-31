#!/usr/bin/python3

import sys
from optparse import OptionParser
from pathlib import Path
from typing import Callable


def readlink_function(can_mode: str | None) -> Callable[[Path], str]:
    match can_mode:
        case None:
            return lambda path: path.readlink()
        case "f":
            return (
                lambda path: path.parent.resolve(strict=True)
                .joinpath(path.name)
                .resolve(strict=False)
            )
        case "e" | "m":
            return lambda path: path.resolve(strict=can_mode == "e")


def readlink(opts, paths: list[Path]):
    # This is the precise behavior of GNU readlink regardless
    # of in what order the -n and -z flags are specified.
    endchar = "" if opts.no_newline else "\0" if opts.zero else "\n"

    func = readlink_function(opts.can_mode)
    failed = False

    for path in paths:
        try:
            print(func(path), end=endchar)
        except OSError as e:
            failed = True

            if opts.verbose:
                print(e, file=sys.stderr)

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [OPTION]... FILE...",
        description="Print the target of each symbolic link FILE.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.add_option(
        "-f",
        "--canonicalize",
        dest="can_mode",
        action="store_const",
        const="f",
        help="all but the last path component must exist",
    )
    parser.add_option(
        "-e",
        "--canonicalize-existing",
        dest="can_mode",
        action="store_const",
        const="e",
        help="all path components must exist",
    )
    parser.add_option(
        "-m",
        "--canonicalize-missing",
        dest="can_mode",
        action="store_const",
        const="m",
        help="no path components need exist or be a directory",
    )

    parser.add_option(
        "-n",
        "--no-newline",
        action="store_true",
        help="do not delimit outputs (overrides -z)",
    )
    parser.add_option(
        "-z",
        "--zero",
        action="store_true",
        help="terminate outputs with NUL instead of newline",
    )

    parser.add_option(
        "-q",
        "--quiet",
        "-s",
        "--silent",
        dest="verbose",
        action="store_false",
        default=False,
        help="suppress error messages (default)",
    )
    parser.add_option(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="report errors",
    )

    opts, args = parser.parse_args()

    if not args:
        parser.error("missing operand")

    if opts.no_newline and len(args) > 1:
        print("ignoring --no-newline with multiple arguments", file=sys.stderr)
        opts.no_newline = False

    readlink(opts, map(Path, args))
