import os
import sys
from typing import Any, Generator


def perror(*errors: Any) -> None:
    print(
        f"{os.path.basename(sys.argv[0])}: {"\n".join(map(str, errors))}",
        file=sys.stderr,
    )


def readlines_stdin() -> Generator[str]:
    while line := sys.stdin.readline():
        yield line


def readlines_stdin_raw() -> Generator[bytes]:
    while line := sys.stdin.buffer.readline():
        yield line


def readwords_stdin() -> Generator[str]:
    for line in readlines_stdin():
        yield from line.split()


def readwords_stdin_raw() -> Generator[bytes]:
    for line in readlines_stdin_raw():
        yield from line.split()
