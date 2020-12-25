"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some test related helpers.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

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

from datetime import timedelta, timezone


def convert_ipv4_to_rpz(subject: str) -> str:
    """
    Converts the given IPv4 into a policy format which can later be used in the
    tests.
    """

    return ".".join(reversed(subject.replace("/", ".").split(".")))


def convert_ipv6_to_rpz(subject: str) -> str:
    """
    Converts the given IPV6 into a policy format which can later be used in the
    tests.
    """

    starting_point = subject.replace("/", ".")

    if "::" in starting_point:
        splitted = starting_point.split("::")

        if splitted[-1] and (splitted[-1].startswith(".") or "." in splitted[-1]):
            starting_point = starting_point.replace("::", ".zz.")
        else:
            starting_point = starting_point.replace("::", ".zz")

    return ".".join(reversed(starting_point.replace(":", ".").split(".")))


def get_timezone(
    sign: str = "+",
    days: int = 0,
    seconds: int = 0,
    microseconds: int = 0,
    milliseconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    weeks: int = 0,
) -> timezone:
    """
    Provides a timezone.

    :param str sign:
        The sign to apply. Should be :code:`+` or :code:`-`.
    :param int weeks:
        The number of weeks from UTC.
    :param int days:
        The number of days from UTC.
    :param int hours:
        The number of hours from UTC.
    :param int minutes:
        The number of minutes from UTC.
    :param int seconds:
        The number of seconds from UTC.
    :param int milliseconds:
        The number of days from UTC.
    :param int microseconds:
        The number of microseconds from UTC.
    """

    if sign == "+":
        sign = 1
    else:
        sign = -1

    delta = timedelta(
        days=days,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks,
    )

    return timezone(sign * delta)
