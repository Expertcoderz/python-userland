from .. import core


parser = core.ExtendedOptionParser(
    "%prog [STRING]...",
    description="Repeatedly output a line with STRING(s) (or 'y' by default).",
)


@core.command(parser)
def python_userland_yes(_, args) -> int:
    try:
        string = " ".join(args or ["y"])
        while True:
            print(string)
    except KeyboardInterrupt:
        # Do not emit a trailing newline on keyboard interrupt.
        return 130
