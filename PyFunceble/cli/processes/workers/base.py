"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all our workers.

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


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025 Nissar Chababy

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

# pylint: disable=import-error,no-name-in-module,no-member

import multiprocessing
from typing import Optional

import sqlalchemy.exc

import PyFunceble.cli.facility
import PyFunceble.cli.factory
import PyFunceble.ext.process_manager
import PyFunceble.facility
import PyFunceble.sessions
import PyFunceble.storage
from PyFunceble.query.requests.requester import Requester


class WorkerBase(PyFunceble.ext.process_manager.WorkerCore):
    """
    Provides the base of all our workers.

    :param input_queue:
        The input queue to read.
    :param output_queue:
        The output queue to write.
    """

    db_session: Optional[PyFunceble.cli.factory.db_session] = None
    requester: Optional[Requester] = None

    def __del__(self) -> None:
        if self.db_session is not None:
            try:
                self.db_session.close()
            except sqlalchemy.exc.OperationalError:
                pass

    def __post_init__(self) -> None:
        self.requester = Requester(config=PyFunceble.storage.CONFIGURATION)
        try:
            self.db_session = (
                PyFunceble.cli.factory.DBSession.get_db_session().get_new_session()()
            )
        except TypeError:
            self.db_session = None

    def perform_external_poweron_checks(self) -> bool:
        """
        Perform the external poweron checks.
        """

        if hasattr(self, "configuration") and self.configuration is not None:
            PyFunceble.facility.ConfigLoader.set_custom_config(self.configuration)

        if (
            multiprocessing.get_start_method() != "fork"
            or not PyFunceble.storage.CONFIGURATION
        ):
            PyFunceble.facility.ConfigLoader.start()
            PyFunceble.cli.facility.CredentialLoader.start()
            PyFunceble.cli.factory.DBSession.init_db_sessions()

        return super().perform_external_poweron_checks()

    def perform_external_preflight_checks(self) -> bool:
        """
        Perform the external preflight checks.
        """

        if (
            hasattr(self, "continuous_integration")
            and self.continuous_integration
            and self.continuous_integration.is_time_exceeded()
        ):
            PyFunceble.facility.Logger.info("CI time exceeded. Stopping worker.")

            if not self.delay_shutdown:
                self.exit_event.set()

            return False

        return super().perform_external_preflight_checks()
