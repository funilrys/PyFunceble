"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the merging helpers.

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


class Merge:
    """
    Simplify the merging of dict and list.

    :param main: The main data to work with.
    :type main: str, tuple, bool, int, dict, list, float
    """

    def __init__(self, main):
        self.main = main

    def __list(self, origin, strict=True):
        """
        Process the list merging.

        :param bool strict:
            Activates the strict mode.

        :rtype: list
        """

        result = []

        if strict:
            for index, element in enumerate(self.main):
                try:
                    if isinstance(element, dict) and isinstance(origin[index], dict):
                        result.append(Merge(element).into(origin[index], strict=strict))
                    elif isinstance(element, list) and isinstance(origin[index], list):
                        result.append(Merge(element).into(origin[index], strict=strict))
                    else:
                        result.append(element)
                except IndexError:  # pragma: no cover
                    result.append(element)
        else:
            result = origin

            for element in self.main:
                if element not in result:
                    result.append(element)

        return result

    def __dict(self, origin, strict=True):
        """
        Process the dict merging.

        :param bool strict:
            Activates the strict mode.

        :rtype: dict
        """

        result = {}

        for index, data in self.main.items():
            if index in origin:
                if isinstance(data, dict) and isinstance(origin[index], dict):
                    result[index] = Merge(data).into(origin[index], strict=strict)
                elif isinstance(data, list) and isinstance(origin[index], list):
                    result[index] = Merge(data).into(origin[index], strict=strict)
                else:
                    result[index] = data
            else:
                result[index] = data

        for index, data in origin.items():
            if index not in result:
                result[index] = data

        return result

    def into(self, origin, strict=True):
        """
        Process the mergin.

        :param origin: The original data.
        :param bool strict:
            Activates the strict mode.
        """

        try:
            origin = origin.copy()
        except AttributeError:
            pass

        if isinstance(self.main, list) and isinstance(origin, list):
            return self.__list(origin, strict=strict)

        if isinstance(self.main, dict) and isinstance(origin, dict):
            return self.__dict(origin, strict=strict)

        return self.main  # pragma: no cover
