import os

from .. import core


parser = core.ExtendedOptionParser(
    usage="%prog",
    description="Print the current username. Same as `id -un`.",
)


@core.command(parser)
def python_userland_whoami(_, args) -> int:
    parser.expect_nargs(args, 0)

    print(os.getlogin())

    return 0
