"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our iana file generator.

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

import concurrent.futures
from typing import Dict, Optional, Tuple

import PyFunceble.facility
from PyFunceble.dataset.iana import IanaDataset
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.regex import RegexHelper
from PyFunceble.query.whois.query_tool import WhoisQueryTool


class IanaDBGenerator:
    """
    Provides an interface for the generation of the iana database file.
    """

    UPSTREAM_LINK: str = "https://www.iana.org/domains/root/db"
    """
    Provides the upstream link.
    """

    IANA_WHOIS_SERVER: str = "whois.iana.org"
    """
    The WHOIS server provided by the IANA.
    """

    MANUAL_SERVER: Dict[str, str] = {
        "bm": "whois.afilias-srs.net",
        "bz": "whois.afilias-grs.net",
        "cd": "chois.nic.cd",
        "cm": "whois.netcom.cm",
        "fj": "whois.usp.ac.fj",
        "ga": "whois.my.ga",
        "int": "whois.iana.org",
        "ipiranga": " whois.nic.ipiranga",
        "lc": "whois2.afilias-grs.net",
        "now": " whois.nic.now",
        "pharmacy": " whois.nic.pharmacy",
        "piaget": " whois.nic.piaget",
        "ps": "whois.pnina.ps",
        "rw": "whois.ricta.org.rw",
        "shaw": "whois.afilias-srs.net",
        "xn--1ck2e1b": "whois.nic.xn--1ck2e1b",
        "xn--2scrj9c": "whois.inregistry.net",
        "xn--3hcrj9c": "whois.inregistry.net",
        "xn--45br5cyl": "whois.inregistry.net",
        "xn--45brj9c": "whois.inregistry.net",
        "xn--8y0a063a": "whois.nic.xn--8y0a063a",
        "xn--bck1b9a5dre4c": "whois.nic.xn--bck1b9a5dre4c",
        "xn--cck2b3b": "whois.nic.xn--cck2b3b",
        "xn--czr694b": "whois.nic.xn--czr694b",
        "xn--e1a4c": "whois.eu",
        "xn--eckvdtc9d": "whois.nic.xn--eckvdtc9d",
        "xn--fct429k": "whois.nic.xn--fct429k",
        "xn--fpcrj9c3d": "whois.inregistry.net",
        "xn--fzc2c9e2c": "whois.nic.lk",
        "xn--g2xx48c": "whois.nic.xn--g2xx48c",
        "xn--gckr3f0f": "whois.nic.xn--gckr3f0f",
        "xn--gecrj9c": "whois.inregistry.net",
        "xn--gk3at1e": "whois.nic.xn--gk3at1e",
        "xn--h2breg3eve": "whois.inregistry.net",
        "xn--h2brj9c": "whois.inregistry.net",
        "xn--h2brj9c8c": "whois.inregistry.net",
        "xn--imr513n": "whois.nic.xn--imr513n",
        "xn--jvr189m": "whois.nic.xn--jvr189m",
        "xn--kpu716f": "whois.nic.xn--kpu716f",
        "xn--mgba3a3ejt": "whois.nic.xn--mgba3a3ejt",
        "xn--mgbb9fbpob": "whois.nic.xn--mgbb9fbpob",
        "xn--mgbbh1a": "whois.inregistry.net",
        "xn--mgbbh1a71e": "whois.inregistry.net",
        "xn--mgbgu82a": "whois.inregistry.net",
        "xn--nyqy26a": "whois.nic.xn--nyqy26a",
        "xn--otu796d": "whois.nic.xn--otu796d",
        "xn--pbt977c": "whois.nic.xn--pbt977c",
        "xn--rhqv96g": "whois.nic.xn--rhqv96g",
        "xn--rovu88b": "whois.nic.xn--rovu88b",
        "xn--rvc1e0am3e": "whois.inregistry.net",
        "xn--s9brj9c": "whois.inregistry.net",
        "xn--ses554g": "whois.registry.knet.cn",
        "xn--wgbh1c": "whois.dotmasr.eg",
        "xn--xkc2al3hye2a": "whois.nic.lk",
        "xn--xkc2dl3a5ee0h": "whois.inregistry.net",
        "za": "whois.registry.net.za",
    }

    _destination: Optional[str] = None

    database: dict = {}
    """
    An internal storage map.
    """

    def __init__(self, destination: Optional[str] = None) -> None:
        if destination is not None:
            self.destination = destination
        else:
            self.destination = IanaDataset().source_file

    @property
    def destination(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_destination` attribute.
        """

        return self._destination

    @destination.setter
    def destination(self, value: str) -> None:
        """
        Sets the destination to write.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._destination = value

    def set_destination(self, value: str) -> "IanaDBGenerator":
        """
        Sets the destination to write.

        :param value:
            The value to set.
        """

        self.destination = value

        return self

    def get_referrer_from_extension(self, extension: str) -> Optional[str]:
        """
        Given an extension, tries to get or guess its extension.
        """

        whois_query_tool = WhoisQueryTool()

        dummy_domain = f"hello.{extension}"
        iana_record = (
            whois_query_tool.set_server(self.IANA_WHOIS_SERVER)
            .set_subject(dummy_domain)
            .record
        )

        if iana_record and "refer" in iana_record:
            regex_referrer = r"(?s)refer\:\s+([a-zA-Z0-9._-]+)\n"

            matched = RegexHelper(regex_referrer).match(
                iana_record, return_match=True, group=1
            )

            if matched:
                return matched

        possible_server = f"whois.nic.{extension}"
        response = whois_query_tool.set_server(possible_server).record

        if response:
            return possible_server

        if extension in self.MANUAL_SERVER:
            possible_server = self.MANUAL_SERVER[extension]

            response = whois_query_tool.set_server(possible_server).record

            if response:
                return possible_server

        return None

    def get_extension_and_referrer_from_block(
        self, block: str
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Given an HTML block, we try to extract an extension and it's underlying
        referrer (WHOIS server).

        The referrer is extracted from the official IANA page, and guessed if
        missing.

        :param block:
            The block to parse.
        """

        regex_valid_extension = r"(/domains/root/db/)(.*)(\.html)"

        regex_helper = RegexHelper(regex_valid_extension)

        if regex_helper.match(block, return_match=False):
            extension = regex_helper.match(block, return_match=True, group=2)

            if extension:
                return extension, self.get_referrer_from_extension(extension)

        return None, None

    def start(self, max_workers: Optional[int] = None) -> "IanaDBGenerator":
        """
        Starts the generation of the dataset file.

        :param max_workers:
            The maximal number of workers we are allowed to use.
        """

        raw_data = (
            DownloadHelper(self.UPSTREAM_LINK)
            .download_text()
            .split('<span class="domain tld">')
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for extension, whois_server in executor.map(
                self.get_extension_and_referrer_from_block, raw_data
            ):
                if extension:
                    self.database[extension] = whois_server

                    PyFunceble.facility.Logger.debug(
                        "Got: extension: %r ; whois server: %r", extension, whois_server
                    )

        DictHelper(self.database).to_json_file(self.destination)

        return self
