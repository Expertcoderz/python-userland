import codecs
import re
from optparse import OptionParser, BadOptionError, AmbiguousOptionError

from .. import core


ESCAPES_PATTERN = re.compile(
    r"(\\0[0-7]{1,3}|\\x[0-9A-Za-z]{1,2}|\\[\\0abcefnrtv])",
    re.UNICODE | re.VERBOSE,
)


class PassthroughOptionParser(OptionParser):
    """
    A modified version of OptionParser that treats unknown options and "--" as
    regular arguments. Always behaves as if interspersed args are disabled.
    """

    def _process_args(self, largs, rargs, values):
        parsing_options = True

        for arg in rargs:
            if parsing_options and arg and arg[0] == "-" and arg != "--":
                try:
                    super()._process_args([], [arg], values)
                except (BadOptionError, AmbiguousOptionError) as e:
                    parsing_options = False
                    largs.append(e.opt_str)
            else:
                parsing_options = False
                largs.append(arg)

        rargs.clear()


parser = core.create_parser(
    usage=("%prog [OPTION]... [STRING]...",),
    description="Print STRING(s) to standard output.",
    parser_class=PassthroughOptionParser,
)
parser.disable_interspersed_args()

parser.add_option("-n", action="store_true", help="do not output the trailing newline")
parser.add_option(
    "-e",
    dest="escapes",
    action="store_true",
    help="enable interpretation of backslash escapes",
)
parser.add_option(
    "-E",
    dest="escapes",
    action="store_false",
    default=False,
    help="disable interpretation of backslash escapes (default)",
)


@core.command(parser)
def python_userland_echo(opts, args):
    string = " ".join(args)

    if opts.escapes:

        def decode_match(match: re.Match[str]) -> str:
            try:
                if (escape := match.group(0))[1] == "0" and len(escape) > 2:
                    # Convert octal escapes from "\0NNN" to Python's form
                    # ("\NNN" without the "0").
                    escape = "\\" + escape[2:]

                return codecs.decode(escape, "unicode_escape")
            except UnicodeDecodeError:
                return match.group(0)

        string = ESCAPES_PATTERN.sub(decode_match, string)

    print(string, end="" if opts.n else "\n")

    return 0
