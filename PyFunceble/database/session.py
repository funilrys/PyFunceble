"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our database session interface.

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

import functools
from typing import Any, Optional

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.pool

import PyFunceble.sessions
from PyFunceble.database.credential.base import CredentialBase


class DBSession:
    """
    Provides our very own database session interface and handler.
    """

    credential: Optional[CredentialBase] = None
    current_session: sqlalchemy.orm.Session = None

    def __enter__(self) -> sqlalchemy.orm.Session:
        # Yes we explicitly re-call.
        self.current_session = self.close().get_db_session()

        return self.current_session

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def ensure_credential_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that a credential object is set before launching the
        decorated method.

        :raise TypeError:
            When :code:`credential` is not correct.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.credential, CredentialBase):
                raise TypeError(
                    f"<self.credential> should be {CredentialBase}, "
                    f"{type(self.credential)} given."
                )

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

    @property
    def authorized(self) -> bool:
        """
        Provides the authorization to operate.
        """

        return self.credential is not None

    @execute_if_authorized(None)
    @ensure_credential_is_given
    def init_global_session(self) -> "DBSession":
        """
        Initiate the global session to work with.
        """

        PyFunceble.sessions.DB_ENGINE = sqlalchemy.create_engine(
            self.credential.get_uri(), poolclass=sqlalchemy.pool.NullPool
        )

        PyFunceble.sessions.DB_FACTORY = sqlalchemy.orm.sessionmaker(
            autocommit=False, autoflush=False, bind=PyFunceble.sessions.DB_ENGINE
        )

        PyFunceble.sessions.DB_SESSION = sqlalchemy.orm.scoped_session(
            PyFunceble.sessions.DB_FACTORY
        )

        return self

    @execute_if_authorized(None)
    def get_db_session(self):
        """
        Provides a new session.
        """

        if PyFunceble.sessions.DB_SESSION is None:
            self.init_global_session()

        return PyFunceble.sessions.DB_SESSION()

    @execute_if_authorized(None)
    @ensure_credential_is_given
    def get_new_session(self) -> sqlalchemy.orm.sessionmaker:
        """
        Creates and returns a new session.

        .. warning::
            This method generate a new session without any pool of connections.
        """

        engine = sqlalchemy.create_engine(
            self.credential.get_uri(), poolclass=sqlalchemy.pool.NullPool
        )

        return sqlalchemy.orm.sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

    @execute_if_authorized(None)
    @ensure_credential_is_given
    def get_new_pool_session(self) -> sqlalchemy.orm.sessionmaker:
        """
        Create and return a new session.
        """

        engine = sqlalchemy.create_engine(
            self.credential.get_uri(),
        )

        return sqlalchemy.orm.sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

    def close(self) -> "DBSession":
        """
        Closes the session if exists.
        """

        if self.current_session is not None:
            try:
                PyFunceble.sessions.DB_SESSION.remove()
            except AttributeError:
                self.current_session.close()

            del self.current_session
            self.current_session = None

        return self

    @execute_if_authorized(None)
    def query(self, *args, **kwargs) -> Any:
        """
        Makes a query.
        """

        # pylint: disable=no-member
        return self.close().get_new_session()().query(*args, **kwargs)
