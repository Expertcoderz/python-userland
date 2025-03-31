#!/usr/bin/env sh

set -eux

start="$(date -u +%s)"

for n in $(seq 0 1000); do
  test "$(./factor.py "${n}")" = "$(factor "${n}")"
done

end="$(date -u +%s)"
printf '%.1f s elapsed\n' $(( end - start ))

exit 0
