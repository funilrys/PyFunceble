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

This submodule will provide the execution time logic.

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
    def _starting_time(cls):  # pragma: no cover
        """
        Set the starting time.
        """

        PyFunceble.CONFIGURATION["start"] = int(strftime("%s"))

    @classmethod
    def _stoping_time(cls):  # pragma: no cover
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
