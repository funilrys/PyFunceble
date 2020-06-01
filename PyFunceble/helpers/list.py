"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the list helpers

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


class List:
    """
    Simplify the list manipulation.

    :param list main: The main list to work with.
    :param bool remove_empty: Process the deletion of empty strings.
    """

    def __init__(self, main, remove_empty=False):
        if remove_empty:
            self.main = [x for x in main if x is None or x]
        else:
            self.main = main

    def format(self):
        """
        Return a well formatted list. Basicaly, it's sort a list and remove duplicate.

        :return: A sorted, without duplicate, list.
        :rtype: list
        """

        try:
            return sorted(list(set(self.main)), key=str.lower)

        except TypeError:  # pragma: no cover
            return self.main

    def custom_format(self, key_method, reverse=False):
        """
        Return a well formatted list. With the key_method as a function/method to format
        the elements before sorting.

        :param key_method:
            A function or method to use to format the
            readed element before sorting.
        :type key_method: function|method

        :param bool reverse: Tell us if we have to reverse the list.

        :return: A sorted list.
        :rtype: list
        """

        try:
            return sorted(list(set(self.main)), key=key_method, reverse=reverse)
        except TypeError:  # pragma: no cover
            return self.main
