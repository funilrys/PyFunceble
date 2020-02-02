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
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

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
