#!/usr/bin/env python3

# pylint:disable=line-too-long, too-many-lines
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
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

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
# pylint: disable=invalid-name,cyclic-import, bad-continuation
import argparse
import socket
from collections import OrderedDict
from inspect import getsourcefile
from itertools import repeat
from os import environ, getcwd, mkdir, path, rename
from os import sep as directory_separator
from os import walk
from platform import system
from random import choice
from shutil import copy, rmtree
from time import mktime, strftime, strptime, time

import requests
from colorama import Back, Fore, Style
from colorama import init as initiate

from PyFunceble.check import Check
from PyFunceble.clean import Clean
from PyFunceble.config import Load, Merge, Version
from PyFunceble.core import Core
from PyFunceble.directory_structure import DirectoryStructure
from PyFunceble.iana import IANA
from PyFunceble.production import Production
from PyFunceble.publicsuffix import PublicSuffix

# We set our project name.
NAME = "PyFunceble"
# We set out project version.
VERSION = "0.136.0.dev-beta (Sarcoline Puku / Mosquito)"

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

    if system().lower() == "linux":
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
    elif system().lower() == "darwin":
        # We are under a Darwin Kernel (probably MacOS)

        from AppKit import (  # pylint: disable=import-error
            NSSearchPathForDirectoriesInDomains,
            NSApplicationSupportDirectory,
            NSUserDomainMask,
        )

        # We follow the directive we described in the documentation.
        # But for those who want it in code...
        #
        # From Mac documentation:
        #   To get the path to this directory use the NSApplicationSupportDirectory
        #   search path key with the NSLocalDomainMask domain.
        #
        # We set the found path as the directory we are working with.
        CURRENT_DIRECTORY = NSSearchPathForDirectoriesInDomains(
            NSApplicationSupportDirectory, NSUserDomainMask, True
        )[0]
    elif system().lower() == "windows":
        # We are under Windows.

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

# We initiate the CLI logo of PyFunceble.
ASCII_PYFUNCEBLE = """
██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝
"""


def test(domain, complete=False):  # pragma: no cover
    """
    Test the availability of the given domain or IP.

    :param domain: The domain or IP to test.
    :type domain: str

    :param complete:
        Activate the return of a dict with some significant data from
        the test.
    :type complete: bool

    :return: The status or the informations of the domain.
    :rtype: str|dict

    .. note::
        This function abstract and simplify for the access to the core for the
        end-user.
    """

    # We silently load the configuration.
    load_config(True)

    # And we return the status of the given domain.
    return Core(domain_or_ip_to_test=domain, modulo_test=True).test(complete)


def syntax_check(domain):  # pragma: no cover
    """
    Check the syntax of the given domain.

    :param domain: The domain to check the syntax for.
    :type domain: str

    :return: The syntax validity.
    :rtype: bool
    """

    # We silently load the configuration.
    load_config(True)

    return Check(domain).is_domain_valid()


def ipv4_syntax_check(ip):  # pragma: no cover
    """
    Check the syntax of the given IPv4.

    :param ip: The IPv4 to check the syntax for.
    :type ip: str

    :return: The syntax validity.
    :rtype: bool
    """

    # We silently load the configuration.
    load_config(True)

    return Check(ip).is_ip_valid()


def url_syntax_check(url):  # pragma: no cover
    """
    Check the syntax of the given URL.

    :param url: The URL to check the syntax for.
    :type url: str

    :return The syntax validity.
    :rtype: bool
    """

    # We silently load the configuration.
    load_config(True)

    return Check(url).is_url_valid()


def url_test(url, complete=False):  # pragma: no covere
    """
    Test the availability of the given URL.

    :param url: The URL to test.
    :type url: str

    :param complete:
        Activate the return of a dict with some significant data from
        the test.
    :type complete: bool

    :return: The status or the informations of the URL.
    :rtype: str|dict

    .. note::
        This function abstract and simplify for the access to the core for the
        end-user.
    """

    # We silently load the configuration.
    load_config(True)

    # And we return the status of the given URL.
    return Core(url_to_test=url, modulo_test=True).test(complete)


