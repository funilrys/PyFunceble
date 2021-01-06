"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the logic behind the threads which is supposed to generate outputs to
the STDOUT.

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
from PyFunceble.cli.filesystem.printer.stdout import StdoutPrinter
from PyFunceble.cli.threads.producer_base import ProducerThreadBase


class StdoutProducerThread(ProducerThreadBase):
    """
    Provides our STDOUT producer thread logic.

    The thread behind this object, will read :code:`the_queue`, and procude
    the outputs to stdout.
    """

    thread_name: str = "pyfunceble_stdout_producer"

    stdout_printer: Optional[StdoutPrinter] = None

    header_already_printed: bool = False

    def __init__(self, output_queue: Optional[queue.Queue] = None) -> None:
        self.stdout_printer = StdoutPrinter()

        super().__init__(output_queue=output_queue)

    @staticmethod
    def shoud_we_print_status(status: str) -> bool:
        """
        Checks if we are allowed to print based on the given status.

        :param status:
            The status to check.
        """

        if isinstance(
            PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.status, list
        ):
            to_keep = PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.status
        else:
            to_keep = [PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.status]

        return "ALL" in to_keep or status in to_keep

    def run_stdout_printer(self, test_result: CheckerStatusBase) -> None:
        """
        Runs the stdout printer if necessary.

        :param test_dataset:
            The test dataset.
        :param test_result:
            The test result object.
        """

        if not PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet:
            # pylint: disable=line-too-long
            if self.shoud_we_print_status(test_result.status):
                self.stdout_printer.template_to_use = (
                    PyFunceble.cli.utils.stdout.get_template_to_use()
                )

                if not self.header_already_printed:
                    self.stdout_printer.print_header()
                    self.header_already_printed = True

                self.stdout_printer.set_dataset(
                    test_result.to_dict()
                ).print_interpolated_line()
            else:
                PyFunceble.cli.utils.stdout.print_single_line()
        else:
            PyFunceble.cli.utils.stdout.print_single_line()

    def send_for_mining(
        self, test_dataset: dict, test_result: CheckerStatusBase
    ) -> None:
        """
        Sends the test dataset to the mining queue (if given).
        """

        self.add_to_output_queue((test_dataset, test_result))

    def target(self) -> None:
        """int
        This is our core logic. Everything starts here!
        """

        stop_message_caught = False

        while True:
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

            self.run_stdout_printer(test_result)
            self.send_for_mining(test_dataset, test_result)

        if stop_message_caught:
            self.add_to_output_queue("stop")
