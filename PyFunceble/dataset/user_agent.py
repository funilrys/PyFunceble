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
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import secrets
from typing import Any, Optional
from warnings import warn

import PyFunceble.storage
from PyFunceble.dataset.base import DatasetBase
from PyFunceble.downloader.user_agents import UserAgentsDownloader


class UserAgentDataset(DatasetBase):
    """
    Provides the dataset and infrastructure for the User Agent navigation
    """

    STORAGE_INDEX: str = "USER_AGENTS"
    downloader: Optional[UserAgentsDownloader] = None

    preferred_browser: str = "chrome"
    preferred_platform: str = "linux"

    def __init__(self) -> None:
        self.downloader = UserAgentsDownloader()
        self.source_file = self.downloader.destination

    def __contains__(self, value: Any) -> bool:
        content = self.get_content()

        if "@modern" in content:
            return value in self.get_content()["@modern"]
        return value in self.get_content()

    def __getattr__(self, value: Any) -> dict:
        if value in self:
            content = self.get_content()

            if "@modern" in content:
                return self.get_content()["@modern"][value]
            return self.get_content()[value]

        return dict()  # pylint: disable=use-dict-literal

    def __getitem__(self, value: Any) -> dict:
        return self.__getattr__(value)

    def set_preferred(
        self, browser_short_name: str, platform: str
    ) -> "UserAgentDataset":
        """
        Sets the preferred browser to work with.

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

        self.preferred_browser = browser_short_name.lower()
        self.preferred_platform = platform.lower()

        return self

    # @deprecated("TODO: Soon we should be able to do this...")
    def set_prefered(
        self, browser_short_name: str, platform: str
    ) -> "UserAgentDataset":
        """
        Sets the preferred browser to work with.

        :param browser_short_name:
            The name of the browser to select.
        :pram platform:
            The name of the platform to select.

        :raise TypeError:
            When the given :code:`name` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is not supported.
        """

        warn(
            "The set_prefered() method is deprecated and will be removed in future "
            " releases. Please consider using the set_preferred() method instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.set_preferred(browser_short_name, platform)

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

            self.set_preferred(
                PyFunceble.storage.CONFIGURATION.user_agent.browser,
                PyFunceble.storage.CONFIGURATION.user_agent.platform,
            )

        result = self[self.preferred_browser][self.preferred_platform]

        if isinstance(result, (list, tuple)):
            return secrets.choice(result)

        return result
