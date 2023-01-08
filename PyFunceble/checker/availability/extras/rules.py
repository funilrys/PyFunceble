"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the extra rules handler based on the status code.

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

import socket
from typing import Callable, List, Optional

from box import Box

import PyFunceble.facility
import PyFunceble.factory
import PyFunceble.storage
from PyFunceble.checker.availability.extras.base import ExtraRuleHandlerBase
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus
from PyFunceble.helpers.regex import RegexHelper


class ExtraRulesHandler(ExtraRuleHandlerBase):
    """
    Provides our very own extra rules handler.

    :param status:
        The previously gathered status.
    :type status:
        :class:`~PyFunceble.checker.availability.status.AvailabilityCheckerStatus`
    """

    regex_active2inactive: dict = {}
    http_codes_dataset: Optional[Box] = None

    def __init__(self, status: Optional[AvailabilityCheckerStatus] = None) -> None:

        self.regex_active2inactive = {
            r"\.000webhostapp\.com": [
                (self.switch_to_down_if_status_code, 410),
            ],
            r"\.24\.eu$": [(self.switch_to_down_if_status_code, 503)],
            r"\.altervista\.org$": [(self.switch_to_down_if_status_code, 403)],
            r"\.angelfire\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.blogspot\.": [self.handle_blogspot],
            r"\.canalblog\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.dr\.ag$": [(self.switch_to_down_if_status_code, 503)],
            r"\.fc2\.com$": [self.handle_fc2_dot_com],
            r"\.github\.io$": [(self.switch_to_down_if_status_code, 404)],
            r"\.godaddysites\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.hpg.com.br$": [(self.switch_to_down_if_status_code, 404)],
            r"\.imgur\.com$": [self.handle_imgur_dot_com],
            r"\.liveadvert\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.skyrock\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.tumblr\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.wix\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.wordpress\.com$": [
                (self.switch_to_down_if_status_code, 410),
                self.handle_wordpress_dot_com,
            ],
            r"\.weebly\.com$": [(self.switch_to_down_if_status_code, 404)],
        }

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.http_codes_dataset = PyFunceble.storage.HTTP_CODES
        else:
            self.http_codes_dataset = PyFunceble.storage.STD_HTTP_CODES

        super().__init__(status)

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
            PyFunceble.factory.Requester.exceptions.RequestException,
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
            data,
        ) in regex_registry.items():
            broken = False
            for element in data:
                if not RegexHelper(regex).match(self.status.netloc, return_match=False):
                    continue

                if isinstance(element, tuple):
                    element[0](*element[1:])
                else:
                    element()

                if self.status.status_after_extra_rules:
                    broken = True
                    break

            if broken:
                break

        return self

    def handle_blogspot(self) -> "ExtraRulesHandler":
        """
        Handles the :code:`blogspot.*` case.

        .. warning::
            This method assume that we know that we are handling a blogspot domain.
        """

        regex_blogger = [r"create-blog.g?", r"87065", r"doesn&#8217;t&nbsp;exist"]

        if self.status.idna_subject.startswith(
            "http:"
        ) or self.status.idna_subject.startswith("https://"):
            url = self.status.idna_subject
        else:
            url = f"http://{self.status.idna_subject}:80"

        self.__web_regex_handler(url, regex_blogger, self.switch_to_down)

        return self

    def handle_wordpress_dot_com(self) -> "ExtraRulesHandler":
        """
        Handles the :code:`wordpress.com` case.

        .. warning::
            This method assume that we know that we are handling a blogspot domain.
        """

        regex_wordpress = [r"doesn&#8217;t&nbsp;exist", r"no\slonger\savailable"]

        if self.status.idna_subject.startswith(
            "http:"
        ) or self.status.idna_subject.startswith("https://"):
            url = self.status.idna_subject
        else:
            url = f"http://{self.status.idna_subject}:80"

        self.__web_regex_handler(url, regex_wordpress, self.switch_to_down)

        return self

    def handle_fc2_dot_com(self) -> "ExtraRulesHandler":
        """
        Handles the :code:`fc2.com` case.

        .. warning::
            This method assume that we know that we are handling a fc2 domain.
        """

        if self.status.idna_subject.startswith(
            "http:"
        ) or self.status.idna_subject.startswith("https://"):
            url = self.status.idna_subject
        else:
            url = f"http://{self.status.idna_subject}:80"

        req = PyFunceble.factory.Requester.get(url, allow_redirects=False)

        if "Location" in req.headers and "error.fc2.com" in req.headers["Location"]:
            self.switch_to_down()

        return self

    def handle_imgur_dot_com(self) -> "ExtraRulesHandler":
        """
        Handles the :code:`imgur.com` case.

        .. warning:.
            This method assume that we know that we are handling a imgur.com
            sub-domain.
        """

        if self.status.idna_subject.startswith(
            "http:"
        ) or self.status.idna_subject.startswith("https://"):
            url = self.status.idna_subject
        else:
            url = f"https://{self.status.idna_subject}"

        req = PyFunceble.factory.Requester.get(url, allow_redirects=False)
        username = self.status.netloc.replace(".imgur.com", "")

        if "Location" in req.headers:
            if req.headers["Location"].endswith(("/removed.png", f"/user/{username}")):
                self.switch_to_down()

        return self

    def __handle_active2inactive(self) -> "ExtraRulesHandler":
        """
        Handles the status deescalation.
        """

        if self.status.http_status_code:
            self.__regex_registry_handler(self.regex_active2inactive)

        return self

    @ExtraRuleHandlerBase.ensure_status_is_given
    @ExtraRuleHandlerBase.setup_status_before
    @ExtraRuleHandlerBase.setup_status_after
    def start(self) -> "ExtraRulesHandler":
        """
        Starts the process.
        """

        PyFunceble.facility.Logger.info(
            "Started to check %r against our own set of extra rules.",
            self.status.idna_subject,
        )

        if self.status.status_before_extra_rules == PyFunceble.storage.STATUS.up:
            self.__handle_active2inactive()

        if (
            not self.status.status_after_extra_rules
            and self.status.status_before_extra_rules in PyFunceble.storage.STATUS.down
        ):
            if self.status.ipv4_range_syntax or self.status.ipv6_range_syntax:
                self.switch_to_up()

        PyFunceble.facility.Logger.info(
            "Finished to check %r against our own set of extra rules.",
            self.status.idna_subject,
        )

        return self
