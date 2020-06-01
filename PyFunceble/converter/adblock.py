"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides an adblock decoding interface.

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

import PyFunceble.helpers as helpers
from PyFunceble.check import Check
from PyFunceble.exceptions import WrongParameterType

from .base import ConverterBase


class AdBlock(ConverterBase):
    """
    Converts an adblock filter line to a list os subject to test.
    """

    options_separator = "$"
    option_separator = ","

    def __init__(self, data_to_convert, aggressive=False):
        if not isinstance(data_to_convert, (str, list)):
            raise WrongParameterType(
                f"<data_to_convert> should be {str} or {list}, {type(data_to_convert)} given."
            )

        super().__init__(data_to_convert)
        self.aggressive = aggressive

    @classmethod
    def ignore_it(cls, subject):
        """
        Checks if we have to ignore the given subject.

        :param str subject: The subject ot work with.

        :return: The result of the check.
        :rtype: bool
        """

        # We set the list of regex to match to be
        # considered as ignored.
        #
        # Note: In a more aggressive way, r"(\$|,)(image)" may be added.
        to_ignore = [r"(^!|^@@|^\/|^\[|^\.|^-|^_|^\?|^&)"]

        for element in to_ignore:
            # We loop through the list of regex.

            if helpers.Regex(element).match(subject.strip(), return_match=False):
                # The currently read line match the currently read
                # regex.

                # We return true, it has to be ignored.
                return True

        # Wer return False, it does not has to be ignored.
        return False

    def remove_ignored(self, subject):
        """
        Removes the ignored element from the given list of subject.
        """

        if isinstance(subject, str):
            if self.ignore_it(subject):
                return []
            return [subject.strip()]

        return [x.strip() for x in subject if not self.ignore_it(x)]

    def extract_from_options(self, options):
        """
        Exctracts the relevant data from the list of options.

        :param list options: The list of options of a rule.

        :return: The list of domains.
        :rtype: list
        """

        result = []

        # We initiate the regex which will be used to extract the domain listed
        # under the option domain=
        regex_domain_option = r"domain=(.*)"

        for option in options:
            # We loop through the list of option.
            try:
                # We try to extract the list of domains from the currently read
                # option.
                domains = helpers.Regex(regex_domain_option).match(
                    option, return_match=True, rematch=True, group=0
                )[-1]

                if domains:
                    # We could extract something.

                    if self.aggressive:  # pragma: no cover
                        result.extend(
                            [
                                x
                                for x in domains.split("|")
                                if x and not x.startswith("~")
                            ]
                        )
                    else:
                        return True
            except TypeError:
                pass

        # We return the result.
        return result

    def extract_base(self, subject):
        """
        Extracts the base of the given element.

        As an example:
            given :code:`"hello.world/?is=beautiful"` returns :code:`"hello.world"`

        :param subject: The subject to work with.
        :type element: str|list
        """

        if isinstance(subject, list):
            return [self.extract_base(x) for x in subject]

        base = Check(subject).is_url(return_base=True)

        if base:
            return base

        if "/" in subject:
            return subject.split("/")[0]

        return subject

    def format_decoded(self, decoded, result=None):  # pragma: no cover
        """
        Formats the extracted adblock line in order to be
        compatible with what the system understand.

        :param str decoded: The decoded data to work with.

        :param list result: A list of the result of this method.

        :return: The list of domains or IP compatible with the system.
        :rtype: list
        """

        if result is None:
            result = []

        for data in decoded:
            if data:
                if "^" in data:
                    # There is an accent in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return self.format_decoded(data.split("^"), result)

                if "#" in data:
                    # There is a dash in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return self.format_decoded(data.split("#"), result)

                if "," in data:
                    # There is a comma in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return self.format_decoded(data.split(","), result)

                if "!" in data:
                    # There is an exclamation mark in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return self.format_decoded(data.split("!"), result)

                if "|" in data:
                    # There is a vertival bar in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return self.format_decoded(data.split("|"), result)

                if data:
                    # The currently read line is not empty.

                    data = self.extract_base(data)

                    # We create an instance of the checker.
                    checker = Check(data)

                    if data and (checker.is_domain() or checker.is_ip()):
                        # The extraced base is not empty.
                        # and
                        # * The currently read line is a valid domain.
                        # or
                        # * The currently read line is a valid IP.

                        # We append the currently read line to the result.
                        result.append(data)
                    elif data:
                        # * The currently read line is not a valid domain.
                        # or
                        # * The currently read line is not a valid IP.

                        # We try to get the url base.
                        url_base = checker.is_url(return_base=True)

                        if url_base:
                            # The url_base is not empty or equal to False or None.

                            # We append the url base to the result.
                            result.append(url_base)

        return result

    def __decode_v1(self, data):
        """
        Decodes the v1.

        :param str data: A string to decode.
        :rtype: list
        """

        result = []

        rematch = helpers.Regex(r"^(?:.*\|\|)([^\/\$\^]{1,}).*$").match(
            data, return_match=True, group=0, rematch=True
        )

        if rematch:
            if self.options_separator in data:
                options = data.split(self.options_separator)[-1].split(
                    self.option_separator
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

                extra = self.extract_from_options(options)

                if extra:
                    if isinstance(extra, list):  # pragma: no cover
                        extra.extend(self.extract_base(rematch))
                        result.extend(self.extract_base(extra))
                    else:
                        result.extend(self.extract_base(rematch))
            else:
                result.extend(self.extract_base(rematch))

        return result

    def __decode_v2(self, data):
        """
        Decodes the v2.

        :param str data: A string to decode.
        :rtype: list
        """

        result = []

        rematch = helpers.Regex(r"^\|(.*\..*)\|$").match(
            data, return_match=True, group=0, rematch=True
        )

        if rematch:
            result.extend(self.format_decoded(rematch))

        return result

    def __decode_v3(self, data):
        """
        Decodes the v3.

        :param str data: A string to decode.
        :rtype: list
        """

        result = []

        rematch = helpers.Regex(
            r"(?:#+(?:[a-z]+?)?\[[a-z]+(?:\^|\*)\=(?:\'|\"))(.*\..*)(?:(?:\'|\")\])"
        ).match(data, return_match=True, group=0, rematch=True)

        if rematch:
            result.extend(self.format_decoded(rematch))

        return result

    def __decode_v4(self, data):
        """
        Decodes the v4.

        :param str data: A string to decode.
        :rtype: list
        """

        result = []

        rematch = helpers.Regex(r"^(.*?)(?:#{2}|#@#)").match(
            data, return_match=True, group=0, rematch=True
        )

        if rematch:
            result.extend(self.format_decoded(rematch))

        return result

    def get_converted(self):
        """
        Converts and return the result of the conversion.

        :rtype: list
        """

        result = []

        for data in self.remove_ignored(self.data_to_convert):
            result.extend(self.__decode_v1(data))
            result.extend(self.__decode_v2(data))
            result.extend(self.__decode_v3(data))
            result.extend(self.__decode_v4(data))

        return helpers.List(result).format()
