# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the conversion of the an RPZ POlicy into testable subjects.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

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
# pylint: enable=line-too-long

from typing import Any, List, Optional

from PyFunceble.converter.rpz_input_line2subject import RPZInputLine2Subject
from PyFunceble.converter.wildcard2subject import Wildcard2Subject


class RPZPolicy2Subject(RPZInputLine2Subject):
    """
    Converts/Extracts the subject from the given RPZ Policy into a subject.
    """

    CLEANUP_MARKERS: list = [".rpz-nsdname"]
    IP_MARKERS: list = [".rpz-client-ip", ".rpz-ip", ".rpz-nsip"]

    _soa: Optional[str] = None
    _soas: List[str] = []

    def __init__(
        self,
        data_to_convert: Optional[Any] = None,
        soas: Optional[List[str]] = None,
        soa: Optional[str] = None,
    ) -> None:

        if soas is not None:
            self.soas = soas

        if soa is not None:
            self.soa = soa

        super().__init__(data_to_convert=data_to_convert)

    @property
    def soa(self) -> Optional[str]:
        """
        Provides the currently set SOA.
        """

        return self._soa

    @soa.setter
    def soa(self, value: str) -> None:
        """
        Sets the current SOA.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._soa = value

        if value not in self._soas:
            self._soas.append(value)

    def set_soa(self, value: str) -> "RPZPolicy2Subject":
        """
        Sets the current SOA.

        :param value:
            The value to set.
        """

        self.soa = value

        return self

    @property
    def soas(self) -> Optional[str]:
        """
        Provides the currently set SOAs.
        """

        return self._soas

    @soas.setter
    def soas(self, value: List[str]) -> None:
        """
        Sets the current SOAs.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class`list`.
        :raise ValueError:
            When one of the given value is not a string.
        """

        if not isinstance(value, list):
            raise TypeError(f"<value> should be {list}, {type(value)} given.")

        if any(not isinstance(x, str) for x in value):
            raise ValueError(f"<value> {value!r} should only contain strings.")

        self._soas = value

    def set_soas(self, value: List[str]) -> "RPZPolicy2Subject":
        """
        Sets the current SOAs.

        :param value:
            The value to set.
        """

        self.soas = value

        return self

    @staticmethod
    def remove_marker(subject: str, marker: str) -> str:
        """
        Removes the given marker from the given subject.
        """

        if marker in subject:
            return subject[: subject.find(marker)]
        return subject

    @classmethod
    def get_matching_cleanup_marker(cls, subject: str) -> Optional[str]:
        """
        Checks if the given subject has a cleanup marker and provides it if found.
        """

        for marker in cls.CLEANUP_MARKERS:
            if subject.endswith(marker):
                return marker
        return None

    @classmethod
    def get_matching_ip_marker(cls, subject: str) -> Optional[str]:
        """
        Checks if the given subject has an IP marker and provides it if found.
        """

        for marker in cls.IP_MARKERS:
            if subject.endswith(marker):
                return marker
        return None

    @classmethod
    def get_subject_from_ip_marker(cls, subject: str, marker: str) -> str:
        """
        Removes the ip marker and converts the IP into a testable subject.
        """

        result = cls.remove_marker(subject, marker)

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

    def get_converted(self) -> Optional[str]:
        """
        Provides the converted data.
        """

        subject = self.data_to_convert.strip()

        if (
            subject
            and not any(subject.startswith(x) for x in self.COMMENT)
            and not any(subject.startswith(x) for x in self.SPECIAL)
        ):
            for comment_sign in self.COMMENT:
                if comment_sign in subject:
                    subject = self.remove_marker(subject, comment_sign).strip()

            subject = Wildcard2Subject(subject).get_converted()

            if self._soas:
                for soa in self._soas:
                    subject = self.remove_marker(subject, f".{soa}")
                    subject = self.remove_marker(subject, soa)

            found_cleanup_marker = self.get_matching_cleanup_marker(subject)

            if found_cleanup_marker:
                return self.remove_marker(subject, found_cleanup_marker)

            found_ip_marker = self.get_matching_ip_marker(subject)

            if found_ip_marker:
                return self.get_subject_from_ip_marker(subject, found_ip_marker)

            return subject

        return None
