import importlib
import importlib.metadata
import sys
from pathlib import Path

file = Path(__file__).resolve(strict=True)

applets = (applet.stem for applet in Path(file.parent, "utilities").glob("*.py"))


def print_usage(prog_name: str) -> None:
    try:
        version = importlib.metadata.version(__package__)
    except importlib.metadata.PackageNotFoundError:
        version = "(unknown version)"

    print(
        f"python-userland v{version}",
        f"Usage: {prog_name} APPLET [ARGUMENT]...",
        f"{7 * " "}{prog_name} --list",
        "\nAvailable applets:",
        ", ".join(sorted(applets)),
        sep="\n"
    )


def main() -> int:
    assert sys.argv

    prog = Path(sys.argv.pop(0))

    if prog.stem in ("python-userland", "__main__"):
        match sys.argv:
            case [] | ["--help"]:
                print_usage(
                    f"{Path(sys.executable).name} -m {__package__}"
                    if prog.stem == "__main__"
                    else prog.name
                )
                return 0
            case ["--list"]:
                print(*sorted(applets), sep="\n")
                return 0

    applet_name = Path(sys.argv[0]).stem.replace("-", "_")

    try:
        applet_module = importlib.import_module(
            f".utilities.{applet_name}", __package__
        )
    except ModuleNotFoundError:
        print(f"{applet_name}: applet not found")
        return 127

    return getattr(applet_module, "python_userland_" + applet_name)()


if __name__ == "__main__":
    sys.exit(main())
