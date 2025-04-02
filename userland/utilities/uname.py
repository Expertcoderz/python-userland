import os

from .. import core


# mapping of uname_result attribute name to option atttribute name
UNAME_ATTRS = {
    "sysname": "kernel_name",
    "nodename": "nodename",
    "release": "kernel_release",
    "version": "kernel_version",
    "machine": "machine",
}


parser = core.create_parser(
    usage=("%prog [OPTION]...",),
    description="Print system information.",
)

parser.add_option(
    "-a",
    "--all",
    action="store_true",
    help="print all",
)
parser.add_option(
    "-s",
    "--kernel-name",
    action="store_true",
    help="print kernel name (default)",
)
parser.add_option(
    "-n",
    "--nodename",
    action="store_true",
    help="print hostname",
)
parser.add_option(
    "-r",
    "--kernel-release",
    action="store_true",
    help="print kernel release",
)
parser.add_option(
    "-v",
    "--kernel-version",
    action="store_true",
    help="print kernel version",
)
parser.add_option(
    "-m",
    "--machine",
    action="store_true",
    help="print machine hardware type",
)
parser.add_option(
    "-p",
    "--processor",
    action="store_true",
    help="print processor type (unimplemented)",
)
parser.add_option(
    "-i",
    "--hardware-platform",
    action="store_true",
    help="print hardware platform (unimplemented)",
)
parser.add_option(
    "-o",
    "--operating-system",
    action="store_true",
    help="print operating system (unimplemented)",
)


@core.command(parser)
def python_userland_uname(opts, args):
    if args:
        parser.error(f"extra operand '{args[0]}'")

    extras: list[str] = []

    if opts.all:
        for optname in UNAME_ATTRS.values():
            setattr(opts, optname, True)
    else:
        if opts.processor:
            extras.append("unknown")

        if opts.hardware_platform:
            extras.append("unknown")

        if opts.operating_system:
            extras.append("unknown")

    if not extras and not any(
        {getattr(opts, optname) for optname in UNAME_ATTRS.values()}
    ):
        opts.kernel_name = True

    uname = os.uname()

    print(
        " ".join(
            [
                getattr(uname, attribute)
                for attribute in [
                    "sysname",
                    "nodename",
                    "release",
                    "version",
                    "machine",
                ]
                if getattr(opts, UNAME_ATTRS[attribute])
            ]
            + extras
        )
    )

    return 0
