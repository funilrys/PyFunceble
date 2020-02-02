"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the regular expressions helpers.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

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

from re import compile as re_compile
from re import escape as re_escape
from re import sub as re_sub


class Regex:
    """
    Simplify the regex matching and usage.

    :param str regex: The regex to use.
    :param bool escape: Escapes the given regex.
    """

    def __init__(self, regex, escape=False):
        if escape:
            self.regex = re_escape(regex)
        else:
            self.regex = regex

    def get_not_matching_list(self, data):
        """
        Returns the strings which does not the match the regex
        in the given data.
        """

        pre_result = re_compile(self.regex)

        return [x for x in data if not pre_result.search(str(x))]

    def get_matching_list(self, data):
        """
        Returns the strings which does the match the regex
        in the given data.
        """

        pre_result = re_compile(self.regex)

        return [x for x in data if pre_result.search(str(x))]

    def match(self, data, rematch=False, group=0, return_match=True):
        """
        Checks if the given data match the given regex string.

        :param str data: The data to work with.
        :param bool rematch:
            The equivalent of the $BASH_REMATCH but in Python.

            It's basically a list of all groups.
        :param bool group:
            The group to return when return_match is set to :code:`True`.
        :param bool return_match:
            Return the part that match the given regex string.
        """
        result = []
        to_match = re_compile(self.regex)

        if rematch:
            pre_result = to_match.findall(data)
        else:
            pre_result = to_match.search(data)

        if return_match and pre_result:
            if rematch:
                for res in pre_result:
                    if isinstance(res, tuple):
                        result.extend(list(res))
                    else:
                        result.append(res)

                if group != 0:
                    return result[group]
            else:
                result = pre_result.group(group).strip()

            return result

        if not return_match and pre_result:
            return True
        return False

    def replace_match(self, data, replacement, occurences=0):
        """
        Replaces the string which match the regex string with
        the given replacement.

        :param str data: The data to work with.
        :param str replacement: The replacement of the matched regex.
        :param int occurences:
            The number of occurences to replace.

            .. note::
                :code:`0` means all occurences.

        :rtype: str
        """

        if replacement:
            return re_sub(self.regex, replacement, data, occurences)
        return data
