"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the configuration loader.

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

import copy
import functools
import os
from typing import Any, Optional

try:
    import importlib.resources as package_resources
except ImportError:  # pragma: no cover ## Retro compatibility
    import importlib_resources as package_resources

from box import Box
from yaml.constructor import ConstructorError

import PyFunceble.cli.storage
import PyFunceble.storage
from PyFunceble.config.compare import ConfigComparison
from PyFunceble.downloader.iana import IANADownloader
from PyFunceble.downloader.public_suffix import PublicSuffixDownloader
from PyFunceble.downloader.user_agents import UserAgentsDownloader
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.merge import Merge


class ConfigLoader:
    """
    Provides the interface which loads and updates the configuration (if needed).

    :param merge_upstream:
        Authorizes the merging of the upstream configuration.

        .. note::
            If value is set to :py:class:`None` (default), we fallback to the
            :code:`PYFUNCEBLE_AUTO_CONFIGURATION` environment variable.
    """

    path_to_config: Optional[str] = None
    path_to_default_config: Optional[str] = None

    _custom_config: dict = dict()
    _merge_upstream: bool = False

    file_helper: FileHelper = FileHelper()
    dict_helper: DictHelper = DictHelper()

    def __init__(self, merge_upstream: Optional[bool] = None) -> None:
        with package_resources.path(
            "PyFunceble.data.infrastructure",
            PyFunceble.storage.DISTRIBUTED_CONFIGURATION_FILENAME,
        ) as file_path:
            self.path_to_default_config = str(file_path)

        self.path_to_config = os.path.join(
            PyFunceble.storage.CONFIG_DIRECTORY,
            PyFunceble.storage.CONFIGURATION_FILENAME,
        )

        if merge_upstream is not None:
            self.merge_upstream = merge_upstream
        elif EnvironmentVariableHelper("PYFUNCEBLE_AUTO_CONFIGURATION").exists():
            self.merge_upstream = True

    def __del__(self) -> None:
        self.destroy()

    def reload_config(func):  # pylint: disable=no-self-argument
        """
        Reload the configuration (if it was already loaded) after launching the
        decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            if self.is_already_loaded():
                self.start()

            return result

        return wrapper

    @staticmethod
    def conditional_switch(config: dict) -> dict:
        """
        Given the configuration that we are going to load, switches some of
        setting.

        :param config:
            The configuration we are going to load.
        """

        # Conditional autocontinue.
        # If we are under continuous integration, the autocontinue should be
        # activated.

        if bool(config["cli_testing"]["ci"]["active"]) and not bool(
            config["cli_testing"]["autocontinue"]
        ):
            config["cli_testing"]["autocontinue"] = True

        return config

    @staticmethod
    def is_already_loaded() -> bool:
        """
        Checks if the configuration was already loaded.
        """

        return bool(PyFunceble.storage.CONFIGURATION)

    @property
    def custom_config(self) -> dict:
        """
        Provides the current state of the :code:`_custom_config` attribute.
        """

        return self._custom_config

    @custom_config.setter
    @reload_config
    def custom_config(self, value: dict) -> None:
        """
        Sets the custom configuration to set after loading.

        Side Effect:
            Directly inject into the configuration variables if it was already
            loaded.

        :raise TypeError:
            When :code:`value` is not a :py:class:`dict`.
        """

        if not isinstance(value, dict):
            raise TypeError(f"<value> should be {dict}, {type(value)} given.")

        if not self._custom_config:
            self._custom_config = value
        else:
            self._custom_config.update(value)

    def set_custom_config(self, value: dict) -> "ConfigLoader":
        """
        Sets the custom configuration to set after loading.

        Side Effect:
            Directly inject into the configuration variables if it was already
            loaded.
        """

        self.custom_config = value

        return self

    @property
    def merge_upstream(self) -> bool:
        """
        Provides the current state of the :code:`_merge_upstream` attribute.
        """

        return self._merge_upstream

    @merge_upstream.setter
    def merge_upstream(self, value: bool) -> None:
        """
        Updates the value of :code:`_merge_upstream` attribute.

        :raise TypeError:
            When :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._merge_upstream = value

    def set_merge_upstream(self, value: bool) -> "ConfigLoader":
        """
        Updates the value of :code:`_merge_upstream` attribute.
        """

        self.merge_upstream = value

        return self

    def config_file_exist(
        self,
    ) -> bool:  # pragma: no cover ## Existance checker already tested.
        """
        Checks if the config file exists.
        """

        return FileHelper(self.path_to_config).exists()

    def default_config_file_exist(
        self,
    ) -> bool:  # pragma: no cover ## Existance checker already tested.
        """
        Checks if the default configuration file exists.
        """

        return self.file_helper.set_path(self.path_to_default_config).exists()

    def install_missing_infrastructure_files(
        self,
    ) -> "ConfigLoader":  # pragma: no cover ## Copy method already tested
        """
        Installs the missing files (when needed).

        .. note::
            Installed if missing:
                - The configuration file.
                - The directory structure file.
        """

        if not self.is_already_loaded():
            if not self.file_helper.set_path(self.path_to_config).exists():
                self.file_helper.set_path(self.path_to_default_config).copy(
                    self.path_to_config
                )

        return self

    @classmethod
    def download_dynamic_infrastructure_files(
        cls,
    ) -> "ConfigLoader":
        """
        Downloads all the dynamicly (generated) infrastructure files.

        .. note::
            Downloaded if missing:
                - The IANA dump file.
                - The Public Suffix dump file.
        """

        ## pragma: no cover ## Underlying download methods already tested.

        if not cls.is_already_loaded():
            IANADownloader().start()
            PublicSuffixDownloader().start()
            UserAgentsDownloader().start()

    def get_config_file_content(self) -> dict:
        """
        Provides the content of the configuration file or the one already loaded.
        """

        def is_3_x_version(config: dict) -> bool:
            """
            Checks if the given configuration is an old one.

            :param config:
                The config to work with.
            """

            return config and "days_between_inactive_db_clean" in config

        if not self.is_already_loaded():
            self.install_missing_infrastructure_files()
            self.download_dynamic_infrastructure_files()

        try:
            config = self.dict_helper.from_yaml_file(self.path_to_config)
        except ConstructorError:
            self.file_helper.set_path(self.path_to_default_config).copy(
                self.path_to_config
            )
            config = self.dict_helper.from_yaml_file(self.path_to_config)

        if (
            not config or self.merge_upstream or is_3_x_version(config)
        ):  # pragma: no cover ## Testing the underlying comparison method is sufficent

            config = ConfigComparison(
                local_config=config,
                upstream_config=self.dict_helper.from_yaml_file(
                    self.path_to_default_config
                ),
            ).get_merged()

            self.dict_helper.set_subject(config).to_yaml_file(self.path_to_config)

        return config

    def get_configured_value(self, entry: str) -> Any:
        """
        Provides the currently configured value.

        :param entry:
            An entry to check.

            multilevel should be separated with a point.

        :raise RuntimeError:
            When the configuration is not loaded yet.

        :raise ValueError:
            When the given :code:`entry` is not found.
        """

        if not self.is_already_loaded():
            raise RuntimeError("Configuration not loaded, yet.")

        flat_config = DictHelper(PyFunceble.storage.CONFIGURATION).flatten()

        if entry not in flat_config:
            raise ValueError(f"<entry> ({entry!r}) not in loaded configuration.")

        return flat_config[entry]

    def start(self) -> "ConfigLoader":
        """
        Starts the loading processIs.
        """

        config = self.get_config_file_content()

        if self.custom_config:
            config = Merge(self.custom_config).into(config)

        config = self.conditional_switch(config)

        PyFunceble.storage.CONFIGURATION = Box(
            copy.deepcopy(config),
        )
        PyFunceble.storage.HTTP_CODES = Box(
            copy.deepcopy(config["http_codes"]),
        )
        PyFunceble.storage.LINKS = Box(
            copy.deepcopy(config["links"]),
        )

        return self

    def destroy(self) -> "ConfigLoader":
        """
        Destroys everything loaded.
        """

        try:
            PyFunceble.storage.CONFIGURATION = Box(
                {},
            )
            PyFunceble.storage.HTTP_CODES = Box({})
            PyFunceble.storage.LINKS = Box({})
        except (AttributeError, TypeError):  # pragma: no cover ## Safety.
            pass

        # This is not a mistake.
        self._custom_config = dict()

        return self
