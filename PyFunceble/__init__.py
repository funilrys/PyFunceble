# pylint:disable=line-too-long, too-many-lines, invalid-name, cyclic-import
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

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
from inspect import getsourcefile
from os import environ, getcwd, mkdir, path, rename
from os import sep as directory_separator
from os import walk
from platform import system
from shutil import copy, rmtree
from time import mktime, strftime, strptime, time

import requests
from colorama import Back, Fore, Style
from colorama import init as initiate_colorama

from PyFunceble.api_core import APICore
from PyFunceble.check import Check
from PyFunceble.clean import Clean
from PyFunceble.cli_core import CLICore
from PyFunceble.config import Load, Merge, Version
from PyFunceble.directory_structure import DirectoryStructure
from PyFunceble.dispatcher import Dispatcher
from PyFunceble.dns_lookup import DNSLookup
from PyFunceble.iana import IANA
from PyFunceble.preset import Preset
from PyFunceble.production import Production
from PyFunceble.publicsuffix import PublicSuffix
from PyFunceble.whois import Whois

# We set our project name.
NAME = "PyFunceble"
# We set out project version.
VERSION = "1.44.2.dev -- 2_0_0_rc3 -- (Blue Bontebok: Beetle)"

# We set the list of windows "platforms"
WINDOWS_PLATFORMS = ["windows", "cygwin", "cygwin_nt-10.0"]

if "PYFUNCEBLE_OUTPUT_DIR" in environ:  # pragma: no cover
    # We handle the case that the `PYFUNCEBLE_OUTPUT_DIR` environnement variable is set.
    CURRENT_DIRECTORY = environ["PYFUNCEBLE_OUTPUT_DIR"]
elif Version(True).is_cloned():  # pragma: no cover
    # We handle the case that we are in a cloned.
    CURRENT_DIRECTORY = getcwd() + directory_separator
elif "TRAVIS_BUILD_DIR" in environ:  # pragma: no cover
    # We handle the case that we are under Travis CI.
    CURRENT_DIRECTORY = getcwd() + directory_separator
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
            CURRENT_DIRECTORY = config_dir_path
        elif path.isdir(path.expanduser("~")):
            # Something went wrong:
            #   * `~/.config` does not exists.
            #   * `~` exists.
            # We set `~/` as the directory we are working with.
            #
            # Note: The `.` at the end is because we want to hide the directory we are
            # going to create.
            CURRENT_DIRECTORY = (
                path.expanduser("~") + directory_separator + "."
            )  # pylint: disable=line-too-long
        else:
            # Everything went wrong:
            #   * `~/.config` does not exists.
            #   * `~` soes not exists.
            # We set the current directory as the directory we are working with.
            CURRENT_DIRECTORY = getcwd() + directory_separator
    elif system().lower() in WINDOWS_PLATFORMS:
        # We are under Windows or CygWin.

        if "APPDATA" in environ:
            # Everything went right:
            #   * `APPDATA` is into the environnement variables.
            # We set it as the directory we are working with.
            CURRENT_DIRECTORY = environ["APPDATA"]
        else:
            # Everything went wrong:
            #   * `APPDATA` is not into the environnement variables.
            # We set the current directory as the directory we are working with.
            CURRENT_DIRECTORY = getcwd() + directory_separator

    if not CURRENT_DIRECTORY.endswith(directory_separator):
        # If the directory we are working with does not ends with the directory
        # separator, we append it to the end.
        CURRENT_DIRECTORY += directory_separator

    # We append the name of the project to the directory we are working with.
    CURRENT_DIRECTORY += NAME + directory_separator

    if not path.isdir(CURRENT_DIRECTORY):
        # If the directory does not exist we create it.
        mkdir(CURRENT_DIRECTORY)

if not CURRENT_DIRECTORY.endswith(directory_separator):  # pragma: no cover
    # Again for safety, if the directory we are working with does not ends with
    # the directory separator, we append it to the end.
    CURRENT_DIRECTORY += directory_separator

# We set the location of the `output` directory which should always be in the current
# directory.
OUTPUT_DIRECTORY = getcwd() + directory_separator

# We set the filename of the default configuration file.
DEFAULT_CONFIGURATION_FILENAME = ".PyFunceble_production.yaml"
# We set the filename of the configuration file we are actually using.
CONFIGURATION_FILENAME = ".PyFunceble.yaml"

# We set the current time (return the current time) in a specific format.
CURRENT_TIME = strftime("%a %d %b %H:%m:%S %Z %Y")

