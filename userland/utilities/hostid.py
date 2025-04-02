from .. import core


parser = core.create_parser(
    usage=("%prog",),
    description="Print a 32-bit numeric host machine identifier.",
    epilog="This implementation gives an all-zero identifier.",
)


@core.command(parser)
def python_userland_hostid(_, args):
    if args:
        parser.error(f"extra operand '{args[0]}'")

    # We're not the only ones being lazy here... musl libc's gethostid(3)
    # returns zero as well. hostid can arguably be considered as obsolete.
    print("00000000")

    return 0
