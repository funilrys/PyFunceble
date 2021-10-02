"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all syntax checker classes.

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

from typing import Optional

from sqlalchemy.orm import Session

import PyFunceble.storage
from PyFunceble.checker.base import CheckerBase
from PyFunceble.checker.syntax.params import SyntaxCheckerParams
from PyFunceble.checker.syntax.status import SyntaxCheckerStatus


class SyntaxCheckerBase(CheckerBase):
    """
    Provides the base of all our syntax checker classes.

    :param str subject:
        Optional, The subject to work with.
    """

    db_session: Optional[Session] = None

    status: Optional[SyntaxCheckerStatus] = None

    params: Optional[SyntaxCheckerParams] = None

    def __init__(
        self,
        subject: Optional[str] = None,
        db_session: Optional[Session] = None,
    ) -> None:
        self.params = SyntaxCheckerParams()

        self.status = SyntaxCheckerStatus()
        self.status.params = self.params

        super().__init__(subject=subject, db_session=db_session)

    def subject_propagator(self) -> "CheckerBase":
        """
        Propagate the currently set subject.

        .. warning::
            You are not invited to run this method directly.
        """

        self.status = SyntaxCheckerStatus()

        self.status.subject = self.subject
        self.status.idna_subject = self.idna_subject

        return self

    @CheckerBase.ensure_subject_is_given
    @CheckerBase.update_status_date_after_query
    def query_status(self) -> "SyntaxCheckerBase":
        """
        Queries the status.
        """

        if self.is_valid():
            self.status.status = PyFunceble.storage.STATUS.valid
        else:
            self.status.status = PyFunceble.storage.STATUS.invalid

        self.status.status_source = "SYNTAX"

        return self

    @CheckerBase.ensure_subject_is_given
    def is_valid(self) -> bool:
        raise NotImplementedError()

    # pylint: disable=useless-super-delegation
    def get_status(
        self,
    ) -> Optional[SyntaxCheckerStatus]:  # pragma: no cover ## Safety.
        return super().get_status()