# We initiate the location where we are going to save our whole configuration content.
CONFIGURATION = {}
# We initiate the location where we are going to get all statuses.
STATUS = {}
# We initiate the location where we are going to get all outputs.
OUTPUTS = {}
# We initiate the location where we are going to get the map of the classification
# of each status codes for the analytic part.
HTTP_CODE = {}
# We initiate the location where we are going to get all links.
LINKS = {}
# We initiate a location which will have all internal data.
INTERN = {
    "counter": {
        "number": {"down": 0, "invalid": 0, "tested": 0, "up": 0},
        "percentage": {"down": 0, "invalid": 0, "up": 0},
    }
}

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
                "domain_syntax_validation": None,
                "expiration_date": None,
                "http_status_code": None,
                "ip4_syntax_validation": None,
                "dns_lookup": [],
                "status_source": None,
                "status": None,
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
    """

    if subject:
        # The given URL is not empty nor None.

        # We retunr the status of the the url.
        return APICore(subject, complete=complete, configuration=config).url()

    # We return None, there is nothing to test.
    return None


def dns_lookup(subject, dns_server=None):  # pragma: no cover
    """
    Make a DNS lookup of the given subject.

    :param str subject: The subject we are working with.
    :param dns_server: A (or list of) DNS server to use while resolving.
    :type dns_server: str|int

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
        return DNSLookup(subject, dns_server=dns_server).request()

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
        return Whois(subject, server=server, timeout=timeout).request()

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

    if "config_loaded" not in INTERN:
        # The configuration was not already loaded.

        # We load and download the different configuration file if they are non
        # existant.
        Load(CURRENT_DIRECTORY)

        if generate_directory_structure:
            # If we are not under test which means that we want to save informations,
            # we initiate the directory structure.
            DirectoryStructure()

        # We save that the configuration was loaded.
        INTERN.update({"config_loaded": True})

    if custom and isinstance(custom, dict):
        # The given configuration is not None or empty.
        # and
        # It is a dict.

        # We update the configuration index.
        CONFIGURATION.update(custom)

        # We save the fact the the custom was loaded.
        INTERN.update({"custom_loaded": True, "custom_config_loaded": custom})


