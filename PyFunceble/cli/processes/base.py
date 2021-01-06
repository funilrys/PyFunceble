"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all multiprocessing jobs.

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

import functools
import multiprocessing
import os
import queue
from typing import Any, List, Optional

import PyFunceble.facility
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.processes.workers.base import WorkerBase


class ProcessesManagerBase:
    """
    Provides the base of all classes.
    """

    CPU_COUNT = os.cpu_count()

    if CPU_COUNT > 2:
        STD_MAX_WORKER: int = CPU_COUNT - 2
    else:
        STD_MAX_WORKER: int = 1

    WORKER_OBJ: Optional[WorkerBase] = None

    input_queue: Optional[queue.Queue] = None
    """
    The input queue. Dataset will be given through this.
    """

    output_queue: Optional[queue.Queue] = None
    """
    The output queue. This is where the result of a worker will be put.
    """

    daemon: Optional[bool] = None

    manager: Optional[multiprocessing.Manager] = None

    global_exit_event: Optional[multiprocessing.Event] = None
    continuous_integration: Optional[ContinuousIntegrationBase] = None

    _created_workers: Optional[List[WorkerBase]] = None
    _running_workers: Optional[List[WorkerBase]] = None

    _max_worker: Optional[int] = None

    def __init__(
        self,
        manager: Optional[multiprocessing.Manager] = None,
        max_worker: Optional[int] = None,
        *,
        continuous_integration: Optional[ContinuousIntegrationBase] = None,
        input_queue: Optional[queue.Queue] = None,
        output_queue: Optional[queue.Queue] = None,
        daemon: bool = False,
        generate_input_queue: bool = True,
        generate_output_queue: bool = True,
    ) -> None:
        if manager is not None:
            self.manager = manager
        else:
            self.manager = multiprocessing.Manager()

        if input_queue is None:
            self.input_queue = self.manager.Queue()
        elif generate_input_queue:
            self.input_queue = input_queue
        else:
            self.input_queue = None

        if output_queue is None:
            self.output_queue = self.manager.Queue()
        elif generate_output_queue:
            self.output_queue = output_queue
        else:
            self.output_queue = None

        if max_worker is not None:
            self.max_worker = max_worker
        else:
            self.max_worker = self.STD_MAX_WORKER

        if continuous_integration is not None:
            self.continuous_integration = continuous_integration

        self.daemon = daemon

        self.global_exit_event = multiprocessing.Event()

        self._running_workers = list()
        self._created_workers = list()

    def ensure_worker_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the worker is proprelly declared before launching the
        decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.WORKER_OBJ is None:
                raise TypeError(f"<self.WORKER_OBJ> should not be {None}!")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def max_worker(self) -> Optional[int]:
        """
        Provides the number of maximul worker we are allowed to generate.
        """

        return self._max_worker

    @max_worker.setter
    def max_worker(self, value: int) -> None:
        """
        Sets the number of maximul worker we are authorized to generate.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`int`.
        :raise ValueError:
            When the given :code:`value` is less than :code:`1`.
        """

        if not isinstance(value, int):
            raise TypeError(f"<value> should be {int}, {type(value)} given.")

        if value < 1:
            raise ValueError("<value> should be greater or equal to one.")

        self._max_worker = value

    def set_max_worker(self, value: int) -> "ProcessesManagerBase":
        """
        Sets the number of maximul worker we are authorized to generate.

        :param value:
            The value to set.
        """

        self.max_worker = value

        return self

    def is_running(self) -> bool:
        """
        Checks if a worker is running.
        """

        for worker in self._running_workers:
            if worker.is_alive():
                return True

        return False

    def send_stop_signal(
        self, *, worker_name: Optional[str] = None
    ) -> "ProcessesManagerBase":
        """
        Sends a stop message to the input queue.
        """

        self.add_to_all_input_queues("stop", worker_name=worker_name)

    def terminate(self) -> "ProcessesManagerBase":
        """
        Terminates all workers.
        """

        for worker in self._running_workers:
            worker.terminate()

    def wait(self) -> "ProcessesManagerBase":
        """
        Wait until all workers are done.
        """

        for worker in self._running_workers:
            worker.join()

        for worker in self._running_workers:
            if worker.exception:
                worker_error, _ = worker.exception

                raise worker_error

    def add_to_all_input_queues(
        self, data: Any, *, worker_name: Optional[str] = None
    ) -> "ProcessesManagerBase":
        """
        Adds the given data to the input queues.

        :param data:
            The data to add into the queue.
        """

        for worker in self._running_workers:
            worker.add_to_input_queue(data, worker_name=worker_name)

        PyFunceble.facility.Logger.debug("Added to all (input) queues: %r", data)

    def add_to_all_output_queues(
        self, data: Any, *, worker_name: Optional[str] = None
    ) -> "ProcessesManagerBase":
        """
        Adds the given data to the output queues.

        :param data:
            The data to add into the queue.
        """

        for worker in self._running_workers:
            worker.add_to_output_queue(data, worker_name=worker_name)

        PyFunceble.facility.Logger.debug("Added to all (output) queues: %r", data)

        return self

    def add_to_input_queue(
        self, data: Any, *, worker_name: Optional[str] = None
    ) -> "ProcessesManagerBase":
        """
        Adds the given data to the current queue.

        :param data:
            The data to add into the queue.
        """

        try:
            self._running_workers[0].add_to_input_queue(data, worker_name=worker_name)
        except IndexError:
            # Example: Not started yet.
            self._created_workers[0].add_to_input_queue(data, worker_name=worker_name)

        PyFunceble.facility.Logger.debug("Added to the (main) queue: %r", data)

    def add_to_output_queue(
        self, data: Any, *, worker_name: Optional[str] = None
    ) -> "ProcessesManagerBase":
        """
        Adds the given data to the output queue.

        :param data:
            The data to add into the queue.
        """

        try:
            self._running_workers[0].add_to_output_queue(data, worker_name=worker_name)
        except IndexError:
            # Example: Not started yet.
            self._created_workers[0].add_to_output_queue(data, worker_name=worker_name)

        PyFunceble.facility.Logger.debug("Added to the (output) queue: %r", data)

        return self

    def create(self) -> "ProcessesManagerBase":
        """
        Creates the defined amount of worker.
        """

        for i in range(self.max_worker):
            worker = self.WORKER_OBJ(  # pylint: disable=not-callable
                self.input_queue,
                self.output_queue,
                self.global_exit_event,
                name=f"{self.WORKER_OBJ.STD_NAME}_{i + 1}",
                daemon=self.daemon,
                continuous_integration=self.continuous_integration,
                configuration=PyFunceble.storage.CONFIGURATION.to_dict(),
            )

            self._created_workers.append(worker)

        PyFunceble.facility.Logger.info(
            "Created %r workers of %r. Details:\n%r",
            len(self._created_workers),
            self.WORKER_OBJ,
            self._created_workers,
        )

        return self

    @ensure_worker_is_given
    def start(self) -> "ProcessesManagerBase":
        """
        Starts a defined number of worker.
        """

        if not self._created_workers:
            self.create()

        for worker in self._created_workers:
            worker.start()

            self._running_workers.append(worker)

        PyFunceble.facility.Logger.info(
            "Started %r workers of %r. Details:\n%r",
            len(self._running_workers),
            self.WORKER_OBJ,
            self._running_workers,
        )

        return self
