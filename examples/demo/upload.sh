#!/usr/bin/env sh

set -e

for file in "$@"; do
    cast="/tmp/PyFunceble/$(basename "$file").cast"
    asciinema upload "$cast" | grep 'https:' | sed 's/^\s*//'
done
