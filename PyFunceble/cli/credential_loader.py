"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our credential loader.

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

import functools
from getpass import getpass
from typing import Any, Optional

import PyFunceble.cli.factory
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.database.credential.base import CredentialBase
from PyFunceble.database.credential.mariadb import MariaDBCredential
from PyFunceble.database.credential.mysql import MySQLCredential
from PyFunceble.database.credential.postgresql import PostgreSQLCredential
from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper


class CredentialLoader:
    """
    Provides our creadential loader.

    The idea is to have an interface which provides the credential to use
    but at the same time load and initiate the credential interface after
    loading it from the user input or the environment variables.

    :param db_type:
        The database type to load the credential for.
    """

    DB_TYPE2OBJ: dict = {
        "csv": None,
        "mysql": MySQLCredential,
        "mariadb": MariaDBCredential,
        "postgresql": PostgreSQLCredential,
    }

    credential: Optional[CredentialBase] = None
    """
    The credential (itself).
    """

    _db_type: Optional[str] = None

    def __init__(self, db_type: Optional[str] = None) -> None:
        if db_type is not None:
            self.db_type = db_type
        elif PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.db_type = PyFunceble.storage.CONFIGURATION.cli_testing.db_type

    def ensure_db_type_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensure that the db type is given before launching the decorated
        method.

        :raise TypeError:
            When the db type is not given.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.db_type, str):
                if PyFunceble.facility.ConfigLoader.is_already_loaded():
                    self.db_type = PyFunceble.storage.CONFIGURATION.cli_testing.db_type
                else:
                    raise TypeError(f"<self.db_type> should be {str}.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

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

    def start_if_not_started(func):  # pylint: disable=no-self-argument
        """
        Launches the start method before launching the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.credential, CredentialBase):
                self.start()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def authorized(self) -> bool:
        """
        Provides the authorization to run.
        """

        return self.db_type != "csv"

    @property
    def db_type(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_db_type` attribute.
        """

        return self._db_type

    @db_type.setter
    def db_type(self, value: str) -> None:
        """
        Sets the database type to work with.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty or not supported.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        value = value.lower()

        if value not in self.DB_TYPE2OBJ:
            raise ValueError(f"<value> ({value!r}) is not supported.")

        self._db_type = value

    def set_db_type(self, value: str) -> "CredentialLoader":
        """
        Sets the database type to work with.

        :param value:
            The value to set.
        """

        self.db_type = value

        return self

    @execute_if_authorized(False)
    def is_already_loaded(self) -> bool:
        """
        Checks if the credential was already loaded.
        """

        return isinstance(self.credential, CredentialBase)

    def set_credential_var(self, var_name: str, value: Any) -> "CredentialLoader":
        """
        Sets the given :code:`var_name` of the credential object with the given
        :code:`value`.

        :param var_name:
            The name of the variable to set.
        :param value:
            The value of to set.
        """

        try:
            setattr(self.credential, var_name, value)
        except TypeError:
            setattr(self.credential, var_name, int(value))

    def ask_for_info(self, var_name: str, default: Any) -> str:
        """
        Asks the credential to the end-user.

        :param var_name:
            The name of the part to ask for example :code:`host` or
            :code:`password`.
        :param default:
            The default value to return if the user don't give us anything.
        """

        message = (
            f"[{self.db_type.upper()}] Please give us your DB {var_name} "
            f"(Default: {default!r}): "
        )

        if var_name == "password":
            user_input = getpass(message)
        else:
            user_input = input(message)

        if user_input:
            return user_input
        return default

    @execute_if_authorized(None)
    @ensure_db_type_is_given
    def start(self, *, ignore_cli: bool = True) -> "CredentialLoader":
        """
        Starts the loading of the credential.

        :param ignore_cli:
            Ignore questions to end-user.
        """

        if not isinstance(self.credential, CredentialBase) and self.authorized:
            # We directly share the credential object into the DBSession object.
            # This will let us use the DBSession without having to think about
            # any other headache.
            self.credential = PyFunceble.cli.factory.DBSession.credential = (
                self.DB_TYPE2OBJ[self.db_type]()
            )

            env_var_helper = EnvironmentVariableHelper(
                env_file_path=self.credential.get_dot_env_file()
            )

            for cred_var, env_var in self.credential.VAR2ENV.items():
                if env_var_helper.set_name(env_var).exists():
                    self.set_credential_var(cred_var, env_var_helper.get_value())
                else:
                    from_file = env_var_helper.get_value_from_env_file()

                    if from_file:
                        self.set_credential_var(cred_var, from_file)
                    elif not ignore_cli:
                        self.set_credential_var(
                            cred_var,
                            self.ask_for_info(
                                cred_var,
                                getattr(self.credential, f"STD_{cred_var.upper()}"),
                            ),
                        )
                    else:
                        self.set_credential_var(
                            cred_var,
                            getattr(self.credential, f"STD_{cred_var.upper()}"),
                        )

                    env_var_helper.set_value_in_env_file(
                        str(getattr(self.credential, cred_var))
                    )

        return self

    @execute_if_authorized("")
    @start_if_not_started
    def get_uri(self) -> str:
        """
        Provides the URI to use.
        """

        return self.credential.get_uri()
