#!/usr/bin/env bash

set -e

workDir="$(dirname $(realpath ${0}))"

for file in ${workDir}/*.tut
do
    ${workDir}/replay.sh ${file}
done
