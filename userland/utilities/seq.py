import math
from decimal import Decimal, InvalidOperation

from .. import core


parser = core.ExtendedOptionParser(
    usage=(
        "%prog [OPTION]... LAST",
        "%prog [OPTION]... FIRST LAST",
        "%prog [OPTION]... FIRST INCREMENT LAST",
    ),
    description="Print numbers from FIRST to LAST, stepping by INCREMENT.",
)

parser.add_option(
    "-f",
    "--format",
    metavar="FORMAT",
    help="format numbers with printf-style FORMAT",
)
parser.add_option(
    "-s",
    "--separator",
    default="\n",
    metavar="STRING",
    help="delimit outputs with STRING instead of newline",
)
parser.add_option(
    "-w",
    "--equal-width",
    action="store_true",
    help="pad with leading zeros to ensure equal width",
)


@core.command(parser)
def python_userland_seq(opts, args):
    parser.expect_nargs(args, (1, 3))

    if opts.format and opts.equal_width:
        parser.error("--format and --equal-width are mutually exclusive")

    def arg_to_decimal(arg: str) -> Decimal:
        try:
            return Decimal(arg)
        except InvalidOperation:
            parser.error(f"invalid decimal argument: {arg}")

    if len(args) == 1:
        first = Decimal(1)
        increment = Decimal(1)
        last = arg_to_decimal(args[0])
        exponent = 0
    elif len(args) == 2:
        first = arg_to_decimal(args[0])
        exponent = first.as_tuple().exponent
        increment = Decimal(1)
        last = arg_to_decimal(args[1]).quantize(first)
    else:
        first = arg_to_decimal(args[0])
        increment = arg_to_decimal(args[1])
        exponent = min(first.as_tuple().exponent, increment.as_tuple().exponent)
        last = arg_to_decimal(args[2]).quantize(
            first
            if first.as_tuple().exponent < increment.as_tuple().exponent
            else increment
        )

    formatstr: str

    if opts.equal_width:
        padding = math.floor(math.log10(last))
        padding += -exponent + 2 if exponent else 1
        if first < 0 or last < 0:
            padding += 1

        formatstr = f"%0{padding}.{-exponent}f" if exponent else f"%0{padding}g"
    elif opts.format:
        formatstr = opts.format
    else:
        formatstr = f"%.{-exponent}f" if exponent else "%g"

    scale = 10**-exponent

    print(formatstr % first, end="")
    for i in range(
        int((first + increment) * scale), int(last * scale) + 1, int(increment * scale)
    ):
        print(opts.separator + formatstr % (i / scale), end="")
    print()

    return 0
