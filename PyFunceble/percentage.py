#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check domains or IP availability.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

This submodule will provide the percentage logic and interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


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
# pylint: enable=line-too-long
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
        elif PyFunceble.CONFIGURATION["counter"]["number"]["tested"] > 0:
            self._calculate()
