"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides everything related to the package and its version.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/master/

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
from PyFunceble import helpers


class Package:
    """
    Provides some packaging related abstractions.
    """

    NAME = "PyFunceble"
    """
    Sets the package name.

    :type: str
    """

    VERSION = "3.3.10. (Teal Blauwbok: Termite)"
    """
    Sets the package version.

    :type: str
    """


class Version:
    """
    Provides a simple way to compare our own versions.
    """

    @classmethod
    def split_versions(cls, version, return_non_digits=False):
        """
        Converts the versions to a shorter one.

        :param str version: The version to split.

        :param bool return_non_digits:
            Activate the return of the non-digits parts of the splitted
            version.

        :return:
            A tuple. The first index is the digit part of the version,
            when the second one is the the non-digit part of the
            version.
        :rtype: tuple
        """

        # We split the version.
        splited_version = version.split(".")

        def get_version_part():
            """
            Provides the version part.
            """

            return [x for x in splited_version if x.isdigit() or x[0].isdigit()]

        def get_codename_part():
            """
            Provides the codename part.
            """

            try:
                return [
                    x for x in splited_version if not x.isdigit() and not x[0].isdigit()
                ][0]
            except IndexError:
                return ""

        if not return_non_digits:
            # We do not have to return the non digits part of the version.

            # We return the digits part of the version.
            return get_version_part()

        # We return a tuple with first the digits part and finally the non digit parts.
        return get_version_part(), get_codename_part()

    @classmethod
    def literally_compare(cls, local, upstream):
        """
        Compares the given versions, literally.

        :param str local:
            The local version converted
            by :py:func:`~PyFunceble.abstracts.package.split_versions`.

        :param str upstream:
            The upstream version converted
            by :py:func:`~PyFunceble.abstracts.package.split_versions`.

        :return:
            - :code:`True`: local == upstream
            - :code:`False`: local != upstream
        :rtype: bool
        """

        return local == upstream

    @classmethod
    def compare(cls, upstream):
        """
        Compares the given versions with the local one.

        :param list local:
            The local version converted
            by :py:func:`~PyFunceble.abstracts.package.split_versions`.

        :param list upstream:
            The upstream version converted
            by :py:func:`~PyFunceble.abstracts.package.split_versions`.

        :return:
            - :code:`True`: local < upstream
            - :code:`None`: local == upstream
            - :code:`False`: local > upstream
        :rtype: bool, None
        """

        def get_version_number_pep440(version_part):
            """
            Given a version part it returns the actual version.
            As example:
                Given :code:`0a1` returns `0971`.
            """

            result = []

            for part in version_part:
                if part.isdigit():
                    result.append(part)
                else:
                    local_result = ""

                    for char in part:
                        if char.isdigit():  # pragma: no cover ## Safety.
                            local_result += local_result
                        else:
                            local_result += str(ord(char))

                    result.append(local_result)

            return "".join(result)

        def compare_them(version_number, upstream_number):
            """
            Compare and provides the result of the comparison.
            """

            # pylint: disable=too-many-return-statements

            # ORD A ==> 65 ==> 650
            if upstream_number < 650 < version_number:
                return True

            if version_number < 650 < upstream_number:
                return False

            if version_number > 650 and upstream_number > 650:

                local_upstream_number = str(upstream_number)

                for index, value in enumerate(str(version_number)):
                    try:
                        if value == local_upstream_number[index]:
                            continue
                    except IndexError:
                        # Example: Comparison of b10 to b1
                        return False

                    if value < local_upstream_number[index]:
                        return True

                    if value > local_upstream_number[index]:
                        return False

                return None

            if version_number < upstream_number:
                return True

            if version_number > upstream_number:
                return False

            return None

        local_digits, _ = Version.split_versions(
            Package.VERSION, return_non_digits=True
        )

        upstream_digits, _ = Version.split_versions(upstream, return_non_digits=True)

        result = []

        for index, version_number in enumerate(local_digits):
            try:
                version_number = int(version_number)
            except ValueError:
                version_number = int(get_version_number_pep440(version_number))

            try:
                upstream_number = int(upstream_digits[index])
            except ValueError:
                upstream_number = int(get_version_number_pep440(upstream_digits[index]))

            result.append(compare_them(version_number, upstream_number))

        try:
            return [x for x in result if x is not None][0]
        except IndexError:
            return None

    @classmethod
    def is_local_dev(cls):
        """
        Checks if the local version is the development version.
        """

        return cls.split_versions(Package.VERSION, return_non_digits=True)[
            -1
        ].startswith("dev")

    @classmethod
    def is_local_cloned(cls):  # pragma: no cover
        """
        Checks if the local version is was downloaded
        per :code:`git clone`.
        """

        if not helpers.Directory(".git").exists():
            # The git directory does not exist.

            # We return False, the current version is not the cloned version.
            return False

        # We list the list of file which can be found only in a cloned version.
        list_of_file = [
            ".coveragerc",
            ".gitignore",
            ".PyFunceble_production.yaml",
            "CODE_OF_CONDUCT.rst",
            "CONTRIBUTING.rst",
            "dir_structure_production.json",
            "MANIFEST.in",
            "README.rst",
            "requirements.txt",
            "setup.py",
            "version.yaml",
        ]

        # We list the list of directory which can be found only in a cloned
        # version.
        list_of_dir = ["docs", "PyFunceble", "tests"]

        if not all([helpers.File(x).exists() for x in list_of_file]):
            return False

        # All required files exist in the current directory.

        if not all([helpers.Directory(x).exists() for x in list_of_dir]):
            return False

        # All required directories exist in the current directory.

        # We return True, the current version is a cloned version.
        return True
