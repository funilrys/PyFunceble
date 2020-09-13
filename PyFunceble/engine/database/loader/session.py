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
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/master/

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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from .credential import Credential


class Session:
    """
    Provides our database session interface,
    """

    migration_effective = False
    current_session = None
    uri = None

    def __init__(self):
        self.uri = Credential().get_uri()

    def __enter__(self):
        return self.create_new_session()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __make_session(self):
        """
        Provides a new session to work with.
        """

        engine = create_engine(self.uri, poolclass=NullPool)
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def query(self, *args, **kwargs):
        """
        Make a query.
        """

        return self.create_new_session().query(*args, **kwargs)

    def close(self):
        """
        Closes the session.
        """

        if self.current_session is not None:
            # pylint: disable=no-member
            self.current_session.close()

            del self.current_session
            self.current_session = None

    def create_new_session(self):
        """
        Provides a new session.
        """

        # Close a previous connection (if exists).
        self.close()

        self.current_session = self.__make_session()()

        return self.current_session
