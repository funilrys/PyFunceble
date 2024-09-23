"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some facilities for the storage module.

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

import os

from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper
from PyFunceble.utils.platform import PlatformUtility
from PyFunceble.utils.version import VersionUtility


def get_config_directory(
    *, project_name: str, project_version: str
) -> str:  # pragma: no cover ## Not relevant
    """
    Provides the location of the configuration directory.
    """

    # pylint: disable=too-many-branches

    env_var_helper = EnvironmentVariableHelper()
    directory_helper = DirectoryHelper()

    if env_var_helper.set_name("PYFUNCEBLE_CONFIG_DIR").exists():
        config_directory = env_var_helper.get_value()
    elif env_var_helper.set_name("PYFUNCEBLE_OUTPUT_DIR").exists():
        config_directory = env_var_helper.get_value()
    elif (
        VersionUtility(project_version).is_cloned()
        or env_var_helper.set_name("TRAVIS_BUILD_DIR").exists()
        or env_var_helper.set_name("CI_PROJECT_DIR").exists()
        and env_var_helper.set_name("GITLAB_CI").exists()
    ):
        config_directory = directory_helper.get_current(with_end_sep=True)
    else:
        if PlatformUtility.is_unix():
            config_dir_path = os.path.expanduser(os.path.join("~", ".config"))

            if directory_helper.set_path(config_dir_path).exists():
                config_directory = config_dir_path
            elif directory_helper.set_path(os.path.expanduser("~")).exists():
                config_directory = directory_helper.join_path(".")
            else:
                config_directory = directory_helper.get_current(with_end_sep=True)
        elif PlatformUtility.is_windows():
            if env_var_helper.set_name("APPDATA").exists():
                config_directory = env_var_helper.get_value()
            else:
                config_directory = directory_helper.get_current(with_end_sep=True)
        else:
            config_directory = directory_helper.get_current(with_end_sep=True)

        if not config_directory.endswith(os.sep):
            config_directory += os.sep
        config_directory += project_name + os.sep

        if not directory_helper.set_path(config_directory).exists():
            directory_helper.create()

    if not config_directory.endswith(os.sep):
        config_directory += os.sep

    return config_directory
