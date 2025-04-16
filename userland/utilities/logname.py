import os

from .. import core


parser = core.ExtendedOptionParser(
    usage="%prog",
    description="Print the current user's login name.",
)


@core.command(parser)
def python_userland_logname(_, args) -> int:
    parser.expect_nargs(args, 0)

    print(os.getlogin())

    return 0
