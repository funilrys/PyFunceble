#!/usr/bin/env bash

set -e

workDir="$(dirname $(realpath ${0}))"
tmpDir="/tmp/pyfunceble-demos"
jsonDest="${tmpDir}/asciinema_demo.json"

jsonTemplate='{"title": "%%title%%","link": "%%link%%"}'
templates=()
finalJson=""

for file in ${workDir}/*.tut
do
    pyfuncebleIOTitle="$(fgrep "pyfunceble-io-title" ${file} | awk -v FS=": " '{ print $2}')"

    if [[ -z "${pyfuncebleIOTitle}" ]]
    then
        pyfuncebleIOTitle="PyFunceble-Demo"
    fi

    # uploadLink=$(${workDir}/upload.sh ${file})
    uploadLink="https://github.com"

    if [[ "${uploadLink}" =~ ^https:.* ]]
    then
        localTemplate="${jsonTemplate}"
        localTemplate="${localTemplate//%%title%%/${pyfuncebleIOTitle}}"
        localTemplate="${localTemplate//%%link%%/${uploadLink}/iframe}"

        templates[${#templates[@]}]="${localTemplate}"
    fi
done

finalJson+="["

templatesLength="${#templates[@]}"

for index in "${!templates[@]}"
do
    if [[ ! -z ${templates[${index}]} ]]
    then
        finalJson+="${templates[${index}]}"

        if [[ "${index}" != "$((${templatesLength}-1))" ]]
        then
            finalJson+=","
        fi
    fi
done

finalJson+="]"

echo "${finalJson}" >> "${jsonDest}"
