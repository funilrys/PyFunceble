"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the logic behind the threads which is supposed to mine the dataset to
later test.

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

import copy
import queue
import socket
from typing import List, Optional

import domain2idna

import PyFunceble.checker.utils.whois
import PyFunceble.cli.utils.stdout
import PyFunceble.cli.utils.testing
import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.threads.base import ThreadsBase
from PyFunceble.converter.url2netloc import Url2Netloc


class MinerThread(ThreadsBase):
    """
    Provides our miner thread logic. The main idea is that we read our queue,
    mine (or at least look for it) and write the new subject to test into
    the output queue.

    The thread behind this object, will read :code:`the_queue`, and write the
    mined subject into the :code:`output_queue` attribute.
    """

    thread_name: str = "pyfunceble_mining"

    continuous_integration: ContinuousIntegrationBase = None

    def __init__(self, output_queue: Optional[queue.Queue] = None) -> None:
        # Be sure that all settings are loaded proprely!!
        PyFunceble.factory.Requester.guess_all_settings()

        super().__init__(output_queue=output_queue)

    @staticmethod
    def mine_from(subject: str) -> Optional[List[str]]:
        """
        Given the subject to work from, try to get the related subjects.

        :param subject:
            The URL to start from.
        """

        result = []

        try:
            req = PyFunceble.factory.Requester.get(subject, allow_redirects=True)

            for element in req.history:
                if "location" in element.headers:
                    result.append(element.headers["location"])

            result.extend([x for x in req.history if isinstance(x, str)])
        except (
            PyFunceble.factory.Requester.exceptions.ConnectionError,
            PyFunceble.factory.Requester.exceptions.Timeout,
            PyFunceble.factory.Requester.exceptions.InvalidURL,
            PyFunceble.factory.Requester.urllib3_exceptions.InvalidHeader,
            socket.timeout,
        ):
            PyFunceble.facility.Logger.error(
                "Could not mine from %r", subject, exc_info=True
            )

        PyFunceble.facility.Logger.info("Mined from %r:\n%r.", subject, result)

        return result

    def target(self) -> None:
        """
        This is our core logic. Everything starts here!
        """

        stop_message_caught = False

        while (
            self.continuous_integration
            and not self.continuous_integration.is_time_exceeded()
        ) or True:
            if self.the_queue.empty():
                continue

            consumed = self.the_queue.get()

            if consumed == "stop":
                PyFunceble.facility.Logger.info(
                    "Got stop message. Stopping reading from the queue."
                )
                stop_message_caught = True
                break

            if not isinstance(consumed, tuple):
                continue

            test_dataset, test_result = consumed

            if "mined" in test_dataset or test_result.status in (
                PyFunceble.storage.STATUS.down,
                PyFunceble.storage.STATUS.invalid,
            ):
                continue

            if test_dataset["subject_type"] == "domain":
                subject = f"http://{test_result.idna_subject}:80"
            else:
                # Assuming it's already a URL.

                subject = test_result.idna_subject

            # M means that we are mining :-).
            PyFunceble.cli.utils.stdout.print_single_line("M")
            mined = self.mine_from(subject)

            for url in mined:
                to_send = copy.deepcopy(test_dataset)
                to_send["mined"] = True

                if test_dataset["subject_type"] == "domain":
                    netloc = Url2Netloc(url).get_converted()

                    if ":" in netloc:
                        netloc = netloc[: netloc.find(":")]

                    to_send["subject"], to_send["idna_subject"] = (
                        netloc,
                        domain2idna.domain2idna(to_send["subject"]),
                    )
                else:
                    if not test_result.idna_subject.endswith("/") and url.endswith("/"):
                        url = url[:-1]

                    to_send["subject"], to_send["idna_subject"] = (
                        url,
                        domain2idna.domain2idna(url),
                    )

                if to_send["idna_subject"] == test_result.idna_subject:
                    continue

                self.add_to_output_queue(to_send)

        if stop_message_caught:
            self.add_to_output_queue("stop")
