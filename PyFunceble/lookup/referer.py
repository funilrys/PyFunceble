"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the referer interface.

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

from random import choice

import PyFunceble


class Referer:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Get the WHOIS server (referer) of the current domain extension according to
    the IANA database.

    :param str subject: The subject we are working with.
    """

    # We create a list of ignored extension.
    # Note: We need the following because those extension does
    # not have a centralized whois server (yet).
    ignored_extension = [
        "ad",
        "al",
        "an",
        "ao",
        "aq",
        "arpa",
        "az",
        "ba",
        "bb",
        "bd",
        "bf",
        "bh",
        "bl",
        "boots",
        "bq",
        "bs",
        "bt",
        "bv",
        "cg",
        "chloe",
        "ck",
        "cu",
        "cv",
        "cw",
        "cy",
        "dj",
        "doosan",
        "eg",
        "eh",
        "er",
        "et",
        "fk",
        "flsmidth",
        "fm",
        "gb",
        "gm",
        "gn",
        "goodhands",
        "gp",
        "gr",
        "gt",
        "gu",
        "gw",
        "htc",
        "iinet",
        "jm",
        "jo",
        "kh",
        "km",
        "kp",
        "lb",
        "lr",
        "mc",
        "meo",
        "mf",
        "mh",
        "mil",
        "mm",
        "mt",
        "mv",
        "mw",
        "ne",
        "ni",
        "np",
        "nr",
        "pa",
        "pamperedchef",
        "panerai",
        "pg",
        "ph",
        "pk",
        "pn",
        "py",
        "sd",
        "sj",
        "spiegel",
        "sr",
        "ss",
        "sv",
        "sz",
        "telecity",
        "tj",
        "tp",
        "tt",
        "um",
        "va",
        "vi",
        "vista",
        "vn",
        "xn--0zwm56d",
        "xn--11b5bs3a9aj6g",
        "xn--54b7fta0cc",
        "xn--80akhbyknj4f",
        "xn--9t4b11yi5a",
        "xn--deba0ad",
        "xn--g6w251d",
        "xn--hgbk6aj7f53bba",
        "xn--hlcj6aya9esc7a",
        "xn--hlcj6aya9esc7a",
        "xn--jxalpdlp",
        "xn--kgbechtv",
        "xn--l1acc",
        "xn--mgbai9azgqp6j",
        "xn--mgbayh7gpa",
        "xn--mgbc0a9azcg",
        "xn--mgbpl2fh",
        "xn--pgbs0dh",
        "xn--qxam",
        "xn--zckzah",
        "xperia",
        "ye",
        "zw",
    ]

    def __init__(self, subject):
        # Note: A URL testing or an IP testing does not come around
        # here. So there is no need to be scared by the following.

        if subject:
            if not isinstance(subject, str):
                raise ValueError("`subject` must be a string.")

            self.subject = subject
        else:
            raise ValueError("`subject` must be given.")

        try:
            # We get the extension of the currently tested element.
            # We basically get everything after the last point.
            self.domain_extension = subject[subject.rindex(".") + 1 :]

            if not self.domain_extension and subject.endswith("."):
                self.domain_extension = [x for x in subject.split(".") if x][-1]
        except (ValueError, IndexError):
            # There was not point, so no extension to work with.
            self.domain_extension = None

        PyFunceble.LOGGER.debug(
            f"Extension to get the referer for: {self.domain_extension}"
        )

    def get(self):
        """
        Return the referer aka the WHOIS server of the current domain extension.

        :return:

            - [0] :code:`None` if there is no referer.

            - [0] :code:`False` if the extension is unknown which implicitly means
               that the subject is :code:`INVALID`

            - [0] :code:`str` The resolved IP to use.

            - [1] :code:`str`, :code:`None` the domain referer.

        :rtype: tuple
        """

        if not PyFunceble.CONFIGURATION.local:
            # We are not running a test in a local network.

            if self.domain_extension not in self.ignored_extension:
                # The extension of the domain we are testing is not into
                # the list of ignored extensions.

                if self.domain_extension in PyFunceble.IANALOOKUP:
                    # The domain extension is in the iana database.

                    if not PyFunceble.CONFIGURATION.no_whois:
                        # We are authorized to use WHOIS for the test result.

                        # We get the referer from the database.
                        referer = PyFunceble.IANALOOKUP[self.domain_extension]

                        if not referer:
                            # The referer is not filled.

                            # We log the case of the current extension.
                            PyFunceble.output.Logs().referer_not_found(
                                self.subject, self.domain_extension
                            )

                            # And we handle and return None status.
                            return None, None

                        # The referer is into the database.

                        PyFunceble.LOGGER.debug(f"Referer: {referer}")

                        resolved_referer = PyFunceble.DNSLOOKUP.a_record(referer)

                        PyFunceble.LOGGER.debug(f"Resolved Referer: {resolved_referer}")

                        try:
                            # We return the extracted referer.
                            return choice(resolved_referer), referer
                        except (IndexError, TypeError):
                            return None, referer

                    # We are not authorized to use WHOIS for the test result.

                # The domain extension is not in the iana database.

            # The extension of the domain we are testing is not into
            # the list of ignored extensions.

        # We are running a test in a local network.

        # We return None.
        return None, None
