import re

import shutil
import sys
from pathlib import Path

from tqdm import tqdm

from .. import core


CHOWN_PATTERN = re.compile("^([^:]+)?(:([^:]+))?$")

parser = core.ExtendedOptionParser(
    usage=(
        "%prog [OPTION]... [USER][:[GROUP]] FILE...",
        "%prog [OPTION]... --reference=RFILE FILE...",
    ),
    description="Change the user and/or group ownership of each FILE.",
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
    dest="preserve_root",
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

parser.add_option("--reference", metavar="RFILE")

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


def get_new_owner(opts, args: list[str], chown_args: dict) -> str | None:
    if opts.reference:
        try:
            ref_stat = Path(opts.reference).stat(follow_symlinks=True)
        except OSError as e:
            core.perror(e)
            return None

        chown_args["user"] = ref_stat.st_uid
        chown_args["group"] = ref_stat.st_gid

        return (
            core.user_display_name_from_id(ref_stat.st_uid)
            + ":"
            + core.group_display_name_from_id(ref_stat.st_gid)
        )

    parser.expect_nargs(args, (2,))
    owner_spec = args.pop(0)

    if not (owner_match := CHOWN_PATTERN.match(owner_spec)):
        parser.error(f"invalid owner spec: {owner_spec}")

    chown_args["user"] = (
        parser.parse_user(owner_match.group(1)) if owner_match.group(1) else None
    )
    chown_args["group"] = (
        parser.parse_group(owner_match.group(3)) if owner_match.group(3) else None
    )

    return owner_spec


@core.command(parser)
def python_userland_chown(opts, args: list[str]) -> int:
    parser.expect_nargs(args, (1,))

    from_uid: int | None = None
    from_gid: int | None = None

    if opts.from_spec:
        from_uid, from_gid = parser.parse_owner_spec(opts.from_spec)

    chown_args = {"follow_symlinks": opts.dereference}

    if not (owner_spec := get_new_owner(opts, args, chown_args)):
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
        (tqdm(args, ascii=True, desc="Changing ownership") if opts.progress else args),
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
            handle_error(
                e, 2, f"failed to change ownership of '{file}' to {owner_spec}"
            )
            continue

        prev_uname = core.user_display_name_from_id(prev_uid)
        prev_gname = core.group_display_name_from_id(prev_gid)

        if (from_uid is not None and prev_uid != from_uid) or (
            from_gid is not None and prev_gid != from_gid
        ):
            if opts.verbosity > 2:
                print(f"ownership of '{file}' retained as {prev_uname}:{prev_gname}")
            continue

        try:
            shutil.chown(file, **chown_args)
        except OSError as e:
            handle_error(
                e, 2, f"failed to change ownership of '{file}' to {owner_spec}"
            )
            continue

        if prev_uid == chown_args["user"] or prev_gid == chown_args["group"]:
            if opts.verbosity > 2:
                print(f"ownership of '{file}' retained as {prev_uname}:{prev_gname}")
        elif opts.verbosity > 1:
            print(
                f"changed ownership of '{file}' from"
                f" {prev_uname}:{prev_gname} to {owner_spec}"
            )

    return int(failed)
