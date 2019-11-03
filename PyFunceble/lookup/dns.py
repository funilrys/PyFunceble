# pylint:disable=line-too-long
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


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long

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
        if dns_server:
            # A dns server is given.

            PyFunceble.LOGGER.info(f"DNS Server explicitly given, using the given one.")
            PyFunceble.LOGGER.debug(f"Given DNS server: {dns_server}")

            # We initiate the default resolver.
            self.dns_resolver = dns.resolver.Resolver(configure=False)

            # We set the nameservers.
            self.dns_resolver.nameservers = self.__get_dns_servers_from(dns_server)
        else:
            # A dns server is not given.

            PyFunceble.LOGGER.info(
                f"DNS Server not explicitly given, using the systemwide one."
            )

            # We configure everything with what the OS gives us.
            self.dns_resolver = dns.resolver.Resolver()

        self.update_lifetime(lifetime)
        self.tcp = tcp

        PyFunceble.LOGGER.debug(
            f"DNS Resolver Nameservers: {self.dns_resolver.nameservers}"
        )
        PyFunceble.LOGGER.debug(f"DNS Resolver timeout: {self.dns_resolver.timeout}")
        PyFunceble.LOGGER.debug(f"DNS Resolver lifetime: {self.dns_resolver.lifetime}")
        PyFunceble.LOGGER.debug(f"DNS Resolver over TCP: {self.tcp}")

        PyFunceble.INTERN["dns_lookup"] = {
            "resolver": self.dns_resolver,
            "given_dns_server": dns_server,
        }

    def update_lifetime(self, lifetime):
        """
        Updates the lifetime of a query.
        """

        if isinstance(lifetime, (int, float)):
            if lifetime == self.dns_resolver.timeout:
                self.dns_resolver.lifetime = float(lifetime) + 2.0
            else:
                self.dns_resolver.lifetime = float(lifetime)
        else:
            self.dns_resolver.lifetime = self.dns_resolver.timeout + 2.0

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
            result = [str(x) for x in self.dns_resolver.query(subject, "A", tcp=tcp)]
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
            result = [str(x) for x in self.dns_resolver.query(subject, "AAAA", tcp=tcp)]
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
            result = [
                str(x) for x in self.dns_resolver.query(subject, "CNAME", tcp=tcp)
            ]
            PyFunceble.LOGGER.info(
                f"Could get CNAME record of {repr(subject)}: {result}"
            )

            return result
        except DNSException:
            PyFunceble.LOGGER.error(f"Could not get CNAME record of {repr(subject)}")

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
            result = [str(x) for x in self.dns_resolver.query(subject, "MX", tcp=tcp)]

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
            result = [str(x) for x in self.dns_resolver.query(subject, "NS", tcp=tcp)]
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
            result = [str(x) for x in self.dns_resolver.query(subject, "TXT", tcp=tcp)]
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
            result = [
                str(x) for x in self.dns_resolver.query(to_request, "PTR", tcp=tcp)
            ]
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

            # We get the A record of the given subject.
            result["A"] = self.a_record(subject, tcp=tcp)

            # We get the AAAA record of the given subject.
            result["AAAA"] = self.aaaa_record(subject, tcp=tcp)

            # We get the CNAME record of the given subject.
            result["CNAME"] = self.cname_record(subject, tcp=tcp)

            # We get the MX record of the given subject.
            result["MX"] = self.mx_record(subject, tcp=tcp)

            # We get the TXT record of the given subject.
            result["TXT"] = self.txt_record(subject, tcp=tcp)

            if "A" in result and result["A"]:
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

        PyFunceble.LOGGER.debug(f"Records for {repr(subject)}:\n{result}")

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
                        "A": [],
                        "AAAA": [],
                        "CNAME": [],
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
