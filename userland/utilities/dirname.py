from pathlib import PurePath

from .. import core


parser = core.ExtendedOptionParser(
    usage="%prog [OPTION]... NAME...",
    description=(
        "Print each path NAME with the last component removed,"
        " or '.' if NAME is the only component."
    ),
)

parser.add_option(
    "-z",
    "--zero",
    action="store_true",
    help="terminate outputs with NUL instead of newline",
)


@core.command(parser)
def python_userland_dirname(opts, args: list[str]) -> int:
    parser.expect_nargs(args, (1,))

    for path in map(PurePath, args):
        print(path.parent, end="\0" if opts.zero else "\n")

    return 0
