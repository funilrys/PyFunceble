"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the extra rules handler based on some DNS records.

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

import PyFunceble.facility
from PyFunceble.checker.availability.extras.base import ExtraRuleHandlerBase
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus


class DNSRulesHandler(ExtraRuleHandlerBase):
    """
    Provides our very own sets of DNS based rules.

    :param status:
        The previously gathered status.
    :type status:
        :class:`~PyFunceble.checker.availability.status.AvailabilityCheckerStatus`
    """

    rulesets: dict = {}

    def __init__(self, status: Optional[AvailabilityCheckerStatus] = None) -> None:
        self.rulesets = {
            r"\.(25u\.com|2waky\.com|3-a\.net|4dq\.com|4pu\.com|acmetoy\.com|"
            r"almostmy\.com|americanunfinished\.com|as19557\.net|"
            r"authorizeddns\.net|authorizeddns\.org|authorizeddns\.us|"
            r"b0tnet\.com|bigmoney\.biz|changeip\.biz|changeip\.co|"
            r"changeip\.net|changeip\.org|changeip\.us|cleansite\.biz|"
            r"cleansite\.info|cleansite\.us|ddns\.info|ddns\.mobi|ddns\.ms|"
            r"ddns\.us|dhcp\.biz|dns-dns\.com|dns-report\.com|dns-stuff\.com|"
            r"dns04\.com|dns05\.com|dns1\.us|dns2\.us|dnset\.com|"
            r"dnsfailover\.net|dnsrd\.com|dsmtp\.biz|dsmtp\.com|dubya\.biz|"
            r"dubya\.info|dubya\.net|dubya\.us|dumb1\.com|dynamic-dns\.net|"
            r"dynamicdns\.biz|dynssl\.com|edns\.biz|esmtp\.biz|ezua\.com|"
            r"faqserv\.com|fartit\.com|freeddns\.com|freetcp\.com|freewww\.biz|"
            r"freewww\.info|ftp1\.biz|ftpserver\.biz|gettrials\.com|"
            r"got-game\.org|gr8domain\.biz|gr8name\.biz|homingbeacon\.net|"
            r"https443\.net|https443\.org|ikwb\.com|instanthq\.com|iownyour\.biz|"
            r"iownyour\.org|isasecret\.com|itemdb\.com|itsaol\.com|jetos\.com|"
            r"jkub\.com|jungleheart\.com|justdied\.com|lflink\.com|lflinkup\.com|"
            r"lflinkup\.net|lflinkup\.org|longmusic\.com|mefound\.com|"
            r"misecure\.com|moneyhome\.biz|mrbasic\.com|mrbonus\.com|mrface\.com|"
            r"mrslove\.com|my03\.com|mydad\.info|myddns\.com|myftp\.info|"
            r"mylftv\.com|mymom\.info|mynetav\.com|mynetav\.net|mynetav\.org|"
            r"mynumber\.org|mypicture\.info|mypop3\.net|mypop3\.org|"
            r"mysecondarydns\.com|mywww\.biz|myz\.info|ninth\.biz|ns01\.biz|"
            r"ns01\.info|ns01\.us|ns02\.biz|ns02\.info|ns02\.us|ns1\.name|"
            r"ns2\.name|ns3\.name|ocry\.com|onedumb\.com|onmypc\.biz|"
            r"onmypc\.info|onmypc\.net|onmypc\.org|onmypc\.us|"
            r"organiccrap\.com|otzo\.com|ourhobby\.com|port25\.biz|"
            r"proxydns\.com|qhigh\.com|qpoe\.com|rebatesrule\.net|"
            r"sendsmtp\.com|serveuser\.com|serveusers\.com|sexidude\.com|"
            r"sexxxy\.biz|sixth\.biz|squirly\.info|ssl443\.org|ssmailer\.com|"
            r"toh\.info|toshibanetcam\.com|toythieves\.com|trickip\.net|"
            r"trickip\.org|vizvaz\.com|wikaba\.com|www1\.biz|"
            r"wwwhost\.biz|wwwhost\.us|x24hr\.com|xxuz\.com|xxxy\.biz|"
            r"xxxy\.info|ygto\.com|youdontcare\.com|yourtrap\.com|"
            r"zyns\.com|zzux\.com)(\.|)$": [
                (self.switch_down_if_dns_match, ("SOA", ["abuse.changeip.com."]))
            ]
        }

        super().__init__(status)

    @ExtraRuleHandlerBase.ensure_status_is_given
    @ExtraRuleHandlerBase.setup_status_before
    @ExtraRuleHandlerBase.setup_status_after
    def start(self) -> "DNSRulesHandler":
        """
        Process the check and handling of the current subject.
        """

        PyFunceble.facility.Logger.info(
            "Started to check %r against our subject switcher rules.",
            self.status.idna_subject,
        )

        for regex, rulesets in self.rulesets.items():
            if self.status.status_after_extra_rules:
                break

            if not self.regex_helper.set_regex(regex).match(
                self.status.netloc, return_match=False
            ):
                break

            for ruler, params in rulesets:
                if self.status.status_after_extra_rules:
                    break

                ruler(*params)

        PyFunceble.facility.Logger.info(
            "Finished to check %r against our subject switcher rules.",
            self.status.idna_subject,
        )
