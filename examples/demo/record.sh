#!/usr/bin/env bash

set -e

hash awk
hash pyfunceble

tmpDir="/tmp/pyfunceble-demos"

if [[ ! -d ${tmpDir} ]]
then
    mkdir -p "${tmpDir}"
fi

echo "Pre-warming for better recording performance"
pyfunceble --version >/dev/null

for file in "${@}"; do
    castFile="${tmpDir}/$(basename "${file}").cast"
    castTitle="$(fgrep "asciinema-title" ${file} | awk -v FS=": " '{ print $2}')"
    castColumns="$(fgrep "asciinema-cols" ${file} | awk -v FS=": " '{ print $2}')"
    castRows="$(fgrep "asciinema-rows" ${file} | awk -v FS=": " '{ print $2}')"

    if [[ -z "${castTitle}" ]]
    then
        castTitle="PyFunceble"
    fi

    if [[ -z "${castColumns}" ]]
    then
        castColumns=200
    fi

    if [[ -z "${castRows}" ]]
    then
        castRows=20
    fi

    rm -f "${castFile}"

    stty cols "${castColumns}" rows "${castRows}"
    asciinema rec -t "${castTitle}" -c "tuterm ${file} --mode demo" "${castFile}"
done
