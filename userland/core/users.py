import functools
import grp
import pwd

from optparse import OptionParser


class OptionParserUsersMixin(OptionParser):
    def parse_owner_spec(self, owner_spec: str) -> tuple[int | None, int | None]:
        """
        Accept a string in the form ``[USER][:[GROUP]]`` and return the UID and GID.
        Either or both may be None if omitted from the input string.
        An appropriate parser error is thrown if obtaining the UID or GID fails.
        """
        tokens = owner_spec.split(":")

        uid: int | None = None
        gid: int | None = None

        if tokens[0]:
            uid = self.parse_user(tokens[0])

        if len(tokens) > 1 and tokens[1]:
            gid = self.parse_group(tokens[1])

        return uid, gid

    # pylint: disable=inconsistent-return-statements
    def parse_user(self, user: str) -> int:
        """
        Accept a string representing a username or UID and return the UID.
        An appropriate parser error is thrown if obtaining the UID fails.
        """
        if user.isdecimal():
            return int(user)

        try:
            return pwd.getpwnam(user).pw_uid
        except KeyError:
            self.error(f"invalid user: {user}")

    # pylint: disable=inconsistent-return-statements
    def parse_group(self, group: str) -> int:
        """
        Accept a string representing a group name or GID and return the GID.
        An appropriate parser error is thrown if obtaining the GID fails.
        """
        if group.isdecimal():
            return int(group)

        try:
            return grp.getgrnam(group).gr_gid
        except KeyError:
            self.error(f"invalid group: {group}")


@functools.lru_cache(1000)
def user_display_name_from_id(uid: int) -> str:
    try:
        return pwd.getpwuid(uid).pw_name
    except KeyError:
        return str(uid)


@functools.lru_cache(1000)
def group_display_name_from_id(gid: int) -> str:
    try:
        return grp.getgrgid(gid).gr_name
    except KeyError:
        return str(gid)
