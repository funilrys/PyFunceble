# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of PyFunceble.converters.adblock

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
# pylint: enable=line-too-long
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.converter.adblock import AdBlock


class TestAdblockDecode(TestCase):
    """
    Tests of PyFunceble.converter.adblock
    """

    def setUp(self):
        """
        Setup everything needed for the test.
        """

        self.given = {
            '##[href^="https://funceble.funilrys.com/"]': ["funceble.funilrys.com"],
            '##div[href^="http://funilrys.com/"]': ["funilrys.com"],
            'com##[href^="ftp://funceble.funilrys-funceble.com/"]': [],
            "!@@||funceble.world/js": [],
            "!||world.hello/*ad.xml": [],
            "!funilrys.com##body": [],
            "[AdBlock Plus 2.0]": [],
            "@@||cnn.com/*ad.xml": [],
            "/banner/*/img^": [],
            "||ad.google.co.uk^": ["ad.google.co.uk"],
            "||ad.google.co.fr^$image,test": [],
            "||api.funilrys.com/widget/$": ["api.funilrys.com"],
            "||api.google.com/papi/action$popup": ["api.google.com"],
            "||funilrys.github.io$script,image": ["funilrys.github.io"],
            "||google.com^$script,image": ["google.com"],
            "||static.quantcast.mgr.consensu.org/*/cmpui-banner.js": [
                "static.quantcast.mgr.consensu.org"
            ],
            "$domain=memy.pl|pwn.pl|translatica.pl": [],
            "||twitter.com^helloworld.com": ["twitter.com"],
            "|github.io|": ["github.io"],
            "~github.com,hello.world##.wrapper": ["hello.world"],
            "bing.com,bingo.com#@##adBanner": ["bing.com", "bingo.com"],
            "facebook.com###player-above-2": ["facebook.com"],
            "hello#@#badads": [],
            "hubgit.com|oohay.com|ipa.elloh.dlorw#@#awesomeWorld": [
                "hubgit.com",
                "oohay.com",
            ],
            "yahoo.com,~msn.com,api.hello.world#@#awesomeWorld": [
                "api.hello.world",
                "yahoo.com",
            ],
            ".com": [],
            "||ggggggggggg.gq^$all": ["ggggggggggg.gq"],
            "||exaaaaaaample.org$document": ["exaaaaaaample.org"],
            "facebook.com##.search": ["facebook.com"],
            "||test.hello.world^$domain=hello.world": ["test.hello.world"],
            "||test.hwllo.world^$third-party": ["test.hwllo.world"],
            "||examplae.com": ["examplae.com"],
            "||examplbe.com^": ["examplbe.com"],
            "||examplce.com$third-party": ["examplce.com"],
            "||examplde.com^$third-party": ["examplde.com"],
            '##[href^="https://examplee.com/"]': ["examplee.com"],
            "||examplfe.com^examplge.com": ["examplfe.com"],
            "||examplhe.com$script,image": ["examplhe.com"],
            "||examplie.com^$domain=domain1.com|domain2.com": ["examplie.com"],
            "||examplje.com^$third-party,image": ["examplje.com"],
        }

        PyFunceble.load_config()

    def test_conversion_single_input(self):
        """
        Tests of the conversion of a single input.
        """

        for given, expected in self.given.items():
            actual = AdBlock(given).get_converted()

            self.assertEqual(expected, actual, f"Input: {given}")

    def test_conversion_multiple_input(self):
        """
        Tests of the conversion with multiple inputs.
        """

        expected = PyFunceble.helpers.List(
            [y for x in self.given.values() for y in x]
        ).format()
        actual = AdBlock(list(self.given.keys())).get_converted()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
