#!/usr/bin/python3

from .. import lib

parser = lib.create_parser(
    usage=("%prog",),
    description="Politely refuse a login.",
)


@lib.command(parser)
def python_userland_nologin(*_):
    print("This account is currently not available.")
    return 1
