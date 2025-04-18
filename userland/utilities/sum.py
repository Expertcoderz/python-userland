import sys

from .. import core


# BSD 16-bit checksum
def sum_bsd(data: bytes) -> str:
    checksum = 0
    for b in data:
        checksum = (checksum >> 1) + ((checksum & 1) << 15)
        checksum += b
        checksum &= 0xFFFF

    return f"{checksum:05}{-(len(data) // -1024):>6}"


# SYSV checksum
def sum_sysv(data: bytes) -> str:
    s = sum(data)
    r = s % 2**16 + (s % 2**32) // 2**16
    checksum = (r % 2**16) + r // 2**16

    return f"{checksum:03} {-(len(data) // -512)}"


SUM_ALGORITHMS = {"bsd": sum_bsd, "sysv": sum_sysv}

parser = core.ExtendedOptionParser(
    usage="%prog [OPTION] [FILE]...",
)

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


@core.command(parser)
def python_userland_sum(opts, args: list[str]) -> int:
    failed = False

    for name in args or ["-"]:
        if name == "-":
            print(SUM_ALGORITHMS[opts.algorithm](sys.stdin.buffer.read()))
        else:
            try:
                with open(name, "rb") as f:
                    print(f"{SUM_ALGORITHMS[opts.algorithm](f.read())} {name}")
            except OSError as e:
                failed = True
                core.perror(e)

    return int(failed)
