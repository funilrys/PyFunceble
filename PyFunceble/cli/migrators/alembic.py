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

import functools
import os
from typing import Any, Optional

from sqlalchemy.orm import Session

try:
    import importlib.resources as package_resources
except ImportError:  # pragma: no cover ## Retro compatibility
    import importlib_resources as package_resources

import alembic
import alembic.config
from alembic import command as alembic_command
from alembic.script.base import ScriptDirectory

import PyFunceble.cli.facility
import PyFunceble.cli.factory
import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.sessions
from PyFunceble.cli.migrators.mariadb.base import MariaDBMigratorBase


class Alembic:
    """
    Provides our very own alambic handler.
    """

    db_session: Optional[Session] = None
    migrator_base: Optional[MariaDBMigratorBase] = None

    alembic_config: Optional[alembic.config.Config] = None

    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

        self.migrator_base = MariaDBMigratorBase()
        self.migrator_base.db_session = db_session

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
    def authorized(self):
        """
        Provides the authorization to process.
        """

        # Here we explicitly start because the usage of alembic may be out
        # of our running context.
        return PyFunceble.cli.facility.CredentialLoader.is_already_loaded()

    @property
    def migration_directory(self) -> str:
        """
        Provides the location of our migration directory.
        """

        with package_resources.path(
            f"PyFunceble.data.{PyFunceble.cli.storage.ALEMBIC_DIRECTORY_NAME}",
            "__init__.py",
        ) as file_path:
            return os.path.split(file_path)[0]

    @execute_if_authorized(None)
    def configure(self) -> "Alembic":
        """
        Configure our alembic configuration based on what we need.
        """

        if self.alembic_config is None:
            self.alembic_config = alembic.config.Config()

        self.alembic_config.set_main_option("script_location", self.migration_directory)
        self.alembic_config.set_main_option(
            "sqlalchemy.url",
            PyFunceble.cli.facility.CredentialLoader.get_uri(),
        )

        return self

    def is_revision_different(self, revision: str) -> bool:
        """
        Checks if the given revision is already set.

        :param revision:
            The revision to check
        """

        revision_id = (
            ScriptDirectory.from_config(self.alembic_config)
            .get_revision(revision)
            .revision
        )

        statement = "SELECT * from alembic_version WHERE version_num = :db_revision"

        result = self.db_session.execute(statement, {"db_revision": revision_id})

        return result.fetchone() is None

    @execute_if_authorized(None)
    def upgrade(self, revision: str = "head") -> "Alembic":
        """
        Upgrades the database structure.

        :param revision:
            The revision to apply.
        """

        self.configure()

        if not self.migrator_base.does_table_exists(
            "alembic_version"
        ) or self.is_revision_different(revision):
            PyFunceble.facility.Logger.info(
                "Started update (%r) of the database schema(s).", revision
            )

            alembic_command.upgrade(self.alembic_config, revision)

            PyFunceble.facility.Logger.info(
                "Finished update (%r) of the database schema(s).", revision
            )

    @execute_if_authorized(None)
    def downgrade(self, revision: str = "head") -> "Alembic":
        """
        Upgrades the database structure.

        :param revision:
            The revision to apply.
        """

        self.configure()

        if not self.migrator_base.does_table_exists(
            "alembic_version"
        ) or self.is_revision_different(revision):

            PyFunceble.facility.Logger.info(
                "Started downgrade (%r) of the database schema(s).", revision
            )

            alembic_command.downgrade(self.alembic_config, revision)

            PyFunceble.facility.Logger.info(
                "Finished downgrade (%r) of the database schema(s).", revision
            )
