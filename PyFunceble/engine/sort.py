"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our sorting engines.

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


class Sort:  # pylint: disable=too-few-public-methods
    """
    Provides some sorting presets which we can
    parse to :py:class:`PyFunceble.helpers.list.List.custom_format`.
    """

    # We initiate a regex which will match everything which is not
    # a letter or a number.
    regex_replace = r"[^a-zA-Z0-9]"

    @classmethod
    def standard(cls, element):
        """
        Implements the standard and alphabetical sorting.

        :param str element: The element we are currently reading.

        :return: The formatted element.
        :rtype: str
        """

        # We remove all special characters and return the formatted string.
        return (
            PyFunceble.helpers.Regex(cls.regex_replace)
            .replace_match(element.strip(), "@funilrys")
            .replace("@funilrys", "")
        )

    @classmethod
    def hierarchical(cls, element):
        """
        The idea behind this method is to sort a list of domain hierarchicaly.

        :param str element: The element we are currently reading.

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
        element = element.lower().strip()

        # We try to get the url base.
        url_base = PyFunceble.Check(element).is_url(return_base=True)

        if not isinstance(url_base, str):
            # The url base is not found.

            if "." in element:
                # There is point in the parsed element.

                # We get the position of the first letter of the extension.
                extension_index = element.rindex(".") + 1

                # We get the extension from the position of the first letter
                # of the extension.
                extension = element[extension_index:]

                if extension in PyFunceble.PSLOOOKUP:
                    # The extension is in the public suffix database.

                    for suffix in PyFunceble.PSLOOOKUP[extension]:
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

                    # We prefix the full extension with the top level
                    # domain name.
                    full_extension = (
                        tros_ot[: tros_ot.index(".")][::-1] + "." + full_extension
                    )

                    # We remove the tor level domain from the rest of
                    # the reversed string.
                    tros_ot = tros_ot[tros_ot.index(".") + 1 :]

                    # * We reverse each level of the parsed element.
                    # and
                    # * We glue each level of the parsed element with each other.
                    #
                    # Note: after this, there is no point anymore.
                    reversion = full_extension + ".".join(
                        [x[::-1] for x in tros_ot.split(".")]
                    )

                    # We remove all special characters and return the formatted string.
                    return (
                        PyFunceble.helpers.Regex(cls.regex_replace)
                        .replace_match(reversion, "@funilrys")
                        .replace("@funilrys", "")
                    )

                # We remove all special characters and return the formatted string.
                return (
                    PyFunceble.helpers.Regex(cls.regex_replace)
                    .replace_match(to_sort + full_extension, "@funilrys")
                    .replace("@funilrys", "")
                )

            # There is no point in the parsed element.

            # We return the parsed element.
            return element

        # The url base is found.

        # We get the position of the element.
        protocol_position = element.rindex(url_base)

        # We extract the protocol from the element position.
        protocol = element[:protocol_position]

        # We return the output of this method but with the url base instead of the full url.
        return protocol + cls.hierarchical(url_base)
