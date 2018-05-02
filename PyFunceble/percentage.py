#!/usr/bin/env python3

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the percentage logic and interface.


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on March 13th, 2018.
At the end of 2017, PyFunceble was described by one of its most active user as:
"[an] excellent script for checking ACTIVE and INACTIVE domain names."

Our main objective is to test domains and IP availability
by generating an accurate result based on results from WHOIS, NSLOOKUP and
HTTP status codes.
As result, PyFunceble returns 3 status: ACTIVE, INACTIVE and INVALID.
The denomination of those statuses can be changed under your personal
`config.yaml`.

At the time we write this, PyFunceble is running actively and daily under 50+
Travis CI repository or process to test the availability of domains which are
present into hosts files, AdBlock filter lists, list of IP, list of domains or
blocklists.

An up to date explanation of all status can be found at https://git.io/vxieo.
You can also find a simple representation of the logic behind PyFunceble at
https://git.io/vxifw.

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
from PyFunceble.helpers import File
from PyFunceble.prints import Prints


class Percentage(object):
    """
    Calculation of the percentage of each status.

    Arguments:
        - domain_status: str
            The status to increment.
        - init: None or dict
            None: we start from 0.
            dict: we start from the passed data.
    """

    def __init__(self, domain_status=None, init=None):
        self.status = domain_status

        if init and isinstance(init, dict):
            for data in init:
                PyFunceble.CONFIGURATION["counter"]["percentage"].update(
                    {data: init[data]}
                )

    def count(self):
        """
        Count the number of domain for each status.
        """

        if self.status:
            PyFunceble.CONFIGURATION["counter"]["number"]["tested"] += 1

            if self.status.lower() in PyFunceble.STATUS["list"]["up"]:
                PyFunceble.CONFIGURATION["counter"]["number"]["up"] += 1
            elif self.status.lower() in PyFunceble.STATUS["list"]["down"]:
                PyFunceble.CONFIGURATION["counter"]["number"]["down"] += 1
            else:
                PyFunceble.CONFIGURATION["counter"]["number"]["invalid"] += 1

    @classmethod
    def _calculate(cls):
        """
        Calculate the percentage of each status.
        """

        percentages = {
            "up": PyFunceble.CONFIGURATION["counter"]["number"]["up"],
            "down": PyFunceble.CONFIGURATION["counter"]["number"]["down"],
            "invalid": PyFunceble.CONFIGURATION["counter"]["number"]["invalid"],
        }

        for percentage in percentages:
            calculation = percentages[percentage] * 100 // PyFunceble.CONFIGURATION[
                "counter"
            ][
                "number"
            ][
                "tested"
            ]
            PyFunceble.CONFIGURATION["counter"]["percentage"].update(
                {percentage: calculation}
            )

    def log(self):
        """
        Print on screen and on file the percentages for each status.
        """

        if PyFunceble.CONFIGURATION["show_percentage"] and PyFunceble.CONFIGURATION[
            "counter"
        ][
            "number"
        ][
            "tested"
        ] > 0:
            output = PyFunceble.CURRENT_DIRECTORY + PyFunceble.OUTPUTS[
                "parent_directory"
            ] + PyFunceble.OUTPUTS[
                "logs"
            ][
                "directories"
            ][
                "parent"
            ] + PyFunceble.OUTPUTS[
                "logs"
            ][
                "directories"
            ][
                "percentage"
            ] + PyFunceble.OUTPUTS[
                "logs"
            ][
                "filenames"
            ][
                "percentage"
            ]
            File(output).delete()

            self._calculate()

            if not PyFunceble.CONFIGURATION["quiet"]:
                print("\n")
                Prints(None, "Percentage", output).header()

                for to_print in [
                    [
                        PyFunceble.STATUS["official"]["up"],
                        str(PyFunceble.CONFIGURATION["counter"]["percentage"]["up"])
                        + "%",
                        PyFunceble.CONFIGURATION["counter"]["number"]["up"],
                    ],
                    [
                        PyFunceble.STATUS["official"]["down"],
                        str(PyFunceble.CONFIGURATION["counter"]["percentage"]["down"])
                        + "%",
                        PyFunceble.CONFIGURATION["counter"]["number"]["down"],
                    ],
                    [
                        PyFunceble.STATUS["official"]["invalid"],
                        str(
                            PyFunceble.CONFIGURATION["counter"]["percentage"]["invalid"]
                        )
                        + "%",
                        PyFunceble.CONFIGURATION["counter"]["number"]["invalid"],
                    ],
                ]:
                    Prints(to_print, "Percentage", output).data()
