from .. import core


parser = core.create_parser(
    usage=("%prog",),
    description="Politely refuse a login.",
)


@core.command(parser)
def python_userland_nologin(*_):
    print("This account is currently not available.")
    return 1
