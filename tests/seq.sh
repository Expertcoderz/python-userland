#!/usr/bin/env sh

set -eux

set -- \
  '10' \
  '5 10' \
  '0 2 10' \
  '1.35 0.05 2' \
  '-- -1.0 2' \
  '-- -1 2.5 3'

for args in "$@"; do
  test "$(python -m userland seq ${args})" = "$(seq ${args})"
  test "$(python -m userland seq -w ${args})" = "$(seq -w ${args})"
done

exit 0