def load_config(under_test=False):  # pragma: no cover
    """
    Load the configuration.

    :param under_test:
        Tell us if we only have to load the configuration file (True)
        or load the configuration file and initate the output directory
        if it does not exist (False).
    :type under_test: bool
    """

    # We load and download the different configuration file if they are non
    # existant.
    Load(CURRENT_DIRECTORY)

    if not under_test:
        # If we are not under test which means that we want to save informations,
        # we initiate the directory structure.
        DirectoryStructure()


def stay_safe():  # pragma: no cover
    """
    Print a friendly message.
    """

    if (
        not CONFIGURATION["quiet"]
        and int(choice(list(filter(lambda x: x.isdigit(), str(time()))))) % 3 == 0
    ):
        print("\n" + Fore.GREEN + Style.BRIGHT + "Thanks for using PyFunceble!")
        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "Share your experience on "
            + Fore.CYAN
            + "Twitter"
            + Fore.YELLOW
            + " with "
            + Fore.CYAN
            + "#PyFunceble"
            + Fore.YELLOW
            + "!"
        )
        print(
            Fore.GREEN
            + Style.BRIGHT
            + "Have a feedback, an issue or an improvement idea ?"
        )
        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "Let us know on "
            + Fore.CYAN
            + "GitHub"
            + Fore.YELLOW
            + "!"
        )


