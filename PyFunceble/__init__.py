#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check domains or IP availability.

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
# pylint: disable=invalid-name,cyclic-import
import argparse
import socket
from collections import OrderedDict
from inspect import getsourcefile
from itertools import repeat
from os import environ, getcwd, mkdir, path, rename
from os import sep as directory_separator
from os import walk
from time import strftime

import requests
from colorama import Back, Fore, Style
from colorama import init as initiate

from PyFunceble.clean import Clean
from PyFunceble.config import Load, Version
from PyFunceble.core import Core
from PyFunceble.directory_structure import DirectoryStructure
from PyFunceble.iana import IANA
from PyFunceble.production import Production

CURRENT_DIRECTORY = getcwd() + directory_separator
VERSION = "0.82.5.beta"

CONFIGURATION_FILENAME = ".PyFunceble.yaml"

CONFIGURATION = {}
CURRENT_TIME = strftime("%a %d %b %H:%m:%S %Z %Y")
STATUS = {}
OUTPUTS = {}
HTTP_CODE = {}
LINKS = {}

ASCII_PYFUNCEBLE = """
██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝
"""


def test(domain):  # pragma: no cover
    """
    This function provide an access to the core while use PyFunceble as an imported module.
    """

    load_config()
    return Core(domain=domain, modulo_test=True).test()


def load_config():  # pragma: no cover
    """
    This function will load the configuration.
    """

    global CURRENT_DIRECTORY  # pylint:disable=global-statement
    Load(CURRENT_DIRECTORY)

    if OUTPUTS["main"]:
        CURRENT_DIRECTORY = OUTPUTS["main"]

        if not CURRENT_DIRECTORY.endswith(directory_separator):
            CURRENT_DIRECTORY += directory_separator

        if path.isfile(CURRENT_DIRECTORY + CONFIGURATION_FILENAME):
            Load(CURRENT_DIRECTORY)

    if not path.isdir(CURRENT_DIRECTORY + OUTPUTS["parent_directory"]):
        DirectoryStructure()


