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

import copy
import functools
from typing import Any, Optional

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.pool

from PyFunceble.database.credential.base import CredentialBase


class DBSession:
    """
    Provides our very own database session interface and handler.
    """

    credential: Optional[CredentialBase] = None
    current_session: sqlalchemy.orm.Session = None

    def __enter__(self) -> sqlalchemy.orm.Session:
        # Yes we explicitly re-call.
        self.current_session = self.close().get_new_session()()

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

    def get_new_db_session(self) -> "DBSession":
        """
        Provides a new representation of the current object.

        The idea of the new object is that we want to avoid connection issues.
        """

        new_obj = DBSession()
        new_obj.__dict__ = copy.deepcopy(self.__dict__)

        return new_obj

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
            self.current_session.close()

            del self.current_session
            self.current_session = None

        return self

    def query(self, *args, **kwargs) -> Any:
        """
        Makes a query.
        """

        # pylint: disable=no-member
        return self.close().get_new_session()().query(*args, **kwargs)
