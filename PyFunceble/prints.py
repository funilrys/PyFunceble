#!/usr/bin/env python3

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
    https://pyfunceble.readthedocs.io/en/dev/

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
from PyFunceble.helpers import Dict, File, List
from PyFunceble.sort import Sort


class Prints:
    """
    Print data on screen and into a file if needed.
    Template Possibilities: Percentage, Less, HTTP and any status you want.

    :param to_print: The list of data to print.
    :type to_pritn: list

    :param template:
        The template to use.

        .. note::
            Available templates:

                - :code:`Percentage`
                - :code:`Less`
                - :code:`HTTP`
                - any of the official status.

    :type template: str

    :param output_file: The path to the file to write.
    :type output_file: str

    :param only_on_file:
        Tell us if we only have to print on file and not on screen.
    :type only_on_file: bool
    """

    def __init__(self, to_print, template, output_file=None, only_on_file=False):
        # We get the template.
        self.template = template
        # We get the output.
        self.output = output_file
        # We get the data to print.
        self.data_to_print = to_print
        # We get the state of the only on file.
        self.only_on_file = only_on_file

        # We initiate the variable which will save the list of header.
        # Note: We initiate an Ordered Dict because we want to keep
        # the order.
        self.headers = PyFunceble.OrderedDict()

        # We iniate the Generic header and the spacement of each colomns.
        self.headers["Generic"] = PyFunceble.OrderedDict(
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

        # We iniate the official UP header and the spacement of each colomns.
        self.headers[PyFunceble.STATUS["official"]["up"]] = PyFunceble.OrderedDict(
            zip(
                ["Domain", "Expiration Date", "Source", "HTTP Code", "Analyze Date"],
                [100, 17, 10, 10, 20],
            )
        )

        # We iniate the official VALID header and the spacement of each colomns.
        self.headers[PyFunceble.STATUS["official"]["valid"]] = PyFunceble.OrderedDict(
            zip(["Domain", "Source", "Analyze Date"], [100, 10, 20])
        )

        # We iniate the official DOWN header and the spacement of each colomns.
        self.headers[PyFunceble.STATUS["official"]["down"]] = PyFunceble.OrderedDict(
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

        # We iniate the official INVALID header and the spacement of each colomns.
        self.headers[PyFunceble.STATUS["official"]["invalid"]] = PyFunceble.OrderedDict(
            zip(["Domain", "Source", "HTTP Code", "Analyze Date"], [100, 10, 10, 20])
        )

        # We iniate the official LESS header and the spacement of each colomns.
        self.headers["Less"] = PyFunceble.OrderedDict(
            zip(["Domain", "Status", "HTTP Code"], [100, 11, 10])
        )

        # We iniate the official Percentage header and the spacement of each colomns.
        self.headers["Percentage"] = PyFunceble.OrderedDict(
            zip(["Status", "Percentage", "Numbers"], [11, 12, 12])
        )

        # We iniate the official HTTP header and the spacement of each colomns.
        self.headers["HTTP"] = PyFunceble.OrderedDict(
            zip(["Domain", "Status", "HTTP Code", "Analyze Date"], [100, 11, 10, 20])
        )

        # We initiate a variable which will save the currently in use header.
        self.currently_used_header = {}

    def _before_header(self):
        """
        Print informations about PyFunceble and the date of generation of a file
        into a given path, if doesn't exist.
        """

        if (
            not PyFunceble.CONFIGURATION["no_files"]
            and self.output
            and not PyFunceble.path.isfile(self.output)
        ):
            # * We are allowed to generate files.
            # and
            # * And output is given.
            # and
            # * The given output does not exist.

            # We initiate the information about what generated the file.
            link = "# File generated by %s\n" % PyFunceble.LINKS["repo"]

            # We initiate the information about the generation date of this file.
            date_of_generation = (
                "# Date of generation: %s \n\n" % PyFunceble.CURRENT_TIME
            )

            # We initiate a variable which will save the list of
            # templates which have to meet in order to write the before
            # header informations.
            authorized_templates = [
                "Generic_File",
                PyFunceble.STATUS["official"]["up"],
                PyFunceble.STATUS["official"]["down"],
                PyFunceble.STATUS["official"]["invalid"],
                PyFunceble.STATUS["official"]["valid"],
                "Less",
            ]

            if self.template in authorized_templates:
                # The current header is in our list of authorized templated.

                # We get the header.
                header = (
                    self._header_constructor(self.currently_used_header, None)[0] + "\n"
                )

            try:
                # We try to print the link, the date of generation and the header in the
                # given file.
                File(self.output).write(link + date_of_generation + header)
            except UnboundLocalError:
                # We don't have any header.

                # We print the link and the date in the given file.
                File(self.output).write(link + date_of_generation)

    @classmethod
    def _header_constructor(
        cls, data_to_print, header_separator="-", column_separator=" "
    ):
        """
        Construct header of the table according to template.

        :param data_to_print:
            The list of data to print into the header of the table.
        :type data_to_print: list

        :param header_separator:
            The separator to use between the table header and our data.
        :type header_separator: str

        :param colomn_separator: The separator to use between each colomns.
        :type colomn_separator: str

        :return: The data to print in a list format.
        :rtype: list
        """

        # We initiate a variable which will save the header data.
        header_data = []

        # We initiate a variable which will save the header sizes.
        header_size = ""

        # We initiate the glue to set before the size.
        before_size = "%-"

        # We initiate the glue to set after the size.
        after_size = "s"

        if header_separator:
            # The header separator is not empty.

            # We initiate a variable which will save the list of
            # separator data.
            header_separator_data = []

        # We get the length of the data to print.
        length_data_to_print = len(data_to_print) - 1

        # We initiate an iterator.
        i = 0

        for data in data_to_print:
            # We loop through the list of data.

            # We get the size of the currently read data.
            size = data_to_print[data]

            # We append the data to the header data list.
            header_data.append(data)

            # We construct the header size.
            # Note: our header size is formatted line %s-sizes
            # (the s at the end is part of the formatting.)
            header_size += before_size + str(size) + after_size

            if i < length_data_to_print:
                # The iterator is less than the length of data to print.

                # We append the the colomn separator to the header size.
                header_size += column_separator

            if header_separator:
                # The header separator is given.

                # We append the right size of separator to the list of
                # separator data.
                header_separator_data.append(header_separator * size)

            # We increase the iterator.
            i += 1

        if header_separator:
            # The header separator is given.

            return [
                # We return the formatted header (like we will do with print('%s' % 'hello'))
                header_size % tuple(header_data),
                # We return the formatted header separator.
                header_size % tuple(header_separator_data),
            ]

        # The header separator is not given.

        # We return the formetted header.
        return [header_size % tuple(header_data)]

    def header(
        self, do_not_print=False
    ):  # pragma: no cover pylint: disable=too-many-branches
        """
        Management and creation of templates of header.
        Please consider as "header" the title of each columns.

        :param do_not_print:
            Tell us if we have to print the header or not.
        :type do_not_print: bool
        """

        if (
            not PyFunceble.CONFIGURATION["header_printed"]
            or self.template == "Percentage"
            or do_not_print
        ):
            # * The header has not been already printed.
            # or
            # * The template is the `Percentage template`.
            # or
            # * We are authorized to print something.

            if (
                self.template.lower() in PyFunceble.STATUS["list"]["generic"]
                or self.template == "Generic_File"
            ):
                # * The template is into the list of generic status.
                # or
                # * The template is equal to `Generic_File`.

                # The data to print is the Generic header.
                to_print = self.headers["Generic"]

                if (
                    self.template.lower() in PyFunceble.STATUS["list"]["generic"]
                    and PyFunceble.HTTP_CODE["active"]
                ):
                    # * The template is in the list of generic status.
                    # and
                    # * the http status code extraction is activated.

                    # We remove the Analyze Date colomn from the data to print.
                    to_print = Dict(to_print).remove_key("Analyze Date")
            elif self.template.lower() in PyFunceble.STATUS["list"]["up"]:
                # The template is in the list of up status.

                # We informations to print is the up header.
                to_print = self.headers[PyFunceble.STATUS["official"]["up"]]
            elif self.template.lower() in PyFunceble.STATUS["list"]["valid"]:
                # The template is in the list of valid status.

                # We informations to print is the valid header.
                to_print = self.headers[PyFunceble.STATUS["official"]["valid"]]
            elif self.template.lower() in PyFunceble.STATUS["list"]["down"]:
                # The template is in the list of down status.

                # We informations to print is the down header.
                to_print = self.headers[PyFunceble.STATUS["official"]["down"]]
            elif self.template.lower() in PyFunceble.STATUS["list"]["invalid"]:
                # The template is in the list of invalid status.

                # We informations to print is the invalid header.
                to_print = self.headers[PyFunceble.STATUS["official"]["invalid"]]
            elif (
                self.template == "Less"
                or self.template == "Percentage"
                or self.template == "HTTP"
            ):  # pylint: disable=line-too-long
                # * The template is equal to `Less`.
                # or
                # * The template is equal to `Percentage`.
                # or
                # * The template is equal to `HTTP`.

                # We get the header with the help of the template name.
                to_print = self.headers[self.template]

                if self.template == "Less" and not PyFunceble.HTTP_CODE["active"]:
                    # * The template is equal to `Less`.
                    # and
                    # * The http status code extraction is deactivated.

                    # We append the source index to the header.
                    to_print["Source"] = 10

            if not PyFunceble.HTTP_CODE["active"]:
                # * The http status code extraction is deactivated.

                # We remove the HTTP Code index from the data to print.
                to_print = Dict(to_print).remove_key("HTTP Code")

            # We update the currently used header.
            self.currently_used_header = to_print

            if not do_not_print:
                # We are not authorized to print anything.

                # We generate the before header.
                self._before_header()

                for formatted_template in self._header_constructor(to_print):
                    # We loop through the formatted template.

                    if not self.only_on_file:
                        # We do not have to print only on file.

                        # We print on screen the formatted header template.
                        print(formatted_template)

                    if not PyFunceble.CONFIGURATION["no_files"] and self.output:
                        # An output destination is given.

                        # We write the file with the formatted header template.
                        File(self.output).write(formatted_template + "\n")

    def _data_constructor(self, size):
        """
        Construct the table of data according to given size.

        :param size: The maximal length of each string in the table.
        :type size: list

        :return:
            A dict with all information about the data and how to which what
            maximal size to print it.
        :rtype: OrderedDict

        :raises:
            :code:`Exception`
                If the data and the size does not have the same length.
        """

        # We initiate a variable which will save what we are going to
        # return.
        result = PyFunceble.OrderedDict()

        if len(self.data_to_print) == len(size):
            # The length of the data to print is equal to the length of the given size.

            for i in range(len(self.data_to_print)):
                # We loop until our iterator is less or equal to the length of the data
                # to print.

                # We initiate the result index and its size.
                result[self.data_to_print[i]] = size[i]
        else:
            # This should never happend. If it's happens then there is something
            # wrong from the inputed data.
            raise Exception(
                "Inputed: " + str(len(self.data_to_print)) + "; Size: " + str(len(size))
            )

        # We return the constructed result.
        return result

    @classmethod
    def _size_from_header(cls, header):
        """
        Get the size of each columns from the header.

        :param header:
            The header template we have to get the size from.
        :type header: dict

        :return: The maximal size of the each data to print.
        :rtype: list
        """

        # We initiate the result we are going to return.
        result = []

        for data in header:
            # We lopp through the header.

            # And we append the size to our result.
            result.append(header[data])

        # We return the result.
        return result

    def _colorify(self, data):
        """
        Retun colored string.

        :param data: The string to colorify.
        :type data: str

        :return: A colored string.
        :rtype: str
        """

        if self.template in ["Generic", "Less"]:
            # The template is in the list of template that need the coloration.

            if (
                self.data_to_print[1].lower() in PyFunceble.STATUS["list"]["up"]
                or self.data_to_print[1].lower() in PyFunceble.STATUS["list"]["valid"]
            ):
                # The status is in the list of up status.

                # We print the data with a green background.
                data = PyFunceble.Fore.BLACK + PyFunceble.Back.GREEN + data
            elif self.data_to_print[1].lower() in PyFunceble.STATUS["list"]["down"]:
                # The status is in the list of down status.

                # We print the data with a red background.
                data = PyFunceble.Fore.BLACK + PyFunceble.Back.RED + data
            else:
                # The status is not in the list of up and down status.

                # We print the data with a cyan background.
                data = PyFunceble.Fore.BLACK + PyFunceble.Back.CYAN + data

        # We return the data.
        return data

    def _json_print(self):  # pragma: no cover
        """
        Management of the json template.
        """

        if self.output:
            # The given output is not empty.

            if PyFunceble.path.isfile(self.output):
                # The given output already exist.

                # We get the content of the output.
                content = Dict().from_json(File(self.output).read())

                if isinstance(content, list):
                    # The content is a list.

                    # We extend the content with our data to print.
                    content.extend(self.data_to_print)

                    # We format our list.
                    content = List(content).custom_format(Sort.standard)

                    if PyFunceble.CONFIGURATION["hierarchical_sorting"]:
                        # The hierarchical sorting is activated.

                        # We format our content hierarchicaly
                        content = List(content).custom_format(Sort.hierarchical)

                    # We finally save our content into the file.
                    Dict(content).to_json(self.output)
                else:
                    # The content is not a list.

                    # We raise an exception.
                    raise Exception("Output not correctly formatted.")
            else:
                # The given output does not already exist.

                # We save our data to print into the output.
                #
                # Note: We do not have to take care if self.data_to_print is a list
                # formatted or not because this method should not be called if it is
                # not the case.
                Dict(self.data_to_print).to_json(self.output)
        else:
            # The given output is empty.

            # We raise an exception.
            raise Exception("Empty output given.")

    def data(self):  #  pragma: no cover  pylint: disable=inconsistent-return-statements
        """
        Management and input of data to the table.

        :raises:
            :code:`Exception`
                When self.data_to_print is not a list.
        """

        if isinstance(self.data_to_print, list):
            # The data to print is a list.

            # We initiate the data we are going to print.
            to_print = {}

            # We initiate the size we are going to print.
            to_print_size = []

            # We initiate a variable which will list the list of
            # alone case.
            alone_cases = ["Percentage", "HTTP"]

            # we initiate a variable which will list the list of
            # template which does not need a header.
            without_header = ["FullHosts", "PlainDomain"]

            if self.template.lower() == "json":
                # The template is the json template.
                return self._json_print()

            if self.template not in alone_cases and self.template not in without_header:
                # * The template is not in the list of alone case.
                # and
                # * THe template is not in the list of template without header.

                # We get the template we should use.
                # Note: We basically only need the self.currently_used_header to be filled.
                self.header(True)

                # And we get the size from the header.
                to_print_size = self._size_from_header(self.currently_used_header)
            elif self.template in without_header:
                # The template is in the list of template which does not need a header.

                for data in self.data_to_print:
                    # We loop through the list of data to print.

                    # And we construct the (spacement) size of the data to print.
                    to_print_size.append(str(len(data)))
            else:
                # We get the size from the given template name.
                to_print_size = self._size_from_header(self.headers[self.template])

            # We construct and format the data to print.
            to_print = self._data_constructor(to_print_size)

            # We print the before header section.
            self._before_header()

            for data in self._header_constructor(to_print, False):
                # We loop through the formatted data.

                if self.template.lower() in PyFunceble.STATUS["list"][
                    "generic"
                ] or self.template in ["Less", "Percentage"]:
                    # * The template is in the list of generic status.
                    # or
                    # * The template is in a specific list.

                    if not self.only_on_file:
                        # We are authorized to print on screen.

                        # We colorify the data to print.
                        colorified_data = self._colorify(data)

                        # And we print the data.
                        print(colorified_data)
                if not PyFunceble.CONFIGURATION["no_files"] and self.output:
                    # * We are authorized to print on any file.
                    # and
                    # * The output is given.

                    # We write our data into the printed file.
                    File(self.output).write(data + "\n")
        else:
            # This should never happend. If it's happens then there's a big issue
            # around data_to_print.
            raise Exception("Please review Prints().data()")
