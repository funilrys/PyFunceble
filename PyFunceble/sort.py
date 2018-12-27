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

This submodule will provide some sorting presets.

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

import PyFunceble
from PyFunceble.check import Check
from PyFunceble.helpers import Regex
from PyFunceble.publicsuffix import PublicSuffix


class Sort:  # pylint: disable=too-few-public-methods
    """
    Provide some sorting presets which we can
    parse to PyFunceble.helpers.List().custom_format().
    """

    # We initiate a regex which will match everything which is not
    # a letter, a number or a point.
    regex_replace = r"[^a-z0-9]"

    @classmethod
    def standard(cls, element):
        """
        Implement the standard and alphabetical sorting.

        :param element: The element we are currently reading.
        :type element: str

        :return: The formatted element.
        :rtype: str
        """

        # We remove all special characters and return the formatted string.
        return (
            Regex(element, cls.regex_replace, replace_with="@funilrys")
            .replace()
            .replace("@funilrys", "")
        )

    @classmethod
    def hierarchical(cls, element):
        """
        The idea behind this method is to sort a list of domain hierarchicaly.

        :param element: The element we are currently reading.
        :type element: str

        :return: The formatted element.
        :rtype: str

        .. note::
            For a domain like :code:`aaa.bbb.ccc.tdl`.

            A normal sorting is done in the following order:
                1. :code:`aaa`
                2. :code:`bbb`
                3. :code:`ccc`
                4. :code:`tdl`

            This method allow the sorting to be done in the following order:
                1. :code:`tdl`
                2. :code:`ccc`
                3. :code:`bbb`
                4. :code:`aaa`

        """

        # We initiate a variable which will save the element to sort without
        # the extension.
        to_sort = ""

        # We initiate a variable which will save the full extension.
        full_extension = ""

        # We convert the parsed element to lower case.
        element = element.lower()

        # We try to get the url base.
        url_base = Check().is_url_valid(element, return_base=True)

        # We laod the public suffix database.
        PublicSuffix(False).load()

        if not isinstance(url_base, str):
            # The url base is not found.

            if "." in element:
                # There is point in the parsed element.

                # We get the position of the first letter of the extension.
                extension_index = element.rindex(".") + 1

                # We get the extension from the position of the last point.
                extension = element[extension_index:]

                if extension in PyFunceble.CONFIGURATION["psl_db"]:
                    # The extension is in the public suffix database.

                    for suffix in PyFunceble.CONFIGURATION["psl_db"][extension]:
                        # We loop through the list of suffix of the extracted extension.

                        # We suffix the sufix with a point.
                        formatted_suffix = "." + suffix

                        if element.endswith(formatted_suffix):
                            # The elements ends with the suffix.

                            # We get the position of the first character of the suffix in
                            # the parsed element.
                            suffix_index = element.rindex(formatted_suffix)

                            # We update the to_sort variable with the element without the suffix.
                            to_sort = element[:suffix_index]

                            # We replace the full extension with the currently read suffix.
                            full_extension = suffix

                            # We break the loop, we got what we wanted.
                            break

                if not full_extension:
                    # The full extension is empty.

                    # We initiate it with the extension.
                    full_extension = element[extension_index:]

                    # We update the to_sort variable with the element without the extension.
                    to_sort = element[: extension_index - 1]

                # We append a point to the full extension because the point has to be
                # at the end and not at the begining of the extension.
                # To understand: Imagine a miror.
                full_extension += "."

                # We reverse the to_sort string.
                tros_ot = to_sort[::-1]

                if "." in tros_ot:
                    # There is a point in the reversed string.

                    # * We reverse each level of the parsed element.
                    # and
                    # * We glue each level of the parsed element with each other.
                    #
                    # Note: after this, there is no point anymore.
                    reversion = full_extension + ".".join(
                        list(map(lambda x: x[::-1], tros_ot.split(".")))
                    )

                    # We remove all special characters and return the formatted string.
                    return (
                        Regex(reversion, cls.regex_replace, replace_with="@funilrys")
                        .replace()
                        .replace("@funilrys", "")
                    )

                # We remove all special characters and return the formatted string.
                return (
                    Regex(
                        full_extension + tros_ot,
                        cls.regex_replace,
                        replace_with="@funilrys",
                    )
                    .replace()
                    .replace("@funilrys", "")
                )

            # There is no point in the parsed element.

            # We return the parsed element.
            return element

        # The url base is not found.

        # We get the position of the element.
        protocol_position = element.rindex(url_base)

        # We extract the protocol from the element position.
        protocol = element[:protocol_position]

        # We return the output of this method but with the url base instead of the full url.
        return protocol + cls.hierarchical(url_base)
