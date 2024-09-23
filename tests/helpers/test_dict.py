"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our dictionnary helper.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2021, 2021 Nissar Chababy

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

import copy
import os
import tempfile
import unittest

from PyFunceble.helpers.dict import DictHelper


class TestDictHelper(unittest.TestCase):
    """
    Provides the test of our dictionnary helper.
    """

    def setUp(self) -> None:
        """
        Setups everything needed for the tests.
        """

        self.test_subject = {
            "Hello": "world",
            "World": {"world": "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
        }

        self.helper = DictHelper()

    def tearDown(self) -> None:
        """
        Destroy everything needed by the tests.
        """

        del self.test_subject
        del self.helper

    def test_set_subject_return(self) -> None:
        """
        Tests the response from the method which let us set the subject to work
        with.
        """

        actual = self.helper.set_subject(self.test_subject)

        self.assertIsInstance(actual, DictHelper)

    def test_set_subject_method(self) -> None:
        """
        Tests the method which let us set the subject to work with.
        """

        given = self.test_subject
        expected = dict(self.test_subject)

        self.helper.set_subject(given)

        actual = self.helper.subject

        self.assertEqual(expected, actual)

    def test_set_subject_attribute(self) -> None:
        """
        Tests overwritting of the :code:`subject` attribute.
        """

        given = self.test_subject
        expected = dict(self.test_subject)

        self.helper.subject = given
        actual = self.helper.subject

        self.assertEqual(expected, actual)

    def test_set_subject_through_init(self) -> None:
        """
        Tests the overwritting of the subject to work through the class
        constructor.
        """

        given = self.test_subject
        expected = dict(self.test_subject)

        helper = DictHelper(given)
        actual = helper.subject

        self.assertEqual(expected, actual)

    def test_has_same_key_as(self) -> None:
        """
        Tests the method which let us know if the keys of 2 dicts are the same.
        """

        origin = {"a": 1, "b": 1}
        target = {"a": 1, "b": 2, "c": {"a": 1, "b": 3, "c": {"x": "x"}}}

        expected = True
        actual = self.helper.set_subject(target).has_same_keys_as(origin)

        self.assertEqual(expected, actual)

        expected = False
        actual = self.helper.set_subject(origin).has_same_keys_as(target)

        self.assertEqual(expected, actual)

        origin["c"] = {"a": 1, "b": 3, "c": {"x": "x"}}

        expected = True
        actual = self.helper.set_subject(target).has_same_keys_as(origin)

        self.assertEqual(expected, actual)

        actual = self.helper.set_subject(origin).has_same_keys_as(target)

        self.assertEqual(expected, actual)

        del origin["c"]["c"]

        expected = False
        actual = self.helper.set_subject(origin).has_same_keys_as(target)

        self.assertEqual(expected, actual)

    def test_remove_key_not_dict(self) -> None:
        """
        Tests the method which let us remove a key from a given dict for the
        case that the given subject is not a dict.
        """

        given = "Hello"

        expected = "Hello"
        actual = self.helper.set_subject(given).remove_key("Py")

        self.assertEqual(expected, actual)

    def test_remove_key(self) -> None:
        """
        Test the method which let us remove a key from a given dict.
        """

        given = copy.deepcopy(self.test_subject)

        expected = {
            "Hello": "world",
            "World": {"world": "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "pyfunceble": ["funilrys"],
        }
        actual = self.helper.set_subject(given).remove_key("Py")

        self.assertEqual(expected, actual)

        actual = self.helper.set_subject(given).remove_key(["Py", "test"])

        self.assertEqual(expected, actual)

    def test_remove_multiple_key(self) -> None:
        """
        Tests the method which let us remove a key with multiple key to
        remove.
        """

        given = copy.deepcopy(self.test_subject)

        expected = {
            "Hello": "world",
            "World": {"world": "hello"},
            "pyfunceble": ["funilrys"],
        }
        actual = self.helper.set_subject(given).remove_key(["funilrys", "Py"])

        self.assertEqual(expected, actual)

    def test_remove_key_not_exists(self) -> None:
        """
        Tests the method which let us remove a key for the cas that the key to
        remove does not exists.
        """

        given = copy.deepcopy(self.test_subject)

        expected = copy.deepcopy(self.test_subject)
        actual = self.helper.set_subject(given).remove_key("xxx.")

        self.assertEqual(expected, actual)

    def test_rename_key_not_dict(self) -> None:
        """
        Tests the method which let us rename a key of a dict for the case that
        the given subject is not a dict.
        """

        given = "Hello, World!"

        expected = "Hello, World!"
        actual = self.helper.set_subject(given).rename_key({"Py": "PyFunceble"})

        self.assertEqual(expected, actual)

    def test_rename_key_strict_single(self) -> None:
        """
        Tests the method which let us rename a key for the case that we only
        want to strictly rename one key.
        """

        given = copy.deepcopy(self.test_subject)

        expected = {
            "Hello": "world",
            "World": {"world": "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "PyFunceble": "Funceble",
            "pyfunceble": ["funilrys"],
        }
        actual = self.helper.set_subject(given).rename_key(
            {"Py": "PyFunceble"}, strict=True
        )

        self.assertEqual(expected, actual)

    def test_rename_key_not_strict_single(self) -> None:
        """
        Tests the method which let us rename a key for the case that we only
        want to rename all occurrences of the given key.
        """

        given = copy.deepcopy(self.test_subject)

        expected = {
            "Hello": "world",
            "World": {"world": "hello"},
            "nuilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "nuceble": ["funilrys"],
        }
        actual = self.helper.set_subject(given).rename_key({"fun": "nuf"}, strict=False)

        self.assertEqual(expected, actual)

    def test_to_and_from_json_file(self) -> None:
        """
        Tests the method which let us save and load a dict into/from a JSON
        file.
        """

        output_file = tempfile.NamedTemporaryFile("w", delete=False)

        given = copy.deepcopy(self.test_subject)
        expected = copy.deepcopy(self.test_subject)

        self.helper.set_subject(given).to_json_file(output_file.name)

        output_file.seek(0)

        actual = self.helper.from_json_file(output_file.name)

        self.assertEqual(expected, actual)

        output_file.close()

        os.remove(output_file.name)

    def test_from_json_file_not_json(self) -> None:
        """
        Tests the method which let us load a JSON file for the case that no
        JSON file is given.
        """

        output_file = tempfile.NamedTemporaryFile("wb", delete=False)
        output_file.write(b"Hello, World!")

        output_file.seek(0)

        expected = dict()  # pylint: disable=use-dict-literal
        actual = self.helper.from_json_file(output_file.name)

        self.assertEqual(expected, actual)

        output_file.close()

        os.remove(output_file.name)

    def test_to_json(self) -> None:
        """
        Tests the method which let us convert a dict to a JSON and vice-versa.
        """

        given = copy.deepcopy(self.test_subject)
        expected = """{
    "Hello": "world",
    "Py": "Funceble",
    "World": {
        "world": "hello"
    },
    "funilrys": [
        "Fun",
        "Ilrys"
    ],
    "pyfunceble": [
        "funilrys"
    ]
}"""

        actual = self.helper.set_subject(given).to_json()

        self.assertIsInstance(actual, str)
        self.assertEqual(expected, actual)

        actual = self.helper.from_json(expected)
        expected = copy.deepcopy(self.test_subject)

        self.assertEqual(expected, actual)

    def test_from_json_not_json(self) -> None:
        """
        Tests the method which let us convert a JSON to a JSON for the case
        that no JSON is given.
        """

        given = "Hello, World!"

        expected = dict()  # pylint: disable=use-dict-literal
        actual = self.helper.from_json(given)

        self.assertEqual(expected, actual)

    def test_from_yaml_file(self) -> None:
        """
        Tests the method which let us save and load a dict into/from a YAML file.
        """

        output_file = tempfile.NamedTemporaryFile("w", delete=False)

        given = copy.deepcopy(self.test_subject)

        expected = copy.deepcopy(self.test_subject)

        self.helper.set_subject(given).to_yaml_file(output_file.name)

        output_file.seek(0)

        actual = self.helper.from_yaml_file(output_file.name)

        self.assertEqual(expected, actual)

        output_file.close()

        os.remove(output_file.name)

    def test_to_yaml(self) -> None:
        """
        Tests the method which let us convert a dict into a YAML and vice-versa.
        """

        expected = """Hello: world
Py: Funceble
World:
    world: hello
funilrys:
- Fun
- Ilrys
pyfunceble:
- funilrys
"""

        given = copy.deepcopy(self.test_subject)
        actual = self.helper.set_subject(given).to_yaml()

        self.assertEqual(expected, actual)

        actual = self.helper.from_yaml(expected)
        expected = copy.deepcopy(self.test_subject)

        self.assertEqual(expected, actual)

    def test_flatten(self) -> None:
        """
        Tests the method which let us flatten a dict.
        """

        expected = {
            "Hello": "world",
            "World.world": "hello",
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
        }

        actual = self.helper.set_subject(self.test_subject).flatten()

        self.assertEqual(expected, actual)

    def test_deeper_flatten(self) -> None:
        """
        Tests the method which let us flatten a dict with more level.
        """

        given = {
            "Hello": "world",
            "World": {"world": "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
            "this": {
                "is": {
                    "a": {
                        "test": {
                            "id": 1,
                            "deep": {"hello": {"world": ["Hello!"]}},
                            "response": "World",
                        }
                    },
                    "b": 1,
                    "c": [{"hello": {"this": {"is": "a test"}}}],
                }
            },
            "": {"hello-fun": "world", "": "hehe"},
        }

        expected = {
            "Hello": "world",
            "World.world": "hello",
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
            "this.is.a.test.deep.hello.world": ["Hello!"],
            "this.is.a.test.id": 1,
            "this.is.a.test.response": "World",
            "this.is.b": 1,
            "this.is.c": [{"hello": {"this": {"is": "a test"}}}],
            "..": "hehe",
            ".hello-fun": "world",
        }

        actual = self.helper.set_subject(given).flatten()

        self.assertEqual(expected, actual)

    def test_unflatten(self) -> None:
        """
        Tests the method which let us unflatten a dict.
        """

        given = {
            "Hello": "world",
            "World.world": "hello",
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
        }

        expected = dict(self.test_subject)

        actual = self.helper.set_subject(given).unflatten()

        self.assertEqual(expected, actual)

    def test_deeper_unflatten(self) -> None:
        """
        Tests the method which let us unflatten a dict with more level.
        """

        given = {
            "Hello": "world",
            "World.world": "hello",
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
            "this.is.a.test.deep.hello.world": ["Hello!"],
            "this.is.a.test.id": 1,
            "this.is.a.test.response": "World",
            "this.is.b": 1,
            "this.is.c": [{"hello": {"this": {"is": "a test"}}}],
            "..": "hehe",
            ".hello-fun": "world",
        }

        expected = {
            "Hello": "world",
            "World": {"world": "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
            "this": {
                "is": {
                    "a": {
                        "test": {
                            "id": 1,
                            "deep": {"hello": {"world": ["Hello!"]}},
                            "response": "World",
                        }
                    },
                    "b": 1,
                    "c": [{"hello": {"this": {"is": "a test"}}}],
                }
            },
            "": {"hello-fun": "world", "": "hehe"},
        }

        actual = self.helper.set_subject(given).unflatten()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
