"""
The tool to check the availability or syntax of domain, IP or URL.

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
    https://pyfunceble.readthedocs.io/en/master/

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


import PyFunceble


class UserAgent:
    """
    A simple interface to get the user agent to use.
    """

    def __init__(self):
        file_instance = PyFunceble.helpers.File(
            PyFunceble.CONFIG_DIRECTORY
            + PyFunceble.abstracts.Infrastructure.USER_AGENT_FILENAME
        )

        if not file_instance.exists():
            PyFunceble.downloader.UserAgents()

        self.dumped = PyFunceble.helpers.Dict().from_json_file(file_instance.path)

    def get(self):
        """
        Provides the user agent to use.
        """

        if "custom" not in PyFunceble.CONFIGURATION.user_agent:
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

        return PyFunceble.CONFIGURATION.user_agent.custom  # pragma: no cover