def _command_line():  # pragma: no cover  # pylint: disable=too-many-branches,too-many-statements
    """
    This function provide the command line arguments of PyFunceble.
    """

    if __name__ == "PyFunceble":
        load_config()

        initiate(autoreset=True)

        PARSER = argparse.ArgumentParser(
            description="The tool to check domain or IP availability.",
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
                + "https://git.io/vND4m "
                + Style.RESET_ALL
                + "&& "
                + Style.BRIGHT
                + Fore.GREEN
                + "https://git.io/vND4a",
            ),
            add_help=False,
        )

        CURRENT_VALUE_FORMAT = Fore.YELLOW + Style.BRIGHT + "Installed value: " + Fore.BLUE

        PARSER.add_argument(
            "-ad",
            "--adblock",
            action="store_true",
            help="Switch the decoding of the adblock format. %s"
            % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["adblock"]) + Style.RESET_ALL),
        )

        PARSER.add_argument(
            "-a",
            "--all",
            action="store_false",
            help="Output all available informations on screen. %s"
            % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["less"]) + Style.RESET_ALL),
        )

        PARSER.add_argument(
            "--cmd-before-end",
            type=str,
            help="Pass a command before the results (final) commit of travis \
            mode. %s"
            % (
                CURRENT_VALUE_FORMAT
                + repr(CONFIGURATION["command_before_end"])
                + Style.RESET_ALL
            ),
        )

        PARSER.add_argument(
            "-c",
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
            help="Update the minimum of minutes before we start commiting \
                to upstream under Travis CI. %s"
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
            "-d", "--domain", type=str, help="Analyze the given domain."
        )

        PARSER.add_argument(
            "-db",
            "--database",
            action="store_true",
            help="Switch the value of the usage of a database to store \
                inactive domains of the currently tested list. %s"
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
            help="Set the numbers of day(s) between each retest of domains present \
            into inactive-db.json. %s"
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
            % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["debug"]) + Style.RESET_ALL),
        )

        PARSER.add_argument(
            "--directory-structure",
            action="store_true",
            help="Generate the directory and files that are needed and which does \
                not exist in the current directory.",
        )

        PARSER.add_argument(
            "-f",
            "--file",
            type=str,
            help="Test a file with a list of domains. If a URL is given we download and test the content of the given URL.",  # pylint: disable=line-too-long
        )

        PARSER.add_argument("--filter", type=str, help="Domain to filter (regex).")

        PARSER.add_argument(
            "-ex",
            "--execution",
            action="store_true",
            help="Switch the dafault value of the execution time showing. %s"
            % (
                CURRENT_VALUE_FORMAT
                + repr(CONFIGURATION["show_execution_time"])
                + Style.RESET_ALL
            ),
        )

        PARSER.add_argument(
            "--help",
            action="help",
            default=argparse.SUPPRESS,
            help="Show this help message and exit.",
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
            % (CURRENT_VALUE_FORMAT + repr(HTTP_CODE["active"]) + Style.RESET_ALL),
        )

        PARSER.add_argument(
            "--iana",
            action="store_true",
            help="Update/Generate `iana-domains-db.json`.",
        )

        PARSER.add_argument(
            "-ip",
            type=str,
            help="Change the ip to print in host file. %s"
            % (
                CURRENT_VALUE_FORMAT
                + repr(CONFIGURATION["custom_ip"])
                + Style.RESET_ALL
            ),
        )

        PARSER.add_argument(
            "--less",
            action="store_true",
            help="Output less informations on screen. %s"
            % (CURRENT_VALUE_FORMAT + repr(Core.switch("less")) + Style.RESET_ALL),
        )

        PARSER.add_argument(
            "-n",
            "--no-files",
            action="store_true",
            help="Switch the value the production of output files. %s"
            % (
                CURRENT_VALUE_FORMAT + repr(CONFIGURATION["no_files"]) + Style.RESET_ALL
            ),
        )

        PARSER.add_argument(
            "--link", type=str, help="Download and test the given file."
        )

        PARSER.add_argument(
            "-nl",
            "--no-logs",
            action="store_true",
            help="Switch the value of the production of logs files in case we \
            encounter some errors. %s"
            % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["logs"]) + Style.RESET_ALL),
        )

        PARSER.add_argument(
            "-nu",
            "--no-unified",
            action="store_true",
            help="Switch the value of the production unified logs \
                under the output directory. %s"
            % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["unified"]) + Style.RESET_ALL),
        )

        PARSER.add_argument(
            "-nw",
            "--no-whois",
            action="store_true",
            help="Switch the value the usage of whois to test domain's status. %s"
            % (
                CURRENT_VALUE_FORMAT + repr(CONFIGURATION["no_whois"]) + Style.RESET_ALL
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
            help="Switch the value of the generation \
                of the plain list of domain. %s"
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
            "-q",
            "--quiet",
            action="store_true",
            help="Run the script in quiet mode. %s"
            % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["quiet"]) + Style.RESET_ALL),
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
            % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["simple"]) + Style.RESET_ALL),
        )

        PARSER.add_argument(
            "--split",
            action="store_true",
            help="Switch the valur of the split of the generated output files. %s"
            % (
                CURRENT_VALUE_FORMAT
                + repr(CONFIGURATION["inactive_database"])
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
            help="Activate the travis mode. %s"
            % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["travis"]) + Style.RESET_ALL),
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

        PARSER.add_argument("-u", "--url", type=str, help="Analyze the given url.")

        PARSER.add_argument(
            "-uf",
            "--url-file",
            type=str,
            help="Test a file with a list of URL.  If a URL is given we download and test the content of the given URL.",  # pylint: disable=line-too-long
        )

        PARSER.add_argument(
            "-v", "--version", action="version", version="%(prog)s " + VERSION
        )

        ARGS = PARSER.parse_args()

        if ARGS.less:
            CONFIGURATION.update({"less": ARGS.less})

        if ARGS.adblock:
            CONFIGURATION.update({"adblock": Core.switch("adblock")})

        if ARGS.auto_continue:
            CONFIGURATION.update({"auto_continue": Core.switch("auto_continue")})

        if ARGS.autosave_minutes:
            CONFIGURATION.update({"travis_autosave_minutes": ARGS.autosave_minutes})

        if ARGS.clean:
            Clean(None)

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

        if ARGS.host:
            CONFIGURATION.update({"generate_hosts": Core.switch("generate_hosts")})

        if ARGS.http:
            HTTP_CODE.update({"active": Core.switch(HTTP_CODE["active"], True)})

        if ARGS.iana:
            IANA()

        if ARGS.ip:
            CONFIGURATION.update({"custom_ip": ARGS.ip})

        if ARGS.no_files:
            CONFIGURATION.update({"no_files": Core.switch("no_files")})

        if ARGS.no_logs:
            CONFIGURATION.update({"logs": Core.switch("logs")})

        if ARGS.no_unified:
            CONFIGURATION.update({"unified": Core.switch("unified")})

        if ARGS.no_whois:
            CONFIGURATION.update({"no_whois": Core.switch("no_whois")})

        if ARGS.percentage:
            CONFIGURATION.update({"show_percentage": Core.switch("show_percentage")})

        if ARGS.plain:
            CONFIGURATION.update(
                {"plain_list_domain": Core.switch("plain_list_domain")}
            )

        if ARGS.production:
            Production()

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

        if ARGS.timeout and ARGS.timeout % 3 == 0:
            CONFIGURATION.update({"seconds_before_http_timeout": ARGS.timeout})

        if ARGS.travis:
            CONFIGURATION.update({"travis": Core.switch("travis")})

        if ARGS.travis_branch:
            CONFIGURATION.update({"travis_branch": ARGS.travis_branch})

        if not CONFIGURATION["quiet"]:
            print(Fore.YELLOW + ASCII_PYFUNCEBLE + Fore.RESET)

        Version().compare()
        Core(
            domain=ARGS.domain,
            file_path=ARGS.file,
            url_to_test=ARGS.url,
            url_file=ARGS.url_file,
            link_to_test=ARGS.link,
        )
