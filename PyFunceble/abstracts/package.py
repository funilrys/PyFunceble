"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

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

import PyFunceble.helpers as helpers


class Package:
    """
    Provides some packaging related abstractions.
    """

    NAME = "PyFunceble"
    """
    Sets the package name.

    :type: str
    """

    VERSION = "3.1.11.dev (Teal Blauwbok: Ladybug)"
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

        # We keep the digits only.
        digits = [x for x in splited_version if x.isdigit()]

        if not return_non_digits:
            # We do not have to return the non digits part of the version.

            # We return the digits part of the version.
            return digits

        # We have to return the non digit parts of the version.

        # We keep the non digits.
        non_digits = [x for x in splited_version if not x.isdigit()]

        # We return a tuple with first the digits part and finally the non digit parts.
        return digits, non_digits[0]

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

        # We get the local version.
        local = cls.split_versions(Package.VERSION)
        # We get the upstream version
        upstream = cls.split_versions(upstream)

        # A version should be in format [1,2,3] which is actually the version `1.2.3`
        # So as we only have 3 elements in the versioning,
        # we initiate the following variable in order to get the status of each parts.
        status = [None, None, None]

        for index, version_number in enumerate(local):
            # We loop through the local version.

            if int(version_number) < int(upstream[index]):
                # The local version is less than the upstream version.

                # We initiate its status to True which means that we are in
                # an old version (for the current version part).
                status[index] = True
            elif int(version_number) > int(upstream[index]):
                # The local version is greater then the upstream version.

                # We initiate its status to False which means that we are in
                # a more recent version (for the current version part).
                status[index] = False
            else:
                # The local version is eqal to the upstream version.

                # We initiate its status to None which means that we are in
                # the same version (for the current version part).
                status[index] = None

            # Otherwise the status stay None which means that there is no change
            # between both local and upstream.

        # We consider that the version is the same.
        result = None

        for data in status:
            # We loop through the list of status.
            # The purpose of this loop is only to
            # get the first not None value.

            if result is None:
                # The result is None (no changes).
                # We set the currently read one as the result.
                result = data

        # We return the result.
        return result

    @classmethod
    def is_local_dev(cls):
        """
        Checks if the local version is the development version.
        """

        return "dev" in Package.VERSION

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
            ".coveralls.yml",
            ".gitignore",
            ".PyFunceble_production.yaml",
            ".travis.yml",
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
