"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some of our scripts.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022 Nissar Chababy

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


import copy
import functools
import os
import pathlib
from typing import List, Optional

import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.cli.filesystem.dir_structure.backup import DirectoryStructureBackup
from PyFunceble.helpers.command import CommandHelper
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.regex import RegexHelper
from PyFunceble.utils.version import VersionUtility


class ProductionPrep:
    """
    Provides an interface for the production file modification.
    The idea is that we always have 2 branches: the `dev` and the `master`
    branch.

    We want to fix all the URL to point to the right one, so this interface
    just provides everything needed for that job.

    Another important part is the cleanup of the production environment.
    What is meant is the cleanup of the `output/` directory and the
    construction of the dir_structure file.

    .. warning::
        This class assumes that you know what you are doing. Meaning that
        you should run this only if your are developing PyFunceble.
    """

    VERSION_FILE_PATH: str = os.path.join(
        PyFunceble.storage.CONFIG_DIRECTORY,
        PyFunceble.cli.storage.DISTRIBUTED_VERSION_FILENAME,
    )
    AVAILABLE_BRANCHES: List[str] = ["dev", "master"]

    regex_helper: RegexHelper = RegexHelper()
    file_helper: FileHelper = FileHelper()
    dict_helper: DictHelper = DictHelper()
    version_utility: VersionUtility = VersionUtility(PyFunceble.storage.PROJECT_VERSION)

    version_file_content: Optional[dict] = None
    """
    A copy of the local version file.
    """

    _branch: Optional[str] = None

    previous_version: Optional[str] = None
    """
    Provides the previous version (from :code:`version_file_content`)
    """

    def __init__(self, branch: Optional[str] = None) -> None:
        self.version_file_content = self.dict_helper.from_yaml_file(
            self.VERSION_FILE_PATH
        )

        self.previous_version = copy.deepcopy(
            self.version_file_content["current_version"]
        )

        if branch is not None:
            self.branch = branch

    def ensure_branch_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the branch is given before running the decorated method.

        :raise TypeError:
            When the :code:`self.branch` is not set.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.branch, str):
                raise TypeError(
                    f"<self.branch> should be {str}, " f"{type(self.branch)} given."
                )

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def branch(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_branch` attribute.
        """

        return self._branch

    @branch.setter
    def branch(self, value: str) -> None:
        """
        Sets the branch to act with.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._branch = value

    def set_branch(self, value: str) -> "ProductionPrep":
        """
        Sets the branch to act with.

        :param value:
            The value to set.
        """

        self.branch = value

        return self

    def should_be_deprecated(self, previous_version: str) -> bool:
        """
        Checks if we should deprecates the current version.
        """

        splitted = self.version_utility.get_splitted(previous_version)[0]
        local_splitted = self.version_utility.get_splitted(
            self.version_utility.local_version
        )[0]

        for index, version_part in enumerate(splitted[:2]):
            if int(version_part) < int(local_splitted[index]):
                return True

        return False

    @ensure_branch_is_given
    def update_urls(self, file: str) -> "ProductionPrep":
        """
        Updates the common URLS which are in the given file.

        :param file:
            The file to work with.

        :raise FileNotFoundError:
            When the given :code:`file` is not found.
        """

        if self.branch == "dev":
            regexes = [
                (r"PyFunceble\/%s\/" % "master", "PyFunceble/%s/" % "dev"),
                ("=%s" % "master", "=%s" % "dev"),
                (r"/{1,}en\/%s" % "latest", "/en/%s" % "dev"),
                (r"\/pyfunceble-dev.png", "/pyfunceble-%s.png" % "dev"),
                (r"\/project\/pyfunceble$", "/project/pyfunceble-%s" % "dev"),
                (
                    r"\/badge\/pyfunceble(/month|/week|)$",
                    "/badge/pyfunceble-%s\\1" % "dev",
                ),
                (r"\/blob\/%s\/" % "master", "/blob/%s/" % "dev"),
                (r"\/pypi\/v\/pyfunceble\.png$", "/pypi/v/pyfunceble-%s.png" % "dev"),
                (r"\/(logo|graphmls|gifs\/raw)\/%s\/" % "master", "/\\1/%s/" % "dev"),
                (r"\/(PyFunceble\/tree)\/%s" % "master", "/\\1/%s" % "dev"),
            ]
        elif self.branch == "master":
            regexes = [
                (r"PyFunceble\/%s\/" % "dev", "PyFunceble/%s/" % "master"),
                ("=%s" % "dev", "=%s" % "master"),
                (r"/{1,}en\/%s" % "dev", "/en/%s" % "latest"),
                (r"\/pyfunceble-dev.png", "/pyfunceble-dev.png"),
                (r"\/project\/pyfunceble-%s$" % "dev", "/project/pyfunceble"),
                (
                    r"\/badge\/pyfunceble-%s(/month|/week|)$" % "dev",
                    "/badge/pyfunceble\\1",
                ),
                (r"\/blob\/%s\/" % "dev", "/blob/%s/" % "master"),
                (
                    r"\/pypi\/v\/pyfunceble-%s\.png$" % "dev",
                    "/pypi/v/pyfunceble.png",
                ),
                (r"\/(logo|graphmls|gifs\/raw)\/%s\/" % "dev", "/\\1/%s/" % "master"),
                (r"\/(PyFunceble\/tree)\/%s" % "dev", "/\\1/%s" % "master"),
            ]
        else:
            regexes = {}

        self.file_helper.set_path(file)

        PyFunceble.facility.Logger.info(
            "Started to update our URL into %r", self.file_helper.path
        )

        if not self.file_helper.exists():
            raise FileNotFoundError(self.file_helper.path)

        to_update = self.file_helper.read()

        for regex, replacement in regexes:
            to_update = self.regex_helper.set_regex(regex).replace_match(
                to_update, replacement, multiline=True
            )

        self.file_helper.write(to_update, overwrite=True)

        PyFunceble.facility.Logger.info(
            "Finished to update our URL into %r", self.file_helper.path
        )

        return self

    def update_docs_urls(self) -> "ProductionPrep":
        """
        Updates all URL in the documentation files.
        """

        to_ignore = ["they-use-d-it.rst"]

        self.update_urls(
            os.path.join(PyFunceble.storage.CONFIG_DIRECTORY, "README.rst")
        )

        for root, _, files in os.walk(
            os.path.join(PyFunceble.storage.CONFIG_DIRECTORY, "docs")
        ):
            for file in files:
                if not file.endswith(".rst"):
                    continue

                full_path = os.path.join(root, file)

                if any(x in full_path for x in to_ignore):
                    continue

                self.update_urls(os.path.join(root, file))

    @staticmethod
    def update_code_format() -> "ProductionPrep":
        """
        Updates the format of the source code using black.
        """

        # pylint: disable=import-outside-toplevel, import-error
        import black
        import isort

        def format_file(file: str, isortconfig: isort.settings.Config) -> None:
            """
            Formats the given file using black.

            :param file:
                The file to format.
            :parm isortconfig:
                The configuration to apply while sorting the imports.
            """

            isort.api.sort_file(pathlib.Path(file), config=isortconfig)

            black.format_file_in_place(
                pathlib.Path(file),
                fast=False,
                mode=black.Mode(),
                write_back=black.WriteBack.YES,
            )

            PyFunceble.facility.Logger.info("Update format of %r", file)

        isort_config = isort.settings.Config(settings_file="setup.cfg")

        files = [
            os.path.join(PyFunceble.storage.CONFIG_DIRECTORY, "setup.py"),
        ]

        for file in files:
            format_file(file, isort_config)

        for root, _, files in os.walk(
            os.path.join(
                PyFunceble.storage.CONFIG_DIRECTORY, PyFunceble.storage.PROJECT_NAME
            )
        ):
            if "__pycache__" in root:
                continue

            for file in files:
                if not file.endswith(".py"):
                    continue

                format_file(os.path.join(root, file), isort_config)

        for root, _, files in os.walk(
            os.path.join(PyFunceble.storage.CONFIG_DIRECTORY, "tests")
        ):
            if "__pycache__" in root:
                continue

            for file in files:
                if not file.endswith(".py"):
                    continue

                format_file(os.path.join(root, file), isort_config)

    @staticmethod
    def update_documentation() -> "ProductionPrep":
        """
        Updates the code documentation.

        :raise RuntimeError:
            When one of the wanted directory is not found.
        """

        PyFunceble.facility.Logger.info(
            "Started to update and generate the documentation.",
        )

        docs_dir_helper = DirectoryHelper("docs")
        source_code_dir_helper = DirectoryHelper("PyFunceble")

        if not docs_dir_helper.exists():
            raise RuntimeError(f"{docs_dir_helper.realpath!r} not found.")

        if not source_code_dir_helper.exists():
            raise RuntimeError(f"{source_code_dir_helper.realpath!r} not found.")

        header = "Code Documentation"
        source_code_destination = os.path.join(docs_dir_helper.realpath, "code")

        CommandHelper(
            f"sphinx-apidoc -d 5 -f -H {header!r} -o "
            f"{source_code_destination!r} {source_code_dir_helper.realpath}"
        ).execute(raise_on_error=True)

        docs_destination = os.path.join(docs_dir_helper.realpath, "_build", "html")

        CommandHelper(
            f"sphinx-build -a -Q {docs_dir_helper.realpath!r} {docs_destination!r}"
        ).execute(raise_on_error=False)

        PyFunceble.facility.Logger.info(
            "Finished to update and generate the documentation.",
        )

    def update_code_urls(self) -> "ProductionPrep":
        """
        Updates all URL in the source code.
        """

        to_ignore = [
            ".gitignore",
            ".keep",
        ]

        self.update_urls(os.path.join(PyFunceble.storage.CONFIG_DIRECTORY, "setup.py"))

        for root, _, files in os.walk(
            os.path.join(
                PyFunceble.storage.CONFIG_DIRECTORY, PyFunceble.storage.PROJECT_NAME
            )
        ):
            if "__pycache__" in root:
                continue

            for file in files:
                if file in to_ignore:
                    continue

                self.update_urls(os.path.join(root, file))

        for root, _, files in os.walk(
            os.path.join(PyFunceble.storage.CONFIG_DIRECTORY, "tests")
        ):
            if "__pycache__" in root:
                continue

            for file in files:
                if file in to_ignore:
                    continue

                self.update_urls(os.path.join(root, file))

    @ensure_branch_is_given
    def update_setup_py(self) -> "ProductionPrep":
        """
        Updates content of :code:`setup.py`.

        :raise FileNotFoundError:
            When the :code:`setup.py` file does not exists.
        """

        PyFunceble.facility.Logger.info(
            "Started to update setup.py.",
        )

        if self.branch == "dev":
            regexes = [
                (r'name=".*"', 'name="PyFunceble-dev"'),
                (r'"Development\sStatus\s::.*"', '"Development Status :: 4 - Beta"'),
            ]
        elif self.branch == "master":
            regexes = [
                (r'name=".*"', 'name="PyFunceble-dev"'),
                (
                    r'"Development\sStatus\s::.*"',
                    '"Development Status :: 5 - Production/Stable"',
                ),
            ]
        else:
            regexes = [
                (r'name=".*"', 'name="PyFunceble-dev"'),
                (
                    r'"Development\sStatus\s::.*"',
                    '"Development Status :: 3 - Alpha"',
                ),
            ]

        self.file_helper.set_path(
            os.path.join(PyFunceble.storage.CONFIG_DIRECTORY, "setup.py")
        )

        if not self.file_helper.exists():
            raise FileNotFoundError(self.file_helper.path)

        to_update = self.file_helper.read()

        for regex, replacement in regexes:
            to_update = self.regex_helper.set_regex(regex).replace_match(
                to_update, replacement, multiline=True
            )

        self.file_helper.write(to_update, overwrite=True)

        PyFunceble.facility.Logger.info(
            "Started to update setup.py.",
        )

        return self

    def update_version_file(self) -> "ProductionPrep":
        """
        Updates the version file.
        """

        PyFunceble.facility.Logger.info(
            "Started to update version file.",
        )

        if self.should_be_deprecated(self.previous_version):
            to_append = ".".join(
                self.version_utility.get_splitted(self.version_utility.local_version)[0]
            )

            if to_append not in self.version_file_content["deprecated"]:
                self.version_file_content["deprecated"].append(to_append)

        self.version_file_content[
            "current_version"
        ] = PyFunceble.storage.PROJECT_VERSION

        self.dict_helper.set_subject(self.version_file_content).to_yaml_file(
            self.VERSION_FILE_PATH
        )

        PyFunceble.facility.Logger.info(
            "Finished to update version file.",
        )

        return self

    def update_dir_structure_file(self) -> "ProductionPrep":
        """
        Updates the directory structure.
        """

        DirectoryStructureBackup().start()

        return self

    def start(self) -> "ProductionPrep":
        """
        Starts the production process.
        """

        return (
            self.update_setup_py()
            .update_code_urls()
            .update_code_format()
            .update_version_file()
        )
