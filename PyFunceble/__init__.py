# pylint:disable=line-too-long, too-many-lines, invalid-name, cyclic-import
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule is the main entry of PyFunceble.

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

import argparse
import socket
import warnings
from collections import OrderedDict
from datetime import datetime, timedelta
from inspect import getsourcefile
from os import environ, getcwd, mkdir, path, rename
from os import sep as directory_separator
from os import walk
from platform import system
from shutil import copy, rmtree
from time import mktime, sleep, strftime, strptime, time

import requests
from colorama import Back, Fore, Style
from colorama import init as initiate_colorama
from dotenv import load_dotenv

from PyFunceble.api_core import APICore
from PyFunceble.check import Check
from PyFunceble.clean import Clean
from PyFunceble.cli_core import CLICore
from PyFunceble.config import Load, Merge, Version
from PyFunceble.directory_structure import DirectoryStructure
from PyFunceble.dispatcher import Dispatcher
from PyFunceble.dns_lookup import DNSLookup
from PyFunceble.iana import IANA
from PyFunceble.logger import Logger
from PyFunceble.preset import Preset
from PyFunceble.production import Production
from PyFunceble.publicsuffix import PublicSuffix
from PyFunceble.whois_lookup import WhoisLookup

# We set our project name.
NAME = "PyFunceble"
# We set out project version.
VERSION = "2.11.2.dev (Green Galago: Skitterbug)"

# We set the list of windows "platforms"
WINDOWS_PLATFORMS = ["windows", "cygwin", "cygwin_nt-10.0"]

if "PYFUNCEBLE_CONFIG_DIR" in environ:  # pragma: no cover
    # We handle the case that the `PYFUNCEBLE_CONFIG_DIR` environnement variable is set.
    CONFIG_DIRECTORY = environ["PYFUNCEBLE_CONFIG_DIR"]
elif "PYFUNCEBLE_OUTPUT_DIR" in environ:  # pragma: no cover
    # We hande the retro compatibility.
    CONFIG_DIRECTORY = environ["PYFUNCEBLE_OUTPUT_DIR"]
elif Version(True).is_cloned():  # pragma: no cover
    # We handle the case that we are in a cloned.
    CONFIG_DIRECTORY = getcwd() + directory_separator
elif "TRAVIS_BUILD_DIR" in environ:  # pragma: no cover
    # We handle the case that we are under Travis CI.
    CONFIG_DIRECTORY = getcwd() + directory_separator
else:  # pragma: no cover
    # We handle all other case and distributions specific cases.

    if system().lower() == "linux" or system().lower() == "darwin":
        # We are under a Linux distribution.

        # We set the default configuration location path.
        config_dir_path = (
            path.expanduser("~" + directory_separator + ".config") + directory_separator
        )

        if path.isdir(config_dir_path):
            # Everything went right:
            #   * `~/.config` exists.
            # We set our configuration location path as the directory we are working with.
            CONFIG_DIRECTORY = config_dir_path
        elif path.isdir(path.expanduser("~")):
            # Something went wrong:
            #   * `~/.config` does not exists.
            #   * `~` exists.
            # We set `~/` as the directory we are working with.
            #
            # Note: The `.` at the end is because we want to hide the directory we are
            # going to create.
            CONFIG_DIRECTORY = (
                path.expanduser("~") + directory_separator + "."
            )  # pylint: disable=line-too-long
        else:
            # Everything went wrong:
            #   * `~/.config` does not exists.
            #   * `~` soes not exists.
            # We set the current directory as the directory we are working with.
            CONFIG_DIRECTORY = getcwd() + directory_separator
    elif system().lower() in WINDOWS_PLATFORMS:
        # We are under Windows or CygWin.

        if "APPDATA" in environ:
            # Everything went right:
            #   * `APPDATA` is into the environnement variables.
            # We set it as the directory we are working with.
            CONFIG_DIRECTORY = environ["APPDATA"]
        else:
            # Everything went wrong:
            #   * `APPDATA` is not into the environnement variables.
            # We set the current directory as the directory we are working with.
            CONFIG_DIRECTORY = getcwd() + directory_separator

    if not CONFIG_DIRECTORY.endswith(directory_separator):
        # If the directory we are working with does not ends with the directory
        # separator, we append it to the end.
        CONFIG_DIRECTORY += directory_separator

    # We append the name of the project to the directory we are working with.
    CONFIG_DIRECTORY += NAME + directory_separator

    if not path.isdir(CONFIG_DIRECTORY):
        # If the directory does not exist we create it.
        mkdir(CONFIG_DIRECTORY)

