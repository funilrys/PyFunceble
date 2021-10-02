# pylint: disable=invalid-name
"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

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

import warnings
from typing import List

import PyFunceble.storage
from PyFunceble.checker.availability.domain import DomainAvailabilityChecker
from PyFunceble.checker.availability.domain_and_ip import DomainAndIPAvailabilityChecker
from PyFunceble.checker.availability.ip import IPAvailabilityChecker
from PyFunceble.checker.availability.status import AvailabilityCheckerStatus
from PyFunceble.checker.availability.url import URLAvailabilityChecker
from PyFunceble.checker.reputation.domain import DomainReputationChecker
from PyFunceble.checker.reputation.domain_and_ip import DomainAndIPReputationChecker
from PyFunceble.checker.reputation.ip import IPReputationChecker
from PyFunceble.checker.reputation.url import URLReputationChecker
from PyFunceble.checker.syntax.domain import DomainSyntaxChecker
from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.checker.syntax.ipv4 import IPv4SyntaxChecker
from PyFunceble.checker.syntax.ipv6 import IPv6SyntaxChecker
from PyFunceble.checker.syntax.second_lvl_domain import SecondLvlDomainSyntaxChecker
from PyFunceble.checker.syntax.subdomain import SubDomainSyntaxChecker
from PyFunceble.checker.syntax.url import URLSyntaxChecker
from PyFunceble.converter.subject2complements import Subject2Complements

__version__ = PyFunceble.storage.PROJECT_VERSION


def load_config(*args, **kwargs) -> None:
    """
    Placeholder before deletion.

    Since 4.0.0, you are not required to load the configuration before hand.
    If you still want too because you may want to use a special CLI related
    method, you can doing it so:

    ::

        import PyFunceble.facility

        PyFunceble.facility.ConfigLoader.start()
    """

    warnings.warn(
        "PyFunceble.load_config may be removed in the future."
        "As of today, because the configuration is not necessary (anymore), "
        "this method does nothing. Consider it a placeholder.I"
        "Please consider using PyFunceble.facility.ConfigLoader.start instead.",
        DeprecationWarning,
    )

    _, _ = args, kwargs


def test(subject: str, **kwargs) -> AvailabilityCheckerStatus:
    """
    Checks the avaialbility of the given subject assuming that it is a domain
    or an IP.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import DomainAndIPAvailabilityChecker

            my_subject = "example.org"
            the_status = DomainAndIPAvailabilityChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is available.
            print(f"{my_subject} is available ? {the_status.is_available()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.test may be removed in the future."
        "Please consider using PyFunceble.DomainAndIPAvailabilityChecker explicitly.",
        DeprecationWarning,
    )

    return DomainAndIPAvailabilityChecker(subject, **kwargs).get_status()


def url_test(subject: str, **kwargs) -> AvailabilityCheckerStatus:
    """
    Checks the availability of the given subject assuming that it is a URL.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import URLAvailabilityChecker

            my_subject = "http://example.org"
            the_status = URLAvailabilityChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is available.
            print(f"{my_subject} is available ? {the_status.is_available()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.test may be removed in the future."
        "Please consider using PyFunceble.URLAvailabilityChecker explicitly.",
        DeprecationWarning,
    )

    return URLAvailabilityChecker(subject, **kwargs).get_status()


def is_second_level_domain(subject: str, **kwargs) -> bool:
    """
    Checks if the given subject is a syntactically valid second level domain.

    .. warning::
        This method was added for retrocompatibility.
        It may be removed in the future and is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import SecondLvlDomainSyntaxChecker

            my_subject = "example.org"
            the_status = SecondLvlDomainSyntaxChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is a second level domain.
            print(f"{my_subject} is 2nd level domain ? {the_status.is_valid()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_second_level_domain was added for retro compatibility. "
        "It may be removed in the future."
        "Please consider using PyFunceble.SecondLvlDomainSyntaxChecker explicitly.",
    )

    return SecondLvlDomainSyntaxChecker(subject, **kwargs).is_valid()


def is_domain(subject: str, **kwargs) -> bool:
    """
    Checks if the given subject is a syntactically valid second level domain
    or subdomain.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import DomainSyntaxChecker

            my_subject = "example.org"
            the_status = DomainSyntaxChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is a domain (2nd level or subdomain).
            print(f"{my_subject} is domain ? {the_status.is_valid()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_domain may be removed in the future."
        "Please consider using PyFunceble.DomainSyntaxChecker explicitly.",
        DeprecationWarning,
    )

    return DomainSyntaxChecker(subject, **kwargs).is_valid()


