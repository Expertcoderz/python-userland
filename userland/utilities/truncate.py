import operator
from pathlib import Path
from typing import Callable

from tqdm import tqdm

from .. import core

PREFIXES: dict[str, Callable[[int, int], int]] = {
    "+": operator.add,
    "-": operator.sub,
    "<": min,
    ">": max,
    "/": lambda old_size, size_num: size_num * (old_size // size_num),
    "%": lambda old_size, size_num: size_num * -(old_size // -size_num),
}

parser = core.ExtendedOptionParser(
    usage=(
        "%prog [OPTION]... -s SIZE FILE...",
        "%prog [OPTION]... -r RFILE FILE...",
    ),
    description="Shrink or extend each FILE to SIZE.",
)

parser.add_option(
    "--progress",
    dest="progress",
    action="store_true",
    help="show a progress bar when truncating files",
)
parser.add_option(
    "--no-progress",
    dest="progress",
    action="store_false",
    default=False,
    help="do not show a progress bar (default)",
)

parser.add_option("-c", "--no-create", action="store_true", help="do not create files")
parser.add_option("-s", "--size", help="set or adjust file size by SIZE bytes")
parser.add_option(
    "-o",
    "--io-blocks",
    action="store_true",
    help="interpret SIZE as number of IO blocks",
)

parser.add_option("-r", "--reference", metavar="RFILE", help="base size on RFILE")


def parse_size_spec(spec: str) -> tuple[str | None, int]:
    prefix = spec[0] if spec[0] in frozenset("+-<>/%") else None
    return prefix, int(spec[1:] if prefix else spec)


def get_size_changer(prefix: str | None, num: int | None) -> Callable[[int], int]:
    if prefix:
        assert num is not None
        return lambda old_size: PREFIXES[prefix](old_size, num)

    return (lambda _: num) if num is not None else (lambda old_size: old_size)


@core.command(parser)
def python_userland_truncate(opts, args: list[str]) -> int:
    if opts.reference:
        opts.reference = Path(opts.reference)

    size_prefix: str | None = None
    size_num: int | None = None

    if opts.size:
        try:
            size_prefix, size_num = parse_size_spec(opts.size)
        except ValueError:
            parser.error(f"invalid number: '{opts.size}'")

        if opts.reference and not size_prefix:
            parser.error("you must specify a relative '--size' with '--reference'")
    elif not opts.reference:
        parser.error("you must specify either '--size' or '--reference'")

    if not args:
        parser.error("missing file operand")

    get_new_size = get_size_changer(size_prefix, size_num)

    size_attr = "st_blocks" if opts.io_blocks else "st_size"

    try:
        reference_size = (
            getattr(opts.reference.stat(follow_symlinks=True), size_attr)
            if opts.reference
            else None
        )
    except OSError as e:
        core.perror(e)
        return 1

    failed = False

    for file in map(
        Path, tqdm(args, ascii=True, desc="Truncating files") if opts.progress else args
    ):
        if not file.exists() and opts.no_create:
            continue

        stat = file.stat(follow_symlinks=True)

        old_size = getattr(stat, size_attr)
        new_size = get_new_size(reference_size or old_size)

        if new_size == old_size:
            continue

        try:
            with open(file, "rb+") as f:
                f.truncate(
                    new_size * stat.st_blksize if opts.io_blocks else new_size,
                )
        except OSError as e:
            failed = True
            core.perror(e)

    return int(failed)
