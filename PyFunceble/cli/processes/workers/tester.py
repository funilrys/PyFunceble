"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our tester worker. This is the description of a single tester worker.

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

import time
from typing import Any, Optional, Tuple

import PyFunceble.cli.utils.testing
import PyFunceble.facility
from PyFunceble.checker.availability.domain_and_ip import DomainAndIPAvailabilityChecker
from PyFunceble.checker.availability.url import URLAvailabilityChecker
from PyFunceble.checker.base import CheckerBase
from PyFunceble.checker.reputation.domain_and_ip import DomainAndIPReputationChecker
from PyFunceble.checker.reputation.url import URLReputationChecker
from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.checker.syntax.url import URLSyntaxChecker
from PyFunceble.cli.processes.workers.base import WorkerBase
from PyFunceble.cli.utils.stdout import print_single_line
from PyFunceble.dataset.autocontinue.base import ContinueDatasetBase
from PyFunceble.dataset.autocontinue.csv import CSVContinueDataset
from PyFunceble.dataset.inactive.base import InactiveDatasetBase
from PyFunceble.helpers.regex import RegexHelper


class TesterWorker(WorkerBase):
    """
    Provides our tester worker. The objective of this worker is to provides
    a single worker (or process if you prefer) which will be used to handle
    the tests.
    """

    STD_NAME: str = "pyfunceble_tester_worker"

    continue_dataset: Optional[ContinueDatasetBase] = None
    inactive_dataset: Optional[InactiveDatasetBase] = None
    testing_object: Optional[CheckerBase] = None

    known_testing_objects: dict = dict()

    def __post_init__(self) -> None:
        self.continue_dataset = (
            PyFunceble.cli.utils.testing.get_continue_databaset_object(
                db_session=self.db_session
            )
        )
        self.inactive_dataset = (
            PyFunceble.cli.utils.testing.get_inactive_dataset_object(
                db_session=self.db_session
            )
        )

        self.known_testing_objects = {
            "SYNTAX": {"domain": DomainSyntaxChecker, "url": URLSyntaxChecker},
            "AVAILABILITY": {
                "domain": DomainAndIPAvailabilityChecker,
                "url": URLAvailabilityChecker,
            },
            "REPUTATION": {
                "domain": DomainAndIPReputationChecker,
                "url": URLReputationChecker,
            },
        }

        return super().__post_init__()

    @staticmethod
    def should_be_ignored(subject: str) -> bool:
        """
        Checks if the given subject should be ignored.
        """

        # pylint: disable=line-too-long
        regex_ignore = r"localhost$|localdomain$|local$|broadcasthost$|0\.0\.0\.0$|allhosts$|allnodes$|allrouters$|localnet$|loopback$|mcastprefix$|ip6-mcastprefix$|ip6-localhost$|ip6-loopback$|ip6-allnodes$|ip6-allrouters$|ip6-localnet$"

        if RegexHelper(regex_ignore).match(subject, return_match=False):
            PyFunceble.facility.Logger.info(
                "Ignoring %r because it is in our default regex.", subject
            )
            return True

        if (
            not PyFunceble.storage.CONFIGURATION.cli_testing.local_network
            and IPSyntaxChecker(subject).is_reserved()
        ):
            PyFunceble.facility.Logger.info(
                "Ignoring %r because it is a reserved IP and we are not testing "
                "for/in a local network.",
                subject,
            )
            return True

        if bool(
            PyFunceble.storage.CONFIGURATION.cli_testing.file_filter
        ) and not RegexHelper(
            PyFunceble.storage.CONFIGURATION.cli_testing.file_filter
        ).match(
            subject, return_match=False
        ):
            PyFunceble.facility.Logger.info(
                "Ignoring %r because it does not match the filter to look for.",
                subject,
            )
            return True

        PyFunceble.facility.Logger.info(
            "Allowed to test %r.",
            subject,
        )

        return False

    def _init_testing_object(
        self, subject_type: str, checker_type: str
    ) -> Optional[CheckerBase]:
        """
        Provides the object to use for testing.

        :raise ValueError:
            When the given subject type is unknown.
        """

        if checker_type in self.known_testing_objects:
            if subject_type in self.known_testing_objects[checker_type]:
                # Yes, we initialize before returning!

                if not isinstance(
                    self.known_testing_objects[checker_type][subject_type],
                    type(self.testing_object),
                ):
                    self.testing_object = self.known_testing_objects[checker_type][
                        subject_type
                    ](db_session=self.db_session)

                    # We want to always check the syntax first (ONLY UNDER THE CLI)
                    self.testing_object.set_do_syntax_check_first(
                        not bool(
                            PyFunceble.storage.CONFIGURATION.cli_testing.local_network
                        )
                    )

                    return self.testing_object

                return None

            raise ValueError(f"<subject_type> ({subject_type!r}) is unknown.")
        raise ValueError(f"<testing_mode> ({checker_type!r}) is unknown.")

    def target(self, consumed: dict) -> Optional[Tuple[Any, ...]]:
        """
        This the target that is run to process something.
        This method should return a result which will pu send to the output
        queue.
        """

        if not isinstance(consumed, dict):
            PyFunceble.facility.Logger.debug(
                "Skipping latest dataset because consumed data was not "
                "a dictionnary."
            )
            return None

        # Just for human brain.
        test_dataset = consumed

        if self.should_be_ignored(test_dataset["idna_subject"]):
            # X means that it was ignored because of our core ignore procedure.
            print_single_line("X")
            return None

        if PyFunceble.storage.CONFIGURATION.cli_testing.cooldown_time > 0:
            PyFunceble.facility.Logger.info(
                "Sleeping: %rs for our own safety :-)",
                PyFunceble.storage.CONFIGURATION.cli_testing.cooldown_time,
            )
            # Apply cooldowntime.
            time.sleep(PyFunceble.storage.CONFIGURATION.cli_testing.cooldown_time)
            PyFunceble.facility.Logger.info(
                "Slept: %rs for our own safety :-)",
                PyFunceble.storage.CONFIGURATION.cli_testing.cooldown_time,
            )

        if test_dataset["type"] != "single":
            if test_dataset["output_dir"] and "from_preload" not in test_dataset:
                if isinstance(self.continue_dataset, CSVContinueDataset):
                    self.continue_dataset.set_base_directory(test_dataset["output_dir"])

                if self.continue_dataset.exists(test_dataset):
                    # A means that it was ignored because of the continue
                    # logic.

                    PyFunceble.facility.Logger.info(
                        "Ignoring %r because it was already tested previously "
                        "(continue).",
                        test_dataset["idna_subject"],
                    )

                    PyFunceble.cli.utils.stdout.print_single_line("A")
                    return None

            if "from_inactive" not in test_dataset and self.inactive_dataset.exists(
                test_dataset
            ):
                # "I" means that it was ignored because of the inactive (db)
                # logic.

                PyFunceble.facility.Logger.info(
                    "Ignoring %r because it was already tested previously "
                    "(inactive).",
                    test_dataset["idna_subject"],
                )

                PyFunceble.cli.utils.stdout.print_single_line("I")

                return test_dataset, "ignored_inactive"

        PyFunceble.facility.Logger.info(
            "Started test of %r.",
            test_dataset["idna_subject"],
        )

        self._init_testing_object(
            test_dataset["subject_type"], test_dataset["checker_type"]
        )

        result = (
            self.testing_object.set_subject(test_dataset["idna_subject"])
            .query_status()
            .get_status()
        )

        PyFunceble.facility.Logger.info(
            "Successfully handled %r.",
            test_dataset["idna_subject"],
        )

        PyFunceble.facility.Logger.debug("Got status:\n%r.", result)

        return test_dataset, result
