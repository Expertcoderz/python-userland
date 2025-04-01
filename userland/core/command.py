import sys
from optparse import OptionParser
from typing import Any, Callable


def create_parser(usage: tuple[str], **kwargs) -> OptionParser:
    if parser_class := kwargs.get("parser_class"):
        del kwargs["parser_class"]

    parser = (parser_class or OptionParser)(
        usage="Usage: " + f"\n{7 * " "}".join(usage),
        **kwargs,
        add_help_option=False,
    )
    parser.add_option(
        "--help",
        action="help",
        help="show usage information and exit",
    )

    return parser


def command(parser: OptionParser | None = None):
    def create_utility(
        func: Callable[[dict[str, Any], list[Any]], int],
    ) -> Callable[[], None]:
        if parser:

            def execute_utility():
                sys.exit(func(*parser.parse_args()))

        else:

            def execute_utility():
                sys.exit(func({}, sys.argv[1:]))

        return execute_utility

    return create_utility
