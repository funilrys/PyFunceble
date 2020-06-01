"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the syntax checker interface.

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

from ipaddress import (
    AddressValueError,
    IPv4Address,
    IPv6Address,
    ip_address,
    ip_interface,
    ip_network,
)

from domain2idna import get as domain2idna

import PyFunceble


class Check:
    """
    Provides our syntax checkers.

    :param str subject: The subject (URL, IP or domain) to check.
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

    def __init__(self, subject):
        self.subject = subject

        if (
            self.subject.startswith("*.")
            and PyFunceble.CONFIGURATION.wildcard
            and PyFunceble.CONFIGURATION.syntax
        ):
            self.subject = self.subject[2:]

    def is_url(
        self, return_base=False, return_formatted=False
    ):  # pylint: disable=too-many-branches
        """
        Checks if the given subject is a valid URL.

        :param bool return_base:
            Allow us the return of the url base (if URL formatted correctly).

        :param bool return_formatted:
            Allow us to get the formatted URL as response.

        :return: The validity or the base if asked.
        :rtype: bool, str
        """

        # We initiate a variable which will save the initial base in case
        # we have to convert the base to IDNA.
        initial_base = None

        if self.subject.startswith("http"):
            # The element to test starts with http.

            try:
                # We initiate a regex which will match the domain or the url base.
                regex = r"(^(http:\/\/|https:\/\/)(.+?(?=\/)|.+?$))"

                # We extract the url base with the help of the initiated regex.
                initial_base = base = PyFunceble.helpers.Regex(regex).match(
                    self.subject, return_match=True, rematch=True
                )[2]

                if PyFunceble.CONFIGURATION.idna_conversion:
                    # We have to convert the domain to IDNA.

                    # We convert the initial base to IDNA.
                    base = domain2idna(base)

                if ":" in base:
                    # The port is explicitly given.

                    # We remove it from the base.
                    splited_base = base.split(":")
                else:
                    splited_base = None

                if splited_base:
                    # We check if the url base is a valid domain.
                    domain_status = Check(splited_base[0]).is_domain()

                    # We check if the url base is a valid IP.
                    ip_status = Check(splited_base[0]).is_ip()
                else:
                    # We check if the url base is a valid domain.
                    domain_status = Check(base).is_domain()

                    # We check if the url base is a valid IP.
                    ip_status = Check(base).is_ip()

                if domain_status or ip_status:
                    # * The url base is a valid domain.
                    # and
                    # * The url base is a valid IP.

                    if splited_base:
                        initial_base = base = splited_base[0]

                    if PyFunceble.CONFIGURATION.idna_conversion and return_formatted:
                        # * We have to convert to IDNA.
                        # and
                        # * We have to return the converted full URL.

                        # We return the converted full URL.
                        return PyFunceble.helpers.Regex(
                            initial_base, escape=True
                        ).replace_match(self.subject, base, occurences=1)

                    if return_formatted:
                        # * We do not have to convert to IDNA.
                        # but
                        # * We have to return the full URL.

                        # We return the initially given URL.
                        return self.subject

                    if return_base:
                        # We have to return the base of the URL.

                        # We return the base of the URL.
                        return base

                    # We return True.
                    return True
            except TypeError:
                pass

        if return_formatted:
            # We have to return an URL.

            # We return the initily given URL.
            return self.subject

        # We return False.
        return False

    def is_domain(
        self, subdomain_check=False
    ):  # pylint:disable=too-many-return-statements, too-many-branches
        """
        Checks if the given subject is a valid domain.

        :param bool subdomain_check:
            Activates the subdomain checking.

            .. warning::
                Do not manually use.

                Please report to :py:func:`~PyFunceble.check.Check.is_subdomain`.

        :return: The validity.
        :rtype: bool
        """

        # We initate our regex which will match for valid domains.
        regex_valid_domains = r"^(?=.{0,253}$)(([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9])\.)+((?=.*[^0-9])([a-z0-9][a-z0-9-]{0,61}[a-z0-9](?:\.)?|[a-z0-9](?:\.)?))$"  # pylint: disable=line-too-long

        # We initiate our regex which will match for valid subdomains.
        regex_valid_subdomains = r"^(?=.{0,253}$)(([a-z0-9_][a-z0-9-_]{0,61}[a-z0-9_-]|[a-z0-9])\.)+((?=.*[^0-9])([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9]))$"  # pylint: disable=line-too-long

        try:
            # We get the position of the last point.
            last_point_index = self.subject.rindex(".")
            # And with the help of the position of the last point, we get the domain extension.
            extension = self.subject[last_point_index + 1 :]

            if not extension and self.subject.endswith("."):
                try:
                    extension = [x for x in self.subject.split(".") if x][-1]
                except IndexError:
                    pass

            if not extension or (
                extension not in PyFunceble.IANALOOKUP
                and extension not in self.SPECIAL_USE_DOMAIN_NAMES_EXTENSIONS
            ):
                # * The extension is not found.
                # or
                # * The extension is not into the IANA database.
                # or
                # * The extension is not into our mapping of
                #   the "Special-Use Domain Names" specification.

                # We return false.
                return False

            if (
                PyFunceble.helpers.Regex(regex_valid_domains).match(
                    self.subject, return_match=False
                )
                and not subdomain_check
            ):
                # * The element pass the domain validation.
                # and
                # * We are not checking if it is a subdomain.

                # We return True. The domain is valid.
                return True

            # The element did not pass the domain validation. That means that
            # it has invalid character or the position of - or _ are not right.

            if extension in PyFunceble.PSLOOOKUP:
                # The extension is into the psl database.

                for suffix in PyFunceble.PSLOOOKUP[extension]:
                    # We loop through the element of the extension into the psl database.

                    try:
                        # We try to get the position of the currently read suffix
                        # in the element ot test.
                        suffix_index = self.subject.rindex("." + suffix)

                        # We get the element to check.
                        # The idea here is to delete the suffix, then retest with our
                        # subdomains regex.
                        to_check = self.subject[:suffix_index]

                        if "." not in to_check and subdomain_check:
                            # * There is no point into the new element to check.
                            # and
                            # * We are checking if it is a subdomain.

                            # We return False, it is not a subdomain.
                            return False

                        if "." in to_check and subdomain_check:
                            # * There is a point into the new element to check.
                            # and
                            # * We are checking if it is a subdomain.

                            # We return True, it is a subdomain.
                            return True

                        # We are not checking if it is a subdomain.

                        if "." in to_check:
                            # There is a point into the new element to check.

                            # We check if it passes our subdomain regex.
                            # * True: It's a valid domain.
                            # * False: It's an invalid domain.
                            return PyFunceble.helpers.Regex(
                                regex_valid_subdomains
                            ).match(to_check, return_match=False)

                    except ValueError:
                        # In case of a value error because the position is not found,
                        # we continue to the next element.
                        pass

            # * The extension is not into the psl database.
            # or
            # * there was no point into the suffix checking.

            # We get the element before the last point.
            to_check = self.subject[:last_point_index]

            if "." in to_check and subdomain_check:
                # * There is a point in to_check.
                # and
                # * We are checking if it is a subdomain.

                # We return True, it is a subdomain.
                return True

            # We are not checking if it is a subdomain.

            if "." in to_check:
                # There is a point in to_check.

                # We check if it passes our subdomain regex.
                # * True: It's a valid domain.
                # * False: It's an invalid domain.
                return PyFunceble.helpers.Regex(regex_valid_subdomains).match(
                    to_check, return_match=False
                )

        except (ValueError, AttributeError):
            # In case of a value or attribute error we ignore them.
            pass

        # And we return False, the domain is not valid.
        return False

    def is_subdomain(self):
        """
        Checks if the given subject is a valid subdomain.

        :return: The validity.
        :rtype: bool
        """

        # We return the status of the check.
        return self.is_domain(subdomain_check=True)

    def is_ip(self):
        """
        Checks if the given subject is a valid IPv4 or IPv6.

        :return: The validity.
        :rtype: bool
        """

        return self.is_ipv4() or self.is_ipv6()

    def is_ipv4(self):
        """
        Checks if the given subject is a valid IPv4.

        :return: The validity.
        :rtype: bool
        """

        try:
            try:
                return ip_address(self.subject).version == 4
            except ValueError:
                try:
                    return ip_interface(self.subject).version == 4
                except ValueError:
                    return ip_network(self.subject, strict=False).version == 4
        except ValueError:
            return False

    def is_ipv6(self):
        """
        Checks if the given subject is a valid IPv6.

        :return: The validity.
        :rtype: bool
        """

        try:
            try:
                return ip_address(self.subject).version == 6
            except ValueError:
                try:
                    return ip_interface(self.subject).version == 6
                except ValueError:
                    return ip_network(self.subject, strict=False).version == 6
        except ValueError:
            return False

    def is_ip_range(self):  # pragma: no cover
        """
        Checks if the given subject is a valid IPv4 or IPv6 range.

        :return: The validity.
        :rtype: bool
        """

        return self.is_ipv4_range() or self.is_ipv6_range()

    def is_ipv4_range(self):
        """
        Checks if the given subject is a valid IPv4 range.

        :return: The validity.
        :rtype: bool
        """

        if self.is_ipv4():
            if "/" in self.subject:
                block = int(self.subject.split("/")[-1])

                return 0 <= block <= 32
        return False

    def is_ipv6_range(self):
        """
        Checks if the given subject is a valid IPv6 range.

        :return: The validity.
        :rtype: bool
        """

        if self.is_ipv6():
            if "/" in self.subject:
                block = int(self.subject.split("/")[-1])

                return 0 <= block <= 128
        return False

    def is_reserved_ip(self):  # pragma: no cover
        """
        Checks if the given subject is a reserved IPv4 or IPv6.

        :return: The validity.
        :rtype: bool
        """

        return self.is_reserved_ipv4() or self.is_reserved_ipv6()

    # pylint: disable=line-too-long
    def is_reserved_ipv4(self):
        """
        Checks if the given subject is a reserved IPv4.

        .. note::
            This method has been written on basis of the following links:

            * https://en.wikipedia.org/wiki/Reserved_IP_addresses

            * https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml

        :return: The validity.
        :rtype: bool
        """

        if self.is_ipv4():
            # We are working with an IPv4.

            # We list the regex which matched everything.
            reserved = [
                # Match 0.0.0.0–0.255.255.255
                r"(0\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 10.0.0.0–10.255.255.255
                r"(10\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 100.64.0.0–100.127.255.255
                r"(100\.(0?6[4-9]|0?[7-9][0-9]|1[0-1][0-9]|12[0-7])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 127.0.0.0–127.255.255.255
                r"(127\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 169.254.0.0–169.254.255.255
                r"(169\.254\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 172.16.0.0–172.31.255.255
                r"(172\.(0?1[6-9]|0?2[0-9]|0?3[0-1])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 192.0.0.0–192.0.0.255
                r"(192\.0\.0\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 192.0.2.0–192.0.2.255
                r"(192\.0\.2\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 192.31.196.0–192.31.196.255
                r"(192\.31\.196\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 192.52.193.0–192.52.193.255
                r"(192\.52\.193\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 192.88.99.0–192.88.99.255
                r"(192\.88\.99\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 192.168.0.0–192.168.255.255
                r"(192\.168\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 192.175.48.0-192.175.48.255
                r"(192\.175\.48\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))",
                # Match 198.18.0.0–198.19.255.255
                r"(198\.(0?1[8-9])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 198.51.100.0–198.51.100.255
                r"(198\.51\.100\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 203.0.113.0–203.0.113.255
                r"(203\.0\.113\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 224.0.0.0–239.255.255.255
                r"((22[4-9]|23[0-9])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 240.0.0.0–255.255.255.254
                r"((24[0-9]|25[0-5])\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,}))",  # pylint: disable=line-too-long
                # Match 255.255.255.255
                r"(255\.255\.255\.255)",  # pylint: disable=line-too-long
            ]

            # We get a single regex out of the list of regex.
            reserved_regex = "({0})".format("|".join(reserved))

            try:
                address = IPv4Address(self.subject)

                # We check if it passes our regex.
                # * True: It's reserved.
                # * False: It's not reserved.
                return (
                    address.is_multicast
                    or address.is_private
                    or address.is_unspecified
                    or address.is_reserved
                    or address.is_loopback
                    or address.is_link_local
                    or not address.is_global
                    or PyFunceble.helpers.Regex(reserved_regex).match(
                        self.subject, return_match=False
                    )
                )
            except AddressValueError:  # pragma: no cover
                return PyFunceble.helpers.Regex(reserved_regex).match(
                    self.subject, return_match=False
                )

        # We return False, we are not working with an IPv4
        return False

    def is_reserved_ipv6(self):
        """
        Checks if the given subject is a reserved IPv6.

        :return: The validity.
        :rtype: bool
        """

        if self.is_ipv6():
            try:
                address = IPv6Address(self.subject)

                return (
                    address.is_multicast
                    or address.is_private
                    or address.is_unspecified
                    or address.is_reserved
                    or address.is_loopback
                    or address.is_link_local
                    or not address.is_global
                )
            except AddressValueError:
                pass
        return False
