"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the endpoint of the PyFunceble CLI tool

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

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
import os
from typing import Any, List, Tuple, Union

import colorama

import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.cli.entry_points.pyfunceble.argsparser import OurArgumentParser
from PyFunceble.cli.system.integrator import SystemIntegrator
from PyFunceble.cli.system.launcher import SystemLauncher


def get_configured_value(entry: str, *, negate=False) -> Any:
    """
    Provides the currently configured value.

    :param entry:
        An entry to check.

        multilevel should be separated with a point.

    :param negate:
        Allows us to negate the result from the configuration.

    :raise ValueError:
        When the given :code:`entry` is not found.
    """

    result = PyFunceble.facility.ConfigLoader.get_configured_value(entry)

    if negate:
        result = not result

    return (
        f"\n{colorama.Fore.YELLOW}{colorama.Style.BRIGHT}"
        f"Configured value: {colorama.Fore.BLUE}"
        f"{result!r}"
        f"{colorama.Style.RESET_ALL}"
    )


# pylint: disable=protected-access
def add_arguments_to_parser(
    parser: Union[argparse.ArgumentParser, argparse._ArgumentGroup],
    arguments: List[Tuple[List[str], dict]],
) -> None:
    """
    Adds the given argument into the given parser.
    """

    for pos_args, opt_args in arguments:
        if "dest" in opt_args:
            opt_args["dest"] = opt_args["dest"].replace(".", "__")

        parser.add_argument(*pos_args, **opt_args)


