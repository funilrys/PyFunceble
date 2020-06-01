"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the CLI core interface.

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

import sys
from datetime import datetime, timezone
from os import sep as directory_separator
from os import walk
from random import choice

from colorama import Fore, Style

import PyFunceble


class CLICore:
    """
    Provides some methods which are dedicated for the CLI.
    """

    def __init__(self):
        self.list_of_up_statuses = PyFunceble.STATUS.list.up
        self.list_of_up_statuses.extend(PyFunceble.STATUS.list.valid)
        self.list_of_up_statuses.extend(PyFunceble.STATUS.list.sane)

        self.preset = PyFunceble.cconfig.Preset()
        self.preset.init_all()

        self.autosave = PyFunceble.engine.AutoSave(
            start_time=PyFunceble.INTERN["start"]
        )
        self.whois_db = PyFunceble.database.Whois(parent_process=True)

        # We initiate a variable which will tell us when
        # we start testing for complements.
        self.complements_test_started = False

    @classmethod
    def sort_generated_files(cls):  # pragma: no cover
        """
        Sort the content of all files we generated.
        """

        header_limit = 3

        for root, _, files in walk(
            PyFunceble.OUTPUT_DIRECTORY + PyFunceble.OUTPUTS.parent_directory
        ):
            # We loop through the list of directories of the output directory.

            for file in files:
                # We loop through the list of file of the
                # currently read directory.

                if file.endswith(".json"):
                    # The currently read filename ends
                    # with .json.

                    # We continue the loop.
                    continue

                if file in [".keep", ".gitignore"]:
                    # The currently read filename is
                    # into a list of filename that are not relevant
                    # for us.

                    # We continue the loop.
                    continue

                if f"{directory_separator}logs" in root:
                    # The currently read root should be ignored.

                    continue

                if f"{directory_separator}splited" in root:
                    header_limit += 1

                # We create an instance of our File().
                file_instance = PyFunceble.helpers.File(
                    "{0}{1}{2}".format(root, directory_separator, file)
                )
                # We get the content of the current file.
                file_content = file_instance.read().splitlines()

                if not PyFunceble.CONFIGURATION.hierarchical_sorting:
                    # We do not have to sort hierarchicaly.

                    # We sort the lines of the file standarly.
                    formatted = PyFunceble.helpers.List(
                        file_content[header_limit:]
                    ).custom_format(PyFunceble.engine.Sort.standard)
                else:
                    # We do have to sort hierarchicaly.

                    # We sort the lines of the file hierarchicaly.
                    formatted = PyFunceble.helpers.List(
                        file_content[header_limit:]
                    ).custom_format(PyFunceble.engine.Sort.hierarchical)

                # We finally put the formatted data in place.
                to_write = file_content[:header_limit]
                to_write.extend(formatted)
                to_write.append("")

                file_instance.write("\n".join(to_write), overwrite=True)

    @classmethod
    def save_into_database(cls, output, filename):  # pragma: no cover
        """
        Saves the current status inside the database.
        """

        if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
            table_name = PyFunceble.engine.MySQL.tables["tested"]

            if not filename:
                filename = "simple"

            to_insert = (
                "INSERT INTO {0} "
                "(tested, file_path, _status, status, _status_source, status_source, "
                "domain_syntax_validation, expiration_date, http_status_code, "
                "ipv4_range_syntax_validation, ipv4_syntax_validation, "
                "ipv6_range_syntax_validation, ipv6_syntax_validation, "
                "subdomain_syntax_validation, url_syntax_validation, whois_server, digest) "
                "VALUES (%(tested)s, %(file_path)s, %(_status)s, %(status)s, %(_status_source)s, "
                "%(status_source)s, %(domain_syntax_validation)s, "
                "%(expiration_date)s, %(http_status_code)s, "
                "%(ipv4_range_syntax_validation)s, %(ipv4_syntax_validation)s, "
                "%(ipv6_range_syntax_validation)s, %(ipv6_syntax_validation)s, "
                "%(subdomain_syntax_validation)s, "
                "%(url_syntax_validation)s, %(whois_server)s, %(digest)s)"
            ).format(table_name)

            to_update = (
                "UPDATE {0} SET _status = %(_status)s, status = %(status)s, "
                "_status_source = %(_status_source)s, status_source = %(status_source)s, "
                "domain_syntax_validation = %(domain_syntax_validation)s, "
                "expiration_date = %(expiration_date)s, http_status_code = %(http_status_code)s, "
                "ipv4_range_syntax_validation = %(ipv4_range_syntax_validation)s, "
                "ipv4_syntax_validation = %(ipv4_syntax_validation)s, "
                "ipv6_range_syntax_validation = %(ipv6_range_syntax_validation)s, "
                "ipv6_syntax_validation = %(ipv6_syntax_validation)s, "
                "subdomain_syntax_validation = %(subdomain_syntax_validation)s, "
                "url_syntax_validation = %(url_syntax_validation)s, "
                "whois_server = %(whois_server)s "
                "WHERE digest = %(digest)s"
            ).format(table_name)

            with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
                to_set = PyFunceble.helpers.Merge({"file_path": filename}).into(output)

                to_set["digest"] = PyFunceble.helpers.Hash(algo="sha256").data(
                    bytes(to_set["file_path"] + to_set["tested"], "utf-8")
                )

                if (
                    isinstance(to_set["http_status_code"], str)
                    and not to_set["http_status_code"].isdigit()
                ):
                    to_set["http_status_code"] = None

                try:
                    cursor.execute(to_insert, to_set)
                except PyFunceble.engine.MySQL.errors:
                    cursor.execute(to_update, to_set)

                PyFunceble.LOGGER.debug(
                    f"Saved into the {repr(table_name)} table:\n{to_set}"
                )

    @classmethod
    def get_simple_coloration(cls, status):
        """
        Given a status we give the coloration for the simple mode.

        :param str status: An official status output.
        """

        if status in [
            PyFunceble.STATUS.official.up,
            PyFunceble.STATUS.official.valid,
            PyFunceble.STATUS.official.sane,
        ]:
            # The status is in the list of UP status.

            # We return the green coloration.
            return Fore.GREEN + Style.BRIGHT

        if status in [
            PyFunceble.STATUS.official.down,
            PyFunceble.STATUS.official.malicious,
        ]:
            # The status is in the list of DOWN status.

            # We return the red coloration.
            return Fore.RED + Style.BRIGHT

        # The status is not in the list of UP nor DOWN status.

        # We return the cyam coloration.
        return Fore.CYAN + Style.BRIGHT

    @classmethod
    def colorify_logo(cls, home=False):
        """
        Print the colored logo based on global results.

        :param bool home: Tell us if we have to print the initial coloration.
        """

        if not PyFunceble.CONFIGURATION.quiet and not PyFunceble.CONFIGURATION.simple:
            # The quiet mode is not activated.

            to_print = []

            if home:
                # We have to print the initial logo.

                for line in PyFunceble.ASCII_PYFUNCEBLE.split("\n"):
                    # We loop through each lines of the ASCII representation
                    # of PyFunceble.

                    # And we append to the data to print the currently read
                    # line with the right coloration.
                    to_print.append(Fore.YELLOW + line + Fore.RESET)

            elif (
                PyFunceble.INTERN["counter"]["percentage"]["up"] >= 50
                or (
                    "valid" in PyFunceble.INTERN["counter"]["percentage"]
                    and PyFunceble.INTERN["counter"]["percentage"]["valid"] >= 50
                )
                or (
                    "sane" in PyFunceble.INTERN["counter"]["percentage"]
                    and PyFunceble.INTERN["counter"]["percentage"]["sane"] >= 50
                )
            ):
                # The percentage of up is greater or equal to 50%.

                for line in PyFunceble.ASCII_PYFUNCEBLE.split("\n"):
                    # We loop through each lines of the ASCII representation
                    # of PyFunceble.

                    # And we append to the data to print the currently read
                    # line with the right coloration.
                    to_print.append(Fore.GREEN + line + Fore.RESET)
            else:
                # The percentage of up is less than 50%.

                for line in PyFunceble.ASCII_PYFUNCEBLE.split("\n"):
                    # We loop through each lines of the ASCII representation
                    # of PyFunceble.

                    # And we append to the data to print the currently read
                    # line with the right coloration.
                    to_print.append(Fore.RED + line + Fore.RESET)

            print("\n".join(to_print))

    @classmethod
    def print_header(cls):  # pragma: no cover
        """
        Prints the header if needed.
        """

        if (
            not PyFunceble.CONFIGURATION.quiet
            and not PyFunceble.CONFIGURATION.header_printed
            and not PyFunceble.CONFIGURATION.simple
        ):
            # * The quiet mode is not activated.
            # and
            # * The header has not been already printed.

            # We print a new line.
            print("\n")

            if PyFunceble.CONFIGURATION.less and not PyFunceble.CONFIGURATION.simple:
                # We have to show less informations on screen.

                # We print the `Less` header.
                PyFunceble.output.Prints(None, "Less").header()
            elif not PyFunceble.CONFIGURATION.simple:
                # We have to show every informations on screen.

                # We print the `Generic` header.
                PyFunceble.output.Prints(None, "Generic").header()

            # The header was printed.

            # We initiate the variable which say that the header has been printed to True.
            PyFunceble.CONFIGURATION.header_printed = True

    @classmethod
    def print_nothing_to_test(cls):
        """
        Prints the nothing to test message.
        """

        print(Fore.CYAN + Style.BRIGHT + "Nothing to test.")

    @classmethod
    def stay_safe(cls):
        """
        Prints a friendly message.
        """

        random = int(choice(str(int(datetime.now().timestamp()))))

        if not PyFunceble.CONFIGURATION.quiet and not PyFunceble.CONFIGURATION.simple:
            print("\n" + Fore.GREEN + Style.BRIGHT + "Thanks for using PyFunceble!")

            if random % 3 == 0:
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
                    + "Have a feedback, an issue or an improvement idea?"
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

    @classmethod
    def logs_sharing(cls):
        """
        Prints an information message when the logs sharing
        is activated.
        """

        if PyFunceble.CONFIGURATION.share_logs:
            print(Fore.GREEN + Style.BRIGHT + "You are sharing your logs!")
            print(
                Fore.MAGENTA + Style.BRIGHT + "Please find more about it at "
                "https://pyfunceble.readthedocs.io/en/dev/logs-sharing.html !"
            )

    @classmethod
    def get_upstream_version_file(cls):  # pragma: no cover
        """
        Provides the upstream version file.
        """

        # We initiate the link to the upstream version file.
        # It is hard coded because we may not have the chance to have the
        # configuration file everytime we need it.
        upstream_link = "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/version.yaml"  # pylint: disable=line-too-long

        upstream_link = PyFunceble.converter.InternalUrl(upstream_link).get_converted()

        return PyFunceble.helpers.Dict().from_yaml(
            PyFunceble.helpers.Download(upstream_link).text()
        )

    @classmethod
    def __check_force_update(cls, upstream_version):  # pragma: no cover
        """
        Checks if we need to force the update.

        If it's the case, we will stop the tool.
        """

        if upstream_version["force_update"]["status"]:
            for minimal in upstream_version["force_update"]["minimal_version"]:
                # We loop through the list of minimal version which trigger the
                # the force update message.

                # We compare the local with the currently read minimal version.
                checked = PyFunceble.abstracts.Version.compare(minimal)

                if not PyFunceble.CONFIGURATION.quiet:
                    # The quiet mode is not activated.

                    if checked or checked is not False and not checked:
                        # The current version is less or equal to
                        # the minimal version.

                        # We initiate the message we are going to return to
                        # the user.
                        message = (
                            Style.BRIGHT
                            + Fore.RED
                            + "A critical issue has been fixed.\n"
                            + Style.RESET_ALL
                        )  # pylint:disable=line-too-long
                        message += (
                            Style.BRIGHT
                            + Fore.GREEN
                            + "Please take the time to update PyFunceble!\n"
                            + Style.RESET_ALL
                        )  # pylint:disable=line-too-long

                        # We print the message on screen.
                        print(message)

                        # We exit PyFunceble with the code 1.
                        sys.exit(1)
                elif checked or checked is not False and not checked:
                    # The quiet mode is activated and the current version
                    # is less or equal to the minimal version.

                    # We raise an exception telling the user to update their
                    # instance of PyFunceble.
                    raise PyFunceble.exceptions.PleaseUpdatePyFunceble(
                        "A critical issue has been fixed. Please take the time to update PyFunceble!"  # pylint:disable=line-too-long
                    )

    @classmethod
    def __check_deprecated(cls, upstream_version):  # pragma: no cover
        """
        Checks if the local version is deprecated.
        """

        for version in reversed(upstream_version["deprecated"]):
            # We loop through the list of deprecated versions.

            # We compare the local with the currently read deprecated version.
            checked = PyFunceble.abstracts.Version.compare(version)

            if (
                not PyFunceble.CONFIGURATION.quiet
                and checked
                or checked is not False
                and not checked
            ):
                # The quiet mode is not activated and the local version is
                # less or equal to the currently read deprecated version.

                # We initiate the message we are going to return to the user.
                message = (
                    Style.BRIGHT
                    + Fore.RED
                    + "Your current version is considered as deprecated.\n"
                    + Style.RESET_ALL
                )  # pylint:disable=line-too-long
                message += (
                    Style.BRIGHT
                    + Fore.GREEN
                    + "Please take the time to update PyFunceble!\n"
                    + Style.RESET_ALL
                )  # pylint:disable=line-too-long

                # We print the message.
                print(message)

                # And we continue to the next logic. There is no need to
                # shutdown PyFunceble as it's just for information.
                return False

            # The quiet mode is activated.

            if checked or checked is not False and not checked:
                # The local version is  less or equal to the currently
                # read deprecated version.
                print("Version deprecated.")

                # And we continue to the next logic. There is no need to
                # shutdown PyFunceble as it's just for information.
                return False
        return True

    @classmethod
    def __print_messages(cls, upstream_version):  # pragma: no cover
        """
        Looks at the messages and prints the one that needs to be
        printed.
        """

        iso_dateformat = "%Y-%m-%dT%H:%M:%S%z"

        if (
            "messages" in upstream_version
            and not PyFunceble.CONFIGURATION.simple
            and not PyFunceble.CONFIGURATION.quiet
        ):
            messages = upstream_version["messages"]
            local_timezone = datetime.now(timezone.utc).astimezone().tzinfo

            for minimal_version, data in messages.items():
                comparison = PyFunceble.abstracts.Version.compare(minimal_version)
                until_date = None
                until_comparison = None

                for single_message in data:
                    if "until_date" in single_message:
                        try:
                            until_date = (
                                datetime.strptime(
                                    single_message["until_date"], iso_dateformat
                                )
                                - datetime.now(tz=local_timezone)
                            ).days
                        except ValueError:
                            until_date = 0

                    if "until" in single_message:
                        until_comparison = PyFunceble.abstracts.Version.compare(
                            single_message["until"]
                        )

                    if "type" in single_message:
                        if single_message["type"] == "info":
                            coloration = Fore.YELLOW + Style.BRIGHT
                        elif single_message["type"] == "warning":
                            coloration = Fore.MAGENTA + Style.BRIGHT
                        else:
                            coloration = Fore.BLUE + Style.BRIGHT
                    else:
                        coloration = Fore.CYAN + Style.BRIGHT

                    if (
                        (comparison is False or comparison is None)
                        and until_comparison is True
                        or (until_date is not None and until_date > 0)
                    ):

                        print(f"{coloration}{single_message['message']}")

    @classmethod
    def compare_version_and_print_messages(cls):  # pragma: no cover
        """
        Compares the local with the upstream version.
        """

        upstream_version = cls.get_upstream_version_file()

        cls.__check_force_update(upstream_version)

        if cls.__check_deprecated(upstream_version):
            # We compare the local version with the upstream version.
            status = PyFunceble.abstracts.Version.compare(
                upstream_version["current_version"]
            )

            if (
                status is not None
                and not status
                and not PyFunceble.CONFIGURATION.quiet
                and not PyFunceble.CONFIGURATION.simple
            ):
                # The quiet mode is not activate and the current version is greater than
                # the upstream version.

                # We initiate the message we are going to return to the user.
                message = (
                    Style.BRIGHT
                    + Fore.CYAN
                    + "Your version is more recent!\nYou should really think about sharing your changes with the community!\n"  # pylint:disable=line-too-long
                    + Style.RESET_ALL
                )
                message += (
                    Style.BRIGHT
                    + "Your version: "
                    + Style.RESET_ALL
                    + PyFunceble.VERSION
                    + "\n"
                )
                message += (
                    Style.BRIGHT
                    + "Upstream version: "
                    + Style.RESET_ALL
                    + upstream_version["current_version"]
                    + "\n"
                )

                # We print the message.
                print(message)
            elif status and not PyFunceble.CONFIGURATION.simple:
                # The current version is less that the upstream version.

                if not PyFunceble.CONFIGURATION.quiet:
                    # The quiet mode is not activated.

                    # We initiate the message we are going to return to the user.
                    message = (
                        Style.BRIGHT
                        + Fore.YELLOW
                        + "Please take the time to update PyFunceble!\n"
                        + Style.RESET_ALL
                    )  # pylint:disable=line-too-long
                    message += (
                        Style.BRIGHT
                        + "Your version: "
                        + Style.RESET_ALL
                        + PyFunceble.VERSION
                        + "\n"
                    )  # pylint:disable=line-too-long
                    message += (
                        Style.BRIGHT
                        + "Upstream version: "
                        + Style.RESET_ALL
                        + upstream_version[  # pylint:disable=line-too-long
                            "current_version"
                        ]
                        + "\n"
                    )

                    # We print the message.
                    print(message)
                else:
                    # The quiet mode is activated.

                    # We print the message.
                    print("New version available.")

        cls.__print_messages(upstream_version)

        # One may use the following as behavior debugger.
        # cls.__print_messages(PyFunceble.helpers.Dict().from_yaml_file("version.yaml"))
