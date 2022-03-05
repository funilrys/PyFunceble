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

import multiprocessing
import multiprocessing.connection
import queue
import time
import traceback
from datetime import datetime, timedelta
from typing import Any, List, Optional, Tuple

import PyFunceble.cli.facility
import PyFunceble.cli.factory
import PyFunceble.facility
import PyFunceble.sessions
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase


class WorkerBase(multiprocessing.Process):
    """
    Provides the base of all our workers.

    :param input_queue:
        The input queue to read.
    :param output_queue:
        The output queue to write.
    """

    STD_NAME: str = "pyfunceble_base_worker"

    MINING_WAIT_TIME: int = 60
    BREAKOFF: float = 2.0

    input_queue: Optional[queue.Queue] = None
    output_queue: Optional[queue.Queue] = None

    continuous_integration: ContinuousIntegrationBase = None

    global_exit_event: Optional[multiprocessing.Event] = None
    exit_it: Optional[multiprocessing.Event] = None

    send_stop_message: Optional[bool] = None
    accept_waiting_delay: Optional[bool] = None

    concurrent_worker_names: Optional[List[str]] = None
    db_session: Optional[PyFunceble.cli.factory.db_session] = None

    _parent_connection: Optional[multiprocessing.connection.Connection] = None
    _child_connection: Optional[multiprocessing.connection.Connection] = None
    _exception: Optional[multiprocessing.Pipe] = None

    _params: Optional[dict] = {}

    def __init__(
        self,
        input_queue: Optional[queue.Queue],
        output_queue: Optional[queue.Queue] = None,
        global_exit_event: Optional[multiprocessing.Event] = None,
        *,
        name: Optional[str] = None,
        daemon: Optional[bool] = None,
        continuous_integration: Optional[ContinuousIntegrationBase] = None,
        configuration: Optional[dict] = None,
    ) -> None:
        self.configuration = self._params["configuration"] = configuration
        self.input_queue = self._params["input_queue"] = input_queue
        self.output_queue = self._params["output_queue"] = output_queue

        self.continuous_integration = self._params[
            "continuous_integration"
        ] = continuous_integration

        self.global_exit_event = self._params["global_exit_event"] = global_exit_event
        self.exit_it = multiprocessing.Event()

        self._parent_connection, self._child_connection = multiprocessing.Pipe()
        self._exception = None

        self.send_stop_message = True
        self.accept_waiting_delay = True
        self.concurrent_worker_names = []

        try:
            self.db_session = (
                PyFunceble.cli.factory.DBSession.get_db_session().get_new_session()()
            )
        except TypeError:
            self.db_session = None

        super().__init__(name=name, daemon=daemon)

        self.__post_init__()

    def __del__(self) -> None:
        if self.db_session is not None:
            self.db_session.close()

    def __post_init__(self) -> None:
        """
        A method which will be executed after the :code:`__init__` method.
        """

    @property
    def exception(self):
        """
        Provides the exception of the current worker.
        """

        if self._parent_connection.poll():
            self._exception = self._parent_connection.recv()

        return self._exception

    def add_to_input_queue(
        self,
        data: Any,
        *,
        worker_name: Optional[str] = None,
        destination_worker: Optional[str] = None,
    ) -> "WorkerBase":
        """
        Adds the given data to the current queue.

        :param data:
            The data to add into the queue.
        :param destination_worker:
            The name of the worker which is supposed to read the message.
        """

        if worker_name:
            to_send = (worker_name, destination_worker, data)
        else:
            to_send = (self.name, destination_worker, data)

        self.input_queue.put(to_send)

        PyFunceble.facility.Logger.debug("Added to the (input) queue: %r", data)

    def add_to_output_queue(
        self,
        data: Any,
        *,
        worker_name: Optional[str] = None,
        destination_worker: Optional[str] = None,
    ) -> "WorkerBase":
        """
        Adds the given data to the output queue queue.

        :param data:
            The data to add into the queue.
        """

        if worker_name:
            to_send = (worker_name, destination_worker, data)
        else:
            to_send = (self.name, destination_worker, data)

        if self.output_queue is not None:
            for output_queue in self.output_queue:
                output_queue.put(to_send)

        PyFunceble.facility.Logger.debug("Added to the (output) queue: %r", data)

        return self

    def target(self, consumed: Any) -> Optional[Tuple[Any, ...]]:
        """
        This the target that is run to process something.
        This method should return a result which will pu send to the output
        queue.
        """

        raise NotImplementedError()

    def share_waiting_message(
        self,
        *,
        overall: bool = False,
        ignore_current_worker: bool = False,
        apply_breakoff: bool = False,
    ) -> "WorkerBase":
        """
        Shares a waiting message to both input and output queues.
        The idea is to keep our worker awake when necessary. This functionality
        is really important when running the mining worker because sometime
        the flow is so long, that we may need some time.

        :param overall:
            Shares the message multiple time to specific destination in our
            current stack.
        :param ignore_current_worker:
            Doesn't share the message with ourself.
        :param apply_breakoff:
            Activates the breakoff (sleep) before starting to share the message.
        """

        if overall:
            for worker_name in self.concurrent_worker_names:
                if apply_breakoff:
                    time.sleep(self.BREAKOFF)

                if not ignore_current_worker:
                    # Give the whole stack a bit more of time.
                    self.add_to_input_queue("wait", destination_worker=worker_name)

                self.add_to_output_queue("wait")
        else:
            if apply_breakoff:
                time.sleep(self.BREAKOFF)

            if not ignore_current_worker:
                self.add_to_input_queue("wait", destination_worker=self.name)

            self.add_to_output_queue("wait")

    def run(self) -> None:  # pylint: disable=too-many-statements
        def break_now() -> bool:
            """
            Checks if it is time to make a break.
            """

            if not wait_for_stop or not self.accept_waiting_delay:
                return True

            return datetime.utcnow() > break_time

        if self.configuration is not None:
            PyFunceble.facility.ConfigLoader.set_custom_config(self.configuration)

        if multiprocessing.get_start_method() != "fork":
            PyFunceble.facility.ConfigLoader.start()
            PyFunceble.cli.facility.CredentialLoader.start()
            PyFunceble.cli.factory.DBSession.init_db_sessions()

        # Be sure that all settings are loaded proprely!!
        PyFunceble.factory.Requester = PyFunceble.factory.requester()

        wait_for_stop = (
            bool(PyFunceble.storage.CONFIGURATION.cli_testing.mining) is True
        )
        break_time = datetime.utcnow() + timedelta(seconds=self.MINING_WAIT_TIME)

        try:  # pylint: disable=too-many-nested-blocks
            while True:
                if self.global_exit_event.is_set():
                    PyFunceble.facility.Logger.info(
                        "Got global exit event. Stopping worker."
                    )

                    break

                if self.exit_it.is_set():
                    PyFunceble.facility.Logger.info("Got exit event. Stopping worker.")
                    break

                if (
                    self.continuous_integration
                    and self.continuous_integration.is_time_exceeded()
                ):
                    PyFunceble.facility.Logger.info(
                        "CI time exceeded. Stopping worker."
                    )

                    if break_now():
                        self.exit_it.set()
                        continue

                    continue

                try:
                    worker_name, destination_worker, consumed = self.input_queue.get()
                except EOFError:
                    PyFunceble.facility.Logger.info("Got EOFError. Stopping worker.")
                    self.global_exit_event.set()
                    break

                if destination_worker and destination_worker != self.name:
                    self.add_to_input_queue(
                        consumed,
                        worker_name=worker_name,
                        destination_worker=destination_worker,
                    )
                    continue

                PyFunceble.facility.Logger.info(
                    "Got (from %r): %r",
                    worker_name,
                    consumed,
                )

                if consumed == "stop":
                    if break_now():
                        PyFunceble.facility.Logger.info(
                            "Got stop message from %r. Applying.",
                            worker_name,
                        )

                        self.exit_it.set()
                        continue

                    self.share_waiting_message(apply_breakoff=wait_for_stop)
                    continue

                if consumed == "wait":
                    if not wait_for_stop:
                        continue

                    if break_now():
                        PyFunceble.facility.Logger.debug(
                            "Waited sufficiently. Stopping current worker."
                        )

                        # The real (break) action shouldn't be handled here.
                        self.exit_it.set()
                        continue

                    PyFunceble.facility.Logger.debug(
                        "We need to wait a bit more. Continue waiting."
                    )

                    self.share_waiting_message(apply_breakoff=wait_for_stop)
                    continue

                result = self.target(consumed)

                if result is not None:
                    self.add_to_output_queue(result)

                    PyFunceble.facility.Logger.info(
                        "Produced: %r",
                        result,
                    )

                break_time = datetime.utcnow() + timedelta(
                    seconds=self.MINING_WAIT_TIME
                )

        except Exception as exception:  # pylint: disable=broad-except
            PyFunceble.facility.Logger.critical(
                "Error while running target", exc_info=True
            )
            trace = traceback.format_exc()
            self._child_connection.send((exception, trace))

            self.exit_it.set()
            raise exception

    def terminate(self) -> None:
        """
        Terminate our worker.
        """

        self.exit_it.set()

        if self.input_queue:
            # Necessary to avoid blocking.
            self.add_to_input_queue("stop", destination_worker=self.name)
