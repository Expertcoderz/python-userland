import grp
import pwd
import os
import sys

from .. import core


parser = core.create_parser(
    usage=("%prog [OPTION]... [USER]...",),
    description="Print user and group information for each USER or the current user.",
)

parser.add_option(
    "-u", "--user", action="store_true", help="print only the effective user ID"
)
parser.add_option(
    "-g", "--group", action="store_true", help="print only the effective group ID"
)
parser.add_option("-G", "--groups", action="store_true", help="print all group IDs")

parser.add_option(
    "-n",
    "--name",
    action="store_true",
    help="print names instead of numbers (for -ugG)",
)
parser.add_option(
    "-r",
    "--real",
    action="store_true",
    help="print the real ID instead of the effective ID (for -ugG)",
)
parser.add_option(
    "-z",
    "--zero",
    action="store_true",
    help="delimit entries with NUL instead of whitespace (for -ugG)",
)

parser.add_option(
    "-a", action="store_true", help="(ignored; present for compatibility)"
)
parser.add_option("-Z", "--context", action="store_true", help="(unimplemented)")


@core.command(parser)
def python_userland_id(opts, args):
    if opts.context:
        parser.error("--context (-Z) is not supported")

    if (ugG := (opts.user, opts.group, opts.groups)).count(True) > 1:
        parser.error("cannot print more than one of -ugG")

    if opts.name or opts.real and not any(ugG):
        parser.error("cannot print only names or real IDs in default format")

    if opts.zero and not any(ugG):
        parser.error("option --zero not permitted in default format")

    process_uid = os.getuid() if opts.real else os.geteuid()
    process_gid = os.getgid() if opts.real else os.getegid()

    failed = False

    for user in args or [str(process_uid)]:
        try:
            passwd = pwd.getpwnam(user)
        except KeyError as e:
            try:
                passwd = pwd.getpwuid(int(user))
            except (KeyError, ValueError):
                failed = True
                print(e, file=sys.stderr)
                continue

        if opts.user:
            print(
                passwd.pw_name if opts.name else passwd.pw_uid,
                end="\0" if opts.zero else "\n",
            )
            continue

        gid = process_gid if passwd.pw_uid == process_uid else passwd.pw_gid

        if opts.group:
            print(
                grp.getgrgid(gid) if opts.name else gid,
                end="\0" if opts.zero else "\n",
            )
            continue

        if opts.groups:
            print(
                ("\0" if opts.zero else "\n").join(
                    map(str, os.getgrouplist(passwd.pw_name, gid))
                ),
                end="\0" if opts.zero else "\n",
            )
            continue

        print(
            f"uid={passwd.pw_uid}({passwd.pw_name})"
            + f" gid={passwd.pw_gid}({grp.getgrgid(passwd.pw_gid).gr_name})"
            + " groups="
            + ",".join(
                [
                    f"{id}({grp.getgrgid(id).gr_name})"
                    for id in os.getgrouplist(passwd.pw_name, passwd.pw_gid)
                ]
            ),
        )

    return int(failed)
