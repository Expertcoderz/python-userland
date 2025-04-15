import sys
from pathlib import Path
from typing import Generator, Iterable, Literal


def traverse_files(
    filenames: Iterable[str],
    recurse_mode: Literal["L", "H", "P"] | None = None,
    preserve_root: bool = False,
) -> Generator[Path | None]:
    if not recurse_mode:
        yield from map(Path, filenames)
        return

    def traverse(file: Path) -> Generator[Path]:
        for child in file.iterdir():
            if child.is_dir(follow_symlinks=recurse_mode == "L"):
                yield from traverse(child)
            yield child

    for file in map(Path, filenames):
        if preserve_root and file.root == str(file):
            print(
                f"recursive operation on '{file}' prevented;"
                " use --no-preserve-root to override",
                file=sys.stderr,
            )
            yield None
            continue

        if file.is_dir(follow_symlinks=recurse_mode in set("HL")):
            yield from traverse(file)
        else:
            yield file
