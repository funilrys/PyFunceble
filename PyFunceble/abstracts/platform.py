"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a simple way to get the current platform.

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

from platform import system


class Platform:  # pragma: no cover
    """
    Provides an easy way to get the current platform.
    """

    WINDOWS = ["windows", "cygwin", "cygwin_nt-10.0"]
    """
    Provides the list of supported windows platform.

    :type: list
    """

    UNIX = ["linux", "darwin"]
    """
    Provides the list of supported unix platform.

    :type: list
    """

    MAC = ["darwin"]
    """
    Provides the list of supported MAC platform.

    :type: list
    """

    @classmethod
    def get(cls):
        """
        Returns the current platform.

        :rtype: str
        """

        return system().lower()

    @classmethod
    def is_windows(cls):
        """
        Checks if the current platform is in our windows list.

        :rtype: bool
        """

        return cls.get() in cls.WINDOWS

    @classmethod
    def is_unix(cls):
        """
        Checks if the current platform is in our unix list.

        :rtype: bool
        """

        return cls.get() in cls.UNIX  # pragma: no cover

    @classmethod
    def is_mac_os(cls):
        """
        Checks if the current platform is in our OSX list.

        :rtype: bool
        """

        return cls.get() in cls.MAC
