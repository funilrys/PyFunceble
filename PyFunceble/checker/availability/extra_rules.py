"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the domains availability checker.

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
import socket
from typing import Callable, List, Optional

from box import Box

import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus
from PyFunceble.helpers.regex import RegexHelper


class ExtraRulesHandler:
    """
    Provides our very own extra rules handler.

    :param status:
        The previously gathered status.
    :type status:
        :class:`~PyFunceble.checker.availability.status.AvailabilityCheckerStatus`
    """

    _status: Optional[AvailabilityCheckerStatus] = None

    regex_active2inactive_through_potentially_down: dict = dict()
    regex_active2inactive_through_potentially_up: dict = dict()

    http_codes_dataset: Optional[Box] = None

    def __init__(self, status: Optional[AvailabilityCheckerStatus]) -> None:
        self.regex_active2inactive_through_potentially_down = {
            r"\.000webhostapp\.com": [self.__switch_to_down_if_410],
            r"\.angelfire\.com$": [self.__switch_to_down_if_404],
            r"\.blogspot\.": [self.__handle_blogspot],
            r"\.canalblog\.com$": [self.__switch_to_down_if_404],
            r"\.github\.io$": [self.__switch_to_down_if_404],
            r"\.hpg.com.br$": [self.__switch_to_down_if_404],
            r"\.liveadvert\.com$": [self.__switch_to_down_if_404],
            r"\.skyrock\.com$": [self.__switch_to_down_if_404],
            r"\.tumblr\.com$": [self.__switch_to_down_if_404],
            r"\.wix\.com$": [self.__switch_to_down_if_404],
        }

        self.regex_active2inactive_through_potentially_up = {
            r"\.blogspot\.": [self.__handle_blogspot],
            r"\.wordpress\.com$": [self.__handle_wordpress_dot_com],
        }

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.http_codes_dataset = PyFunceble.storage.HTTP_CODES
        else:
            self.http_codes_dataset = PyFunceble.storage.STD_HTTP_CODES

        if status is not None:
            self.status = status

        # Be sure that all settings are loaded proprely!!
        PyFunceble.factory.Requester.guess_all_settings()

    def ensure_status_is_given(
        func: Callable[..., "ExtraRulesHandler"]
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

    def set_status(self, value: AvailabilityCheckerStatus) -> "ExtraRulesHandler":
        """
        Sets the status to work with.

        :param value:
            The status to work with.
        """

        self.status = value

        return self

    def __web_regex_handler(
        self,
        url: str,
        regex_list: List[str],
        method: Callable[..., "ExtraRulesHandler"],
    ) -> "ExtraRulesHandler":
        """
        Handles a web request along with a regex filter.
        """

        try:
            req = PyFunceble.factory.Requester.get(url, allow_redirects=True)

            for regex in regex_list:
                if regex in req.text or RegexHelper(regex).match(
                    req.text, return_match=False
                ):
                    method()
                    break
        except (
            PyFunceble.factory.Requester.exceptions.InvalidURL,
            PyFunceble.factory.Requester.exceptions.Timeout,
            PyFunceble.factory.Requester.exceptions.ConnectionError,
            PyFunceble.factory.Requester.urllib3_exceptions.InvalidHeader,
            socket.timeout,
        ):
            pass

        return self

    def __regex_registry_handler(self, regex_registry: dict) -> "ExtraRulesHandler":
        """
        Handles the standard regex lookup case.
        """

        for (
            regex,
            methods,
        ) in regex_registry.items():
            broken = False
            for method in methods:
                if RegexHelper(regex).match(self.status.subject, return_match=False):
                    method()

                    broken = True
                    break

            if broken:
                break

        return self

    def __switch_to_down(self) -> "ExtraRulesHandler":
        """
        Switches the status to inactive.
        """

        self.status.status_after_extra_rules = PyFunceble.storage.STATUS.down
        self.status.status_source_after_extra_rules = "SPECIAL"

        return self

    def __switch_to_down_if_404(self) -> "ExtraRulesHandler":
        """
        Switches the status to inactive if the status code is set to 404.
        """

        if self.status.http_status_code == 404:
            self.__switch_to_down()

        return self

    def __switch_to_down_if_410(self) -> "ExtraRulesHandler":
        """
        Switches the status to inactive if the status code is set to 410.
        """

        if self.status.http_status_code == 410:
            self.__switch_to_down()

        return self

    def __switch_to_up(self) -> "ExtraRulesHandler":
        """
        Switches the status to active.
        """

        self.status.status_after_extra_rules = PyFunceble.storage.STATUS.up
        self.status.status_source_after_extra_rules = "SPECIAL"

    def __handle_blogspot(self) -> "ExtraRulesHandler":
        """
        Handles the :code:`blogspot.*` case.

        .. warning::
            This method assume that we know that we are handling a blogspot domain.
        """

        regex_blogger = [r"create-blog.g?", r"87065", r"doesn&#8217;t&nbsp;exist"]

        if self.status.subject.starts("http:"):
            url = self.status.subject
        else:
            url = f"http://{self.status.subject}:80"

        self.__web_regex_handler(url, regex_blogger, self.__switch_to_down)

        return self

    def __handle_wordpress_dot_com(self) -> "ExtraRulesHandler":
        """
        Handles the :code:`wordpress.com` case.

        .. warning::
            This method assume that we know that we are handling a blogspot domain.
        """

        regex_wordpress = [r"doesn&#8217;t&nbsp;exist"]

        if self.status.subject.starts("http:"):
            url = self.status.subject
        else:
            url = f"http://{self.status.subject}:80"

        self.__web_regex_handler(url, regex_wordpress, self.__switch_to_down)

        return self

    def __handle_potentially_down(self) -> "ExtraRulesHandler":
        """
        Handles the status deescalation though the list of potentially DOWN
        status code.
        """

        if (
            self.status.http_status_code
            and self.status.http_status_code
            in self.http_codes_dataset.list.potentially_down
        ):
            self.__regex_registry_handler(
                self.regex_active2inactive_through_potentially_down
            )

        return self

    def __handle_potentially_up(self) -> "ExtraRulesHandler":
        """
        Handles the status deescalation though the list of potentially UP
        status code.
        """

        if (
            self.status.http_status_code
            and self.status.http_status_code
            in self.http_codes_dataset.list.potentially_up
        ):
            self.__regex_registry_handler(
                self.regex_active2inactive_through_potentially_up
            )

        return self

    @ensure_status_is_given
    def start(self) -> "ExtraRulesHandler":
        """
        Starts the process.
        """

        PyFunceble.facility.Logger.info(
            "Started to check %r against our own set of rules.",
            self.status.idna_subject,
        )

        self.status.status_before_extra_rules = self.status.status
        self.status.status_source_before_extra_rules = self.status.status_source

        if self.status.status_before_extra_rules == PyFunceble.storage.STATUS.up:
            if (
                self.status.http_status_code
                in self.http_codes_dataset.list.potentially_down
            ):
                self.__handle_potentially_down()

            if not self.status.status_after_extra_rules:
                self.__handle_potentially_up()

        if (
            not self.status.status_after_extra_rules
            and self.status.status_before_extra_rules in PyFunceble.storage.STATUS.down
        ):
            if self.status.ipv4_range_syntax or self.status.ipv6_range_syntax:
                self.__switch_to_up()

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

        PyFunceble.facility.Logger.info(
            "Finished to check %r against our own set of rules.",
            self.status.idna_subject,
        )
