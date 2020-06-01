"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the IANA database generation tool.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

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


from multiprocessing import Pool

import PyFunceble


class Iana:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Logic behind the update and usage of `iana-domains-db.json`
    """

    # We map the list of server which have to be set manually because
    # they are not present into the IANA Root Zone Database.
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
        "doosan": "whois.nic.doosan",
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
        "htc": "whois.nic.htc",
        "hyatt": "whois.nic.hyatt",
        "ieee": "whois.nic.ieee",
        "iinet": "whois.nic.iinet",
        "imdb": "whois.nic.imdb",
        "int": "whois.iana.org",
        "intel": "whois.nic.intel",
        "intuit": "whois.nic.intuit",
        "ipiranga": " whois.nic.ipiranga",
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
        "lupin": "whois.nic.lupin",
        "maif": "whois.nic.maif",
        "marshalls": "whois.nic.marshalls",
        "mattel": "whois.nic.mattel",
        "mcd": "whois.nic.mcd",
        "mcdonalds": "whois.nic.mcdonalds",
        "merckmsd": "whois.nic.merckmsd",
        "microsoft": "whois.nic.microsoft",
        "mint": "whois.nic.mint",
        "mlb": "whois.nic.mlb",
        "mobily": "whois.nic.mobily",
        "moi": "whois.nic.moi",
        "montblanc": "whois.nic.montblanc",
        "moto": "whois.nic.moto",
        "msd": "whois.nic.msd",
        "mtpc": "whois.nic.mtpc",
        "mutual": "whois.nic.mutual",
        "mutuelle": "whois.nic.mutuelle",
        "nagoya": "whois.nic.nagoya",
        "nba": "whois.nic.nba",
        "netflix": "whois.nic.netflix",
        "neustar": "whois.nic.neustar",
        "nfl": "whois.nic.nfl",
        "nhk": "whois.nic.nhk",
        "nike": "whois.nic.nike",
        "northwesternmutual": "whois.nic.northwesternmutual",
        "now": " whois.nic.now",
        "ntt": "whois.nic.ntt",
        "nyc": "whois.nic.nyc",
        "office": "whois.nic.office",
        "okinawa": "whois.nic.okinawa",
        "oldnavy": "whois.nic.oldnavy",
        "open": "whois.nic.open",
        "orientexpress": "whois.nic.orientexpress",
        "otsuka": "whois.nic.otsuka",
        "passagens": "whois.nic.passagens",
        "pay": "whois.nic.pay",
        "pfizer": "whois.nic.pfizer",
        "pharmacy": " whois.nic.pharmacy",
        "piaget": " whois.nic.piaget",
        "pictet": "whois.nic.pictet",
        "pin": "whois.nic.pin",
        "ping": "whois.nic.ping",
        "pramerica": "whois.nic.pramerica",
        "praxi": "whois.nic.praxi",
        "prime": "whois.nic.prime",
        "pru": "whois.nic.pru",
        "prudential": "whois.nic.prudential",
        "ps": "whois.pnina.ps",
        "qvc": "whois.nic.qvc",
        "read": "whois.nic.read",
        "realtor": "whois.nic.realtor",
        "ren": "whois.nic.ren",
        "rocher": "whois.nic.rocher",
        "room": "whois.nic.room",
        "rw": "whois.ricta.org.rw",
        "ryukyu": "whois.nic.ryukyu",
        "safe": "whois.nic.safe",
        "safety": "whois.nic.safety",
        "sakura": "whois.nic.sakura",
        "sapo": "whois.nic.sapo",
        "sas": "whois.nic.sas",
        "save": "whois.nic.save",
        "secure": "whois.nic.secure",
        "sener": "whois.nic.sener",
        "shaw": "whois.afilias-srs.net",
        "shop": "whois.nic.shop",
        "silk": "whois.nic.silk",
        "skype": "whois.nic.skype",
        "sl": "whois.nic.sl",
        "smile": "whois.nic.smile",
        "sohu": "whois.nic.sohu",
        "song": "whois.nic.song",
        "spot": "whois.nic.spot",
        "staples": "whois.nic.staples",
        "statefarm": "whois.nic.statefarm",
        "stream": "whois.nic.stream",
        "suzuki": "whois.nic.suzuki",
        "swiftcover": "whois.nic.swiftcover",
        "talk": "whois.nic.talk",
        "taobao": "whois.nic.taobao",
        "target": "whois.nic.target",
        "tjmaxx": "whois.nic.tjmaxx",
        "tjx": "whois.nic.tjx",
        "tkmaxx": "whois.nic.tkmaxx",
        "tmall": "whois.nic.tmall",
        "tokyo": "whois.nic.tokyo",
        "tube": "whois.nic.tube",
        "tunes": "whois.nic.tunes",
        "tushu": "whois.nic.tushu",
        "tvs": "whois.nic.tvs",
        "unicom": "whois.nic.unicom",
        "uno": "whois.nic.uno",
        "vivo": "whois.nic.vivo",
        "vuelos": "whois.nic.vuelos",
        "wanggou": "whois.nic.wanggou",
        "watches": "whois.nic.watches",
        "weather": "whois.nic.weather",
        "weatherchannel": "whois.nic.weatherchannel",
        "weir": "whois.nic.weir",
        "whois": "whois.nic.qpon",
        "windows": "whois.nic.windows",
        "winners": "whois.nic.winners",
        "wow": "whois.nic.wow",
        "xbox": "whois.nic.xbox",
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
        "yahoo": "whois.nic.yahoo",
        "yamaxun": "whois.nic.yamaxun",
        "yandex": "whois.nic.yandex",
        "yokohama": "whois.nic.yokohama",
        "you": "whois.nic.you",
        "za": "whois.registry.net.za",
        "zappos": "whois.nic.zappos",
        "zero": "whois.nic.zero",
        "zippo": "whois.nic.zippo",
    }

    def __init__(self):
        # We get the destination of the constructed IANA database.
        self.destination = (
            PyFunceble.CONFIG_DIRECTORY + PyFunceble.OUTPUTS.default_files.iana
        )

        if PyFunceble.helpers.File(self.destination).exists():
            # The destination exist.

            # We get its content.
            self.database = PyFunceble.helpers.Dict().from_json_file(self.destination)
        else:
            # The destination does not exist.

            # We initiate the local variable which will save the content of the database.
            self.database = {}

        # We initiate the URL to the IANA Root Zone Database page.
        self.iana_url = "https://www.iana.org/domains/root/db"

    def load(self):
        """
        Initiate the IANA database if it is not the case.
        """

        if "database" not in PyFunceble.INTERN or not PyFunceble.INTERN["database"]:
            # The global database is empty, None or does not exist.

            # We update it with the database content.
            PyFunceble.INTERN.update({"database": self.database.copy()})

    @classmethod
    def _get_referer(cls, extension):
        """
        Return the referer for the given extension.

        :param str extension: A valid domain extension.

        :return: The whois server to use to get the WHOIS record.
        :rtype: str
        """

        PyFunceble.LOGGER.info(f"Trying to find the referer of {repr(extension)}.")

        # We get the  whois record related to the domain extension we are currently
        # working with.
        iana_record = PyFunceble.lookup.Whois(
            "hello.{}".format(extension), PyFunceble.CONFIGURATION.iana_whois_server
        ).request()

        if iana_record and "refer" in iana_record:
            # The record is not empty.

            PyFunceble.LOGGER.info("Referer probably present. Trying to extract it.")

            # We initiate a regex which will extract the referer.
            regex_referer = r"(?s)refer\:\s+([a-zA-Z0-9._-]+)\n"

            # We try to extract the referer.
            matched = PyFunceble.helpers.Regex(regex_referer).match(
                iana_record, return_match=True, group=1
            )

            PyFunceble.LOGGER.debug(f"Extracted: {repr(matched)}")

            if matched:
                # The referer was extracted successfully.

                # We return the matched referer.
                return matched

        PyFunceble.LOGGER.info(
            "Could not extract nor find the referer from record. "
            "Trying to find it into our local entries."
        )

        # * The referer was not extracted successfully.
        # or
        # * The iana record is empty.

        if extension in cls.manual_server:
            # The extension is in the list of manual entries.

            PyFunceble.LOGGER.debug(
                f"Found local entry for {repr(extension)}: "
                f"{repr(cls.manual_server[extension])}"
            )

            # We return the server which we set manually.
            return cls.manual_server[extension]

        # We return None because we weren't able to get the server to call for
        # the given extension.
        return None

    @classmethod
    def _check_referer(cls, extension, referer):
        """
        Check if the given referer is reachable

        :param str extension: The extension the referer refers to.
        :param str referer: The referer to check.

        :rtype: bool
        """

        return (
            PyFunceble.lookup.Whois(
                "hello.{0}".format(extension), server=referer
            ).request()
            is not None
        )

    @classmethod
    def _get_extension_and_referer_from_block(cls, block):
        """
        Extract the extention from the given HTML block.
        Plus get its referer.

        :param str block: An HTML block.
        """

        # We extract the different extension from the currently readed line.
        regex_valid_extension = r"(/domains/root/db/)(.*)(\.html)"

        if "/domains/root/db/" in block:
            # The link is in the line.

            # We try to extract the extension.
            matched = PyFunceble.helpers.Regex(regex_valid_extension).match(
                block, return_match=True, rematch=True
            )[1]

            if matched:
                # The extraction is not empty or None.

                # We get the referer.
                referer = cls._get_referer(matched)

                if not referer:
                    referer = "whois.nic.{0}".format(matched)

                if cls._check_referer(matched, referer):
                    return matched, referer, True

                return matched, referer, False

        return None, None, None

    def update(self):
        """
        Update the content of `iana-domains-db.json` file.
        """

        if not PyFunceble.CONFIGURATION.quiet:
            # The quiet mode is not activated.

            # We print on screen what we are doing.
            print(
                "Update of {0}".format(PyFunceble.OUTPUTS.default_files.iana), end=" "
            )

        upstream_lines = (
            PyFunceble.helpers.Download(self.iana_url)
            .text()
            .split('<span class="domain tld">')
        )

        with Pool(PyFunceble.CONFIGURATION.maximal_processes) as pool:
            already_checked = []
            for extension, referer, referer_checked in pool.map(
                self._get_extension_and_referer_from_block, upstream_lines
            ):
                if (extension is not None and referer) and (
                    referer_checked or referer in already_checked
                ):
                    if (
                        extension not in self.database
                        or self.database[extension] != referer
                    ):
                        # We add the extension to the databae.
                        self.database[extension] = referer

                already_checked.append(referer)

        # We save the content of the constructed database.
        PyFunceble.helpers.Dict(self.database).to_json_file(self.destination)

        if not PyFunceble.CONFIGURATION.quiet:
            # The quiet mode is not activated.

            # We indicate that the work is done without any issue.
            print(PyFunceble.INTERN["done"] + "\n")
