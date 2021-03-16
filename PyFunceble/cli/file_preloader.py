"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the interface for the preloading of a given file.

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

import copy
import functools
import os
from datetime import datetime, timedelta
from typing import Any, Optional

from domain2idna import domain2idna

import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.processes.workers.tester import TesterWorker
from PyFunceble.cli.utils.stdout import print_single_line
from PyFunceble.cli.utils.testing import get_subjects_from_line
from PyFunceble.converter.adblock_input_line2subject import AdblockInputLine2Subject
from PyFunceble.converter.cidr2subject import CIDR2Subject
from PyFunceble.converter.input_line2subject import InputLine2Subject
from PyFunceble.converter.rpz_input_line2subject import RPZInputLine2Subject
from PyFunceble.converter.rpz_policy2subject import RPZPolicy2Subject
from PyFunceble.converter.subject2complements import Subject2Complements
from PyFunceble.converter.url2netloc import Url2Netloc
from PyFunceble.converter.wildcard2subject import Wildcard2Subject
from PyFunceble.dataset.autocontinue.base import ContinueDatasetBase
from PyFunceble.dataset.autocontinue.csv import CSVContinueDataset
from PyFunceble.dataset.inactive.base import InactiveDatasetBase
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.hash import HashHelper


class FilePreloader:
    """
    Provides an interface for the file preloading.
    The main idea behind this interface is to read all lines of the given file
    parse each lines into something our autocontinue dataset understand.

    Once everything preloaded in the autocontinue dataset, one can use the
    :meth:`PyFunceble.dataset.autocontinue.base.ContinueDataset.get_to_test`
    to get the next subject to test.

    By doing this, we don't have to re-read a file completely once we are sure
    that the hash of the file didn't changed.

    :param authorized:
        The authorization to launch.
        If :py:class:`None` is given, we will try to guess the best value.

    :param protocol:
        The protocol describing the file to test.
    """

    STD_AUTHORIZED: bool = False

    _authorized: Optional[bool] = False
    _protocol: Optional[dict] = None

    __description: dict = dict()
    __description_file: Optional[str] = None

    continuous_integration: Optional[ContinuousIntegrationBase] = None

    continue_dataset: Optional[ContinueDatasetBase] = None

    checker_type: Optional[str] = None

    subject2complements: Optional[Subject2Complements] = None
    inputline2subject: Optional[InputLine2Subject] = None
    adblock_inputline2subject: Optional[AdblockInputLine2Subject] = None
    wildcard2subject: Optional[Wildcard2Subject] = None
    rpz_policy2subject: Optional[RPZPolicy2Subject] = None
    rpz_inputline2subject: Optional[RPZInputLine2Subject] = None
    url2netloc: Optional[Url2Netloc] = None
    cidr2subject: Optional[CIDR2Subject] = None

    def __init__(
        self,
        *,
        authorized: Optional[bool] = None,
        protocol: Optional[dict] = None,
        continuous_integration: Optional[ContinuousIntegrationBase] = None,
        checker_type: Optional[str] = None,
        adblock_inputline2subject: Optional[AdblockInputLine2Subject] = None,
        wildcard2subject: Optional[Wildcard2Subject] = None,
        rpz_policy2subject: Optional[RPZPolicy2Subject] = None,
        rpz_inputline2subject: Optional[RPZInputLine2Subject] = None,
        inputline2subject: Optional[InputLine2Subject] = None,
        subject2complements: Optional[Subject2Complements] = None,
        url2netloc: Optional[Url2Netloc] = None,
        continue_dataset: Optional[ContinueDatasetBase] = None,
        inactive_dataset: Optional[InactiveDatasetBase] = None,
        cidr2subject: Optional[CIDR2Subject] = None,
    ) -> None:
        if authorized is not None:
            self.authorized = authorized
        else:
            self.guess_and_set_authorized()

        if protocol is not None:
            self.file_path = protocol

        self.continuous_integration = continuous_integration

        self.checker_type = checker_type
        self.adblock_inputline2subject = adblock_inputline2subject
        self.wildcard2subject = wildcard2subject
        self.rpz_policy2subject = rpz_policy2subject
        self.rpz_inputline2subject = rpz_inputline2subject
        self.inputline2subject = inputline2subject
        self.subject2complements = subject2complements
        self.url2netloc = url2netloc
        self.continue_dataset = continue_dataset
        self.inactive_dataset = inactive_dataset
        self.cidr2subject = cidr2subject

    def execute_if_authorized(default: Any = None):  # pylint: disable=no-self-argument
        """
        Executes the decorated method only if we are authorized to process.
        Otherwise, apply the given :code:`default`.

        .. warning::
            If :py:class:`None` is given as default value, this method will
            return the :code:`self` object.
        """

        def inner_method(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.authorized:
                    return func(self, *args, **kwargs)  # pylint: disable=not-callable
                return self if default is None else default

            return wrapper

        return inner_method

    def ensure_protocol_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the protocol is given before launching the decorated method.

        :raise RuntimeError:
            When the protocol is not declared yet.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.protocol is None:
                raise RuntimeError("<self.protocol> is not given.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def authorized(self) -> Optional[bool]:
        """
        Provides the current state of the :code:`_authorized` attribute.
        """

        return self._authorized

    @authorized.setter
    def authorized(self, value: bool) -> None:
        """
        Sets the value of the :code:`_authorized` attribute.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._authorized = value

    def set_authorized(self, value: bool) -> "FilePreloader":
        """
        Sets the value of the :code:`_authorized` attribute.

        :param value:
            The value to set.
        """

        self.authorized = value

        return self

    @property
    def protocol(self) -> Optional[dict]:
        """
        Provides the current state of the :code:`_file_path` attribute.
        """

        return self._protocol

    @protocol.setter
    def protocol(self, value: dict) -> None:
        """
        Sets the value of the :code:`_protocol` attribute.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`dict`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, dict):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._protocol = value
        self.__description_file = os.path.join(
            self._protocol["output_dir"], PyFunceble.cli.storage.PRE_LOADER_FILE
        )

    def set_protocol(self, value: dict) -> "FilePreloader":
        """
        Sets the value of the :code:`_protocol` attribute.

        :param value:
            The value to set.
        """

        self.protocol = value

        return self

    def guess_and_set_authorized(self) -> "FilePreloader":
        """
        Try to guess and set the value of the :code:`_authorized` attribute.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if bool(PyFunceble.storage.CONFIGURATION.cli_testing.autocontinue) and bool(
                PyFunceble.storage.CONFIGURATION.cli_testing.preload_file
            ):
                self.authorized = True
            else:
                self.authorized = self.STD_AUTHORIZED
        else:
            self.authorized = self.STD_AUTHORIZED

        return self

    @execute_if_authorized(False)
    @ensure_protocol_is_given
    def does_preloader_description_file_exists(self) -> bool:
        """
        Checks if our preloader file exists.
        """

        return FileHelper(self.__description_file).exists()

    def __load_description(self) -> "FilePreloader":
        """
        Loads the description into the interface.
        """

        if self.does_preloader_description_file_exists():
            self.__description = DictHelper().from_json_file(self.__description_file)
        else:
            self.__description = copy.deepcopy(self.protocol)
            self.__description["previous_hash"] = None
            self.__description["hash"] = None
            self.__description["line_number"] = 1

        return self

    def __save_description(self) -> "FilePreloader":
        """
        Saves the description at its destination.
        """

        self.__description.update(self.protocol)

        DictHelper(self.__description).to_json_file(self.__description_file)

    @execute_if_authorized(None)
    @ensure_protocol_is_given
    def start(self, print_dots: bool = False) -> "FilePreloader":
        """
        Starts the pre-loading of the currently set file path.
        """

        self.__load_description()

        broken = False
        file_helper = FileHelper(self.protocol["subject"])
        self.__description["hash"] = HashHelper().hash_file(file_helper.path)

        if isinstance(self.continue_dataset, CSVContinueDataset):
            self.continue_dataset.set_base_directory(self.protocol["output_dir"])

        if (
            self.__description["checker_type"] != self.protocol["checker_type"]
            or self.__description["subject_type"] != self.protocol["subject_type"]
        ):
            try:
                self.continue_dataset.cleanup()
            except TypeError:
                self.continue_dataset.cleanup(session_id=self.protocol["session_id"])

        if self.__description["hash"] != self.__description["previous_hash"]:
            # Forces the reading of each lines because there is literally no
            # way to know where something has been changed.
            self.__description["line_number"] = 1

        if (
            self.__description["checker_type"] != self.protocol["checker_type"]
            or self.__description["subject_type"] != self.protocol["subject_type"]
            or self.__description["hash"] != self.__description["previous_hash"]
        ):
            try:
                with file_helper.open("r", encoding="utf-8") as file_stream:
                    line_num = 1

                    for line in file_stream:
                        if line_num < self.__description["line_number"]:
                            line_num += 1
                            continue

                        if (
                            self.continuous_integration
                            and self.continuous_integration.is_time_exceeded()
                        ):
                            broken = True
                            break

                        line = line.strip()

                        if self.rpz_policy2subject and "SOA" in line:
                            self.rpz_policy2subject.set_soa(line.split()[0])

                        for subject in get_subjects_from_line(
                            line,
                            self.checker_type,
                            adblock_inputline2subject=self.adblock_inputline2subject,
                            wildcard2subject=self.wildcard2subject,
                            rpz_policy2subject=self.rpz_policy2subject,
                            rpz_inputline2subject=self.rpz_inputline2subject,
                            inputline2subject=self.inputline2subject,
                            subject2complements=self.subject2complements,
                            url2netloc=self.url2netloc,
                            cidr2subject=self.cidr2subject,
                        ):

                            to_send = copy.deepcopy(self.protocol)
                            to_send["subject"] = subject
                            to_send["idna_subject"] = domain2idna(subject)
                            to_send["tested_at"] = datetime.utcnow() - timedelta(
                                days=365.25 * 20
                            )

                            if self.inactive_dataset.exists(to_send):
                                print_single_line("I")
                                continue

                            if TesterWorker.should_be_ignored(
                                subject=to_send["idna_subject"]
                            ):
                                print_single_line("X")
                                continue

                            self.continue_dataset.update(to_send, ignore_if_exist=True)

                            if print_dots:
                                print_single_line()

                        self.__description["line_number"] += 1
                        line_num += 1
            except KeyboardInterrupt as exception:
                self.__save_description()
                raise exception

        if not broken:
            self.__description["previous_hash"] = self.__description["hash"]

        self.__save_description()

        return self
