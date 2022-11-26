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

from typing import Optional

import requests

import PyFunceble.factory
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

    req: Optional[requests.Response] = None

    def _do_request(self, *, allow_redirects: bool = True) -> "ParkedRulesHandler":
        """
        Do a request and store its response into the `req` attribute.

        :param bool allow_redirects:
            Whether we shoold follow the redirection - or not.
        """

        if self.status.idna_subject.startswith(
            "http:"
        ) or self.status.idna_subject.startswith("https://"):
            url = self.status.idna_subject
        else:
            url = f"http://{self.status.idna_subject}:80"

        self.req = PyFunceble.factory.Requester.get(
            url, allow_redirects=allow_redirects
        )

        return self

    def _switch_down_by_cookie(self) -> "ParkedRulesHandler":
        """
        Tries to switch the status to inactive if some special cookies where found.
        """

        if "parking_session" in self.req.cookies:
            self.switch_to_down()

        return self

    def _swith_down_by_content(self) -> "ParkedRulesHandler":
        """
        Tries to switch the status to inactive if some relative content were found.
        """

        content = self.req.text.lower()

        if (  # pylint: disable=too-many-boolean-expressions
            'class="parked-domains' in content
            or "buy-domain" in content
            or "this domain name is parked" in content
            or "this domain is parked" in content
            or "interested in this domain" in content
            or "really cool domain parked" in content
            or "domain is for sale" in content
            or '_trackpageview("/parked/[% parked_type %]/' in content
            or "| parked domain" in content
            or "parked banner" in content
            or "contact with domain owner" in content
            or "web page is parked" in content
            or "buy or lease this domain" in content
            or "parked domain name on " in content
            or "it is currently parked by the owner" in content
            or "parked page for" in content
        ):
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
            self._do_request()

            if self.status.status_before_extra_rules == PyFunceble.storage.STATUS.up:
                self._switch_down_by_cookie()

            if not self.status.status_after_extra_rules:
                self._swith_down_by_content()

            PyFunceble.facility.Logger.info(
                "Finished to check %r against our own set of parked rules.",
                self.status.idna_subject,
            )
        except PyFunceble.factory.Requester.exceptions.RequestException:
            pass

        return self
