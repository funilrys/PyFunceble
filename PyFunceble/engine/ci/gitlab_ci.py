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
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
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
