"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the DNS lookup interface.

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

from socket import IPPROTO_TCP, gaierror, getaddrinfo, gethostbyaddr, herror

import dns.resolver
import dns.reversename
from dns.exception import DNSException

import PyFunceble


class DNSLookup:  # pylint: disable=too-few-public-methods
    """
    DNS lookup interface.

    :param str subject: The subject we are working with.
    :param dns_server: The DNS server we are working with.
    :type dns_server: list|tuple|str
    :param int lifetime: Set the lifetime of a query.
    """

    def __init__(self, dns_server=None, lifetime=3, tcp=False):
        self.given_dns_server = dns_server
        self.resolver = self.__get_resolver(dns_server)

        self.update_nameserver(dns_server)
        self.update_lifetime(lifetime)
        self.tcp = tcp

        PyFunceble.LOGGER.debug(
            f"DNS Resolver Nameservers: {self.resolver.nameservers}"
        )
        PyFunceble.LOGGER.debug(
            f"DNS Resolver (Nameservers) Port: {self.resolver.nameserver_ports}"
        )
        PyFunceble.LOGGER.debug(f"DNS Resolver Port: {self.resolver.port}")
        PyFunceble.LOGGER.debug(f"DNS Resolver timeout: {self.resolver.timeout}")
        PyFunceble.LOGGER.debug(f"DNS Resolver lifetime: {self.resolver.lifetime}")
        PyFunceble.LOGGER.debug(f"DNS Resolver over TCP: {self.tcp}")

        PyFunceble.INTERN["dns_lookup"] = {
            "resolver": self.resolver,
            "given_dns_server": dns_server,
        }

    @classmethod
    def __get_resolver(cls, dns_server):
        """
        Provides the configured dns resolver.
        """

        if dns_server:
            # A dns server is given.

            PyFunceble.LOGGER.info(
                "DNS Server explicitly given, generating a new configurable resolver."
            )
            PyFunceble.LOGGER.debug(f"Given DNS server: {dns_server}")

            # We initiate and configure the resolver.
            resolver = dns.resolver.Resolver(configure=False)

            return resolver

        # A dns server is not given.

        PyFunceble.LOGGER.info(
            "DNS Server not explicitly given, providing the systemwide one."
        )

        # We configure everything with what the OS gives us.
        return dns.resolver.Resolver()

    def update_lifetime(self, lifetime):
        """
        Updates the lifetime of a query.
        """

        if isinstance(lifetime, (int, float)):
            if lifetime == self.resolver.timeout:
                self.resolver.lifetime = float(lifetime) + 2.0
            else:
                self.resolver.lifetime = float(lifetime)
        else:
            self.resolver.lifetime = self.resolver.timeout + 2.0

    def update_nameserver(self, nameserver):
        """
        Updates the nameserver to query.
        """

        if nameserver:
            nameserver = (
                [nameserver]
                if not isinstance(nameserver, (list, tuple))
                else nameserver
            )

            self.resolver.nameserver_ports = {
                z: y
                for x, y in self.__get_server_and_port_from(nameserver)
                for z in self.__get_dns_servers_from(x)
            }

            self.resolver.nameservers = list(self.resolver.nameserver_ports.keys())

            PyFunceble.LOGGER.info(
                f"Switched Resolver nameserver to: {self.resolver.nameservers}"
            )
            PyFunceble.LOGGER.info(
                f"Switched Resolver nameserver port to: {self.resolver.nameserver_ports}"
            )

    def __get_server_and_port_from(self, inputed_dns):  # pragma: no cover
        """
        Given a list or an input representing dns server,
        we split the server from the port.

        :param inputed_dns: The inputed DNS server(s).
        :type input: str, list, tuple

        :return:
            A tuple with:

            (The DNS, the port)
        :rtype: tuple
        """

        if isinstance(inputed_dns, (list, tuple)):
            result = []

            for dns_server in inputed_dns:
                result.append(self.__get_server_and_port_from(dns_server))

            return result

        if ":" in inputed_dns:
            splited = inputed_dns.split(":")

            if len(splited) > 1 and splited[-1] and splited[-1].isdigit():
                return ":".join(splited[:-1]), int(splited[-1])

            if not splited[-1]:
                return ":".join(splited[:-1]), 53

        return inputed_dns, 53

    def __get_dns_servers_from(self, inputed_dns):  # pragma: no cover
        """
        Given a list or an input representing dns servers,
        we ensure that we have a list of a string which
        represent an IP.

        :param input: The inputed DNS server(s).
        :type input: str, list, tuple

        :return: The list of dns server to use.
        :rtype: list
        """

        if isinstance(inputed_dns, (list, tuple)):
            result = []
            for dns_server in inputed_dns:
                result.extend(self.__get_dns_servers_from(dns_server))

            return result

        result = []

        try:
            if PyFunceble.Check(inputed_dns).is_domain():
                result.extend(
                    [x.address for x in dns.resolver.Resolver().query(inputed_dns)]
                )
            else:
                result.append(inputed_dns)
        except DNSException:
            result.extend(dns.resolver.get_default_resolver().nameservers)

        return result

    def a_record(self, subject, tcp=None):
        """
        Return the A record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param bool tcp: Tell us to use TCP for query.

        :return: A list of A record(s).
        :rtype: list, None
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        if tcp is None:
            tcp = self.tcp

        PyFunceble.LOGGER.debug(f"Query over TCP: {self.tcp}")

        try:
            PyFunceble.LOGGER.info(f"Getting A record of {repr(subject)}")
            # We get the A record of the given subject.
            result = [str(x) for x in self.resolver.query(subject, "A", tcp=tcp)]
            PyFunceble.LOGGER.info(f"Could get A record of {repr(subject)}: {result}")

            return result
        except DNSException:
            PyFunceble.LOGGER.error(f"Could not get A record of {repr(subject)}")

        return None

    def aaaa_record(self, subject, tcp=None):
        """
        Return the AAAA record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param bool tcp: Tell us to use TCP for query.

        :return: A list of A record(s).
        :rtype: list, None
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        if tcp is None:
            tcp = self.tcp

        PyFunceble.LOGGER.debug(f"Query over TCP: {self.tcp}")

        try:
            PyFunceble.LOGGER.info(f"Getting AAAA record of {repr(subject)}")
            # We get the A record of the given subject.
            result = [str(x) for x in self.resolver.query(subject, "AAAA", tcp=tcp)]
            PyFunceble.LOGGER.info(
                f"Could get AAAA record of {repr(subject)}: {result}"
            )

            return result
        except DNSException:
            PyFunceble.LOGGER.error(f"Could not get AAAA record of {repr(subject)}")

        return None

    def cname_record(self, subject, tcp=None):
        """
        Return the CNAME record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param bool tcp: Tell us to use TCP for query.

        :return: A list of CNAME record(s).
        :rtype: list, None
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        if tcp is None:
            tcp = self.tcp

        PyFunceble.LOGGER.debug(f"Query over TCP: {self.tcp}")

        try:
            PyFunceble.LOGGER.info(f"Getting CNAME record of {repr(subject)}")
            # We get the A record of the given subject.
            result = [str(x) for x in self.resolver.query(subject, "CNAME", tcp=tcp)]
            PyFunceble.LOGGER.info(
                f"Could get CNAME record of {repr(subject)}: {result}"
            )

            return result
        except DNSException:
            PyFunceble.LOGGER.error(f"Could not get CNAME record of {repr(subject)}")

        return None

    def dname_record(self, subject, tcp=None):  # pragma: no cover
        """
        Return the DNAME record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param bool tcp: Tell us to use TCP for query.

        :return: A list of DNAME record(s).
        :rtype: list, None
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        if tcp is None:
            tcp = self.tcp

        PyFunceble.LOGGER.debug(f"Query over TCP: {self.tcp}")

        try:
            PyFunceble.LOGGER.info(f"Getting DNAME record of {repr(subject)}")
            # We get the A record of the given subject.
            result = [str(x) for x in self.resolver.query(subject, "DNAME", tcp=tcp)]
            PyFunceble.LOGGER.info(
                f"Could get DNAME record of {repr(subject)}: {result}"
            )

            return result
        except DNSException:
            PyFunceble.LOGGER.error(f"Could not get DNAME record of {repr(subject)}")

        return None

    def mx_record(self, subject, tcp=None):
        """
        Return the MX record of the given subject (if found).

        :param str subject: The subject we are working with.

        :return: A list of MX record(s).
        :rtype: list, None
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        if tcp is None:
            tcp = self.tcp

        PyFunceble.LOGGER.debug(f"Query over TCP: {self.tcp}")

        try:
            PyFunceble.LOGGER.info(f"Getting MX record of {repr(subject)}")
            # We get the MX record of the given subject.
            result = [str(x) for x in self.resolver.query(subject, "MX", tcp=tcp)]

            PyFunceble.LOGGER.info(f"Could get MX record of {repr(subject)}: {result}")

            return result
        except DNSException:
            PyFunceble.LOGGER.error(f"Could not get MX record of {repr(subject)}")

        return None

    def ns_record(self, subject, tcp=None):
        """
        Return the NS record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param bool tcp: Tell us to use TCP for query.

        :return: A list of NS record(s).
        :rtype: list, None
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        if tcp is None:
            tcp = self.tcp

        PyFunceble.LOGGER.debug(f"Query over TCP: {self.tcp}")

        try:
            PyFunceble.LOGGER.info(f"Getting NS record of {repr(subject)}")
            # We get the NS record of the given subject.
            result = [str(x) for x in self.resolver.query(subject, "NS", tcp=tcp)]
            PyFunceble.LOGGER.info(f"Could get NS record of {repr(subject)}: {result}")

            return result
        except DNSException:
            PyFunceble.LOGGER.error(f"Could not get NS record of {repr(subject)}")

        return None

    def txt_record(self, subject, tcp=None):
        """
        Return the TXT record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param bool tcp: Tell us to use TCP for query.

        :return: A list of TXT record(s).
        :rtype: list, None
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        if tcp is None:
            tcp = self.tcp

        PyFunceble.LOGGER.debug(f"Query over TCP: {self.tcp}")

        try:
            PyFunceble.LOGGER.info(f"Getting TXT record of {repr(subject)}")
            # We get the TXT record of the given subject.
            result = [str(x) for x in self.resolver.query(subject, "TXT", tcp=tcp)]
            PyFunceble.LOGGER.info(f"Could get TXT record of {repr(subject)}: {result}")

            return result
        except DNSException:
            PyFunceble.LOGGER.error(f"Could not get TXT record of {repr(subject)}")

        return None

    def ptr_record(self, subject, reverse_name=True, tcp=None):
        """
        Return the PTR record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param bool tcp: Tell us to use TCP for query.

        :return: A list of PTR record(s).
        :rtype: list, None
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        if tcp is None:
            tcp = self.tcp

        PyFunceble.LOGGER.debug(f"Query over TCP: {self.tcp}")

        try:
            PyFunceble.LOGGER.info(f"Getting TXT record of {repr(subject)}")
            if reverse_name:
                # We get the reverse name we are going to request.
                to_request = dns.reversename.from_address(subject)
            else:
                to_request = subject

            # We get the PTR record of the currently read A record.
            result = [str(x) for x in self.resolver.query(to_request, "PTR", tcp=tcp)]
            PyFunceble.LOGGER.info(f"Could get PTR record of {repr(subject)}: {result}")

            return result
        except DNSException:
            PyFunceble.LOGGER.error(f"Could not get PTR record of {repr(subject)}")

        return None

    @classmethod
    def get_addr_info(cls, subject):  # pragma: no cover
        """
        Get and return the information of the given subject (address).

        :param str subject: The subject we are working with.

        :return: A list of address.
        :rtype: list, None
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        try:  # pragma: no cover
            # We request the address information.
            req = getaddrinfo(subject, 80, proto=IPPROTO_TCP)

            # We format the addr infos.
            return [x[-1][0] for x in req]
        except (gaierror, OSError, herror, UnicodeError):
            pass

        return None

    @classmethod
    def get_host_by_addr(cls, subject):  # pragma: no cover
        """
        Get and return the host of the given subject (address).

        :param str subject: The subject we are working with.

        :return:
            A dict in the following format or :code:`None`.

            ::

                {
                    "hostname": "",
                    "aliases": [],
                    "ips": []
                }

        :rtype: dict, None
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        try:
            # We get the host by addr.
            req = gethostbyaddr(subject)

            # And we format the result.
            return {"hostname": req[0], "aliases": req[1], "ips": req[2]}

        except (gaierror, OSError, herror):
            pass

        return None

    @classmethod
    def is_record_present_in_result(cls, to_check, result, allow_empty=False):
        """
        Checks if the given record type is in the result.

        :param to_check:
            The record to check the presence.
        :type to_check: list, str, tuple
        :param dict result:
            The result to work with.
        :param bool allow_empty:
            Tell to if we allow and empty result as present.

        :rtype: bool
        """

        if isinstance(to_check, (list, tuple)):
            return any(
                [
                    cls.is_record_present_in_result(x, result, allow_empty=allow_empty)
                    for x in to_check
                ]
            )

        if to_check in result:
            if not allow_empty and not result[to_check]:
                PyFunceble.LOGGER.debug(
                    f"{to_check} record is not in result:\n{result}"
                )
                return False
            PyFunceble.LOGGER.debug(f"{to_check} record is in result:\n{result}")
            return True
        PyFunceble.LOGGER.debug(f"{to_check} record is not in result:\n{result}")
        return False

    def __request_complete_not_ip(self, subject, tcp=None):  # pragma: no cover
        """
        Requests and provides the complete DNS spectrum.

        :rtype: dict
        """

        result = {}

        # We get the A record of the given subject.
        result["A"] = self.a_record(subject, tcp=tcp)

        # We get the AAAA record of the given subject.
        result["AAAA"] = self.aaaa_record(subject, tcp=tcp)

        # We get the CNAME record of the given subject.
        result["CNAME"] = self.cname_record(subject, tcp=tcp)

        # We get the DNAME record of the given subject.
        result["DNAME"] = self.dname_record(subject, tcp=tcp)

        # We get the MX record of the given subject.
        result["MX"] = self.mx_record(subject, tcp=tcp)

        # We get the TXT record of the given subject.
        result["TXT"] = self.txt_record(subject, tcp=tcp)

        if self.is_record_present_in_result("A", result):
            # We could get some A record(s).

            # We initiate the PTR.
            result["PTR"] = []

            for a_result in result["A"]:
                # We loop through the list of A records.

                if "." not in a_result:  # pragma: no cover
                    # There is no "." in the currently
                    # read A record.

                    # We continue the loop.
                    continue

                try:
                    # We get the PTR record of the currently read A record.
                    result["PTR"].extend(self.ptr_record(a_result, tcp=tcp))
                except TypeError:  # pragma: no cover
                    pass

            if not all(result["PTR"]):  # pragma: no cover
                # No PTR record was found.

                # We delete the PTR entry.
                del result["PTR"]

        return result

    def __request_not_ip(self, subject, complete=False, tcp=None):  # pragma: no cover
        """
        Handle the request for a subject which is not an IP.

        :rtype: dict
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        if tcp is None:
            tcp = self.tcp

        PyFunceble.LOGGER.debug(f"{repr(subject)} is not IP. Requesting record.")

        result = {}

        # We get the NS record of the given subject.
        result["NS"] = self.ns_record(subject, tcp=tcp)

        if complete:  # pragma: no cover
            result = PyFunceble.helpers.Merge(
                self.__request_complete_not_ip(subject, tcp=tcp)
            ).into(result)

        if not self.is_record_present_in_result(["CNAME", "NS"], result):
            # As sometime we may not have a NS but a CNAME, we handle that case.
            result["CNAME"] = self.cname_record(subject, tcp=tcp)

        if not self.is_record_present_in_result(["CNAME", "DNAME", "NS"], result):
            # Same but with DNAME.
            result["DNAME"] = self.dname_record(subject, tcp=tcp)

        if not self.is_record_present_in_result(["A", "CNAME", "DNAME", "NS"], result):
            # Same but with A.
            result["A"] = self.a_record(subject, tcp=tcp)

        if not self.is_record_present_in_result(
            ["A", "AAAA", "CNAME", "DNAME", "NS"], result
        ):
            # Same but with A.
            result["AAAA"] = self.aaaa_record(subject, tcp=tcp)

        # We get the list of index to delete.
        to_delete = [x for x in result if not result[x]]

        for index in to_delete:
            # We loop through the list of index to delete.

            # And we delete them.
            del result[index]

        if not result and complete:  # pragma: no cover
            # We could not get DNS records about the given subject.

            # We get the addr infos.
            result["addr_info"] = self.get_addr_info(subject)

            if not result["addr_info"]:
                # The addr_info index is empty.

                # We delete it.
                del result["addr_info"]
        elif result:
            result["nameservers"] = self.resolver.nameservers

        PyFunceble.LOGGER.debug(
            f"Records for {repr(subject)} (with {self.resolver.nameservers}):\n{result}"
        )

        return result

    def __request_ip(self, subject, tcp=None):  # pragma: no cover
        """
        Handle the request for a subject which is an IP.

        :param str subject: The subject we are working with.
        :param bool tcp: Tell us to use TCP for query.

        :rtype: dict
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        if tcp is None:
            tcp = self.tcp

        PyFunceble.LOGGER.info(f"{repr(subject)} is an IP. Requesting PTR record.")

        result = {}

        # We get the PTR record of the given subject.
        result["PTR"] = self.ptr_record(subject, tcp=tcp)

        if "PTR" not in result or not result["PTR"]:
            del result["PTR"]

            PyFunceble.LOGGER.error(f"PTR record for {repr(subject)} not found.")
        elif result["PTR"]:
            result["nameservers"] = self.resolver.nameservers

        if not result:
            # We could not get DNS records about the given subject.

            PyFunceble.LOGGER.info(f"Getting hosts by addr for {repr(subject)}")

            result = self.get_host_by_addr(subject)

        PyFunceble.LOGGER.debug(f"Request result: \n{result}")

        return result

    def request(self, subject, complete=False, tcp=None):  # pragma: no cover
        """
        Perform a DNS lookup/requests.

        :param str subject: The subject we are working with.
        :param bool complete: Tell us to return as many result as possible.
        :param bool tcp: Tell us to use TCP for query.

        :return:
            A dict with following index if the given subject is not registered into the
            given DNS server. (More likely local subjects).

                ::

                    {
                        "hostname": "",
                        "aliases": [],
                        "ips": []
                    }

            A dict with following index for everything else (and if found).

                ::

                    {
                        "nameservers: [],
                        "A": [],
                        "AAAA": [],
                        "CNAME": [],
                        "DNAME": [],
                        "MX": [],
                        "NS": [],
                        "TXT": [],
                        "PTR": []
                    }

        :rtype: dict
        :raise ValueError: When a non string :code:`subject` is given.
        """

        if not subject or not isinstance(subject, str):
            raise ValueError(f"<subject> must be of type {str} and not empty.")

        if tcp is None:
            tcp = self.tcp

        result = {}

        if not PyFunceble.Check(subject).is_ip():
            # We are looking for something which is not an IPv4 or IPv6.

            temp_result = self.__request_not_ip(subject, complete=complete, tcp=tcp)

            if isinstance(temp_result, dict):
                result.update(temp_result)
        else:
            # We are working with something which is an IPv4 or IPv6.

            temp_result = self.__request_ip(subject, tcp=tcp)

            if isinstance(temp_result, dict):
                result.update(temp_result)

        return result
