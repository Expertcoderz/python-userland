import os
import sys
from typing import Any, Generator


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
