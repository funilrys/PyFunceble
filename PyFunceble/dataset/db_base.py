"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all datasets which acts as database interface.

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

import functools
from typing import Any, Generator, List, Optional

from PyFunceble.dataset.base import DatasetBase


class DBDatasetBase(DatasetBase):
    """
    Provides the base of all datasets which acts as database interface.
    """

    STD_REMOVE_UNNEEDED_FIELDS: bool = True
    STD_AUTHORIZED: bool = False

    FIELDS: List[str] = []
    COMPARISON_FIELDS: List[str] = []

    source_file: Optional[str] = None

    _remove_unneeded_fields: Optional[bool] = True
    _authorized: Optional[bool] = False

    def __init__(
        self,
        *,
        authorized: Optional[bool] = None,
        remove_unneeded_fields: Optional[bool] = None,
    ) -> None:
        if authorized is not None:
            self.set_authorized(authorized)

        if remove_unneeded_fields is not None:
            self.set_remove_unneeded_fields(remove_unneeded_fields)

        self.__post_init__()

    def __post_init__(self) -> None:
        """
        A method to be called (automatically) after __init__.
        """

    def execute_if_authorized(default: Any = None):  # pylint: disable=no-self-argument
        """
        Executes the decorated method only if we are authorized to process.
        Otherwise, apply the given :code:`default`.
        """

        def inner_metdhod(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.authorized:
                    return func(self, *args, **kwargs)  # pylint: disable=not-callable
                return default

            return wrapper

        return inner_metdhod

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
            When the given :code:`value` is not a :py:class:`bool`
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._authorized = value

    def set_authorized(self, value: bool) -> "DBDatasetBase":
        """
        Sets the value of the :code:`_authorized` attribute.

        :param value:
            The value to set.
        """

        self.authorized = value

        return self

    @property
    def remove_unneeded_fields(self) -> Optional[bool]:
        """
        Provides the current state of the :code:`_remove_unneeded_fields`.
        """

        return self._remove_unneeded_fields

    @remove_unneeded_fields.setter
    def remove_unneeded_fields(self, value: bool) -> None:
        """
        Sets the value of the :code:`_remove_unneeded_fields` attribute.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`bool`
        """

        if not isinstance(value, bool):
            raise TypeError(f"<value> should be {bool}, {type(value)} given.")

        self._remove_unneeded_fields = value

    def set_remove_unneeded_fields(self, value: bool) -> "DBDatasetBase":
        """
        Sets the value of the :code:`_remove_unneeded_fields` attribute.

        :param value:
            The value to set.
        """

        self.remove_unneeded_fields = value

        return self

    @execute_if_authorized(dict())  # pylint: disable=use-dict-literal
    def get_filtered_row(self, row: dict) -> dict:
        """
        Removes all unkowns fields (not declared) from the given row.

        :param row:
            The row to work with.
        """

        result = {}

        for key, value in row.items():
            if value is None:
                value = ""

            if key in self.FIELDS:
                result[key] = value

        for field in self.COMPARISON_FIELDS:
            if field not in result:
                result[field] = ""

        return result

    def add(self, row: dict) -> "DBDatasetBase":
        """
        Adds the given dataset into the database.

        :param row:
            The row or dataset to add.

        :raise TypeError:
            When the given :code:`row` is not a :py:class`dict`.
        """

        raise NotImplementedError()

    def remove(self, row: dict) -> "DBDatasetBase":
        """
        Removes the given dataset from the database.

        :param row:
            The row or dataset to remove.

        :raise TypeError:
            When the given :code:`row` is not a :py:class`dict`.
        """

        raise NotImplementedError()

    def update(self, row: dict, *, ignore_if_exist: bool = False) -> "DBDatasetBase":
        """
        Adds the given dataset into the database if it does not exists.
        Update otherwise.

        :param row:
            The row or dataset to manipulate.

        :param ignore_if_exist:
            Ignores the insertion/update if the row already exists.


        :raise TypeError:
            When the given :code:`row` is not a :py:class`dict`.
        """

        raise NotImplementedError()

    def get_content(self) -> Generator[Optional[dict], None, None]:
        """
        Provides a generator which provides the next line to read.
        """

        raise NotImplementedError()

    def cleanup(self) -> "DBDatasetBase":
        """
        Cleanups the dataset.
        """

        raise NotImplementedError()

    @execute_if_authorized(None)
    def get_filtered_content(
        self, filter_map: dict
    ) -> Generator[Optional[dict], None, None]:
        """
        Provides a generator which provides the next dataset. to read.

        :param filter_map:
            A dictionary representing what we need to filter.

        :raise TypeError:
            When the given :code:`filter_map` is not a :py:class:`dict`.
        """

        if not isinstance(filter_map, dict):
            raise TypeError(f"<filter_map> should be {dict}, {type(filter_map)} given.")

        for row in self.get_content():
            for key, value in filter_map.items():
                if key not in row:
                    continue

                if row[key] == value:
                    yield row

    def exists(self, row: dict) -> bool:
        """
        Checks if the given dataset exists in our dataset.

        :param row:
            The row or dataset to add.
        """

        raise NotImplementedError()

    def are_equal(self, read_row: dict, row: dict) -> bool:
        """
        Compares the given :code:`read_row` to the `row`.

        :param read_row:
            The row read from the dataset infrastructure.
        :param row:
            The row given by the testing infrastructure.
        """

        raise NotImplementedError()
