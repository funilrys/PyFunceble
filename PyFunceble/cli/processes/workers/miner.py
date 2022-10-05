"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our miner worker. This is the description of a single miner worker.

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

import copy
import socket
from typing import List, Optional, Tuple

from domain2idna import domain2idna

import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.cli.processes.workers.base import WorkerBase
from PyFunceble.cli.utils.stdout import print_single_line
from PyFunceble.converter.url2netloc import Url2Netloc


class MinerWorker(WorkerBase):
    """
    Provides our miner worker. The objective of this worker is to provides
    a single worker (or process if you prefer) which will be used to handle
    the mining of dataset to test.
    """

    STD_NAME: str = "pyfunceble_miner_worker"

    INACTIVE_STATUSES: Tuple[str, ...] = (
        PyFunceble.storage.STATUS.down,
        PyFunceble.storage.STATUS.invalid,
    )

    url2netloc: Optional[Url2Netloc] = None

    def __post_init__(self) -> None:
        self.url2netloc = Url2Netloc()

        return super().__post_init__()

    @staticmethod
    def mine_from(subject: str) -> Optional[List[str]]:
        """
        Given the subject to work from, try to get the related subjects.

        :param subject:
            The URL to start from.
        """

        PyFunceble.facility.Logger.info("Started mining from %r", subject)
        result = []

        try:
            req = PyFunceble.factory.Requester.get(subject, allow_redirects=True)

            for element in req.history:
                if "location" in element.headers:
                    result.append(element.headers["location"])

            result.extend([x for x in req.history if isinstance(x, str)])
        except (
            PyFunceble.factory.Requester.exceptions.RequestException,
            PyFunceble.factory.Requester.exceptions.ConnectionError,
            PyFunceble.factory.Requester.exceptions.Timeout,
            PyFunceble.factory.Requester.exceptions.InvalidURL,
            PyFunceble.factory.Requester.urllib3_exceptions.InvalidHeader,
            socket.timeout,
        ):
            PyFunceble.facility.Logger.error(
                "Could not mine from %r", subject, exc_info=True
            )

        PyFunceble.facility.Logger.debug("Mined from %r:\n%r.", subject, result)

        PyFunceble.facility.Logger.info("Finished mining from %r", subject)

        return result

    def target(self, consumed: Tuple[dict, CheckerStatusBase]) -> None:
        if not isinstance(consumed, tuple) or not isinstance(
            consumed[1], CheckerStatusBase
        ):
            PyFunceble.facility.Logger.info(
                "Skipping latest dataset because consumed data was not a tuple."
            )
            return None

        # Just for human brain.
        test_dataset, test_result = consumed

        if "from_miner" in test_dataset:
            PyFunceble.facility.Logger.info(
                "Skipping dataset because it comes from the mining mechanism."
            )
            return None

        if test_result.status in self.INACTIVE_STATUSES:
            PyFunceble.facility.Logger.info(
                "Skipping dataset because status is not active."
            )
            return None

        if test_dataset["subject_type"] == "domain":
            subject = f"http://{test_result.idna_subject}:80"
        else:
            # Assuming it's already a URL.

            subject = test_result.idna_subject

        print_single_line("M")

        self.add_to_output_queue("pyfunceble")
        self.share_waiting_message()
        mined = self.mine_from(subject)

        for url in mined:
            to_send = copy.deepcopy(test_dataset)
            to_send["from_miner"] = True

            if test_dataset["subject_type"] == "domain":
                netloc = self.url2netloc.set_data_to_convert(url).get_converted()

                if ":" in netloc:
                    netloc = netloc[: netloc.find(":")]

                to_send["subject"] = netloc
                to_send["idna_subject"] = domain2idna(netloc)
            else:
                if not test_result.idna_subject.endswith("/") and url.endswith("/"):
                    url = url[:-1]

                to_send["subject"] = url
                to_send["idna_subject"] = domain2idna(url)

            if to_send["idna_subject"] == test_result.idna_subject:
                PyFunceble.facility.Logger.info(
                    "Skipping %r because found in test result.", url
                )
                continue

            self.add_to_output_queue(to_send)

        # Returning None because we manually add into the queue.
        return None