if not CONFIG_DIRECTORY.endswith(directory_separator):  # pragma: no cover
    # Again for safety, if the directory we are working with does not ends with
    # the directory separator, we append it to the end.
    CONFIG_DIRECTORY += directory_separator

# We set the location of the `output` directory which should always be in the current
# directory.
OUTPUT_DIRECTORY = getcwd() + directory_separator

# We set the filename of the default configuration file.
DEFAULT_CONFIGURATION_FILENAME = ".PyFunceble_production.yaml"
# We set the filename of the configuration file we are actually using.
CONFIGURATION_FILENAME = ".PyFunceble.yaml"
# We set the filename of our env file.
ENV_FILENAME = ".pyfunceble-env"

# We set the current time (return the current time) in a specific format.
CURRENT_TIME = strftime("%a %d %b %H:%m:%S %Z %Y")

# We initiate the location where we are going to save our whole configuration content.
CONFIGURATION = None
# We initiate the location where we are going to get all statuses.
STATUS = None
# We initiate the location where we are going to get all outputs.
OUTPUTS = None
# We initiate the location where we are going to get the map of the classification
# of each status codes for the analytic part.
HTTP_CODE = None
# We initiate the location where we are going to get all links.
LINKS = None
# We initiate a location which will have all internal data.
INTERN = {
    "counter": {
        "number": {"down": 0, "invalid": 0, "tested": 0, "up": 0},
        "percentage": {"down": 0, "invalid": 0, "up": 0},
    }
}

load_dotenv()
load_dotenv(CONFIG_DIRECTORY + ".env")
load_dotenv(CONFIG_DIRECTORY + ENV_FILENAME)

# We initiate the CLI logo of PyFunceble.
ASCII_PYFUNCEBLE = """
██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝
"""


def test(subject, complete=False, config=None):  # pragma: no cover
    """
    Test the availability of the given subject (domain or IP).

    :param subject: The subject (IP or domain) to test.
    :type subject: str|list

    :param bool complete:
        Activate the return of a dict with some significant data from
        the test.

    :param dict config:
        A dict with the configuration index (from .PyFunceble.yaml) to update.

    :return: The status or the informations of the domain.
    :rtype: str|dict

    .. note::
        If :code:`config` is given, the given :code:`dict` overwrite
        the last value of the given indexes in the configuration.

        It's actually something like following:

        ::

            pyfunceble.configuration.update(config_given_by_user)

    .. note::
        If :code:`complete` is set to :code:`True`, we return the following indexes.

        ::

            {
                "_status_source": None,
                "_status": None,
                "dns_lookup": [],
                "domain_syntax_validation": None,
                "expiration_date": None,
                "http_status_code": None,
                "ipv4_range_syntax_validation": None,
                "ipv4_syntax_validation": None,
                "ipv6_range_syntax_validation": None,
                "ipv6_syntax_validation": None,
                "status": None,
                "status_source": None,
                "subdomain_syntax_validation": None,
                "tested": None,
                "url_syntax_validation": None,
                "whois_record": None,
                "whois_server": None,
            }
    """

    if subject:
        # The subject is not empty nor None.

        # We return the status of the given subject.
        return APICore(subject, complete=complete, configuration=config).domain_and_ip()

    # We return None, there is nothing to test.
    return None


def url_test(subject, complete=False, config=None):  # pragma: no covere
    """
    Test the availability of the given subject (URL).

    :param subject: The subject (URL) to test.
    :type subject: str|list

    :param bool complete:
        Activate the return of a dict with some significant data from
        the test.

    :param dict config:
        A dict with the configuration index (from .PyFunceble.yaml) to update.

    :return: The status or the informations of the URL.
    :rtype: str|dict

    .. note::
        If :code:`config` is given, the given :code:`dict` overwrite
        the last value of the given indexes in the configuration.

        It's actually something like following:

        ::

            pyfunceble.configuration.update(config_given_by_user)

    .. note::
        If :code:`complete` is set to :code:`True`, we return the following indexes.

        ::

            {
                "_status_source": None,
                "_status": None,
                "dns_lookup": [],
                "domain_syntax_validation": None,
                "expiration_date": None,
                "http_status_code": None,
                "ipv4_range_syntax_validation": None,
                "ipv4_syntax_validation": None,
                "ipv6_range_syntax_validation": None,
                "ipv6_syntax_validation": None,
                "status": None,
                "status_source": None,
                "subdomain_syntax_validation": None,
                "tested": None,
                "url_syntax_validation": None,
                "whois_record": None,
                "whois_server": None,
            }
    """

    if subject:
        # The given URL is not empty nor None.

        # We retunr the status of the the url.
        return APICore(subject, complete=complete, configuration=config).url()

    # We return None, there is nothing to test.
    return None


