"""
The tool to check the availability or syntax of domain, IP or URL.

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
    https://pyfunceble.readthedocs.io/en/master/

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
from urllib.parse import urlparse

import PyFunceble


class Sort:  # pylint: disable=too-few-public-methods
    """
    Provides some sorting presets which we can
    parse to :py:class:`PyFunceble.helpers.list.List.custom_format`.
    """

    @classmethod
    def __get_url_base(cls, element):
        """
        Provides the URL base if needed.
        """

        if element.startswith("http:") or element.startswith("https:"):
            parsed = urlparse(element)

            if parsed.netloc:
                return parsed.netloc

        return element

    @classmethod
    def standard(cls, element):
        """
        Implements the standard and alphabetical sorting.

        :param str element: The element we are currently reading.

        :return: The formatted element.
        :rtype: str
        """

        element = cls.__get_url_base(element)
        regex_replace = r"[^a-zA-Z0-9\.]"

        # We remove all special characters and return the formatted string.
        cleaned = (
            PyFunceble.helpers.Regex(regex_replace)
            .replace_match(element.strip(), "")
            .lower()
        )

        return [
            int(x) if x.isdigit() else x
            for x in PyFunceble.helpers.Regex(r"(\d+)").split(cleaned)
        ]

    @classmethod
    def hierarchical(cls, element):
        """
        The idea behind this method is to sort a list of domain hierarchically.

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

        element = cls.__get_url_base(element)

        return cls.standard(".".join(reversed(element.strip().split("."))))
