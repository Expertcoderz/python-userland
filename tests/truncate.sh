#!/usr/bin/env sh

set -eux

tempdir="$(mktemp -d)"

trap 'rm -rf ${tempdir}' EXIT

get_size() {
  wc -c "$1" | cut -d ' ' -f 1
}

## basic truncation

echo 'foo bar' > "${tempdir}"/a

./truncate.py -s 3 "${tempdir}"/a

test "$(cat "${tempdir}"/a)" = 'foo'

## size extension

./truncate.py -s +7 "${tempdir}"/a

size="$(get_size "${tempdir}"/a)"
test "${size}" = 10

## ensure minimum size

./truncate.py -s '>5' "${tempdir}"/a

size="$(get_size "${tempdir}"/a)"
test "${size}" = 10

## truncate to maximum size

./truncate.py -s '<8' "${tempdir}"/a

size="$(get_size "${tempdir}"/a)"
test "${size}" = 8

## round size to multiple

./truncate.py -s %5 "${tempdir}"/a

size="$(get_size "${tempdir}"/a)"
test "${size}" = 10

## ensure size is multiple

./truncate.py -s /2 "${tempdir}"/a

size="$(get_size "${tempdir}"/a)"
test "${size}" = 10

## truncate with reference file

touch "${tempdir}"/b

./truncate.py -r "${tempdir}"/a "${tempdir}"/b

size="$(get_size "${tempdir}"/b)"
test "${size}" = 10

## truncate with reference file and size adjustment

./truncate.py -r "${tempdir}"/a -s +10 "${tempdir}"/b

size="$(get_size "${tempdir}"/b)"
test "${size}" = 20

## truncate with block size

./truncate.py -s 0 -o "${tempdir}"/a

test ! -s "${tempdir}"/a

exit 0
