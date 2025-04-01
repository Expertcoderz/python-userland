import itertools
import sys
from io import BufferedReader
from typing import BinaryIO, Generator

from .. import core


def squeeze_blank_lines(io: BinaryIO) -> Generator[bytes]:
    was_blank = False

    for line in io:
        is_blank = len(line) < 2

        if was_blank and is_blank:
            continue

        yield line
        was_blank = is_blank


def number_lines(io: BinaryIO) -> Generator[bytes]:
    for i, _ in enumerate(io):
        yield f"{i + 1:>6}  ".encode()


def number_nonblank_lines(io: BinaryIO) -> Generator[bytes]:
    i = 1
    for line in io:
        if len(line) > 1:
            yield f"{i:>6}  ".encode()
            i += 1
        else:
            yield b""


def format_chars(
    data: bytes, show_ends: bool, show_tabs: bool, show_nonprinting: bool
) -> Generator[bytes]:
    for n in data:
        if n == ord(b"\n"):
            if show_ends:
                yield b"$\n"
                continue
        elif n == ord(b"\t"):
            if show_tabs:
                yield b"^I"
                continue
        elif show_nonprinting and (n < 32 or n > 126):
            if n < 32:
                yield b"^" + (n + 64).to_bytes()
            elif n == 127:
                yield b"^?"
            elif n < 128 + 32:
                yield b"M-^" + (n - 128 + 64).to_bytes()
            elif n < 128 + 127:
                yield b"M-" + (n - 128).to_bytes()
            else:
                yield b"M-?"
            continue

        yield n.to_bytes()


def format_lines(io: BinaryIO, *args) -> Generator[bytes]:
    for line in io:
        yield b"".join(format_chars(line, *args))


def cat_io(opts, io: BinaryIO) -> None:
    if opts.squeeze_blank:
        io = squeeze_blank_lines(io)

    io1, io2 = itertools.tee(io, 2)
    gen1, gen2 = None, None

    if opts.number_nonblank:
        gen1 = number_nonblank_lines(io1)
    elif opts.number:
        gen1 = number_lines(io1)

    if opts.show_ends or opts.show_tabs or opts.show_nonprinting:
        gen2 = format_lines(io2, opts.show_ends, opts.show_tabs, opts.show_nonprinting)
    else:
        gen2 = io2

    if gen1 and gen2:
        for part1, part2 in zip(gen1, gen2, strict=True):
            sys.stdout.buffer.write(part1 + part2)
            sys.stdout.buffer.flush()
    else:
        for line in gen2:
            sys.stdout.buffer.write(line)
            sys.stdout.buffer.flush()


parser = core.create_parser(
    usage=("%prog [OPTION]... [FILE]...",),
    description="Concatenate each FILE to standard output.",
)

parser.add_option(
    "-E", "--show-ends", action="store_true", help="append '$' to each LF"
)
parser.add_option("-T", "--show-tabs", action="store_true", help="convert TABs to '^I'")
parser.add_option(
    "-v",
    "--show-nonprinting",
    action="store_true",
    help="show nonprinting characters except LF and TAB with ^ and M- notation",
)
parser.add_option("-A", "--show-all", action="store_true", help="equivalent to -vET")
parser.add_option("-e", action="store_true", help="equivalent to -vE")
parser.add_option("-t", action="store_true", help="equivalent to -vT")

parser.add_option("-n", "--number", action="store_true", help="number each output line")
parser.add_option(
    "-b",
    "--number-nonblank",
    action="store_true",
    help="number each nonempty output line (overrides -n)",
)

parser.add_option(
    "-s",
    "--squeeze-blank",
    action="store_true",
    help="collapse repeated empty output lines",
)

parser.add_option(
    "-u", action="store_true", help="(ignored; present for POSIX compatibility)"
)


@core.command(parser)
def python_userland_cat(opts, args):
    if opts.show_all:
        opts.show_ends = True
        opts.show_tabs = True
        opts.show_nonprinting = True
    elif opts.e:
        opts.show_ends = True
        opts.show_nonprinting = True
    elif opts.t:
        opts.show_tabs = True
        opts.show_nonprinting = True

    generators = [
        core.readlines_stdin_raw() if name == "-" else open(name, "rb")
        for name in args or ["-"]
    ]

    try:
        cat_io(opts, itertools.chain(*generators))
    except KeyboardInterrupt:
        print()
        return 130
    finally:
        for gen in generators:
            # Close opened files other than stdin.
            if isinstance(gen, BufferedReader):
                gen.close()

    return 0
