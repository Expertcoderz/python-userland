import grp
import pwd

from optparse import OptionParser


def parse_onwer_spec(
    parser: OptionParser, owner_spec: str
) -> tuple[int | None, int | None]:
    """
    Process a string in the form ``[USER][:GROUP]`` and return the UID and GID.
    Either or both may be None if omitted from the input string.
    An appropriate parser error is thrown if obtaining the UID or GID fails.
    """
    tokens = owner_spec.split(":")

    uid: int | None = None
    gid: int | None = None

    if tokens[0]:
        if tokens[0].isdecimal():
            uid = int(tokens[0])
        else:
            try:
                uid = pwd.getpwnam(tokens[0])
            except KeyError:
                parser.error(f"invalid user: '{tokens}'")

    if len(tokens) > 1 and tokens[1]:
        if tokens[1].isdecimal():
            gid = int(tokens[1])
        else:
            try:
                gid = grp.getgrnam(tokens[1])
            except KeyError:
                parser.error(f"invalid group: '{tokens}'")

    return uid, gid
