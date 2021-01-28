"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides an easy way to convert a RPZ policy into a testable subject.

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

from PyFunceble.exceptions import WrongParameterType

from .base import ConverterBase


class RPZ2Subject(ConverterBase):
    """
    Converts a given RPZ policy into a testable subject.
    """

    COMMENT_SIGN = ";"
    CLEANUP_MARKERS = [".rpz-nsdname"]
    IP_MARKERS = [".rpz-client-ip", ".rpz-ip", ".rpz-nsip"]

    def __init__(self, data_to_convert):
        if not isinstance(data_to_convert, str):
            raise WrongParameterType(
                f"<data_to_convert> should be {str}, {type(data_to_convert)} given."
            )

        super().__init__(data_to_convert)

    @classmethod
    def __remove_marker(cls, subject, marker):
        """
        Removes the marker from the given subject.

        ..warning::
            This method assume that the marker is into the
            given string.
        """

        return subject[: subject.find(marker)]

    def __has_cleanup_marker(self, subject, *, return_matching=False):
        """
        Checks if the given subject has our cleanup marker.
        """

        for marker in self.CLEANUP_MARKERS:
            if subject.endswith(marker):
                return True if not return_matching else marker

        return False if not return_matching else None

    def __has_ip_marker(self, subject, *, return_matching=False):
        """
        Checks if the given subject has our ip marker.
        """

        for marker in self.IP_MARKERS:
            if subject.endswith(marker):
                return True if not return_matching else marker

        return False if not return_matching else None

    def __handle_cleanup_marker(self, subject, marker):
        """
        Handles the cleanup marker.
        """

        return self.__remove_marker(subject, marker)

    def __handle_ip_marker(self, subject, marker):
        """
        Handles the IP marker.
        """

        result = self.__remove_marker(subject, marker)
        splitted_reversed_result = list(reversed(result.split(".")))

        if (
            len(splitted_reversed_result) > 4
            and splitted_reversed_result[-1].isdigit()
            and len(splitted_reversed_result[-1]) <= 2
            and 0 <= int(splitted_reversed_result[-1]) <= 32
        ):
            result = (
                ".".join(splitted_reversed_result[:-1])
                + f"/{splitted_reversed_result[-1]}"
            )
        else:
            result = ".".join(splitted_reversed_result)

        possible_range = result[result.rfind(".") + 1 :]

        if (
            ".zz." in result
            and possible_range.isdigit()
            and len(possible_range) <= 3
            and 0 <= int(possible_range) <= 128
        ):
            result = "/".join(result.rsplit(".", 1)).replace(".", ":")

        if "zz" in result:
            result = (
                result.replace(".zz.", "::")
                .replace(":zz:", "::")
                .replace(".zz", "::")
                .replace(":zz", "::")
                .replace("zz.", "::")
                .replace("zz:", "::")
                .replace(".", ":")
            )

        if any(x.isalpha() for x in result):
            result = result.replace(".", ":")

        return result

    def get_converted(self):
        """
        Process the conversion of the given data to convert.
        """

        subject = self.data_to_convert.strip()

        if not subject or subject.startswith(self.COMMENT_SIGN):
            return None

        if self.COMMENT_SIGN in subject:
            subject = subject[: subject.find(self.COMMENT_SIGN)].strip()

        if subject.startswith("*."):
            subject = subject[2:]

        cleanup_marker = self.__has_cleanup_marker(subject, return_matching=True)

        if cleanup_marker:
            return self.__handle_cleanup_marker(subject, cleanup_marker)

        ip_marker = self.__has_ip_marker(subject, return_matching=True)

        if ip_marker:
            return self.__handle_ip_marker(subject, ip_marker)

        return subject
