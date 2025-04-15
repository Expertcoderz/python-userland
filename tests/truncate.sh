#!/usr/bin/env sh

set -eux

tempdir="$(mktemp -d)"

trap 'rm -rf ${tempdir}' EXIT

get_size() {
  wc -c "$1" | cut -d ' ' -f 1
}

## basic truncation

echo 'foo bar' > "${tempdir}"/a

python -m userland truncate -s 3 "${tempdir}"/a

test "$(cat "${tempdir}"/a)" = 'foo'

## size extension

python -m userland truncate -s +7 "${tempdir}"/a

size="$(get_size "${tempdir}"/a)"
test "${size}" = 10

## ensure minimum size

python -m userland truncate -s '>5' "${tempdir}"/a

size="$(get_size "${tempdir}"/a)"
test "${size}" = 10

## truncate to maximum size

python -m userland truncate -s '<8' "${tempdir}"/a

size="$(get_size "${tempdir}"/a)"
test "${size}" = 8

## round size to multiple

python -m userland truncate -s %5 "${tempdir}"/a

size="$(get_size "${tempdir}"/a)"
test "${size}" = 10

## ensure size is multiple

python -m userland truncate -s /2 "${tempdir}"/a

size="$(get_size "${tempdir}"/a)"
test "${size}" = 10

## truncate with reference file

touch "${tempdir}"/b

python -m userland truncate -r "${tempdir}"/a "${tempdir}"/b

size="$(get_size "${tempdir}"/b)"
test "${size}" = 10

## truncate with reference file and size adjustment

python -m userland truncate -r "${tempdir}"/a -s +10 "${tempdir}"/b

size="$(get_size "${tempdir}"/b)"
test "${size}" = 20

## truncate with block size

python -m userland truncate -s 0 -o "${tempdir}"/a

test ! -s "${tempdir}"/a

exit 0
