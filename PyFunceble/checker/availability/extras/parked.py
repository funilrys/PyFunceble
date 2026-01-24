"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the extra rules handler based on the "parked status" of a subject.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025, 2026 Nissar Chababy

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

import PyFunceble.storage
from PyFunceble.checker.availability.extras.base import ExtraRuleHandlerBase


class ParkedRulesHandler(ExtraRuleHandlerBase):
    """
    Provides our very own parked rules handler. This handler will try to check
    if a subject is parked.

    :param status:
        The previously gathered status.
    :type status:
        :class:`~PyFunceble.checker.availability.status.AvailabilityCheckerStatus`
    """

    PARKED_CONTENT_PATTERNS = (
        'class="parked-domains',
        "buy-domain",
        "this domain name is parked",
        "this domain is parked",
        "interested in this domain",
        "really cool domain parked",
        "domain is for sale",
        '_trackpageview("/parked/[% parked_type %]/',
        "| parked domain",
        "parked banner",
        "contact with domain owner",
        "web page is parked",
        "buy or lease this domain",
        "parked domain name on ",
        "it is currently parked by the owner",
        "parked page for",
    )

    def _switch_down_by_cookie(self) -> "ParkedRulesHandler":
        """
        Tries to switch the status to inactive if some special cookies where found.
        """

        if "parking_session" in self.req.cookies:
            self.switch_to_down()

        return self

    def _switch_down_by_content(self) -> "ParkedRulesHandler":
        """
        Tries to switch the status to inactive if some relative content were found.
        """

        content = self.req.text.lower()

        if any(x in content for x in self.PARKED_CONTENT_PATTERNS):
            self.switch_to_down()

        return self

    @ExtraRuleHandlerBase.ensure_status_is_given
    @ExtraRuleHandlerBase.setup_status_before
    @ExtraRuleHandlerBase.setup_status_after
    def start(self) -> "ParkedRulesHandler":
        PyFunceble.facility.Logger.info(
            "Started to check %r against our own set of parked rules.",
            self.status.idna_subject,
        )

        try:
            self.do_request()

            if self.status.status_before_extra_rules == PyFunceble.storage.STATUS.up:
                self._switch_down_by_cookie()

            if not self.status.status_after_extra_rules:
                self._switch_down_by_content()

            PyFunceble.facility.Logger.info(
                "Finished to check %r against our own set of parked rules.",
                self.status.idna_subject,
            )
        except self.requester.exceptions.RequestException:
            pass

        return self
