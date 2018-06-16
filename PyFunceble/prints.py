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

This submodule will provide the printing interface and logic.

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
from PyFunceble import Back, Fore, OrderedDict, path
from PyFunceble.helpers import Dict, File


class Prints(object):
    """
    Print data on screen and into a file if needed.
    Template Possibilities: Percentage, Less, HTTP and any status you want.

    Arguments:
        - to_print: list
            The list of data to print.
        - template: str
            The template to use.
        - output_file: str
            The path to the file to write.
        - only_on_file: bool
            True: We don't print data on screen.
            False: We print data on screen.
    """

    def __init__(self, to_print, template, output_file=None, only_on_file=False):
        self.template = template
        self.output = output_file
        self.data_to_print = to_print
        self.only_on_file = only_on_file

        self.headers = OrderedDict()

        self.headers["Generic"] = OrderedDict(
            zip(
                [
                    "Domain",
                    "Status",
                    "Expiration Date",
                    "Source",
                    "HTTP Code",
                    "Analyze Date",
                ],
                [100, 11, 17, 10, 10, 20],
            )
        )

        self.headers[PyFunceble.STATUS["official"]["up"]] = OrderedDict(
            zip(
                ["Domain", "Expiration Date", "Source", "HTTP Code", "Analyze Date"],
                [100, 17, 10, 10, 20],
            )
        )

        self.headers[PyFunceble.STATUS["official"]["down"]] = OrderedDict(
            zip(
                [
                    "Domain",
                    "WHOIS Server",
                    "Status",
                    "Source",
                    "HTTP Code",
                    "Analyze Date",
                ],
                [100, 35, 11, 10, 10, 20],
            )
        )

        self.headers[PyFunceble.STATUS["official"]["invalid"]] = OrderedDict(
            zip(["Domain", "Source", "HTTP Code", "Analyze Date"], [100, 10, 10, 20])
        )

        self.headers["Less"] = OrderedDict(
            zip(["Domain", "Status", "HTTP Code"], [100, 11, 10])
        )

        self.headers["Percentage"] = OrderedDict(
            zip(["Status", "Percentage", "Numbers"], [11, 12, 12])
        )

        self.headers["HTTP"] = OrderedDict(
            zip(["Domain", "Status", "HTTP Code", "Analyze Date"], [100, 11, 10, 20])
        )

        self.currently_used_header = {}

    def _before_header(self):
        """
        Print informations about PyFunceble and the date of generation of a file
        into a given path, if doesn't exist.
        """

        if not PyFunceble.CONFIGURATION["no_files"] and self.output and not path.isfile(
            self.output
        ):
            link = ("# File generated with %s\n" % PyFunceble.LINKS["repo"])
            date_of_generation = (
                "# Date of generation: %s \n\n" % PyFunceble.CURRENT_TIME
            )

            if self.template in [
                "Generic_File",
                PyFunceble.STATUS["official"]["up"],
                PyFunceble.STATUS["official"]["down"],
                PyFunceble.STATUS["official"]["invalid"],
                "Less",
            ]:
                header = self._header_constructor(self.currently_used_header, None)[
                    0
                ] + "\n"

            try:
                File(self.output).write(link + date_of_generation + header)
            except UnboundLocalError:
                File(self.output).write(link + date_of_generation)

    @classmethod
    def _header_constructor(cls, data_to_print, separator="-"):
        """
        Construct header of the table according to template.

        Arguments:
            - data_to_print: list
                The list of data to print into the header.
            - separator: str
                The separator to use for the table header generation.

        Returns: list
            The data to print in list format.
        """

        header_data = []
        header_size = ""
        before_size = "%-"
        after_size = "s "

        if separator:
            separator_data = []

        for data in data_to_print:
            size = data_to_print[data]
            header_data.append(data)

            header_size += before_size + str(size) + after_size

            if separator:
                separator_data.append(separator * size)

        if separator:
            return [
                header_size % tuple(header_data), header_size % tuple(separator_data)
            ]

        return [header_size % tuple(header_data)]

    def header(
        self, do_not_print=False
    ):  # pragma: no cover # pylint: disable=too-many-branches
        """
        Management and creation of templates of header.
        Please consider as "header" the title of each columns.
        """

        if not PyFunceble.CONFIGURATION[
            "header_printed"
        ] or self.template == "Percentage" or do_not_print:
            if self.template.lower() in PyFunceble.STATUS["list"][
                "generic"
            ] or self.template == "Generic_File":
                to_print = self.headers["Generic"]

                if self.template.lower() in PyFunceble.STATUS["list"][
                    "generic"
                ] and PyFunceble.HTTP_CODE[
                    "active"
                ]:
                    to_print = Dict(to_print).remove_key("Analyze Date")
            if self.template.lower() in PyFunceble.STATUS["list"]["up"]:
                to_print = self.headers[PyFunceble.STATUS["official"]["up"]]
            elif self.template.lower() in PyFunceble.STATUS["list"]["down"]:
                to_print = self.headers[PyFunceble.STATUS["official"]["down"]]
            elif self.template.lower() in PyFunceble.STATUS["list"]["invalid"]:
                to_print = self.headers[PyFunceble.STATUS["official"]["invalid"]]
            elif self.template == "Less" or self.template == "Percentage" or self.template == "HTTP":  # pylint: disable=line-too-long
                to_print = self.headers[self.template]

                if self.template == "Less" and not PyFunceble.HTTP_CODE["active"]:
                    to_print["Source"] = 10

            if not PyFunceble.HTTP_CODE["active"]:
                to_print = Dict(to_print).remove_key("HTTP Code")

            self.currently_used_header = to_print

            if not do_not_print:
                self._before_header()
                for formated_template in self._header_constructor(to_print):
                    if not self.only_on_file:
                        print(formated_template)
                    if self.output:
                        File(self.output).write(formated_template + "\n")

    def _data_constructor(self, size):
        """
        Construct the table of data according to given size.

        Argument:
            - size: list
                The maximal length of each string in the table.

        Returns: OrderedDict
            An dict with all information about the data and how to which what
            maximal size to print it.

        Raise:
            - Exception: if the data and the size does not have the same length.
        """

        result = OrderedDict()
        if len(self.data_to_print) == len(size):
            for i in range(len(self.data_to_print)):
                result[self.data_to_print[i]] = size[i]
        else:
            # This should never happend. If it's happens then there is something
            # wrong from the inputed data.
            raise Exception(
                "Inputed: " + str(len(self.data_to_print)) + "; Size: " + str(len(size))
            )

        return result

    @classmethod
    def _size_from_header(cls, header):
        """
        Get the size of each columns from the header.

        Argument:
            - header_type: dict
                The header we have to get the size from.

        Returns: list
            The maximal size of the each data to print.
        """

        result = []

        for data in header:
            result.append(header[data])

        return result

    def _colorify(self, data):
        """
        Retun colored string.

        Argument:
            - data: str
                The string to colorify.

        Returns: str
            A colored string.
        """

        if self.template in ["Generic", "Less"]:
            if self.data_to_print[1].lower() in PyFunceble.STATUS["list"]["up"]:
                data = Fore.BLACK + Back.GREEN + data
            elif self.data_to_print[1].lower() in PyFunceble.STATUS["list"]["down"]:
                data = Fore.BLACK + Back.RED + data
            else:
                data = Fore.BLACK + Back.CYAN + data
        return data

    def data(self):  # pragma: no cover
        """
        Management and input of data to the table.

        Raise:
            - Exception: When self.data_to_print is not a list.
        """

        if isinstance(self.data_to_print, list):
            to_print = {}
            to_print_size = []

            alone_cases = ["Percentage", "HTTP"]
            without_header = ["FullHosts", "PlainDomain"]

            if self.template not in alone_cases and self.template not in without_header:
                self.header(True)
                to_print_size = self._size_from_header(self.currently_used_header)
            elif self.template in without_header:
                for data in self.data_to_print:
                    to_print_size.append(str(len(data)))
            else:
                to_print_size = self._size_from_header(self.headers[self.template])

            to_print = self._data_constructor(to_print_size)

            self._before_header()

            for data in self._header_constructor(to_print, False):
                if self.template.lower() in PyFunceble.STATUS["list"][
                    "generic"
                ] or self.template in [
                    "Less", "Percentage"
                ]:
                    if not self.only_on_file:
                        data = self._colorify(data)
                        print(data)
                if not PyFunceble.CONFIGURATION["no_files"] and self.output:
                    File(self.output).write(data + "\n")
        else:
            # This should never happend. If it's happens then there's a big issue
            # around data_to_print.
            raise Exception("Please review Prints().data()")
