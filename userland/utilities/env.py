import os
import shlex

from .. import core


parser = core.ExtendedOptionParser(
    usage="%prog [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]",
    description="Run a program in a modified environment or print environment variables.",
)
parser.disable_interspersed_args()

parser.add_option(
    "-a",
    "--argv0",
    metavar="ARG",
    help="pass ARG as zeroth argument instead of COMMAND",
)
parser.add_option(
    "-i",
    "--ignore-environment",
    action="store_true",
    help="start with empty environment",
)
parser.add_option(
    "-u",
    "--unset",
    action="append",
    metavar="NAME",
    help="remove variable NAME from the environment",
)
parser.add_option(
    "-0",
    "--null",
    action="store_true",
    help="terminate outputs with NUL instead of newline",
)
parser.add_option(
    "-C",
    "--chdir",
    metavar="DIR",
    help="change working directory to DIR",
)
parser.add_option(
    "-S",
    "--split-string",
    metavar="STRING",
    help="split STRING into separate arguments",
)


def parse_env_args(args: list[str], env: dict[str, str], prog_args: list[str]) -> None:
    parsing_decls = True

    for arg in args:
        if parsing_decls and (eq_pos := arg.find("=")) >= 0:
            env[arg[:eq_pos]] = arg[eq_pos + 1 :]
        else:
            prog_args.append(arg)
            parsing_decls = False


@core.command(parser)
# pylint: disable=inconsistent-return-statements
def python_userland_env(opts, args: list[str]) -> int:
    if args and args[0] == "-":
        opts.ignore_environment = True
        del args[0]

    env: dict[str, str]

    if opts.ignore_environment:
        env = {}
    elif opts.unset:
        env = {
            name: value for name, value in os.environ.items() if name not in opts.unset
        }
    else:
        env = os.environ.copy()

    prog_args = []
    parse_env_args(args, env, prog_args)

    if opts.split_string:
        prog_args = shlex.split(opts.split_string) + prog_args

    if not prog_args:
        for name, value in env.items():
            print(f"{name}={value}", end="\0" if opts.null else "\n")
        return 0

    if opts.chdir:
        try:
            os.chdir(opts.chdir)
        except OSError as e:
            core.perror(e)
            return 125

    prog_args.insert(1, opts.argv0 if opts.argv0 else prog_args[0])

    try:
        os.execvpe(prog_args[0], prog_args[1:], env)
    except OSError as e:
        core.perror(e)
        return 126 if isinstance(e, FileNotFoundError) else 127
