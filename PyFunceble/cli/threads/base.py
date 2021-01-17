"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of our threads classes.

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
import queue
import threading
from typing import Any, Optional, Tuple, Union

import PyFunceble.cli.threads.threading
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.helpers.regex import RegexHelper


class ThreadsBase:
    """
    Provides the base of all classes.
    """

    thread_name: Optional[str] = "pyfunceble"

    the_queue: Optional[queue.Queue] = None
    the_thread: Optional[PyFunceble.cli.threads.threading.Thread] = None

    _output_queue: Optional[Union[queue.Queue, Tuple[queue.Queue]]] = None

    def __init__(
        self, output_queue: Optional[Union[queue.Queue, Tuple[queue.Queue]]] = None
    ) -> None:
        self.the_queue = queue.Queue()

        if output_queue is not None:
            self.output_queue = output_queue

    def ensure_thread_is_not_initiated(func):  # pylint: disable=no-self-argument
        """
        Ensures that the thread was not initiated before launching the decorated
        method.

        :raise RuntimeError:
            When the thread was already launched.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.is_initiated():
                # if self.the_thread is not None:
                raise RuntimeError("Thread already initiated.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable.

        return wrapper

    def ensure_thread_is_initiated(func):  # pylint: disable=no-self-argument
        """
        Ensures that the thread was initiated before launching the decorated
        method.

        :raise RuntimeError:
            When the thread was not launched.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.is_initiated():
                # if not isinstance(self.the_thread, threading.Thread):
                raise RuntimeError("Thread not initiated yet.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable.

        return wrapper

    def ensure_output_queue_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the output queue was given before launching the decorated
        method.

        :raise RuntimeError:
            When the thread was not launched.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.output_queue, (queue.Queue, tuple)):
                raise RuntimeError("Output queue not given.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable.

        return wrapper

    @property
    def output_queue(self) -> Optional[queue.Queue]:
        """
        Provides the current state of the :code:`_output_queue` attribute.
        """

        return self._output_queue

    @output_queue.setter
    def output_queue(self, value: Union[queue.Queue, Tuple[queue.Queue]]):
        """
        Sets the output queue with the given queue.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`queue.Queue` or
            a :py:class:`tuple` of :py:class:`queue.Queue`.
        """

        if not isinstance(value, (queue.Queue, tuple)):
            raise TypeError(
                f"<value> should be {queue.Queue} or {tuple}, {type(value)} given."
            )

        if isinstance(value, tuple) and not all(
            isinstance(x, queue.Queue) for x in value
        ):
            raise TypeError(f"<value> should be a {tuple} of {queue.Queue}.")

        self._output_queue = value

    def set_output_queue(self, value: Union[queue.Queue, Tuple[queue.Queue]]):
        """
        Sets the output queue with the given queue.

        :param value:
            The value to set.
        """

        self.output_queue = value

        return self

    def is_initiated(self) -> bool:
        """
        Checks if the current thread was initiated.
        """

        return isinstance(self.the_thread, threading.Thread)

    def is_running(self) -> bool:
        """
        Checks if the current thread is running.
        """

        return self.the_thread is not None and self.the_thread.is_alive()

    def is_failed(self) -> bool:
        """
        Checks if the current thread has failed.
        """

        return self.the_thread.is_failed()

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

    def target(self) -> None:
        """
        The target to give to the thread. This is where the magic happens :-)
        """

        raise NotImplementedError()

    @ensure_thread_is_not_initiated
    def start(self, *, daemon: bool = True) -> "ThreadsBase":
        """
        Starts the threads itself.

        :param daemon:
            Tells us to starts the threads as a daemon.
        """

        self.the_thread = PyFunceble.cli.threads.threading.Thread(
            target=self.target, name=self.thread_name
        )

        if daemon:
            self.the_thread.setDaemon(True)

        self.the_thread.start()

        PyFunceble.facility.Logger.info(
            "Started underlying thread of %r (daemon=%r).", self.thread_name, daemon
        )

        return self

    @ensure_thread_is_initiated
    def send_stop_signal(self) -> "ThreadsBase":
        """
        Puts the :code:`stop` message into the queue.
        """

        self.the_queue.put("stop")

        PyFunceble.facility.Logger.info(
            "Sent stop signal to the (main) queue of %r.", self.thread_name
        )

        return self

    @ensure_thread_is_initiated
    def wait(self) -> "ThreadsBase":
        """
        Stops the threads itself.
        """

        self.the_thread.join()

        if self.is_failed():
            raise self.the_thread.exception

        return self

    def add_to_the_queue(self, data: Any) -> "ThreadsBase":
        """
        Adds the given :code:`data` to the current queue.

        :param data:
            The data to add into the queue.
        """

        self.the_queue.put(data)

        PyFunceble.facility.Logger.debug("Added to the (main) queue: %r", data)

        return self

    def add_to_output_queue(self, data: Any) -> "ThreadsBase":
        """
        Adds the given :code:`data` to the output queue.

        :param data:
            The data to add into the output queue.
        """

        if self.output_queue:
            if isinstance(self.output_queue, tuple):
                for output_queue in self.output_queue:
                    output_queue.put(data)

                    PyFunceble.facility.Logger.debug(
                        "Added to the (output) queue: %r", data
                    )
            else:
                self.output_queue.put(data)
                PyFunceble.facility.Logger.debug(
                    "Added to the (output) queue: %r", data
                )

        return self