def tool() -> None:
    """
    Provides the CLI of PyFunceble.
    """

    # pylint: disable=too-many-locals

    # We start with loading the configuration. That way, we don't have to
    # think of this anymore as soon as the CLI is called.
    # As the merging is now done on demand and not on first hand, this will
    # give us a bit of agility.
    PyFunceble.facility.ConfigLoader.start()

    colorama.init(autoreset=True)

    description = (
        f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}PyFunceble PSG Generator"
        f"{colorama.Style.RESET_ALL} - "
        "The Public Suffix List file generator for PyFunceble."
    )

    our_epilog = (
        f"{colorama.Style.BRIGHT}{colorama.Fore.YELLOW}For an in-depth usage, "
        "explanation and examples of the arguments,\n"
        f"you should read the documentation at{colorama.Fore.GREEN} "
        "https://pyfunceble.readthedocs.io/en/dev/"
        f"{colorama.Style.RESET_ALL}\n\n"
    )

    parser = OurArgumentParser(
        description=description,
        epilog=our_epilog + PyFunceble.cli.storage.STD_EPILOG,
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    source_group = parser.add_argument_group("Source")
    filtering_group = parser.add_argument_group(
        "Source filtering, decoding, conversion and expansion"
    )
    test_control_group = parser.add_argument_group("Test control")
    dns_control_group = parser.add_argument_group("DNS control")
    database_control_group = parser.add_argument_group("Databases")
    output_control_group = parser.add_argument_group("Output control")
    multiprocessing_group = parser.add_argument_group("Multithreading")
    ci_group = parser.add_argument_group("CI / CD")

    available_cpu = os.cpu_count()

    if available_cpu:
        default_max_workers = available_cpu * 5
    else:
        default_max_workers = 1

    source_groups_data = [
        (
            [
                "-d",
                "--domain",
            ],
            {
                "dest": "domains",
                "type": str.lower,
                "nargs": "+",
                "help": "Test one or more domains, separated by spaces.\n\n"
                "When this option is used, no output files are generated.",
            },
        ),
        (
            [
                "-u",
                "--url",
            ],
            {
                "dest": "urls",
                "type": str,
                "nargs": "+",
                "help": "Test one or more full URL, separated by spaces.",
            },
        ),
        (
            [
                "-f",
                "--file",
            ],
            {
                "dest": "files",
                "type": str,
                "nargs": "+",
                "help": "Read a local or remote (RAW link) file and test all "
                "domains inside it."
                "\nIf remote (RAW link) file is given, PyFunceble will download "
                "it,\n and test the content of the given RAW link as if it was a"
                " locally stored file.",
            },
        ),
        (
            [
                "-uf",
                "--url-file",
            ],
            {
                "dest": "url_files",
                "type": str,
                "nargs": "+",
                "help": "Read a local or remote (RAW link) file and test all "
                "(full) URLs inside it."
                "\nIf remote (RAW link) file is given, PyFunceble will download "
                "it,\n and test the content of the given RAW link as if it was a"
                " locally stored file. "
                "\n\nThis argument test if an URL is available. It ONLY test "
                "full URLs.",
            },
        ),
    ]

    filtering_groups_data = [
        (
            [
                "--adblock",
            ],
            {
                "dest": "cli_decoding.adblock",
                "action": "store_true",
                "help": "Switch the decoding of the adblock format. %s"
                % get_configured_value("cli_decoding.adblock"),
            },
        ),
        (
            [
                "--aggressive",
            ],
            {
                "dest": "cli_decoding.adblock_aggressive",
                "action": "store_true",
                "help": argparse.SUPPRESS,
            },
        ),
        (
            [
                "--complements",
            ],
            {
                "dest": "cli_testing.complements",
                "action": "store_true",
                "help": "Switch the value of the generation and test of the "
                "complements. "
                "\nA complement is for example `example.org` if "
                "`www.example.org` "
                "is given and vice-versa. %s"
                % get_configured_value("cli_testing.complements"),
            },
        ),
        (
            [
                "--filter",
            ],
            {
                "dest": "cli_testing.file_filter",
                "type": str,
                "help": "Regex to match in order to test a given line. %s"
                % get_configured_value("cli_testing.file_filter"),
            },
        ),
        (
            [
                "--mining",
            ],
            {
                "dest": "cli_testing.mining",
                "action": "store_true",
                "help": "Switch the value of the mining subsystem usage. %s"
                % get_configured_value("cli_testing.mining"),
            },
        ),
    ]

    test_control_groups_data = [
        (
            [
                "-c",
                "--auto-continue",
                "--continue",
            ],
            {
                "dest": "cli_testing.autocontinue",
                "action": "store_true",
                "help": "Switch the value of the auto continue mode. %s"
                % get_configured_value("cli_testing.autocontinue"),
            },
        ),
        (
            [
                "--cooldown-time",
            ],
            {
                "dest": "cli_testing.cooldown_time",
                "type": float,
                "help": "Sets the cooldown time (in second) to apply between "
                "each test. %s" % get_configured_value("cli_testing.cooldown_time"),
            },
        ),
        (
            [
                "--local",
            ],
            {
                "dest": "cli_testing.local_network",
                "action": "store_true",
                "help": "Switch the value of the local network testing. %s"
                % get_configured_value("cli_testing.local_network"),
            },
        ),
        (
            [
                "--no-http",
            ],
            {
                "dest": "lookup.http_status_code",
                "action": "store_true",
                "help": "Switch the value of the usage of HTTP code. %s"
                % get_configured_value("lookup.http_status_code", negate=True),
            },
        ),
        (
            [
                "--no-special",
            ],
            {
                "dest": "lookup.special",
                "action": "store_true",
                "help": "Switch the value of the usage of the SPECIAL rules. %s"
                % get_configured_value("lookup.special", negate=True),
            },
        ),
        (
            [
                "--no-whois",
            ],
            {
                "dest": "lookup.whois",
                "action": "store_true",
                "help": "Switch the value of the usage of WHOIS to test the "
                "subject's status. %s"
                % get_configured_value("lookup.whois", negate=True),
            },
        ),
        (
            [
                "--no-netinfo",
            ],
            {
                "dest": "lookup.netinfo",
                "action": "store_true",
                "help": "Switch the value of the usage of network information "
                "to test the subject's status. %s"
                % get_configured_value("lookup.netinfo", negate=True),
            },
        ),
        (
            [
                "--no-dns",
            ],
            {
                "dest": "lookup.dns",
                "action": "store_true",
                "help": "Switch the value of the usage of DNS Lookup to test "
                "the subject's status. %s"
                % get_configured_value("lookup.dns", negate=True),
            },
        ),
        (
            [
                "--no-reputation",
            ],
            {
                "dest": "lookup.reputation",
                "action": "store_true",
                "help": "Switch the value of the usage of reputation Lookup to "
                "test the subject's status. %s"
                % get_configured_value("lookup.reputation", negate=True),
            },
        ),
        (
            [
                "--reputation",
            ],
            {
                "dest": "cli_testing.testing_mode.reputation",
                "action": "store_true",
                "help": "Switch the value of the reputation test mode. %s"
                % get_configured_value("cli_testing.testing_mode.reputation"),
            },
        ),
        (
            [
                "--rpz",
            ],
            {
                "dest": "cli_decoding.rpz",
                "action": "store_true",
                "help": "Switch the value of the RPZ policies test.\n\n"
                "When used, RPZ policies will be properly tested.\n\n %s"
                % get_configured_value("cli_decoding.rpz"),
            },
        ),
        (
            [
                "--syntax",
            ],
            {
                "dest": "cli_testing.testing_mode.syntax",
                "action": "store_true",
                "help": "Switch the value of the syntax test mode. %s"
                % get_configured_value("cli_testing.testing_mode.syntax"),
            },
        ),
        (
            [
                "-t",
                "--timeout",
            ],
            {
                "dest": "lookup.timeout",
                "type": float,
                "help": "Switch the value of the timeout in seconds. %s"
                % get_configured_value("lookup.timeout"),
            },
        ),
        (
            [
                "--use-reputation-data",
            ],
            {
                "dest": "lookup.reputation",
                "action": "store_true",
                "help": "Switch the value of the reputation data usage. %s"
                % get_configured_value("lookup.reputation"),
            },
        ),
        (
            [
                "-ua",
                "--user-agent",
            ],
            {
                "dest": "user_agent.custom",
                "type": str,
                "help": "Set the user-agent to use and set every time we "
                "interact with everything which\nis not part of the "
                "PyFunceble infrastructure.",
            },
        ),
        (
            [
                "-vsc",
                "--verify-ssl-certificate",
            ],
            {
                "dest": "verify_ssl_certificate",
                "action": "store_true",
                "help": "Switch the value of the verification of the "
                "SSL/TLS certificate when testing for URL. %s"
                % get_configured_value("verify_ssl_certificate"),
            },
        ),
        (
            [
                "--wildcard",
            ],
            {
                "dest": "cli_decoding.wildcard",
                "action": "store_true",
                "help": "Switch the value of the wildcards test.\n\n"
                "When used, wildcards will be properly tested. %s"
                % get_configured_value("cli_decoding.wildcard"),
            },
        ),
    ]

    dns_control_groups_data = [
        (
            [
                "--dns",
            ],
            {
                "dest": "dns.server",
                "nargs": "+",
                "type": str,
                "help": "Set one or more DNS server(s) to use during testing. "
                "Separated by spaces.\n\nTo specify a port number for the "
                "DNS server you append it as :port [ip:port].\n\n"
                "If no port is specified, the default DNS port (53) is used. %s"
                % get_configured_value("dns.server"),
            },
        ),
        (
            [
                "--dns-protocol",
            ],
            {
                "dest": "dns.protocol",
                "type": str,
                "choices": ["UDP", "TCP", "HTTPS", "TLS"],
                "help": "Set the protocol to use for the DNS queries. %s"
                % get_configured_value("dns.protocol"),
            },
        ),
    ]

    database_control_groups_data = [
        (
            [
                "--inactive-db",
            ],
            {
                "dest": "cli_testing.inactive_db",
                "action": "store_true",
                "help": "Switch the value of the usage of a database to store "
                "inactive domains of the currently tested list. %s"
                % get_configured_value("cli_testing.inactive_db"),
            },
        ),
        (
            [
                "--database-type",
            ],
            {
                "dest": "cli_testing.db_type",
                "type": str,
                "choices": ["csv", "mariadb", "mysql"],
                "help": "Tell us the type of database to use. "
                "\nYou can choose between the following: "
                "`csv | mariadb | mysql` %s"
                % get_configured_value("cli_testing.db_type"),
            },
        ),
        (
            [
                "-dbr",
                "--days-between-db-retest",
            ],
            {
                "dest": "cli_testing.days_between.db_retest",
                "type": int,
                "help": "Set the numbers of days between each retest of domains "
                "present into inactive-db.json. %s"
                % get_configured_value("cli_testing.days_between.db_retest"),
            },
        ),
        (
            [
                "-dbc",
                "--days-between-db-clean",
            ],
            {
                "dest": "cli_testing.days_between.db_clean",
                "type": int,
                "help": "Set the numbers of days since the introduction of a "
                "subject into inactive-db.json for it to qualifies for "
                "deletion. %s"
                % get_configured_value("cli_testing.days_between.db_clean"),
            },
        ),
        (
            [
                "-wdb",
                "--whois-database",
            ],
            {
                "dest": "cli_testing.whois_db",
                "type": int,
                "help": "Switch the value of the usage of a database to store "
                "whois data to avoid whois servers rate limit. %s"
                % get_configured_value("cli_testing.whois_db"),
            },
        ),
    ]

    output_control_groups_data = [
        (
            [
                "-a",
                "--all",
            ],
            {
                "dest": "cli_testing.display_mode.all",
                "action": "store_true",
                "help": "Output all available information on the screen. %s"
                % get_configured_value("cli_testing.display_mode.all"),
            },
        ),
        (
            [
                "-ex",
                "--execution",
            ],
            {
                "dest": "cli_testing.display_mode.execution_time",
                "action": "store_true",
                "help": "Switch the default value of the execution time showing. %s"
                % get_configured_value("cli_testing.display_mode.execution_time"),
            },
        ),
        (
            [
                "--hierarchical",
            ],
            {
                "dest": "cli_testing.sorting_mode.hierarchical",
                "action": "store_true",
                "help": "Switch the value of the hierarchical sorting of the "
                "tested file. %s"
                % get_configured_value("cli_testing.sorting_mode.hierarchical"),
            },
        ),
        (
            [
                "-h",
                "--host",
            ],
            {
                "dest": "cli_testing.file_generation.hosts",
                "action": "store_true",
                "help": "Switch the value of the generation of hosts file. %s"
                % get_configured_value("cli_testing.file_generation.hosts"),
            },
        ),
        (
            ["-ip", "--hosts-ip"],
            {
                "dest": "cli_testing.hosts_ip",
                "type": str,
                "help": "Change the IP to print in the hosts files with the "
                "given one. %s" % get_configured_value("cli_testing.hosts_ip"),
            },
        ),
        (
            [
                "--no-files",
            ],
            {
                "dest": "cli_testing.file_generation.no_file",
                "action": "store_true",
                "help": "Switch the value of the production of output files. %s"
                % get_configured_value("cli_testing.file_generation.no_file"),
            },
        ),
        (
            [
                "--no-unified",
            ],
            {
                "dest": "cli_testing.file_generation.unified_results",
                "action": "store_true",
                "help": "Switch the value of the production unified logs "
                "under the output directory. %s"
                % get_configured_value(
                    "cli_testing.file_generation.unified_results", negate=True
                ),
            },
        ),
        (
            [
                "--percentage",
            ],
            {
                "dest": "cli_testing.display_mode.percentage",
                "action": "store_true",
                "help": "Switch the value of the percentage output mode. %s"
                % get_configured_value("cli_testing.display_mode.percentage"),
            },
        ),
        (
            [
                "--plain",
            ],
            {
                "dest": "cli_testing.file_generation.plain",
                "action": "store_true",
                "help": "Switch the value of the generation "
                "of the plain list of domains. %s"
                % get_configured_value("cli_testing.file_generation.plain"),
            },
        ),
        (
            [
                "--dots",
            ],
            {
                "dest": "cli_testing.display_mode.dots",
                "action": "store_true",
                "help": "Prints dots to stdout instead of giving the impression "
                "that we hang on. %s"
                % get_configured_value("cli_testing.display_mode.dots"),
            },
        ),
        (
            [
                "-q",
                "--quiet",
            ],
            {
                "dest": "cli_testing.display_mode.quiet",
                "action": "store_true",
                "help": "Run the script in quiet mode. %s"
                % get_configured_value("cli_testing.display_mode.quiet"),
            },
        ),
        (
            [
                "--share-logs",
            ],
            {
                "dest": "share_logs",
                "action": "store_true",
                "help": argparse.SUPPRESS,
            },
        ),
        (
            [
                "-s",
                "--simple",
            ],
            {
                "dest": "cli_testing.display_mode.simple",
                "action": "store_true",
                "help": "Switch the value of the simple output mode. %s"
                % get_configured_value("cli_testing.display_mode.simple"),
            },
        ),
    ]

    multiprocessing_groups_data = [
        (
            [
                "-w",
                "--max-workers",
            ],
            {
                "dest": "cli_testing.max_workers",
                "type": int,
                "help": "Sets the number of maximal worker to use.\n"
                f"If not given, {default_max_workers} "
                "(based on the current machine) will be applied. %s"
                % get_configured_value("cli_testing.max_workers"),
            },
        ),
    ]

    ci_groups_data = [
        (
            ["--ci-max-minutes", "--autosave-minutes"],
            {
                "dest": "cli_testing.ci.max_exec_minutes",
                "type": int,
                "help": "Update the minimum of minutes before we start "
                "committing to upstream under the CI mode. %s"
                % get_configured_value("cli_testing.ci.max_exec_minutes"),
            },
        ),
        (
            ["--ci"],
            {
                "dest": "cli_testing.ci.active",
                "action": "store_true",
                "help": "Update the minimum of minutes before we start "
                "committing to upstream under the CI mode. %s"
                % get_configured_value("cli_testing.ci.active"),
            },
        ),
        (
            ["--ci-branch"],
            {
                "dest": "cli_testing.ci.branch",
                "type": str,
                "help": "Switch the branch name where we are going to push the "
                "temporary results. %s" % get_configured_value("cli_testing.ci.branch"),
            },
        ),
        (
            ["--ci-distribution-branch"],
            {
                "dest": "cli_testing.ci.distribution_branch",
                "type": str,
                "help": "Switch the branch name where we are going to push the "
                "final results. %s"
                % get_configured_value("cli_testing.ci.distribution_branch"),
            },
        ),
        (
            ["--cmd"],
            {
                "dest": "cli_testing.ci.command",
                "type": str,
                "help": "Pass a command to run before each commit "
                "(except the final one) under the CI mode. %s"
                % get_configured_value("cli_testing.ci.command"),
            },
        ),
        (
            ["--cmd-before-end"],
            {
                "dest": "cli_testing.ci.end_command",
                "type": str,
                "help": "Pass a command to run before the results "
                "(final) commit under the CI mode. %s"
                % get_configured_value("cli_testing.ci.end_command"),
            },
        ),
        (
            ["--commit-autosave-message"],
            {
                "dest": "cli_testing.ci.commit_message",
                "type": str,
                "help": "Replace the default autosave commit message. %s"
                % get_configured_value("cli_testing.ci.commit_message"),
            },
        ),
        (
            [
                "--commit-results-message",
            ],
            {
                "dest": "cli_testing.ci.end_commit_message",
                "type": str,
                "help": "Replace the default results (final) commit message. %s"
                % get_configured_value("cli_testing.ci.end_commit_message"),
            },
        ),
    ]

    default_groups_data = [
        (
            ["--debug"],
            {
                "dest": "debug.active",
                "action": "store_true",
                "help": argparse.SUPPRESS,
            },
        ),
        (
            ["--logging-level"],
            {
                "dest": "debug.level",
                "choices": ["debug", "info", "warning", "error", "critical"],
                "default": None,
                "type": str.lower,
                "help": argparse.SUPPRESS,
            },
        ),
        (
            ["--help"],
            {
                "action": "help",
                "help": "Show this help message and exit.",
                "default": argparse.SUPPRESS,
            },
        ),
        (
            [
                "-v",
                "--version",
            ],
            {
                "action": "version",
                "help": "Show the version of PyFunceble and exit.",
                "version": "%(prog)s " + PyFunceble.storage.PROJECT_VERSION,
            },
        ),
    ]

    add_arguments_to_parser(source_group, source_groups_data)
    add_arguments_to_parser(filtering_group, filtering_groups_data)
    add_arguments_to_parser(test_control_group, test_control_groups_data)
    add_arguments_to_parser(dns_control_group, dns_control_groups_data)
    add_arguments_to_parser(database_control_group, database_control_groups_data)
    add_arguments_to_parser(output_control_group, output_control_groups_data)
    add_arguments_to_parser(multiprocessing_group, multiprocessing_groups_data)
    add_arguments_to_parser(ci_group, ci_groups_data)
    add_arguments_to_parser(parser, default_groups_data)

    args = parser.parse_args()

    if any(getattr(args, x) for x in ["domains", "urls", "files", "url_files"]):
        SystemIntegrator(args).start()
        SystemLauncher(args).start()
