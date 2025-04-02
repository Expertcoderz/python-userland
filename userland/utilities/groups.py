import grp
import pwd
import os
import sys

from .. import core


parser = core.create_parser(
    usage=("%prog [USERNAME]...",),
    description="Print a list of groups for each USERNAME or the current user.",
)


@core.command(parser)
def python_userland_groups(_, args):
    failed = False

    for user in args or [os.getlogin()]:
        try:
            user_info = pwd.getpwnam(user)
        except KeyError as e:
            failed = True
            print(e, file=sys.stderr)
            continue

        print(
            (user + " : " if args else "")
            + " ".join(
                [
                    grp.getgrgid(id).gr_name
                    for id in os.getgrouplist(user, user_info.pw_gid)
                ]
            ),
        )

    return int(failed)
