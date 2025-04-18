import os

from tqdm import tqdm

from .. import core


parser = core.ExtendedOptionParser(
    usage="%prog [OPTION] [FILE]...",
    description="Sync the filesystem or write each FILE's blocks to disk.",
)

parser.add_option(
    "--progress",
    dest="progress",
    action="store_true",
    help="show a progress bar when syncing files",
)
parser.add_option(
    "--no-progress",
    dest="progress",
    action="store_false",
    default=False,
    help="do not show a progress bar (default)",
)


@core.command(parser)
def python_userland_sync(opts, args: list[str]) -> int:
    if not args:
        os.sync()
        return 0

    failed = False

    for name in tqdm(args, ascii=True, desc="Syncing files") if opts.progress else args:
        try:
            with open(name, "rb+") as f:
                os.fsync(f)
        except OSError as e:
            failed = True
            core.perror(e)

    return int(failed)
