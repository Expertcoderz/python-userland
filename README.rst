===============
python-userland
===============

python-userland is an experimental cross-platform implementation of various
UNIX and Linux utilities, written purely in Python 3.

Note that this project is a work-in-progress. Not many utilities have been
finished, and existing utilities may be limited in functionality, performance
and correctness.

Utilities Featured
==================

python-userland aims to implement as much as can be done in Python and its
standard library, without relying on additional C bindings for system-specific
functions. Currently, the focus is on achieving feature parity with `GNU
Coreutils <https://www.gnu.org/software/coreutils/>`_, although not all
utilities (e.g. ``clear``) are necessarily from the Coreutils project.

Platform Support
================

python-userland should, in principle, run on any OS that runs Python. However,
much testing has only been done in a Linux environment. This will hopefully
change in the future.

License
=======

python-userland is licensed under the GPL. See the LICENSE file for more
information.