def _command_line():  # pragma: no cover pylint: disable=too-many-branches,too-many-statements
    """
    Provide the command line interface.
    """

    if __name__ == "PyFunceble":
        # We initiate the end of the coloration at the end of each line.
        initiate(autoreset=True)

        # We load the configuration and the directory structure.
        load_config(True)
        try:
            # The following handle the command line argument.

            try:
                PARSER = argparse.ArgumentParser(
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
                        + "https://pyfunceble.rtfd.io/en/dev/contributors.html "
                        + Style.RESET_ALL
                        + "&& "
                        + Style.BRIGHT
                        + Fore.GREEN
                        + "https://pyfunceble.rtfd.io/en/dev/special-thanks.html",
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
                    help="Output all available informations on screen. %s"
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
                    "--clean", action="store_true", help="Clean all files under output."
                )

                PARSER.add_argument(
                    "--clean-all",
                    action="store_true",
                    help="Clean all files under output and all file generated by PyFunceble.",
                )

                PARSER.add_argument(
                    "--cmd",
                    type=str,
                    help="Pass a command to run before each commit "
                    "(except the final one) under the travis mode. %s"
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
                    "(final) commit under the travis mode. %s"
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
                    help="Set the numbers of day(s) between each retest of domains present "
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
                    help="Switch the value of the hierarchical sorting of tested file. %s"
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
                    help="Change the ip to print in the hosts files. %s"
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
                    "of the json list of domain. %s"
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
                        + repr(Core.switch("less"))
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--local",
                    action="store_true",
                    help="Switch the value of the local network testing. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(Core.switch("local"))
                        + Style.RESET_ALL
                    ),
                )

                PARSER.add_argument(
                    "--link", type=str, help="Download and test the given file."
                )

                PARSER.add_argument(
                    "-m",
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
                    "-n",
                    "--no-files",
                    action="store_true",
                    help="Switch the value the production of output files. %s"
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
                    "-nu",
                    "--no-unified",
                    action="store_true",
                    help="Switch the value of the production unified logs "
                    "under the output directory. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(not CONFIGURATION["unified"])
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
                    "-p",
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
                    "of the plain list of domain. %s"
                    % (
                        CURRENT_VALUE_FORMAT
                        + repr(CONFIGURATION["plain_list_domain"])
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
                    help="Switch the value of the travis mode. %s"
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
                    "-u", "--url", type=str, help="Analyze the given URL."
                )

                PARSER.add_argument(
                    "-uf",
                    "--url-file",
                    type=str,
                    help="Read and test the list of URL of the given file. "
                    "If a URL is given we download and test the content of the given URL.",  # pylint: disable=line-too-long
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
                    CONFIGURATION.update({"adblock": Core.switch("adblock")})

                if ARGS.auto_continue:
                    CONFIGURATION.update(
                        {"auto_continue": Core.switch("auto_continue")}
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

                if ARGS.database:
                    CONFIGURATION.update(
                        {"inactive_database": Core.switch("inactive_database")}
                    )

                if ARGS.days_between_db_retest:
                    CONFIGURATION.update(
                        {"days_between_db_retest": ARGS.days_between_db_retest}
                    )

                if ARGS.debug:
                    CONFIGURATION.update({"debug": Core.switch("debug")})

                if ARGS.directory_structure:
                    DirectoryStructure()

                if ARGS.execution:
                    CONFIGURATION.update(
                        {"show_execution_time": Core.switch("show_execution_time")}
                    )

                if ARGS.filter:
                    CONFIGURATION.update({"to_filter": ARGS.filter})

                if ARGS.hierarchical:
                    CONFIGURATION.update(
                        {"hierarchical_sorting": Core.switch("hierarchical_sorting")}
                    )

                if ARGS.host:
                    CONFIGURATION.update(
                        {"generate_hosts": Core.switch("generate_hosts")}
                    )

                if ARGS.http:
                    HTTP_CODE.update({"active": Core.switch(HTTP_CODE["active"], True)})

                if ARGS.iana:
                    IANA()

                if ARGS.idna:
                    CONFIGURATION.update(
                        {"idna_conversion": Core.switch("idna_conversion")}
                    )

                if ARGS.ip:
                    CONFIGURATION.update({"custom_ip": ARGS.ip})

                if ARGS.json:
                    CONFIGURATION.update(
                        {"generate_json": Core.switch("generate_json")}
                    )

                if ARGS.local:
                    CONFIGURATION.update({"local": Core.switch("local")})

                if ARGS.mining:
                    CONFIGURATION.update({"mining": Core.switch("mining")})

                if ARGS.no_files:
                    CONFIGURATION.update({"no_files": Core.switch("no_files")})

                if ARGS.no_logs:
                    CONFIGURATION.update({"logs": Core.switch("logs")})

                if ARGS.no_unified:
                    CONFIGURATION.update({"unified": Core.switch("unified")})

                if ARGS.no_whois:
                    CONFIGURATION.update({"no_whois": Core.switch("no_whois")})

                if ARGS.percentage:
                    CONFIGURATION.update(
                        {"show_percentage": Core.switch("show_percentage")}
                    )

                if ARGS.plain:
                    CONFIGURATION.update(
                        {"plain_list_domain": Core.switch("plain_list_domain")}
                    )

                if ARGS.production:
                    Production()

                if ARGS.public_suffix:
                    PublicSuffix()

                if ARGS.quiet:
                    CONFIGURATION.update({"quiet": Core.switch("quiet")})

                if ARGS.share_logs:
                    CONFIGURATION.update({"share_logs": Core.switch("share_logs")})

                if ARGS.simple:
                    CONFIGURATION.update(
                        {"simple": Core.switch("simple"), "quiet": Core.switch("quiet")}
                    )

                if ARGS.split:
                    CONFIGURATION.update({"split": Core.switch("split")})

                if ARGS.syntax:
                    CONFIGURATION.update({"syntax": Core.switch("syntax")})

                if ARGS.timeout and ARGS.timeout % 3 == 0:
                    CONFIGURATION.update({"seconds_before_http_timeout": ARGS.timeout})

                if ARGS.travis:
                    CONFIGURATION.update({"travis": Core.switch("travis")})

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
                        {"whois_database": Core.switch("whois_database")}
                    )

                if not CONFIGURATION["quiet"]:
                    print(Fore.YELLOW + ASCII_PYFUNCEBLE + Fore.RESET)

                # We compare the versions (upstream and local) and in between.
                Version().compare()

                # We call our Core which will handle all case depending of the configuration or
                # the used command line arguments.
                Core(
                    domain_or_ip_to_test=ARGS.domain,
                    file_path=ARGS.file,
                    url_to_test=ARGS.url,
                    url_file=ARGS.url_file,
                    link_to_test=ARGS.link,
                )
            except KeyError as e:
                if not Version(True).is_cloned():
                    Merge(CURRENT_DIRECTORY)
                else:
                    raise e
        except KeyboardInterrupt:
            stay_safe()
