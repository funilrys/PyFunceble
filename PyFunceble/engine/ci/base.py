"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base to all CI engines.

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

import sys

import PyFunceble


class CIBase:
    """
    Provides a base for all CI engines.
    """

    authorized = False

    # We set the regex to match in order to bypass the execution of
    # PyFunceble.
    regex_bypass = r"\[PyFunceble\sskip\]"

    def __init__(self):
        self.git_email = PyFunceble.helpers.EnvironmentVariable("GIT_EMAIL").get_value(
            default=None
        )

        self.git_name = PyFunceble.helpers.EnvironmentVariable("GIT_NAME").get_value(
            default=None
        )

    def authorization(self):
        """
        Provides the operation authorization.
        """

        raise NotImplementedError()

    def permissions(self):
        """
        Provides a permission fixer.
        """

    def git_var_checker(self):
        """
        Process some checks of the git related variables.
        """

        if self.authorized:
            if not self.git_email:
                raise PyFunceble.exceptions.GitEmailNotFound()

            if not self.git_name:
                raise PyFunceble.exceptions.GitNameNotFound()

    def init_git_remote_with_token(self, token):
        """
        Provides a simple way to initiate the git remote url.

        :param str token: A token with push access.
        """

        if self.authorized:
            remote = self.get_remote_destination()

            commands = [
                ("git remote rm origin", False),
                ("git remote add origin " f"https://{token}@{remote}", False),
                ("git remote update", False),
                ("git fetch", False),
            ]

            self.exec_commands(commands)

    def init_git(self, token):
        """
        Initiate the git project/repository.
        """

        if self.authorized:
            self.git_var_checker()
            self.init_git_remote_with_token(token)

            commands = [
                (f'git config --global user.email "{self.git_email}"', False),
                (f'git config --global user.name "{self.git_name}"', False),
                ("git config --global push.default simple", False),
                (f'git checkout "{PyFunceble.CONFIGURATION.ci_branch}"', False),
                (
                    f'git pull origin "{PyFunceble.CONFIGURATION.ci_distribution_branch}"',
                    False,
                ),
            ]

            self.exec_commands(commands)

    def init(self):
        """
        Init the CI machine/environment.
        """

        raise NotImplementedError()

    @classmethod
    def get_remote_destination(cls):
        """
        Provides the remote destination to use.
        """

        regex = r"(?:[a-z]+(?:\s+|\t+))(.*)(?:(?:\s+|\t+)\([a-z]+\))"
        remote_of_interest = [
            x
            for x in PyFunceble.helpers.Command("git remote -v").execute().splitlines()
            if "(fetch)" in x
        ][0]

        filtered = PyFunceble.helpers.Regex(regex).match(
            remote_of_interest, return_match=True, group=1
        )

        if filtered and "@" in filtered:
            return filtered[filtered.find("@") + 1 :]

        if filtered and "//" in filtered:
            return filtered[filtered.find("//") + 2 :]

        raise ValueError("Could not find remote.")

    @classmethod
    def exec_commands(cls, commands):
        """
        Execute a set of commands.

        :param list commands: A list of command to run.
        """

        for command, allow_stdout in commands:
            if allow_stdout or PyFunceble.LOGGER.authorized:
                PyFunceble.LOGGER.debug(f"Executing: {repr(command)}")
                PyFunceble.helpers.Command(command).run_to_stdout()
            else:
                PyFunceble.helpers.Command(command).execute()

    def bypass(self):
        """
        Stop everything if :code:`[PyFunceble skip]` is matched into
        the latest commit message.
        """

        if self.authorized and PyFunceble.helpers.Regex(self.regex_bypass).match(
            PyFunceble.helpers.Command("git log -1").execute(), return_match=False
        ):

            PyFunceble.LOGGER.info("Bypass given. Ending process.")

            self.end_commit()

    def push(self, exit_it=True):
        """
        Push.

        :param bool exit_it: Allow us to directly exit after pushing.
        """

        if self.authorized:

            commands = [
                (f"git push origin {PyFunceble.CONFIGURATION.ci_branch}", False)
            ]

            self.exec_commands(commands)

            if exit_it:
                sys.exit(0)

    def end_commit(self):
        """
        Commit and push at the very end of the test.
        """

        if self.authorized:
            PyFunceble.output.Percentage().log()
            self.permissions()

            commands = [
                ("git add --all", True),
                (
                    "git commit -a -m "
                    f'"{PyFunceble.CONFIGURATION.ci_autosave_final_commit} [ci skip]"',
                    True,
                ),
            ]

            if PyFunceble.CONFIGURATION.command_before_end:
                PyFunceble.LOGGER.info(
                    f"Executing: {PyFunceble.CONFIGURATION.command_before_end}"
                )

                PyFunceble.helpers.Command(
                    PyFunceble.CONFIGURATION.command_before_end
                ).run_to_stdout()
                self.permissions()

            self.exec_commands(commands)

            if (
                PyFunceble.CONFIGURATION.ci_distribution_branch
                != PyFunceble.CONFIGURATION.ci_branch
            ):
                self.push(exit_it=False)

                # We now merge to the destination branch.
                commands = [
                    (
                        f'git checkout "{PyFunceble.CONFIGURATION.ci_distribution_branch}"',
                        True,
                    ),
                    (f'git pull origin "{PyFunceble.CONFIGURATION.ci_branch}"', False),
                    (
                        f'git push origin "{PyFunceble.CONFIGURATION.ci_distribution_branch}"',
                        False,
                    ),
                ]

                self.exec_commands(commands)
                sys.exit(0)
            else:
                self.push()

    def not_end_commit(self):
        """
        Commit and push at on the middle of the test.
        """

        if self.authorized:
            PyFunceble.output.Percentage().log()
            self.permissions()

            command = 'git add --all && git commit -a -m "{0}"'.format(
                PyFunceble.CONFIGURATION.ci_autosave_commit
            )

            if PyFunceble.CONFIGURATION.command:
                PyFunceble.LOGGER.info(f"Executing: {PyFunceble.CONFIGURATION.command}")

                PyFunceble.helpers.Command(
                    PyFunceble.CONFIGURATION.command
                ).run_to_stdout()
                self.permissions()

            PyFunceble.LOGGER.info(f"Executing: {command}")

            PyFunceble.helpers.Command(command).run_to_stdout()

            self.push()
