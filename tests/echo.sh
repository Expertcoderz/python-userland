#!/usr/bin/env sh

set -eux

## basic echo

result="$(python -m userland echo foo bar)"

test "${result}" = 'foo bar'

## double hyphen

result="$(python -m userland echo -- foo)"

test "${result}" = '-- foo'

## multiple double hyphens

result="$(python -m userland echo -- foo --)"

test "${result}" = '-- foo --'

## unknown option

result="$(python -m userland echo -x foo)"

test "${result}" = '-x foo'

## unknown option and double hyphen

result="$(python -m userland echo -x -- foo)"

test "${result}" = '-x -- foo'

## escape codes

result="$(python -m userland echo -e 'foo \x41' '\0102')"

test "${result}" = 'foo A B'

## no arguments

result="$(python -m userland echo)"

test "${result}" = "$(printf '\n')"

## empty arguments

result="$(python -m userland echo '' foo '' bar '' '')"

test "${result}" = ' foo  bar  '

## no trailing newline

n_lines="$(python -m userland echo -n 'foo' | wc -l)"

test "${n_lines}" = 0

exit 0
