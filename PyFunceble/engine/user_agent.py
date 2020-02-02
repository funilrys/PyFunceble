"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a simple way to get the latest or the defined User-Agent.

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


import PyFunceble


class UserAgent:
    """
    A simple interface to get the user agent to use.
    """

    def __init__(self):
        self.dumped = PyFunceble.helpers.Dict().from_json_file(
            PyFunceble.CONFIG_DIRECTORY
            + PyFunceble.abstracts.Infrastructure.USER_AGENT_FILENAME
        )

    def get(self):
        """
        Provides the user agent to use.
        """

        if not PyFunceble.CONFIGURATION.user_agent.custom:
            if (
                not PyFunceble.CONFIGURATION.user_agent.browser
                or PyFunceble.CONFIGURATION.user_agent.browser not in self.dumped
            ):
                raise PyFunceble.exceptions.UserAgentBrowserNotFound(
                    PyFunceble.CONFIGURATION.user_agent.browser
                )

            if (
                not PyFunceble.CONFIGURATION.user_agent.platform
                or PyFunceble.CONFIGURATION.user_agent.platform
                not in self.dumped[PyFunceble.CONFIGURATION.user_agent.browser]
            ):
                raise PyFunceble.exceptions.UserAgentPlatformNotFound(
                    PyFunceble.CONFIGURATION.user_agent.platform
                )

            if not self.dumped[PyFunceble.CONFIGURATION.user_agent.browser][
                PyFunceble.CONFIGURATION.user_agent.platform
            ]:
                raise PyFunceble.exceptions.UserAgentNotFound(
                    "Browser: "
                    f"{PyFunceble.CONFIGURATION.user_agent.browser}; "
                    f"Platform: {PyFunceble.CONFIGURATION.user_agent.platform}"
                )

            return self.dumped[PyFunceble.CONFIGURATION.user_agent.browser][
                PyFunceble.CONFIGURATION.user_agent.platform
            ]

        return PyFunceble.CONFIGURATION.user_agent.custom
