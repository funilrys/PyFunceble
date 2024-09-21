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

Provides the default input line converter.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from typing import Any, List

from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.converter.base import ConverterBase
from PyFunceble.converter.url2netloc import Url2Netloc


class InputLine2Subject(ConverterBase):
    """
    Converts/Extract the subjcts to test from an inputed line.
    """

    COMMENT: str = "#"
    PARTICULAR_COMMENT: List[str] = ["!"]
    SPACE: str = " "
    NSLOOKUP_SPACE: str = "\\032"
    TAB: str = "\t"

    @ConverterBase.data_to_convert.setter
    def data_to_convert(self, value: Any) -> None:
        """
        Overrites the default behavior.

        :raise TypeError:
            When the given data to convert is not :py:class:`str`
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        # pylint: disable=no-member
        super(InputLine2Subject, self.__class__).data_to_convert.fset(self, value)

    def get_converted(self) -> List[str]:
        """
        Provides the subject to test.
        """

        return self.convert(self.data_to_convert, aggressive=self.aggressive)

    @staticmethod
    def extract_base(subject: str) -> str:
        """
        Extracts the base of the given subject - assuming that it may be a URL.

        :param subject:
            The subject to work with.
        """

        try:
            return Url2Netloc(subject).get_converted()
        except ValueError:
            return subject

    def convert(self, data: Any, *, aggressive: bool = False) -> List[str]:
        """
        Converts the given dataset.

        :param data:
            The data to convert.
        :param bool aggressive:
            Whether we should aggressively decode subjects.
        """

        result = []

        subject = data.strip()

        if subject and (
            not subject.startswith(self.COMMENT)
            and any(not subject.startswith(x) for x in self.PARTICULAR_COMMENT)
        ):
            if self.COMMENT in subject:
                subject = subject[: subject.find(self.COMMENT)].strip()

            if self.NSLOOKUP_SPACE in subject:
                # Comply with RFC 6367:
                #    Note that nslookup escapes spaces as "\032" for display
                #    purposes, but a graphical DNS-SD browser should not.
                subject = subject.replace(self.NSLOOKUP_SPACE, self.SPACE)

            if self.SPACE in subject or self.TAB in subject:
                splitted = subject.split()

                if IPSyntaxChecker(splitted[0]).is_valid():
                    # This is for the hosts format.
                    # If the first entry is an IP, we will only extract
                    # the entries after the first one.

                    datasets = splitted[1:]

                    if aggressive:
                        datasets = [self.extract_base(x) for x in datasets]

                    result.extend(datasets)
                else:
                    if aggressive:
                        splitted = [self.extract_base(x) for x in splitted]

                    # All other cases, we extract every entries.
                    result.extend(splitted)
            else:
                if aggressive:
                    subject = self.extract_base(subject)

                result.append(subject)
        return result
