#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check domains or IP availability.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

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

import PyFunceble
from PyFunceble import Fore, Style, directory_separator
from PyFunceble.clean import Clean
from PyFunceble.config import Version
from PyFunceble.directory_structure import DirectoryStructure
from PyFunceble.helpers import Command, Dict, File, Regex


class Production(object):  # pylint: disable=too-few-public-methods
    """
    This class will manage and provide the production logic.

    Argument:
        - extern: bool
            True: We do not execute the logic and allow method to be called.
    """

    def __init__(self, extern=False):
        if not extern:

            if not self._is_dev_version() and not self._is_master_version():
                raise Exception("Please switch to `dev` or `master` branch.")

            self.data_version_yaml = self._get_current_version_yaml()

            self.version_yaml = Version(True).split_versions(
                self.data_version_yaml["current_version"]
            )
            self.current_version = Version(True).split_versions(
                PyFunceble.VERSION, True
            )

            if self._is_version_greater():
                Clean(None)
                DirectoryStructure(production=True)

                if self._does_require_deprecation():
                    to_deprecate = ".".join(self.version_yaml)

                    self.data_version_yaml["deprecated"].append(to_deprecate)

                if self._does_require_force_update():
                    to_force_update = ".".join(self.version_yaml)

                    self.data_version_yaml["force_update"]["minimal_version"].append(
                        to_force_update
                    )

                if self.current_version[-1]:
                    self.current_version[0].append(self.current_version[-1])

                self.data_version_yaml["current_version"] = ".".join(
                    self.current_version[0]
                )

                self._update_docs(PyFunceble.CURRENT_DIRECTORY + "README.md")
                self._update_docs(
                    PyFunceble.CURRENT_DIRECTORY
                    + directory_separator
                    + "docs"
                    + directory_separator
                    + "index.rst"
                )
                self._update_setup_py()
                self._update_travis_yml()

                Dict(self.data_version_yaml).to_yaml(
                    PyFunceble.CURRENT_DIRECTORY + "version.yaml"
                )

                message = Fore.GREEN + Style.BRIGHT + "We are ready to ship!! \n"
                message += Fore.CYAN + "Please do not touch version.yaml nor setup.py (version update)"  # pylint: disable=line-too-long

                print(message)
                exit(0)
            else:
                print(
                    Fore.YELLOW
                    + Style.BRIGHT
                    + "Are you sure that you did some changes ? Please update PyFunceble.VERSION if it is the case."  # pylint: disable=line-too-long
                )
                exit(1)

    @classmethod
    def _get_current_version_yaml(cls):
        """
        This method get and return the content of version.yaml
        """

        return Dict().from_yaml(
            File(PyFunceble.CURRENT_DIRECTORY + "version.yaml").read()
        )

    def _is_version_greater(self):
        """
        This method check if the current version is greater as the older older one.
        """

        checked = Version(True).check_versions(
            self.current_version[0], self.version_yaml
        )

        if checked != None and not checked:
            return True

        return False

    @classmethod
    def _is_dev_version(cls):
        """
        This method check if the current branch is `dev`.
        """

        command = "git branch"
        command_result = Command(command).execute()

        for branch in command_result.split("\n"):
            if branch.startswith("*") and "dev" in branch:
                return True

        return False

    @classmethod
    def _is_master_version(cls):
        """
        This method check if the current branch is `master`.
        """

        command = "git branch"
        command_result = Command(command).execute()

        for branch in command_result.split("\n"):
            if branch.startswith("*") and "master" in branch:
                return True

        return False

    def _does_require_deprecation(self):
        """
        This method check if we have to put the previous version into the deprecated list.
        """

        for index, version_number in enumerate(self.current_version[0][:2]):
            if version_number > self.version_yaml[index]:
                return True

        return False

    def _does_require_force_update(self):
        """
        This method check if we have to put the previsous verion into the list of minimal version
        for force_update.
        """

        if self.current_version[0][0] > self.version_yaml[0]:
            return True

        return False

    def _update_docs(self, file_to_update):
        """
        This method update README.md so that it's always giving branch related bases.
        Note: This only apply to `dev` and `master` branch.

        Argument:
            - file_to_update: str
                The file to update.
        """

        if self._is_dev_version():
            regexes = {"/dev/": r"\/master\/", "=dev": "=master"}
        elif self._is_master_version():
            regexes = {"/master/": r"\/dev\/", "=master": "=dev"}
        else:
            raise Exception("Please switch to `dev` or `master` branch.")

        to_update = File(file_to_update).read()

        for replacement, regex in regexes.items():
            to_update = Regex(to_update, regex, replace_with=replacement).replace()

        File(file_to_update).write(to_update, overwrite=True)

    def _update_setup_py(self):
        """
        This method will update setup.py so that it always have the right name.
        """

        setup_py_path = PyFunceble.CURRENT_DIRECTORY + "setup.py"

        if self._is_dev_version():
            regexes = {
                'name="PyFunceble-dev"': r'name=".*"',
                '"Development Status :: 4 - Beta"': r'"Development\sStatus\s::.*"',
            }
        elif self._is_master_version():
            regexes = {
                'name="PyFunceble"': r'name=".*"',
                '"Development Status :: 5 - Production/Stable"': r'"Development\sStatus\s::.*"',
            }
        else:
            raise Exception("Please switch to `dev` or `master` branch.")

        to_update = File(setup_py_path).read()

        for replacement, regex in regexes.items():
            to_update = Regex(to_update, regex, replace_with=replacement).replace()

        File(setup_py_path).write(to_update, overwrite=True)

    def _update_travis_yml(self):
        """
        This method will update .travis.yml according to current branch.
        """

        travis_yml_path = PyFunceble.CURRENT_DIRECTORY + ".travis.yml"

        if self._is_dev_version():
            regexes = {
                "pip3 install pyfunceble-dev": r"pip3\sinstall\spyfunceble.*",
                "pip-autoremove pyfunceble-dev ": r"pip-autoremove\spyfunceble[a-z-_]+\s",
            }
        elif self._is_master_version():
            regexes = {
                "pip3 install pyfunceble": r"pip3\sinstall\spyfunceble.*",
                "pip-autoremove pyfunceble ": r"pip-autoremove\spyfunceble[a-z-_]+\s",
            }
        else:
            raise Exception("Please switch to `dev` or `master` branch.")

        to_update = File(travis_yml_path).read()

        for replacement, regex in regexes.items():
            to_update = Regex(to_update, regex, replace_with=replacement).replace()

        File(travis_yml_path).write(to_update, overwrite=True)
