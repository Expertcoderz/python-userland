import os
import sys

from .. import core


# Note: os.path is used instead of pathlib because certain functionality such as
# os.path.normpath() lack a pathlib equivalent.


def resolve_filename(opts, name: str) -> str:
    if opts.symlink_mode:
        if opts.symlink_mode == "L":
            # resolve instances of ".." first
            name = os.path.normpath(name)

        name = os.path.realpath(name, strict=opts.can_mode == "e")

        if not opts.can_mode:
            # raise an error if directory missing
            os.path.realpath(os.path.dirname(name), strict=True)
    else:
        if opts.can_mode == "e":
            # raise an error if missing
            os.path.realpath(name, strict=True)

        name = os.path.abspath(name)

    return name


parser = core.create_parser(
    usage=("%prog [OPTION]... FILE...",),
    description="Print the resolved path of each FILE.",
)

parser.add_option("-q", "--quiet", action="store_true", help="suppress error messages")

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
    "-L",
    "--logical",
    dest="symlink_mode",
    action="store_const",
    const="L",
    help="resolve '..' components before symlinks",
)
parser.add_option(
    "-P",
    "--physical",
    dest="symlink_mode",
    action="store_const",
    const="P",
    default="P",
    help="resolve symlinks as encountered (default)",
)
parser.add_option(
    "-s",
    "--strip",
    "--no-symlinks",
    dest="symlink_mode",
    action="store_const",
    const="",
    help="do not resolve symlinks",
)

parser.add_option(
    "--relative-to", metavar="DIR", help="resolve the path relative to DIR"
)
parser.add_option(
    "--relative-base",
    default="",
    metavar="DIR",
    help="print absolute paths except those below DIR",
)

parser.add_option(
    "-z",
    "--zero",
    action="store_true",
    help="terminate outputs with NUL instead of newline",
)


@core.command(parser)
def python_userland_realpath(opts, args):
    if not args:
        parser.error("missing operand")

    endchar = "\0" if opts.zero else "\n"

    if opts.relative_to:
        args = (os.path.join(opts.relative_to, name) for name in args)

    failed = False

    for name in args:
        try:
            name = resolve_filename(opts, name)
        except OSError as e:
            failed = True

            if not opts.quiet:
                print(e, file=sys.stderr)
        else:
            if opts.relative_to and not opts.relative_base:
                name = os.path.relpath(name, opts.relative_to)
            elif opts.relative_base and not opts.relative_to:
                name = os.path.relpath(name, opts.relative_base)

            print(name, end=endchar)

    return int(failed)
