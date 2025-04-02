import os

from .. import core


parser = core.create_parser(
    usage=(" %prog [OPTION] [VARIABLE]...",),
    description="Print VARIABLE(s) or all environment variables, and their values.",
)

parser.add_option("-0", "--null", action="store_true")


@core.command(parser)
def python_userland_printenv(opts, var_names: list[str]):
    endchar = "\0" if opts.null else "\n"

    if not var_names:
        for name, value in os.environ.items():
            print(f"{name}={value}", end=endchar)
        return 0

    failed = False
    for name in var_names:
        if value := os.environ.get(name):
            print(f"{name}={value}", end=endchar)
        else:
            failed = True

    return int(failed)
