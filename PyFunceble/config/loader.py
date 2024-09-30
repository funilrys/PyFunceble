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

import functools
import os
from typing import Any, Optional

try:
    import importlib.resources as package_resources
except ImportError:  # pragma: no cover ## Retro compatibility
    import importlib_resources as package_resources

from box import Box
from dotenv import load_dotenv
from yaml.error import MarkedYAMLError

import PyFunceble.cli.storage
import PyFunceble.storage
from PyFunceble.config.compare import ConfigComparison
from PyFunceble.downloader.iana import IANADownloader
from PyFunceble.downloader.public_suffix import PublicSuffixDownloader
from PyFunceble.downloader.user_agents import UserAgentsDownloader
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.download import DownloadHelper
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

    _path_to_config: Optional[str] = None
    _remote_config_location: Optional[str] = None
    path_to_default_config: Optional[str] = None
    path_to_overwrite_config: Optional[str] = None

    _custom_config: dict = {}
    _merge_upstream: bool = False
    _config_dir: Optional[str] = None

    file_helper: FileHelper = FileHelper()
    dict_helper: DictHelper = DictHelper()

    def __init__(
        self, merge_upstream: Optional[bool] = None, *, config_dir: Optional[str] = None
    ) -> None:
        with package_resources.path(
            "PyFunceble.data.infrastructure",
            PyFunceble.storage.DISTRIBUTED_CONFIGURATION_FILENAME,
        ) as file_path:
            self.path_to_default_config = str(file_path)

        if config_dir is not None:
            self.config_dir = config_dir
        else:
            self.config_dir = PyFunceble.storage.CONFIG_DIRECTORY

        self.path_to_config = os.path.join(
            self.config_dir,
            PyFunceble.storage.CONFIGURATION_FILENAME,
        )

        self.path_to_remote_config = None

        self.path_to_overwrite_config = os.path.join(
            self.config_dir,
            ".PyFunceble.overwrite.yaml",
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
                self.reload(keep_custom=True)

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

        # pylint: disable=too-many-boolean-expressions
        if (
            "cli_testing" in config
            and "ci" in config["cli_testing"]
            and "active" in config["cli_testing"]["ci"]
            and "autocontinue" in config["cli_testing"]
            and bool(config["cli_testing"]["ci"]["active"])
            and not bool(config["cli_testing"]["autocontinue"])
        ):
            # Conditional autocontinue.
            # If we are under continuous integration, the autocontinue should be
            # activated.

            config["cli_testing"]["autocontinue"] = True

        if (
            "lookup" in config
            and "timeout" in config["lookup"]
            and config["lookup"]["timeout"]
            and config["lookup"]["timeout"] < 0
        ):
            # If timeout is set to a negative digit, switch to the default one.
            config["lookup"]["timeout"] = 5

        if (
            "cli_testing" in config
            and "testing_mode" in config["cli_testing"]
            and "platform_contribution" in config["cli_testing"]["testing_mode"]
            and config["cli_testing"]["testing_mode"]["platform_contribution"]
        ):
            # If we are under a special testing mode. We shouldn't generate
            # any files
            config["cli_testing"]["file_generation"]["no_file"] = True
            config["cli_testing"]["display_mode"]["dots"] = True
            config["cli_testing"]["autocontinue"] = False
            config["cli_testing"]["inactive_db"] = False
            config["cli_testing"]["mining"] = False
            config["cli_testing"]["local_network"] = False
            config["cli_testing"]["preload_file"] = False
            config["cli_testing"]["display_mode"]["percentage"] = False
            config["lookup"]["platform"] = False

        return config

    @staticmethod
    def is_already_loaded() -> bool:
        """
        Checks if the configuration was already loaded.
        """

        return bool(PyFunceble.storage.CONFIGURATION)

    @property
    def config_dir(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_config_dir` attribute.
        """

        return self._config_dir

    @config_dir.setter
    @reload_config
    def config_dir(self, value: str) -> None:
        """
        Sets the configuration directory.

        :param value:
            The value to set.

        :raise TypeError:
            When value is not a :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._config_dir = value

    def set_config_dir(self, value: str) -> "ConfigLoader":
        """
        Sets the configuration directory.

        :param value:
            The value to set.
        """

        self.config_dir = value

        return self

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

    @property
    def remote_config_location(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_remote_config_location` attribute.
        """

        return self._remote_config_location

    @remote_config_location.setter
    def remote_config_location(self, value: Optional[str]) -> None:
        """
        Updates the value of :code:`_remote_config_location` attribute.

        :raise TypeError:
            When :code:`value` is not a :py:class:`str`.
        """

        if value is not None and not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value.startswith("http") and not value.startswith("https"):
            self.path_to_remote_config = os.path.realpath(value)
        else:
            self.path_to_remote_config = os.path.join(
                self.config_dir,
                ".PyFunceble.remote.yaml",
            )

        self._remote_config_location = value

    def set_remote_config_location(self, value: Optional[str]) -> "ConfigLoader":
        """
        Updates the value of :code:`_remote_config_location` attribute.
        """

        self.remote_config_location = value

        return self

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

        def download_remote_config(src: str, dest: str = None) -> None:
            """
            Downloads the remote configuration.

            :param src:
                The source to download from.
            :param dest:
                The destination to download
            """

            if src and (src.startswith("http") or src.startswith("https")):
                if dest is None:
                    destination = os.path.join(
                        self.config_dir,
                        os.path.basename(dest),
                    )
                else:
                    destination = dest

                DownloadHelper(src).download_text(destination=destination)

        if not self.is_already_loaded():
            self.install_missing_infrastructure_files()
            self.download_dynamic_infrastructure_files()
            download_remote_config(
                self.remote_config_location, self.path_to_remote_config
            )
            download_remote_config(self.path_to_config)

        try:
            config = self.dict_helper.from_yaml_file(self.path_to_config)
        except MarkedYAMLError:
            self.file_helper.set_path(self.path_to_default_config).copy(
                self.path_to_config
            )
            config = self.dict_helper.from_yaml_file(self.path_to_config)

        config_comparer = ConfigComparison(
            local_config=config,
            upstream_config=self.dict_helper.from_yaml_file(
                self.path_to_default_config
            ),
        )

        if (
            not config
            or not isinstance(config, dict)
            or self.merge_upstream
            or is_3_x_version(config)
            or not config_comparer.is_local_identical()
        ):  # pragma: no cover ## Testing the underlying comparison method is sufficent
            config = config_comparer.get_merged()

            self.dict_helper.set_subject(config).to_yaml_file(self.path_to_config)

        if (
            self.path_to_remote_config
            and self.file_helper.set_path(self.path_to_remote_config).exists()
        ):
            remote_data = self.dict_helper.from_yaml_file(self.path_to_remote_config)

            if isinstance(remote_data, dict):
                config = Merge(remote_data).into(config)

        if self.file_helper.set_path(self.path_to_overwrite_config).exists():
            overwrite_data = self.dict_helper.from_yaml_file(
                self.path_to_overwrite_config
            )

            if isinstance(overwrite_data, dict):
                config = Merge(overwrite_data).into(config)
        else:  # pragma: no cover  ## Just make it visible to end-user.
            self.file_helper.write("")

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

        if entry not in PyFunceble.storage.FLATTEN_CONFIGURATION:
            raise ValueError(f"<entry> ({entry!r}) not in loaded configuration.")

        return PyFunceble.storage.FLATTEN_CONFIGURATION[entry]

    def reload(self, keep_custom: bool = False) -> "ConfigLoader":
        """
        Reloads the configuration.

        :param bool keep_custom:
            If set to :code:`True`, we keep the custom configuration, otherwise
            we delete it.
        """

        self.destroy(keep_custom=keep_custom)
        self.start()

    def start(self) -> "ConfigLoader":
        """
        Starts the loading processIs.
        """

        load_dotenv(os.path.join(self.config_dir, ".env"))
        load_dotenv(os.path.join(self.config_dir, PyFunceble.storage.ENV_FILENAME))

        config = self.get_config_file_content()

        if self.custom_config:
            config = Merge(self.custom_config).into(config)

        config = self.conditional_switch(config)

        PyFunceble.storage.CONFIGURATION = Box(
            config,
        )
        PyFunceble.storage.FLATTEN_CONFIGURATION = DictHelper(
            PyFunceble.storage.CONFIGURATION
        ).flatten()
        PyFunceble.storage.HTTP_CODES = Box(
            config["http_codes"],
        )
        if "platform" in config and config["platform"]:
            PyFunceble.storage.PLATFORM = Box(config["platform"])
        PyFunceble.storage.LINKS = Box(config["links"])

        if "proxy" in config and config["proxy"]:
            PyFunceble.storage.PROXY = Box(config["proxy"])

        return self

    def destroy(self, keep_custom: bool = False) -> "ConfigLoader":
        """
        Destroys everything loaded.

        :param bool keep_custom:
            If set to :code:`True`, we keep the custom configuration, otherwise
            we delete it.
        """

        try:
            PyFunceble.storage.CONFIGURATION = Box(
                {},
            )
            PyFunceble.storage.FLATTEN_CONFIGURATION = {}
            PyFunceble.storage.HTTP_CODES = Box({})
            PyFunceble.storage.PLATFORM = Box({})
            PyFunceble.storage.LINKS = Box({})
            PyFunceble.storage.PROXY = Box({})
        except (AttributeError, TypeError):  # pragma: no cover ## Safety.
            pass

        if not keep_custom:
            # This is not a mistake.
            self._custom_config = {}

        return self
