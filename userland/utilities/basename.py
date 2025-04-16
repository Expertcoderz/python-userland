from pathlib import PurePath

from .. import core


parser = core.ExtendedOptionParser(
    usage=("%prog NAME [SUFFIX]", "%prog OPTION... NAME..."),
    description="Print the last component of each path NAME.",
)
parser.add_option(
    "-a", "--multiple", action="store_true", help="support multiple NAMES"
)
parser.add_option(
    "-s",
    "--suffix",
    metavar="SUFFIX",
    help="remove trailing SUFFIX; implies -a",
)

parser.add_option(
    "-z",
    "--zero",
    action="store_true",
    help="terminate outputs with NUL instead of newline",
)


@core.command(parser)
def python_userland_basename(opts, args: list[str]) -> int:
    parser.expect_nargs(args, (1,))

    if opts.suffix:
        opts.multiple = True
    elif not opts.multiple and len(args) > 1:
        parser.expect_nargs(args, 2)

        opts.suffix = args.pop()
    else:
        opts.suffix = ""

    for path in map(PurePath, args):
        print(
            path.name.removesuffix(opts.suffix),
            end="\0" if opts.zero else "\n",
        )

    return 0
