#!/usr/bin/env sh

set -e

# Pre-warm PyFunceble for better performance
echo Pre-warming for better recording performance
for i in $(seq 1 10); do
    PyFunceble --version >/dev/null
done

for file in "$@"; do
    mkdir -p "/tmp/PyFunceble"
    cast="/tmp/PyFunceble/$(basename "$file").cast"
    rm -f "$cast"
    stty cols 166 rows 45
    asciinema rec -c "tuterm $file --mode demo" "$cast"
done
