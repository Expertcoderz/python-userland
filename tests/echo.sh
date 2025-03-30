#!/usr/bin/env sh

set -eux

## basic echo

result="$(./echo.py foo bar)"

test "${result}" = 'foo bar'

## double hyphen

result="$(./echo.py -- foo)"

test "${result}" = '-- foo'

## multiple double hyphens

result="$(./echo.py -- foo --)"

test "${result}" = '-- foo --'

## unknown option

result="$(./echo.py -x foo)"

test "${result}" = '-x foo'

## unknown option and double hyphen

result="$(./echo.py -x -- foo)"

test "${result}" = '-x -- foo'

## escape codes

result="$(./echo.py -e 'foo \x41' '\0102')"

test "${result}" = 'foo A B'

## no arguments

result="$(./echo.py)"

test "${result}" = "$(printf '\n')"

## empty arguments

result="$(./echo.py '' foo '' bar '' '')"

test "${result}" = ' foo  bar  '

## no trailing newline

n_lines="$(./echo.py -n 'foo' | wc -l)"

test "${n_lines}" = 0

exit 0
