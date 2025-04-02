import os

from .. import core


parser = core.create_parser(
    usage=("%prog [OPTION]",),
    description="Print the path to the current working directory.",
)

parser.add_option(
    "-L",
    "--logical",
    dest="resolve",
    action="store_false",
    help="don't resolve symlinks",
)
parser.add_option(
    "-P",
    "--physical",
    dest="resolve",
    action="store_true",
    default=True,
    help="resolve all encountered symlinks",
)


@core.command(parser)
def python_userland_pwd(opts, args):
    if args:
        parser.error("too many arguments")

    resolved_pwd = os.getcwd()

    print(
        resolved_pwd
        if opts.resolve
        or not (
            # Only use PWD's contents if it accurately
            # points to the current working directory
            # and the -L flag is also given.
            (pwd_from_env := os.environ.get("PWD"))
            and os.path.samefile(pwd_from_env, resolved_pwd)
        )
        else pwd_from_env
    )

    return 0
