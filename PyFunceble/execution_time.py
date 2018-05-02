#!/usr/bin/env python3

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the execution time logic.


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
from PyFunceble import Fore, OrderedDict, Style, strftime


class ExecutionTime(object):  # pylint: disable=too-few-public-methods
    """
    Set and return the exection time of the program.

    Arguments:
        - action: 'start' or 'stop'
        - return_result: bool
            True: we return the execution time.
            False: we return nothing.
    """

    def __init__(self, action="start"):
        if PyFunceble.CONFIGURATION["show_execution_time"] or PyFunceble.CONFIGURATION[
            "travis"
        ]:
            if action == "start":
                self._starting_time()
            elif action == "stop":
                self._stoping_time()

                print(
                    Fore.MAGENTA
                    + Style.BRIGHT
                    + "\nExecution Time: "
                    + self.format_execution_time()
                )

    @classmethod
    def _starting_time(cls): # pragma: no cover
        """
        Set the starting time.
        """

        PyFunceble.CONFIGURATION["start"] = int(strftime("%s"))

    @classmethod
    def _stoping_time(cls): # pragma: no cover
        """
        Set the ending time.
        """

        PyFunceble.CONFIGURATION["end"] = int(strftime("%s"))

    @classmethod
    def _calculate(cls):
        """
        calculate the difference between starting and ending time.

        Returns: dict
            A dics with `days`,`hours`,`minutes` and `seconds`.
        """

        time_difference = PyFunceble.CONFIGURATION["end"] - PyFunceble.CONFIGURATION[
            "start"
        ]

        data = OrderedDict()

        data["days"] = str((time_difference // 24) % 24).zfill(2)
        data["hours"] = str(time_difference // 3600).zfill(2)
        data["minutes"] = str((time_difference % 3600) // 60).zfill(2)
        data["seconds"] = str(time_difference % 60).zfill(2)

        return data

    def format_execution_time(self):
        """
        Format the calculated time into a human readable format.

        Returns: str
            A human readable date.
        """

        result = ""
        calculated_time = self._calculate()
        times = list(calculated_time.keys())

        for time in times:
            result += calculated_time[time]

            if time != times[-1]:
                result += ":"

        return result
