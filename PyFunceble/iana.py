#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the IANA logic and interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long
# pylint: disable=bad-continuation
import PyFunceble
from PyFunceble.helpers import Dict, Download, File, Regex


class IANA:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Logic behind the update of `iana-domains-db.json`
    """

    def __init__(self):
        if not PyFunceble.CONFIGURATION["quiet"]:
            # The quiet mode is not activated.

            # We print on screen what we are doing.
            print("Update of iana-domains-db", end=" ")

        # We get the destination of the constructed IANA database.
        self.destination = PyFunceble.OUTPUTS["default_files"]["iana"]

        if PyFunceble.path.isfile(self.destination):
            # The destination exist.

            # We get its content.
            self.iana_db = Dict().from_json(File(self.destination).read())
        else:
            # The destination does not exist.

            # We initiate the local variable which will save the content of the database.
            self.iana_db = {}

        # We initiate the URL to the IANA Root Zone Database page.
        self.iana_url = "https://www.iana.org/domains/root/db"

        # We map the list of server which have to be set manually because
        # they are not present into the IANA Root Zone Database.
        self.manual_server = {
            "aaa": "whois.nic.aaa",
            "abb": "whois.nic.abb",
            "able": "whois.nic.able",
            "accenture": "whois.nic.accenture",
            "aetna": "whois.nic.aetna",
            "aig": "whois.nic.aig",
            "americanexpress": "whois.nic.americanexpress",
            "amex": "whois.nic.amex",
            "amica": "whois.nic.amica",
            "amsterdam": "whois.nic.amsterdam",
            "analytics": "whois.nic.analytics",
            "aramco": "whois.nic.aramco",
            "arte": "whois.nic.arte",
            "as": "whois.nic.as",
            "athleta": "whois.nic.athleta",
            "audible": "whois.nic.audible",
            "author": "whois.nic.author",
            "aws": "whois.nic.aws",
            "axa": "whois.nic.axa",
            "azure": "whois.nic.azure",
            "baby": "whois.nic.baby",
            "banamex": "whois.nic.banamex",
            "bananarepublic": "whois.nic.bananarepublic",
            "baseball": "whois.nic.baseball",
            "bharti": "whois.nic.bharti",
            "bing": "whois.nic.bing",
            "bloomberg": "whois.nic.bloomberg",
            "bm": "whois.afilias-srs.net",
            "book": "whois.nic.book",
            "booking": "whois.nic.booking",
            "bot": "whois.nic.bot",
            "buzz": "whois.nic.buzz",
            "bz": "whois.afilias-grs.net",
            "call": "whois.nic.call",
            "calvinklein": "whois.nic.calvinklein",
            "caravan": "whois.nic.caravan",
            "cartier": "whois.nic.cartier",
            "caseih": "whois.nic.caseih",
            "cbn": "whois.nic.cbn",
            "cbre": "whois.nic.cbre",
            "cd": "chois.nic.cd",
            "chase": "whois.nic.chase",
            "circle": "whois.nic.circle",
            "cisco": "whois.nic.cisco",
            "citadel": "whois.nic.citadel",
            "citi": "whois.nic.citi",
            "citic": "whois.nic.citic",
            "cm": "whois.netcom.cm",
            "coupon": "whois.nic.coupon",
            "crown": "whois.nic.crown",
            "crs": "whois.nic.crs",
            "deal": "whois.nic.deal",
            "dealer": "whois.nic.dealer",
            "dell": "whois.nic.dell",
            "dhl": "whois.nic.dhl",
            "discover": "whois.nic.discover",
            "dnp": "whois.nic.dnp",
            "duns": "whois.nic.duns",
            "dupont": "whois.nic.dupont",
            "earth": "whois.nic.earth",
            "energy": "whois.nic.energy",
            "epost": "whois.nic.epost",
            "everbank": "whois.nic.everbank",
            "farmers": "whois.nic.farmers",
            "fast": "whois.nic.fast",
            "ferrero": "whois.nic.ferrero",
            "fire": "whois.nic.fire",
            "fj": "whois.usp.ac.fj",
            "flickr": "whois.nic.flickr",
            "flir": "whois.nic.flir",
            "food": "whois.nic.food",
            "ford": "whois.nic.ford",
            "fox": "whois.nic.fox",
            "free": "whois.nic.free",
            "frontier": "whois.nic.frontier",
            "ftr": "whois.nic.ftr",
            "ga": "whois.my.ga",
            "gap": "whois.nic.gap",
            "gh": "whois.nic.gh",
            "gmo": "whois.nic.gmo",
            "got": "whois.nic.got",
            "grainger": "whois.nic.grainger",
            "grocery": "whois.nic.grocery",
            "guardian": "whois.nic.guardian",
            "gucci": "whois.nic.gucci",
            "hair": "whois.nic.hair",
            "hbo": "whois.nic.hbo",
            "health": "whois.nic.health",
            "homegoods": "whois.nic.homegoods",
            "homesense": "whois.nic.homesense",
            "honeywell": "whois.nic.honeywell",
            "hot": "whois.nic.hot",
            "hoteles": "whois.nic.hoteles",
            "hotels": "whois.nic.hotels",
            "hotmail": "whois.nic.hotmail",
            "hsbc": "whois.nic.hsbc",
            "hyatt": "whois.nic.hyatt",
            "ieee": "whois.nic.ieee",
            "imdb": "whois.nic.imdb",
            "int": "whois.iana.org",
            "intel": "whois.nic.intel",
            "intuit": "whois.nic.intuit",
            "ipirange": "whois.nic.ipiranga",
            "itau": "whois.nic.itau",
            "iwc": "whois.nic.iwc",
            "jetzt": "whois.nic.jetzt",
            "jlc": "whois.nic.jlc",
            "jmp": "whois.nic.jmp",
            "jnj": "whois.nic.jnj",
            "jot": "whois.nic.jot",
            "joy": "whois.nic.joy",
            "jpmorgan": "whois.nic.jpmorgan",
            "jprs": "whois.nic.jprs",
            "kinder": "whois.nic.kinder",
            "kindle": "whois.nic.kindle",
            "kpmg": "whois.nic.kpmg",
            "kpn": "whois.nic.kpn",
            "kred": "whois.nic.kred",
            "kw": "whois.nic.kw",
            "lanxess": "whois.nic.lanxess",
            "lc": "whois2.afilias-grs.net",
            "lifeinsurance": "whois.nic.lifeinsurance",
            "like": "whois.nic.like",
            "lilly": "whois.nic.lilly",
            "lincoln": "whois.nic.lincoln",
            "living": "whois.nic.living",
            "lk": "whois.nic.lk",
            "loft": "whois.nic.loft",
            "microsoft": "whois.nic.microsoft",
            "moi": "whois.nic.moi",
            "nagoya": "whois.nic.nagoya",
            "nyc": "whois.nic.nyc",
            "ps": "whois.pnina.ps",
            "ren": "whois.nic.ren",
            "rw": "whois.ricta.org.rw",
            "shaw": "whois.afilias-srs.net",
            "shop": "whois.nic.shop",
            "sl": "whois.nic.sl",
            "stream": "whois.nic.stream",
            "tokyo": "whois.nic.tokyo",
            "tvs": "whois.nic.tvs",
            "uno": "whois.nic.uno",
            "xn--e1a4c": "whois.eu",
            "xn--ses554g": "whois.registry.knet.cn",
            "za": "whois.registry.net.za",
        }

        # And we run the update logic.
        self.update()

    def _referer(self, extension):
        """
        Return the referer for the given extension.

        :param extension: A valid domain extension.
        :type extension: str

        :return: The whois server to use to get the WHOIS record.
        :rtype: str
        """

        # We get the a copy of the page.
        iana_record = Download(
            self.iana_url + "/" + extension + ".html", return_data=True
        ).text()

        if iana_record:
            # The record is not empty.

            # We initiate a regex which will extract the referer.
            regex_referer = r"(?s)\<b\>(?:WHOIS\sServer:)\<\/b>\s+([a-zA-Z0-9._-]+)"

            # We try to extract the referer.
            matched = Regex(
                iana_record, regex_referer, return_data=True, group=1
            ).match()

            if matched:
                # The referer was extracted successfully.

                # We return the matched referer.
                return matched

        # *The referer was not extracted successfully.
        # or
        # * The iana record is empty.

        if extension in self.manual_server:
            # The extension is in the list of manual entries.

            # We return the server which we set manually.
            return self.manual_server[extension]

        # We return None because we weren't able to get the server to call for
        # the given extension.
        return None

    def _extensions(self, block):
        """
        Extract the extention from the given block.
        Plus get its referer.

        :param block: The line from the IANA database.
        :type block: str
        """

        # We extract the different extension from the currently readed line.
        regex_valid_extension = r"(/domains/root/db/)(.*)(\.html)"

        if "/domains/root/db/" in block:
            # The link is in the line.

            # We try to extract the extension.
            matched = Regex(
                block, regex_valid_extension, return_data=True, rematch=True
            ).match()[1]

            if matched:
                # The extraction is not empty or None.

                # We get the referer.
                referer = self._referer(matched)

                if (
                    matched in self.iana_db and referer != self.iana_db[matched]
                ) or matched not in self.iana_db:
                    # * The referer is different from the previously set
                    # or
                    # * The extension is not already into the database.

                    # We update/set the referer.
                    self.iana_db[matched] = referer

                    # We save the content of the constructed database.
                    Dict(self.iana_db).to_json(self.destination)

    def update(self):
        """
        Update the content of the `iana-domains-db` file.
        """

        # We loop through the line of the iana website.
        list(
            map(
                self._extensions,
                Download(self.iana_url, return_data=True)
                .text()
                .split('<span class="domain tld">'),
            )
        )

        if not PyFunceble.CONFIGURATION["quiet"]:
            # The quiet mode is not activated.

            # We indicate that the work is done without any issue.
            print(PyFunceble.CONFIGURATION["done"])
