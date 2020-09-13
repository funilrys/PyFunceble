"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our very own alembic interface.

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

from alembic import command
from alembic.config import Config
from pkg_resources import resource_filename

import PyFunceble

from .old2new import CleanupOldTables


class Alembic:
    """
    Provides our very own alambic handler.

    :param credentials:
        A credentials instance
    """

    configured = False
    alembic_config = None

    def __init__(self, credentials):
        self.migration_directory = resource_filename(
            f"PyFunceble.data.{PyFunceble.abstracts.Infrastructure.ALEMBIC_DIRECTORY_NAME}",
            "__init__.py",
        ).replace("__init__.py", "")

        self.credentials = credentials
        self.configure()

    @property
    def authorized(self):
        """
        Provides the authorization to run.
        """

        return PyFunceble.CONFIGURATION.db_type in ["mysql", "mariadb"]

    def configure(self):
        """
        Configures alembic for our needs.
        """

        if self.authorized:
            if self.alembic_config is None:
                self.alembic_config = Config()

            self.alembic_config.set_main_option(
                "script_location", self.migration_directory
            )
            self.alembic_config.set_main_option(
                "sqlalchemy.url", self.credentials.get_uri()
            )

    def upgrade(self, revision="head"):
        """
        Upgrades the database structure.
        """

        if self.authorized:
            command.upgrade(self.alembic_config, revision)

            CleanupOldTables(self.credentials).start()

    def downgrade(self, revision="head"):
        """
        Downgrades the database structure.
        """

        if self.authorized:
            command.downgrade(self.alembic_config, revision)
