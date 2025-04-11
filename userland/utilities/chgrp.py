import grp
import pwd
import shutil
import sys
from pathlib import Path

from tqdm import tqdm

from .. import core


parser = core.create_parser(
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
    metavar="[CURRENT_OWNER][:CURRENT_GROUP]",
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


@core.command(parser)
def python_userland_chgrp(opts, args):
    if not args:
        parser.error("missing operand")

    from_uid: int | None = None
    from_gid: int | None = None

    if opts.from_spec:
        from_spec = opts.from_spec.split(":")

        if from_spec[0]:
            try:
                from_uid = pwd.getpwnam(from_spec[0])
            except KeyError:
                parser.error(f"invalid user: '{opts.from_spec}'")

        if len(from_spec) > 1 and from_spec[1]:
            try:
                from_gid = grp.getgrnam(from_spec[1])
            except KeyError:
                parser.error(f"invalid group: '{opts.from_spec}'")

    gid: int
    gname: str | None = None

    if opts.reference:
        try:
            gid = Path(opts.reference).stat(follow_symlinks=True).st_gid
        except OSError as e:
            print(e, file=sys.stderr)
            return 1
    else:
        gname = args.pop(0)

        if not args:
            parser.error(f"missing operand after '{gname}'")

        if gname.isdecimal():
            gid = int(gname)
        else:
            try:
                gid = grp.getgrnam(gname).gr_gid
            except KeyError:
                parser.error(f"invalid group: '{gname}'")

    failed = False

    def chown(file: Path) -> None:
        nonlocal failed

        try:
            stat = file.stat(follow_symlinks=opts.dereference)
            prev_uid = stat.st_uid
            prev_gid = stat.st_gid
        except OSError as e:
            failed = True
            if opts.verbosity:
                print(e, file=sys.stderr)
                print(
                    f"failed to change group of '{file}' to {gname or gid}",
                    file=sys.stderr,
                )
            return

        try:
            prev_gname = grp.getgrgid(prev_gid).gr_name
        except KeyError:
            prev_gname = str(prev_gid)

        # Note: while it's possible, we do not check if prev_gid == gid at
        # this point because even if they are the same, an error should be
        # printed if the current user has insufficient permission to change
        # the group membership of that file (for coreutils compat).
        if (from_uid is not None and prev_uid == from_uid) or (
            from_gid is not None and prev_gid == from_gid
        ):
            if opts.verbosity > 2:
                print(f"group of '{file}' retained as {prev_gname}")
            return

        try:
            shutil.chown(file, group=gid, follow_symlinks=opts.dereference)
        except OSError as e:
            failed = True
            if opts.verbosity:
                print(e, file=sys.stderr)
                if opts.verbosity:
                    print(
                        f"failed to change group of '{file}' to {gname or gid}",
                        file=sys.stderr,
                    )
            return

        if prev_gid == gid:
            if opts.verbosity > 2:
                print(f"group of '{file}' retained as {prev_gname}")
        elif opts.verbosity > 1:
            print(f"changed group of '{file}' from {prev_gname} to {gname or gid}")

    files = map(
        Path,
        (
            tqdm(args, ascii=True, desc="Changing group ownership")
            if opts.progress
            else args
        ),
    )

    if opts.recursive:

        def traverse(file: Path) -> None:
            nonlocal failed

            if opts.preserve_root and file.root == str(file):
                print(
                    f"recursive operation on '{file}' prevented; use --no-preserve-root to override",
                    file=sys.stderr,
                )
                failed = True
                return

            for child in file.iterdir():
                if child.is_dir(follow_symlinks=opts.recurse_mode == "L"):
                    traverse(child)
                chown(file)

        for file in files:
            if file.is_dir(
                follow_symlinks=opts.recurse_mode == "H" or opts.recurse_mode == "L"
            ):
                traverse(file)
            else:
                chown(file)
    else:
        for file in files:
            chown(file)

    return int(failed)
