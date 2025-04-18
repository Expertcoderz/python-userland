#!/usr/bin/env sh

set -eux

## cut by bytes with range

result="$(echo 'abcdefghi' | python -m userland cut -b -3,5-6,8-)"

test "${result}" = 'abcefhi'

## cut by bytes, zero-terminated

result="$(printf 'foo\0bar' | python -m userland cut -b 3 -z)"

test "${result}" = 'or'

## cut by field

result="$(echo 'foo:bar' | python -m userland cut -f 2 -d ':')"

test "${result}" = 'bar'

## cut by field complement

result="$(echo 'foo:bar' | python -m userland cut -f 2 -d ':' --complement)"

test "${result}" = 'foo'

## cut by field, only delimited

result="$(printf 'foo\tbar\naaa\n' | python -m userland cut -f 2 -s)"

test "${result}" = 'bar'

## cut by field, with output delimiter

result="$(echo 'foo:bar' | python -m userland cut -f 1,2 -d ':' \
  --output-delimiter='d')"

test "${result}" = 'foodbar'

## cut by field, with newline as delimiter

result="$(printf 'foo\nbar' | python -m userland cut -f 2 -d '
')"

test "${result}" = 'bar'

## cut by field, with newline as delimiter, only delimited

result="$(printf 'foo\0bar\nx' | python -m userland cut -f 2 -d '
' -s -z)"

test "${result}" = 'x'

exit 0
