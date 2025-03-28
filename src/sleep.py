#!/usr/bin/python3

import sys
import time
from decimal import Decimal
from optparse import OptionParser

SUFFIXES = {"s": 1, "m": 60, "h": 60 * 60, "d": 24 * 60 * 60}


def sleep(total_secs: Decimal):
    try:
        time.sleep(float(total_secs))
    except KeyboardInterrupt:
        print()
        sys.exit(130)


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog DURATION[SUFFIX]...",
        description=(
            "Delay for the sum of each DURATION."
            f" SUFFIX may be one of the following: {", ".join(SUFFIXES.keys())}."
        ),
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    _, args = parser.parse_args()

    total_secs = Decimal()

    for spec in args:
        if spec[-1].isdecimal():
            total_secs += Decimal(spec)
        else:
            if not (multiplier := SUFFIXES.get(spec[-1])):
                parser.error(f"invalid duration: {spec}")
            total_secs += Decimal(spec[:-1]) * multiplier

    sleep(total_secs)
