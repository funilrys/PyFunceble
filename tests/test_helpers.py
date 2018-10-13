# pylint:disable=line-too-long
"""
The tool to check the availability of domains, IPv4 or URL.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

This submodule will test PyFunceble.helpers.

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
# pylint: disable=import-error
from unittest import TestCase
from unittest import main as launch_tests

import PyFunceble
from PyFunceble.helpers import Command, Dict, Directory, File, Hash, Regex


class TestHash(TestCase):
    """
    This class will test PyFunceble.helpers.Hash
    """

    def setUp(self):
        """
        This method will initiate everything needed for the tests.
        """

        self.file = "this_file_should_be_deleted"
        self.data_to_write = ["Hello World!", "Thanks for using PyFunceble"]

        self.expected_hashed = {
            "md5": "ba2e0e1774c2e60e2327f263402facd4",
            "sha1": "b5c8520cd2c422019997dc6fdbc9cb9d7002356e",
            "sha224": "863c46d5ed52b439da8f62a791e77c0cbbfb7d92af7c5549279f580d",
            "sha384": "6492f4b5732e0af4b9edf2c29ee4622c62ee418e5d6e0f34b13cb80560a28256c6e21e949119872d26d2327fc112a63b",  # pylint: disable=line-too-long
            "sha512": "f193ad6ee2cfbecd580225d8e6bfb9df1910e5ca6135b21b03ae208a007f71e9b57b55e299d27157551a18ef4dfdde23c96aaea796064846edc6cd25ac7eaf7f",  # pylint: disable=line-too-long
        }

    def testhash_data(self):
        """
        This method will test Hash.hash_data().
        """

        expected = False
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)

        File(self.file).write("\n".join(self.data_to_write))
        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        for algo, result in self.expected_hashed.items():
            self.assertEqual(
                result,
                Hash(self.file).hash_data(algo),
                msg="%s did not passed the test" % repr(algo),
            )

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

    def test_get_path_not_exist(self):
        """
        This method will test Hash.get() for the case that the given file does
        not exist.
        """

        expected = False
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)

        expected = None
        actual = Hash(self.file).get()
        self.assertEqual(expected, actual)

    def test_get_all(self):
        """
        This method will test Hash.get() for the case that we want all.
        """

        expected = False
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)

        File(self.file).write("\n".join(self.data_to_write))
        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        expected = self.expected_hashed
        actual = Hash(self.file, algorithm="all").get()
        self.assertEqual(expected, actual)

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)

    def test_get_specific_algo(self):
        """
        This method will test Hash.get() for the case that we want a specifig
        algorithm.
        """

        expected = False
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)

        File(self.file).write("\n".join(self.data_to_write))
        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)

        expected = self.expected_hashed["sha512"]
        actual = Hash(self.file, algorithm="sha512", only_hash=True).get()
        self.assertEqual(expected, actual)

        File(self.file).delete()

        expected = False
        actual = PyFunceble.path.isfile(self.file)
        self.assertEqual(expected, actual)


class TestCommand(TestCase):
    """
    This class will test PyFunceble.helpers.Command().
    """

    def test_command(self):
        """
        This method test Command().execute().
        """

        expected = "PyFunceble has been written by Fun Ilrys."
        actual = Command("echo '%s'" % expected).execute()

        self.assertEqual(expected + "\n", actual)


class TestDict(TestCase):
    """
    This class will test PyFunceble.helpers.Dict().
    """

    def setUp(self):
        """
        This method will setup everything needed for the tests.
        """

        self.to_test = {
            "Hello": "world",
            "World": {"world", "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "Py": "Funceble",
            "pyfunceble": ["funilrys"],
        }

    def test_remove_key(self):
        """
        This method will test Dict().remove_key().
        """

        expected = {
            "Hello": "world",
            "World": {"world", "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "pyfunceble": ["funilrys"],
        }

        actual = Dict(self.to_test).remove_key("Py")

        self.assertEqual(expected, actual)

        # Test of the case that a dict is not given
        expected = None
        actual = Dict(["Hello", "World!"]).remove_key("Py")

        self.assertEqual(expected, actual)

    def test_rename_key_not_dict(self):
        """
        This method will test Dict().rename_key() for the case that no dict is
        given.
        """

        expected = None
        actual = Dict(self.to_test).rename_key(["Fun", "Ilrys"])

        self.assertEqual(expected, actual)

    def test_rename_key_single(self):
        """
        This method will test Dict().rename_key() for the case that we want to
        rename only one key.
        """

        # Test of the strict case
        expected = {
            "Hello": "world",
            "World": {"world", "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "PyFunceble": "Funceble",
            "pyfunceble": ["funilrys"],
        }

        actual = Dict(self.to_test).rename_key({"Py": "PyFunceble"})

        self.assertEqual(expected, actual)

        # Test of the non-strict case
        expected = {
            "Hello": "world",
            "World": {"world", "hello"},
            "funilrys": ["Fun", "Ilrys"],
            "PyFunceble": "Funceble",
            "pyfunceble": ["funilrys"],
        }

        actual = Dict(self.to_test).rename_key({"fun": "nuf"}, strict=False)

    def test_to_yaml(self):
        """
        This method will test Dict().to_yaml.
        """
        file_to_read = "this_yaml_is_a_ghost.yaml"

        expected = False
        actual = PyFunceble.path.isfile(file_to_read)

        self.assertEqual(expected, actual)

        to_write = {"hello": ["This is PyFunceble!", "Uhh!"], "world": "Fun Ilrys"}

        expected = """hello: [This is PyFunceble!, Uhh!]
