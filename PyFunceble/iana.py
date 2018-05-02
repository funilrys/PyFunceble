#!/usr/bin/env python3

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the IANA logic and interface.


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on March 13th, 2018.
At the end of 2017, PyFunceble was described by one of its most active user as:
"[an] excellent script for checking ACTIVE and INACTIVE domain names."

Our main objective is to test domains and IP availability
by generating an accurate result based on results from WHOIS, NSLOOKUP and
HTTP status codes.
As result, PyFunceble returns 3 status: ACTIVE, INACTIVE and INVALID.
The denomination of those statuses can be changed under your personal
`config.yaml`.

At the time we write this, PyFunceble is running actively and daily under 50+
Travis CI repository or process to test the availability of domains which are
present into hosts files, AdBlock filter lists, list of IP, list of domains or
blocklists.

An up to date explanation of all status can be found at https://git.io/vxieo.
You can also find a simple representation of the logic behind PyFunceble at
https://git.io/vxifw.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
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
import PyFunceble
from PyFunceble.helpers import Dict, Download, Regex
from PyFunceble.lookup import Lookup


class IANA(object):
    """
    Logic behind the update of `iana-domains-db.json`
    """

    def __init__(self):
        if not PyFunceble.CONFIGURATION["quiet"]:
            print("Update of iana-domains-db", end=" ")

        self.destination = PyFunceble.OUTPUTS["default_files"]["iana"]
        self.iana_db = {}

        self.update()

    @classmethod
    def data(cls):
        """
        Get the database from IANA website.
        """
        iana_url = "https://www.iana.org/domains/root/db"

        return Download(iana_url, return_data=True).text()

    @classmethod
    def referer(cls, extension):
        """
        Return the referer for the given extension.

        :pram extension: A string, a valid domain extension.
        """

        manual_server = {
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
            "bz": "whois.afilias-grs.net",
            "buzz": "whois.nic.buzz",
            "call": "whois.nic.call",
            "calvinklein": "whois.nic.calvinklein",
            "caravan": "whois.nic.caravan",
            "cartier": "whois.nic.cartier",
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
            "hoteles": "whois.nic.hoteles",
            "hotels": "whois.nic.hotels",
            "hotmail": "whois.nic.hotmail",
            "hyatt": "whois.nic.hyatt",
            "hsbc": "whois.nic.hsbc",
            "hot": "whois.nic.hot",
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
            "lifeinsurance": "whois.nic.lifeinsurance",
            "like": "whois.nic.like",
            "lc": "whois2.afilias-grs.net",
            "lk": "whois.nic.lk",
            "microsoft": "whois.nic.microsoft",
            "nagoya": "whois.nic.nagoya",
            "nyc": "whois.nic.nyc",
            "ps": "whois.pnina.ps",
            "ren": "whois.nic.ren",
            "rw": "whois.ricta.org.rw",
            "shop": "whois.nic.shop",
            "sl": "whois.nic.sl",
            "stream": "whois.nic.stream",
            "tokyo": "whois.nic.tokyo",
            "uno": "whois.nic.uno",
            "za": "whois.registry.net.za",
        }

        if extension in manual_server:
            return manual_server[extension]

        else:
            whois_record = Lookup().whois(
                PyFunceble.CONFIGURATION["iana_whois_server"], "hello." + extension, 10
            )

            if whois_record:
                regex_referer = r"(refer:)\s+(.*)"

                matched = Regex(
                    whois_record, regex_referer, return_data=True, rematch=True
                ).match()

                if matched:
                    return matched[1]

            return None

    def _extensions(self, line):
        """
        Extract the extention from the given line.
        Plus get its referer.

        Argument:
            - line: str
                The line from self.iana_url.
        """

        regex_valid_extension = r"(/domains/root/db/)(.*)(\.html)"

        if "/domains/root/db/" in line:
            matched = Regex(
                line, regex_valid_extension, return_data=True, rematch=True
            ).match()[
                1
            ]

            if matched:
                self.iana_db.update({matched: self.referer(matched)})

    def update(self):
        """
        Update the content of the `iana-domains-db` file.
        """

        list(map(self._extensions, self.data().split("\n")))
        Dict(self.iana_db).to_json(self.destination)

        if not PyFunceble.CONFIGURATION["quiet"]:
            print(PyFunceble.CONFIGURATION["done"])
