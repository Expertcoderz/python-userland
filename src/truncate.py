#!/usr/bin/python3

import sys
from optparse import OptionParser
from pathlib import Path
from typing import Callable


def truncate(opts, files: list[Path], size_prefix: str | None, size_num: int | None):
    get_new_size: Callable[[int], int] = (
        {
            "+": lambda old_size: old_size + size_num,
            "-": lambda old_size: old_size - size_num,
            "<": lambda old_size: min(old_size, size_num),
            ">": lambda old_size: max(old_size, size_num),
            "/": lambda old_size: size_num * (old_size // size_num),
            "%": lambda old_size: size_num * -(old_size // -size_num),
        }[size_prefix]
        if size_prefix
        else (
            (lambda _: size_num)
            if size_num is not None
            else (lambda old_size: old_size)
        )
    )

    size_attr = "st_blocks" if opts.io_blocks else "st_size"

    try:
        reference_size = (
            getattr(opts.reference.stat(follow_symlinks=True), size_attr)
            if opts.reference
            else None
        )
    except OSError as e:
        print(e)
        sys.exit(1)

    for file in files:
        if not file.exists() and opts.no_create:
            continue

        stat = file.stat(follow_symlinks=True)

        old_size = getattr(stat, size_attr)
        new_size = get_new_size(reference_size or old_size)

        if new_size == old_size:
            continue

        try:
            with file.open("rb+") as io:
                io.truncate(
                    new_size * stat.st_blksize if opts.io_blocks else new_size,
                )
        except OSError as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [OPTION]... -s SIZE FILE..."
        + "\n       %prog [OPTION]... -r RFILE FILE...",
        description="Shrink or extend each FILE to SIZE.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.add_option(
        "-c", "--no-create", action="store_true", help="do not create files"
    )
    parser.add_option("-s", "--size", help="set or adjust file size by SIZE bytes")
    parser.add_option(
        "-o",
        "--io-blocks",
        action="store_true",
        help="interpret SIZE as number of IO blocks",
    )

    parser.add_option("-r", "--reference", metavar="RFILE", help="base size on RFILE")

    opts, args = parser.parse_args()

    if opts.reference:
        opts.reference = Path(opts.reference)

    size_prefix: int | None = None
    size_num: int | None = None

    if opts.size:
        if opts.size[0] in frozenset("+-<>/%"):
            size_prefix = opts.size[0]

        try:
            size_num = int(opts.size[1:] if size_prefix else opts.size)
        except ValueError:
            parser.error(f"invalid number: '{opts.size}'")

        if opts.reference and not size_prefix:
            parser.error("you must specify a relative '--size' with '--reference'")
    elif not opts.reference:
        parser.error("you must specify either '--size' or '--reference'")

    if not args:
        parser.error("missing file operand")

    truncate(opts, map(Path, args), size_prefix, size_num)
