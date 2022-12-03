"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all extra handlers.

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

import functools
from typing import Callable, List, Optional

import requests

import PyFunceble.factory
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus
from PyFunceble.query.dns.query_tool import DNSQueryTool


class ExtraRuleHandlerBase:
    """
    Provides the base of all extra rules handler.

    :param statatus:
        The previously gathered status.
    :type status:
        :class:`~PyFunceble.checker.availability.status.AvailabilityCheckerStatus`
    """

    _status: Optional[AvailabilityCheckerStatus] = None
    req: Optional[requests.Response] = None
    dns_query_tool: Optional[DNSQueryTool] = None
    req_url: Optional[str] = None

    def __init__(self, status: Optional[AvailabilityCheckerStatus] = None) -> None:
        if status is not None:
            self.status = status

        # Be sure that all settings are loaded proprely!!
        PyFunceble.factory.Requester.guess_all_settings()
        self.dns_query_tool = DNSQueryTool()

    def ensure_status_is_given(
        func: Callable[..., "ExtraRuleHandlerBase"]
    ):  # pylint: disable=no-self-argument
        """
        Ensures that the status is given before running the decorated method.

        :raise TypeError:
            If the subject is not a string.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Safety!
            if not self.status:
                raise TypeError(
                    f"<self.status> should be {AvailabilityCheckerStatus}, "
                    f"{type(self.status)} given."
                )

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def setup_status_before(
        func: Callable[..., "ExtraRuleHandlerBase"]
    ):  # pylint: disable=no-self-argument
        """
        Ensures that the status is given before running the decorated method.

        :raise TypeError:
            If the subject is not a string.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Safety!
            self.status.status_before_extra_rules = self.status.status
            self.status.status_source_before_extra_rules = self.status.status_source

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def setup_status_after(
        func: Callable[..., "ExtraRuleHandlerBase"]
    ):  # pylint: disable=no-self-argument
        """
        Ensures that the status is given before running the decorated method.

        :raise TypeError:
            If the subject is not a string.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Safety!
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            if self.status.status_after_extra_rules:
                self.status.status = self.status.status_after_extra_rules
                self.status.status_source = self.status.status_source_after_extra_rules

                PyFunceble.facility.Logger.info(
                    "Could define the status of %r from our own set of rules.",
                    self.status.idna_subject,
                )
            else:
                self.status.status_before_extra_rules = None
                self.status.status_source_before_extra_rules = None
                self.status.status_after_extra_rules = None
                self.status.status_source_after_extra_rules = None

            return result

        return wrapper

    @property
    def status(self) -> Optional[AvailabilityCheckerStatus]:
        """
        Provides the current state of the :code:`_status` attribute.
        """

        return self._status

    @status.setter
    def status(self, value: AvailabilityCheckerStatus) -> None:
        """
        Sets the status to work with.

        :param value:
            The status to work with.

        :raise TypeError:
            When the given :code:`value` is not a
            :class:`~PyFunceble.checker.availability.status.AvailabilityCheckerStatus`.
        """

        if not isinstance(value, AvailabilityCheckerStatus):
            raise TypeError(
                f"<value> should be {AvailabilityCheckerStatus}, {type(value)} given."
            )

        self._status = value

    def set_status(self, value: AvailabilityCheckerStatus) -> "ExtraRuleHandlerBase":
        """
        Sets the status to work with.

        :param value:
            The status to work with.
        """

        self.status = value

        return self

    def do_request(self, *, allow_redirects: bool = True) -> requests.Response:
        """
        Do a request and store its response into the `req` attribute.

        :param bool allow_redirects:
            Whether we shoold follow the redirection - or not.
        """

        if any(self.status.idna_subject.startswith(x) for x in ("http:", "https:")):
            self.req_url = url = self.status.idna_subject
        else:
            self.req_url = url = f"http://{self.status.idna_subject}:80"

        self.req = PyFunceble.factory.Requester.get(
            url, allow_redirects=allow_redirects
        )

        return self

    def do_dns_lookup(self, *, subject: str, query_type: str) -> List[str]:
        """
        Do a DNS lookup and return its response.

        :param subject:
            The subject to query.
        :param query_type:
            The query type.
        """

        return (
            self.dns_query_tool.set_query_record_type(query_type)
            .set_subject(subject)
            .query()
        )

    def start(self) -> "ExtraRuleHandlerBase":
        """
        Starts the gathering process.
        """

        raise NotImplementedError()

    def switch_to_down(self) -> "ExtraRuleHandlerBase":
        """
        Switches the status to inactive.
        """

        self.status.status_after_extra_rules = PyFunceble.storage.STATUS.down
        self.status.status_source_after_extra_rules = "SPECIAL"

        return self

    def switch_to_up(self) -> "ExtraRuleHandlerBase":
        """
        Switches the status to active.
        """

        self.status.status_after_extra_rules = PyFunceble.storage.STATUS.up
        self.status.status_source_after_extra_rules = "SPECIAL"