def dns_lookup(
    subject, dns_server=None, complete=False, lifetime=3
):  # pragma: no cover
    """
    Make a DNS lookup of the given subject.

    :param str subject: The subject we are working with.
    :param dns_server: A (or list of) DNS server to use while resolving.
    :type dns_server: str|int
    :param bool complete:
        Tell us to look for everything instead of :code:`NS` only.
    :param int lifetime: The query lifetime.

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

    if subject:
        # The subject is not empty nor None.

        # We return the lookup.
        return DNSLookup(
            subject, dns_server=dns_server, complete=complete, lifetime=lifetime
        ).request()

    # We return None, there is nothing to work with.
    return None


def whois(subject, server=None, timeout=3):  # pragma: no cover
    """
    Request the WHOIS record of the given subject.

    :param str subject: The subject we are working with.
    :param str server:
        The WHOIS server to communicate with.

        .. note::
            If :code:`None` is given, we look for the best one.
    :param int timeout: The timeout to apply to the request.

    :return: None or the WHOIS record.
    :rtype: None|str
    """

    if subject:
        # The subject is not empty nor None.

        # We return the whois record.
        return WhoisLookup(subject, server=server, timeout=timeout).request()

    # We return None, there is nothing to work with.
    return None


def syntax_check(domain):  # pragma: no cover
    """
    Check the syntax of the given domain.

    :param domain: The domain to check the syntax from.
    :type domain: str|list

    :return: The syntax validity.
    :rtype: bool|dict

    .. warning::
        This method will be deprecated one day in the future.

        Please report to :func:`~PyFunceble.is_domain`.
    """

    warnings.warn(
        "`PyFunceble.syntax_check` will be deprecated in future version. "
        "Please use `PyFunceble.is_domain` instead.",
        DeprecationWarning,
    )

    return is_domain(domain)


def is_domain(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid domain.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validiry of the given subject.
        return APICore(subject).domain_syntax()

    # We return None, there is nothing to check.
    return None


def is_subdomain(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid subdomain.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We retun the validity of the given subject.
        return APICore(subject).subdomain_syntax()

    # We return None, there is nothing to check.
    return None


def ipv4_syntax_check(ip):  # pragma: no cover
    """
    Check the syntax of the given IPv4.

    :param ip: The IPv4 to check the syntax for.
    :type ip: str|list

    :return: The syntax validity.
    :rtype: bool|dict

    .. warning::
        This method will be deprecated one day in the future.

        Please report to :func:`~PyFunceble.is_ipv4`.
    """

    warnings.warn(
        "`PyFunceble.ipv4_syntax_check` will be deprecated in future version. "
        "Please use `PyFunceble.is_ipv4` instead.",
        DeprecationWarning,
    )

    return is_ipv4(ip)


def is_ip(subject):  # pragma: no cover
    """
    Checks if the given subject is a syntactivally valid IPv4 or IPv6.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validity of the given subject.
        return APICore(subject).ip_syntax()

    # We return None, there is nothing to check.
    return None


