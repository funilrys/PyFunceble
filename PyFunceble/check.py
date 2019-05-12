# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide a checking logic.

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

from domain2idna import get as domain2idna

import PyFunceble
from PyFunceble.helpers import Regex


class Check:
    """
    Provide severar "checker" around URL, IP or domain syntax..

    :param str subject: The subject (URL, IP or domain) to check.
    """

    def __init__(self, subject):
        self.subject = subject

    def is_url(self, return_base=False, return_formatted=False):
        """
        Check if the given subject is a valid URL.

        :param str url: The url to validate.

        :param bool return_base:
            Allow us the return of the url base (if URL formatted correctly).

        :param bool return_formatted:
            Allow us to get the URL converted to IDNA if the conversion
            is activated.

        :return: The validity or the base if asked.
        :rtype: bool|str
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
                initial_base = base = Regex(
                    self.subject, regex, return_data=True, rematch=True
                ).match()[2]

                if PyFunceble.CONFIGURATION["idna_conversion"]:
                    # We have to convert the domain to IDNA.

                    # We convert the initial base to IDNA.
                    base = domain2idna(base)

                # We check if the url base is a valid domain.
                domain_status = Check(base).is_domain()

                # We check if the url base is a valid IP.
                ip_status = Check(base).is_ipv4()

                if domain_status or ip_status:
                    # * The url base is a valid domain.
                    # and
                    # * The url base is a valid IP.

                    if PyFunceble.CONFIGURATION["idna_conversion"] and return_formatted:
                        # * We have to convert to IDNA.
                        # and
                        # * We have to return the converted full URL.

                        # We return the converted full URL.
                        return Regex(
                            self.subject,
                            initial_base,
                            escape=True,
                            return_data=True,
                            replace_with=base,
                            occurences=1,
                        ).replace()

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
        Check if the given subject is a valid domain.

        :param bool subdomain_check:
            Activate the subdomain checking.

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

            if not extension or extension not in PyFunceble.INTERN["iana_db"]:
                # * The extension is not found.
                # or
                # * The extension is not into the IANA database.

                # We return false.
                return False

            if (
                Regex(self.subject, regex_valid_domains, return_data=False).match()
                and not subdomain_check
            ):
                # * The element pass the domain validation.
                # and
                # * We are not checking if it is a subdomain.

                # We return True. The domain is valid.
                return True

            # The element did not pass the domain validation. That means that
            # it has invalid character or the position of - or _ are not right.

            if extension in PyFunceble.INTERN["psl_db"]:
                # The extension is into the psl database.

                for suffix in PyFunceble.INTERN["psl_db"][extension]:
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
                            return Regex(
                                to_check, regex_valid_subdomains, return_data=False
                            ).match()

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
                return Regex(
                    to_check, regex_valid_subdomains, return_data=False
                ).match()

        except (ValueError, AttributeError):
            # In case of a value or attribute error we ignore them.
            pass

        # And we return False, the domain is not valid.
        return False

    def is_subdomain(self):
        """
        Check if the given subject is a valid subdomain.

        :return: The validity.
        :rtype: bool
        """

        # We return the status of the check.
        return self.is_domain(subdomain_check=True)

    def is_ipv4(self):
        """
        Check if the given subject is a valid IPv4.

        :return: The validity.
        :rtype: bool

        .. note::
            We only test IPv4 because for now we only them for now.
        """

        # We initate our regex which will match for valid IPv4.
        regex_ipv4 = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,})$"  # pylint: disable=line-too-long

        # We check if it passes our IPv4 regex.
        # * True: It's a valid IPv4.
        # * False: It's an invalid IPv4.
        return Regex(self.subject, regex_ipv4, return_data=False).match()

    def is_ipv4_range(self):
        """
        Check if the given subject is a valid IPv4 range.

        :return: The validity.
        :rtype: bool

        .. note::
            We only test IPv4 because for now we only them for now.
        """

        if self.is_ipv4():
            # We initate our regex which will match for valid IPv4 ranges.
            regex_ipv4_range = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.([0-9]{1,}\/[0-9]{1,})$"  # pylint: disable=line-too-long

            # We check if it passes our regex.
            # * True: It's an IPv4 range.
            # * False: It's not an IPv4 range.
            return Regex(self.subject, regex_ipv4_range, return_data=False).match()
        return False

    # pylint: disable=line-too-long
    def is_reserved_ipv4(self):
        """
        Check if the given subject is a reserved IPv4.

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

            # We check if it passes our regex.
            # * True: It's reserved.
            # * False: It's not reserved.
            return Regex(self.subject, reserved_regex, return_data=False).match()

        # We return False, we are not working with an IPv4
        return False
