#!/usr/bin/env python3

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the production logic. We understand by production login
the logic to apply before commiting new code.


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

import PyFunceble
from PyFunceble import Fore, Style
from PyFunceble.config import Version
from PyFunceble.directory_structure import DirectoryStructure
from PyFunceble.helpers import Dict, File


class Production(object):  # pylint: disable=too-few-public-methods
    """
    This class will manage and provide the production logic.
    """

    def __init__(self):
        self.data_version_yaml = self._get_current_version_yaml()

        self.version_yaml = Version(True).split_versions(
            self.data_version_yaml["current_version"]
        )
        self.current_version = Version(True).split_versions(PyFunceble.VERSION, True)

        if self._is_version_greater():
            DirectoryStructure(production=True)

            if self._does_require_deprecation():
                to_deprecate = ".".join(self.version_yaml)

                self.data_version_yaml["deprecated"].append(to_deprecate)

            if self._does_require_force_update():
                to_force_update = ".".join(self.version_yaml)

                self.data_version_yaml["force_update"]["minimal_version"].append(
                    to_force_update
                )

            if self.current_version[-1]:
                self.current_version[0].append(self.current_version[-1])

            self.data_version_yaml["current_version"] = ".".join(
                self.current_version[0]
            )

            Dict(self.data_version_yaml).to_yaml(
                PyFunceble.CURRENT_DIRECTORY + "version.yaml"
            )

            message = Fore.GREEN + Style.BRIGHT + "We are ready to ship!! \n"
            message += Fore.CYAN + "Please do not touch version.yaml nor setup.py (version update)"

            print(message)
            exit(0)
        else:
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + "Are you sure that you did some changes ? Please update PyFunceble.VERSION if it is the case."  # pylint: disable=line-too-long
            )
            exit(1)

    @classmethod
    def _get_current_version_yaml(cls):
        """
        This method get and return the content of version.yaml
        """

        return Dict().from_yaml(
            File(PyFunceble.CURRENT_DIRECTORY + "version.yaml").read()
        )

    def _is_version_greater(self):
        """
        This method check if the current version is greater as the older older one.
        """

        checked = Version(True).check_versions(
            self.current_version[0], self.version_yaml
        )

        if checked != None and not checked:
            return True

        return False

    def _does_require_deprecation(self):
        """
        This method check if we have to put the previous version into the deprecated list.
        """

        for index, version_number in enumerate(self.current_version[0][:2]):
            if version_number > self.version_yaml[index]:
                return True

        return False

    def _does_require_force_update(self):
        """
        This method check if we have to put the previsous verion into the list of minimal version
        for force_update.
        """

        if self.current_version[0][0] > self.version_yaml[0]:
            return True

        return False
