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

This submodule will provide adblock decoding interface.

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


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

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

from PyFunceble.check import Check
from PyFunceble.helpers import List, Regex


class AdBlock:  # pylint: disable=too-few-public-methods
    """
    Provide the adblock decoding logic.

    :param list list_from_file: The file in list format.
    :param bool aggressive:
        Activate the extration of all domains present into
        the given adbloack filter list.

        .. warning::
            This is for now for testing purpose.

            It may be one day accessible to the public
            but please if you read this, think twice
            before using it.
    """

    def __init__(self, list_from_file, aggressive=False):
        self.to_format = self._remove_ignored(list_from_file)
        self.aggressive = aggressive

        # We set the options separator.
        self.options_separator = "$"

        # We set the separator of options
        self.option_separator = ","

    def _remove_ignored(self, list_from_file):
        """
        Removed the ignored element from the given list.

        :param list list_from_file:
            The list which represent the file we are decoding.

        :return: The filtered list.
        :rtype: list
        """

        return [x for x in list_from_file if not self._is_to_ignore(x)]

    @classmethod
    def _is_to_ignore(cls, line):
        """
        Check if we have to ignore the given line.

        :param str line: The line from the file.


        :return: The result of the check.
        :rtype: bool
        """

        # We set the list of regex to match to be
        # considered as ignored.
        to_ignore = [r"(^!|^@@|^\/|^\[|^\.|^-|^_|^\?|^&)"]  # , r"(\$|,)(image)"]

        for element in to_ignore:
            # We loop through the list of regex.

            if Regex(line, element, return_data=False).match():
                # The currently read line match the currently read
                # regex.

                # We return true, it has to be ignored.
                return True

        # Wer return False, it does not has to be ignored.
        return False

    def _handle_options(self, options):
        """
        Handle the data from the options.

        :param list options: The list of options from the rule.

        :return: The list of domains to return globally.
        :rtype: list
        """

        # We initiate a variable which will save our result
        result = []

        # We initiate the regex which will be used to extract the domain listed
        # under the option domain=
        regex_domain_option = r"domain=(.*)"

        for option in options:
            # We loop through the list of option.
            try:
                # We try to extract the list of domains from the currently read
                # option.
                domains = Regex(
                    option, regex_domain_option, return_data=True, rematch=True, group=0
                ).match()[-1]

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
                        # We return True.
                        return True
            except TypeError:
                pass

        # We return the result.
        return result

    def _extract_base(self, element):
        """
        Extract the base of the given element.

        As an example:
            given :code:`"hello.world/?is=beautiful"` returns :code:`"hello.world"`

        :param element: The element we are working with.
        :type element: str|list
        """

        if isinstance(element, list):
            # The given element is a list.

            # We get the base of each element of the list.
            return [self._extract_base(x) for x in element]

        # We get the base if it is an URL.
        base = Check(element).is_url(return_base=True)

        if base:
            # It is an URL.

            # We return the extracted base.
            return base

        if "/" in element:
            # / is in the given element.

            # We return the first element before the
            # first /
            return element.split("/")[0]

        # / is not in the given element.

        # We return the given element.
        return element

    def decode(self):
        """
        Decode/extract the domains to test from the adblock formated file.

        :return: The list of domains to test.
        :rtype: list
        """

        # We initiate a variable which will save what we are going to return.
        result = []

        # We initiate the first regex we are going to use to get
        # the element to format.
        regex = r"^(?:.*\|\|)([^\/\$\^]{1,}).*$"

        # We initiate the third regex we are going to use to get
        # the element to format.
        regex_v3 = (
            r"(?:#+(?:[a-z]+?)?\[[a-z]+(?:\^|\*)\=(?:\'|\"))(.*\..*)(?:(?:\'|\")\])"
        )

        # We initiate the fourth regex we are going to use to get
        # the element to format.
        regex_v4 = r"^\|(.*\..*)\|$"

        for line in self.to_format:
            # We loop through the different line.

            rematch = rematch_v3 = rematch_v4 = None

            # We extract the different group from our first regex.
            rematch = Regex(
                line, regex, return_data=True, rematch=True, group=0
            ).match()

            # We extract the different group from our fourth regex.
            #
            # Note: We execute the following in second because it is more
            # specific that others.
            rematch_v4 = Regex(
                line, regex_v4, return_data=True, rematch=True, group=0
            ).match()

            # We extract the different group from our third regex.
            rematch_v3 = Regex(
                line, regex_v3, return_data=True, rematch=True, group=0
            ).match()

            if rematch:
                # The first extraction was successfull.

                if self.options_separator in line:
                    options = line.split(self.options_separator)[-1].split(
                        self.option_separator
                    )

                    if (
                        not options[-1]
                        or "third-party" in options
                        or "script" in options
                        or "popup" in options
                        or "xmlhttprequest" in options
                    ):
                        # We extend the result with the extracted elements.
                        result.extend(self._extract_base(rematch))

                    extra = self._handle_options(options)

                    if extra and isinstance(extra, list):  # pragma: no cover
                        extra.extend(self._extract_base(rematch))
                        result.extend(self._extract_base(extra))
                    elif extra:
                        result.extend(self._extract_base(rematch))

                else:
                    # We extend the result with the extracted elements.
                    result.extend(self._extract_base(rematch))

            if rematch_v4:
                # The fourth extraction was successfull.

                # We extend the formatted elements from the extracted elements.
                result.extend(List(self._format_decoded(rematch_v4)).format())

            if rematch_v3:
                # The second extraction was successfull.

                # We extend the formatted elements from the extracted elements.
                result.extend(List(self._format_decoded(rematch_v3)).format())

        # We return the result.
        return List(result).format()

    def _format_decoded(self, to_format, result=None):  # pragma: no cover
        """
        Format the exctracted adblock line before passing it to the system.

        :param str to_format: The extracted line from the file.

        :param list result: A list of the result of this method.

        :return: The list of domains or IP to test.
        :rtype: list
        """

        if not result:
            # The result is not given.

            # We set the result as an empty list.
            result = []

        for data in List(to_format).format():
            # We loop through the different lines to format.

            if data:
                # The currently read line is not empty.

                if "^" in data:
                    # There is an accent in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return self._format_decoded(data.split("^"), result)

                if "#" in data:
                    # There is a dash in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return self._format_decoded(data.split("#"), result)

                if "," in data:
                    # There is a comma in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return self._format_decoded(data.split(","), result)

                if "!" in data:
                    # There is an exclamation mark in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return self._format_decoded(data.split("!"), result)

                if "|" in data:
                    # There is a vertival bar in the currently read line.

                    # We recall this method but with the current result state
                    # and splited data.
                    return self._format_decoded(data.split("|"), result)

                if data:
                    # The currently read line is not empty.

                    data = self._extract_base(data)

                    # We create an instance of the checker.
                    checker = Check(data)

                    if data and (checker.is_domain() or checker.is_ipv4()):
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

        # We return the result element.
        return result
