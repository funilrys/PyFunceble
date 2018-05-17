#!/usr/bin/env python3

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the configuration.


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on 13th March, 2018.

Its main objective is to get and the return domains and IPs availability by
generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

In its daily usage, PyFunceble is mostly used to clean `hosts` files or blocklist.
Indeed, it is possible because PyFunceble generates a list of all `ACTIVE` domains
or IPs but in the same time, it creates by default a database of the `INACTIVE`
domains or IPs so we can retest them overtime automatically at the next execution.

PyFunceble is running actively and daily with the help of Travis CI under 60+
repositories. It is used to clean or test the availability of data which are
present in hosts files, list of IP, list of domains, blocklists or even AdBlock
filter lists.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: disable=bad-continuation
import PyFunceble
from PyFunceble import Fore, Style, directory_separator, environ, path
from PyFunceble.helpers import Dict, Directory, Download, File


def load_config_file(path_to_config):
    """
    This function will load .PyFunceble.yaml.
    """

    PyFunceble.CONFIGURATION.update(Dict.from_yaml(File(path_to_config).read()))


def install_production_config(path_to_config):
    """
    This function download the production configuration and install it in the
    current directory.

    Argument:
        - path_to_config: str
            The path were we have to install the configuration file.
    """

    production_config_link = "https://raw.githubusercontent.com/funilrys/PyFunceble/master/.PyFunceble_production.yaml"  # pylint: disable=line-too-long

    if "dev" in PyFunceble.VERSION:
        production_config_link = production_config_link.replace("master", "dev")
    else:
        production_config_link = production_config_link.replace("dev", "master")

    return Download(production_config_link, path_to_config).text()


def install_iana_config():
    """
    This function download `iana-domains-db.json` if not present.
    """

    iana_link = "https://raw.githubusercontent.com/funilrys/PyFunceble/master/iana-domains-db.json"
    destination = PyFunceble.CURRENT_DIRECTORY + "iana-domains-db.json"

    if "dev" in PyFunceble.VERSION:
        iana_link = iana_link.replace("master", "dev")
    else:
        iana_link = iana_link.replace("dev", "master")

    if not path.isfile(destination):
        return Download(iana_link, destination).text()

    return True


def load_configuration(path_to_config):
    """
    This function will load and adjust .PyFunceble.yaml before parsing CONFIGURATION
    to CONFIGURATION.

    Argument:
        - path_to_config: str
            The path to the .PyFunceble.yaml to read.
    """

    if not path_to_config.endswith(directory_separator):
        path_to_config += directory_separator

    path_to_config += ".PyFunceble.yaml"

    try:
        load_config_file(path_to_config)
        install_iana_config()
    except FileNotFoundError:

        if "PYFUNCEBLE_AUTO_CONFIGURATION" not in environ:
            while True:
                response = input(
                    "%s was not found.\n\
Install the default configuration in the current directory ? [y/n] "
                    % (Style.BRIGHT + path_to_config + Style.RESET_ALL)
                )

                if isinstance(response, str):
                    if response.lower() == "y":
                        install_production_config(path_to_config)
                        load_config_file(path_to_config)
                        install_iana_config()
                        break

                    elif response.lower() == "n":
                        raise Exception("Unable to find the configuration file.")

        else:
            install_production_config(path_to_config)
            load_config_file(path_to_config)
            install_iana_config()

    for main_key in ["domains", "hosts", "splited"]:
        PyFunceble.CONFIGURATION["outputs"][main_key]["directory"] = Directory(
            PyFunceble.CONFIGURATION["outputs"][main_key]["directory"]
        ).fix_path()

    for main_key in ["http_analytic", "logs"]:
        for key, value in PyFunceble.CONFIGURATION["outputs"][main_key][
            "directories"
        ].items():
            PyFunceble.CONFIGURATION["outputs"][main_key]["directories"][
                key
            ] = Directory(
                value
            ).fix_path()

    PyFunceble.CONFIGURATION["outputs"]["main"] = Directory(
        PyFunceble.CONFIGURATION["outputs"]["main"]
    ).fix_path()

    PyFunceble.STATUS.update(PyFunceble.CONFIGURATION["status"])
    PyFunceble.OUTPUTS.update(PyFunceble.CONFIGURATION["outputs"])
    PyFunceble.HTTP_CODE.update(PyFunceble.CONFIGURATION["http_codes"])
    PyFunceble.LINKS.update(PyFunceble.CONFIGURATION["links"])

    PyFunceble.CONFIGURATION.update({"done": Fore.GREEN + "✔", "error": Fore.RED + "✘"})

    return True


def compare_version():
    """
    This function will compare the current version with the upstream saved version.
    """

    upstream_link = "https://raw.githubusercontent.com/funilrys/PyFunceble/master/version.yaml"

    if "dev" in PyFunceble.VERSION:
        upstream_link = upstream_link.replace("master", "dev")
    else:
        upstream_link = upstream_link.replace("dev", "master")

    data = Dict().from_yaml(Download(upstream_link, return_data=True).text())

    if data["force_update"] and data["current_version"] != PyFunceble.VERSION:
        message = Style.BRIGHT + Fore.RED + "A critical issue has been fixed.\n" + Style.RESET_ALL
        message += Style.BRIGHT + Fore.GREEN + "Please take the time to update PyFunceble!\n" + Style.RESET_ALL  # pylint:disable=line-too-long

        print(message)
        exit(1)

    if PyFunceble.VERSION in data["deprecated"]:
        message = Style.BRIGHT + Fore.RED + "Your current version is considered as deprecated.\n" + Style.RESET_ALL  # pylint:disable=line-too-long
        message += Style.BRIGHT + Fore.GREEN + "Please take the time to update PyFunceble!\n" + Style.RESET_ALL  # pylint:disable=line-too-long

        print(message)

    elif data["current_version"] != PyFunceble.VERSION:
        message = Style.BRIGHT + Fore.YELLOW + "Please take the time to update PyFunceble!\n" + Style.RESET_ALL  # pylint:disable=line-too-long
        message += Style.BRIGHT + "Your version: " + Style.RESET_ALL + PyFunceble.VERSION + "\n"
        message += Style.BRIGHT + "Upstream version: " + Style.RESET_ALL + data[
            "current_version"
        ] + "\n"

        print(message)