def is_ipv4(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid IPv4.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validity of the given subject.
        return APICore(subject).ipv4_syntax()

    # We return None, there is nothing to check.
    return None


def is_ipv6(subject):  # pragma: no cover
    """
    Checks if the given subject is syntactivally valid IPv6.

    :param subject: The subject to check the syntax from.
    :type subject: str, list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty not None.

        # We return the validity of the given subject.
        return APICore(subject).ipv6_syntax()

    # We return None, there is nothing to check.
    return None


def is_ip_range(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid IPv4 or IPv6 range.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The IPv4 range state.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validity of the given subject.
        return APICore(subject).ip_range_syntax()

    # We return None, there is nothing to check.
    return None


def is_ipv4_range(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid IPv4 range.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The IPv4 range state.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validity of the given subject.
        return APICore(subject).ipv4_range_syntax()

    # We return None, there is nothing to check.
    return None


def url_syntax_check(url):  # pragma: no cover
    """
    Check the syntax of the given URL.

    :param url: The URL to check the syntax for.
    :type url: str|list

    :return: The syntax validity.
    :rtype: bool|dict

    .. warning::
        This method will be deprecated one day in the future.

        Please report to :func:`~PyFunceble.is_url`.
    """

    warnings.warn(
        "`PyFunceble.url_syntax_check` will be deprecated in future version. "
        "Please use `PyFunceble.is_url` instead.",
        DeprecationWarning,
    )

    return is_url(url)


def is_url(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid URL.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validity of the given subject.
        return APICore(subject).url_syntax()

    # We return None, there is nothing to check.
    return None


def load_config(generate_directory_structure=False, custom=None):  # pragma: no cover
    """
    Load the configuration.

    :param bool generate_directory_structure:
        Tell us if we generate the directory structure
        along with loading the configuration file.

    :param dict custom:
        A dict with the configuration index (from .PyFunceble.yaml) to update.

    .. note::
        If :code:`config` is given, the given :code:`dict` overwrite
        the last value of the given indexes in the configuration.

        It's actually something like following:

        ::

            pyfunceble.configuration.update(config_given_by_user)
    """

    # We load and download the different configuration file if they are non
    # existant.
    Load(CONFIG_DIRECTORY, custom)

    if generate_directory_structure:
        # If we are not under test which means that we want to save informations,
        # we initiate the directory structure.
        DirectoryStructure()


def _command_line():  # pragma: no cover pylint: disable=too-many-branches,too-many-statements
    """
    Provide the command line interface.
    """

    if __name__ == "PyFunceble":
        # We initiate the end of the coloration at the end of each line.
        initiate_colorama(autoreset=True)

        try:
            # The following handle the command line argument.

            try:
                # We load the configuration.
                load_config(generate_directory_structure=False)

                preset = Preset()

                parser = argparse.ArgumentParser(
                    description="The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.",  # pylint: disable=line-too-long
                    epilog="Crafted with %s by %s"
                    % (
                        Fore.RED + "♥" + Fore.RESET,
                        Style.BRIGHT
                        + Fore.CYAN
                        + "Nissar Chababy (Funilrys) "
                        + Style.RESET_ALL
                        + "with the help of "
                        + Style.BRIGHT
                        + Fore.GREEN
                        + "https://pyfunceble.github.io/contributors.html "
                        + Style.RESET_ALL
                        + "&& "
                        + Style.BRIGHT
                        + Fore.GREEN
                        + "https://pyfunceble.github.io/special-thanks.html",
                    ),
                    add_help=False,
                )

                current_value_format = (
                    Fore.YELLOW + Style.BRIGHT + "Configured value: " + Fore.BLUE
                )

                parser.add_argument(
                    "-ad",
                    "--adblock",
                    action="store_true",
                    help="Switch the decoding of the adblock format. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.adblock)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--aggressive", action="store_true", help=argparse.SUPPRESS
                )

                parser.add_argument(
                    "-a",
                    "--all",
                    action="store_false",
                    help="Output all available information on the screen. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.less)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "" "-c",
                    "--auto-continue",
                    "--continue",
                    action="store_true",
                    help="Switch the value of the auto continue mode. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.auto_continue)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--autosave-minutes",
                    type=int,
                    help="Update the minimum of minutes before we start "
                    "committing to upstream under Travis CI. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.travis_autosave_minutes)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--clean",
                    action="store_true",
                    help="Clean all files under the output directory.",
                )

                parser.add_argument(
                    "--clean-all",
                    action="store_true",
                    help="Clean all files under the output directory "
                    "along with all file generated by PyFunceble.",
                )

                parser.add_argument(
                    "--cmd",
                    type=str,
                    help="Pass a command to run before each commit "
                    "(except the final one) under the Travis mode. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.command_before_end)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--cmd-before-end",
                    type=str,
                    help="Pass a command to run before the results "
                    "(final) commit under the Travis mode. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.command_before_end)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--commit-autosave-message",
                    type=str,
                    help="Replace the default autosave commit message. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.travis_autosave_commit)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--commit-results-message",
                    type=str,
                    help="Replace the default results (final) commit message. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.travis_autosave_final_commit)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--complements",
                    action="store_true",
                    help="Switch the value of the generation and test of the complements. "
                    "A complement is for example `example.org` if `www.example.org` "
                    "is given and vice-versa. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.generate_complements)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-d", "--domain", type=str, help="Set and test the given domain."
                )

                parser.add_argument(
                    "-db",
                    "--database",
                    action="store_true",
                    help="Switch the value of the usage of a database to store "
                    "inactive domains of the currently tested list. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.inactive_database)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--database-type",
                    type=str,
                    help="Tell us the type of database to use. "
                    "You can choose between the following: `json|mariadb|mysql` %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.db_type)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-dbr",
                    "--days-between-db-retest",
                    type=int,
                    help="Set the numbers of days between each retest of domains present "
                    "into inactive-db.json. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.days_between_db_retest)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--debug", action="store_true", help=argparse.SUPPRESS
                )

                parser.add_argument(
                    "--directory-structure",
                    action="store_true",
                    help="Generate the directory and files that are needed and which does "
                    "not exist in the current directory.",
                )

                parser.add_argument(
                    "--dns",
                    nargs="+",
                    help="Set the DNS server(s) we have to work with. "
                    "Multiple space separated DNS server can be given. %s"
                    % (
                        current_value_format + repr(", ".join(CONFIGURATION.dns_server))
                        if CONFIGURATION.dns_server
                        else current_value_format + "Follow OS DNS" + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-ex",
                    "--execution",
                    action="store_true",
                    help="Switch the default value of the execution time showing. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.show_execution_time)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-f",
                    "--file",
                    type=str,
                    help="Read the given file and test all domains inside it. "
                    "If a URL is given we download and test the content of the given URL.",  # pylint: disable=line-too-long
                )

                parser.add_argument(
                    "--filter", type=str, help="Domain to filter (regex)."
                )

                parser.add_argument(
                    "--help",
                    action="help",
                    default=argparse.SUPPRESS,
                    help="Show this help message and exit.",
                )

                parser.add_argument(
                    "--hierarchical",
                    action="store_true",
                    help="Switch the value of the hierarchical sorting of the tested file. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.hierarchical_sorting)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-h",
                    "--host",
                    action="store_true",
                    help="Switch the value of the generation of hosts file. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.generate_hosts)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--http",
                    action="store_true",
                    help="Switch the value of the usage of HTTP code. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.http_codes.active)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--iana",
                    action="store_true",
                    help="Update/Generate `iana-domains-db.json`.",
                )

                parser.add_argument(
                    "--idna",
                    action="store_true",
                    help="Switch the value of the IDNA conversion. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.idna_conversion)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-ip",
                    type=str,
                    help="Change the IP to print in the hosts files with the given one. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.custom_ip)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--json",
                    action="store_true",
                    help="Switch the value of the generation "
                    "of the JSON formatted list of domains. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.generate_json)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--less",
                    action="store_true",
                    help="Output less informations on screen. %s"
                    % (
                        current_value_format
                        + repr(preset.switch("less"))
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--local",
                    action="store_true",
                    help="Switch the value of the local network testing. %s"
                    % (
                        current_value_format
                        + repr(preset.switch("local"))
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--link", type=str, help="Download and test the given file."
                )

                parser.add_argument(
                    "--mining",
                    action="store_true",
                    help="Switch the value of the mining subsystem usage. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.mining)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-m",
                    "--multiprocess",
                    action="store_true",
                    help="Switch the value of the usage of multiple process. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.multiprocess)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-n",
                    "--no-files",
                    action="store_true",
                    help="Switch the value of the production of output files. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.no_files)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-nl",
                    "--no-logs",
                    action="store_true",
                    help="Switch the value of the production of logs files "
                    "in the case we encounter some errors. %s"
                    % (
                        current_value_format
                        + repr(not CONFIGURATION.logs)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-ns",
                    "--no-special",
                    action="store_true",
                    help="Switch the value of the usage of the SPECIAL rules. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.no_special)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-nu",
                    "--no-unified",
                    action="store_true",
                    help="Switch the value of the production unified logs "
                    "under the output directory. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.unified)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-nw",
                    "--no-whois",
                    action="store_true",
                    help="Switch the value the usage of whois to test domain's status. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.no_whois)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--percentage",
                    action="store_true",
                    help="Switch the value of the percentage output mode. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.show_percentage)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--plain",
                    action="store_true",
                    help="Switch the value of the generation "
                    "of the plain list of domains. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.plain_list_domain)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-p",
                    "--processes",
                    type=int,
                    help="Set the number of simultaneous processes to use while "
                    "using multiple processes. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.maximal_processes)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--production", action="store_true", help=argparse.SUPPRESS
                )

                parser.add_argument(
                    "-psl",
                    "--public-suffix",
                    action="store_true",
                    help="Update/Generate `public-suffix.json`.",
                )

                parser.add_argument(
                    "-q",
                    "--quiet",
                    action="store_true",
                    help="Run the script in quiet mode. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.quiet)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--share-logs",
                    action="store_true",
                    help="Switch the value of the sharing of logs. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.share_logs)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-s",
                    "--simple",
                    action="store_true",
                    help="Switch the value of the simple output mode. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.simple)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--split",
                    action="store_true",
                    help="Switch the value of the split of the generated output files. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.inactive_database)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--syntax",
                    action="store_true",
                    help="Switch the value of the syntax test mode. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.syntax)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-t",
                    "--timeout",
                    type=int,
                    default=10,
                    help="Switch the value of the timeout. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.timeout)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--travis",
                    action="store_true",
                    help="Switch the value of the Travis mode. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.travis)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "--travis-branch",
                    type=str,
                    default="master",
                    help="Switch the branch name where we are going to push. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.travis_branch)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-u", "--url", type=str, help="Set and test the given URL."
                )

                parser.add_argument(
                    "-uf",
                    "--url-file",
                    type=str,
                    help="Read and test the list of URL of the given file. "
                    "If a URL is given we download and test the list (of URL) of the given URL content.",  # pylint: disable=line-too-long
                )

                parser.add_argument(
                    "-ua",
                    "--user-agent",
                    type=str,
                    help="Set the user-agent to use and set every time we "
                    "interact with everything which is not our logs sharing system.",  # pylint: disable=line-too-long
                )

                parser.add_argument(
                    "-v",
                    "--version",
                    help="Show the version of PyFunceble and exit.",
                    action="version",
                    version="%(prog)s " + VERSION,
                )

                parser.add_argument(
                    "-vsc",
                    "--verify-ssl-certificate",
                    action="store_true",
                    help="Switch the value of the verification of the "
                    "SSL/TLS certificate when testing for URL. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.verify_ssl_certificate)
                        + Style.RESET_ALL
                    ),
                )

                parser.add_argument(
                    "-wdb",
                    "--whois-database",
                    action="store_true",
                    help="Switch the value of the usage of a database to store "
                    "whois data in order to avoid whois servers rate limit. %s"
                    % (
                        current_value_format
                        + repr(CONFIGURATION.whois_database)
                        + Style.RESET_ALL
                    ),
                )

                args = parser.parse_args()

                if args.less:
                    CONFIGURATION.less = args.less
                elif not args.all:
                    CONFIGURATION.less = args.all

                if args.adblock:
                    CONFIGURATION.adblock = preset.switch("adblock")

                if args.aggressive:
                    CONFIGURATION.aggressive = preset.switch("aggressive")

                if args.auto_continue:
                    CONFIGURATION.auto_continue = preset.switch("auto_continue")

                if args.autosave_minutes:
                    CONFIGURATION.travis_autosave_minutes = args.autosave_minutes

                if args.cmd:
                    CONFIGURATION.command = args.cmd

                if args.cmd_before_end:
                    CONFIGURATION.command_before_end = args.cmd_before_end

                if args.commit_autosave_message:
                    CONFIGURATION.travis_autosave_commit = args.commit_autosave_message

                if args.commit_results_message:
                    CONFIGURATION.travis_autosave_final_commit = (
                        args.commit_results_message
                    )

                if args.complements:
                    CONFIGURATION.generate_complements = preset.switch(
                        "generate_complements"
                    )

                if args.database:
                    CONFIGURATION.inactive_database = preset.switch("inactive_database")

                if args.database_type:
                    if args.database_type.lower() in ["json", "mariadb", "mysql"]:
                        CONFIGURATION.db_type = args.database_type.lower()
                    else:
                        print(
                            Style.BRIGHT
                            + Fore.RED
                            + "Unknown database type: {0}".format(
                                repr(args.database_type)
                            )
                        )
                        exit(1)

                if args.days_between_db_retest:
                    CONFIGURATION.days_between_db_retest = args.days_between_db_retest

                if args.debug:
                    CONFIGURATION.debug = preset.switch("debug")

                if args.dns:
                    CONFIGURATION.dns_server = args.dns

                if args.execution:
                    CONFIGURATION.show_execution_time = preset.switch(
                        "show_execution_time"
                    )

                if args.filter:
                    CONFIGURATION.filter = args.filter

                if args.hierarchical:
                    CONFIGURATION.hierarchical_sorting = preset.switch(
                        "hierarchical_sorting"
                    )

                if args.host:
                    CONFIGURATION.generate_hosts = preset.switch("generate_hosts")

                if args.http:
                    CONFIGURATION.http_codes.active = preset.switch(
                        CONFIGURATION.http_codes.active, True
                    )

                if args.idna:
                    CONFIGURATION.idna_conversion = preset.switch("idna_conversion")

                if args.ip:
                    CONFIGURATION.custom_ip = args.ip

                if args.json:
                    CONFIGURATION.generate_json = preset.switch("generate_json")

                if args.local:
                    CONFIGURATION.local = preset.switch("local")

                if args.mining:
                    CONFIGURATION.mining = preset.switch("mining")

                if args.multiprocess:
                    CONFIGURATION.multiprocess = preset.switch("multiprocess")

                if args.no_files:
                    CONFIGURATION.no_files = preset.switch("no_files")

                if args.no_logs:
                    CONFIGURATION.logs = preset.switch("logs")

                if args.no_special:
                    CONFIGURATION.no_special = preset.switch("no_special")

                if args.no_unified:
                    CONFIGURATION.unified = preset.switch("unified")

                if args.no_whois:
                    CONFIGURATION.no_whois = preset.switch("no_whois")

                if args.percentage:
                    CONFIGURATION.show_percentage = preset.switch("show_percentage")

                if args.plain:
                    CONFIGURATION.plain_list_domain = preset.switch("plain_list_domain")

                if args.processes and args.processes >= 2:
                    CONFIGURATION.maximal_processes = args.processes

                if args.quiet:
                    CONFIGURATION.quiet = preset.switch("quiet")

                if args.share_logs:
                    CONFIGURATION.share_logs = preset.switch("share_logs")

                if args.simple:
                    CONFIGURATION.simple = preset.switch("simple")
                    CONFIGURATION.quiet = True

                if args.split:
                    CONFIGURATION.split = preset.switch("split")

                if args.syntax:
                    CONFIGURATION.syntax = preset.switch("syntax")

                if args.timeout:
                    CONFIGURATION.timeout = args.timeout

                if args.travis:
                    CONFIGURATION.travis = preset.switch("travis")

                if args.travis_branch:
                    CONFIGURATION.travis_branch = args.travis_branch

                if args.user_agent:
                    CONFIGURATION.user_agent = args.user_agent

                if args.verify_ssl_certificate:
                    CONFIGURATION.verify_ssl_certificate = args.verify_ssl_certificate

                if args.whois_database:
                    CONFIGURATION.whois_database = preset.switch("whois_database")

                if not CONFIGURATION.quiet:
                    CLICore.colorify_logo(home=True)

                if args.clean:
                    Clean()

                if args.clean_all:
                    Clean(args.clean_all)

                if args.directory_structure:
                    DirectoryStructure()

                if args.iana:
                    IANA().update()

                if args.production:
                    Production()

                if args.public_suffix:
                    PublicSuffix().update()

                Logger().info(f"ARGS:\n{args}")

                # We compare the versions (upstream and local) and in between.
                Version().compare()
                Version().print_message()

                if not Version(True).is_cloned():
                    # We are not into the cloned version.

                    # We run the merging logic.
                    #
                    # Note: Actually, it compared the local and the upstream configuration.
                    # if a new key is present, it proposes the enduser to merge upstream
                    # into the local configuration.
                    Merge(CONFIG_DIRECTORY)

                # We call our Core which will handle all case depending of the configuration or
                # the used command line arguments.
                Dispatcher(
                    preset,
                    domain_or_ip=args.domain,
                    file_path=args.file,
                    url_to_test=args.url,
                    url_file_path=args.url_file,
                    link_to_test=args.link,
                )
            except Exception as e:
                Logger().exception()

                raise e

        except KeyboardInterrupt:
            CLICore.stay_safe()
