from pathlib import PurePath

from .. import core


parser = core.create_parser(
    usage=("%prog [OPTION]... NAME...",),
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
def python_userland_dirname(opts, args):
    if not args:
        parser.error("missing operand")

    for path in map(PurePath, args):
        print(path.parent, end="\0" if opts.zero else "\n")

    return 0
