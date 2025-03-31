#!/usr/bin/python3

import grp
import pwd
import os
import sys
from optparse import OptionParser


def groups(_, usernames: list[str]):
    failed = False

    for user in usernames or [os.getlogin()]:
        try:
            user_info = pwd.getpwnam(user)
        except KeyError as e:
            failed = True
            print(e, file=sys.stderr)
            continue

        print(
            (user + " : " if usernames else "")
            + " ".join(
                [
                    grp.getgrgid(id).gr_name
                    for id in os.getgrouplist(user, user_info.pw_gid)
                ]
            ),
        )

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [USERNAME]...",
        description="Print a list of groups for each USERNAME or the current user.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    groups(*parser.parse_args())
