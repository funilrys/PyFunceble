"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all checker.

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

import datetime
import functools
from typing import Optional

import domain2idna
from sqlalchemy.orm import Session

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.params_base import CheckerParamsBase
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.converter.url2netloc import Url2Netloc
from PyFunceble.query.collection import CollectionQueryTool


class CheckerBase:
    """
    Provides the base of all checker.

    :param str subject:
        Optional, The subject to work with.
    :param bool do_syntax_check_first:
        Optional, Forces the checker to first perform a syntax check,

        .. warning::
            This does not apply to the syntax checker - itself.
    """

    STD_DO_SYNTAX_CHECK_FIRST: bool = False
    STD_USE_COLLECTION: bool = False

    _do_syntax_check_first: bool = False
    _use_collection: bool = False

    _subject: Optional[str] = None
    _idna_subject: Optional[str] = None

    url2netloc: Optional[Url2Netloc] = None

    db_session: Optional[Session] = None
    collection_query_tool: Optional[CollectionQueryTool] = None

    status: Optional[CheckerStatusBase] = None
    params: Optional[CheckerParamsBase] = None

    def __init__(
        self,
        subject: Optional[str] = None,
        *,
        do_syntax_check_first: Optional[bool] = None,
        db_session: Optional[Session] = None,
        use_collection: Optional[bool] = None,
    ) -> None:
        self.collection_query_tool = CollectionQueryTool()
        self.url2netloc = Url2Netloc()

        if self.params is None:
            self.params = CheckerParamsBase()

        if self.status is None:
            self.status = CheckerStatusBase()

        if subject is not None:
            self.subject = subject

        if do_syntax_check_first is not None:
            self.do_syntax_check_first = do_syntax_check_first
        else:
            self.do_syntax_check_first = self.STD_DO_SYNTAX_CHECK_FIRST

        if use_collection is not None:
            self.use_collection = use_collection
        else:
            self.guess_and_set_use_collection()

        self.db_session = db_session

    def propagate_subject(func):  # pylint: disable=no-self-argument
        """
        Propagates the subject to the object that need it after launching
        the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            self.subject_propagator()

            return result

        return wrapper

    def ensure_subject_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the subject is given before running the decorated method.

        :raise TypeError:
            If the subject is not a string.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Safety!
            if not isinstance(self.subject, str):
                raise TypeError(
                    f"<self.subject> should be {str}, {type(self.subject)} given."
                )

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def query_status_if_missing(func):  # pylint: disable=no-self-argument
        """
        Queries the status if it's missing.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Safety!
            if not self.status.status or self.status.status is None:
                self.query_status()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def update_status_date_after_query(func):  # pylint: disable=no-self-argument
        """
        Updates the status dates after running the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Safety!
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            self.status.tested_at = datetime.datetime.utcnow()

            return result

        return wrapper

    @property
    def subject(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_subject` attribute.
        """

        return self._subject

    @subject.setter
    @propagate_subject
    def subject(self, value: str) -> None:
        """
        Sets the subject to work with.

        :param value:
            The subject to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._subject = value

        try:
            self.idna_subject = domain2idna.domain2idna(value)
        except ValueError:
            self.idna_subject = value

    def set_subject(self, value: str) -> "CheckerBase":
        """
        Sets the subject to work with.

        :param value:
            The subject to set.
        """

        self.subject = value

        return self

    @property
    def idna_subject(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_idna_subject` attribute.
        """

        return self._idna_subject

    @idna_subject.setter
    def idna_subject(self, value: str) -> None:
        """
        Sets the subject to work with.

        :param value:
            The subject to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._idna_subject = value

    def set_idna_subject(self, value: str) -> "CheckerBase":
        """
        Sets the subject to work with.

        :param value:
            The subject to set.
        """

        self.idna_subject = value

        return self

    @property
    def do_syntax_check_first(self) -> None:
        """
        Provides the current state of the :code:`do_syntax_check_first`
        attribute.
        """

        return self._do_syntax_check_first

    @do_syntax_check_first.setter
    def do_syntax_check_first(self, value: bool) -> None:
        """
        Sets the value which allow us to do a syntax check first.

        :param value:
            The subject to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._do_syntax_check_first = self.params.do_syntax_check_first = value

    def set_do_syntax_check_first(self, value: bool) -> "CheckerBase":
        """
        Sets the value which allow us to do a syntax check first.

        :param value:
            The subject to set.
        """

        self.do_syntax_check_first = value

        return self

    @property
    def use_collection(self) -> bool:
        """
        Provides the current value of the :code:`_use_collection` attribute.
        """

        return self._use_collection

    @use_collection.setter
    def use_collection(self, value: bool) -> None:
        """
        Sets the value which authorizes the usage of the Collection.

        :param value:
            The value to set.

        :param TypeError:
            When the given :code:`value` is not a :py:class:`bool`.
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._use_collection = self.params.use_collection = value

    def set_use_collection(self, value: bool) -> "CheckerBase":
        """
        Sets the value which authorizes the usage of the Collection.

        :param value:
            The value to set.
        """

        self.use_collection = value

        return self

    def guess_and_set_use_collection(self) -> "CheckerBase":
        """
        Try to guess and set the value of the :code:`use_collection` attribute.
        """

        if PyFunceble.facility.ConfigLoader.is_already_loaded():
            if isinstance(PyFunceble.storage.CONFIGURATION.lookup.collection, bool):
                self.use_collection = PyFunceble.storage.CONFIGURATION.lookup.collection
            else:
                self.use_collection = self.STD_USE_COLLECTION
        else:
            self.use_collection = self.STD_USE_COLLECTION

    def subject_propagator(self) -> "CheckerBase":
        """
        Propagate the currently set subject.

        .. warning::
            You are not invited to run this method directly.

            Only the :code:`propagate_subject` decorator should call this
            method.
        """

        return self

    @ensure_subject_is_given
    def is_valid(self) -> bool:
        """
        Provides the result of the validation.
        """

        raise NotImplementedError()

    @ensure_subject_is_given
    @update_status_date_after_query
    def query_status(self) -> "CheckerBase":
        """
        Queries the status.
        """

        raise NotImplementedError()

    @query_status_if_missing
    def get_status(self) -> Optional[CheckerStatusBase]:
        """
        Provides the current state of the status.

        .. note::
            This method will automatically query status using the
            :meth:`PyFunceble.checker.base.CheckerBase.query_status` if
            the
            :attr:`PyFunceble.checker.status_base.CheckerStatusBase.status`
            attribute is not set.
        """

        return self.status