def _command_line():  # pragma: no cover pylint: disable=too-many-branches,too-many-statements
    """
    Provide the command line interface.
    """

    if __name__ == "PyFunceble":
        # We initiate the end of the coloration at the end of each line.
        initiate_colorama(autoreset=True)

        # We load the configuration.
        load_config(generate_directory_structure=False)
        try:
            # The following handle the command line argument.

            try:
                PARSER = argparse.ArgumentParser(
                    description="The tool to check the availability or syntax of domains, IPv4 or URL.",  # pylint: disable=line-too-long
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

                CURRENT_VALUE_FORMAT = (
                    Fore.YELLOW + Style.BRIGHT + "Configured value: " + Fore.BLUE
                )

                PARSER.add_argument(
                    "-ad",
                    "--adblock",
                    action="store_true",
                    help="Switch the decoding of the adblock format. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["adblock"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-a",
                    "--all",
                    action="store_false",
                    help="Output all available information on the screen. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["less"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "" "-c",
                    "--auto-continue",
                    "--continue",
                    action="store_true",
                    help="Switch the value of the auto continue mode. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["auto_continue"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--autosave-minutes",
                    type=int,
                    help="Update the minimum of minutes before we start "
                    "committing to upstream under Travis CI. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["travis_autosave_minutes"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--clean",
                    action="store_true",
                    help="Clean all files under the output directory.",
                )

                PARSER.add_argument(
                    "--clean-all",
                    action="store_true",
                    help="Clean all files under the output directory "
                    "along with all file generated by PyFunceble.",
                )

                PARSER.add_argument(
                    "--cmd",
                    type=str,
                    help="Pass a command to run before each commit "
                    "(except the final one) under the Travis mode. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["command_before_end"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--cmd-before-end",
                    type=str,
                    help="Pass a command to run before the results "
                    "(final) commit under the Travis mode. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["command_before_end"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--commit-autosave-message",
                    type=str,
                    help="Replace the default autosave commit message. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["travis_autosave_commit"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--commit-results-message",
                    type=str,
                    help="Replace the default results (final) commit message. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["travis_autosave_final_commit"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--complements",
                    action="store_true",
                    help="Switch the value of the generation and test of the complements. "
                    "A complement is for example `example.org` if `www.example.org` "
                    "is given and vice-versa. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["generate_complements"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-d", "--domain", type=str, help="Set and test the given domain."
                )

                PARSER.add_argument(
                    "-db",
                    "--database",
                    action="store_true",
                    help="Switch the value of the usage of a database to store "
                    "inactive domains of the currently tested list. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["inactive_database"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-dbr",
                    "--days-between-db-retest",
                    type=int,
                    help="Set the numbers of days between each retest of domains present "
                    "into inactive-db.json. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["days_between_db_retest"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--debug",
                    action="store_true",
                    help="Switch the value of the debug mode. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["debug"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--directory-structure",
                    action="store_true",
                    help="Generate the directory and files that are needed and which does "
                    "not exist in the current directory.",
                )

                PARSER.add_argument(
                    "--dns",
                    nargs="+",
                    help="Set the DNS server(s) we have to work with. "
                    "Multiple space separated DNS server can be given. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(", ".join(CONFIGURATION["dns_server"]))
                        if CONFIGURATION["dns_server"]
                        else CURRENT_VALUE_FORMAT + "Follow OS DNS" + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-ex",
                    "--execution",
                    action="store_true",
                    help="Switch the default value of the execution time showing. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["show_execution_time"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-f",
                    "--file",
                    type=str,
                    help="Read the given file and test all domains inside it. "
                    "If a URL is given we download and test the content of the given URL.",  # pylint: disable=line-too-long
                )

                PARSER.add_argument(
                    "--filter", type=str, help="Domain to filter (regex)."
                )

                PARSER.add_argument(
                    "--help",
                    action="help",
                    default=argparse.SUPPRESS,
                    help="Show this help message and exit.",
                )

                PARSER.add_argument(
                    "--hierarchical",
                    action="store_true",
                    help="Switch the value of the hierarchical sorting of the tested file. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["hierarchical_sorting"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-h",
                    "--host",
                    action="store_true",
                    help="Switch the value of the generation of hosts file. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["generate_hosts"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--http",
                    action="store_true",
                    help="Switch the value of the usage of HTTP code. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(HTTP_CODE["active"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--iana",
                    action="store_true",
                    help="Update/Generate `iana-domains-db.json`.",
                )

                PARSER.add_argument(
                    "--idna",
                    action="store_true",
                    help="Switch the value of the IDNA conversion. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["idna_conversion"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-ip",
                    type=str,
                    help="Change the IP to print in the hosts files with the given one. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["custom_ip"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--json",
                    action="store_true",
                    help="Switch the value of the generation "
                    "of the JSON formatted list of domains. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["generate_json"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--less",
                    action="store_true",
                    help="Output less informations on screen. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(Preset().switch("less"))
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--local",
                    action="store_true",
                    help="Switch the value of the local network testing. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(Preset().switch("local"))
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--link", type=str, help="Download and test the given file."
                )

                PARSER.add_argument(
                    "--mining",
                    action="store_true",
                    help="Switch the value of the mining subsystem usage. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["mining"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-m",
                    "--multiprocess",
                    action="store_true",
                    help="Switch the value of the usage of multiple process. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["multiprocess"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-n",
                    "--no-files",
                    action="store_true",
                    help="Switch the value of the production of output files. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["no_files"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-nl",
                    "--no-logs",
                    action="store_true",
                    help="Switch the value of the production of logs files "
                    "in the case we encounter some errors. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(not CONFIGURATION["logs"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-ns",
                    "--no-special",
                    action="store_true",
                    help="Switch the value of the usage of the SPECIAL rules. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["no_special"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-nu",
                    "--no-unified",
                    action="store_true",
                    help="Switch the value of the production unified logs "
                    "under the output directory. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["unified"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-nw",
                    "--no-whois",
                    action="store_true",
                    help="Switch the value the usage of whois to test domain's status. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["no_whois"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--percentage",
                    action="store_true",
                    help="Switch the value of the percentage output mode. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["show_percentage"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--plain",
                    action="store_true",
                    help="Switch the value of the generation "
                    "of the plain list of domains. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["plain_list_domain"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-p",
                    "--processes",
                    type=int,
                    help="Set the number of simultaneous processes to use while "
                    "using multiple processes. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["maximal_processes"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--production",
                    action="store_true",
                    help="Prepare the repository for production.",
                )

                PARSER.add_argument(
                    "-psl",
                    "--public-suffix",
                    action="store_true",
                    help="Update/Generate `public-suffix.json`.",
                )

                PARSER.add_argument(
                    "-q",
                    "--quiet",
                    action="store_true",
                    help="Run the script in quiet mode. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["quiet"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--share-logs",
                    action="store_true",
                    help="Switch the value of the sharing of logs. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["share_logs"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-s",
                    "--simple",
                    action="store_true",
                    help="Switch the value of the simple output mode. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["simple"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--split",
                    action="store_true",
                    help="Switch the value of the split of the generated output files. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["inactive_database"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--syntax",
                    action="store_true",
                    help="Switch the value of the syntax test mode. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["syntax"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-t",
                    "--timeout",
                    type=int,
                    default=3,
                    help="Switch the value of the timeout. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["seconds_before_http_timeout"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--travis",
                    action="store_true",
                    help="Switch the value of the Travis mode. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["travis"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--travis-branch",
                    type=str,
                    default="master",
                    help="Switch the branch name where we are going to push. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["travis_branch"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-u", "--url", type=str, help="Set and test the given URL."
                )

                PARSER.add_argument(
                    "-uf",
                    "--url-file",
                    type=str,
                    help="Read and test the list of URL of the given file. "
                    "If a URL is given we download and test the list (of URL) of the given URL content.",  # pylint: disable=line-too-long
                )

                PARSER.add_argument(
                    "-ua",
                    "--user-agent",
                    type=str,
                    help="Set the user-agent to use and set every time we "
                    "interact with everything which is not our logs sharing system.",  # pylint: disable=line-too-long
                )

                PARSER.add_argument(
                    "-v",
                    "--version",
                    help="Show the version of PyFunceble and exit.",
                    action="version",
                    version="%(prog)s " + VERSION,
                )

                PARSER.add_argument(
                    "-vsc",
                    "--verify-ssl-certificate",
                    action="store_true",
                    help="Switch the value of the verification of the "
                    "SSL/TLS certificate when testing for URL. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["verify_ssl_certificate"])
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "-wdb",
                    "--whois-database",
                    action="store_true",
                    help="Switch the value of the usage of a database to store "
                    "whois data in order to avoid whois servers rate limit. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["whois_database"])
                        + Style.RESET_ALL
                    ),
                )

                ARGS = PARSER.parse_args()

                if ARGS.less:
                    CONFIGURATION.update({"less": ARGS.less})
                elif not ARGS.all:
                    CONFIGURATION.update({"less": ARGS.all})

                if ARGS.adblock:
                    CONFIGURATION.update({"adblock": Preset().switch("adblock")})

                if ARGS.auto_continue:
                    CONFIGURATION.update(
                        {"auto_continue": Preset().switch("auto_continue")}
                    )

                if ARGS.autosave_minutes:
                    CONFIGURATION.update(
                        {"travis_autosave_minutes": ARGS.autosave_minutes}
                    )

                if ARGS.clean:
                    Clean(None)

                if ARGS.clean_all:
                    Clean(None, ARGS.clean_all)

                if ARGS.cmd:
                    CONFIGURATION.update({"command": ARGS.cmd})

                if ARGS.cmd_before_end:
                    CONFIGURATION.update({"command_before_end": ARGS.cmd_before_end})

                if ARGS.commit_autosave_message:
                    CONFIGURATION.update(
                        {"travis_autosave_commit": ARGS.commit_autosave_message}
                    )

                if ARGS.commit_results_message:
                    CONFIGURATION.update(
                        {"travis_autosave_final_commit": ARGS.commit_results_message}
                    )

                if ARGS.complements:
                    CONFIGURATION.update(
                        {
                            "generate_complements": Preset().switch(
                                "generate_complements"
                            )
                        }
                    )

                if ARGS.database:
                    CONFIGURATION.update(
                        {"inactive_database": Preset().switch("inactive_database")}
                    )

                if ARGS.days_between_db_retest:
                    CONFIGURATION.update(
                        {"days_between_db_retest": ARGS.days_between_db_retest}
                    )

                if ARGS.debug:
                    CONFIGURATION.update({"debug": Preset().switch("debug")})

                if ARGS.directory_structure:
                    DirectoryStructure()

                if ARGS.dns:
                    print(ARGS.dns)
                    CONFIGURATION.update({"dns_server": ARGS.dns})

                if ARGS.execution:
                    CONFIGURATION.update(
                        {"show_execution_time": Preset().switch("show_execution_time")}
                    )

                if ARGS.filter:
                    CONFIGURATION.update({"filter": ARGS.filter})

                if ARGS.hierarchical:
                    CONFIGURATION.update(
                        {
                            "hierarchical_sorting": Preset().switch(
                                "hierarchical_sorting"
                            )
                        }
                    )

                if ARGS.host:
                    CONFIGURATION.update(
                        {"generate_hosts": Preset().switch("generate_hosts")}
                    )

                if ARGS.http:
                    HTTP_CODE.update(
                        {"active": Preset().switch(HTTP_CODE["active"], True)}
                    )

                if ARGS.iana:
                    IANA().update()

                if ARGS.idna:
                    CONFIGURATION.update(
                        {"idna_conversion": Preset().switch("idna_conversion")}
                    )

                if ARGS.ip:
                    CONFIGURATION.update({"custom_ip": ARGS.ip})

                if ARGS.json:
                    CONFIGURATION.update(
                        {"generate_json": Preset().switch("generate_json")}
                    )

                if ARGS.local:
                    CONFIGURATION.update({"local": Preset().switch("local")})

                if ARGS.mining:
                    CONFIGURATION.update({"mining": Preset().switch("mining")})

                if ARGS.multiprocess:
                    CONFIGURATION.update(
                        {"multiprocess": Preset().switch("multiprocess")}
                    )

                if ARGS.no_files:
                    CONFIGURATION.update({"no_files": Preset().switch("no_files")})

                if ARGS.no_logs:
                    CONFIGURATION.update({"logs": Preset().switch("logs")})

                if ARGS.no_special:
                    CONFIGURATION.update({"no_special": Preset().switch("no_special")})

                if ARGS.no_unified:
                    CONFIGURATION.update({"unified": Preset().switch("unified")})

                if ARGS.no_whois:
                    CONFIGURATION.update({"no_whois": Preset().switch("no_whois")})

                if ARGS.percentage:
                    CONFIGURATION.update(
                        {"show_percentage": Preset().switch("show_percentage")}
                    )

                if ARGS.plain:
                    CONFIGURATION.update(
                        {"plain_list_domain": Preset().switch("plain_list_domain")}
                    )

                if ARGS.processes and ARGS.processes >= 2:
                    CONFIGURATION.update({"maximal_processes": ARGS.processes})

                if ARGS.production:
                    Production()

                if ARGS.public_suffix:
                    PublicSuffix().update()

                if ARGS.quiet:
                    CONFIGURATION.update({"quiet": Preset().switch("quiet")})

                if ARGS.share_logs:
                    CONFIGURATION.update({"share_logs": Preset().switch("share_logs")})

                if ARGS.simple:
                    CONFIGURATION.update(
                        {"simple": Preset().switch("simple"), "quiet": True}
                    )

                if ARGS.split:
                    CONFIGURATION.update({"split": Preset().switch("split")})

                if ARGS.syntax:
                    CONFIGURATION.update({"syntax": Preset().switch("syntax")})

                if ARGS.timeout and ARGS.timeout % 3 == 0:
                    CONFIGURATION.update({"seconds_before_http_timeout": ARGS.timeout})

                if ARGS.travis:
                    CONFIGURATION.update({"travis": Preset().switch("travis")})

                if ARGS.travis_branch:
                    CONFIGURATION.update({"travis_branch": ARGS.travis_branch})

                if ARGS.user_agent:
                    CONFIGURATION.update({"user_agent": ARGS.user_agent})

                if ARGS.verify_ssl_certificate:
                    CONFIGURATION.update(
                        {"verify_ssl_certificate": ARGS.verify_ssl_certificate}
                    )

                if ARGS.whois_database:
                    CONFIGURATION.update(
                        {"whois_database": Preset().switch("whois_database")}
                    )

                if not CONFIGURATION["quiet"]:
                    CLICore.colorify_logo(home=True)

                # We compare the versions (upstream and local) and in between.
                Version().compare()

                # We call our Core which will handle all case depending of the configuration or
                # the used command line arguments.
                Dispatcher(
                    domain_or_ip=ARGS.domain,
                    file_path=ARGS.file,
                    url_to_test=ARGS.url,
                    url_file_path=ARGS.url_file,
                    link_to_test=ARGS.link,
                )
            except KeyError as e:
                if not Version(True).is_cloned():
                    # We are not into the cloned version.

                    # We merge the local with the upstream configuration.
                    Merge(CURRENT_DIRECTORY)
                else:
                    # We are in the cloned version.

                    # We raise the exception.
                    #
                    # Note: The purpose of this is to avoid having
                    # to search for a mistake while developing.
                    raise e
        except KeyboardInterrupt:
            CLICore.stay_safe()
