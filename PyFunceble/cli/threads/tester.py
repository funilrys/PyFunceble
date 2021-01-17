"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the logic behind the threads which is supposed to test the given subject.

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

import concurrent.futures
import time
from typing import List, Optional

import PyFunceble.cli.utils.stdout
import PyFunceble.cli.utils.testing
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.availability.domain_and_ip import DomainAndIPAvailabilityChecker
from PyFunceble.checker.availability.url import URLAvailabilityChecker
from PyFunceble.checker.base import CheckerBase
from PyFunceble.checker.reputation.domain_and_ip import DomainAndIPReputationChecker
from PyFunceble.checker.reputation.url import URLReputationChecker
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.checker.syntax.url import URLSyntaxChecker
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.threads.base import ThreadsBase
from PyFunceble.cli.threads.utils import wait_until_completion


class TesterThread(ThreadsBase):
    """
    Provides our tester thread logic.

    The thread behind this object, will read :code:`the_queue`, test all entries
    until a `stop` is given and store the result into :code:`output_queue`.
    """

    thread_name: str = "pyfunceble_tester"

    continuous_integration: ContinuousIntegrationBase = None

    @staticmethod
    def done_callback(func: concurrent.futures.Future) -> None:
        """
        This method will be executed after each task run.

        :raise Exception:
            The the task has some exception.
        """

        if func.done() and func.exception():
            PyFunceble.facility.Logger.critical(
                "Fatal error while testing.", exc_info=True
            )
            raise func.exception()

    @staticmethod
    def get_testing_object(subject_type: str, checker_type: str) -> CheckerBase:
        """
        Provides the object to use for testing.

        :raise ValueError:
            When the given subject type is unkown.
        """

        known = {
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

        if checker_type in known:
            if subject_type in known[checker_type]:
                # Yes, we initialize before returning!
                return known[checker_type][subject_type]()

            raise ValueError(f"<subject_type> ({subject_type!r}) is unknwon.")
        raise ValueError(f"<testing_mode> ({checker_type!r}) is unknwon.")

    def get_status(self, test_dataset: dict) -> Optional[CheckerStatusBase]:
        """
        This is our part our our target. Meaning that you shouldn't be playing
        with this outside the CLI.

        This method reads the given dataset, starts the test and return the
        result of it after putting it into the declared output queue.

        Please note a slighly side effect of this method. Indeed,
        :py:class:`None` will be returned if the subject to test should be
        ignored.
        """

        if self.should_be_ignored(test_dataset["idna_subject"]):
            # X means that it was ignored because of our core ignore procedure.
            PyFunceble.cli.utils.stdout.print_single_line("X")
            return None

        if test_dataset["type"] != "single":
            continue_object = (
                PyFunceble.cli.utils.testing.get_continue_databaset_object()
            )

            if test_dataset["output_dir"]:
                try:
                    continue_object.set_base_directory(test_dataset["output_dir"])
                except NotImplementedError:
                    pass

                if continue_object.exists(test_dataset):
                    # A means that it was ignored because of the continue
                    # logic.

                    PyFunceble.facility.Logger.info(
                        "Ignoring %r because it was already tested previously "
                        "(continue).",
                        test_dataset["idna_subject"],
                    )

                    PyFunceble.cli.utils.stdout.print_single_line("A")
                    return None

            if "from_inactive" not in test_dataset:
                inactive_object = (
                    PyFunceble.cli.utils.testing.get_inactive_dataset_object()
                )

                if inactive_object.exists(test_dataset):
                    # I means that it was ignored because of the inactive (db)
                    # logic.

                    PyFunceble.facility.Logger.info(
                        "Ignoring %r because it was already tested previously "
                        "(inactive).",
                        test_dataset["idna_subject"],
                    )

                    PyFunceble.cli.utils.stdout.print_single_line("I")

                    self.add_to_output_queue((test_dataset, "ignored_inactive"))
                    return None

        testing_object = self.get_testing_object(
            test_dataset["subject_type"], test_dataset["checker_type"]
        )

        # We want to always check the syntax first (ONLY UNDER THE CLI)
        testing_object.set_do_syntax_check_first(
            not bool(PyFunceble.storage.CONFIGURATION.cli_testing.local_network)
        )

        result = (
            testing_object.set_subject(test_dataset["idna_subject"])
            .query_status()
            .get_status()
        )

        PyFunceble.facility.Logger.debug("Got status:\n%r.", result)

        self.add_to_output_queue((test_dataset, result))

        return result

    @ThreadsBase.ensure_output_queue_is_given
    def target(self) -> None:
        """
        This is our core logic. Everything starts here!
        """

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=PyFunceble.storage.CONFIGURATION.cli_testing.max_workers,
            thread_name_prefix=self.thread_name,
        ) as executor:
            submitted_list: List[concurrent.futures.Future] = []
            stop_message_caught = False

            # Don't worry, if we are not under a CI engine, the
            # is_time_exceeded will automatically return false (cf: decorators)
            while (
                self.continuous_integration
                and not self.continuous_integration.is_time_exceeded()
            ) or True:
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

                if not isinstance(consumed, dict):
                    PyFunceble.facility.Logger.debug(
                        "Waiting for new dataset "
                        "because inputed data was not a dictionnary."
                    )
                    continue

                PyFunceble.facility.Logger.debug("Submitting: %r", consumed)
                submitted = executor.submit(self.get_status, consumed)
                PyFunceble.facility.Logger.debug("Submitted: %r", consumed)

                PyFunceble.facility.Logger.debug(
                    "Adding callback into submitted: %r", submitted
                )
                # submitted.add_done_callback(self.done_callback)
                PyFunceble.facility.Logger.debug(
                    "Added callback into submitted: %r", submitted
                )

                submitted_list.append(submitted)

                if PyFunceble.storage.CONFIGURATION.cli_testing.cooldown_time > 0:
                    PyFunceble.facility.Logger.info(
                        "Sleeping: %rs for our own safety :-)",
                        PyFunceble.storage.CONFIGURATION.cli_testing.cooldown_time,
                    )
                    # Apply cooldowntime.
                    time.sleep(
                        PyFunceble.storage.CONFIGURATION.cli_testing.cooldown_time
                    )
                    PyFunceble.facility.Logger.info(
                        "Slept: %rs for our own safety :-)",
                        PyFunceble.storage.CONFIGURATION.cli_testing.cooldown_time,
                    )

            wait_until_completion(submitted_list, raise_exc=True)

        if stop_message_caught:
            self.add_to_output_queue("stop")
