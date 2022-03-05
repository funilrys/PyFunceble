"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the CI engine and detection tool for the GitHub Actions.

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


    Copyright 2017, 2018, 2019, 2020, 2022 Nissar Chababy

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

import PyFunceble.facility
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper


class GitHubActions(ContinuousIntegrationBase):
    """
    Provides the interface which detects and work under the GitHub Actions
    infrastructure.
    """

    end_commit_marker: str = "[GHA skip]"

    def guess_and_set_authorized(self) -> "GitHubActions":
        """
        Tries to guess the authorization.
        """

        needed_environment_vars = ["GITHUB_ACTIONS"]

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if bool(PyFunceble.storage.CONFIGURATION.cli_testing.ci.active):
                self.authorized = all(
                    EnvironmentVariableHelper(x).exists()
                    for x in needed_environment_vars
                )
            else:
                super().guess_and_set_authorized()
        elif all(
            EnvironmentVariableHelper(x).exists() for x in needed_environment_vars
        ):
            self.authorized = True
        else:
            super().guess_and_set_authorized()

        return self

    def guess_and_set_token(self) -> "GitHubActions":
        """
        Tries to guess and set the token.
        """

        environment_var = EnvironmentVariableHelper("GITHUB_TOKEN")

        if environment_var.exists():
            self.token = environment_var.get_value()

        return self
