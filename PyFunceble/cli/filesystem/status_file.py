"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides everything related to our status file generation.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

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

import functools
import os
from typing import Optional, Union

import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus
from PyFunceble.checker.reputation.status import ReputationCheckerStatus
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.checker.syntax.status import SyntaxCheckerStatus
from PyFunceble.cli.filesystem.dir_base import FilesystemDirBase
from PyFunceble.cli.filesystem.dir_structure.restore import (
    DirectoryStructureRestoration,
)
from PyFunceble.cli.filesystem.printer.file import FilePrinter
from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.utils.platform import PlatformUtility


class StatusFileGenerator(FilesystemDirBase):
    """
    Provides an interface for the generation of the status file from
    a given status.
    """

    # pylint: disable=too-many-public-methods

    STD_HOSTS_IP: str = "0.0.0.0"
    STD_ALLOW_HOSTS_FILES: bool = True
    STD_ALLOW_PLAIN_FILES: bool = True
    STD_ALLOW_ANALYTIC_FILES: bool = True
    STD_ALLOW_UNIFIED_FILE: bool = False

    file_printer: FilePrinter = FilePrinter()

    _test_dataset: Optional[dict] = None
    _status: Optional[
        Union[SyntaxCheckerStatus, AvailabilityCheckerStatus, ReputationCheckerStatus]
    ] = None

    _allow_hosts_files: bool = True
    _allow_plain_files: bool = True
    _allow_analytic_files: bool = True
    _allow_unified_file: bool = False

    _hosts_ip: Optional[str] = None

    def __init__(
        self,
        status: Optional[
            Union[
                SyntaxCheckerStatus, AvailabilityCheckerStatus, ReputationCheckerStatus
            ]
        ] = None,
        *,
        allow_hosts_files: Optional[bool] = None,
        allow_plain_files: Optional[bool] = None,
        allow_analytic_files: Optional[bool] = None,
        hosts_ip: Optional[str] = None,
        allow_unified_file: Optional[bool] = None,
        parent_dirname: Optional[str] = None,
        test_dataset: Optional[dict] = None,
    ) -> None:
        if status is not None:
            self.status = status

        if allow_hosts_files is not None:
            self.allow_hosts_files = allow_hosts_files
        else:
            self.guess_and_set_allow_hosts_files()

        if allow_plain_files is not None:
            self.allow_plain_files = allow_plain_files
        else:
            self.guess_and_set_allow_plain_files()

        if allow_analytic_files is not None:
            self.allow_analytic_files = allow_analytic_files
        else:
            self.guess_and_set_allow_analytic_files()

        if hosts_ip is not None:
            self.hosts_ip = hosts_ip
        else:
            self.guess_and_set_hosts_ip()

        if allow_unified_file is not None:
            self.allow_unified_file = allow_unified_file
        else:
            self.guess_and_set_allow_unified_file()

        if test_dataset is not None:
            self.test_dataset = test_dataset

        super().__init__(parent_dirname=parent_dirname)

    def ensure_status_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the status is given before launching the decorated method.

        :raise TypeError:
            When :code:`self.status` is not set.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(
                self.status,
                CheckerStatusBase,
            ):
                raise TypeError("<self.status> is not given.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def status(self) -> CheckerStatusBase:
        """
        Provides the current state of the :code:`_status` attribute.
        """

        return self._status

    @status.setter
    def status(self, value: CheckerStatusBase) -> None:
        """
        Sets the status to work with.

        :param value:
            The value to set.

        :raise TypeError:
            When the given value is not a
            :class`~ PyFunceble.checker.syntax.status.SyntaxCheckerStatus`,
            :class:`~PyFunceble.checker.availability.status.AvailabilityCheckerStatus`
            or :class:`~PyFunceble.checker.reputation.status.ReputationCheckerStatus`
        """

        if not isinstance(
            value,
            CheckerStatusBase,
        ):
            raise TypeError(
                f"<value> should be {CheckerStatusBase}, {type(value)} given."
            )

        self._status = value

    def set_status(
        self,
        value: CheckerStatusBase,
    ) -> "StatusFileGenerator":
        """
        Sets the status to work with.

        :param value:
            The value to set.
        """

        self.status = value

        return self

    @property
    def test_dataset(self) -> Optional[dict]:
        """
        Provides the current state of the :code:`_test_dataset` attribute.
        """

        return self._test_dataset

    @test_dataset.setter
    def test_dataset(self, value: dict) -> None:
        """
        Sets the test dataset which was given to the tester.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class`dict`.
        """

        if not isinstance(value, dict):
            raise TypeError(f"<value> should be {dict}, {type(value)} given.")

        self._test_dataset = value

    def set_test_dataset(self, value: dict) -> "StatusFileGenerator":
        """
        Sets the test dataset which was given to the tester.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class`dict`.
        """

        self.test_dataset = value

        return self

    @property
    def allow_hosts_files(self) -> bool:
        """
        Provides the current state of the :code:`_allow_hosts_files` attribute.
        """

        return self._allow_hosts_files

    @allow_hosts_files.setter
    def allow_hosts_files(self, value: bool) -> None:
        """
        Sets the authorization to generation of hosts files.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._allow_hosts_files = value

    def set_allow_hosts_files(self, value: bool) -> "StatusFileGenerator":
        """
        Sets the authorization to generation of hosts files.

        :param value:
            The value to set.
        """

        self.allow_hosts_files = value

        return self

    def guess_and_set_allow_hosts_files(self) -> "StatusFileGenerator":
        """
        Tries to guess the value of the :code:`allow_hosts_files` from the
        configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.allow_hosts_files = (
                PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.hosts
            )
        else:
            self.allow_hosts_files = self.STD_ALLOW_HOSTS_FILES

    @property
    def allow_plain_files(self) -> bool:
        """
        Provides the current state of the :code:`_allow_plain_file` attribute.
        """

        return self._allow_plain_files

    @allow_plain_files.setter
    def allow_plain_files(self, value: bool) -> None:
        """
        Sets the authorization to generation of plain files.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._allow_plain_files = value

    def set_allow_plain_files(self, value: bool) -> "StatusFileGenerator":
        """
        Sets the authorization to generation of plain files.

        :param value:
            The value to set.
        """

        self.allow_plain_files = value

        return self

    def guess_and_set_allow_plain_files(self) -> "StatusFileGenerator":
        """
        Tries to guess the value of the :code:`allow_plain_files` from the
        configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.allow_plain_files = (
                PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.plain
            )
        else:
            self.allow_plain_files = self.STD_ALLOW_PLAIN_FILES

    @property
    def allow_analytic_files(self) -> bool:
        """
        Provides the current state of the :code:`_allow_analytic_files`
        attribute.
        """

        return self._allow_analytic_files

    @allow_analytic_files.setter
    def allow_analytic_files(self, value: bool) -> None:
        """
        Sets the authorization to generation of analytic files.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._allow_analytic_files = value

    def set_allow_analytic_files(self, value: bool) -> "StatusFileGenerator":
        """
        Sets the authorization to generation of analytic files.

        :param value:
            The value to set.
        """

        self.allow_analytic_files = value

        return self

    def guess_and_set_allow_analytic_files(self) -> "StatusFileGenerator":
        """
        Tries to guess the value of the :code:`allow_analytic_files` from the
        configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.allow_analytic_files = (
                PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.analytic
            )
        else:
            self.allow_analytic_files = self.STD_ALLOW_ANALYTIC_FILES

    @property
    def hosts_ip(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_hosts_ip` attribute.
        """

        return self._hosts_ip

    @hosts_ip.setter
    def hosts_ip(self, value: str) -> None:
        """
        Sets the hosts IP to use while generating the hosts files.

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

        self._hosts_ip = value

    def set_hosts_ip(self, value: str) -> "StatusFileGenerator":
        """
        Sets the hosts IP to use while generating the hosts files.

        :param value:
            The value to set.
        """

        self.hosts_ip = value

        return self

    def guess_and_set_hosts_ip(self) -> "StatusFileGenerator":
        """
        Tries to guess the value of the :code:`hosts_ip` from the
        configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            self.hosts_ip = PyFunceble.storage.CONFIGURATION.cli_testing.hosts_ip
        else:
            self.hosts_ip = self.STD_HOSTS_IP

    @property
    def allow_unified_file(self) -> bool:
        """
        Provides the current state of the :code:`allow_unified_file` attribute.
        """

        return self._allow_unified_file

    @allow_unified_file.setter
    def allow_unified_file(self, value: bool) -> None:
        """
        Sets the authorization to generation of the unified status file.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._allow_unified_file = value

    def set_allow_unified_file(self, value: bool) -> "StatusFileGenerator":
        """
        Sets the authorization to generation of the unified status file.

        :param value:
            The value to set.
        """

        self.allow_unified_file = value

        return self

    def guess_and_set_allow_unified_file(self) -> "StatusFileGenerator":
        """
        Tries to guess the value of the :code:`allow_unified_file` from the
        configuration file.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            # pylint: disable=line-too-long
            self.allow_unified_file = (
                PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.unified_results
            )
        else:
            self.allow_unified_file = self.STD_ALLOW_UNIFIED_FILE

    def guess_all_settings(self) -> "StatusFileGenerator":
        """
        Try to guess all settings.
        """

        to_ignore = ["guess_all_settings"]

        for method in dir(self):
            if method in to_ignore or not method.startswith("guess_"):
                continue

            getattr(self, method)()

        return self

    def get_output_basedir(self) -> str:
        """
        Provides the output base directory.

        :param create_if_missing:
            Authorizes the creation of the directory if it's missing.
        """

        result = super().get_output_basedir()

        if not DirectoryHelper(result).exists():
            DirectoryStructureRestoration(self.parent_dirname).start()
        return result

    @ensure_status_is_given
    def generate_hosts_file(self) -> "StatusFileGenerator":
        """
        Generates the hosts file.
        """

        our_dataset = self.status.to_dict()
        our_dataset["ip"] = self.hosts_ip

        if not hasattr(self.status, "ip_syntax") or not self.status.ip_syntax:
            location = os.path.join(
                self.get_output_basedir(),
                PyFunceble.cli.storage.OUTPUTS.hosts.directory,
                self.status.status.upper(),
                PyFunceble.cli.storage.OUTPUTS.hosts.filename,
            )
        else:
            location = os.path.join(
                self.get_output_basedir(),
                PyFunceble.cli.storage.OUTPUTS.hosts.directory,
                self.status.status.upper(),
                PyFunceble.cli.storage.OUTPUTS.hosts.ip_filename,
            )

        self.file_printer.destination = location
        self.file_printer.dataset = our_dataset
        self.file_printer.template_to_use = "hosts"
        self.file_printer.print_interpolated_line()

        return self

    @ensure_status_is_given
    def generate_plain_file(self) -> "StatusFileGenerator":
        """
        Generates the plain file.
        """

        location = None

        if not hasattr(self.status, "ip_syntax") or not self.status.ip_syntax:
            location = os.path.join(
                self.get_output_basedir(),
                PyFunceble.cli.storage.OUTPUTS.domains.directory,
                self.status.status.upper(),
                PyFunceble.cli.storage.OUTPUTS.domains.filename,
            )

            self.file_printer.destination = location
            self.file_printer.dataset = self.status.to_dict()
            self.file_printer.template_to_use = "plain"
            self.file_printer.print_interpolated_line()

        if not hasattr(self.status, "ip_syntax") or self.status.subject_kind == "ip":
            location = os.path.join(
                self.get_output_basedir(),
                PyFunceble.cli.storage.OUTPUTS.ips.directory,
                self.status.status.upper(),
                PyFunceble.cli.storage.OUTPUTS.ips.filename,
            )

            self.file_printer.destination = location
            self.file_printer.dataset = self.status.to_dict()
            self.file_printer.template_to_use = "plain"
            self.file_printer.print_interpolated_line()

        return self

    @ensure_status_is_given
    def generate_analytic_file(self) -> "StatusFileGenerator":
        """
        Generates the analytic files.
        """

        locations_data_and_template = []

        # pylint: disable=line-too-long

        if hasattr(self.status, "http_status_code") and self.status.http_status_code:
            if PyFunceble.facility.ConfigLoader.is_already_loaded():
                http_code_dataset = PyFunceble.storage.HTTP_CODES
            else:
                http_code_dataset = PyFunceble.storage.STD_HTTP_CODES

            if (
                self.status.http_status_code in http_code_dataset.list.potentially_down
                or self.status.status
                in (PyFunceble.storage.STATUS.down, PyFunceble.storage.STATUS.invalid)
            ):
                locations_data_and_template.append(
                    (
                        os.path.join(
                            self.get_output_basedir(),
                            PyFunceble.cli.storage.OUTPUTS.analytic.directories.parent,
                            PyFunceble.cli.storage.OUTPUTS.analytic.directories.potentially_down,
                            PyFunceble.cli.storage.OUTPUTS.analytic.filenames.potentially_down,
                        ),
                        "plain",
                        self.status.to_dict(),
                    )
                )

            if self.status.http_status_code in http_code_dataset.list.up:
                locations_data_and_template.append(
                    (
                        os.path.join(
                            self.get_output_basedir(),
                            PyFunceble.cli.storage.OUTPUTS.analytic.directories.parent,
                            PyFunceble.cli.storage.OUTPUTS.analytic.directories.potentially_down,
                            PyFunceble.cli.storage.OUTPUTS.analytic.filenames.up,
                        ),
                        "plain",
                        self.status.to_dict(),
                    )
                )

            if (
                self.status.http_status_code in http_code_dataset.list.potentially_up
                or self.status.status == PyFunceble.storage.STATUS.down
            ):
                locations_data_and_template.append(
                    (
                        os.path.join(
                            self.get_output_basedir(),
                            PyFunceble.cli.storage.OUTPUTS.analytic.directories.parent,
                            PyFunceble.cli.storage.OUTPUTS.analytic.directories.potentially_down,
                            PyFunceble.cli.storage.OUTPUTS.analytic.filenames.potentially_up,
                        ),
                        "plain",
                        self.status.to_dict(),
                    )
                )

        if self.test_dataset and "from_inactive" in self.test_dataset:
            # Let's generate the supicious file :-)
            if self.status.status in [
                PyFunceble.storage.STATUS.up,
                PyFunceble.storage.STATUS.valid,
                PyFunceble.storage.STATUS.sane,
            ]:
                locations_data_and_template.append(
                    (
                        os.path.join(
                            self.get_output_basedir(),
                            PyFunceble.cli.storage.OUTPUTS.analytic.directories.parent,
                            PyFunceble.cli.storage.OUTPUTS.analytic.directories.suspicious,
                            PyFunceble.cli.storage.OUTPUTS.analytic.filenames.suspicious,
                        ),
                        "plain",
                        self.status.to_dict(),
                    )
                )

        for file_location, template, our_dataset in locations_data_and_template:
            self.file_printer.destination = file_location
            self.file_printer.dataset = our_dataset
            self.file_printer.template_to_use = template
            self.file_printer.print_interpolated_line()

        return self

    @ensure_status_is_given
    def generate_splitted_status_file(self) -> "StatusFileGenerator":
        """
        Generates the splitted status file.
        """

        self.file_printer.destination = os.path.join(
            self.get_output_basedir(),
            PyFunceble.cli.storage.OUTPUTS.splitted.directory,
            self.status.status.upper(),
        )

        if not PlatformUtility.is_unix():
            self.file_printer.destination += ".txt"

        self.file_printer.template_to_use = "all"
        self.file_printer.dataset = self.status.to_dict()
        self.file_printer.print_interpolated_line()

        return self

    @ensure_status_is_given
    def generate_unified_status_file(self) -> "StatusFileGenerator":
        """
        Generates the unified status file.
        """

        self.file_printer.destination = os.path.join(
            self.get_output_basedir(),
            PyFunceble.cli.storage.RESULTS_RAW_FILE,
        )
        self.file_printer.template_to_use = "all"
        self.file_printer.dataset = self.status.to_dict()
        self.file_printer.print_interpolated_line()

        return self

    def start(self) -> "StatusFileGenerator":
        """
        Starts the generation of everything possible.
        """

        if self.allow_hosts_files:
            self.generate_hosts_file()

        if self.allow_plain_files:
            self.generate_plain_file()

        if self.allow_analytic_files:
            self.generate_analytic_file()

        if self.allow_unified_file:
            self.generate_unified_status_file()
        else:
            self.generate_splitted_status_file()
