"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the printing interface.

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

from collections import OrderedDict
from datetime import datetime

from colorama import Back, Fore, Style

import PyFunceble


class Prints:
    """
    Print data on screen and into a file if needed.
    Template Possibilities: Percentage, Less, HTTP and any status you want.

    :param list to_print: The list of data to print.

    :param str template:
        The template to use.

        .. note::
            Available templates:

                - :code:`Percentage`
                - :code:`Less`
                - :code:`HTTP`
                - any of the official status.

    :param str output_file: The path to the file to write.

    :param bool only_on_file:
        Tell us if we only have to print on file and not on screen.
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
        self.headers = OrderedDict()

        PyFunceble.LOGGER.debug(f"Template: {self.template}")
        PyFunceble.LOGGER.debug(f"Destination: {self.output}")
        PyFunceble.LOGGER.debug(f"Data to print:\n{self.data_to_print}")
        PyFunceble.LOGGER.debug(f"Only print on file: {self.only_on_file}")

        # We iniate the Generic header and the spacement of each colomns.
        self.headers["Generic"] = OrderedDict(
            zip(
                [
                    "Subject",
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
        self.headers[PyFunceble.STATUS.official.up] = OrderedDict(
            zip(
                ["Subject", "Expiration Date", "Source", "HTTP Code", "Analyze Date"],
                [100, 17, 10, 10, 20],
            )
        )

        # We iniate the official VALID header and the spacement of each colomns.
        self.headers[PyFunceble.STATUS.official.valid] = OrderedDict(
            zip(["Subject", "Source", "Analyze Date"], [100, 10, 20])
        )

        # We iniate the official SANE header and the spacement of each colomns.
        self.headers[PyFunceble.STATUS.official.sane] = OrderedDict(
            zip(["Subject", "Source", "Analyze Date"], [100, 10, 20])
        )

        # We iniate the official MALICIOUS header and the spacement of each colomns.
        self.headers[PyFunceble.STATUS.official.malicious] = OrderedDict(
            zip(["Subject", "Source", "Analyze Date"], [100, 10, 20])
        )

        # We iniate the official DOWN header and the spacement of each colomns.
        self.headers[PyFunceble.STATUS.official.down] = OrderedDict(
            zip(
                [
                    "Subject",
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
        self.headers[PyFunceble.STATUS.official.invalid] = OrderedDict(
            zip(["Subject", "Source", "HTTP Code", "Analyze Date"], [100, 10, 10, 20])
        )

        # We iniate the official LESS header and the spacement of each colomns.
        self.headers["Less"] = OrderedDict(
            zip(["Subject", "Status", "HTTP Code"], [100, 11, 10])
        )

        try:
            # We iniate the official Simple header and the spacement of each colomns.
            self.headers["Simple"] = OrderedDict(
                zip(["Subject", "Status"], [len(self.data_to_print[0]), 11])
            )
        except TypeError:
            pass

        # We iniate the official Percentage header and the spacement of each colomns.
        self.headers["Percentage"] = OrderedDict(
            zip(["Status", "Percentage", "Numbers"], [11, 12, 12])
        )

        # We iniate the official HTTP header and the spacement of each colomns.
        self.headers["HTTP"] = OrderedDict(
            zip(["Subject", "Status", "HTTP Code", "Analyze Date"], [100, 11, 10, 20])
        )

        # We initiate a variable which will save the currently in use header.
        self.currently_used_header = {}

        # We initate a instance of the file output.
        self.file_output_instance = PyFunceble.helpers.File(self.output)

    def before_header(self):
        """
        Print informations about PyFunceble and the date of generation of a file
        into a given path, if doesn't exist.
        """

        if (
            not PyFunceble.CONFIGURATION.no_files
            and self.output
            and not self.file_output_instance.exists()
        ):

            # * We are allowed to generate files.
            # and
            # * And output is given.
            # and
            # * The given output does not exist.

            # We initiate the information about what generated the file.
            link = "# Generated by {0} (v{1}) / {2}\n".format(
                PyFunceble.NAME,
                PyFunceble.VERSION.split()[0],
                PyFunceble.abstracts.Infrastructure.REPO_LINK,
            )

            # We initiate the information about the generation date of this file.
            date_of_generation = (
                "# Date of generation: %s\n\n" % datetime.now().isoformat()
            )

            # We initiate a variable which will save the list of
            # templates which have to meet in order to write the before
            # header informations.
            authorized_templates = [
                "Generic_File",
                PyFunceble.STATUS.official.up,
                PyFunceble.STATUS.official.down,
                PyFunceble.STATUS.official.invalid,
                PyFunceble.STATUS.official.valid,
                PyFunceble.STATUS.official.sane,
                PyFunceble.STATUS.official.malicious,
                "Less",
            ]

            if self.template in authorized_templates:
                # The current header is in our list of authorized templated.

                # We get the header.
                header = (
                    self.header_constructor(self.currently_used_header, None)[0] + "\n"
                )

                PyFunceble.LOGGER.debug(f"HEADER: {header}")

            try:
                # We try to print the link, the date of generation and the header in the
                # given file.
                self.file_output_instance.write(link + date_of_generation + header)
            except UnboundLocalError:
                # We don't have any header.

                # We print the link and the date in the given file.
                self.file_output_instance.write(link + date_of_generation)

            PyFunceble.LOGGER.info(
                f"Created the {self.file_output_instance.path} file with the header."
            )

    @classmethod
    def header_constructor(
        cls, data_to_print, header_separator="-", column_separator=" "
    ):
        """
        Construct header of the table according to template.

        :param list data_to_print:
            The list of data to print into the header of the table.

        :param str header_separator:
            The separator to use between the table header and our data.

        :param str colomn_separator: The separator to use between each colomns.

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

        :param bool do_not_print:
            Tell us if we have to print the header or not.
        """

        if (
            not PyFunceble.CONFIGURATION.header_printed
            or self.template == "Percentage"
            or do_not_print
        ):
            # * The header has not been already printed.
            # or
            # * The template is the `Percentage template`.
            # or
            # * We are authorized to print something.

            if (
                self.template.lower() in PyFunceble.STATUS.list.generic
                or self.template == "Generic_File"
            ):
                # * The template is into the list of generic status.
                # or
                # * The template is equal to `Generic_File`.

                # The data to print is the Generic header.
                to_print = self.headers["Generic"]

                if (
                    self.template.lower() in PyFunceble.STATUS.list.generic
                    and PyFunceble.HTTP_CODE.active
                ):
                    # * The template is in the list of generic status.
                    # and
                    # * the http status code extraction is activated.

                    # We remove the Analyze Date colomn from the data to print.
                    to_print = PyFunceble.helpers.Dict(to_print).remove_key(
                        "Analyze Date"
                    )
            elif self.template.lower() in PyFunceble.STATUS.list.up:
                # The template is in the list of up status.

                # We informations to print is the up header.
                to_print = self.headers[PyFunceble.STATUS.official.up]
            elif self.template.lower() in PyFunceble.STATUS.list.valid:
                # The template is in the list of valid status.

                # We informations to print is the valid header.
                to_print = self.headers[PyFunceble.STATUS.official.valid]
            elif self.template.lower() in PyFunceble.STATUS.list.sane:
                # The template is in the list of sane status.

                # We informations to print is the sane header.
                to_print = self.headers[PyFunceble.STATUS.official.sane]
            elif self.template.lower() in PyFunceble.STATUS.list.malicious:
                # The template is in the list of malicious status.

                # We informations to print is the malicious header.
                to_print = self.headers[PyFunceble.STATUS.official.malicious]
            elif self.template.lower() in PyFunceble.STATUS.list.down:
                # The template is in the list of down status.

                # We informations to print is the down header.
                to_print = self.headers[PyFunceble.STATUS.official.down]
            elif self.template.lower() in PyFunceble.STATUS.list.invalid:
                # The template is in the list of invalid status.

                # We informations to print is the invalid header.
                to_print = self.headers[PyFunceble.STATUS.official.invalid]
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

                if self.template == "Less" and not PyFunceble.HTTP_CODE.active:
                    # * The template is equal to `Less`.
                    # and
                    # * The http status code extraction is deactivated.

                    # We append the source index to the header.
                    to_print["Source"] = 10
            elif self.template == "Simple":
                to_print = self.headers[self.template]

            if not PyFunceble.HTTP_CODE.active:
                # * The http status code extraction is deactivated.

                # We remove the HTTP Code index from the data to print.
                to_print = PyFunceble.helpers.Dict(to_print).remove_key("HTTP Code")

            # We update the currently used header.
            self.currently_used_header = to_print

            if not do_not_print:
                # We are not authorized to print anything.

                # We generate the before header.
                self.before_header()

                for formatted_template in self.header_constructor(to_print):
                    # We loop through the formatted template.

                    if not self.only_on_file:
                        # We do not have to print only on file.

                        # We print on screen the formatted header template.
                        print(formatted_template)

                    if not PyFunceble.CONFIGURATION.no_files and self.output:
                        # An output destination is given.

                        # We write the file with the formatted header template.
                        self.file_output_instance.write(formatted_template + "\n")

    def data_constructor(self, size):
        """
        Construct the table of data according to given size.

        :param list size: The maximal length of each string in the table.

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
        result = OrderedDict()

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

        :param dict header:
            The header template we have to get the size from.

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

        :param str data: The string to colorify.

        :return: A colored string.
        :rtype: str
        """

        if self.template in ["Generic", "Less"]:
            # The template is in the list of template that need the coloration.

            if (
                self.data_to_print[1].lower() in PyFunceble.STATUS.list.up
                or self.data_to_print[1].lower() in PyFunceble.STATUS.list.valid
                or self.data_to_print[1].lower() in PyFunceble.STATUS.list.sane
            ):
                # The status is in the list of up status.

                # We print the data with a green background.
                data = Fore.BLACK + Back.GREEN + data
            elif (
                self.data_to_print[1].lower() in PyFunceble.STATUS.list.down
                or self.data_to_print[1].lower() in PyFunceble.STATUS.list.malicious
            ):
                # The status is in the list of down status.

                # We print the data with a red background.
                data = Fore.BLACK + Back.RED + data
            else:
                # The status is not in the list of up and down status.

                # We print the data with a cyan background.
                data = Fore.BLACK + Back.CYAN + data

        # We return the data.
        return data

    def _json_print(self):  # pragma: no cover
        """
        Management of the json template.
        """

        if self.output:
            # The given output is not empty.

            if self.file_output_instance.exists():
                # The given output already exist.

                # We get the content of the output.
                content = PyFunceble.helpers.Dict().from_json_file(
                    self.file_output_instance.path
                )

                if not content or isinstance(content, dict):
                    content = []

                if isinstance(content, list):
                    # The content is a list.

                    # We extend the content with our data to print.
                    content.extend(self.data_to_print)

                    # We format our list.
                    content = PyFunceble.helpers.List(content).custom_format(
                        PyFunceble.engine.Sort.standard
                    )

                    if PyFunceble.CONFIGURATION.hierarchical_sorting:
                        # The hierarchical sorting is activated.

                        # We format our content hierarchicaly
                        content = PyFunceble.helpers.List(content).custom_format(
                            PyFunceble.engine.Sort.hierarchical
                        )

                    # We finally save our content into the file.
                    PyFunceble.helpers.Dict(content).to_json_file(self.output)
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
                PyFunceble.helpers.Dict(self.data_to_print).to_json_file(self.output)
        else:
            # The given output is empty.

            # We raise an exception.
            raise Exception("Empty output given.")

    def __get_print_size(self):  # pragma: no cover
        """
        Provides the size of the element to print.
        """

        # We initiate a variable which will list the list of
        # alone case.
        alone_cases = ["Percentage", "HTTP"]

        # we initiate a variable which will list the list of
        # template which does not need a header.
        without_header = ["FullHosts", "PlainDomain"]

        result = []

        if self.template not in alone_cases and self.template not in without_header:
            # * The template is not in the list of alone case.
            # and
            # * THe template is not in the list of template without header.

            # We get the template we should use.
            # Note: We basically only need the self.currently_used_header to be filled.
            self.header(True)

            # And we get the size from the header.
            return self._size_from_header(self.currently_used_header)

        if self.template in without_header:
            # The template is in the list of template which does not need a header.

            result = []
            for data in self.data_to_print:
                # We loop through the list of data to print.

                # And we construct the (spacement) size of the data to print.
                result.append(str(len(data)))
            return result

        # We get the size from the given template name.
        return self._size_from_header(self.headers[self.template])

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

            if self.template.lower() == "json":
                # The template is the json template.

                if not PyFunceble.CONFIGURATION.no_files and self.output:
                    # * We are allowed to generate file.
                    # and
                    # * The given output is not empty.

                    # We print the json file.
                    return self._json_print()

                # We return nothing.
                return None

            # We initiate the size we are going to print.
            to_print_size = self.__get_print_size()

            # We construct and format the data to print.
            to_print = self.data_constructor(to_print_size)

            # We print the before header section.
            self.before_header()

            for data in self.header_constructor(to_print, False):
                # We loop through the formatted data.

                if self.template.lower() in PyFunceble.STATUS.list.generic or self.template in [
                    "Less",
                    "Percentage",
                ]:
                    # * The template is in the list of generic status.
                    # or
                    # * The template is in a specific list.

                    if not self.only_on_file:
                        # We are authorized to print on screen.

                        # We colorify the data to print.
                        colorified_data = self._colorify(data)

                        # And we print the data.
                        print(colorified_data)

                elif self.template == "Simple":
                    if not self.only_on_file:
                        print(
                            PyFunceble.core.CLI.get_simple_coloration(
                                self.data_to_print[-1]
                            )
                            + data
                            + Style.RESET_ALL
                        )

                if not PyFunceble.CONFIGURATION.no_files and self.output:
                    # * We are authorized to print on any file.
                    # and
                    # * The output is given.

                    # We write our data into the printed file.
                    self.file_output_instance.write(data + "\n")
        else:
            # This should never happend. If it's happens then there's a big issue
            # around data_to_print.
            raise Exception("Please review Prints().data()")
