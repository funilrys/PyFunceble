"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the percentage interface.

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


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import PyFunceble


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
            PyFunceble.INTERN["counter"]["number"].update(init)

    def count(self):
        """
        Count the number of domain for each status.
        """

        if self.status:
            # The status is parsed.

            # We increase the number of tested.
            PyFunceble.INTERN["counter"]["number"]["tested"] += 1

            if (
                self.status.lower() in PyFunceble.STATUS.list.up
                or self.status.lower() in PyFunceble.STATUS.list.valid
                or self.status.lower() in PyFunceble.STATUS.list.sane
            ):
                # The status is in the list of up status.

                # We increase the number of up.
                PyFunceble.INTERN["counter"]["number"]["up"] += 1
            elif (
                self.status.lower() in PyFunceble.STATUS.list.down
                or self.status.lower() in PyFunceble.STATUS.list.malicious
            ):
                # The status is in the list of down status.

                # We increase the number of down.
                PyFunceble.INTERN["counter"]["number"]["down"] += 1
            else:
                # The status is not in the list of up nor down status.

                # We increase the number of invalid.
                PyFunceble.INTERN["counter"]["number"]["invalid"] += 1

    @classmethod
    def calculate(cls):
        """
        Calculate the percentage of each status.
        """

        PyFunceble.INTERN["counter"]["percentage"] = {}

        # We map the current state/counters of the different status.
        percentages = {
            x: PyFunceble.INTERN["counter"]["number"][x]
            for x in PyFunceble.STATUS.official.keys()
            if x in PyFunceble.INTERN["counter"]["number"]
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

        # raise Exception(PyFunceble.INTERN["counter"]["percentage"])

    def log(self):
        """
        Print on screen and on file the percentages for each status.
        """

        if (
            PyFunceble.CONFIGURATION.show_percentage
            and PyFunceble.INTERN["counter"]["number"]["tested"] > 0
        ):
            # * We are allowed to show the percentage on screen.
            # and
            # * The number of tested is greater than 0.

            # We initiate the output file.
            output = (
                PyFunceble.OUTPUT_DIRECTORY
                + PyFunceble.OUTPUTS.parent_directory
                + PyFunceble.OUTPUTS.logs.directories.parent
                + PyFunceble.OUTPUTS.logs.directories.percentage
                + PyFunceble.OUTPUTS.logs.filenames.percentage
            )

            # We delete the output file if it does exist.
            PyFunceble.helpers.File(output).delete()

            # We calculate the percentage of each statuses.
            self.calculate()

            # We construct the different lines/data to print on screen and file.
            lines_to_print = [
                [
                    PyFunceble.STATUS.official.up,
                    str(PyFunceble.INTERN["counter"]["percentage"]["up"]) + "%",
                    PyFunceble.INTERN["counter"]["number"]["up"],
                ],
                [
                    PyFunceble.STATUS.official.down,
                    str(PyFunceble.INTERN["counter"]["percentage"]["down"]) + "%",
                    PyFunceble.INTERN["counter"]["number"]["down"],
                ],
                [
                    PyFunceble.STATUS.official.invalid,
                    str(PyFunceble.INTERN["counter"]["percentage"]["invalid"]) + "%",
                    PyFunceble.INTERN["counter"]["number"]["invalid"],
                ],
            ]

            if PyFunceble.CONFIGURATION.syntax:
                # We are checking for syntax.

                # We update the denomination of the UP.
                lines_to_print[0][0] = PyFunceble.STATUS.official.valid
                lines_to_print[0][1] = (
                    str(PyFunceble.INTERN["counter"]["percentage"]["valid"]) + "%"
                )

                lines_to_print[0][2] = PyFunceble.INTERN["counter"]["number"]["valid"]

                # And we unset the INACTIVE line.
                del lines_to_print[1]
                del PyFunceble.INTERN["counter"]["number"]["down"]
                del PyFunceble.INTERN["counter"]["number"]["up"]

            if PyFunceble.CONFIGURATION.reputation:
                # We are checking for reputation.

                # We update the denomination of the UP.
                lines_to_print[0][0] = PyFunceble.STATUS.official.sane
                lines_to_print[0][1] = (
                    str(PyFunceble.INTERN["counter"]["percentage"]["sane"]) + "%"
                )

                lines_to_print[0][2] = PyFunceble.INTERN["counter"]["number"]["sane"]

                # We update the denomination of the Down.
                lines_to_print[1][0] = PyFunceble.STATUS.official.malicious
                lines_to_print[1][1] = (
                    str(PyFunceble.INTERN["counter"]["percentage"]["malicious"]) + "%"
                )
                lines_to_print[1][2] = PyFunceble.INTERN["counter"]["number"][
                    "malicious"
                ]

                # And we unset the INVALID line.
                del lines_to_print[2]
                del PyFunceble.INTERN["counter"]["number"]["invalid"]
                del PyFunceble.INTERN["counter"]["number"]["up"]
                del PyFunceble.INTERN["counter"]["number"]["down"]

            if (
                not PyFunceble.CONFIGURATION.quiet
                and not PyFunceble.CONFIGURATION.simple
            ):
                # * The quiet mode is not activated.
                # or
                # * We are testing in simple mode.

                # We print a new line.
                print("\n")

                # We print the percentage header on file and screen.
                PyFunceble.output.Prints(None, "Percentage", output).header()

                for to_print in lines_to_print:
                    # We loop throught the different line to print.
                    # (one line for each status.)

                    # And we print the current status line on file and screen.
                    PyFunceble.output.Prints(to_print, "Percentage", output).data()
            else:  # pragma: no cover
                # The quiet mode is activated.

                # We print the percentage header on file.
                PyFunceble.output.Prints(
                    None, "Percentage", output, only_on_file=True
                ).header()

                for to_print in lines_to_print:
                    # We loop throught the different line to print.
                    # (one line for each status.)

                    # And we print the current status line on file.
                    PyFunceble.output.Prints(
                        to_print, "Percentage", output, only_on_file=True
                    ).data()

        elif PyFunceble.INTERN["counter"]["number"]["tested"] > 0:
            # * We are not allowed to show the percentage on screen.
            # but
            # * The number of tested is greater than 0.

            # We run the calculation.
            # Note: The following is needed, because all counter calculation are
            # done by this class.
            self.calculate()
