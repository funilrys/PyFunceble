"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the configuration loader and merger.

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

from functools import wraps
from os import sep as directory_separator
from typing import Optional

from box import Box
from colorama import Fore, Style

import PyFunceble


class Loader:
    """
    Loads the configuration(s) file(s).
    """

    # pylint: disable=too-many-instance-attributes

    UPDATED_LINKS: dict = {
        "psl": "funilrys/PyFunceble",
        "iana": "funilrys/PyFunceble",
    }

    intern: dict = {
        "counter": {
            "number": {"down": 0, "invalid": 0, "tested": 0, "up": 0},
            "percentage": {"down": 0, "invalid": 0, "up": 0},
        },
        "done": Fore.GREEN + "✔",
        "error": Fore.RED + "✘",
    }

    path_to_config: str = None
    path_to_default_config: str = None

    config: Box = Box({}, default_box=True, default_box_attr=None)
    custom_config: dict = dict()
    custom_loaded: dict = dict()

    def __init__(self):
        self.logger: Optional[PyFunceble.engine.Logger] = None
        self.request_lookup: Optional[PyFunceble.lookup.Requests] = None
        self.psl_lookup: Optional[PyFunceble.lookup.PublicSuffix] = None
        self.iana_lookup: Optional[PyFunceble.lookup.Iana] = None
        self.dns_lookup: Optional[PyFunceble.lookup.Dns] = None

        PyFunceble.downloader.Config()

    def empty_custom_config(func):  # pylint: disable=no-self-argument
        """
        Decorator which will empty the custom entries of the configuration
        before calling the wrapped method.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.custom = dict()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def empty_config(func):  # pylint: disable=no-self-argument
        """
        Decorator which will empty the configuration
        before calling the wrapped method.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.config = Box({}, default_box=True, default_box_attr=None)

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def load_all(func):  # pylint: disable=no-self-argument
        """
        Decorator which will load everything before calling
        the wrapped method.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.__load_them_all()  # pylint: disable=protected-access

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def load_config_if_empty(func):  # pylint: disable=no-self-argument
        """
        Decorator which will load the configuration if
        it was not loaded before.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.was_configuration_loaded():
                self.load_all()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def was_configuration_loaded(self) -> bool:
        """
        Checks if the configuration was already loaded.
        """

        to_check = [
            "CONFIGURATION",
            "DNSLOOKUP",
            "HTTP_CODE",
            "IANALOOKUP",
            "INTERN",
            "LINKS",
            "LOADER",
            "LOGGER",
            "OUTPUTS",
            "PSLOOOKUP",
            "REQUESTS",
            "STATUS",
        ]

        return self.config and all(
            [getattr(PyFunceble, x) is not None for x in to_check]
        )

    def set_path_to_config(self, value: str) -> None:
        """
        Sets the path to the configuration file.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value.endswith(directory_separator):
            value += directory_separator

        self.path_to_config = (
            f"{value}{PyFunceble.abstracts.Infrastructure.CONFIGURATION_FILENAME}"
        )
        self.path_to_default_config = (
            f"{value}"
            f"{PyFunceble.abstracts.Infrastructure.DEFAULT_CONFIGURATION_FILENAME}"
        )

    def get_path_to_config(self) -> Optional[str]:
        """
        Provides the path to the configuration file.
        """

        return self.path_to_config

    def get_path_to_default_config(self) -> Optional[str]:
        """
        Provides the path to the default configuration file.
        """

        return self.path_to_default_config

    @empty_custom_config
    def set_custom_config(self, value: dict) -> None:
        """
        Sets the custom configuration to load.
        """

        if value is not None:
            if not isinstance(value, dict):
                raise TypeError(f"<value> should be {dict}, {type(value)} given.")

            self.custom_config = value

            if self.was_configuration_loaded():
                self.config.update(self.custom_config)
                self.custom_loaded.update(self.custom_config)

    def get_custom_config(self) -> Optional[dict]:
        """
        Provides the currently set custom configuration.
        """

        return self.custom_config

    @load_all
    def get_config(self) -> Box:
        """
        Provides the configuration to use.
        """

        return self.config

    def is_current_version_different_from_upstream(self) -> bool:
        """
        Checks if the local is different from the last download upstream
        version.
        """

        local = PyFunceble.helpers.Dict.from_yaml_file(self.path_to_config)
        upstream = PyFunceble.helpers.Dict.from_yaml_file(self.path_to_default_config)

        if not PyFunceble.helpers.Dict(local).has_same_keys_as(upstream):
            return True

        if "links" not in local:
            return True

        for index, value in local["links"].items():
            if (
                index not in self.UPDATED_LINKS
                or self.UPDATED_LINKS[index] not in value
            ):
                continue

            return True

        if "user_agent" not in local:
            return True

        if not isinstance(local["user_agent"], dict):
            return True

        return False

    def __merge_upstream(self):
        """
        Merges the upstream into the local scope.
        """

        old_to_new = {
            "seconds_before_http_timeout": "timout",
            "travis_autosave_final_commit": "travis_autosave_final_commit",
            "travis_autosave_minutes": "travis_autosave_minutes",
            "travis_branch": "ci_branch",
            "travis_distribution_branch": "ci_distribution_branch",
            "travis": "ci",
        }

        local = PyFunceble.helpers.Dict.from_yaml_file(self.path_to_config)
        upstream = PyFunceble.helpers.Dict.from_yaml_file(self.path_to_default_config)

        new_config = PyFunceble.helpers.Merge(local).into(upstream)
        new_config_copy = new_config.copy()

        for old, new in old_to_new.items():
            if old in new_config:
                new_config[new] = new_config_copy[old]

        new_config = PyFunceble.helpers.Dict(new_config).remove_key(
            list(old_to_new.keys())
        )

        for index, value in self.UPDATED_LINKS.items():
            if value in new_config["links"][index]:
                continue

            new_config["links"][index] = upstream["links"][index]

        if not isinstance(local["user_agent"], dict):
            new_config["user_agent"] = upstream["user_agent"]

        PyFunceble.helpers.Dict(new_config).to_yaml_file(self.path_to_config)

        if (
            upstream["links"]["config"]
            != PyFunceble.abstracts.Infrastructure.PROD_CONFIG_LINK
        ):
            PyFunceble.helpers.Dict(upstream).to_yaml_file(self.path_to_default_config)

        self.config.update(new_config)

    @empty_config
    def __load_central_config(self) -> None:
        """
        Loads the central configuration file.
        """

        try:
            file_instance = PyFunceble.helpers.File(self.path_to_config)

            if not file_instance.exists() or file_instance.is_empty():
                raise FileNotFoundError(self.path_to_config)

            self.config.update(
                PyFunceble.helpers.Dict.from_yaml_file(self.path_to_config)
            )
        except (FileNotFoundError, TypeError):
            raise PyFunceble.exceptions.ConfigurationFileNotFound()

        self.fix_paths()
        if (
            self.is_current_version_different_from_upstream()
            and self.are_we_allowed_to_merge_upstream()
        ):
            self.__merge_upstream()

        self.config.update(self.custom_config)
        self.custom_loaded = self.custom_config

    def are_we_allowed_to_install_upstream(self) -> bool:
        """
        Checks if we are allowed to install the upstream configuration.
        """

        if PyFunceble.helpers.EnvironmentVariable(
            "PYFUNCEBLE_AUTO_CONFIGURATION"
        ).exists():
            return True

        while True:
            response = input(
                f"{Style.BRIGHT}{self.path_to_config!r}{Style.RESET_ALL} was not found.\n"
                "Install and load hte default configuration at the mentioned location? [y/n] "
            ).lower()

            if response[0] not in ["y", "n"]:
                continue

            if response[0] == "y":
                return True

            if response[0] == "n":
                return False

            break

        return False

    def are_we_allowed_to_merge_upstream(self) -> bool:
        """
        Checks if we are allowed to merge the upstream configuration.
        """

        if PyFunceble.helpers.EnvironmentVariable(
            "PYFUNCEBLE_AUTO_CONFIGURATION"
        ).exists():
            return True

        while True:
            response = input(
                f"{Style.BRIGHT}{Fore.RED}A configuration key is "
                f"missing or a new version is available.{Style.RESET_ALL}\n"
                f"Try to merge upstream configuration file "
                f"into {Style.BRIGHT}{self.path_to_config!r}{Style.RESET_ALL}? [y/n] "
            ).lower()

            if response[0] not in ["y", "n"]:
                continue

            if response[0] == "y":
                return True

            if response[0] == "n":
                return False

            break

        return False

    def create_config_file_from_upstream(self) -> None:
        """
        Copy the production (upstream) configuration file into the
        one we should use.
        """

        PyFunceble.helpers.File(self.path_to_default_config).copy(self.path_to_config)

    def fix_paths(self) -> None:
        """
        Fixes all the paths. In other words, it ensures the the trailing
        directory separator is always given.
        """

        for main_key in [
            "domains",
            "hosts",
            "splited",
            "json",
            "complements",
            "db_type",
        ]:
            try:
                self.config["outputs"][main_key][
                    "directory"
                ] = PyFunceble.helpers.Directory(
                    self.config["outputs"][main_key]["directory"]
                ).fix_path()
            except KeyError:
                pass

        for main_key in ["analytic", "logs"]:
            for key, value in self.config["outputs"][main_key]["directories"].items():
                self.config["outputs"][main_key]["directories"][
                    key
                ] = PyFunceble.helpers.Directory(value).fix_path()

        self.config["outputs"]["parent_directory"] = PyFunceble.helpers.Directory(
            self.config["outputs"]["parent_directory"]
        ).fix_path()

    @classmethod
    def __download_complementary(cls) -> None:
        """
        Download the complementary files.
        """

        PyFunceble.downloader.IANA()
        PyFunceble.downloader.PublicSuffix()
        PyFunceble.downloader.UserAgents()
        PyFunceble.downloader.DirectoryStructure()

    def inject_all(self) -> None:
        """
        Inject everything at their final location.
        """

        PyFunceble.INTERN = self.intern
        PyFunceble.CONFIGURATION = self.config
        PyFunceble.STATUS = PyFunceble.CONFIGURATION.status
        PyFunceble.OUTPUTS = PyFunceble.CONFIGURATION.outputs
        PyFunceble.HTTP_CODE = PyFunceble.CONFIGURATION.http_codes
        PyFunceble.LINKS = PyFunceble.CONFIGURATION.links

        self.logger = PyFunceble.engine.Logger(debug=PyFunceble.CONFIGURATION.debug)
        PyFunceble.LOGGER = self.logger

        self.__download_complementary()

        self.psl_lookup = PyFunceble.lookup.PublicSuffix()
        PyFunceble.PSLOOOKUP = self.psl_lookup

        self.request_lookup = PyFunceble.lookup.Requests()
        PyFunceble.REQUESTS = self.request_lookup

        self.iana_lookup = PyFunceble.lookup.Iana()
        PyFunceble.IANALOOKUP = self.iana_lookup

        self.dns_lookup = PyFunceble.lookup.Dns(
            dns_server=PyFunceble.CONFIGURATION.dns_server,
            lifetime=PyFunceble.CONFIGURATION.timeout,
            tcp=PyFunceble.CONFIGURATION.dns_lookup_over_tcp,
        )
        PyFunceble.DNSLOOKUP = self.dns_lookup
        PyFunceble.LOADER = self

    def __load_them_all(self) -> None:
        """
        Loads the configuration.
        """

        if "links" not in self.config or "outputs" not in self.config:
            try:
                self.__load_central_config()
            except PyFunceble.exceptions.ConfigurationFileNotFound:
                if not self.are_we_allowed_to_install_upstream():
                    raise PyFunceble.exceptions.ConfigurationFileNotFound()

                self.create_config_file_from_upstream()
                self.__load_central_config()

        self.inject_all()
