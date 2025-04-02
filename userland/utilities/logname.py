import os

from .. import core


parser = core.create_parser(
    usage=("%prog",),
    description="Print the current user's login name.",
)


@core.command(parser)
def python_userland_logname(_, args):
    if args:
        parser.error(f"extra operand '{args[0]}'")

    print(os.getlogin())

    return 0
