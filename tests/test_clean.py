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

This submodule will test PyFunceble.clean.

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


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

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
from PyFunceble.clean import Clean
from PyFunceble.config import Version
from PyFunceble.helpers import File


class TestClean(TestCase):
    """
    Testing of PyFunceble.clean.
    """

    def setUp(self):
        """
        Setup everything that is needed.
        """

        PyFunceble.load_config(generate_directory_structure=False)

        self.file = (
            PyFunceble.OUTPUT_DIRECTORY
            + PyFunceble.OUTPUTS.parent_directory
            + "hello_world"
        )
        self.types = ["up", "down", "invalid", "tested"]

    def test_clean_all(self):
        """
        Test the clean_all process.
        """

        if not Version(True).is_cloned():  # pragma: no cover
            file = "whois_db.json"

            File(file).write("Hello, World!")

            expected = True
            actual = PyFunceble.path.isfile(file)

            self.assertEqual(expected, actual)
            Clean(clean_all=True)

            expected = False
            actual = PyFunceble.path.isfile(file)

            self.assertEqual(expected, actual)

    def test_with_empty_list(self):
        """
        Test the cleaning in the case that we have to test an empty
        list.
        """

        File(self.file).write("Hello, World!")

        expected = True
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)
        Clean(None)

        expected = False
        actual = PyFunceble.path.isfile(self.file)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
