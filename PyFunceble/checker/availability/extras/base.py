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


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import functools
import socket
from typing import Callable, Dict, List, Optional, Union

import requests

import PyFunceble.factory
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus
from PyFunceble.helpers.regex import RegexHelper
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
    regex_helper: Optional[RegexHelper] = None

    def __init__(self, status: Optional[AvailabilityCheckerStatus] = None) -> None:
        if status is not None:
            self.status = status

        # Be sure that all settings are loaded proprely!!
        PyFunceble.factory.Requester.guess_all_settings()
        self.dns_query_tool = DNSQueryTool()
        self.regex_helper = RegexHelper()

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
    def req_url(self) -> Optional[str]:
        """
        Provides a viable request URL.
        """

        if any(self.status.idna_subject.startswith(x) for x in ("http:", "https:")):
            return self.status.idna_subject
        return f"http://{self.status.idna_subject}:80"

    @property
    def req_url_https(self) -> Optional[str]:
        """
        Provides a viable request URL that default to an HTTPS URL.
        """

        if any(self.status.idna_subject.startswith(x) for x in ("http:", "https:")):
            return self.status.idna_subject
        return f"https://{self.status.idna_subject}:443"

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

        self.req = PyFunceble.factory.Requester.get(
            self.req_url, allow_redirects=allow_redirects
        )

        return self

    def do_on_body_match(
        self,
        url: str,
        matches: List[str],
        *,
        method: Callable[..., "ExtraRuleHandlerBase"],
        match_mode: str = "regex",
        strict: bool = False,
        allow_redirects: bool = False,
    ) -> "ExtraRuleHandlerBase":
        """
        Make a request to the given :code:`url` and run the given :code:`method`,
        if one of the given :code:`matches` matches.

        :param url:
            The URL to query.
        :param matches:
            A list of strings to match.
        :param match_mode:
            A matching mode. Use :code:`regex` for a regex match, and anything
            else for a string match.
        :param strict:
            Whether we should match any (:code:`False`) or all (:code:`True`).
        """

        matcher = any if not strict else all

        def handle_regex_match_mode(_req: requests.Response):
            if matcher(
                self.regex_helper.set_regex(x).match(_req.text, return_match=False)
                for x in matches
            ):
                method()

        def handle_string_match_mode(_req: requests.Response):
            if matcher(x in _req.text for x in matches):
                method()

        try:
            req = PyFunceble.factory.Requester.get(url, allow_redirects=allow_redirects)

            if match_mode == "regex":
                handle_regex_match_mode(req)
            else:
                handle_string_match_mode(req)
        except (
            PyFunceble.factory.Requester.exceptions.RequestException,
            PyFunceble.factory.Requester.exceptions.InvalidURL,
            PyFunceble.factory.Requester.exceptions.Timeout,
            PyFunceble.factory.Requester.exceptions.ConnectionError,
            PyFunceble.factory.Requester.urllib3_exceptions.InvalidHeader,
            socket.timeout,
        ):
            pass

        return self

    def do_on_header_match(
        self,
        url: str,
        matches: Dict[str, List[str]],
        *,
        method: Callable[..., "ExtraRuleHandlerBase"],
        match_mode: str = "regex",
        strict: bool = False,
        allow_redirects: bool = True,
    ) -> "ExtraRuleHandlerBase":
        """
        Make a request to the given :code:`url` and run the given :code:`method`,
        if one of the chosen header matches any of the given matches.

        :param url:
            The URL to query.
        :param matches:
            A dict representing the match.

            .. example::

                {
                    "Location": ["foo", "bar"] // try to match foo or bar
                }
        :param match_mode:
            A matching mode. Use :code:`regex` for a regex match, and anything
            else for a string match.
        :param strict:
            Whether we should match any (:code:`False`) or all (:code:`True`).
        :param allow_redirects:
            Whether we should allow redirect.
        """

        matcher = any if not strict else all

        def handle_regex_match_mode(_req: requests.Response):
            matches2search_result = {}

            for header, loc_matches in matches:
                matches2search_result[header] = False

                if header not in _req.headers:
                    continue

                if matcher(
                    self.regex_helper.set_regex(x).match(
                        _req.headers[header], return_match=False
                    )
                    for x in loc_matches
                ):
                    matches2search_result[header] = True
                    continue

            if matcher(x for x in matches2search_result.values()):
                method()

        def handle_string_match_mode(_req: requests.Response):
            matches2search_result = {}

            for header, loc_matches in matches.items():
                matches2search_result[header] = False

                if header not in _req.headers:
                    continue

                if matcher(x in _req.headers[header] for x in loc_matches):
                    matches2search_result[header] = True
                    continue

            if matcher(x for x in matches2search_result.values()):
                method()

        try:
            req = PyFunceble.factory.Requester.get(url, allow_redirects=allow_redirects)

            if match_mode == "regex":
                handle_regex_match_mode(req)
            else:
                handle_string_match_mode(req)
        except (
            PyFunceble.factory.Requester.exceptions.RequestException,
            PyFunceble.factory.Requester.exceptions.InvalidURL,
            PyFunceble.factory.Requester.exceptions.Timeout,
            PyFunceble.factory.Requester.exceptions.ConnectionError,
            PyFunceble.factory.Requester.urllib3_exceptions.InvalidHeader,
            socket.timeout,
        ):
            pass

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

    def switch_to_down_if_status_code(
        self, status_code: Union[int, List[int]]
    ) -> "ExtraRuleHandlerBase":
        """
        Switches the status to inactive if the caught status code matches one
        of the given one.
        """

        if not isinstance(status_code, (list, tuple, set)):
            status_code = [status_code]

        if any(self.status.http_status_code == x for x in status_code):
            self.switch_to_down()

        return self

    def switch_down_if_dns_match(
        self, query_type: str, matches: list
    ) -> "ExtraRuleHandlerBase":
        """
        Switches the status to inactive if the DNS query of the type :code:`query_type`
        matches any of the given :code:`matches`.

        :param query_type:
            A DNS query type.
        :param matches:
            A list of string (not regex) to match.
        """

        for record in (
            self.dns_query_tool.set_query_record_type(query_type)
            .set_subject(self.status.netloc)
            .query()
        ):
            for match in matches:
                if match in record:
                    self.switch_to_down()
                    break

        return self

    def switch_to_up(self) -> "ExtraRuleHandlerBase":
        """
        Switches the status to active.
        """

        self.status.status_after_extra_rules = PyFunceble.storage.STATUS.up
        self.status.status_source_after_extra_rules = "SPECIAL"
