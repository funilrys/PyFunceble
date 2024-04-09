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

from typing import Optional

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
                (self.switch_to_down_if_status_code, {410, 424}),
            ],
            r"\.24\.eu$": [(self.switch_to_down_if_status_code, 503)],
            r"\.altervista\.org$": [(self.switch_to_down_if_status_code, 403)],
            r"\.angelfire\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.blogspot\.": [self.handle_blogspot],
            r"\.canalblog\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.dr\.ag$": [(self.switch_to_down_if_status_code, 503)],
            r"\.fc2\.com$": [self.handle_fc2_dot_com],
            r"\.github\.io$": [(self.switch_to_down_if_status_code, 404)],
            r"\.glitchz\.me$": [(self.switch_to_down_if_status_code, 403)],
            r"\.godaddysites\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.hpg.com.br$": [(self.switch_to_down_if_status_code, 404)],
            r"\.imgur\.com$": [self.handle_imgur_dot_com],
            r"\.liveadvert\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.myhuaweicloudz\.com$": [(self.switch_to_down_if_status_code, 403)],
            r"\.skyrock\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.sz.id$": [(self.switch_to_down_if_status_code, 302)],
            r"\.translate\.goog$": [(self.switch_to_down_if_status_code, 403)],
            r"\.tumblr\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"\.web\.app$": [(self.switch_to_down_if_status_code, 404)],
            r"\.wix\.com$": [(self.switch_to_down_if_status_code, 404)],
            r"^s3\.ap-south-1\.amazonaws\.com$": [
                (self.switch_to_down_if_status_code, 403)
            ],
            r"^u\.pcloud\.com$": [(self.switch_to_down_if_status_code, 302)],
            r"\.wordpress\.com$": [
                (self.switch_to_down_if_status_code, 410),
                self.handle_wordpress_dot_com,
            ],
            r"\.weebly\.com$": [(self.switch_to_down_if_status_code, {"404", "406"})],
            r"\.zzz\.com\.ua$": [(self.switch_to_down_if_status_code, {"402"})],
        }

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.http_codes_dataset = PyFunceble.storage.HTTP_CODES
        else:
            self.http_codes_dataset = PyFunceble.storage.STD_HTTP_CODES

        super().__init__(status)

    def __regex_registry_handler(self, regex_registry: dict) -> "ExtraRulesHandler":
        """
        Handles the standard regex lookup case.
        """

        regex_helper = RegexHelper()

        for (
            regex,
            data,
        ) in regex_registry.items():
            broken = False
            for element in data:
                if not regex_helper.set_regex(regex).match(
                    self.status.netloc, return_match=False
                ):
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

        self.do_on_body_match(
            self.req_url,
            regex_blogger,
            method=self.switch_to_down,
            allow_redirects=True,
        )

        return self

    def handle_wordpress_dot_com(self) -> "ExtraRulesHandler":
        """
        Handles the :code:`wordpress.com` case.

        .. warning::
            This method assume that we know that we are handling a blogspot domain.
        """

        regex_wordpress = [r"doesn&#8217;t&nbsp;exist", r"no\slonger\savailable"]

        self.do_on_body_match(
            self.req_url,
            regex_wordpress,
            method=self.switch_to_down,
            allow_redirects=True,
        )

        return self

    def handle_fc2_dot_com(self) -> "ExtraRulesHandler":
        """
        Handles the :code:`fc2.com` case.

        .. warning::
            This method assume that we know that we are handling a fc2 domain.
        """

        self.do_on_header_match(
            self.req_url,
            {"location": ["error.fc2.com"]},
            method=self.switch_to_down,
            match_mode="std",
            strict=True,
            allow_redirects=False,
        )

        return self

    def handle_imgur_dot_com(self) -> "ExtraRulesHandler":
        """
        Handles the :code:`imgur.com` case.

        .. warning:.
            This method are assuming we are handling a imgur.com subdomain.
        """

        req = PyFunceble.factory.Requester.get(
            self.req_url_https, allow_redirects=False
        )
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
