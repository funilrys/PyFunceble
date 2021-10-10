"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of our platform utility.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/latest/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

import platform
import unittest
import unittest.mock

from PyFunceble.utils.platform import PlatformUtility


class TestPlatformUtility(unittest.TestCase):
    """
    Tests our platform utility.
    """

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.system_platform_mock = unittest.mock.patch.object(platform, "system")

    def tearDown(self) -> None:
        """
        Destroys everything set up previously.
        """

        del self.system_platform_mock

    def test_is_cygwin(self):
        """
        Tests the method which let us know if the current platform is the
        CygWin one.
        """

        with self.system_platform_mock as platform_patch:
            platform_patch.return_value = "Cygwin"

            expected = True
            actual = PlatformUtility.is_cygwin()

            self.assertEqual(expected, actual)

    def test_is_cygwin_with_version(self):
        """
        Tests the method which let us know if the current platform is the CygWin
        one for the case that it's given with a certain version.
        """

        with self.system_platform_mock as platform_patch:
            platform_patch.return_value = "Cygwin-NT-50.0.1"

            expected = True
            actual = PlatformUtility.is_cygwin()

            self.assertEqual(expected, actual)

    def test_is_not_cygwin(self):
        """
        Tests the method which let us know if the current platform is the CygWin
        one for the case it's no cygwin version.
        """

        with self.system_platform_mock as platform_patch:
            platform_patch.return_value = "Windows"

            expected = False
            actual = PlatformUtility.is_cygwin()

            self.assertEqual(expected, actual)

    def test_is_windows(self):
        """
        Tests the method which let us know if the current platform is the
        Windows one.
        """

        with self.system_platform_mock as platform_patch:
            platform_patch.return_value = "windows"

            expected = True
            actual = PlatformUtility.is_windows()

            self.assertEqual(expected, actual)

    def test_is_not_windows(self):
        """
        Tests the method which let us know if the current platform is the
        Windows one for that case that it's the linux one.
        """

        with self.system_platform_mock as platform_patch:
            platform_patch.return_value = "Linux"

            expected = False
            actual = PlatformUtility.is_windows()

            self.assertEqual(expected, actual)

    def test_is_unix(self):
        """
        Tests the method which let us know if the current platform is the
        Linux one.
        """

        with self.system_platform_mock as platform_patch:
            platform_patch.return_value = "Linux"

            expected = True
            actual = PlatformUtility.is_unix()

            self.assertEqual(expected, actual)

    def test_is_unix_darwin(self):
        """
        Tests the method which let us know if the current platform is the
        Darwin (OSX) one.
        """

        with self.system_platform_mock as platform_patch:
            platform_patch.return_value = "Darwin"

            expected = True
            actual = PlatformUtility.is_unix()

            self.assertEqual(expected, actual)

    def test_is_not_unix(self):
        """
        Tests the method which let us know if the current platform is the
        Linux one for that case that it's the Windows one.
        """

        with self.system_platform_mock as platform_patch:
            platform_patch.return_value = "Windows"

            expected = False
            actual = PlatformUtility.is_unix()

            self.assertEqual(expected, actual)

    def test_is_mac_os(self):
        """
        Tests the method which let us know if the current platform is the
        MacOS one.
        """

        with self.system_platform_mock as platform_patch:
            platform_patch.return_value = "Darwin"

            expected = True
            actual = PlatformUtility.is_mac_os()

            self.assertEqual(expected, actual)

    def test_is_not_mac_os(self):
        """
        Tests the method which let us know if the current platform is the
        MacOS one for that case that it's the Windows one.
        """

        with self.system_platform_mock as platform_patch:
            platform_patch.return_value = "Windows"

            expected = False
            actual = PlatformUtility.is_mac_os()

            self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
