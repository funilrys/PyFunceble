"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the GitLab CI/CD interface.

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

import PyFunceble

from .base import CIBase


class GitLabCI(CIBase):
    """
    Provides the GitLab CI preset and initializer.
    """

    def __init__(self):
        self.authorized = self.authorization()
        super().__init__()

    @classmethod
    def authorization(cls):
        needed_environment_vars = ["GITLAB_CI", "GITLAB_USER_ID"]

        return (
            all(
                [
                    PyFunceble.helpers.EnvironmentVariable(x).exists()
                    for x in needed_environment_vars
                ]
            )
            and PyFunceble.CONFIGURATION.ci
        )

    def init_git_remote_with_token(self, token):
        """
        Provides a simple way to initiate the git remote url.

        :param str token: A token with push access.
        """

        if self.authorized:
            remote = self.get_remote_destination()

            commands = [
                ("git remote rm origin", True),
                ("git remote add origin " f"https://oauth2:{token}@{remote}", False),
                ("git remote update", False),
                ("git fetch", False),
            ]

            self.exec_commands(commands)

    def init(self):
        """
        Initiate the CI machine/environment.
        """

        if self.authorized:
            gl_token = PyFunceble.helpers.EnvironmentVariable("GL_TOKEN").get_value(
                default=None
            )

            if not gl_token:
                raise PyFunceble.exceptions.GitLabTokenNotFound()

            self.init_git(gl_token)
