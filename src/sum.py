#!/usr/bin/python3

import sys
from optparse import OptionParser


# BSD 16-bit checksum
def sum_bsd(data: bytes) -> str:
    checksum = 0
    for b in data:
        checksum = (checksum >> 1) + ((checksum & 1) << 15)
        checksum += b
        checksum &= 0xFFFF

    return f"{checksum:05}{-(len(data) // -1024):>6}"


# SYSV checksum
def sum_sysv(data: bytes) -> int:
    s = sum(data)
    r = s % 2**16 + (s % 2**32) // 2**16
    checksum = (r % 2**16) + r // 2**16

    return f"{checksum:03} {-(len(data) // -512)}"


SUM_ALGORITHMS = {"bsd": sum_bsd, "sysv": sum_sysv}


def _sum(opts, filenames: list[str]):
    for name in filenames:
        if name == "-":
            print(SUM_ALGORITHMS[opts.algorithm](sys.stdin.buffer.read()))
        else:
            with open(name, "rb") as io:
                print(f"{SUM_ALGORITHMS[opts.algorithm](io.read())} {name}")


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog [OPTION] [FILE]...", add_help_option=False
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    parser.add_option(
        "-r",
        dest="algorithm",
        action="store_const",
        const="bsd",
        default="bsd",
        help="use the BSD (16-bit) checksum algorithm (1KiB blocks)",
    )
    parser.add_option(
        "-s",
        dest="algorithm",
        action="store_const",
        const="sysv",
        help="use the System V sum algorithm (512B blocks)",
    )

    opts, args = parser.parse_args()

    _sum(opts, args or ["-"])
