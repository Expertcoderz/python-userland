#!/usr/bin/python3

import os
import sys


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(
            f"""\
Usage: {os.path.basename(sys.argv[0])} [IGNORED]...

Return an exit status of 0.

Options:
  --help  show usage information and exit"""
        )
