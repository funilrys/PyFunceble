"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides an interface which let us interact with the Public Suffix List.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

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

import os
from typing import Any

import PyFunceble.storage
from PyFunceble.dataset.base import DatasetBase
from PyFunceble.downloader.user_agents import UserAgentsDownloader


class UserAgentDataset(DatasetBase):
    """
    Provides the dataset and infrastructure for the User Agent navigation
    """

    STORAGE_INDEX: str = "USER_AGENTS"
    DOWNLOADER: UserAgentsDownloader = UserAgentsDownloader()

    prefered_browser: str = "chrome"
    prefered_platform: str = "linux"

    def __init__(self) -> None:
        self.source_file = os.path.join(
            PyFunceble.storage.CONFIG_DIRECTORY,
            PyFunceble.storage.USER_AGENT_FILENAME,
        )

    def __contains__(self, value: Any) -> bool:
        return value in self.get_content()

    def __getattr__(self, value: Any) -> dict:
        if value in self:
            return self.get_content()[value]

        return dict()

    def __getitem__(self, value: Any) -> dict:
        return self.__getattr__(value)

    def set_prefered(
        self, browser_short_name: str, platform: str
    ) -> "UserAgentDataset":
        """
        Sets the prefered browser to work with.

        :param browser_short_name:
            The name of the browser to select.
        :pram platform:
            The name of the platform to select.

        :raise TypeError:
            When the given :code:`name` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is not supported.
        """

        if not self.is_supported(browser_short_name, platform):
            raise ValueError(
                f"The given name ({browser_short_name!r}) or platform "
                f"({platform!r}) is not supported."
            )

        self.prefered_browser = browser_short_name.lower()
        self.prefered_platform = platform.lower()

        return self

    def is_supported_browser(self, browser_short_name: str) -> bool:
        """
        Checks if the given browser is supported.

        :raise TypeError:
            When :code:`browser_short_name` is not a :py:class:`str`.
        """

        if not isinstance(browser_short_name, str):
            raise TypeError(
                f"<browser_short_name> should be {str}, "
                f"{type(browser_short_name)} given."
            )

        return bool(browser_short_name.lower() in self) and bool(
            self[browser_short_name.lower()]
        )

    def is_supported(self, browser_short_name: str, platform: str) -> bool:
        """
        Checks if the given browser and platform is supported.

        :param browser_short_name:
            The short name of the browser.

        :param platform:
            The platform name.

        :raise TypeError:
            When :code:`browser_short_name` or :code:`platform` are not :py:class:`str`.
        """

        if not isinstance(browser_short_name, str):
            raise TypeError(
                f"<browser_short_name> should be {str}, "
                f"{type(browser_short_name)} given."
            )

        if not isinstance(platform, str):
            raise TypeError(f"<platform> should be {str}, {type(platform)} given.")

        return (
            self.is_supported_browser(browser_short_name)
            and bool(platform.lower() in self[browser_short_name.lower()])
            and bool(self[browser_short_name.lower()][platform.lower()])
        )

    def get_latest(self) -> str:
        """
        Provides the latest user agent for the given platform.

        Side Effect:
            It tries to get the platform and browser from the configuration
            (if exists).
        """

        if PyFunceble.storage.CONFIGURATION:
            if (
                PyFunceble.storage.CONFIGURATION.user_agent
                and PyFunceble.storage.CONFIGURATION.user_agent.custom
            ):
                return PyFunceble.storage.CONFIGURATION.user_agent.custom

            self.set_prefered(
                PyFunceble.storage.CONFIGURATION.user_agent.browser,
                PyFunceble.storage.CONFIGURATION.user_agent.platform,
            )

        return self[self.prefered_browser][self.prefered_platform]
