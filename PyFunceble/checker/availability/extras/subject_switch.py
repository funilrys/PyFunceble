"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the extra rules handler based on the "switching" domain behavior of some
subjects.

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

import PyFunceble.facility
from PyFunceble.checker.availability.extras.base import ExtraRuleHandlerBase
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus
from PyFunceble.converter.url2netloc import Url2Netloc


class SubjectSwitchRulesHandler(ExtraRuleHandlerBase):
    """
    Provides our very own "subject switch" handler.

    This handler will be used to detects a subject switch behavior from a server.
    In other words, this handler should be able to detect the following scenario
    and switch the original subject to :code:`INACTIVE`.

        1. https://www.example.org/hello/world -> https://example.org/hello/world
        2. https://m.example.org/hello/world -> https://example.org/hello/world
    """

    url2netloc: Optional[Url2Netloc] = None

    def __init__(self, status: Optional[AvailabilityCheckerStatus] = None) -> None:
        self.url2netloc = Url2Netloc()
        super().__init__(status)

    def _switch_down_by_history(self) -> "SubjectSwitchRulesHandler":
        """
        Tries to switch the status to :code:`INACTIVE` by following hte history.
        """

        variations = set(
            [
                self.status.netloc.replace("www.", "", 1),
                self.status.netloc.replace("m.", "", 1),
            ]
        )
        # The current netloc should be included in the variations
        variations.remove(self.status.netloc)

        start_path = (
            self.url2netloc.set_data_to_convert(self.req_url)
            .parse_url()
            .parsed_url.path
        )

        for response in self.req.history:
            if (
                not str(response.status_code).startswith("3")
                or "location" not in response.headers
            ):
                continue

            redirect_url = response.headers["location"]

            netloc = self.url2netloc.set_data_to_convert(redirect_url).get_converted()
            local_path = self.url2netloc.parsed_url.path

            if netloc == self.status.idna_subject and netloc not in variations:
                continue

            if not start_path:
                if local_path != "/":
                    continue
            elif start_path != local_path:
                continue

            self.switch_to_down()
            break

        return self

    @ExtraRuleHandlerBase.ensure_status_is_given
    @ExtraRuleHandlerBase.setup_status_before
    @ExtraRuleHandlerBase.setup_status_after
    def start(self) -> "SubjectSwitchRulesHandler":
        """
        Process the check and handling of the current subject.
        """

        PyFunceble.facility.Logger.info(
            "Started to check %r against our subject switcher rules.",
            self.status.idna_subject,
        )

        try:
            if any(self.status.netloc.startswith(x) for x in ("www.", "m.")):
                self.do_request()

                if not self.status.status_after_extra_rules:
                    self._switch_down_by_history()
        except PyFunceble.factory.Requester.exceptions.RequestException:
            pass

        PyFunceble.facility.Logger.info(
            "Finished to check %r against our subject switcher rules.",
            self.status.idna_subject,
        )

        return self