def is_subdomain(subject: str, **kwargs) -> bool:
    """
    Checks if the given subject is a syntactically valid subdomain.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import SubDomainSyntaxChecker

            my_subject = "hello.example.org"
            the_status = SubDomainSyntaxChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is a subdomain.
            print(f"{my_subject} is subdomain ? {the_status.is_valid()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_subdomain may be removed in the future."
        "Please consider using PyFunceble.SubDomainSyntaxChecker explicitly.",
        DeprecationWarning,
    )

    return SubDomainSyntaxChecker(subject, **kwargs).is_valid()


def is_ip(subject: str, **kwargs) -> bool:
    """
    Checks if the given subject is a syntactically valid IP range.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import IPSyntaxChecker

            my_subject = "192.168.0.0"
            the_status = IPSyntaxChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is an IP (v4 or v6).
            print(f"{my_subject} is IP ? {the_status.is_valid()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_ip may be removed in the future."
        "Please consider using PyFunceble.IPSyntaxChecker explicitly.",
        DeprecationWarning,
    )

    return IPSyntaxChecker(subject, **kwargs).is_valid()


def is_ipv4(subject: str, **kwargs) -> bool:
    """
    Checks if the given subject is a syntactically valid IPv4.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import IPSyntaxChecker

            my_subject = "192.168.0.0"
            the_status = IPSyntaxChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is an IPv4.
            print(f"{my_subject} is IPv4 ? {the_status.is_valid_v4()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_ipv4 be removed in the future."
        "Please consider using PyFunceble.IPSyntaxChecker explicitly.",
        DeprecationWarning,
    )

    return IPSyntaxChecker(subject, **kwargs).is_valid_v4()


def is_ipv6(subject: str, **kwargs) -> bool:
    """
    Checks if the given subject is a syntactically valid IPv6.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import IPSyntaxChecker

            my_subject = "192.168.0.0"
            the_status = IPSyntaxChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is an IPv6.
            print(f"{my_subject} is IPv6 ? {the_status.is_valid_v6()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_ipv6 be removed in the future."
        "Please consider using PyFunceble.IPSyntaxChecker explicitly.",
        DeprecationWarning,
    )

    return IPSyntaxChecker(subject, **kwargs).is_valid_v6()


def is_ip_range(subject: str, **kwargs) -> bool:
    """
    Checks if the given subject is a syntactically valid IP range.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import IPSyntaxChecker

            my_subject = "192.168.0.0"
            the_status = IPSyntaxChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is an IP range (v4 or v6).
            print(f"{my_subject} is IP range ? {the_status.is_valid_range()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_ip_range may be removed in the future."
        "Please consider using PyFunceble.IPSyntaxChecker explicitly.",
        DeprecationWarning,
    )

    return IPSyntaxChecker(subject, **kwargs).is_valid_range()


def is_ipv4_range(subject: str, **kwargs) -> bool:
    """
    Checks if the given subject is a syntactically valid IPv4 range.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import IPSyntaxChecker

            my_subject = "192.168.0.0"
            the_status = IPSyntaxChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is IPv4 range.
            print(f"{my_subject} is IPv4 range ? {the_status.is_valid_v4_range()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_ipv4_range may be removed in the future."
        "Please consider using PyFunceble.IPSyntaxChecker explicitly.",
        DeprecationWarning,
    )

    return IPSyntaxChecker(subject, **kwargs).is_valid_v4_range()


