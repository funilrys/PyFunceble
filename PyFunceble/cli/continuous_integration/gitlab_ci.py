"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the CI engine and detection tool for the GitLab CI.

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


class GitLabCI(ContinuousIntegrationBase):
    """
    Provides the interface which detects and work under the GitLab CI
    infrastructure.
    """

    def guess_and_set_authorized(self) -> "GitLabCI":
        """
        Tries to guess the authorization.
        """

        needed_environment_vars = ["GITLAB_CI", "GITLAB_USER_ID"]

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

    def guess_and_set_token(self) -> "GitLabCI":
        """
        Tries to guess and set the token.
        """

        environment_var = EnvironmentVariableHelper("GL_TOKEN")

        if environment_var.exists():
            self.token = environment_var.get_value()

        return self

    @ContinuousIntegrationBase.execute_if_authorized(None)
    @ContinuousIntegrationBase.ensure_token_is_given
    def init_git_remote_with_token(self) -> "GitLabCI":
        """
        Initiates the git remote URL with the help of the given token.
        """

        self.token = f"oauth2:{self.token}"
        super().init_git_remote_with_token()

        return self
