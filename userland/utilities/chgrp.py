import shutil
import sys
from pathlib import Path

from tqdm import tqdm

from .. import core


parser = core.ExtendedOptionParser(
    usage=(
        "%prog [OPTION]... GROUP FILE...",
        "%prog [OPTION]... --reference=RFILE FILE...",
    ),
    description="Change the group ownership of each FILE.",
)

parser.add_option(
    "-f",
    "--silent",
    "--quiet",
    dest="verbosity",
    action="store_const",
    const=0,
    default=1,
    help="suppress most error messages",
)
parser.add_option(
    "-c",
    "--changes",
    dest="verbosity",
    action="store_const",
    const=2,
    help="report only when changes are made",
)
parser.add_option(
    "-v",
    "--verbose",
    dest="verbosity",
    action="store_const",
    const=3,
    help="print a diagnostic for each file",
)

parser.add_option(
    "--progress",
    dest="progress",
    action="store_true",
    help="show a progress bar when changing groups",
)
parser.add_option(
    "--no-progress",
    dest="progress",
    action="store_false",
    default=False,
    help="do not show a progress bar (default)",
)

parser.add_option(
    "--dereference",
    action="store_true",
    default=True,
    help="affect symlink referents instead of the symlinks themselves (default)",
)
parser.add_option(
    "-h",
    "--no-dereference",
    dest="dereference",
    action="store_false",
    help="opposite of --dereference",
)

parser.add_option(
    "--no-preserve-root",
    dest="preserve_root",
    action="store_false",
    default=False,
    help="do not treat '/' specially (default)",
)
parser.add_option(
    "--preserve-root",
    action="store_true",
    help="fail to operate recursively on '/'",
)

parser.add_option(
    "--from",
    dest="from_spec",  # prevent name collision with the `from` keyword
    metavar="[CURRENT_OWNER][:[CURRENT_GROUP]]",
    help="only affect files with CURRENT_OWNER and CURRENT_GROUP"
    " (either is optional and only checked if given)",
)

parser.add_option(
    "--reference",
    metavar="RFILE",
    help="use the group of RFILE instead of from an argument",
)

parser.add_option(
    "-R", "--recursive", action="store_true", help="operate on directories recursively"
)
parser.add_option(
    "-H",
    dest="recurse_mode",
    action="store_const",
    const="H",
    help="traverse directory symlinks only if they were given as command line arguments",
)
parser.add_option(
    "-L",
    dest="recurse_mode",
    action="store_const",
    const="L",
    help="traverse all directory symlinks encountered",
)
parser.add_option(
    "-P",
    dest="recurse_mode",
    action="store_const",
    const="P",
    default="P",
    help="do not traverse any symlinks (default)",
)


def get_new_group(opts, args: list[str]) -> tuple[int, str]:
    if opts.reference:
        gid = Path(opts.reference).stat(follow_symlinks=True).st_gid

        return gid, core.group_display_name_from_id(gid)

    parser.expect_nargs(args, (2,))
    gname = args.pop(0)

    return parser.parse_group(gname), gname


@core.command(parser)
def python_userland_chgrp(opts, args: list[str]) -> int:
    parser.expect_nargs(args, (1,))

    from_uid: int | None = None
    from_gid: int | None = None

    if opts.from_spec:
        from_uid, from_gid = parser.parse_owner_spec(opts.from_spec)

    try:
        gid, gname = get_new_group(opts, args)
    except OSError as e:
        core.perror(e)
        return 1

    failed = False

    def handle_error(err: Exception, level: int, msg: str) -> None:
        nonlocal failed
        failed = True

        if opts.verbosity:
            core.perror(err)
            if opts.verbosity > level:
                print(msg, file=sys.stderr)

    for file in core.traverse_files(
        (
            tqdm(args, ascii=True, desc="Changing group ownership")
            if opts.progress
            else args
        ),
        recurse_mode=opts.recurse_mode if opts.recursive else None,
        preserve_root=opts.preserve_root,
    ):
        if not file:
            failed = True
            continue

        try:
            stat = file.stat(follow_symlinks=opts.dereference)
            prev_uid = stat.st_uid
            prev_gid = stat.st_gid
        except OSError as e:
            handle_error(e, 2, f"failed to change group of '{file}' to {gname or gid}")
            continue

        prev_gname = core.group_display_name_from_id(prev_gid)

        # Note: while it's possible, we do not check if prev_gid == gid at
        # this point because even if they are the same, an error should be
        # printed if the current user has insufficient permission to change
        # the group membership of that file (for coreutils compat).
        if (from_uid is not None and prev_uid != from_uid) or (
            from_gid is not None and prev_gid != from_gid
        ):
            if opts.verbosity > 2:
                print(f"group of '{file}' retained as {prev_gname}")
            continue

        try:
            shutil.chown(file, group=gid, follow_symlinks=opts.dereference)
        except OSError as e:
            handle_error(e, 2, f"failed to change group of '{file}' to {gname or gid}")
            continue

        if prev_gid == gid:
            if opts.verbosity > 2:
                print(f"group of '{file}' retained as {prev_gname}")
        elif opts.verbosity > 1:
            print(f"changed group of '{file}' from {prev_gname} to {gname or gid}")

    return int(failed)
