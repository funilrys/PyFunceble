"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all domain syntax checker.

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
from typing import Optional, Tuple

from PyFunceble.checker.base import CheckerBase
from PyFunceble.dataset.iana import IanaDataset
from PyFunceble.dataset.public_suffix import PublicSuffixDataset


class DomainSyntaxCheckerBase(CheckerBase):
    """
    Provides an interface to check the syntax of a second domain.

    :param str subject:
        Optional, The subject to work with.
    """

    # pylint: disable=line-too-long
    SPECIAL_USE_DOMAIN_NAMES_EXTENSIONS = ["onion"]
    """
    Specifies the extension which are specified as "Special-Use Domain Names"
    and supported by our project.

    :type: list

    .. seealso::
       * `RFC6761`_
       * `IANA Special-Use Domain Names`_ assignments.
       * `RFC7686`_

    .. _RFC6761: https://tools.ietf.org/html/rfc6761
    .. _RFC7686: https://tools.ietf.org/html/rfc6761
    .. _IANA Special-Use Domain Names: https://www.iana.org/assignments/special-use-domain-names/special-use-domain-names.txt
    """

    last_point_index: Optional[int] = None
    """
    Saves the index of the last point.
    """

    iana_dataset: Optional[IanaDataset] = None
    public_suffix_dataset: Optional[PublicSuffixDataset] = None

    def __init__(self, subject: Optional[str] = None) -> None:
        self.iana_dataset = IanaDataset()
        self.public_suffix_dataset = PublicSuffixDataset()

        super().__init__(subject)

    def reset_last_point_index(func):  # pylint: disable=no-self-argument
        """
        Resets the last point index before executing the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.last_point_index = None

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def find_last_point_index(func):  # pylint: disable=no-self-argument
        """
        Try to find the index of the last point after the execution of the
        decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            self.last_point_index = self.get_last_point_index(self.idna_subject)

            return result

        return wrapper

    @CheckerBase.subject.setter
    @reset_last_point_index
    @find_last_point_index
    def subject(self, value: str):
        """
        Sets the subject to work with.

        :param value:
            The subject to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        # pylint: disable=no-member
        super(DomainSyntaxCheckerBase, self.__class__).subject.fset(self, value)

    @staticmethod
    def get_last_point_index(subject: str) -> Optional[int]:
        """
        Provides the index of the last point of the given subject.
        """

        try:
            if subject.endswith("."):
                return subject[:-1].rfind(".")

            return subject.rindex(".")
        except ValueError:
            return None

    def get_subject_without_suffix(
        self, subject: str, extension: str
    ) -> Optional[Tuple[Optional[int], Optional[str]]]:
        """
        Provides the given subject without the suffix.

        :param subject:
            The subject to work with.
        :param extension:
            The extension previously extracted.
        """

        if extension in self.public_suffix_dataset:
            for suffix in self.public_suffix_dataset.get_available_suffix(extension):
                try:
                    return subject[: subject.rindex(f".{suffix}")], suffix
                except ValueError:
                    continue

        return None, None

    @CheckerBase.ensure_subject_is_given
    def get_extension(self) -> Optional[str]:
        """
        Provides the extension to work with (if exists).
        """

        if self.last_point_index is None:
            return None

        # Plus one is for the leading point.
        extension = self.idna_subject[self.last_point_index + 1 :]

        if extension.endswith("."):
            extension = extension[:-1]

        return extension

    def is_valid(self) -> bool:
        """
        Validate the given subject.
        """

        raise NotImplementedError()
