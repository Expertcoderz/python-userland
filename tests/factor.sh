#!/usr/bin/env sh

set -eux

numbers="$(seq 0 10000)"
test "$(python -m userland factor ${numbers})" = "$(factor ${numbers})"

exit 0
