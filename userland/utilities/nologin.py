from .. import core


parser = core.ExtendedOptionParser(
    usage="%prog",
    description="Politely refuse a login.",
)


@core.command(parser)
def python_userland_nologin(*_) -> int:
    print("This account is currently not available.")
    return 1
