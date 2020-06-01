# pylint: disable=too-many-lines, line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the CLI entry points.

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

import argparse
import sys
from multiprocessing import set_start_method
from os import cpu_count

from colorama import Back, Fore, Style
from colorama import init as initiate_colorama

import PyFunceble

from .dispatcher import Dispatcher
from .iana import Iana
from .production import Production
from .publicsuffix import PublicSuffix


def tool():  # pragma: no cover pylint: disable=too-many-branches,too-many-statements,too-many-locals
    """
    Provides the CLI.
    """

    if __name__ == "PyFunceble.cli":
        if (
            PyFunceble.abstracts.Platform.is_windows()
            or PyFunceble.abstracts.Platform.is_mac_os()
        ):
            set_start_method("spawn")
        # We initiate the end of the coloration at the end of each line.
        initiate_colorama(autoreset=True)

        try:
            # The following handle the command line argument.

            try:
                # We load the configuration.
                PyFunceble.load_config(generate_directory_structure=False)

                preset = PyFunceble.cconfig.Preset()

                description = (
                    f"{Style.BRIGHT}{Fore.GREEN}PyFunceble{Style.RESET_ALL} - "
                    "The tool to check the availability or syntax of domains, IPv4, IPv6 or URL."
                )

                epilog = (
                    f"{Style.BRIGHT}{Fore.YELLOW}For an in-depth usage, explanation and examples of the arguments, "
                    f"you should read the documentation at{Fore.GREEN} https://pyfunceble.readthedocs.io/en/dev/"
                    f"{Style.RESET_ALL}\n\n"
                    f"Crafted with {Fore.RED}♥{Fore.RESET} by "
                    f"{Style.BRIGHT}{Fore.CYAN}Nissar Chababy (@funilrys){Style.RESET_ALL} "
                    f"with the help of{Style.BRIGHT}{Fore.GREEN} "
                    f"https://pyfunceble.github.io/contributors.html{Style.RESET_ALL} "
                    f"&& {Style.BRIGHT}{Fore.GREEN}"
                    "https://pyfunceble.github.io/special-thanks.html"
                )

                parser = argparse.ArgumentParser(
                    description=description,
                    epilog=epilog,
                    add_help=False,
                    formatter_class=argparse.RawTextHelpFormatter,
                )

                source_group = parser.add_argument_group("Source")
                filtering_group = parser.add_argument_group(
                    "Source filtering, decoding, conversion and expansion"
                )
                test_control = parser.add_argument_group("Test control")
                dns_control_group = parser.add_argument_group("DNS (resolver) control")
                database_control_group = parser.add_argument_group("Databases")
                output_control_group = parser.add_argument_group("Output control")
                multiprocessing_group = parser.add_argument_group("Multiprocessing")
                ci_group = parser.add_argument_group("CI / CD")
                unique_group = parser.add_argument_group("Unique actions")

                current_value_format = (
                    f"\n{Fore.YELLOW}{Style.BRIGHT}Configured value: {Fore.BLUE}"
                )

                source_group.add_argument(
                    "-d",
                    "--domain",
                    type=str,
                    nargs="+",
                    help="Test one or more domains, separated by spaces.\n\n"
                    "When this option is used, no output files are generated.",
                )

                source_group.add_argument(
                    "-u",
                    "--url",
                    type=str,
                    nargs="+",
                    help="Test one or more full URL, separated by spaces.",
                )

                source_group.add_argument(
                    "-f",
                    "--file",
                    type=str,
                    help="Read a local or remote (RAW link) file and test all domains inside it."
                    "\nIf remote (RAW link) file is given, PyFunceble will download it,\n "
                    "and test the content of the given RAW link as if it was a locally stored file.",
                )

                source_group.add_argument(
                    "-uf",
                    "--url-file",
                    type=str,
                    help="Read a local or remote (RAW link) file and test all (full) URLs inside it."
                    "\nIf remote (RAW link) file is given, PyFunceble will download it,\n "
                    "and test the content of the given RAW link as if it was a locally stored file. "
                    "\n\nThis argument test if an URL is available. It ONLY test full URLs.",
                )

                filtering_group.add_argument(
                    "-ad",
                    "--adblock",
                    action="store_true",
                    help="Switch the decoding of the adblock format. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.adblock)
                        + Style.RESET_ALL
                    ),
                )

                filtering_group.add_argument(
                    "--aggressive", action="store_true", help=argparse.SUPPRESS
                )

                filtering_group.add_argument(
                    "--complements",
                    action="store_true",
                    help="Switch the value of the generation and test of the complements. "
                    "\nA complement is for example `example.org` if `www.example.org` "
                    "is given and vice-versa. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.generate_complements)
                        + Style.RESET_ALL
                    ),
                )

                filtering_group.add_argument(
                    "--filter", type=str, help="Domain to filter (regex)."
                )

                filtering_group.add_argument(
                    "--idna",
                    action="store_true",
                    help="Switch the value of the IDNA conversion. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.idna_conversion)
                        + Style.RESET_ALL
                    ),
                )

                filtering_group.add_argument(
                    "--mining",
                    action="store_true",
                    help="Switch the value of the mining subsystem usage. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.mining)
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "" "-c",
                    "--auto-continue",
                    "--continue",
                    action="store_true",
                    help="Switch the value of the auto continue mode. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.auto_continue)
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "--cooldown-time",
                    type=float,
                    default=0,
                    help="Switch the value of the cooldown time to apply between each test. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.cooldown_time)
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "--http",
                    action="store_true",
                    help="Switch the value of the usage of HTTP code. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.http_codes.active)
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "--local",
                    action="store_true",
                    help="Switch the value of the local network testing. %s"
                    % (
                        current_value_format
                        + repr(preset.switch("local"))
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "-ns",
                    "--no-special",
                    action="store_true",
                    help="Switch the value of the usage of the SPECIAL rules. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.no_special)
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "-nw",
                    "--no-whois",
                    action="store_true",
                    help="Switch the value of the usage of WHOIS to test the domain's status. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.no_whois)
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "--syntax",
                    action="store_true",
                    help="Switch the value of the syntax test mode. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.syntax)
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "-t",
                    "--timeout",
                    type=float,
                    default=0,
                    help="Switch the value of the timeout in seconds. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.timeout)
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "--reputation",
                    action="store_true",
                    help="Switch the value of the reputation test mode. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.reputation)
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "--use-reputation-data",
                    action="store_true",
                    help="Switch the value of the reputation data usage. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.use_reputation_data)
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "-ua",
                    "--user-agent",
                    type=str,
                    help="Set the user-agent to use and set every time we "
                    "interact with everything which\nis not the logs sharing system.",
                )

                test_control.add_argument(
                    "-vsc",
                    "--verify-ssl-certificate",
                    action="store_true",
                    help="Switch the value of the verification of the "
                    "SSL/TLS certificate when testing for URL. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.verify_ssl_certificate)
                        + Style.RESET_ALL
                    ),
                )

                test_control.add_argument(
                    "--wildcard",
                    action="store_true",
                    help="Switch the value of the wildcards test.\n\n"
                    "When used, wildcards will be proprely tested.\n\n"
                    f"{Fore.MAGENTA}{Style.BRIGHT}Warning: This is not taken in consideration if the "
                    f"'--syntax' argument is not given.{Style.RESET_ALL} %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.wildcard)
                        + Style.RESET_ALL
                    ),
                )

                dns_control_group.add_argument(
                    "--dns",
                    nargs="+",
                    help="Set one or more DNS server(s) to use during testing. "
                    "Separated by spaces.\n\nTo specify a port number for the "
                    "DNS server you append it as :port [ip:port].\n\n"
                    "If no port is specified, the default DNS port (53) is used. %s"
                    % (
                        current_value_format
                        + repr(", ".join(PyFunceble.CONFIGURATION.dns_server))
                        if PyFunceble.CONFIGURATION.dns_server
                        else current_value_format
                        + "OS (declared) DNS server"
                        + Style.RESET_ALL
                    ),
                )

                dns_control_group.add_argument(
                    "--dns-lookup-over-tcp",
                    action="store_true",
                    help="Make all DNS queries with TCP. "
                    "%s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.dns_lookup_over_tcp)
                    ),
                )

                database_control_group.add_argument(
                    "-db",
                    "--database",
                    action="store_true",
                    help="Switch the value of the usage of a database to store "
                    "inactive domains of the currently tested list. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.inactive_database)
                        + Style.RESET_ALL
                    ),
                )

                database_control_group.add_argument(
                    "--database-type",
                    type=str,
                    help="Tell us the type of database to use. "
                    "\nYou can choose between the following: `json | mariadb | mysql` %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.db_type)
                        + Style.RESET_ALL
                    ),
                )

                database_control_group.add_argument(
                    "-dbr",
                    "--days-between-db-retest",
                    type=int,
                    help="Set the numbers of days between each retest of domains present "
                    "into inactive-db.json. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.days_between_db_retest)
                        + Style.RESET_ALL
                    ),
                )

                database_control_group.add_argument(
                    "-dbc",
                    "--days-between-db-clean",
                    type=int,
                    help="Set the numbers of days since the introduction of a subject "
                    "into inactive-db.json for it to qualifies for deletion. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.days_between_inactive_db_clean)
                        + Style.RESET_ALL
                    ),
                )

                database_control_group.add_argument(
                    "-wdb",
                    "--whois-database",
                    action="store_true",
                    help="Switch the value of the usage of a database to store "
                    "whois data to avoid whois servers rate limit. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.whois_database)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "-a",
                    "--all",
                    action="store_false",
                    help="Output all available information on the screen. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.less)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "-ex",
                    "--execution",
                    action="store_true",
                    help="Switch the default value of the execution time showing. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.show_execution_time)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "--hierarchical",
                    action="store_true",
                    help="Switch the value of the hierarchical sorting of the tested file. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.hierarchical_sorting)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "-h",
                    "--host",
                    action="store_true",
                    help="Switch the value of the generation of hosts file. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.generate_hosts)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "-ip",
                    type=str,
                    help="Change the IP to print in the hosts files with the given one. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.custom_ip)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "--json",
                    action="store_true",
                    help="Switch the value of the generation "
                    "of the JSON formatted list of domains. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.generate_json)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "--less",
                    action="store_true",
                    help="Output less informations on screen. %s"
                    % (
                        current_value_format
                        + repr(preset.switch("less"))
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "-nf",
                    "--no-files",
                    action="store_true",
                    help="Switch the value of the production of output files. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.no_files)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "-nl",
                    "--no-logs",
                    action="store_true",
                    help="Switch the value of the production of logs files "
                    "in the case we encounter some errors. %s"
                    % (
                        current_value_format
                        + repr(not PyFunceble.CONFIGURATION.logs)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "-nu",
                    "--no-unified",
                    action="store_true",
                    help="Switch the value of the production unified logs "
                    "under the output directory. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.unified)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "--percentage",
                    action="store_true",
                    help="Switch the value of the percentage output mode. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.show_percentage)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "--plain",
                    action="store_true",
                    help="Switch the value of the generation "
                    "of the plain list of domains. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.plain_list_domain)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "--dots",
                    action="store_true",
                    help="Prints dots to stdout instead of giving the impression that we hang on. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.print_dots)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "-q",
                    "--quiet",
                    action="store_true",
                    help="Run the script in quiet mode. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.quiet)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "--share-logs",
                    action="store_true",
                    help="Switch the value of the sharing of logs. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.share_logs)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "-s",
                    "--simple",
                    action="store_true",
                    help="Switch the value of the simple output mode. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.simple)
                        + Style.RESET_ALL
                    ),
                )

                output_control_group.add_argument(
                    "--split",
                    action="store_true",
                    help="Switch the value of the split of the generated output files. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.inactive_database)
                        + Style.RESET_ALL
                    ),
                )

                multiprocessing_group.add_argument(
                    "-m",
                    "--multiprocess",
                    action="store_true",
                    help="Switch the value of the usage of multiple processes. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.multiprocess)
                        + Style.RESET_ALL
                    ),
                )

                multiprocessing_group.add_argument(
                    "--multiprocess-merging-mode",
                    type=str,
                    help="Sets the multiprocess merging mode. "
                    "\nYou can choose between the following: `live|ends`. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.multiprocess_merging_mode)
                        + Style.RESET_ALL
                    ),
                )

                multiprocessing_group.add_argument(
                    "-p",
                    "--processes",
                    type=int,
                    help="Set the number of simultaneous processes to use while "
                    "using multiple processes.\nIf omited, the number of "
                    "available CPU cores will be used instead.%s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.maximal_processes)
                        + Style.RESET_ALL
                    ),
                )

                ci_group.add_argument(
                    "--autosave-minutes",
                    type=int,
                    help="Update the minimum of minutes before we start "
                    "committing to upstream under the CI mode. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.ci_autosave_minutes)
                        + Style.RESET_ALL
                    ),
                )

                ci_group.add_argument(
                    "--travis", action="store_true", help=argparse.SUPPRESS,
                )

                ci_group.add_argument(
                    "--ci",
                    action="store_true",
                    help="Switch the value of the CI mode. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.ci)
                        + Style.RESET_ALL
                    ),
                )

                ci_group.add_argument(
                    "--ci-branch",
                    type=str,
                    default="master",
                    help="Switch the branch name where we are going to push the temporary results. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.ci_branch)
                        + Style.RESET_ALL
                    ),
                )

                ci_group.add_argument(
                    "--travis-branch",
                    type=str,
                    default="master",
                    help=argparse.SUPPRESS,
                )

                ci_group.add_argument(
                    "--ci-distribution-branch",
                    type=str,
                    default="master",
                    help="Switch the branch name where we are going to push the final results. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.ci_distribution_branch)
                        + Style.RESET_ALL
                    ),
                )

                ci_group.add_argument(
                    "--travis-distribution-branch",
                    type=str,
                    default="master",
                    help=argparse.SUPPRESS,
                )

                ci_group.add_argument(
                    "--cmd",
                    type=str,
                    help="Pass a command to run before each commit "
                    "(except the final one) under the CI mode. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.command_before_end)
                        + Style.RESET_ALL
                    ),
                )

                ci_group.add_argument(
                    "--cmd-before-end",
                    type=str,
                    help="Pass a command to run before the results "
                    "(final) commit under the CI mode. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.command_before_end)
                        + Style.RESET_ALL
                    ),
                )

                ci_group.add_argument(
                    "--commit-autosave-message",
                    type=str,
                    help="Replace the default autosave commit message. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.travis_autosave_commit)
                        + Style.RESET_ALL
                    ),
                )

                ci_group.add_argument(
                    "--commit-results-message",
                    type=str,
                    help="Replace the default results (final) commit message. %s"
                    % (
                        current_value_format
                        + repr(PyFunceble.CONFIGURATION.travis_autosave_final_commit)
                        + Style.RESET_ALL
                    ),
                )

                unique_group.add_argument(
                    "--clean",
                    action="store_true",
                    help="Clean all files under the output directory.",
                )

                unique_group.add_argument(
                    "--clean-all",
                    action="store_true",
                    help="Clean all files under the output directory "
                    "along with all file generated by PyFunceble.",
                )

                unique_group.add_argument(
                    "--directory-structure",
                    action="store_true",
                    help="Generate the directory and files that are needed and which does "
                    "not exist in the current directory.",
                )

                unique_group.add_argument(
                    "--iana", action="store_true", help=argparse.SUPPRESS,
                )

                unique_group.add_argument(
                    "--production", action="store_true", help=argparse.SUPPRESS
                )

                unique_group.add_argument(
                    "-psl",
                    "--public-suffix",
                    action="store_true",
                    help=argparse.SUPPRESS,
                )

                unique_group.add_argument(
                    "--generate-files-from-database",
                    action="store_true",
                    help=argparse.SUPPRESS,
                )

                unique_group.add_argument(
                    "--generate-all-files-from-database",
                    action="store_true",
                    help=argparse.SUPPRESS,
                )

                parser.add_argument(
                    "--debug", action="store_true", help=argparse.SUPPRESS
                )

                parser.add_argument(
                    "--help",
                    action="help",
                    default=argparse.SUPPRESS,
                    help="Show this help message and exit.",
                )

                parser.add_argument(
                    "-v",
                    "--version",
                    help="Show the version of PyFunceble and exit.",
                    action="version",
                    version="%(prog)s " + PyFunceble.VERSION,
                )

                args = parser.parse_args()

                if args.debug:
                    PyFunceble.CONFIGURATION.debug = preset.switch("debug")
                    PyFunceble.LOGGER.authorized = PyFunceble.LOGGER.authorization(None)
                    PyFunceble.LOGGER.init()

                if args.less:
                    PyFunceble.CONFIGURATION.less = args.less
                elif not args.all:
                    PyFunceble.CONFIGURATION.less = args.all

                if args.adblock:
                    PyFunceble.CONFIGURATION.adblock = preset.switch("adblock")

                if args.aggressive:
                    PyFunceble.CONFIGURATION.aggressive = preset.switch("aggressive")

                if args.auto_continue:
                    PyFunceble.CONFIGURATION.auto_continue = preset.switch(
                        "auto_continue"
                    )

                if args.autosave_minutes:
                    PyFunceble.CONFIGURATION.ci_autosave_minutes = args.autosave_minutes

                if args.cmd:
                    PyFunceble.CONFIGURATION.command = args.cmd

                if args.cmd_before_end:
                    PyFunceble.CONFIGURATION.command_before_end = args.cmd_before_end

                if args.commit_autosave_message:
                    PyFunceble.CONFIGURATION.ci_autosave_commit = (
                        args.commit_autosave_message
                    )

                if args.commit_results_message:
                    PyFunceble.CONFIGURATION.ci_autosave_final_commit = (
                        args.commit_results_message
                    )

                if args.complements:
                    PyFunceble.CONFIGURATION.generate_complements = preset.switch(
                        "generate_complements"
                    )

                if args.cooldown_time >= 0:
                    PyFunceble.CONFIGURATION.cooldown_time = args.cooldown_time

                if args.database:
                    PyFunceble.CONFIGURATION.inactive_database = preset.switch(
                        "inactive_database"
                    )

                if args.database_type:
                    if args.database_type.lower() in ["json", "mariadb", "mysql"]:
                        PyFunceble.CONFIGURATION.db_type = args.database_type.lower()
                    else:
                        print(
                            Style.BRIGHT
                            + Fore.RED
                            + "Unknown database type: {0}".format(
                                repr(args.database_type)
                            )
                        )
                        sys.exit(1)

                if args.days_between_db_retest:
                    PyFunceble.CONFIGURATION.days_between_db_retest = (
                        args.days_between_db_retest
                    )

                if args.days_between_db_clean:
                    PyFunceble.CONFIGURATION.days_between_inactive_db_clean = (
                        args.days_between_db_clean
                    )

                if args.dns:
                    PyFunceble.CONFIGURATION.dns_server = args.dns

                if args.dns_lookup_over_tcp:
                    PyFunceble.CONFIGURATION.dns_lookup_over_tcp = preset.switch(
                        "dns_lookup_over_tcp"
                    )

                if args.execution:
                    PyFunceble.CONFIGURATION.show_execution_time = preset.switch(
                        "show_execution_time"
                    )

                if args.filter:
                    PyFunceble.CONFIGURATION.filter = args.filter

                if args.hierarchical:
                    PyFunceble.CONFIGURATION.hierarchical_sorting = preset.switch(
                        "hierarchical_sorting"
                    )

                if args.host:
                    PyFunceble.CONFIGURATION.generate_hosts = preset.switch(
                        "generate_hosts"
                    )

                if args.http:
                    PyFunceble.CONFIGURATION.http_codes.active = preset.switch(
                        PyFunceble.CONFIGURATION.http_codes.active, True
                    )

                if args.idna:
                    PyFunceble.CONFIGURATION.idna_conversion = preset.switch(
                        "idna_conversion"
                    )

                if args.ip:
                    PyFunceble.CONFIGURATION.custom_ip = args.ip

                if args.json:
                    PyFunceble.CONFIGURATION.generate_json = preset.switch(
                        "generate_json"
                    )

                if args.local:
                    PyFunceble.CONFIGURATION.local = preset.switch("local")

                if args.mining:
                    PyFunceble.CONFIGURATION.mining = preset.switch("mining")

                if args.multiprocess:
                    PyFunceble.CONFIGURATION.multiprocess = preset.switch(
                        "multiprocess"
                    )

                if args.multiprocess_merging_mode:
                    if args.multiprocess_merging_mode.lower() in ["end", "live"]:
                        PyFunceble.CONFIGURATION.multiprocess_merging_mode = (
                            args.multiprocess_merging_mode.lower()
                        )
                    else:
                        print(
                            Style.BRIGHT
                            + Fore.RED
                            + "Unknown multiprocess merging mode: {0}".format(
                                repr(args.multiprocess_merging_mode)
                            )
                        )
                        sys.exit(1)

                if args.no_files:
                    PyFunceble.CONFIGURATION.no_files = preset.switch("no_files")

                if args.no_logs:
                    PyFunceble.CONFIGURATION.logs = preset.switch("logs")

                if args.no_special:
                    PyFunceble.CONFIGURATION.no_special = preset.switch("no_special")

                if args.no_unified:
                    PyFunceble.CONFIGURATION.unified = preset.switch("unified")

                if args.no_whois:
                    PyFunceble.CONFIGURATION.no_whois = preset.switch("no_whois")

                if args.percentage:
                    PyFunceble.CONFIGURATION.show_percentage = preset.switch(
                        "show_percentage"
                    )

                if args.plain:
                    PyFunceble.CONFIGURATION.plain_list_domain = preset.switch(
                        "plain_list_domain"
                    )

                if args.dots:
                    PyFunceble.CONFIGURATION.print_dots = preset.switch("print_dots")

                if args.processes:
                    PyFunceble.CONFIGURATION.maximal_processes = args.processes
                else:
                    PyFunceble.CONFIGURATION.maximal_processes = cpu_count()

                if args.quiet:
                    PyFunceble.CONFIGURATION.quiet = preset.switch("quiet")

                if args.reputation:
                    PyFunceble.CONFIGURATION.reputation = preset.switch("reputation")

                if args.share_logs:
                    PyFunceble.CONFIGURATION.share_logs = preset.switch("share_logs")

                if args.simple:
                    PyFunceble.CONFIGURATION.simple = preset.switch("simple")

                if args.split:
                    PyFunceble.CONFIGURATION.split = preset.switch("split")

                if args.syntax:
                    PyFunceble.CONFIGURATION.syntax = preset.switch("syntax")

                if args.timeout >= 0:
                    PyFunceble.CONFIGURATION.timeout = args.timeout

                if args.use_reputation_data:
                    PyFunceble.CONFIGURATION.use_reputation_data = preset.switch(
                        "use_reputation_data"
                    )

                if args.ci or args.travis:
                    PyFunceble.CONFIGURATION.ci = preset.switch("ci")

                if args.ci_distribution_branch:
                    PyFunceble.CONFIGURATION.ci_distribution_branch = (
                        args.ci_distribution_branch
                    )
                elif args.travis_distribution_branch:
                    PyFunceble.CONFIGURATION.ci_distribution_branch = (
                        args.travis_distribution_branch
                    )

                if args.ci_branch:
                    PyFunceble.CONFIGURATION.ci_branch = args.ci_branch
                elif args.travis_branch:
                    PyFunceble.CONFIGURATION.ci_branch = args.travis_branch

                if args.user_agent:
                    PyFunceble.CONFIGURATION.user_agent.custom = args.user_agent

                if args.verify_ssl_certificate:
                    PyFunceble.CONFIGURATION.verify_ssl_certificate = (
                        args.verify_ssl_certificate
                    )

                if args.whois_database:
                    PyFunceble.CONFIGURATION.whois_database = preset.switch(
                        "whois_database"
                    )

                if args.wildcard:
                    PyFunceble.CONFIGURATION.wildcard = preset.switch("wildcard")

                PyFunceble.core.CLI.colorify_logo(home=True)

                preset.timeout()
                preset.cooldown_time()
                preset.dns_lookup_over_tcp()

                if args.clean:
                    PyFunceble.output.Clean()

                if args.clean_all:
                    PyFunceble.output.Clean(args.clean_all)

                if args.directory_structure:
                    PyFunceble.output.Constructor()

                if args.iana:
                    Iana().update()

                if args.production:
                    Production()

                if args.public_suffix:
                    PublicSuffix().update()

                PyFunceble.LOGGER.info(f"ARGS:\n{args}")

                # We compare the versions (upstream and local) and in between.
                PyFunceble.core.CLI.compare_version_and_print_messages()

                # We call our Core which will handle all case depending of the configuration or
                # the used command line arguments.
                Dispatcher(
                    preset,
                    domain_or_ip=args.domain,
                    file_path=args.file,
                    url_to_test=args.url,
                    url_file_path=args.url_file,
                    generate_results_only=args.generate_files_from_database,
                    generate_all_results_only=args.generate_all_files_from_database,
                )
            except Exception as exception:
                try:
                    PyFunceble.LOGGER.exception()
                except AttributeError:
                    pass

                raise exception

        except KeyboardInterrupt:
            PyFunceble.core.CLI.stay_safe()
