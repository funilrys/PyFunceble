"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all our printers.

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
import string
from typing import Dict, Optional


class PrinterBase:
    """
    Provides the base of all printer class.

    Printer classes are classes which derivate from this class. their objectives
    should be the same: Unify and simplify the way to print something to a given
    destination.
    """

    STD_UNKNOWN: str = "Unknown"

    STD_LENGTH: Dict[str, int] = {
        "idna_subject": 100,
        "status": 11,
        "status_source": 10,
        "http_status_code": 10,
        "percentage": 12,
        "expiration_date": 17,
        "amount": 12,
        "checker_type": 13,
        "days": 2,
        "hours": 2,
        "minutes": 2,
        "seconds": 6,
    }

    TEMPLATES: Dict[str, string.Template] = {
        "all": string.Template(
            "$idna_subject $status $status_source $expiration_date "
            "$http_status_code $checker_type"
        ),
        "less": string.Template("$idna_subject $status $status_source"),
        "simple": string.Template("$idna_subject $status"),
        "percentage": string.Template("$status $percentage $amount"),
        "hosts": string.Template("$ip $idna_subject"),
        "plain": string.Template("$idna_subject"),
        "execution_time": string.Template(
            "\nExecution Time: $days:$hours:$minutes:$seconds\n"
        ),
    }

    HEADERS: Dict[str, str] = {
        "idna_subject": "Subject",
        "status": "Status",
        "status_source": "Source",
        "http_status_code": "HTTP Code",
        "expiration_date": "Expiration Date",
        "percentage": "Percentage",
        "amount": "Amount",
        "ip": "IP",
        "checker_type": "Checker",
        "days": "Days",
        "hours": "Hours",
        "minutes": "Minutes",
        "seconds": "Seconds",
    }

    _template_to_use: Optional[str] = None
    _dataset: Optional[Dict[str, str]] = None

    def __init__(
        self,
        template_to_use: Optional[str] = None,
        *,
        dataset: Optional[Dict[str, str]] = None,
    ) -> None:
        if template_to_use is not None:
            self.template_to_use = template_to_use

        if dataset is not None:
            self.dataset = dataset

    def ensure_template_to_use_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the template to use is given before launching the
        decorated method.

        :raise TypeError:
            When the current :code:`self.template_to_use` is not set.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.template_to_use, str):
                raise TypeError("<self.template_to_use> is not given.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def ensure_dataset_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the dataset to write is given before launching the
        decorated method.

        :raise TypeError:
            When the current :code:`self.template_to_use` is not set.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.dataset, dict):
                raise TypeError("<self.dataset> is not given.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def template_to_use(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_template_to_use` attribute.
        """

        return self._template_to_use

    @template_to_use.setter
    def template_to_use(self, value: str) -> None:
        """
        Sets the template to use.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is not supported.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if value not in self.TEMPLATES:
            raise ValueError(
                f"<value> ({value!r}) is not supported "
                f"({list(self.TEMPLATES.keys())!r})."
            )

        self._template_to_use = value

    def set_template_to_use(self, value: str) -> "PrinterBase":
        """
        Sets the template to use.

        :param value:
            The value to set.
        """

        self.template_to_use = value

        return self

    @property
    def dataset(self) -> Optional[Dict[str, str]]:
        """
        Provides the current state of the :code:`_dataset` attribute.
        """

        return self._dataset

    @dataset.setter
    def dataset(self, value: Dict[str, str]) -> None:
        """
        Sets the dataset to apply to the template.

        :param value:
            The value to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`dict`
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, dict):
            raise TypeError(f"<value> should be {dict}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._dataset = copy.deepcopy(value)

    def set_dataset(self, value: Dict[str, str]) -> "PrinterBase":
        """
        Sets the dataset to apply to the template.

        :param value:
            The value to set.
        """

        self.dataset = value

        return self

    @ensure_template_to_use_is_given
    def get_header_to_print(self) -> str:
        """
        Provides the template header to print.
        """

        ignore_header = ["simple", "hosts", "plain", "execution_time"]

        to_print_data = [dict(), dict()]

        if self.template_to_use not in ignore_header:
            for key, value in self.HEADERS.items():
                if key not in self.TEMPLATES[self.template_to_use].template:
                    continue

                to_print_data[0][key] = f"{value:<{self.STD_LENGTH[key]}}"

            for key, value in to_print_data[0].items():
                to_print_data[1][key] = "-" * len(value)

            to_print = [
                self.TEMPLATES[self.template_to_use].safe_substitute(
                    **to_print_data[0]
                ),
                self.TEMPLATES[self.template_to_use].safe_substitute(
                    **to_print_data[1]
                ),
            ]

            return "\n".join(to_print)
        return ""

    @ensure_template_to_use_is_given
    @ensure_dataset_is_given
    def get_line_to_print(self) -> str:
        """
        Provides the line to print.
        """

        to_print = {}
        ignore_length = ["simple", "hosts", "plain", "execution_time"]

        for key, value in self.dataset.items():
            if key not in self.HEADERS:
                continue

            if not value and value != 0:
                value = self.STD_UNKNOWN

            if self.template_to_use not in ignore_length:
                to_print[key] = f"{value:<{self.STD_LENGTH[key]}}"
            else:
                to_print[key] = value

        missings = [
            x[1:]
            for x in self.TEMPLATES[self.template_to_use].template.split()
            if x.startswith("$") and x[1:] not in to_print
        ]

        for missing in missings:
            try:
                to_print[missing] = f"{self.STD_UNKNOWN:<{self.STD_LENGTH[missing]}}"
            except KeyError:
                # Example: execution time
                pass

        return self.TEMPLATES[self.template_to_use].safe_substitute(**to_print)

    def print_header(self) -> None:
        """
        Prints the header.
        """

        header = self.get_header_to_print()

        if header:
            print(f"\n\n{header}")

    def print_interpolated_line(self) -> None:
        """
        Prints the line where we are suppose to write it.
        """

        raise NotImplementedError()
