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

from typing import Any, List, Optional, Set, Union

from PyFunceble.converter.base import ConverterBase
from PyFunceble.converter.url2netloc import Url2Netloc
from PyFunceble.helpers.list import ListHelper
from PyFunceble.helpers.regex import RegexHelper


class AdblockInputLine2Subject(ConverterBase):
    """
    Provides an interface for the conversion or extraction of valuable subjects
    from an inputted AdBlock line.
    """

    _aggressive: bool = False

    _regex_helper: Optional[RegexHelper] = None

    def __init__(
        self,
        data_to_convert: Optional[Any] = None,
        *,
        aggressive: bool = False,
        regex_helper: Optional[RegexHelper] = None,
    ) -> None:
        if regex_helper is None:
            self._regex_helper = RegexHelper()
        else:
            self._regex_helper = regex_helper

        super().__init__(data_to_convert=data_to_convert, aggressive=aggressive)

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

    @staticmethod
    def should_be_ignored(line: str) -> bool:
        """
        Checks if we should ignore the given line.
        """

        starting_chars = ["!", "@@", "/", "[", ".", "-", "_", "?", "&"]

        return any(line.startswith(x) for x in starting_chars)

    @staticmethod
    def extract_base(subject: Union[str, List[str]]) -> Union[str, List[str]]:
        """
        Extracts the base of the given subject (supposely URL).

        :param subject:
            The subject to work with.

        Example:

            Giving :code:`"hello.world/?is=beautiful"` returns :code:`"hello.world"`
        """

        subject = subject.replace("*", "").replace("~", "")

        try:
            return Url2Netloc(subject).get_converted()
        except ValueError:
            return subject

    def _decode_multiple_subject(self, decoded: str) -> Set[str]:
        """
        Implementation of the decoding of the case that multiple
        subjects are possible in the given :py:class:`str`.

        :param decoded:
            The decoded part to split.
        """

        result = set()

        rematch = self._regex_helper.set_regex(r"((?:[^~\*,]+))").match(
            decoded, rematch=True, return_match=True
        )

        if rematch:
            result.update({self.extract_base(x) for x in rematch})

        return result

    def _decode_options(self, decoded_options: List[str]) -> Set[str]:
        """
        Handle the decoding of the options.

        What it does:

            - It extracts all :code:`domain=` component - when found.
            - It extracts all :code:`href` URL base - when found.


        :param decoded_options:
            The splitted list of options.
        """

        result = set()

        for rule in decoded_options:
            if "domain=" in rule:
                rule = rule.replace("domain=", "").replace("|", ",")

                result.update(self._decode_multiple_subject(rule))
                continue

            if "href" in rule:
                matched = self._regex_helper.set_regex(
                    r"((?:\"|\')(.*)(?:\"|\'))"
                ).match(rule, return_match=True, rematch=True, group=1)

                if matched:
                    result.add(self.extract_base(matched))
                continue

        return result

    def _decode_v1(self, line: str) -> Set[str]:
        """
        Implementation of our first decoding mode.

        In this mode we try to decode the simple:

            ||ads.example.com^

        rule.

        :param line:
            The line to decode.
        """

        result = set()

        local_line = line.strip()

        if local_line.startswith("||") and (
            local_line.endswith("^") or local_line.endswith("$")
        ):
            local_line = local_line.replace("||", "", 1)

            if local_line.endswith("^"):
                local_line = "".join(local_line.rsplit("^", 1))
            elif local_line.endswith("$"):
                local_line = "".join(local_line.rsplit("$", 1))

            result.update(self._decode_multiple_subject(local_line))

        return {x for x in result if "." in x}

    def _decode_v2(self, line: str) -> Set[str]:
        """
        Implementation of our second decoding mode.

        In this mode, we try to decode the simple:

            |https://ads.example.com|

        rule.

        :param line:
            The line to decode.
        """

        result = set()

        local_line = line.strip()

        if local_line.startswith("|") and local_line.endswith("|"):
            local_line = local_line.replace("|", "", 1)
            local_line = "".join(local_line.rsplit("|", 1))

            result.add(self.extract_base(local_line))

        return {x for x in result if "." in x}

    def _decode_v3(self, line: str, *, aggressive: bool = False) -> Set[str]:
        """
        Implementation of our third decoding mode.

        In this mode, we try to decode the simple:

            ||ads.example.com^$script,image,domain=example.com|~foo.example.info
            ||ads.example.com$script,image,domain=example.com|~foo.example.info

        rule.

        :param line:
            The line to decode.
        :param aggressive:
            Whether we should aggressively extract datasets.
        """

        result = set()

        local_line = line.strip()

        if not local_line.startswith("||"):
            return result

        if "$" in local_line:
            v1_mode, options = local_line.split("$", 1)

            if not v1_mode.endswith("^"):
                v1_mode += "^"

            result.update(self._decode_v1(v1_mode))

            if aggressive:
                result.update(self._decode_options(options.split(",")))
        elif "^" not in local_line:
            result.update(self._decode_v1(f"{local_line}^"))
        else:
            result.update(self._decode_v1(local_line[: local_line.find("^") + 1]))

        return {x for x in result if "." in x}

    def _decode_v4(self, line: str, *, aggressive: bool = False) -> Set[str]:
        """
        Implementation of our fourth decoding mode.

        In this mode, we try to decode the simple:

            @@||ads.example.com/notbanner^$~script

        rule.

        :param line:
            The line to decode.
        :param aggressive:
            Whether we should aggressively extract datasets.
        """

        result = set()
        local_line = line.strip()

        if (
            not aggressive
            or not local_line.startswith("@@||")
            or "^$" not in local_line
        ):
            return result

        v1_mode, options = local_line.split("$", 1)

        result.update(
            {self.extract_base(x) for x in self._decode_v1(v1_mode.replace("@@", ""))}
        )

        result.update(self._decode_options(options.split(",")))

        return {x for x in result if "." in x}

    def _decode_v5(self, line: str, *, aggressive: bool = False) -> Set[str]:
        """
        Implementation of our fifth decoding mode.

        In this mode, we try to decode the simple:

            example.com,example.net##.advert
            exception.example.com#@#.advert
            example.com,example.net#?#div:-abp-has(> div > img.advert)
            exception.example.com#@#div:-abp-has(> div > img.advert)

        rule.

        :param line:
            The line to decode.
        :param aggressive:
            Whether we should aggressively extract datasets.
        """

        local_line = line.strip()
        result = set()

        if not aggressive:
            return result

        separators = ["##", "#@#", "#?#"]

        obj_of_interest, options = "", ""

        for separator in separators:
            if separator in local_line:
                obj_of_interest, options = local_line.split(separator, 1)
                break

        result.update(self._decode_multiple_subject(obj_of_interest))
        result.update(self._decode_options(options.split(",")))

        return {x for x in result if "." in x}

    def _decode_v6(self, line: str, *, aggressive: bool = False) -> Set[str]:
        """
        Implementation of our sixth decoding mode.

        In this mode we try to decode the simple:

            $domain=exam.pl|elpmaxe.pl|example.pl
            ^hello^$domain=example.com

        rule.

        :param line:
            The line to decode.
        :param aggressive:
            Whether we should aggressively extract datasets.
        """

        local_line = line.strip()
        result = set()

        if not aggressive:
            return result

        separators = ["$"]

        for separator in separators:
            if separator not in line:
                continue

            options = local_line[local_line.find(separator) + 1 :]

            result.update(self._decode_options(options.split(",")))

        return {x for x in result if "." in x}

    def get_converted(self) -> List[str]:
        """
        Provides the converted data.
        """

        return self.convert(self.data_to_convert, aggressive=self.aggressive)

    def convert(self, data: Any, *, aggressive: bool = False) -> List[str]:
        """
        Converts the given dataset.

        :param data:
            The data to convert.
        :param aggressive:
            Whether we should aggressively extract datasets.
        """

        result = set()

        if not self.should_be_ignored(data.strip()):
            result.update(self._decode_v1(data))
            result.update(self._decode_v2(data))
            result.update(self._decode_v3(data, aggressive=aggressive))
            result.update(self._decode_v5(data, aggressive=aggressive))
            result.update(self._decode_v6(data, aggressive=aggressive))

        result.update(self._decode_v4(data, aggressive=aggressive))

        return ListHelper(list(result)).sort().subject
