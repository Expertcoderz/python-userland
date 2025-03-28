#!/usr/bin/python3

from optparse import OptionParser


def hostid():
    # We're not the only ones being lazy here... musl libc's gethostid(3)
    # returns zero as well. hostid can arguably be considered as obsolete.
    print("00000000")


if __name__ == "__main__":
    parser = OptionParser(
        usage="Usage: %prog",
        description="Print a 32-bit numeric host machine identifier.",
        epilog="This implementation gives an all-zero identifier.",
        add_help_option=False,
    )
    parser.add_option("--help", action="help", help="show usage information and exit")

    _, args = parser.parse_args()

    if args:
        parser.error(f"extra operand '{args[0]}'")

    hostid()
