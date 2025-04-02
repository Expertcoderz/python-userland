import os

from .. import core


parser = core.create_parser(
    usage=(" %prog [OPTION]...",),
    description="Print the number of processing units available to the process.",
)

parser.add_option(
    "--all",
    action="store_true",
    help="print the total number of installed processors",
)

parser.add_option(
    "--ignore",
    type="int",
    default=0,
    metavar="N",
    help="exclude up to N processors if possible",
)


@core.command(parser)
def python_userland_nproc(opts, args):
    if args:
        parser.error(f"extra operand '{args[0]}'")

    n_cpus = os.cpu_count() if opts.all else os.process_cpu_count()

    print(max(n_cpus - opts.ignore, 1))

    return 0
