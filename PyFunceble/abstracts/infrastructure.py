"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides everything related to the PyFunceble infrastructure.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

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


class Infrastructure:
    """
    Provides some infrastructure related abstractions.
    """

    DEFAULT_CONFIGURATION_FILENAME = ".PyFunceble_production.yaml"
    """
    Sets the name of the default configuration file.

    :type: str
    """

    CONFIGURATION_FILENAME = ".PyFunceble.yaml"
    """
    Sets the name of the user editable configuration file.

    :type: str
    """

    ENV_FILENAME = ".pyfunceble-env"
    """
    Sets the name of our own environment file.

    :type: str
    """

    DOWN_FILENAME = ".pyfunceble_intern_downtime.json"
    """
    Sets the name of our own download time record
    file.

    :type: str
    """

    IANA_FILENAME = "iana-domains-db.json"
    """
    Sets the name of our own IANA database file.

    :type: str
    """

    USER_AGENT_FILENAME = "user_agents.json"
    """
    Sets the name of our own copy of the user agents file.
    """

    IPV4_REPUTATION_FILENAME = "ipv4_reputation.data"
    """
    Sets the name of our own copy of the IPv4 reputation data file.

    :type: str
    """

    PROD_CONFIG_LINK = "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/.PyFunceble_production.yaml"  # pylint: disable=line-too-long
    """
    Sets the link to the production configuration file.

    :type: str
    """
