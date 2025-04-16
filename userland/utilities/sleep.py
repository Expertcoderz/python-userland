import time
from decimal import Decimal

from .. import core


SUFFIXES = {"s": 1, "m": 60, "h": 60 * 60, "d": 24 * 60 * 60}


parser = core.ExtendedOptionParser(
    usage="%prog DURATION[SUFFIX]...",
    description=(
        "Delay for the sum of each DURATION."
        f" SUFFIX may be one of the following: {", ".join(SUFFIXES.keys())}."
    ),
)


@core.command(parser)
def python_userland_sleep(_, args) -> int:
    total_secs = Decimal()

    for spec in args:
        if spec[-1].isdecimal():
            total_secs += Decimal(spec)
        else:
            if not (multiplier := SUFFIXES.get(spec[-1])):
                parser.error(f"invalid duration: {spec}")
            total_secs += Decimal(spec[:-1]) * multiplier

    time.sleep(float(total_secs))

    return 0
