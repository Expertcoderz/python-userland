import os
import sys
from typing import Any, Generator, IO


def perror(*errors: Any) -> None:
    print(
        f"{os.path.basename(sys.argv[0])}: {"\n".join(map(str, errors))}",
        file=sys.stderr,
    )


def readwords_stdin() -> Generator[str]:
    for line in sys.stdin:
        yield from line.split()


def readwords_stdin_raw() -> Generator[bytes]:
    for line in sys.stdin.buffer:
        yield from line.split()


def get_lines_by_delimiter[T: (
    str,
    bytes,
)](stream: IO[T], delimiter: T) -> Generator[T]:
    joiner = type(delimiter)()
    line = []

    while char := stream.read(1):
        if char == delimiter:
            yield joiner.join(line)
            line.clear()
        else:
            line.append(char)

    if line:
        yield joiner.join(line)
