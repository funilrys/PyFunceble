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


    Copyright 2017, 2018, 2019, 2020, 2022, 2023 Nissar Chababy

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
from typing import List

from PyFunceble.converter.adblock_input_line2subject import AdblockInputLine2Subject


class TestAdblockInputLine2Subject(unittest.TestCase):
    """
    Tests our adblock 2 subject converter.
    """

    EXTENDED_TEST_SUBJECT: List[dict] = [
        {
            "subject": '##[href^="https://funceble.funilrys.com/"]',
            "expected": {
                "aggressive": ["funceble.funilrys.com"],
                "standard": [],
            },
        },
        {
            "subject": "||test.hello.world^$domain=hello.world",
            "expected": {
                "aggressive": ["hello.world", "test.hello.world"],
                "standard": ["test.hello.world"],
            },
        },
        {
            "subject": '##div[href^="http://funilrys.com/"]',
            "expected": {"aggressive": ["funilrys.com"], "standard": []},
        },
        {
            "subject": 'com##[href^="ftp://funceble.funilrys-funceble.com/"]',
            "expected": {
                "aggressive": ["funceble.funilrys-funceble.com"],
                "standard": [],
            },
        },
        {
            "subject": "!@@||funceble.world/js",
            "expected": {"aggressive": [], "standard": []},
        },
        {
            "subject": "!||world.hello/*ad.xml",
            "expected": {"aggressive": [], "standard": []},
        },
        {
            "subject": "!funilrys.com##body",
            "expected": {"aggressive": [], "standard": []},
        },
        {
            "subject": "[AdBlock Plus 2.0]",
            "expected": {"aggressive": [], "standard": []},
        },
        {
            "subject": "@@||ads.example.com/notbanner^$~script",
            "expected": {"aggressive": ["ads.example.com"], "standard": []},
        },
        {"subject": "/banner/*/img^", "expected": {"aggressive": [], "standard": []}},
        {
            "subject": "||ad.example.co.uk^",
            "expected": {
                "aggressive": ["ad.example.co.uk"],
                "standard": ["ad.example.co.uk"],
            },
        },
        {
            "subject": "||ad.example.fr^$image,test",
            "expected": {
                "aggressive": ["ad.example.fr"],
                "standard": ["ad.example.fr"],
            },
        },
        {
            "subject": "||api.funilrys.com/widget/$",
            "expected": {
                "aggressive": ["api.funilrys.com"],
                "standard": ["api.funilrys.com"],
            },
        },
        {
            "subject": "||api.example.com/papi/action$popup",
            "expected": {
                "aggressive": ["api.example.com"],
                "standard": ["api.example.com"],
            },
        },
        {
            "subject": "||funilrys.github.io$script,image",
            "expected": {
                "aggressive": ["funilrys.github.io"],
                "standard": ["funilrys.github.io"],
            },
        },
        {
            "subject": "||example.net^$script,image",
            "expected": {"aggressive": ["example.net"], "standard": ["example.net"]},
        },
        {
            "subject": "||static.hello.world.examoke.org/*/exit-banner.js",
            "expected": {
                "aggressive": ["static.hello.world.examoke.org"],
                "standard": ["static.hello.world.examoke.org"],
            },
        },
        {
            "subject": "$domain=exam.pl|elpmaxe.pl|example.pl",
            "expected": {
                "aggressive": ["elpmaxe.pl", "exam.pl", "example.pl"],
                "standard": [],
            },
        },
        {
            "subject": "||example.de^helloworld.com",
            "expected": {
                "aggressive": ["example.de"],
                "standard": ["example.de"],
            },
        },
        {
            "subject": "|github.io|",
            "expected": {"aggressive": ["github.io"], "standard": ["github.io"]},
        },
        {
            "subject": "~github.com,hello.world##.wrapper",
            "expected": {"aggressive": ["github.com", "hello.world"], "standard": []},
        },
        {
            "subject": "bing.com,bingo.com#@##adBanner",
            "expected": {"aggressive": ["bing.com", "bingo.com"], "standard": []},
        },
        {
            "subject": "example.org#@##test",
            "expected": {"aggressive": ["example.org"], "standard": []},
        },
        {
            "subject": "hubgit.com|oohay.com|ipa.elloh.dlorw#@#awesomeWorld",
            "expected": {
                "aggressive": ["hubgit.com|oohay.com|ipa.elloh.dlorw"],
                "standard": [],
            },
        },
        {"subject": ".com", "expected": {"aggressive": [], "standard": []}},
        {
            "subject": "||ggggggggggg.gq^$all",
            "expected": {
                "aggressive": ["ggggggggggg.gq"],
                "standard": ["ggggggggggg.gq"],
            },
        },
        {
            "subject": "facebook.com##.search",
            "expected": {"aggressive": ["facebook.com"], "standard": []},
        },
        {
            "subject": "||test.hello.world^$domain=hello.world",
            "expected": {
                "aggressive": ["hello.world", "test.hello.world"],
                "standard": ["test.hello.world"],
            },
        },
        {
            "subject": "||examplae.com",
            "expected": {"aggressive": ["examplae.com"], "standard": ["examplae.com"]},
        },
        {
            "subject": "||examplbe.com^",
            "expected": {"aggressive": ["examplbe.com"], "standard": ["examplbe.com"]},
        },
        {
            "subject": "||examplce.com$third-party",
            "expected": {"aggressive": ["examplce.com"], "standard": ["examplce.com"]},
        },
        {
            "subject": "||examplde.com^$third-party",
            "expected": {"aggressive": ["examplde.com"], "standard": ["examplde.com"]},
        },
        {
            "subject": '##[href^="https://examplee.com/"]',
            "expected": {"aggressive": ["examplee.com"], "standard": []},
        },
        {
            "subject": "||examplfe.com^examplge.com",
            "expected": {"aggressive": ["examplfe.com"], "standard": ["examplfe.com"]},
        },
        {
            "subject": "||examplhe.com$script,image",
            "expected": {"aggressive": ["examplhe.com"], "standard": ["examplhe.com"]},
        },
        {
            "subject": "||examplie.com^$domain=domain1.com|domain2.com",
            "expected": {
                "aggressive": [
                    "domain1.com",
                    "domain2.com",
                    "examplie.com",
                ],
                "standard": ["examplie.com"],
            },
        },
        {
            "subject": 'examlple.com##[href^="http://hello.world."], '
            '[href^="http://example.net/"]',
            "expected": {
                "aggressive": ["examlple.com", "example.net", "hello.world."],
                "standard": [],
            },
        },
        {"subject": "##.ad-href1", "expected": {"aggressive": [], "standard": []}},
        {
            "subject": "^hello^$domain=example.com",
            "expected": {"standard": [], "aggressive": ["example.com"]},
        },
        {
            "subject": "hello$domain=example.net|example.com",
            "expected": {"standard": [], "aggressive": ["example.com", "example.net"]},
        },
        {
            "subject": "hello^$domain=example.org|example.com|example.net",
            "expected": {
                "standard": [],
                "aggressive": ["example.com", "example.net", "example.org"],
            },
        },
    ]

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

        for test_dataset in self.EXTENDED_TEST_SUBJECT:
            given = test_dataset["subject"]
            expected_std = test_dataset["expected"]["standard"]
            expected_aggressive = test_dataset["expected"]["aggressive"]

            self.converter.data_to_convert = given

            self.converter.aggressive = True
            actual = self.converter.get_converted()

            self.assertEqual(
                expected_aggressive,
                actual,
                f"Aggressive: {self.converter.aggressive} | {given}",
            )

            self.converter.aggressive = False
            actual = self.converter.get_converted()

            self.assertEqual(
                expected_std,
                actual,
                f"Aggressive: {self.converter.aggressive} | {given}",
            )

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
