from pathlib import Path
from typing import Callable, Literal

from .. import core


def readlink_function(
    can_mode: Literal["f", "e", "m"] | None,
) -> Callable[[Path], Path]:
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


parser = core.ExtendedOptionParser(
    usage="%prog [OPTION]... FILE...",
    description="Print the target of each symbolic link FILE.",
)

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


@core.command(parser)
def python_userland_readlink(opts, args: list[str]) -> int:
    parser.expect_nargs(args, (1,))

    if opts.no_newline and len(args) > 1:
        core.perror("ignoring --no-newline with multiple arguments")
        opts.no_newline = False

    # This is the precise behavior of GNU readlink regardless
    # of in what order the -n and -z flags are specified.
    endchar = "" if opts.no_newline else "\0" if opts.zero else "\n"

    func = readlink_function(opts.can_mode)
    failed = False

    for path in map(Path, args):
        try:
            print(func(path), end=endchar)
        except OSError as e:
            failed = True

            if opts.verbose:
                core.perror(e)

    return int(failed)
