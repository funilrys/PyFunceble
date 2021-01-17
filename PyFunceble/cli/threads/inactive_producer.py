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
related to the inactive dataset.

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
from PyFunceble.dataset.inactive.base import InactiveDatasetBase


class InactiveProducerThread(ProducerThreadBase):
    """
    Provides our inactive handler logic.

    The thread behind this object, will read :code:`the_queue`, and produce
    into the inactive dataset.
    """

    thread_name: str = "pyfunceble_inactive_producer"

    dataset: Optional[InactiveDatasetBase] = None

    def __init__(self, output_queue: Optional[queue.Queue] = None) -> None:
        self.dataset = PyFunceble.cli.utils.testing.get_inactive_dataset_object()
        self.dataset.keep_session_open = False

        super().__init__(output_queue=output_queue)

    def run_inactive(self, test_dataset: dict, test_result: CheckerStatusBase) -> None:
        """
        Processes the update of a dataset which was previously inactive.

        The idea is that if the status is OK, we just remove it from the
        database. Otherwise, we just keep it in there :-)
        """

        if test_dataset["type"] != "single":
            inactive_statuses = (
                PyFunceble.storage.STATUS.down,
                PyFunceble.storage.STATUS.invalid,
            )
            dataset = test_result.to_dict()
            dataset.update(test_dataset)

            PyFunceble.facility.Logger.debug("Test Dataset: %r", test_dataset)
            PyFunceble.facility.Logger.debug("Test Result: %r", test_result)

            if "from_inactive" in dataset:
                if test_result.status in self.INACTIVE_STATUSES:
                    if dataset["destination"]:
                        # Note: This handles the case that someone try to test a
                        # single subject.
                        # In fact, we should not generate any file if the output
                        # directory is not given.

                        self.dataset.update(dataset)
                else:
                    self.dataset.remove(dataset)
            elif test_result.status in inactive_statuses and dataset["destination"]:
                self.dataset.update(dataset)

    def target(self) -> None:
        """int
        This is our core logic. Everything starts here!
        """

        stop_message_caught = False

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

            test_dataset, test_result = consumed

            if self.should_we_ignore(test_result):
                continue

            self.run_inactive(test_dataset, test_result)

        if stop_message_caught:
            self.add_to_output_queue("stop")
