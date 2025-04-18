import sys
from typing import BinaryIO, Callable, Iterable, cast

from .. import core


type Ranges = list[int | tuple[int, int | None]]
type RangeChecker = Callable[[int], bool]

type Cutter = Callable[[bytes], bytes | None]


def get_check_range(ranges: Ranges, complement: bool) -> RangeChecker:
    def check_range(pos: int) -> bool:
        for r in ranges:
            match r:
                case [min_pos, None]:
                    if pos >= min_pos:
                        return True
                case [min_pos, max_pos]:
                    if min_pos <= pos <= max_pos:
                        return True
                case wanted_pos:
                    if pos == wanted_pos:
                        return True

        return False

    return (lambda pos: not check_range(pos)) if complement else check_range


def get_cut_by_bytes(check_range: RangeChecker, line_terminator: bytes) -> Cutter:
    def cut_by_bytes(data: bytes) -> bytes:
        return b"".join(
            [n.to_bytes() for i, n in enumerate(data) if check_range(i + 1)]
            + [line_terminator]
        )

    return cut_by_bytes


def get_cut_by_fields(
    check_range: RangeChecker,
    input_delimiter: bytes,
    output_delimiter: bytes,
    only_delimited: bool,
) -> Cutter:
    def cut_by_fields(data: bytes) -> bytes | None:
        fields = data.split(input_delimiter)

        if len(fields) < 2:
            return None if only_delimited else data

        return output_delimiter.join(
            [field for i, field in enumerate(fields) if check_range(i + 1)]
        )

    return cut_by_fields


def cut_and_print_stream(stream: Iterable[bytes], cutter: Cutter) -> None:
    for line in stream:
        if (processed := cutter(line)) is not None:
            sys.stdout.buffer.write(processed)
            sys.stdout.buffer.flush()


parser = core.ExtendedOptionParser(usage="%prog OPTION... [FILE]...", description="wow")

parser.add_option("-b", "--bytes", metavar="LIST", help="select bytes in LIST")
parser.add_option("-c", "--characters", metavar="LIST", help="identical to -b")
parser.add_option("-f", "--fields", metavar="LIST", help="select fields in LIST")

parser.add_option("--complement", action="store_true", help="invert selection")

parser.add_option(
    "-s",
    "--only-delimited",
    action="store_true",
    help="ignore lines not containing the delimiter",
)
parser.add_option(
    "-d",
    "--delimiter",
    metavar="STRING",
    help="use STRING instead of TAB as field delimiter",
)
parser.add_option(
    "--output-delimiter",
    metavar="STRING",
    help="use STRING instead of input delimiter as output delimiter",
)

parser.add_option(
    "-z",
    "--zero-terminated",
    action="store_true",
    help="line delimiter is NUL instead of newline",
)

parser.add_option(
    "-n", action="store_true", help="(ignored; present for POSIX compatibility)"
)


def parse_range(range_specs: str) -> Ranges:
    ranges: Ranges = []

    for range_spec in range_specs.split(","):
        parts = range_spec.split("-")

        try:
            match parts:
                case [n]:
                    ranges.append(int(n))
                case [n, ""]:
                    ranges.append((int(n), None))
                case ["", m]:
                    ranges.append((0, int(m)))
                case [n, m]:
                    ranges.append((int(n), int(m)))
                case _:
                    raise ValueError
        except ValueError:
            parser.error(f"invalid range specification: {range_specs}")

    return ranges


@core.command(parser)
def python_userland_cut(opts, args: list[str]) -> int:
    cutter: Cutter

    match (opts.bytes, opts.characters, opts.fields):
        case (None, None, None):
            parser.error("expected one of --bytes, --characters or --fields")
        case (byte_range_spec, None, None) | (None, byte_range_spec, None):
            if opts.delimiter:
                parser.error("--delimiter is only allowed with --fields")

            if opts.only_delimited:
                parser.error("--only-delimited is only allowed with --fields")

            cutter = get_cut_by_bytes(
                check_range=get_check_range(
                    parse_range(cast(str, byte_range_spec)), opts.complement
                ),
                line_terminator=b"\0" if opts.zero_terminated else b"\n",
            )
        case (None, None, field_range_spec):
            opts.delimiter = opts.delimiter or "\t"

            if len(opts.delimiter) > 1:
                parser.error("the delimiter must be a single character")

            cutter = get_cut_by_fields(
                check_range=get_check_range(
                    parse_range(field_range_spec), opts.complement
                ),
                input_delimiter=(input_delimiter := opts.delimiter.encode()),
                output_delimiter=(
                    opts.output_delimiter.encode()
                    if opts.output_delimiter is not None
                    else input_delimiter
                ),
                only_delimited=opts.only_delimited,
            )
        case _:
            parser.error("only one list may be specified")

    append_newline = False

    # This is a hack to handle "\n" as a field delimiter.
    def process_line_stream(stream: BinaryIO) -> Iterable[bytes]:
        nonlocal append_newline

        if not (opts.fields and opts.delimiter == "\n"):
            return stream

        data = stream.read()
        if data and data[-1] == ord(b"\n"):
            # Don't treat the last newline as a delimiter.
            data = data[:-1]
            append_newline = True

        return (data for _ in (None,))

    failed = False

    for name in args or ["-"]:
        append_newline = False

        if name == "-":
            cut_and_print_stream(
                (
                    core.get_lines_by_delimiter(sys.stdin.buffer, b"\0")
                    if opts.zero_terminated
                    else process_line_stream(sys.stdin.buffer)
                ),
                cutter,
            )
        else:
            try:
                with open(name, "rb") as f:
                    cut_and_print_stream(
                        (
                            core.get_lines_by_delimiter(f, b"\0")
                            if opts.zero_terminated
                            else process_line_stream(f)
                        ),
                        cutter,
                    )
            except OSError as e:
                failed = True
                core.perror(e)
                continue

        if append_newline:
            print()

    return int(failed)
