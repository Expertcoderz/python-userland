from .. import core


parser = core.create_parser(
    ("%prog [STRING]...",),
    description="Repeatedly output a line with STRING(s) (or 'y' by default).",
)


@core.command(parser)
def python_userland_yes(_, args):
    try:
        string = " ".join(args or ["y"])
        while True:
            print(string)
    except KeyboardInterrupt:
        return 130
