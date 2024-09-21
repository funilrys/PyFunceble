"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the CI engine and detection tool for standalone instances.

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

import PyFunceble.cli.continuous_integration.exceptions
import PyFunceble.facility
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper


class Standalone(ContinuousIntegrationBase):
    """
    Provides a standalone interface which let end-user run PyFunceble in a standalone
    environment, without any GIT related CI/CD stuff.
    """

    def guess_and_set_authorized(self) -> "Standalone":
        """
        Tries to guess the authorization.
        """

        needed_environment_vars = ["PYFUNCEBLE_STANDALONE_CI"]

        if all(EnvironmentVariableHelper(x).exists() for x in needed_environment_vars):
            self.authorized = True
        elif PyFunceble.facility.ConfigLoader.is_already_loaded():
            if bool(PyFunceble.storage.CONFIGURATION.cli_testing.ci.active):
                self.authorized = all(
                    EnvironmentVariableHelper(x).exists()
                    for x in needed_environment_vars
                )
            else:
                super().guess_and_set_authorized()
        else:
            super().guess_and_set_authorized()

        return self

    def guess_and_set_token(self) -> "Standalone":
        return self

    @ContinuousIntegrationBase.execute_if_authorized(None)
    def init_git(self) -> ContinuousIntegrationBase:
        return self

    @ContinuousIntegrationBase.execute_if_authorized(None)
    def bypass(self) -> None:
        return None

    @ContinuousIntegrationBase.execute_if_authorized(None)
    def init_git_remote_with_token(self) -> "Standalone":
        return self

    @ContinuousIntegrationBase.execute_if_authorized(None)
    def apply_commit(self, *, push: bool = True) -> None:
        return super().apply_end_commit(push=push)
