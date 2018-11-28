#!/usr/bin/env python3

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

This submodule will provide the production logic. We understand by production login
the logic to apply before commiting new code.

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
# pylint: disable=bad-continuation

import PyFunceble
from PyFunceble.clean import Clean
from PyFunceble.config import Version
from PyFunceble.directory_structure import DirectoryStructure
from PyFunceble.helpers import Command, Dict, File, Regex


class Production:  # pylint: disable=too-few-public-methods
    """
    Manage and provide the production preparation logic.

    :param extern:
        Tell us if we do not have to execute the logic automatically.
        This allow method to be called.
    :type extern: bool
    """

    def __init__(self, extern=False):
        if not extern:
            # A method of this class is not called.

            if not self.is_dev_version() and not self.is_master_version():
                # The version is not the `dev` version nor the `master` version.

                # We raise an exception telling the user that there is a
                # problem somewhere around the versioning.
                raise Exception("Please switch to `dev` or `master` branch.")

            # We read and get the current content of `version.yaml`.
            self.data_version_yaml = self._get_current_version_yaml()

            # We split the version in oder to get only the list of digits from
            # the local version.
            self.version_yaml = Version(True).split_versions(
                self.data_version_yaml["current_version"]
            )

            # We we get the full version with the non-digits and the digits.
            self.current_version = Version(True).split_versions(
                PyFunceble.VERSION, True
            )

            if self._is_version_greater():
                # The local version is greater than the older one.

                # We clean the output directory.
                Clean(None)

                # We generate the productive directory structure file.
                DirectoryStructure(production=True)

                if self._does_require_deprecation():
                    # We have to put the previous version into the list of deprecated list.

                    # We reconstruct the version.
                    to_deprecate = ".".join(self.version_yaml)

                    # And we append it into the list of deprecated version.
                    self.data_version_yaml["deprecated"].append(to_deprecate)

                if self._does_require_force_update():
                    # We have to put the previous version into the list of forced for update list.

                    # We reconstruct the version.
                    to_force_update = ".".join(self.version_yaml)

                    # And we append it into the list of minimal version.
                    self.data_version_yaml["force_update"]["minimal_version"].append(
                        to_force_update
                    )

                if self.current_version[-1]:
                    # The non digit part of the version is not empty.

                    # We append it to the digit part.
                    self.current_version[0].append(self.current_version[-1])

                # We update the current version.
                self.data_version_yaml["current_version"] = ".".join(
                    self.current_version[0]
                )

                # We fix the urls in the README file.
                self._update_docs(PyFunceble.CURRENT_DIRECTORY + "README.rst")

                # We fix the urls in the configuration file.
                self._update_docs(
                    PyFunceble.CURRENT_DIRECTORY + ".PyFunceble_production.yaml"
                )

                # We fix the urls in the documentation index.
                self._update_docs(
                    PyFunceble.CURRENT_DIRECTORY
                    + PyFunceble.directory_separator
                    + "docs"
                    + PyFunceble.directory_separator
                    + "index.rst"
                )

                # We fix the urls in the documentation logic representation.
                self._update_docs(
                    PyFunceble.CURRENT_DIRECTORY
                    + PyFunceble.directory_separator
                    + "docs"
                    + PyFunceble.directory_separator
                    + "logic-representation.rst"
                )

                # We fix the urls in the code.
                self._update_code_urls()

                # We fix the setup.py.
                self._update_setup_py()

                # We fix the .travis.yml file.
                self._update_travis_yml()

                # We save our version data into our `version.yaml` file.
                Dict(self.data_version_yaml).to_yaml(
                    PyFunceble.CURRENT_DIRECTORY + "version.yaml", flow_style=None
                )

                # We prepare the message we are going to print on screen.
                message = (
                    PyFunceble.Fore.GREEN
                    + PyFunceble.Style.BRIGHT
                    + "We are ready to ship!! \n"
                )
                message += (
                    PyFunceble.Fore.CYAN
                    + "Please do not touch version.yaml nor setup.py (version update)"
                )  # pylint: disable=line-too-long

                # We print the message.
                print(message)

                # We exit the process.
                exit(0)
            else:
                # The local version is less or equal to the older one.

                # We print a message on screen.
                print(
                    PyFunceble.Fore.YELLOW
                    + PyFunceble.Style.BRIGHT
                    + "Are you sure that you did some changes ? Please update PyFunceble.VERSION if it is the case."  # pylint: disable=line-too-long
                )

                # We exit the process.
                exit(1)

    def _update_code_urls(self):
        """
        Read the code and update all links.
        """

        to_ignore = [".gitignore", ".keep", "production.py", "publicsuffix.py"]

        for root, _, files in PyFunceble.walk(
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.directory_separator
            + "PyFunceble"
            + PyFunceble.directory_separator
        ):
            # We loop through every directories and files in the `PyFunceble` directory.

            for file in files:
                # We loop through the list of files of the currently read directory.

                if file not in to_ignore and "__pycache__" not in root:
                    # * The filename is not into the list of file to ignore.
                    # and
                    # * The directory we are reading is not `__pycache__`.

                    if root.endswith(PyFunceble.directory_separator):
                        # The root directory ends with the directory separator.

                        # We fix the path in the currently read file.
                        self._update_docs(root + file)
                    else:
                        # The root directory does not ends with the directory separator.

                        # We fix the path in the currently read file.
                        # (after appending the directory separator between the root and file)
                        self._update_docs(root + PyFunceble.directory_separator + file)

        for root, _, files in PyFunceble.walk(
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.directory_separator
            + "tests"
            + PyFunceble.directory_separator
        ):
            # We loop through every directories and files in the `tests` directory.
            for file in files:
                # We loop through the list of files of the currently read directory.

                if file not in to_ignore and "__pycache__" not in root:
                    # * The filename is not into the list of file to ignore.
                    # and
                    # * The directory we are reading is not `__pycache__`.

                    if root.endswith(PyFunceble.directory_separator):
                        # The root directory ends with the directory separator.

                        # We fix the path in the currently read file.
                        self._update_docs(root + file)
                    else:
                        # The root directory does not ends with the directory separator.

                        # We fix the path in the currently read file.
                        # (after appending the directory separator between the root and file)
                        self._update_docs(root + PyFunceble.directory_separator + file)

    @classmethod
    def _get_current_version_yaml(cls):
        """
        Get and return the content of version.yaml
        """

        return Dict().from_yaml(
            File(PyFunceble.CURRENT_DIRECTORY + "version.yaml").read()
        )

    def _is_version_greater(self):
        """
        Check if the current version is greater as the older older one.
        """

        # we compare the 2 versions.
        checked = Version(True).check_versions(
            self.current_version[0], self.version_yaml
        )

        if checked is not None and not checked:
            # The current version is greater as the older one.

            # We return True.
            return True

        # We return False
        return False

    @classmethod
    def is_dev_version(cls):
        """
        Check if the current branch is `dev`.
        """

        # We initiate the command we have to run in order to
        # get the branch we are currently working with.
        command = "git branch"

        # We execute and get the command output.
        command_result = Command(command).execute()

        for branch in command_result.split("\n"):
            # We loop through each line of the command output.

            if branch.startswith("*") and "dev" in branch:
                # The current branch is `dev`.

                # We return True.
                return True

        # The current branch is not `dev`.

        # We return False.
        return False

    @classmethod
    def is_master_version(cls):
        """
        Check if the current branch is `master`.
        """

        # We initiate the command we have to run in order to
        # get the branch we are currently working with.
        command = "git branch"

        # We execute and get the command output.
        command_result = Command(command).execute()

        for branch in command_result.split("\n"):
            # We loop through each line of the command output.

            if branch.startswith("*") and "master" in branch:
                # The current branch is `master`.

                # We return True.
                return True

        # The current branch is not `master`.

        # We return False.
        return False

    def _does_require_deprecation(self):
        """
        Check if we have to put the previous version into the deprecated list.
        """

        for index, version_number in enumerate(self.current_version[0][:2]):
            # We loop through the 2 last elements of the version.

            if version_number > self.version_yaml[index]:
                # The currently read version number is greater than the one we have in
                # the version.yaml.

                # We return True.
                return True

        # We return False, we do not need to deprecate anything.
        return False

    def _does_require_force_update(self):
        """
        Check if we have to put the previsous verion into the list of minimal version
        for force_update.
        """

        if self.current_version[0][0] > self.version_yaml[0]:
            # The current version first index is greater than the one we have in the
            # current version.yaml.

            # We return True.
            return True

        # We return False, we do not need to force the update for
        # the current version number.
        return False

    def _update_docs(self, file_to_update):
        """
        Update the given documentation file or :code:`README.rst` so that
        it always gives branch related URL and informations.

        .. note::
            This only apply to :code:`dev` and :code:`master` branch.

        :param file_to_update: The file to update.
        :type file_to_update: str
        """

        if self.is_dev_version():
            # The current version is the dev version.

            # We map what we have to replace.
            # Format: {match:replacement}
            regexes = {"/dev/": r"\/master\/", "=dev": "=master"}
        elif self.is_master_version():
            # The current version is the master version.

            # We map what we have to replace.
            regexes = {"/master/": r"\/dev\/", "=master": "=dev"}
        else:
            # The current version is not the master nor the dev version.

            # We raise an exception as the branch we are currently is not meaned
            # for production.
            raise Exception("Please switch to `dev` or `master` branch.")

        # We get the content of the file to fix.
        to_update = File(file_to_update).read()

        for replacement, regex in regexes.items():
            # We loop through reach element of the map.

            # We process the replacement.
            to_update = Regex(to_update, regex, replace_with=replacement).replace()

        # We finally overwrite the file to fix with the filtered.
        # content.
        File(file_to_update).write(to_update, overwrite=True)

    def _update_setup_py(self):
        """
        Update :code:`setup.py` so that it always have the right name.
        """

        # We initiate the path to the file we have to filter.
        setup_py_path = PyFunceble.CURRENT_DIRECTORY + "setup.py"

        if self.is_dev_version():
            # The current version is the `dev` version.

            # We map what we have to replace.
            # Format: {match:replacement}
            regexes = {
                'name="PyFunceble-dev"': r'name=".*"',
                '"Development Status :: 4 - Beta"': r'"Development\sStatus\s::.*"',
            }
        elif self.is_master_version():
            # The current version is the `dev` version.

            # We map what we have to replace.
            regexes = {
                'name="PyFunceble"': r'name=".*"',
                '"Development Status :: 5 - Production/Stable"': r'"Development\sStatus\s::.*"',
            }
        else:
            # The current version is not the `dev` nor the `master` version.

            # We raise an exception to the user, the current branch is not meant for
            # production.
            raise Exception("Please switch to `dev` or `master` branch.")

        # We get the file content.
        to_update = File(setup_py_path).read()

        for replacement, regex in regexes.items():
            # We loop through our map.

            # And we process the replacement.
            to_update = Regex(to_update, regex, replace_with=replacement).replace()

        # We finally replace the content of the file with the filtered
        # version.
        File(setup_py_path).write(to_update, overwrite=True)

    def _update_travis_yml(self):
        """
        Update :code:`.travis.yml` according to current branch.
        """

        # We initiate the file we have to filter/update.
        travis_yml_path = PyFunceble.CURRENT_DIRECTORY + ".travis.yml"

        if self.is_dev_version():
            # The current version is the `dev` version.

            # We map what we have to replace.
            # Format: {match:replacement}
            regexes = {
                "pip3 install pyfunceble-dev": r"pip3\sinstall\spyfunceble.*",
                "pip-autoremove pyfunceble-dev ": r"pip-autoremove\spyfunceble\s",
            }
        elif self.is_master_version():
            # The current version is the `master` version.

            # We map what we have to replace.
            regexes = {
                "pip3 install pyfunceble": r"pip3\sinstall\spyfunceble.*",
                "pip-autoremove pyfunceble ": r"pip-autoremove\spyfunceble[a-z-_]+\s",
            }
        else:
            # The current version is not the `master` nor the `dev` version.

            # We raise an exception, the current branch is not meant for production.
            raise Exception("Please switch to `dev` or `master` branch.")

        # We get the file content.
        to_update = File(travis_yml_path).read()

        for replacement, regex in regexes.items():
            # We loop through the map.

            # And we process the replacement.
            to_update = Regex(to_update, regex, replace_with=replacement).replace()

        # We finaly replace the file content with the filtered
        # content.
        File(travis_yml_path).write(to_update, overwrite=True)
