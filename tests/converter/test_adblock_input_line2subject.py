"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our adblock 2 subject converter.

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

import unittest

from PyFunceble.converter.adblock_input_line2subject import AdblockInputLine2Subject


class TestAdblockInputLine2Subject(unittest.TestCase):
    """
    Tests our adblock 2 subject converter.
    """

    TEST_SUBJECT: dict = {
        '##[href^="https://funceble.funilrys.com/"]': ["funceble.funilrys.com"],
        '##div[href^="http://funilrys.com/"]': ["funilrys.com"],
        'com##[href^="ftp://funceble.funilrys-funceble.com/"]': [
            "funceble.funilrys-funceble.com"
        ],
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

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.converter = AdblockInputLine2Subject()

    def tearDown(self) -> None:
        """
        Destroys everything previously created for the tests.
        """

        del self.converter

    def test_set_data_to_convert_no_string(self) -> None:
        """
        Tests the method which let us set the data to work with for the case
        that a non-string value is given.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.converter.set_data_to_convert(given))

    def test_set_aggressive_return(self) -> None:
        """
        Tests the response from the method which let us activate the
        aggressive mode.
        """

        given = True

        actual = self.converter.set_aggressive(given)

        self.assertIsInstance(actual, AdblockInputLine2Subject)

    def test_set_aggressive_method(self) -> None:
        """
        Tests the method which let us set activate the aggressive mode.
        """

        given = True
        expected = True

        self.converter.set_aggressive(given)

        actual = self.converter.aggressive

        self.assertEqual(expected, actual)

    def test_set_aggressive_attribute(self) -> None:
        """
        Tests overwritting of the :code:`aggressive` attribute.
        """

        given = True
        expected = True

        self.converter.aggressive = given
        actual = self.converter.aggressive

        self.assertEqual(expected, actual)

    def test_set_aggressive_through_init(self) -> None:
        """
        Tests the activation of the aggressive mode through the class constructor.
        """

        given = True
        expected = True

        converter = AdblockInputLine2Subject(aggressive=given)
        actual = converter.aggressive

        self.assertEqual(expected, actual)

    def test_set_aggressive_not_bool(self) -> None:
        """
        Tests the response from the method which let us set the activate
        the aggressive mode for the case that the given value is not a bool.
        """

        given = ["Hello", "World"]

        self.assertRaises(TypeError, lambda: self.converter.set_aggressive(given))

    def test_get_converted(self) -> None:
        """
        Tests the method which let us get the converted data.
        """

        for given, expected in self.TEST_SUBJECT.items():
            self.converter.data_to_convert = given
            actual = self.converter.get_converted()

            self.assertEqual(expected, actual, given)

    def test_get_converted_aggressive(self) -> None:
        """
        Tests the method which let us get the converted data for the case that
        the aggressive mode is activated.
        """

        self.converter.aggressive = True

        given = "||test.hello.world^$domain=hello.world"
        expected = ["hello.world", "test.hello.world"]

        self.converter.data_to_convert = given
        actual = self.converter.get_converted()

        self.assertEqual(expected, actual)

    def test_extract_base(self) -> None:
        """
        Tests the method which let us get the base fo a given URL (or dataset.)
        """

        test_map = {
            "example.org": "example.org/?is=beautiful",
            "example.de": "://example.de/",
            "example.net": "example.net",
        }

        for expected, given in test_map.items():
            actual = self.converter.extract_base(given)

            self.assertEqual(expected, actual)

        expected = ""
        given = ""
        actual = self.converter.extract_base(given)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
