"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the logic behind the threads which is supposed to handle everything
related to the WHOIS dataset.

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

import datetime
import queue
from typing import Optional

import PyFunceble.checker.utils.whois
import PyFunceble.cli.storage
import PyFunceble.cli.utils.stdout
import PyFunceble.cli.utils.testing
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.cli.threads.producer_base import ProducerThreadBase
from PyFunceble.dataset.whois.base import WhoisDatasetBase


class WhoisProducerThread(ProducerThreadBase):
    """
    Provides our WHOIS dataset handler logic.

    The thread behind this object, will read :code:`the_queue`, and produce
    into the whois dataset.
    """

    thread_name: str = "pyfunceble_whois_producer"

    dataset: Optional[WhoisDatasetBase] = None

    def __init__(self, output_queue: Optional[queue.Queue] = None) -> None:
        self.dataset = PyFunceble.checker.utils.whois.get_whois_dataset_object()
        self.dataset.keep_session_open = False

        super().__init__(output_queue=output_queue)

    def run_whois_backup(self, test_result: CheckerStatusBase) -> None:
        """
        Runs the WHOIS record backup.

        :param test_result:
            The test result object.
        """

        if (
            hasattr(test_result, "expiration_date")
            and test_result.expiration_date
            and test_result.whois_record
        ):
            # Note: The whois record is always given if the status does not come
            # from the database.

            self.dataset.update(
                {
                    "subject": test_result.subject,
                    "idna_subject": test_result.idna_subject,
                    "expiration_date": test_result.expiration_date,
                    "epoch": str(
                        datetime.datetime.strptime(
                            test_result.expiration_date, "%d-%b-%Y"
                        ).timestamp()
                    ),
                }
            )

    def target(self) -> None:
        """int
        This is our core logic. Everything starts here!
        """

        stop_message_caught = False

        # We starts with the cleanup of unneeded WHOIS records.
        # WARNING: People using the API should be aware that this should be
        # done before playing with our system. The cleanup is executed only
        # on purpose and not automaticaly, like we used to do in the past.
        self.dataset.cleanup()

        while self.dataset.authorized:
            if self.the_queue.empty():
                continue

            consumed = self.the_queue.get()

            PyFunceble.facility.Logger.debug("Got: %r", consumed)

            if consumed == "stop":
                PyFunceble.facility.Logger.info(
                    "Got stop message. Stopping reading from the queue."
                )

                stop_message_caught = True
                break

            if not isinstance(consumed, tuple):
                continue

            PyFunceble.facility.Logger.debug("Got: %r", consumed)

            _, test_result = consumed

            if self.should_we_ignore(test_result):
                continue

            self.run_whois_backup(test_result)

        if stop_message_caught:
            self.add_to_output_queue("stop")
