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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

# pylint: disable=too-many-lines

import argparse
import os
import sys
from typing import Any, List, Optional, Tuple, Union

import colorama

import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.cli.entry_points.pyfunceble.argsparser import OurArgumentParser
from PyFunceble.cli.system.integrator import SystemIntegrator
from PyFunceble.cli.system.launcher import SystemLauncher
from PyFunceble.helpers.regex import RegexHelper


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

    if ":" in entry:
        location, var_name = entry.split(":", 1)

        if location == "cli_storage":
            result = getattr(PyFunceble.cli.storage, var_name)
        else:
            raise RuntimeError("<entry> ({entry!r}) not supported.")

        if var_name == "OUTPUT_DIRECTORY":
            result = os.path.join(*os.path.split(result)[:-1])
    else:
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


def get_source_group_data() -> List[Tuple[List[str], dict]]:
    """
    Provides the arguments of the source group.
    """

    return [
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


def get_filtering_group_data() -> List[Tuple[List[str], dict]]:
    """
    Provides the argument of the filtering group.
    """

    return [
        (
            [
                "--adblock",
            ],
            {
                "dest": "cli_decoding.adblock",
                "action": "store_true",
                "help": "Activates or deactivates the decoding of the adblock "
                "format. %s" % get_configured_value("cli_decoding.adblock"),
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
            ["--cidr"],
            {
                "dest": "cli_testing.cidr_expand",
                "action": "store_true",
                "help": "Activates or disables the expansion of CIDR formatted\n"
                "addresses. %s" % get_configured_value("cli_testing.cidr_expand"),
            },
        ),
        (
            [
                "--complements",
            ],
            {
                "dest": "cli_testing.complements",
                "action": "store_true",
                "help": "Activates or disables the generation and test of the\n"
                "complements. "
                "\nA complement is for example `example.org` if "
                "'www.example.org'\nis given and vice-versa. %s"
                % get_configured_value("cli_testing.complements"),
            },
        ),
        (
            [
                "--preload",
            ],
            {
                "dest": "cli_testing.preload_file",
                "action": "store_true",
                "help": "Activates or disables the preloading of the input\n"
                "file(s) into the continue dataset before starting the tests.\n\n"
                "This reduces the waiting time while continuing a previous\n"
                "session.\n"
                "Note: This is useless when the auto continue subsystem is not "
                "active. %s" % get_configured_value("cli_testing.preload_file"),
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
                "help": "Activates or disables the mining subsystem. %s"
                % get_configured_value("cli_testing.mining"),
            },
        ),
        (
            [
                "--rpz",
            ],
            {
                "dest": "cli_decoding.rpz",
                "action": "store_true",
                "help": "Activates or disables the decoding of RPZ policies\n"
                "from each given input files. %s"
                % get_configured_value("cli_decoding.rpz"),
            },
        ),
        (
            [
                "--wildcard",
            ],
            {
                "dest": "cli_decoding.wildcard",
                "action": "store_true",
                "help": "Activates or disables the decoding of wildcards for\n"
                "each given input files. %s"
                % get_configured_value("cli_decoding.wildcard"),
            },
        ),
    ]


def get_test_control_group_data() -> List[Tuple[List[str], dict]]:
    """
    Provides the argument of the test control data group.
    """

    return [
        (
            [
                "-c",
                "--auto-continue",
                "--continue",
            ],
            {
                "dest": "cli_testing.autocontinue",
                "action": "store_true",
                "help": "Activates or disables the autocontinue subsystem. %s"
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
                "help": "Sets the cooldown time (in second) to apply between\n"
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
                "help": "Activates or disables the consideration of the test(s)\n"
                "in or for a local or private network context. %s"
                % get_configured_value("cli_testing.local_network"),
            },
        ),
        (
            ["--dns-lookup"],
            {
                "dest": "lookup.dns",
                "action": "store_true",
                "help": "Activates or disables the usage of the DNS lookup\n"
                "whether possible. %s" % get_configured_value("lookup.dns"),
            },
        ),
        (
            ["--http", "--http-status-code-lookup"],
            {
                "dest": "lookup.http_status_code",
                "action": "store_true",
                "help": "Switch the value of the usage of HTTP code. %s"
                % get_configured_value("lookup.http_status_code"),
            },
        ),
        (
            [
                "--netinfo-lookup",
            ],
            {
                "dest": "lookup.netinfo",
                "action": "store_true",
                "help": "Activates or disables the usage of the network\n"
                "information (or network socket) whether possible. %s"
                % get_configured_value("lookup.netinfo"),
            },
        ),
        (
            [
                "--special-lookup",
            ],
            {
                "dest": "lookup.special",
                "action": "store_true",
                "help": "Activates or disables the usage of our SPECIAL and\n"
                "extra rules whether possible. %s"
                % get_configured_value("lookup.special"),
            },
        ),
        (
            [
                "--whois-lookup",
            ],
            {
                "dest": "lookup.whois",
                "action": "store_true",
                "help": "Activates or disables the usage of the WHOIS record\n"
                "(or better said the expiration date in it) whether possible. %s"
                % get_configured_value("lookup.whois"),
            },
        ),
        (
            [
                "--reputation-lookup",
            ],
            {
                "dest": "lookup.reputation",
                "action": "store_true",
                "help": "Activates or disables the usage of the reputation\n"
                "dataset whether possible. %s"
                % get_configured_value("lookup.reputation"),
            },
        ),
        (
            [
                "--reputation",
            ],
            {
                "dest": "cli_testing.testing_mode.reputation",
                "action": "store_true",
                "help": "Activates or disables the reputation checker. %s"
                % get_configured_value("cli_testing.testing_mode.reputation"),
            },
        ),
        (
            [
                "--syntax",
            ],
            {
                "dest": "cli_testing.testing_mode.syntax",
                "action": "store_true",
                "help": "Activates or disables the syntax checker. %s"
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
                "default": 5.0,
                "help": "Sets the default timeout to apply to each lookup\n"
                "utilities every time it is possible to define a timeout. %s"
                % get_configured_value("lookup.timeout"),
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
                "help": "Sets the user agent to use.\n\nIf not given, we try to "
                "get the latest (automatically) for you.",
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
                "help": "Activates or disables the verification of the SSL/TLS\n"
                "certificate when testing for URL. %s"
                % get_configured_value("verify_ssl_certificate"),
            },
        ),
    ]


def get_dns_control_group_data() -> List[Tuple[List[str], dict]]:
    """
    Provides the argument of the DNS control group.
    """

    return [
        (
            [
                "--dns",
            ],
            {
                "dest": "dns.server",
                "nargs": "+",
                "type": str,
                "help": "Sets one or more (space separated) DNS server(s) to "
                "use during testing."
                "\n\nTo specify a port number for the "
                "DNS server you append\nit as :port [ip:port].\n\n"
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
                "help": "Sets the protocol to use for the DNS queries. %s"
                % get_configured_value("dns.protocol"),
            },
        ),
        (
            ["--follow-server-order"],
            {
                "dest": "dns.follow_server_order",
                "action": "store_true",
                "help": "Let us follow or mix the order of usage of the given\n"
                "or found DNS server(s). %s"
                % get_configured_value("dns.follow_server_order"),
            },
        ),
        (
            ["--trust-dns-server"],
            {
                "dest": "dns.trust_server",
                "action": "store_true",
                "help": "Activates or disable the trust mode.\n\n"
                "When active, when the first read DNS server give us a negative\n"
                "response - without error - we take it as it it.\n"
                "Otherwise, if not active, when the first read DNS server give us\n"
                "a negative response - without error - we still consolidate by\n"
                "checking all given/found server.\n%s"
                % get_configured_value("dns.trust_server"),
            },
        ),
    ]


def get_database_control_group_data() -> List[Tuple[List[str], dict]]:
    """
    Provides the arguments of the database group.
    """

    return [
        (
            [
                "--inactive-db",
            ],
            {
                "dest": "cli_testing.inactive_db",
                "action": "store_true",
                "help": "Activates or disables the usage of a 'database' to\n"
                f"store all {PyFunceble.storage.STATUS.down!r} and "
                f"{PyFunceble.storage.STATUS.invalid!r} "
                " subject for continuous retest. %s"
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
                "help": "Sets the database engine to use. "
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
                "help": "Sets the numbers of days since the introduction of\n"
                "subject into the inactive dataset before it gets retested. %s"
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
                "help": argparse.SUPPRESS,
            },
        ),
        (
            [
                "-wdb",
                "--whois-database",
            ],
            {
                "dest": "cli_testing.whois_db",
                "action": "store_true",
                "help": "Activates or disables the usage of a 'database' to\n"
                "store the expiration date of all domains with a valid\n"
                "expiration date. %s" % get_configured_value("cli_testing.whois_db"),
            },
        ),
    ]


def get_output_control_group_data() -> List[Tuple[List[str], dict]]:
    """
    Provides the argument of the output group.
    """

    return [
        (
            [
                "-a",
                "--all",
            ],
            {
                "dest": "cli_testing.display_mode.all",
                "action": "store_true",
                "help": "Activates or disables the display of the all\n"
                "information in the table we print to stdout. %s"
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
                "help": "Activates or disables the display of the execution time. %s"
                % get_configured_value("cli_testing.display_mode.execution_time"),
            },
        ),
        (
            ["--colour", "--color"],
            {
                "dest": "cli_testing.display_mode.colour",
                "action": "store_true",
                "help": "Activates or disables the coloration to STDOUT. %s"
                % get_configured_value("cli_testing.display_mode.colour"),
            },
        ),
        (
            ["--display-status"],
            {
                "dest": "cli_testing.display_mode.status",
                "type": str.upper,
                "choices": ["all"] + list(PyFunceble.storage.STATUS.values()),
                "nargs": "+",
                "help": "Sets the status that we are allowed to print to STDOUT.\n\n"
                "Multiple space separated statuses can be given."
                "%s" % get_configured_value("cli_testing.display_mode.status"),
                "default": "all",
            },
        ),
        (
            [
                "--hierarchical",
            ],
            {
                "dest": "cli_testing.sorting_mode.hierarchical",
                "action": "store_true",
                "help": "Activates or disables the sorting of the files\n"
                "content (output) in a hierarchical order. %s"
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
                "help": "Activates or disables the generation of the\n"
                "hosts file(s). %s"
                % get_configured_value("cli_testing.file_generation.hosts"),
            },
        ),
        (
            ["-ip", "--hosts-ip"],
            {
                "dest": "cli_testing.hosts_ip",
                "type": str,
                "help": "Sets the IP to prefix each lines of the hosts file. %s"
                % get_configured_value("cli_testing.hosts_ip"),
            },
        ),
        (
            [
                "--no-files",
            ],
            {
                "dest": "cli_testing.file_generation.no_file",
                "action": "store_true",
                "help": "Activates or disables the generation of any non-logs\n"
                "file(s). %s"
                % get_configured_value("cli_testing.file_generation.no_file"),
            },
        ),
        (
            [
                "--output-location",
            ],
            {
                "dest": "output_location",
                "type": str,
                "help": "Sets the location where we are supposed to generation\n"
                "the output directory from. %s"
                % get_configured_value("cli_storage:OUTPUT_DIRECTORY"),
            },
        ),
        (
            [
                "--unified-results",
            ],
            {
                "dest": "cli_testing.file_generation.unified_results",
                "action": "store_true",
                "help": "Activates or disables the generation of the unified\n"
                "results file instead of the divided ones. %s"
                % get_configured_value(
                    "cli_testing.file_generation.unified_results",
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
                "help": "Activates or disables the display and generation\n"
                "of the percentage - file - of each status. %s"
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
                "help": "Activates or disables the generation of the\n"
                "RAW file(s). What is meant is a list with only a list of\n"
                "subject (one per line). %s"
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
                "help": "Activate or disables the display of dots or other\n"
                "characters when we skip the test of a subject. %s"
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
                "help": "Activates or disables the display of output to the\n"
                "terminal. %s" % get_configured_value("cli_testing.display_mode.quiet"),
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
                "help": "Activates or disables the simple output mode. %s"
                % get_configured_value("cli_testing.display_mode.simple"),
            },
        ),
    ]


def get_multiprocessing_group_data() -> List[Tuple[List[str], dict]]:
    """
    Provides the argument of the multithreading group data.
    """

    available_cpu = os.cpu_count()

    if available_cpu:
        default_max_workers = available_cpu * 5
    else:
        default_max_workers = 1

    return [
        (
            [
                "-w",
                "--max-workers",
            ],
            {
                "dest": "cli_testing.max_workers",
                "type": int,
                "help": "Sets the number of maximal workers to use.\n"
                f"If not given, {default_max_workers} "
                "(based on the current machine) will be applied. %s"
                % get_configured_value("cli_testing.max_workers"),
            },
        ),
    ]


def get_ci_group_data() -> List[Tuple[List[str], dict]]:
    """
    Provides the argument of the CI group data.
    """

    return [
        (
            ["--ci-max-minutes"],
            {
                "dest": "cli_testing.ci.max_exec_minutes",
                "type": int,
                "help": "Sets the number of minutes to wait before starting\n"
                "to stop a CI session. %s"
                % get_configured_value("cli_testing.ci.max_exec_minutes"),
            },
        ),
        (
            ["--ci"],
            {
                "dest": "cli_testing.ci.active",
                "action": "store_true",
                "help": "Activates or disables the Continuous Integration\n"
                "mechanism. %s" % get_configured_value("cli_testing.ci.active"),
            },
        ),
        (
            ["--ci-branch"],
            {
                "dest": "cli_testing.ci.branch",
                "type": str,
                "help": "Sets our git working branch. This is the branch\n"
                "from where we are supposed to store the tests\n"
                "(excepts the final results). %s"
                % get_configured_value("cli_testing.ci.branch"),
            },
        ),
        (
            ["--ci-distribution-branch"],
            {
                "dest": "cli_testing.ci.distribution_branch",
                "type": str,
                "help": "Sets our git distributions branch. This is the\n"
                "branch from where we are supposed to store and push\n"
                "the final results. %s"
                % get_configured_value("cli_testing.ci.distribution_branch"),
            },
        ),
        (
            ["--ci-command"],
            {
                "dest": "cli_testing.ci.command",
                "type": str,
                "help": "Sets the command to execute before each commit\n"
                "(except the final one). %s"
                % get_configured_value("cli_testing.ci.command"),
            },
        ),
        (
            ["--ci-end-command"],
            {
                "dest": "cli_testing.ci.end_command",
                "type": str,
                "help": "Sets the command to execute before the final commit. %s"
                % get_configured_value("cli_testing.ci.end_command"),
            },
        ),
        (
            ["--ci-commit-message"],
            {
                "dest": "cli_testing.ci.commit_message",
                "type": str,
                "help": "Sets the commit message to apply every time we have\n"
                "to apply a commit except for the really last one. %s"
                % get_configured_value("cli_testing.ci.commit_message"),
            },
        ),
        (
            [
                "--ci-end-commit-message",
            ],
            {
                "dest": "cli_testing.ci.end_commit_message",
                "type": str,
                "help": "Sets the commit message to apply at the really end. %s"
                % get_configured_value("cli_testing.ci.end_commit_message"),
            },
        ),
    ]


def get_default_group_data() -> List[Tuple[List[str], dict]]:
    """
    Provides the argument of the default group.
    """

    return [
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


def ask_authorization_to_merge_config(missing_key: Optional[str] = None) -> bool:
    """
    Asks the end-user for the authorization to merge the upstream
    configuration and - finally - return the new authorization status.

    :param missing_key:
        The name of a missing key. If not given, a more generic message will be
        given to end-user.
    """

    if missing_key:
        message = (
            f"{colorama.Fore.RED}{colorama.Style.BRIGHT}The {missing_key!r} "
            f"key is missing from your configuration file."
            f"{colorama.Style.RESET_ALL}\n"
            f"Are we authorized to merge it from upstream ? {colorama.Style.BRIGHT}"
            "[y/n] "
        )
    else:
        message = (
            f"{colorama.Fore.RED}{colorama.Style.BRIGHT}A "
            f"key is missing from your configuration file."
            f"{colorama.Style.RESET_ALL}\n"
            f"Are we authorized to merge it from upstream ? {colorama.Style.BRIGHT}"
            "[y/n] "
        )

    while True:
        response = input(message).lower()

        if response[0] not in ("y", "n"):
            continue

        if response[0] == "y":
            return True

        return False


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
        f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}PyFunceble"
        f"{colorama.Style.RESET_ALL} - "
        "The tool to check the availability or syntax of domain, IP or URL."
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

    # pylint:  disable=possibly-unused-variable

    source_group = parser.add_argument_group("Test sources")
    filtering_group = parser.add_argument_group(
        "Source filtering, decoding, conversion and expansion"
    )
    test_control_group = parser.add_argument_group("Test control")
    dns_control_group = parser.add_argument_group("DNS control")
    database_control_group = parser.add_argument_group("Databases")
    output_control_group = parser.add_argument_group("Output control")
    multiprocessing_group = parser.add_argument_group("Multiprocessing")
    ci_group = parser.add_argument_group("CI / CD")

    funcs = [
        get_source_group_data,
        get_filtering_group_data,
        get_test_control_group_data,
        get_dns_control_group_data,
        get_database_control_group_data,
        get_output_control_group_data,
        get_multiprocessing_group_data,
        get_ci_group_data,
    ]

    for func in funcs:
        parser_name = func.__name__.replace("get_", "").replace("_data", "")

        try:
            add_arguments_to_parser(locals()[parser_name], func())
        except ValueError as exception:
            exception_message = str(exception)
            if "configuration" not in exception_message:
                raise exception

            missing_key = RegexHelper(r"<entry>\s\(\'(.*)\'\)").match(
                exception_message, return_match=True, group=1
            )

            if ask_authorization_to_merge_config(missing_key):
                PyFunceble.facility.ConfigLoader.set_merge_upstream(True).start()
                add_arguments_to_parser(locals()[parser_name], func())
            else:
                print(
                    f"{colorama.Fore.RED}{colorama.Style.BRIGHT}Could not find "
                    f"the {missing_key!r} in your configuration.\n"
                    f"{colorama.Fore.MAGENTA}Please fix your "
                    "configuration file manually or fill a new issue if you "
                    "don't understand this error."
                )
                sys.exit(1)

    add_arguments_to_parser(parser, get_default_group_data())

    args = parser.parse_args()

    if any(getattr(args, x) for x in ["domains", "urls", "files", "url_files"]):
        SystemIntegrator(args).start()
        SystemLauncher(args).start()
