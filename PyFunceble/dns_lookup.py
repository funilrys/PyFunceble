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

This submodule will provide the DNS lookup interface.

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

from PyFunceble.check import Check
from PyFunceble.logger import Logger


class DNSLookup:  # pylint: disable=too-few-public-methods
    """
    DNS lookup interface.

    :param str subject: The subject we are working with.
    :param dns_server: The DNS server we are working with.
    :type dns_server: list|tuple|str
    :param int lifetime: Set the lifetime of a query.
    """

    def __init__(self, subject, dns_server=None, complete=False, lifetime=3):
        if subject:
            if isinstance(subject, str):
                self.subject = subject
            else:
                raise ValueError("{0} expected".format(type(subject)))

            if dns_server:
                # A dns server is given.

                Logger().info(f"DNS Server explicitly given, using the given one.")
                Logger().debug(f"Given DNS server: {dns_server}")

                # We initiate the default resolver.
                self.dns_resolver = dns.resolver.Resolver(configure=False)

                # We set the nameservers.
                self.dns_resolver.nameservers = self.__get_dns_servers_from(dns_server)
            else:
                # A dns server is not given.

                Logger().info(
                    f"DNS Server not explicitly given, using the systemwide one."
                )

                # We configure everything with what the OS gives us.
                self.dns_resolver = dns.resolver.Resolver()

            # We set the timeout
            self.dns_resolver.timeout = lifetime
            self.dns_resolver.lifetime = lifetime

            Logger().debug(f"DNS Resolver Nameservers: {self.dns_resolver.nameservers}")
            Logger().debug(f"DNS Resolver timeout: {self.dns_resolver.timeout}")
            Logger().debug(f"DNS Resolver lifetime: {self.dns_resolver.lifetime}")

            self.complete = complete

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
        checker = Check(inputed_dns)

        try:
            if checker.is_domain():
                result.extend(
                    [x.address for x in dns.resolver.Resolver().query(inputed_dns)]
                )
            else:
                result.append(inputed_dns)
        except DNSException:
            result.append(inputed_dns)

        return result

    def a_record(self, subject=None, lifetime=3.0):  # pragma: no cover
        """
        Return the A record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param float lifetime: The number of second before timeout.

        :return: A list of A record(s).
        :rtype: list
        """

        if not subject:
            subject = self.subject

        try:
            # We get the A record of the given subject.
            return [
                str(x) for x in self.dns_resolver.query(subject, "A", lifetime=lifetime)
            ]
        except DNSException:
            pass

        return None

    def aaaa_record(self, subject=None, lifetime=3.0):  # pragma: no cover
        """
        Return the AAAA record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param float lifetime: The number of second before timeout.

        :return: A list of A record(s).
        :rtype: list
        """

        if not subject:
            subject = self.subject

        try:
            # We get the A record of the given subject.
            return [
                str(x)
                for x in self.dns_resolver.query(subject, "AAAA", lifetime=lifetime)
            ]
        except DNSException:
            pass

        return None

    def cname_record(self, subject=None, lifetime=3.0):  # pragma: no cover
        """
        Return the CNAME record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param float lifetime: The number of second before timeout.

        :return: A list of CNAME record(s).
        :rtype: list
        """

        if not subject:
            subject = self.subject

        try:
            # We get the A record of the given subject.
            return [
                str(x)
                for x in self.dns_resolver.query(subject, "CNAME", lifetime=lifetime)
            ]
        except DNSException:
            pass

        return None

    def mx_record(self, subject=None, lifetime=3.0):  # pragma: no cover
        """
        Return the MX record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param float lifetime: The number of second before timeout.

        :return: A list of MX record(s).
        :rtype: list
        """

        if not subject:
            subject = self.subject

        try:
            # We get the MX record of the given subject.
            return [
                str(x)
                for x in self.dns_resolver.query(subject, "MX", lifetime=lifetime)
            ]
        except DNSException:
            pass

        return None

    def ns_record(self, subject=None, lifetime=3.0):
        """
        Return the NS record of the given subject (if found).

        :param str subject: The subject we are working with.
         :param float lifetime: The number of second before timeout.

        :return: A list of NS record(s).
        :rtype: list
        """

        if not subject:
            subject = self.subject

        try:
            # We get the NS record of the given subject.
            return [
                str(x)
                for x in self.dns_resolver.query(subject, "NS", lifetime=lifetime)
            ]
        except DNSException:
            pass

        return None

    def txt_record(self, subject=None, lifetime=3.0):  # pragma: no cover
        """
        Return the TXT record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param float lifetime: The number of second before timeout.

        :return: A list of TXT record(s).
        :rtype: list
        """

        if not subject:
            subject = self.subject

        try:
            # We get the TXT record of the given subject.
            return [
                str(x)
                for x in self.dns_resolver.query(subject, "TXT", lifetime=lifetime)
            ]
        except DNSException:
            pass

        return None

    def ptr_record(self, subject=None, reverse_name=True, lifetime=3.0):
        """
        Return the PTR record of the given subject (if found).

        :param str subject: The subject we are working with.
        :param float lifetime: The number of second before timeout.

        :return: A list of PTR record(s).
        :rtype: list
        """

        if not subject:
            subject = self.subject

        try:
            if reverse_name:
                # We get the reverse name we are going to request.
                to_request = dns.reversename.from_address(subject)
            else:  # pragma: no cover
                to_request = subject

            # We get the PTR record of the currently read A record.
            return [
                str(x) for x in dns.resolver.query(to_request, "PTR", lifetime=lifetime)
            ]
        except DNSException:  # pragma: no cover
            pass

        return None  # pragma: no cover

    def get_addr_info(self, subject=None):
        """
        Get and return the information of the given subject (address).

        :param str subject: The subject we are working with.

        :return: A list of address.
        :rtype: list
        """

        if not subject:
            subject = self.subject

        try:  # pragma: no cover
            # We request the address information.
            req = getaddrinfo(subject, 80, proto=IPPROTO_TCP)

            # We format the addr infos.
            return [x[-1][0] for x in req]
        except (gaierror, OSError, herror, UnicodeError):
            pass

        return None

    def get_host_by_addr(self, subject=None):  # pragma: no cover
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

        :rtype: list
        """

        if not subject:
            subject = self.subject

        try:
            # We get the host by addr.
            req = gethostbyaddr(subject)

            # And we format the result.
            return {"hostname": req[0], "aliases": req[1], "ips": req[2]}

        except (gaierror, OSError, herror):
            pass

        return None

    def __request_not_ip(self):
        """
        Handle the request for a subject which is not an IP.
        """

        Logger().debug(f"{repr(self.subject)} is not IP. Requesting record.")

        result = {}

        # We get the NS record of the given subject.
        result["NS"] = self.ns_record()

        if self.complete:  # pragma: no cover

            # We get the A record of the given subject.
            result["A"] = self.a_record()

            # We get the AAAA record of the given subject.
            result["AAAA"] = self.aaaa_record()

            # We get the CNAME record of the given subject.
            result["CNAME"] = self.cname_record()

            # We get the MX record of the given subject.
            result["MX"] = self.mx_record()

            # We get the TXT record of the given subject.
            result["TXT"] = self.txt_record()

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
                        result["PTR"].extend(self.ptr_record(a_result))
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

        if not result:
            # We could not get DNS records about the given subject.

            # We get the addr infos.
            result["addr_info"] = self.get_addr_info()

            if not result["addr_info"]:
                # The addr_info index is empty.

                # We delete it.
                del result["addr_info"]

        Logger().debug(f"Records for {repr(self.subject)}:\n{result}")

        return result

    def __request_ip(self):
        """
        Handle the request for a subject which is an IP.
        """

        Logger().info(f"{repr(self.subject)} is an IP. Requesting PTR record.")

        result = {}

        # We get the PTR record of the given subject.
        result["PTR"] = self.ptr_record()

        if "PTR" not in result or not result["PTR"]:  # pragma: no cover
            del result["PTR"]

            Logger().error(f"PTR record for {repr(self.subject)} not found.")

        if not result:  # pragma: no cover
            # We could not get DNS records about the given subject.

            Logger().info(f"Getting hosts by addr for {repr(self.subject)}")

            result = self.get_host_by_addr()

        Logger().debug(f"Request result: \n{result}")

        return result

    def request(self):
        """
        Perform the NS request.

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
        """

        result = {}

        if not Check(self.subject).is_ip():
            # We are looking for something which is not an IPv4.

            temp_result = self.__request_not_ip()

            if isinstance(temp_result, dict):
                result.update(temp_result)
        else:
            # We are working with something which is an IPv4.

            temp_result = self.__request_ip()

            if isinstance(temp_result, dict):
                result.update(temp_result)

        return result
