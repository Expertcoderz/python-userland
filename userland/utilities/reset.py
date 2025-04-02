import os
import sys

from .. import core


# reset(1), roughly modelled off the ncurses implementation.

parser = core.create_parser(
    usage=("%prog [OPTION]... [IGNORED]...",),
    description="Initialize or reset the terminal state.",
)

parser.add_option("-I", action="store_true", help="(unimplemented)")
parser.add_option("-c", action="store_true", help="(unimplemented)")
parser.add_option("-Q", action="store_true", help="(unimplemented)")

parser.add_option(
    "-q",
    action="store_true",
    help="print the terminal type; do not initialize the terminal",
)
parser.add_option(
    "-r", action="store_true", help="print the terminal type to standard error"
)
parser.add_option(
    "-s",
    action="store_true",
    help="print the sequence of shell commands to initialize the TERM environment variable",
)

parser.add_option("-w", action="store_true", help="(unimplemented)")

parser.add_option("-e", metavar="CHAR", help="(unimplemented)")
parser.add_option("-i", metavar="CHAR", help="(unimplemented)")
parser.add_option("-k", metavar="CHAR", help="(unimplemented)")

parser.add_option("-m", metavar="MAPPING", help="(unimplemented)")


@core.command(parser)
def python_userland_reset(opts, args):
    if args and args[0] == "-":
        opts.q = True
        del args[0]

    term = args[0] if args else os.environ.get("TERM")

    if opts.q:
        if not term:
            print("unknown terminal type ", file=sys.stderr)
            try:
                while True:
                    if term := input("Terminal type? "):
                        break
            except KeyboardInterrupt:
                print()
                return 130

        print(term)
        return 0

    print("\x1bc", end="")

    if opts.r:
        print(f"Terminal type is {term}.")

    if opts.s:
        print(f"TERM={term};")

    return 0
