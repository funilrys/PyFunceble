"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all our subclasses related to the system management.

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

import argparse
import functools
from typing import Callable, Optional


class SystemBase:
    """
    Provides the base of all system classes. The idea is that every
    system classes will have access to the argument given by end-user.

    Each of them will have a start method which will run a set of predefined
    action. But the start method -in comparison to previous versions -
    starts on purpose.

    :param args:
        The arguments from :py:class:`argparse.ArgumentParser`.
    """

    _args: Optional[argparse.Namespace] = None

    def __init__(self, args: Optional[argparse.Namespace] = None) -> None:
        if args is not None:
            self.args = args

    def ensure_args_is_given(
        func: Callable[["SystemBase"], "SystemBase"]
    ):  # pylint: disable=no-self-argument
        """
        Ensures that the :code:`self.args` attribute is given before launching
        the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.args, argparse.Namespace):
                raise TypeError("<self.args> is not given.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def args(self) -> Optional[argparse.Namespace]:
        """
        Provides the current state of the :code:`_args` attribute.
        """

        return self._args

    @args.setter
    def args(self, value: argparse.Namespace) -> None:
        """
        Sets the given args.

        :param value:
            The arguments to work with.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`argparse.Namespace`
        """

        if not isinstance(value, argparse.Namespace):
            raise TypeError(
                f"<value> should be {argparse.Namespace}, {type(value)} given."
            )

        self._args = value

    def set_args(self, value: argparse.Namespace) -> "SystemBase":
        """
        Sets the given args.

        :param value:
            The arguments to work with.
        """

        self.args = value

        return self

    @ensure_args_is_given
    def start(self) -> "SystemBase":
        """
        Provides a launcher for a brunch of predefined actions defined by
        the current object.
        """

        raise NotImplementedError()
