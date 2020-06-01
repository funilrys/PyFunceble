"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the environment variable helpers.

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

from os import environ


class EnvironmentVariable:
    """
    Simplify the way we work with environment variable.

    :param str name:
        The name of the environment variable to work with.
    """

    def __init__(self, name):
        self.name = name

    def exists(self, name=None):
        """
        Checks if the given environement variable name exists.

        :param str name
            The name of the environment variable to work with.

            .. note::
                If this is not given, we report to the globally
                give one.

        :rtype: bool
        """

        if name is None:
            name = self.name

        return name in environ

    def get_value(self, name=None, default=None):
        """
        Returns the value of the given environment variable name
        (if exists.)

        :param str name
            The name of the environment variable to work with.

            .. note::
                If this is not given, we report to the globally
                give one.
        :param default: The default value to return.
        """

        if name is None:
            name = self.name

        if self.exists(name=name):
            return environ[name]

        return default

    def set_value(self, value):
        """
        Sets the given value into the given environment variable name.

        :param str value:
            The value to set.
        :raise TypeError: When the value is not a string.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> must be {str}, {type(value)} given.")

        environ[self.name] = value

        return self.exists(name=self.name) and self.get_value(name=self.name) == value
