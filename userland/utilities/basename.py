from pathlib import PurePath

from .. import core


parser = core.create_parser(
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
def python_userland_basename(opts, args):
    if not args:
        parser.error("missing operand")

    if opts.suffix:
        opts.multiple = True
    elif not opts.multiple and len(args) > 1:
        if len(args) > 2:
            parser.error(f"extra operand '{args[2]}'")

        opts.suffix = args.pop()
    else:
        opts.suffix = ""

    for path in map(PurePath, args):
        print(
            path.name.removesuffix(opts.suffix),
            end="\0" if opts.zero else "\n",
        )

    return 0
