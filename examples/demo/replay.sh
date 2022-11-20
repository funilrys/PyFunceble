#!/usr/bin/env bash

set -e

hash pyfunceble

tmpDir="/tmp/pyfunceble-demos"

for file in "${@}"; do
    castFile="${tmpDir}/$(basename "${file}").cast"

    if [[ -f "${castFile}" ]]
    then
        asciinema play "${castFile}"
    else
        echo "File not found: ${castFile}"
    fi
done
