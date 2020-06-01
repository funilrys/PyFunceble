"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the Travis CI interface.

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

from itertools import repeat
from os import sep as directory_separator

import PyFunceble

from .base import CIBase


class TravisCI(CIBase):
    """
    Provides the Travis CI preset and initializer.
    """

    def __init__(self):
        self.authorized = self.authorization()
        super().__init__()

    @classmethod
    def authorization(cls):
        """
        Provide the operation authorization.
        """

        return (
            PyFunceble.helpers.EnvironmentVariable("TRAVIS_BUILD_DIR").exists()
            and PyFunceble.CONFIGURATION.ci
        )

    def init(self):
        """
        Init the CI machine/environment.
        """

        if self.authorized:
            gh_token = PyFunceble.helpers.EnvironmentVariable("GH_TOKEN").get_value(
                default=None
            )

            if not gh_token:
                raise PyFunceble.exceptions.GitHubTokenNotFound()

            self.init_git(gh_token)

    def permissions(self):
        """
        Set permissions in order to avoid issues before commiting.
        """

        if self.authorized:
            build_dir = PyFunceble.helpers.EnvironmentVariable(
                "TRAVIS_BUILD_DIR"
            ).get_value()

            commands = [
                f"sudo chown -R travis:travis {build_dir}",
                f"sudo chgrp -R travis {build_dir}",
                f"sudo chmod -R g+rwX {build_dir}",
                f"sudo chmod 777 -Rf {build_dir}{directory_separator}.git",
                f"sudo find {build_dir} -type d -exec chmod g+x '{{}}' \;",  # pylint: disable=anomalous-backslash-in-string
            ]

            self.exec_commands(zip(commands, repeat(False)))

            if (
                PyFunceble.helpers.Command("git config core.sharedRepository").execute()
                == ""
            ):
                PyFunceble.helpers.Command(
                    "git config core.sharedRepository group"
                ).execute()
