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

from .credential import Credential


class Session:
    """
    Provides our database session interface,
    """

    migration_effective = False

    def __init__(self):
        self.credentials = Credential()
        self.engine = create_engine(
            self.credentials.get_uri(), pool_pre_ping=True, pool_recycle=180
        )
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        self.current_session = None

    def __enter__(self):
        self.create_new_session()

        return self.current_session

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

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

    def create_new_session(self):
        """
        Provides a new session.
        """

        if self.current_session is not None:
            self.current_session.close()
            self.current_session = None

        self.current_session = self.session()

        return self.current_session
