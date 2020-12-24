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

import functools
import os
from typing import Any, Optional

try:
    import importlib.resources as package_resources
except ImportError:  # pragma: no cover ## Retro compatibility
    import importlib_resources as package_resources

import alembic
import alembic.config
from alembic import command as alembic_command

import PyFunceble.cli.facility
import PyFunceble.cli.storage
import PyFunceble.facility


class Alembic:
    """
    Provides our very own alambic handler.
    """

    alembic_config: Optional[alembic.config.Config] = None

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

    @execute_if_authorized(None)
    def upgrade(self, revision: str = "head") -> "Alembic":
        """
        Upgrades the database structure.

        :param revision:
            The revision to apply.
        """

        PyFunceble.facility.Logger.info(
            "Started update (%r) of the database schema(s).", revision
        )

        self.configure()
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

        PyFunceble.facility.Logger.info(
            "Started downgrade (%r) of the database schema(s).", revision
        )

        self.configure()
        alembic_command.downgrade(self.alembic_config, revision)

        PyFunceble.facility.Logger.info(
            "Finished downgrade (%r) of the database schema(s).", revision
        )