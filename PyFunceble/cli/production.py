"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the production preparation logic. We understand by production logic
the logic to apply before commiting/publishing a new version of the code.

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

import sys
from os import sep as directory_separator
from os import walk

from colorama import Fore, Style

import PyFunceble


class Production:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Manages and provides the production preparation logic.

    .. note::
        We do this because we want to be able to distribute
        a new version without having to have a separate
        tool/argument/logic.

        For the history, in Funceble, this class will be the
        equivalent of the `tool` script/file.

    :param bool extern:
        Tell us if we do not have to execute the logic automatically.
        This allow method to be called.
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
            self.version_yaml = PyFunceble.abstracts.Version.split_versions(
                self.data_version_yaml["current_version"]
            )

            # We we get the full version with the non-digits and the digits.
            self.current_version = PyFunceble.abstracts.Version.split_versions(
                PyFunceble.VERSION, return_non_digits=True
            )

            if self._is_version_greater() or not PyFunceble.abstracts.Version.literally_compare(
                PyFunceble.VERSION, self.data_version_yaml["current_version"]
            ):
                # * The local version is greater than the older one.
                # or
                # * The local version is literally different than the
                # upstream one.

                # We clean the output directory.
                PyFunceble.output.Clean(clean_all=True)

                # We generate the productive directory structure file.
                PyFunceble.output.Constructor(production=True)

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

                # We fix the urls everywhere needed.
                self._update_urls()

                # We fix the urls in the code.
                self._update_code_urls()

                # We fix the setup.py.
                self._update_setup_py()

                # We fix the .travis.yml file.
                self._update_travis_yml()

                # We save our version data into our `version.yaml` file.
                PyFunceble.helpers.Dict(self.data_version_yaml).to_yaml_file(
                    PyFunceble.CONFIG_DIRECTORY + "version.yaml"
                )

                # We prepare the message we are going to print on screen.
                message = Fore.GREEN + Style.BRIGHT + "We are ready to ship!! \n"
                message += (
                    Fore.CYAN
                    + "Please do not touch version.yaml nor setup.py (version update)"
                )  # pylint: disable=line-too-long

                # We print the message.
                print(message)

                # We exit the process.
                sys.exit(0)
            else:
                # The local version is less or equal to the older one.

                # We print a message on screen.
                print(
                    Fore.YELLOW
                    + Style.BRIGHT
                    + "Are you sure that you did some changes ? Please update PyFunceble.VERSION if it is the case."  # pylint: disable=line-too-long
                )

                # We exit the process.
                sys.exit(1)

    def _update_urls(self):
        """
        Reads the file/dir and update all links/URL.
        """

        to_fix = [
            # We fix the urls in the README file.
            PyFunceble.CONFIG_DIRECTORY + "README.rst",
            # We fix the urls in the configuration file.
            PyFunceble.CONFIG_DIRECTORY + ".PyFunceble_production.yaml",
            # We fix the urls in the setup.py file.
            PyFunceble.CONFIG_DIRECTORY + "setup.py",
            # We fix the urls in the documentation index.
            PyFunceble.CONFIG_DIRECTORY
            + directory_separator
            + "docs"
            + directory_separator
            + "index.rst",
            # We fix the urls in the documentation logic representation.
            PyFunceble.CONFIG_DIRECTORY
            + directory_separator
            + "docs"
            + directory_separator
            + "code"
            + directory_separator
            + "logic-representation.rst",
            # We fix the urls in the usage documentation.
            PyFunceble.CONFIG_DIRECTORY
            + directory_separator
            + "docs"
            + directory_separator
            + "usage"
            + directory_separator
            + "from-a-terminal.rst",
            # We fix the urls in the links configuration documentation.
            PyFunceble.CONFIG_DIRECTORY
            + directory_separator
            + "docs"
            + directory_separator
            + "configuration"
            + directory_separator
            + "links.rst",
            # We fix the urls in the db_types directory.
            PyFunceble.CONFIG_DIRECTORY
            + directory_separator
            + "db_types"
            + directory_separator,
        ]

        for fix_it in to_fix:
            if PyFunceble.helpers.File(fix_it).exists():
                self._update_docs(fix_it)
            elif PyFunceble.helpers.Directory(fix_it).exists():
                for root, _, files in walk(fix_it):
                    for file in files:
                        self._update_docs(root + directory_separator + file)
            else:
                raise FileNotFoundError(fix_it)

    def _update_code_urls(self):
        """
        Reads the code and update all links/URL.
        """

        to_ignore = [".gitignore", ".keep", "test_converter_internal_url.py"]

        for root, _, files in walk(
            PyFunceble.CONFIG_DIRECTORY
            + directory_separator
            + "PyFunceble"
            + directory_separator
        ):
            # We loop through every directories and files in the `PyFunceble` directory.

            for file in files:
                # We loop through the list of files of the currently read directory.

                if file not in to_ignore and "__pycache__" not in root:
                    # * The filename is not into the list of file to ignore.
                    # and
                    # * The directory we are reading is not `__pycache__`.

                    if root.endswith(directory_separator):
                        # The root directory ends with the directory separator.

                        # We fix the path in the currently read file.
                        self._update_docs(root + file)
                    else:
                        # The root directory does not ends with the directory separator.

                        # We fix the path in the currently read file.
                        # (after appending the directory separator between the root and file)
                        self._update_docs(root + directory_separator + file)

        for root, _, files in walk(
            PyFunceble.CONFIG_DIRECTORY
            + directory_separator
            + "tests"
            + directory_separator
        ):
            # We loop through every directories and files in the `tests` directory.
            for file in files:
                # We loop through the list of files of the currently read directory.

                if file not in to_ignore and "__pycache__" not in root:
                    # * The filename is not into the list of file to ignore.
                    # and
                    # * The directory we are reading is not `__pycache__`.

                    if root.endswith(directory_separator):
                        # The root directory ends with the directory separator.

                        # We fix the path in the currently read file.
                        self._update_docs(root + file)
                    else:
                        # The root directory does not ends with the directory separator.

                        # We fix the path in the currently read file.
                        # (after appending the directory separator between the root and file)
                        self._update_docs(root + directory_separator + file)

    @classmethod
    def _get_current_version_yaml(cls):
        """
        Gets and returns the content of version.yaml
        """

        return PyFunceble.helpers.Dict().from_yaml_file(
            PyFunceble.CONFIG_DIRECTORY + "version.yaml"
        )

    def _is_version_greater(self):
        """
        Checks if the current version is greater as the older older one.
        """

        # we compare the 2 versions.
        checked = PyFunceble.abstracts.Version.compare(
            self.data_version_yaml["current_version"]
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
        Checks if the current branch is `dev`.
        """

        # We initiate the command we have to run in order to
        # get the branch we are currently working with.
        command = "git branch"

        # We execute and get the command output.
        command_result = PyFunceble.helpers.Command(command).execute()

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
        Checks if the current branch is `master`.
        """

        # We initiate the command we have to run in order to
        # get the branch we are currently working with.
        command = "git branch"

        # We execute and get the command output.
        command_result = PyFunceble.helpers.Command(command).execute()

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
        Checks if we have to put the previous version into the deprecated list.
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
        Checks if we have to put the previous version into the list of minimal version
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
        Updates the given documentation file or :code:`README.rst` so that
        it always gives branch related URL and information.

        .. note::
            This only apply to :code:`dev` and :code:`master` branch.

        :param str file_to_update: The file to update.
        """

        if self.is_dev_version():
            # The current version is the dev version.

            # We map what we have to replace.
            # Format: {replacement:match}
            regexes = {
                "PyFunceble/%s/" % "dev": r"PyFunceble\/%s\/" % "master",
                "=%s" % "dev": "=%s" % "master",
                "/en/%s" % "dev": "en/%s" % "master",
            }
        elif self.is_master_version():
            # The current version is the master version.

            # We map what we have to replace.
            regexes = {
                "PyFunceble/%s/" % "master": r"PyFunceble\/%s\/" % "dev",
                "=%s" % "master": "=%s" % "dev",
                "/en/%s" % "master": "en/%s" % "dev",
            }
        else:
            # The current version is not the master nor the dev version.

            # We raise an exception as the branch we are currently is not meaned
            # for production.
            raise Exception("Please switch to `dev` or `master` branch.")

        file_instance = PyFunceble.helpers.File(file_to_update)

        # We get the content of the file to fix.
        to_update = file_instance.read()

        for replacement, regex in regexes.items():
            # We loop through reach element of the map.

            # We process the replacement.
            to_update = PyFunceble.helpers.Regex(regex).replace_match(
                to_update, replacement
            )

        to_update = PyFunceble.helpers.Regex(r"/{1,}en/(dev|master)").replace_match(
            to_update, "/en/\\1"
        )

        # We finally overwrite the file to fix with the filtered.
        # content.
        file_instance.write(to_update, overwrite=True)

    def _update_setup_py(self):
        """
        Updates :code:`setup.py` so that it always have the right name.
        """

        # We initiate the path to the file we have to filter.
        setup_py_path = PyFunceble.CONFIG_DIRECTORY + "setup.py"

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

        file_instance = PyFunceble.helpers.File(setup_py_path)

        # We get the file content.
        to_update = file_instance.read()

        for replacement, regex in regexes.items():
            # We loop through our map.

            # And we process the replacement.
            to_update = PyFunceble.helpers.Regex(regex).replace_match(
                to_update, replacement
            )

        # We finally replace the content of the file with the filtered
        # version.
        file_instance.write(to_update, overwrite=True)

    def _update_travis_yml(self):
        """
        Updates :code:`.travis.yml` according to current branch.
        """

        # We initiate the file we have to filter/update.
        travis_yml_path = PyFunceble.CONFIG_DIRECTORY + ".travis.yml"

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

        file_instance = PyFunceble.helpers.File(travis_yml_path)

        # We get the file content.
        to_update = file_instance.read()

        for replacement, regex in regexes.items():
            # We loop through the map.

            # And we process the replacement.
            to_update = PyFunceble.helpers.Regex(regex).replace_match(
                to_update, replacement
            )

        # We finally replace the file content with the filtered
        # content.
        file_instance.write(to_update, overwrite=True)