def is_ipv6_range(subject: str, **kwargs) -> bool:
    """
    Checks if the given subject is a syntactically valid IPv6 range.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import IPSyntaxChecker

            my_subject = "::1"
            the_status = IPSyntaxChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is IPv6 range.
            print(f"{my_subject} is IPv6 range ? {the_status.is_valid_v6_range()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_ipv6_range may be removed in the future."
        "Please consider using PyFunceble.IPSyntaxChecker explicitly.",
        DeprecationWarning,
    )

    return IPSyntaxChecker(subject, **kwargs).is_valid_v6_range()


def is_url(subject: str, **kwargs) -> bool:
    """
    Checks if the given subject is syntactically a valid URL.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import DomainReputationChecker

            my_subject = "https://example.org"
            the_status = URLSyntaxChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is a URL.
            print(f"{my_subject} is URL ? {the_status.is_valid()}")

    :parma subject:
        The subject to check.
    """

    warnings.warn(
        "PyFunceble.is_url may be removed in the future."
        "Please consider using PyFunceble.URLSyntaxChecker explicitly.",
        DeprecationWarning,
    )

    # pylint: disable=no-member
    return URLSyntaxChecker(subject, **kwargs).get_status().is_valid()


def is_domain_malicious(subject: str, **kwargs) -> bool:
    """
    Checks if the given domain is malicious.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import DomainReputationChecker

            my_subject = "example.org"
            the_status = DomainReputationChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is malicious.
            print(f"{my_subject} is Malicious ? {the_status.is_malicious()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_domain_malicious may be removed in the future."
        "Please consider using PyFunceble.DomainReputationChecker explicitly.",
        DeprecationWarning,
    )

    # pylint: disable=no-member
    return DomainReputationChecker(subject, **kwargs).get_status().is_malicious()


def is_ipv4_malicious(subject: str, **kwargs) -> bool:
    """
    Checks if the given IPv4 is malicious.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import IPReputationChecker

            my_subject = "192.168.0.1"
            the_status = IPReputationChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is malicious.
            print(f"{my_subject} is Malicious ? {the_status.is_malicious()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_ipv4_malicious may be removed in the future."
        "Please consider using PyFunceble.IPReputationChecker explicitly.",
        DeprecationWarning,
    )

    # pylint: disable=no-member
    return IPReputationChecker(subject, **kwargs).get_status().is_malicious()


def is_url_malicious(subject: str, **kwargs) -> bool:
    """
    Checks if the given URL is malicious.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import URLReputationChecker

            my_subject = "https://example.org"
            the_status = URLReputationChecker(
                my_subject
            ).get_status()

            # Get the status in dict format.
            print(the_status.to_dict())

            # Get the status in json format.
            print(the_status.to_json())

            # Check if it is malicious.
            print(f"{my_subject} is Malicious ? {the_status.is_malicious()}")

    :param subject:
        The subject to work with.
    """

    warnings.warn(
        "PyFunceble.is_url_malicious may be removed in the future."
        "Please consider using PyFunceble.URLReputationChecker explicitly.",
        DeprecationWarning,
    )

    # pylint: disable=no-member
    return URLReputationChecker(subject, **kwargs).get_status().is_malicious()


def get_complements(subject: str, include_given: bool = False) -> List[str]:
    """
    Provides the complements of a given subject.

    A complement is a for example :code:`example.org` if :code:`www.example.org`
    is given and vice-versa.

    .. warning::
        This method may be removed in the future.
        It is still available for convenience.

        Please consider the following alternative example:

        ::

            from PyFunceble import Subject2Complements

            my_subject = "example.org"
            complements = Subject2Complements(
                my_subject
            ).get_converted(include_given=True)

    :param subject:
        The subject to work with.

    :param include_given:
        Include the given subject in the result.
    """

    warnings.warn(
        "PyFunceble.get_complements may be removed in the future."
        "Please consider using PyFunceble.Subject2Complements explicitly",
        DeprecationWarning,
    )

    return Subject2Complements(subject, include_given=include_given).get_converted()
