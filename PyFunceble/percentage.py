# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the percentage logic and interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

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
import PyFunceble
from PyFunceble.helpers import File
from PyFunceble.prints import Prints


class Percentage:
    """
    Calculation of the percentage of each status.

    :param str domain_status: The status to increment.
    :param dict init:
        The data from a previous session we are continuing.

        .. warning::
            We expect the numbers and not the percentages.
    """

    def __init__(self, domain_status=None, init=None):
        # We get the status.
        self.status = domain_status

        if init and isinstance(init, dict):
            # * An information to init is given.
            # and
            # * It is a dictionnary.

            # We update the counter from the currently read data.
            PyFunceble.INTERN["counter"]["number"].update(
                {x: y for x, y in init.items()}
            )

    def count(self):
        """
        Count the number of domain for each status.
        """

        if self.status:
            # The status is parsed.

            # We increase the number of tested.
            PyFunceble.INTERN["counter"]["number"]["tested"] += 1

            if (
                self.status.lower() in PyFunceble.STATUS["list"]["up"]
                or self.status.lower() in PyFunceble.STATUS["list"]["valid"]
            ):
                # The status is in the list of up status.

                # We increase the number of up.
                PyFunceble.INTERN["counter"]["number"]["up"] += 1
            elif self.status.lower() in PyFunceble.STATUS["list"]["down"]:
                # The status is in the list of down status.

                # We increase the number of down.
                PyFunceble.INTERN["counter"]["number"]["down"] += 1
            else:
                # The status is not in the list of up nor down status.

                # We increase the number of invalid.
                PyFunceble.INTERN["counter"]["number"]["invalid"] += 1

    @classmethod
    def _calculate(cls):
        """
        Calculate the percentage of each status.
        """

        PyFunceble.INTERN["counter"]["percentage"] = {}

        # We map the current state/counters of the different status.
        percentages = {
            "up": PyFunceble.INTERN["counter"]["number"]["up"],
            "down": PyFunceble.INTERN["counter"]["number"]["down"],
            "invalid": PyFunceble.INTERN["counter"]["number"]["invalid"],
        }

        for percentage in percentages:
            # We loop through our map index.

            # We calculate the percentage.
            calculation = (
                percentages[percentage]
                * 100
                // PyFunceble.INTERN["counter"]["number"]["tested"]
            )

            # And we update the percentage counter of the actual status.
            PyFunceble.INTERN["counter"]["percentage"].update({percentage: calculation})

    def log(self):
        """
        Print on screen and on file the percentages for each status.
        """

        if (
            PyFunceble.CONFIGURATION["show_percentage"]
            and PyFunceble.INTERN["counter"]["number"]["tested"] > 0
        ):
            # * We are allowed to show the percentage on screen.
            # and
            # * The number of tested is greater than 0.

            # We initiate the output file.
            output = (
                PyFunceble.OUTPUT_DIRECTORY
                + PyFunceble.OUTPUTS["parent_directory"]
                + PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
                + PyFunceble.OUTPUTS["logs"]["directories"]["percentage"]
                + PyFunceble.OUTPUTS["logs"]["filenames"]["percentage"]
            )

            # We delete the output file if it does exist.
            File(output).delete()

            # We calculate the percentage of each statuses.
            self._calculate()

            # We construct the different lines/data to print on screen and file.
            lines_to_print = [
                [
                    PyFunceble.STATUS["official"]["up"],
                    str(PyFunceble.INTERN["counter"]["percentage"]["up"]) + "%",
                    PyFunceble.INTERN["counter"]["number"]["up"],
                ],
                [
                    PyFunceble.STATUS["official"]["down"],
                    str(PyFunceble.INTERN["counter"]["percentage"]["down"]) + "%",
                    PyFunceble.INTERN["counter"]["number"]["down"],
                ],
                [
                    PyFunceble.STATUS["official"]["invalid"],
                    str(PyFunceble.INTERN["counter"]["percentage"]["invalid"]) + "%",
                    PyFunceble.INTERN["counter"]["number"]["invalid"],
                ],
            ]

            if PyFunceble.CONFIGURATION["syntax"]:
                # We are checking for syntax.

                # We update the denomination of the UP.
                lines_to_print[0][0] = PyFunceble.STATUS["official"]["valid"]

                # And we unset the INACTIVE line.
                del lines_to_print[1]

            if (
                not PyFunceble.CONFIGURATION["quiet"]
                or PyFunceble.CONFIGURATION["simple"]
            ):
                # * The quiet mode is not activated.
                # or
                # * We are testing in simple mode.

                # We print a new line.
                print("\n")

                # We print the percentage header on file and screen.
                Prints(None, "Percentage", output).header()

                for to_print in lines_to_print:
                    # We loop throught the different line to print.
                    # (one line for each status.)

                    # And we print the current status line on file and screen.
                    Prints(to_print, "Percentage", output).data()
            else:  # pragma: no cover
                # The quiet mode is activated.

                # We print the percentage header on file.
                Prints(None, "Percentage", output, only_on_file=True).header()

                for to_print in lines_to_print:
                    # We loop throught the different line to print.
                    # (one line for each status.)

                    # And we print the current status line on file.
                    Prints(to_print, "Percentage", output, only_on_file=True).data()

        elif PyFunceble.INTERN["counter"]["number"]["tested"] > 0:
            # * We are not allowed to show the percentage on screen.
            # but
            # * The number of tested is greater than 0.

            # We run the calculation.
            # Note: The following is needed, because all counter calculation are
            # done by this class.
            self._calculate()
