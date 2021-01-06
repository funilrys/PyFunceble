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

Provides the conversion of an AdBlock input line into testable subjests.

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

from typing import Any, List, Optional, Union

from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.converter.base import ConverterBase
from PyFunceble.converter.url2netloc import Url2Netloc
from PyFunceble.helpers.list import ListHelper
from PyFunceble.helpers.regex import RegexHelper


class AdblockInputLine2Subject(ConverterBase):
    """
    Converts/Extract the subjects to test from an inputed AdBlock line.

    In order to decode the given line, this class and its conversion method
    will go though a brunch of decoding method.
    """

    OPTION_SEPARATOR: str = ","
    OPTIONS_SEPARATOR: str = "$"

    _aggressive: bool = False

    def __init__(
        self, data_to_convert: Optional[Any] = None, aggressive: bool = False
    ) -> None:
        if aggressive is not None:
            self.aggressive = aggressive

        super().__init__(data_to_convert)

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
        super(AdblockInputLine2Subject, self.__class__).data_to_convert.fset(
            self, value
        )

    @property
    def aggressive(self) -> bool:
        """
        Provides the state of the :code:`_aggressive` attribute.
        """

        return self._aggressive

    @aggressive.setter
    def aggressive(self, value: bool) -> None:
        """
        Provides a way to activate/deactivate the aggressive decoding.

        :raise TypeError:
            When the given data to convert is not :py:class:`str`
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._aggressive = value

    def set_aggressive(self, value: bool) -> "AdblockInputLine2Subject":
        """
        Provides a way to activate/deactivate the aggressive decoding.
        """

        self.aggressive = value

        return self

    @staticmethod
    def should_be_ignored(line: str) -> bool:
        """
        Checks if we should ignore the given line.
        """

        to_ignore = r"(^!|^@@|^\/|^\[|^\.|^-|^_|^\?|^&)"

        return RegexHelper(to_ignore).match(line.strip(), return_match=False)

    @classmethod
    def extract_base(cls, subject: Union[str, list]) -> str:
        """
        Extracts the base of the given element (supposed URL).

        As example:
            Giving :code:`"hello.world/?is=beautiful"` returns :code:`"hello.world"`
        """

        if isinstance(subject, list):
            return [cls.extract_base(x) for x in subject]

        try:
            return Url2Netloc(subject).get_converted()
        except ValueError:
            return subject

    @classmethod
    def __format_decoded(
        cls, decoded: str, *, result: Optional[List[str]] = None
    ) -> List[str]:
        """
        A recursive method which infinitly filter and format the decoded data
        in order to delete uneeded parts.

        :param decoded:
            The decoded part.
        """

        if result is None:
            result = []

        chars_to_split = ["^", "#", ",", "!", "|"]

        for data in decoded:
            if not data:
                continue

            for char_to_split in chars_to_split:
                if char_to_split in data:
                    return cls.__format_decoded(
                        data.split(char_to_split), result=result
                    )

            data = cls.extract_base(data)

            if data and (
                DomainSyntaxChecker(data).is_valid() or IPSyntaxChecker(data).is_valid()
            ):
                result.append(data)

        return result

    def __filter_options(self, options: List[str]) -> Union[bool, List[str]]:
        """
        Filters the interessting parts of the given list of options.

        :param options:
            The extracted options to filter.

        .. warning::
            Thís method only works if the aggressive method is given.
        """

        result = []

        regex_domain_in_option = r"domain=(.*)"

        for option in options:
            try:
                domains = RegexHelper(regex_domain_in_option).match(
                    option, return_match=True, rematch=True, group=0
                )[-1]
            except TypeError:
                continue

            result.extend(
                [x for x in domains.split("|") if x and not x.startswith("~")]
            )

        if self.aggressive:
            return result

        return bool(result)

    def __decode_v1(self, line: str) -> List[str]:
        """
        Our first decoding version.

        The main idea is to filter based on option and a pattern common to all
        AdBlock / Ublock format.

        :param line:
            The line to decode.
        """

        result = []

        # Get all groups :-)
        rematch = RegexHelper(r"^(?:.*\|\|)([^\/\$\^]{1,}).*$").match(
            line, return_match=True, group=0, rematch=True
        )

        if rematch:
            if self.OPTIONS_SEPARATOR in line:
                # We get the list of options for filtering.
                options = line.split(self.OPTIONS_SEPARATOR)[-1].split(
                    self.OPTION_SEPARATOR
                )

                # pylint: disable=too-many-boolean-expressions
                if (
                    not options[-1]
                    or "third-party" in options
                    or "script" in options
                    or "popup" in options
                    or "xmlhttprequest" in options
                    or "all" in options
                    or "document" in options
                ):
                    result.extend(self.extract_base(rematch))

                extra = self.__filter_options(options)

                if extra:
                    if isinstance(extra, list):
                        extra.extend(self.extract_base(rematch))
                        result.extend(self.extract_base(extra))
                    else:
                        result.extend(self.extract_base(rematch))
            else:
                result.extend(self.extract_base(rematch))

        return result

    def __decode_v2(self, line: str) -> List[str]:
        """
        Our second decoding version.

        The main idea here is that we will match simple records.

        :param line:
            The line to decode.
        """

        result = []

        rematch = RegexHelper(r"^\|(.*\..*)\|$").match(
            line, return_match=True, rematch=True, group=0
        )

        if rematch:
            result.extend(self.__format_decoded(rematch))

        return result

    def __decode_v3(self, line: str) -> List[str]:
        """
        Our third decoding version.

        This one is for more complex formats (and Ublock).

        :param line:
            The line to decode.
        """

        result = []

        rematch = RegexHelper(
            r"(?:#+(?:[a-z]+?)?\[[a-z]+(?:\^|\*)\=(?:\'|\"))(.*\..*)(?:(?:\'|\")\])"
        ).match(line, return_match=True, rematch=True, group=0)

        if rematch:
            result.extend(self.__format_decoded(rematch))

        return result

    def __decode_v4(self, line: str) -> List[str]:
        """
        Our fourth decoding version.

        This is is for the one who are surrounded by #.

        :param line:
            The line to decode.
        """

        result = []

        rematch = RegexHelper(r"^(.*?)(?:#{2}|#@#)").match(
            line, return_match=True, rematch=True, group=0
        )

        if rematch:
            result.extend(self.__format_decoded(rematch))

        return result

    def get_converted(self) -> List[str]:
        """
        Provides the subjects to test.
        """

        result = []

        if not self.should_be_ignored(self.data_to_convert.strip()):
            result.extend(self.__decode_v1(self.data_to_convert))
            result.extend(self.__decode_v2(self.data_to_convert))
            result.extend(self.__decode_v3(self.data_to_convert))
            result.extend(self.__decode_v4(self.data_to_convert))

        return ListHelper(result).remove_duplicates().sort().subject
