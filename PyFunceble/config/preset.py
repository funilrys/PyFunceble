# pylint: disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a way to preset the configuration before launching a specific test type.

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
# pylint: enable=line-too-long

from os import cpu_count

from colorama import Fore, Style

import PyFunceble


class Preset:  # pragma: no cover
    """
    Checks or update the global configuration based on some events.
    """

    # List all index which can be superset.
    # In other words if an index which is listed here
    # is also listed into PyFunceble.INTERN["custom_config_loaded"],
    # We do not update it.
    do_not_overwrite_if_customized = [
        "ci",
        "cooldown_time",
        "inactive_database",
        "no_files",
        "print_dots",
        "quiet",
        "reputation",
        "timeout",
        "use_reputation_data",
        "whois_database",
    ]

    def init_all(self):
        """
        Initiate all presets which are independent from others.
        """

        self.timeout()
        self.dns_lookup_over_tcp()
        self.dns_nameserver()

        self.cooldown_time()
        self.multiprocess()

        self.syntax_test()
        self.reputation_data()

        self.db_types()

    @classmethod
    def switch(
        cls, variable, custom=False
    ):  # pylint: disable=inconsistent-return-statements
        """
        Switches :code:`PyFunceble.CONFIGURATION` variables to their opposite.

        :param variable:
            The variable name to switch.
            The variable should be an index our configuration system.
            If we want to switch a bool variable, we should parse
            it here.
        :type variable: str|bool

        :param bool custom:
            Let us know if have to switch the parsed variable instead
            of our configuration index.

        :return:
            The opposite of the configuration index or the given variable.
        :rtype: bool

        :raises:
            :code:`Exception`
                When the configuration is not valid. In other words,
                if the PyFunceble.CONFIGURATION[variable_name] is not a bool.
        """

        if not custom:
            # We are not working with custom variable which is not into
            # the configuration.

            # We get the current state.
            current_state = dict.get(PyFunceble.CONFIGURATION, variable)
        else:
            # We are working with a custom variable which is not into the
            # configuration
            current_state = variable

        if isinstance(current_state, bool):
            # The current state is a boolean.

            if current_state:
                # The current state is equal to True.

                # We return False.
                return False

            # The current state is equal to False.

            # We return True.
            return True

        # The current state is not a boolean.

        # We set the message to raise.
        to_print = "Impossible to switch %s. Please post an issue to %s"

        # We raise an exception inviting the user to report an issue.
        raise Exception(to_print % (repr(variable), PyFunceble.LINKS.repo + "/issues."))

    @classmethod
    def __are_we_allowed_to_overwrite(cls, index):
        """
        Checks if we are allowed to overwrite an index.
        """

        return not (
            index in cls.do_not_overwrite_if_customized
            and PyFunceble.LOADER.custom_loaded
            and index in PyFunceble.LOADER.custom_loaded
        )

    @classmethod
    def disable(cls, indexes):
        """
        Sets the given configuration index to :code:`False`.
        """

        # pylint: disable=unsupported-membership-test,unsubscriptable-object,unsupported-assignment-operation

        if isinstance(indexes, list):
            for index in indexes:
                cls.disable(index)

            return None

        if not cls.__are_we_allowed_to_overwrite(indexes):
            PyFunceble.LOGGER.debug(f"Not allowed to switch {indexes}.")

            return None

        if indexes not in PyFunceble.CONFIGURATION or PyFunceble.CONFIGURATION[indexes]:
            PyFunceble.CONFIGURATION[indexes] = False

            PyFunceble.LOGGER.debug(
                f"CONFIGURATION.{indexes} switched to {PyFunceble.CONFIGURATION[indexes]}"
            )

            return None

        PyFunceble.LOGGER.debug(
            f"Not allowed to switch {indexes} because "
            "it is already to the right value. "
            f"({PyFunceble.CONFIGURATION[indexes]})"
        )

        return None

    @classmethod
    def enable(cls, indexes):
        """
        Sets the given configuration index to :code:`True`.
        """

        # pylint: disable=unsupported-membership-test,unsubscriptable-object,unsupported-assignment-operation

        if isinstance(indexes, list):
            for index in indexes:
                cls.enable(index)

            return None

        if not cls.__are_we_allowed_to_overwrite(indexes):
            PyFunceble.LOGGER.debug(f"Not allowed to switch {indexes}.")

            return None

        if (
            indexes not in PyFunceble.CONFIGURATION
            or not PyFunceble.CONFIGURATION[indexes]
        ):
            PyFunceble.CONFIGURATION[indexes] = True

            PyFunceble.LOGGER.debug(
                f"CONFIGURATION.{indexes} switched to {PyFunceble.CONFIGURATION[indexes]}"
            )
            return None

        PyFunceble.LOGGER.debug(
            f"Not allowed to switch {indexes} because "
            "it is already to the right value. "
            f"({PyFunceble.CONFIGURATION[indexes]})"
        )

        return None

    @classmethod
    def reset_counters(cls):
        """
        Resets the counters.
        """

        for status in ["up", "down", "invalid", "tested"]:
            # We loop through to the index of the autoContinue subsystem.

            # And we set the counter of the currently read status to 0.
            PyFunceble.INTERN["counter"]["number"][status] = 0
            PyFunceble.INTERN["counter"]["percentage"][status] = 0

        PyFunceble.LOGGER.debug("Counter resetted.")

    def syntax_test(self):
        """
        Disables the HTTP status code if we are
        testing for syntax
        """

        if PyFunceble.CONFIGURATION.syntax:
            # We are checking for syntax.

            # We deactivate the http status code.
            PyFunceble.HTTP_CODE.active = False

            should_be_disabled = ["generate_hosts", "reputation", "use_reputation_data"]
            should_be_enabled = ["plain_list_domain"]

            self.disable(should_be_disabled)
            self.enable(should_be_enabled)

    @classmethod
    def maximal_processes(cls):
        """
        Ensures that the number of maximal processes is alway >= 1.
        """

        if PyFunceble.CONFIGURATION.maximal_processes < 1:
            PyFunceble.CONFIGURATION.maximal_processes = 1

    @classmethod
    def db_types(cls):
        """
        Ensure that the files are downloaded when the db types is not
        the JSON one.
        """

        PyFunceble.downloader.DBType()

    @classmethod
    def multiprocess_merging_mode(cls):
        """
        Ensures that a valid merging mode is given.
        """

        # pylint: disable=line-too-long
        if not PyFunceble.CONFIGURATION.multiprocess_merging_mode or PyFunceble.CONFIGURATION.multiprocess_merging_mode.lower() not in [
            "end",
            "live",
        ]:
            PyFunceble.CONFIGURATION.multiprocess_merging_mode = "end"

        if PyFunceble.CONFIGURATION.db_type in ["mysql", "mariadb"]:
            PyFunceble.CONFIGURATION.multiprocess_merging_mode = "end"

    def simple_domain(self):
        """
        Prepares the global configuration for a domain
        test.
        """

        should_be_disabled = ["show_percentage", "whois_database"]

        for index in should_be_disabled:
            self.disable(index)

    def simple_url(self):
        """
        Prepares the global configuration for an URL test.
        """

        should_be_disabled = ["show_percentage", "whois_database"]

        self.disable(should_be_disabled)

    def complements(self):
        """
        Prepares the global configuration for a complements generation.
        """

        should_be_enabled = ["auto_continue"]

        self.enable(should_be_enabled)

    def file_url(self):
        """
        Prepares the global configuration for a list of URL to test.
        """

        should_be_disabled = ["generate_hosts"]
        should_be_enabled = ["no_whois", "plain_list_domain", "split"]

        self.disable(should_be_disabled)
        self.enable(should_be_enabled)

    def api(self):
        """
        Prepares the global configuration for a test from the API.
        """

        should_be_disabled = [
            "inactive_database",
            "auto_continue",
            "show_execution_time",
        ]
        should_be_enabled = ["quiet", "whois_database", "no_files"]

        self.disable(should_be_disabled)
        self.enable(should_be_enabled)

        if PyFunceble.CONFIGURATION.api_file_generation:
            PyFunceble.CONFIGURATION.no_files = False

    def multiprocess(self):
        """
        Prepares the global configuration for a test with multiple processes.
        """

        if PyFunceble.CONFIGURATION.multiprocess:
            if (
                "multiprocess_warning_printed" not in PyFunceble.INTERN
                and not PyFunceble.CONFIGURATION.simple
                and not PyFunceble.CONFIGURATION.quiet
            ):
                if PyFunceble.CONFIGURATION.db_type not in ["mysql", "mariadb"]:
                    print(
                        f"{Fore.RED + Style.BRIGHT}The "
                        f"{repr(PyFunceble.CONFIGURATION.db_type)} database type "
                        "is not recommended with the multiprocessing mode."
                    )

                available_cpu = cpu_count()

                if PyFunceble.CONFIGURATION.maximal_processes > available_cpu:
                    print(
                        f"{Fore.RED + Style.BRIGHT}You're using more processes "
                        f"({repr(PyFunceble.CONFIGURATION.maximal_processes)}) than "
                        f"the number of available CPU ({available_cpu}). Use at your own risk!"
                    )

                PyFunceble.INTERN["multiprocess_warning_printed"] = True
            self.maximal_processes()
            self.multiprocess_merging_mode()

    @classmethod
    def timeout(cls):
        """
        Ensures that the timeout is always correct.
        """

        if cls.__are_we_allowed_to_overwrite("timeout") and (
            not PyFunceble.CONFIGURATION.timeout or PyFunceble.CONFIGURATION.timeout < 0
        ):
            PyFunceble.CONFIGURATION.timeout = float(3)

            PyFunceble.LOGGER.debug(
                f"CONFIGURATION.timeout switched to {PyFunceble.CONFIGURATION.timeout}"
            )

        if not isinstance(PyFunceble.CONFIGURATION.timeout, float):
            PyFunceble.CONFIGURATION.timeout = float(PyFunceble.CONFIGURATION.timeout)

            PyFunceble.LOGGER.debug(
                f"CONFIGURATION.timeout switched to {PyFunceble.CONFIGURATION.timeout}"
            )

        PyFunceble.DNSLOOKUP.update_lifetime(PyFunceble.CONFIGURATION.timeout)

    @classmethod
    def dns_lookup_over_tcp(cls):
        """
        Ensures that the DNS lookup over tcp is proprely set.
        """

        PyFunceble.DNSLOOKUP.tcp = PyFunceble.CONFIGURATION.dns_lookup_over_tcp

    @classmethod
    def dns_nameserver(cls):
        """
        Ensures that the DNS nameserver is proprely set.
        """

        PyFunceble.DNSLOOKUP.update_nameserver(PyFunceble.CONFIGURATION.dns_server)

    def reputation_data(self):
        """
        Ensures that the usage of reputation data is activated when needed.
        """

        if PyFunceble.CONFIGURATION.reputation:
            should_be_enabled = ["use_reputation_data", "no_whois", "plain_list_domain"]
            should_be_disabled = ["whois_database", "inactive_database", "mining"]

            self.enable(should_be_enabled)
            self.disable(should_be_disabled)

            PyFunceble.HTTP_CODE.active = False

    def cooldown_time(self):
        """
        Ensures that we always have a correct cooldown time.
        """

        if (
            self.__are_we_allowed_to_overwrite("cooldown_time")
            and PyFunceble.CONFIGURATION.cooldown_time
            and not isinstance(PyFunceble.CONFIGURATION.cooldown_time, float)
        ):
            PyFunceble.CONFIGURATION.cooldown_time = float(
                PyFunceble.CONFIGURATION.cooldown_time
            )