world: Fun Ilrys
"""

        Dict(to_write).to_yaml(file_to_read)

        actual = File(file_to_read).read()
        self.assertEqual(expected, actual)

        File(file_to_read).delete()

        expected = False
        actual = PyFunceble.path.isfile(file_to_read)

        self.assertEqual(expected, actual)


class TestDirectory(TestCase):
    """
    This method will test PyFunceble.helpers.Directory().
    """

    def test_fix_path(self):
        """
        This method will test Directory.fix_path().
        """

        expected = (
            "hello"
            + PyFunceble.directory_separator
            + "world"
            + PyFunceble.directory_separator
        )  # pylint: disable=line-too-long
        actual = Directory("/hello/world").fix_path()

        self.assertEqual(expected, actual)

        actual = Directory("\\hello\\world").fix_path()
        self.assertEqual(expected, actual)

        actual = Directory("hello\\world").fix_path()
        self.assertEqual(expected, actual)

        actual = Directory(r"hello\world").fix_path()
        self.assertEqual(expected, actual)

        actual = Directory(r"hello/world/").fix_path()
        self.assertEqual(expected, actual)

        to_test = ["", None, []]

        for element in to_test:
            actual = Directory(element).fix_path()
            self.assertEqual(element, actual)


class TestFile(TestCase):
    """
    This class will test PyFunceble.helpers.File()
    """

    def test_write_delete(self):
        """
        This method test File.write() along with File.delete().
        """

        expected = "Hello, World! I'm domain2idna"
        File("hi").write(expected)

        with open("hi") as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        expected = False
        File("hi").delete()
        actual = PyFunceble.path.isfile("hi")

        self.assertEqual(expected, actual)

    def test_write_overwrite_delete(self):
        """
        This metthod test File.write() along with File.write() for the case that
        we want to overwrite the content of a file.
        """

        expected = "Hello, World! I'm domain2idna"
        File("hi").write(expected)

        with open("hi") as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        expected = "Hello, World! Python is great, you should consider learning it!"
        File("hi").write(expected, overwrite=True)

        with open("hi") as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        expected = False
        File("hi").delete()
        actual = PyFunceble.path.isfile("hi")

        self.assertEqual(expected, actual)

    def test_copy(self):
        """
        This method test File.copy().
        """

        file_to_write = "hello_world"
        copy_destination = "world_hello"

        expected = False
        actual = PyFunceble.path.isfile(file_to_write)

        self.assertEqual(expected, actual)

        expected = "Hello, World! Python is great, you should consider learning it!"
        File(file_to_write).write(expected)

        with open(file_to_write) as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        expected = False
        actual = PyFunceble.path.isfile(copy_destination)

        self.assertEqual(expected, actual)

        File(file_to_write).copy(copy_destination)

        expected = True
        actual = PyFunceble.path.isfile(copy_destination)

        self.assertEqual(expected, actual)

        expected = "Hello, World! Python is great, you should consider learning it!"

        with open(copy_destination) as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        File(copy_destination).delete()
        File(file_to_write).delete()
        expected = False
        actual = PyFunceble.path.isfile(copy_destination)

        self.assertEqual(expected, actual)

        actual = PyFunceble.path.isfile(file_to_write)

        self.assertEqual(expected, actual)

    def test_read_delete(self):
        """
        This method test File.read() along with helpers.File.delete.
        """

        expected = "Hello, World! This has been written by Fun Ilrys."
        File("hi").write(expected)
        actual = File("hi").read()

        self.assertEqual(expected, actual)

        expected = False
        File("hi").delete()
        actual = PyFunceble.path.isfile("hi")

        self.assertEqual(expected, actual)


class TestRegex(TestCase):
    """
    This class will test Regex().
    """

    def setUp(self):
        """
        This method will setup everything needed for the tests.
        """

        self.data_list = [
            "hello",
            "world",
            "funilrys",
            "funceble",
            "PyFunceble",
            "pyfunceble",
        ]
        self.data = "Hello, this is Fun Ilrys. I just wanted to know how things goes around the tests."  # pylint: disable=line-too-long

    def test_not_matching_list(self):
        """
        This method will test Regex.not_matching_list().
        """

        regex = "fun"
        expected = ["hello", "world", "PyFunceble"]
        actual = Regex(self.data_list, regex).not_matching_list()

        self.assertEqual(expected, actual)

    def test_matching_list(self):
        """
        This method will test Regex.match_list().
        """

        regex = "fun"
        expected = ["funilrys", "funceble", "pyfunceble"]
        actual = Regex(self.data_list, regex).matching_list()

        self.assertEqual(expected, actual)

    def test_match(self):
        """
        This method will test Regex.match() for the case that we want a specific
        group.
        """

        # Test of the rematch case.
        regex = r"([a-z]{1,})\s([a-z]{1,})\s"
        expected = "is"
        actual = Regex(self.data, regex, rematch=True, group=1).match()

        self.assertEqual(expected, actual)

        # Test of the group case
        regex = "e"
        expected = "e"
        actual = Regex(self.data, regex, group=0).match()

        self.assertEqual(expected, actual)

    def test_replace(self):
        """
        This method will test Regex.replace().
        """

        regex = "th"
        expected = "Hello, htis is Fun Ilrys. I just wanted to know how htings goes around hte tests."  # pylint: disable=line-too-long
        actual = Regex(self.data, regex, replace_with="ht").replace()

        self.assertEqual(expected, actual)

        # Test of the case that there is not replace_with
        regex = "th"
        expected = self.data
        actual = Regex(self.data, regex).replace()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
