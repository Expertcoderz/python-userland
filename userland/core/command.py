import sys
from optparse import OptionParser, Values
from typing import Callable

from .users import OptionParserUsersMixin


class ExtendedOptionParser(OptionParserUsersMixin, OptionParser):
    def __init__(self, usage: str | tuple[str, ...], **kwargs):
        super().__init__(
            usage="Usage: "
            + f"\n{7 * " "}".join(usage if isinstance(usage, tuple) else (usage,)),
            add_help_option=False,
            **kwargs,
        )

        self.add_option(
            "--help",
            action="help",
            help="show usage information and exit",
        )

    def expect_nargs(self, args: list[str], nargs: int | tuple[int] | tuple[int, int]):
        if isinstance(nargs, int):
            nargs = (nargs, nargs)

        if len(nargs) == 1:
            nargs = (nargs[0], len(args))

        if nargs[0] <= len(args) <= nargs[1]:
            return

        if args:
            if len(args) < nargs[0]:
                self.error(f"missing operand after '{args[-1]}'")
            else:
                self.error(f"extra operand '{args[nargs[1]]}'")
        else:
            self.error("missing operand")


def command(parser: OptionParser | None = None):
    def create_utility(
        func: Callable[[Values, list[str]], int],
    ) -> Callable[[], None]:
        def execute_utility():
            try:
                sys.exit(
                func(*parser.parse_args()) if parser else func(Values(), sys.argv[1:])
            )
            except KeyboardInterrupt:
                print()
                sys.exit(130)

        return execute_utility

    return create_utility
