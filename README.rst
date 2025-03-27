===============
python-userland
===============

python-userland is a cross-platform implementation of various UNIX and Linux
utilities, written purely in Python 3. It aims to eventually achieve feature
parity with well-known projects such as GNU coreutils.

Source files are located under the `src/`; for portability, each of them is a
standalone Python executable that relies only on a Python interpreter and
standard library. No third-party libraries are (currently) used.

Note that this project is a work-in-progress. Not many utilities have been
finished, and existing utilities may be limited in functionality, performance
and correctness.

Compatibility with Other Implementations
========================================

Currently undecided.

Platform Support
================

python-userland should, in principle, run on any OS that runs Python. However,
much testing has only been done in a Linux environment. This will hopefully
change in the future.

License
=======

python-userland is licensed under the GPL. See the LICENSE file for more
information.
