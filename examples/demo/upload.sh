#!/usr/bin/env bash

set -e

hash asciinema
hash grep
hash sed

tmpDir="/tmp/pyfunceble-demos"

for file in "${@}"; do
    castFile="/${tmpDir}/$(basename "${file}").cast"

    asciinema upload ${castFile} | grep 'https:' | sed 's/^\s*//'
done
