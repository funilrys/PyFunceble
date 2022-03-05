"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all our CI classes.

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

# pylint: disable=too-many-lines

import datetime
import functools
import secrets
from typing import Any, Optional

import PyFunceble.cli.continuous_integration.exceptions
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.helpers.command import CommandHelper
from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper
from PyFunceble.helpers.regex import RegexHelper


class ContinuousIntegrationBase:
    """
    Provides the base of all continuous integration methods.

    :param authorized:
        The authorization to run.
    :param git_email:
        The email to apply while initilizing the git repository for push.
    :param git_name:
        The name to apply while initilizing the git repository for push.
    :param git_branch:
        The branch to use while testing.
    :param git_distribution_branch:
        The branch to push the results into.
    :param token:
        The token to apply while initilizing the git repository for push.
    :param command:
        The command to execute before each push (except the latest one).
    :param end_command:
        The commant to execute at the very end.
    :param commit_message:
        The commit message to apply before each push (except the latest one).
    :param end_commit_message:
        The commit message to apply at the very end.
    :param max_exec_minutes:
        The maximum of minutes to apply before considering the current
        session as finished.
    """

    STD_AUTHORIZED: bool = False
    STD_GIT_EMAIL: Optional[str] = None
    STD_GIT_NAME: Optional[str] = None
    STD_GIT_BRANCH: Optional[str] = "master"
    STD_GIT_DISTRIBUTION_BRANCH: Optional[str] = "master"
    STD_COMMAND: Optional[str] = None
    STD_END_COMMAND: Optional[str] = None
    STD_COMMIT_MESSAGE: str = "PyFunceble - AutoSave"
    STD_END_COMMIT_MESSAGE: str = "PyFunceble - Results"
    STD_MAX_EXEC_MINUTES: int = 15

    end_commit_marker: str = "[ci skip]"

    _authorized: bool = False
    _git_email: Optional[str] = None
    _git_name: Optional[str] = None
    _git_branch: Optional[str] = None
    _git_distribution_branch: Optional[str] = None
    _token: Optional[str] = None
    _command: Optional[str] = None
    _end_command: Optional[str] = None
    _commit_message: Optional[str] = None
    _end_commit_message: Optional[str] = None
    _max_exec_minutes: Optional[int] = None

    start_time: Optional[datetime.datetime] = None
    expected_end_time: Optional[datetime.datetime] = None

    git_initialized: bool = False

    def __init__(
        self,
        *,
        authorized: Optional[bool] = None,
        git_email: Optional[str] = None,
        git_name: Optional[str] = None,
        git_branch: Optional[str] = None,
        git_distribution_branch: Optional[str] = None,
        token: Optional[str] = None,
        command: Optional[str] = None,
        end_command: Optional[str] = None,
        commit_message: Optional[str] = None,
        end_commit_message: Optional[str] = None,
        max_exec_minutes: Optional[int] = None,
    ) -> None:
        if authorized is not None:
            self.authorized = authorized
        else:
            self.guess_and_set_authorized()

        if git_email is not None:
            self.git_email = git_email
        else:
            self.guess_and_set_git_email()

        if git_name is not None:
            self.git_name = git_name
        else:
            self.guess_and_set_git_name()

        if git_branch is not None:
            self.git_branch = git_branch
        else:
            self.guess_and_set_git_branch()

        if git_distribution_branch is not None:
            self.git_distribution_branch = git_distribution_branch
        else:
            self.guess_and_set_git_distribution_branch()

        if token is not None:
            self.token = token
        else:
            self.guess_and_set_token()

        if command is not None:
            self.command = command
        else:
            self.guess_and_set_command()

        if end_command is not None:
            self.end_command = end_command
        else:
            self.guess_and_set_end_command()

        if commit_message is not None:
            self.commit_message = commit_message
        else:
            self.guess_and_set_commit_message()

        if end_commit_message is not None:
            self.end_commit_message = end_commit_message
        else:
            self.guess_and_set_end_commit_message()

        if max_exec_minutes is not None:
            self.max_exec_minutes = max_exec_minutes
        else:
            self.guess_and_set_max_exec_minutes()

    def execute_if_authorized(default: Any = None):  # pylint: disable=no-self-argument
        """
        Executes the decorated method only if we are authorized to process.
        Otherwise, apply the given :code:`default`.
        """

        def inner_metdhod(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.authorized:
                    return func(self, *args, **kwargs)  # pylint: disable=not-callable
                return self if default is None else default

            return wrapper

        return inner_metdhod

    def ensure_git_email_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the Git Email is given before launching the decorated
        method.

        :raise PyFunceble.cli.continuous_integration.exceptions.GitEmailNotFound:
            When the Git Email is not found.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.git_email:
                # pylint: disable=line-too-long
                raise PyFunceble.cli.continuous_integration.exceptions.GitEmailNotFound()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def ensure_git_name_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the Git Name is given before launching the decorated
        method.

        :raise PyFunceble.cli.continuous_integration.exceptions.GitNameNotFound:
            When the Git Name is not found.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.git_name:
                raise PyFunceble.cli.continuous_integration.exceptions.GitNameNotFound()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def ensure_git_branch_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the Git Branch is given before launching the decorated
        method.

        :raise PyFunceble.cli.continuous_integration.exceptions.GitBranchNotFound:
            When the Git Branch is not found.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.git_name:
                raise PyFunceble.cli.continuous_integration.exceptions.GitNameNotFound()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def ensure_git_distribution_branch_is_given(
        func,
    ):  # pylint: disable=no-self-argument,line-too-long
        """
        Ensures that the Git distribution Branch is given before launching the
        decorated method.

        :raise PyFunceble.cli.continuous_integration.exceptions.GitDistributionBranchNotFound:
            When the Git distribution Branch is not found.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.git_name:
                raise PyFunceble.cli.continuous_integration.exceptions.GitNameNotFound()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def ensure_token_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the token is given before launching the decorated method.

        :raise PyFunceble.cli.continuous_integration.exceptions.TokenNotFound:
            When the token is not found.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.token:
                raise PyFunceble.cli.continuous_integration.exceptions.TokenNotFound()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def ensure_start_time_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the starting time is given before launching the decorated
        method.

        :raise PyFunceble.cli.continuous_integration.exceptions.StartTimeNotFound:
            When the token is not found.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.start_time:
                # pylint: disable=line-too-long
                raise PyFunceble.cli.continuous_integration.exceptions.StartTimeNotFound()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def authorized(self) -> Optional[bool]:
        """
        Provides the currently state of the :code:`_authorized` attribute.
        """

        return self._authorized

    @authorized.setter
    def authorized(self, value: bool) -> None:
        """
        Sets the value of the :code:`authorized` attribute.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._authorized = value

    def set_authorized(self, value: bool) -> "ContinuousIntegrationBase":
        """
        Sets the value of the :code:`authorized` attribute.

        :param value:
            The value to set.
        """

        self.authorized = value

        return self

    @property
    def git_email(self) -> Optional[str]:
        """
        Provides the currently state of the :code:`_git_email` attribute.
        """

        return self._git_email

    @git_email.setter
    def git_email(self, value: str) -> None:
        """
        Sets the Git Email to use.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise valueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._git_email = value

    def set_git_email(self, value: str) -> "ContinuousIntegrationBase":
        """
        Sets the Git Email to use.

        :param value:
            The value to set.
        """

        self.git_email = value

        return self

    @property
    def git_name(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_git_name` attribute.
        """

        return self._git_name

    @git_name.setter
    def git_name(self, value: str) -> None:
        """
        Sets the Git Name to use.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise valueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._git_name = value

    def set_git_name(self, value: str) -> "ContinuousIntegrationBase":
        """
        Sets the Git Name to use.

        :param value:
            The value to set.
        """

        self.git_name = value

        return self

    @property
    def git_branch(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_git_branch` attribute.
        """

        return self._git_branch

    @git_branch.setter
    def git_branch(self, value: str) -> None:
        """
        Sets the Git Branch to use.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise valueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._git_branch = value

    def set_git_branch(self, value: str) -> "ContinuousIntegrationBase":
        """
        Sets the Git Branch to use.

        :param value:
            The value to set.
        """

        self.git_branch = value

        return self

    @property
    def git_distribution_branch(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_git_distribution_branch`
        attribute.
        """

        return self._git_distribution_branch

    @git_distribution_branch.setter
    def git_distribution_branch(self, value: str) -> None:
        """
        Sets the Git distribution Branch to use.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise valueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._git_distribution_branch = value

    def set_git_distribution_branch(self, value: str) -> "ContinuousIntegrationBase":
        """
        Sets the Git distribution Branch to use.

        :param value:
            The value to set.
        """

        self.git_distribution_branch = value

        return self

    @property
    def token(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_token` attribute.
        """

        return self._token

    @token.setter
    def token(self, value: str) -> None:
        """
        Sets the token to use.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise valueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._token = value

    def set_token(self, value: str) -> "ContinuousIntegrationBase":
        """
        Sets the token to use.

        :param value:
            The value to set.
        """

        self.token = value

        return value

    @property
    def command(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_command` attribute.
        """

        return self._command

    @command.setter
    def command(self, value: str) -> None:
        """
        Sets the command to work with.

        :param value:
            The command to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empy.")

        self._command = value

    def set_command(self, value: str) -> "ContinuousIntegrationBase":
        """
        Sets the command to work with.

        :param value:
            The command to set.
        """

        self.command = value

        return self

    @property
    def end_command(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_end_command` attribute.
        """

        return self._end_command

    @end_command.setter
    def end_command(self, value: str) -> None:
        """
        Sets the command to execute at the really end of the process with.

        :param value:
            The command to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empy.")

        self._end_command = value

    def set_end_command(self, value: str) -> "ContinuousIntegrationBase":
        """
        Sets the command to execute at the really end of the process with.

        :param value:
            The command to set.
        """

        self.end_command = value

        return self

    @property
    def commit_message(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_commit_message` attribute.
        """

        return self._commit_message

    @commit_message.setter
    def commit_message(self, value: str) -> None:
        """
        Sets the commit message to apply to all commits except the final one.

        :param value:
            The message to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empy.")

        self._commit_message = value

    def set_commit_message(self, value: str) -> "ContinuousIntegrationBase":
        """
        Sets the commit message to apply to all commits except the final one.

        :param value:
            The message to set.
        """

        self.commit_message = value

        return self

    @property
    def end_commit_message(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_end_commit_message` attribute.
        """

        return self._end_commit_message

    @end_commit_message.setter
    def end_commit_message(self, value: str) -> None:
        """
        Sets the commit message to apply to the final one.

        :param value:
            The message to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empy.")

        self._end_commit_message = value

    def set_end_commit_message(self, value: str) -> "ContinuousIntegrationBase":
        """
        Sets the commit message to apply to the final one.

        :param value:
            The command to set.
        """

        self.end_commit_message = value

        return self

    @property
    def max_exec_minutes(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_max_exec_minutes` attribute.
        """

        return self._max_exec_minutes

    @max_exec_minutes.setter
    def max_exec_minutes(self, value: str) -> None:
        """
        Sets the maximum waiting time before considering the time as exceeded.

        :param value:
            The message to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`int`.
        :raise ValueError:
            When the given :code:`value` is less than :code:`1`.
        """

        if not isinstance(value, int):
            raise TypeError(f"<value> should be {int}, {type(value)} given.")

        if value < 1:
            raise ValueError("<value> should be greater or equal to 1.")

        self._max_exec_minutes = value

    def set_max_exec_minutes(self, value: str) -> "ContinuousIntegrationBase":
        """
        Sets the maximum waiting time before considering the time as exceeded.

        :param value:
            The command to set.
        """

        self._max_exec_minutes = value

        return self

    @execute_if_authorized(None)
    def set_start_time(self) -> "ContinuousIntegrationBase":
        """
        Sets the starting time to now.
        """

        self.start_time = datetime.datetime.utcnow()
        self.expected_end_time = self.start_time + datetime.timedelta(
            minutes=self.max_exec_minutes
        )

    @staticmethod
    def get_remote_destination():
        """
        Provides the remote destination to use.

        :raise PyFunceble.cli.continuous_integration.exceptions.RemoteURLNotFound:
            When we could not determine the remote destination.
        """

        regex = r"(?:[a-z]+(?:\s+|\t+))(.*)(?:(?:\s+|\t+)\([a-z]+\))"
        remote_of_interest = [
            x
            for x in CommandHelper("git remote -v").execute().splitlines()
            if "(fetch)" in x
        ][0]

        filtered = RegexHelper(regex).match(
            remote_of_interest, return_match=True, group=1
        )

        if filtered:
            if "@" in filtered:
                return filtered[filtered.find("@") + 1 :]
            if "//" in filtered:
                return filtered[filtered.find("//") + 2 :]

        raise PyFunceble.cli.continuous_integration.exceptions.RemoteURLNotFound()

    @staticmethod
    def exec_command(command: str, allow_stdout: bool) -> None:
        """
        Exceutes the given command.

        :param command:
            The command to execute.

        :param allow_stdout:
            Allows us to return the command output to stdout.
        """

        PyFunceble.facility.Logger.debug("Executing %r", command)

        command_helper = CommandHelper(command)

        if allow_stdout:
            command_helper.run_to_stdout()
        else:
            command_helper.execute()

    def guess_and_set_authorized(self) -> "ContinuousIntegrationBase":
        """
        Tries to guess the authorization.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.authorized = bool(
                PyFunceble.storage.CONFIGURATION.cli_testing.ci.active
            )
        else:
            self.authorized = self.STD_AUTHORIZED

        return self

    def guess_and_set_git_email(self) -> "ContinuousIntegrationBase":
        """
        Tries to guess and set the Git Email.
        """

        environment_var = EnvironmentVariableHelper("GIT_EMAIL")

        if environment_var.exists():
            self.git_email = environment_var.get_value()

        return self

    def guess_and_set_git_name(self) -> "ContinuousIntegrationBase":
        """
        Tries to guess and set the Git Name.
        """

        environment_var = EnvironmentVariableHelper("GIT_NAME")

        if environment_var.exists():
            self.git_name = environment_var.get_value()

        return self

    def guess_and_set_git_branch(self) -> "ContinuousIntegrationBase":
        """
        Tries to guess and set the Git Branch.
        """

        environment_var = EnvironmentVariableHelper("GIT_BRANCH")

        if environment_var.exists():
            self.git_branch = environment_var.get_value()
        elif PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.git_branch = PyFunceble.storage.CONFIGURATION.cli_testing.ci.branch
        else:
            self.git_branch = self.STD_GIT_BRANCH

        return self

    def guess_and_set_git_distribution_branch(self) -> "ContinuousIntegrationBase":
        """
        Tries to guess and set the Git distribution Branch.
        """

        environment_var = EnvironmentVariableHelper("GIT_DISTRIBUTION_BRANCH")

        if environment_var.exists():
            self.git_distribution_branch = environment_var.get_value()
        elif PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.git_distribution_branch = (
                PyFunceble.storage.CONFIGURATION.cli_testing.ci.distribution_branch
            )
        else:
            self.git_distribution_branch = self.STD_GIT_DISTRIBUTION_BRANCH

        return self

    def guess_and_set_token(self) -> "ContinuousIntegrationBase":
        """
        Tries to guess and set the token.
        """

        raise NotImplementedError()

    def guess_and_set_command(self) -> "ContinuousIntegrationBase":
        """
        Tries to guess and set the command to execute.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if PyFunceble.storage.CONFIGURATION.cli_testing.ci.command:
                self.command = PyFunceble.storage.CONFIGURATION.cli_testing.ci.command

        return self

    def guess_and_set_end_command(self) -> "ContinuousIntegrationBase":
        """
        Tries to guess and set the command to execute at the very end.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if PyFunceble.storage.CONFIGURATION.cli_testing.ci.end_command:
                self.end_command = (
                    PyFunceble.storage.CONFIGURATION.cli_testing.ci.end_command
                )

        return self

    def guess_and_set_commit_message(self) -> "ContinuousIntegrationBase":
        """
        Tries to guess and set the commit message to apply.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if PyFunceble.storage.CONFIGURATION.cli_testing.ci.commit_message:
                self.commit_message = (
                    PyFunceble.storage.CONFIGURATION.cli_testing.ci.commit_message
                )
            else:
                self.commit_message = self.STD_COMMIT_MESSAGE
        else:
            self.commit_message = self.STD_COMMIT_MESSAGE

        return self

    def guess_and_set_end_commit_message(self) -> "ContinuousIntegrationBase":
        """
        Tries to guess and set the commit message to apply at the very end.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if PyFunceble.storage.CONFIGURATION.cli_testing.ci.end_commit_message:
                self.end_commit_message = (
                    PyFunceble.storage.CONFIGURATION.cli_testing.ci.end_commit_message
                )
            else:
                self.end_commit_message = self.STD_END_COMMIT_MESSAGE
        else:
            self.end_commit_message = self.STD_END_COMMIT_MESSAGE

        return self

    def guess_and_set_max_exec_minutes(self) -> "ContinuousIntegrationBase":
        """
        Tries to guess and set the maximum execution time.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.max_exec_minutes = (
                PyFunceble.storage.CONFIGURATION.cli_testing.ci.max_exec_minutes
            )
        else:
            self.max_exec_minutes = self.STD_MAX_EXEC_MINUTES

        return self

    def guess_all_settings(self) -> "ContinuousIntegrationBase":
        """
        Try to guess all settings.
        """

        to_ignore = ["guess_all_settings"]

        for method in dir(self):
            if method in to_ignore or not method.startswith("guess_"):
                continue

            getattr(self, method)()

        return self

    def is_authorized(self) -> bool:
        """
        Checks if the current object is authorized to run.
        """

        return self.authorized is True

    @execute_if_authorized(False)
    @ensure_start_time_is_given
    def is_time_exceeded(self) -> bool:
        """
        Checks if we exceeded the allocated time we have.
        """

        return self.expected_end_time < datetime.datetime.utcnow()

    @execute_if_authorized(None)
    @ensure_token_is_given
    def init_git_remote_with_token(self) -> "ContinuousIntegrationBase":
        """
        Initiates the git remote URL with the help of the given token.
        """

        remote = self.get_remote_destination()

        # Each entries should have a tuple containing the command to run and
        # if we are authorized to print to STDOUT.
        commands_to_execute = [
            ("git remote rm origin", False),
            ("git remote add origin " f"https://{self.token}@{remote}", False),
            ("git remote update", False),
            ("git fetch", False),
        ]

        for command, allow_stdout in commands_to_execute:
            self.exec_command(command, allow_stdout)

        return self

    @execute_if_authorized(None)
    @ensure_git_name_is_given
    @ensure_git_email_is_given
    @ensure_git_branch_is_given
    @ensure_git_distribution_branch_is_given
    def init_git(self) -> "ContinuousIntegrationBase":
        """
        Initiate the git repository.
        """

        PyFunceble.facility.Logger.info("Started initialization of GIT.")

        if self.token:
            self.init_git_remote_with_token()

        commands = [
            (f'git config --local user.email "{self.git_email}"', False),
            (f'git config --local user.name "{self.git_name}"', False),
            ("git config --local push.default simple", False),
            ("git config --local pull.rebase true", False),
            ("git config --local core.autocrlf true", False),
            ("git config --local branch.autosetuprebase always", False),
            (f'git checkout "{self.git_branch}"', False),
            ("git fetch origin", False),
            (
                f"git rebase -X theirs " f"origin/{self.git_distribution_branch}",
                False,
            ),
        ]

        for command, allow_stdout in commands:
            self.exec_command(command, allow_stdout)

        self.git_initialized = True

        PyFunceble.facility.Logger.info("Finished initialization of GIT.")

        return self

    def fix_permissions(self) -> "ContinuousIntegrationBase":
        """
        A method to overwrite when custom rules for permissions are needed.

        .. note::
            This method is automatically called by the methods who apply
            commits.
        """

        return self

    @execute_if_authorized(None)
    def push_changes(self, branch: str, *, exit_it: bool = True) -> None:
        """
        Pushes the changes.

        :param branch:
            The branch to push.

        :param exit_it:
            Exits after the push ?

        :raise PyFunceble.cli.continuous_integration.exceptions.StopExecution:
            When the :code:`exit_it` is set to :code:`True`.
        """

        PyFunceble.facility.Logger.info("Started to push GIT changes.")

        commands = []

        if self.git_initialized:
            commands.extend(
                [
                    (
                        f'git checkout "{branch}"',
                        True,
                    ),
                    ("git fetch origin", True),
                    (f"git rebase -X theirs origin/{branch}", True),
                    (f"git push origin {branch}", True),
                ]
            )

        for command, allow_stdout in commands:
            self.exec_command(command, allow_stdout)

        PyFunceble.facility.Logger.info("Finished to push GIT changes.")

        if exit_it:
            raise PyFunceble.cli.continuous_integration.exceptions.StopExecution()

    @execute_if_authorized(None)
    def apply_end_commit(self) -> None:
        """
        Apply the "end" commit and push.

        Side effect:
            It runs the declared command to execute.
        """

        PyFunceble.facility.Logger.info(
            "Started to prepare and apply final GIT commit."
        )

        self.fix_permissions()

        commands = []

        if self.git_distribution_branch != self.git_branch:
            branch_to_use = self.git_distribution_branch
        else:
            branch_to_use = self.git_branch

        if self.end_command:
            commands.append((self.end_command, True))

        if self.git_initialized:
            commands.extend(
                [
                    ("git fetch origin", True),
                    (
                        f"git rebase -X theirs origin/{branch_to_use}",
                        True,
                    ),
                    ("git add --all", True),
                    (
                        "git commit -a -m "
                        f'"{self.end_commit_message} {self.end_commit_marker}\n\n'
                        f'{secrets.token_urlsafe(18)}"',
                        True,
                    ),
                ]
            )

        for command, allow_stdout in commands:
            self.exec_command(command, allow_stdout)

        if self.end_command:
            # Fix permissions because we met some strange behaviors in the past.
            self.fix_permissions()

        PyFunceble.facility.Logger.info(
            "Finished to prepare and apply final GIT commit."
        )

        if self.git_distribution_branch != self.git_branch:
            self.push_changes(branch_to_use)
        else:
            self.push_changes(branch_to_use)

    @execute_if_authorized(None)
    def apply_commit(self) -> None:
        """
        Apply the commit and push.

        Side effect:
            It runs the declared command to execute.
        """

        PyFunceble.facility.Logger.info("Started to prepare and apply GIT commit.")

        self.fix_permissions()

        commands = []

        if self.command:
            commands.append((self.command, True))

        if self.git_initialized:
            commands.extend(
                [
                    ("git add --all", True),
                    (
                        "git commit -a -m "
                        f'"{self.commit_message}\n\n'
                        f'{secrets.token_urlsafe(18)}"',
                        True,
                    ),
                ]
            )

        for command, allow_stdout in commands:
            self.exec_command(command, allow_stdout)

        if self.command:
            # Fix permissions because we met some strange behaviors in the past.
            self.fix_permissions()

        PyFunceble.facility.Logger.info("Finished to prepare and apply GIT commit.")

        self.push_changes(self.git_branch)

    @execute_if_authorized(None)
    def bypass(self) -> None:
        """
        Stops everything if the latest commit message match any of those:

            - :code:`[PyFunceble skip]` (case insensitive)
            - :code:`[PyFunceble-skip]` (case insensitive)
            - :attr:`~PyFunceble.cli.continuous_integration.base.end_commit_marker`
        """

        our_marker = ["[pyfunceble skip]", "[pyfunceble-skip]", self.end_commit_marker]
        latest_commit = CommandHelper("git log -1").execute().lower()

        if any(x.lower() in latest_commit for x in our_marker):
            PyFunceble.facility.Logger.info(
                "Bypass marker caught. Saving and stopping process."
            )

            raise PyFunceble.cli.continuous_integration.exceptions.StopExecution()

    @execute_if_authorized(None)
    def init(self) -> "ContinuousIntegrationBase":
        """
        Initiate our infrastructure for the current CI engine.

        The purpose of this method is to be able to have some custom init based
        on the CI we are currently on.

        The init method should be manually started before runing any further
        action.

        .. warning::
            We assume that we are aware that you should run this method first.
        """

        PyFunceble.facility.Logger.info("Started initizalization of workflow.")

        self.init_git()

        PyFunceble.facility.Logger.info("Finished initizalization of workflow.")

        return self
