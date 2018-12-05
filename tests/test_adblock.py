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

This submodule will test PyFunceble.adblock.

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
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.adblock import AdBlock


class TestAdblockDecode(TestCase):
    """
    Test if the adblock decoder works.
    """

    def setUp(self):
        """
        Setup everything needed for the test.
        """

        PyFunceble.load_config(True)
        self.lines = [
            '##[href^="https://funceble.funilrys.com/"]',
            '##div[href^="http://funilrys.com/"]',
            'com##[href^="ftp://funceble.funilrys-funceble.com/"]',
            "!@@||funceble.world/js",
            "!||world.hello/*ad.xml",
            "!funilrys.com##body",
            "[AdBlock Plus 2.0]",
            "@@||cnn.com/*ad.xml",
            "/banner/*/img^",
            "||ad.google.co.uk^",
            "||ad.google.co.fr^$image,test",
            "||api.funilrys.com/widget/$",
            "||api.google.com/papi/action$popup",
            "||funilrys.github.io$script,image",
            "||google.com^$script,image",
            "||static.quantcast.mgr.consensu.org/*/cmpui-banner.js"
            "$domain=memy.pl|pwn.pl|translatica.pl",
            "||twitter.com^helloworld.com",
            "|github.io|",
            "~github.com,hello.world##.wrapper",
            "bing.com,bingo.com#@##adBanner",
            "facebook.com###player-above-2",
            "hello#@#badads",
            "hubgit.com|oohay.com|ipa.elloh.dlorw#@#awesomeWorld",
            "yahoo.com,~msn.com,api.hello.world#@#awesomeWorld",
            ".com",
        ]

        self.expected = [
            "ad.google.co.uk",
            "api.funilrys.com",
            "api.google.com",
            "funceble.funilrys.com",
            "funilrys.com",
            "funilrys.github.io",
            "github.io",
            "google.com",
            "static.quantcast.mgr.consensu.org",
            "twitter.com",
        ]

    def test_adblock_decode(self):
        """
        Test that the adblock decoding system is working proprely
        """

        actual = AdBlock(self.lines).decode()
        self.assertEqual(self.expected, actual)


if __name__ == "__main__":
    launch_tests()
