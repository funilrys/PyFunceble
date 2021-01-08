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
related to the autocontinue.

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
from PyFunceble.dataset.autocontinue.base import ContinueDatasetBase
from PyFunceble.dataset.autocontinue.csv import CSVContinueDataset


class ContinueProducerThread(ProducerThreadBase):
    """
    Provides our autocontienue handler logic.

    The thread behind this object, will read :code:`the_queue`, and produce
    into the autocontinue dataset.
    """

    thread_name: str = "pyfunceble_continue_producer"

    dataset: Optional[ContinueDatasetBase] = None

    def __init__(self, output_queue: Optional[queue.Queue] = None) -> None:
        self.dataset = PyFunceble.cli.utils.testing.get_continue_databaset_object()
        self.dataset.keep_session_open = False

        super().__init__(output_queue=output_queue)

    def run_continue(self, test_dataset: dict, test_result: CheckerStatusBase) -> None:
        """
        Reads the given test dataset, interpret it and add the given test
        result to the dataset if needed.

        :param test_dataset:
            The test dataset as per protocol.

        :param test_result_dict:
            The test result object.
        """

        if test_dataset["type"] != "single":
            to_save = test_result.to_dict()
            to_save.update(test_dataset)

            if isinstance(self.dataset, CSVContinueDataset) and to_save["output_dir"]:
                # Note: This handles the case that someone try to test a single subject.
                # In fact, we should not generate any file if the output directory
                # is not given.
                #
                # The exception handler is just there to catch the case that the
                # method is not implemented because we are more likely using an
                # alternative backup (for example mariadb).

                self.dataset.set_base_directory(test_dataset["output_dir"])

            self.dataset.update(to_save)

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

            self.run_continue(test_dataset, test_result)

        if stop_message_caught:
            self.add_to_output_queue("stop")
