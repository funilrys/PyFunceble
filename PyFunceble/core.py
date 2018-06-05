#!/usr/bin/env python3
"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This module is half of the brain of PyFunceble.


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on 13th March, 2018.

Its main objective is to get and the return domains and IPs availability by
generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

In its daily usage, PyFunceble is mostly used to clean `hosts` files or blocklist.
Indeed, it is possible because PyFunceble generates a list of all `ACTIVE` domains
or IPs but in the same time, it creates by default a database of the `INACTIVE`
domains or IPs so we can retest them overtime automatically at the next execution.

PyFunceble is running actively and daily with the help of Travis CI under 60+
repositories. It is used to clean or test the availability of data which are
present in hosts files, list of IP, list of domains, blocklists or even AdBlock
filter lists.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
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
# pylint: disable=bad-continuation

import PyFunceble
from PyFunceble import Fore, path, repeat
from PyFunceble.auto_continue import AutoContinue
from PyFunceble.auto_save import AutoSave
from PyFunceble.database import Database
from PyFunceble.execution_time import ExecutionTime
from PyFunceble.expiration_date import ExpirationDate
from PyFunceble.helpers import Command, Download, List, Regex
from PyFunceble.percentage import Percentage
from PyFunceble.prints import Prints
from PyFunceble.url import URL


class Core(object):  # pragma: no cover
    """
    Main entry to PYFunceble. Brain of the program. Also known as "put everything
    together to make the system works".

    Arguments:
        - domain: str
            A domain or IP to test.
        - file_path: str
            A path to a file to read.
    """

    def __init__(self, domain=None, file_path=None, **args):

        optional_arguments = {
            "url_to_test": None,
            "file_urls": None,
            "modulo_test": False,
            "link_to_test": None,
        }

        # We initiate our optional_arguments in order to be usable all over the
        # class
        for (arg, default) in optional_arguments.items():
            setattr(self, arg, args.get(arg, default))

        if not self.modulo_test:  # pylint: disable=no-member

            PyFunceble.CONFIGURATION[
                "file_to_test"
            ] = file_path  # pylint: disable=no-member

            if self.file_urls:  # pylint: disable=no-member
                PyFunceble.CONFIGURATION[
                    "file_to_test"
                ] = self.file_urls  # pylint: disable=no-member

            if PyFunceble.CONFIGURATION["travis"]:
                AutoSave().travis_permissions()

            self.bypass()
            ExecutionTime("start")

            if domain:
                PyFunceble.CONFIGURATION["show_percentage"] = False
                PyFunceble.CONFIGURATION["domain"] = domain.lower()
                self.domain()
            elif self.url_to_test and not file_path:  # pylint: disable=no-member
                PyFunceble.CONFIGURATION["show_percentage"] = False
                PyFunceble.CONFIGURATION[
                    "URL"
                ] = self.url_to_test  # pylint: disable=no-member
                self.url()
            elif self.file_urls:  # pylint: disable=no-member
                PyFunceble.CONFIGURATION["no_whois"] = PyFunceble.CONFIGURATION[
                    "plain_list_domain"
                ] = PyFunceble.CONFIGURATION[
                    "split"
                ] = True
                PyFunceble.CONFIGURATION["generate_hosts"] = False

                self.url_file()
            elif file_path:
                self.file()
            elif self.link_to_test and self.link_to_test.startswith(  # pylint: disable=no-member
                "http"
            ):
                file_to_test = self.link_to_test.split(  # pylint: disable=no-member
                    "/"
                )[
                    -1
                ]
                Download(
                    self.link_to_test, file_to_test  # pylint: disable=no-member
                ).text()

                PyFunceble.CONFIGURATION["file_to_test"] = file_to_test

                self.file()

            ExecutionTime("stop")
            Percentage().log()

            if domain:
                self.colored_logo()
        else:
            PyFunceble.CONFIGURATION["simple"] = True
            PyFunceble.CONFIGURATION["quiet"] = True
            PyFunceble.CONFIGURATION["no_files"] = True

            if domain:
                PyFunceble.CONFIGURATION["domain"] = domain.lower()

    def test(self):
        """
        This method avoid confusion between self.domain which is called into
        __main__ and test() which should be called out of PyFunceble's scope.

        Returns: str
            ACTIVE, INACTIVE or INVALID.

        Raise:
            - Exception: when this method is called under __name___
        """

        if not self.modulo_test:  # pylint: disable=no-member
            raise Exception(
                "You should not use this method. Please prefer self.domain()"
            )

        else:
            return ExpirationDate().get()

    @classmethod
    def bypass(cls):
        """
        Exit the script if `[PyFunceble skip]` is matched into the latest
        commit message.
        """

        regex_bypass = r"\[PyFunceble\sskip\]"

        if PyFunceble.CONFIGURATION["travis"] and Regex(
            Command("git log -1").execute(), regex_bypass, return_data=False
        ).match():

            AutoSave(True, is_bypass=True)

    @classmethod
    def print_header(cls):
        """
        Decide if we print or not the header.
        """

        if not PyFunceble.CONFIGURATION["quiet"] and not PyFunceble.CONFIGURATION[
            "header_printed"
        ]:
            print("\n")
            if PyFunceble.CONFIGURATION["less"]:
                Prints(None, "Less").header()
            else:
                Prints(None, "Generic").header()

            PyFunceble.CONFIGURATION["header_printed"] = True

    def _file_decision(self, current, last, status=None):
        """
        Manage the database, autosave and autocontinue systems for the case that we are reading
        a file.

        Arguments:
            - status: str
                The current status of current.
            - current: str
                The current domain or URL we are testing.
            - last: str
                The last domain or URL of the file we are testing.
        """

        if status:
            if not PyFunceble.CONFIGURATION["simple"] and PyFunceble.CONFIGURATION[
                "file_to_test"
            ]:
                if PyFunceble.CONFIGURATION["inactive_database"]:
                    if status.lower() in PyFunceble.STATUS["list"]["up"]:
                        Database().remove()
                    else:
                        Database().add()

                AutoContinue().backup()

                if current != last:
                    AutoSave()
                else:
                    ExecutionTime("stop")
                    Percentage().log()
                    self.reset_counters()
                    AutoContinue().backup()

                    self.colored_logo()

                    AutoSave(True)

        for index in ["http_code", "referer"]:
            if index in PyFunceble.CONFIGURATION:
                PyFunceble.CONFIGURATION[index] = ""

    def domain(self, domain=None, last_domain=None):
        """
        Manage the case that we want to test only a domain.

        Argument:
            - domain: str
                The domain or IP to test.
            - last_domain: str
                The last domain of the file we are testing.
        """

        if domain:
            PyFunceble.CONFIGURATION["domain"] = self._format_domain(domain)
        self.print_header()

        if __name__ == "PyFunceble.core":
            if PyFunceble.CONFIGURATION["simple"]:
                print(ExpirationDate().get())
            else:
                status = ExpirationDate().get()

            self._file_decision(domain, last_domain, status)
        else:
            ExpirationDate().get()
            return

    @classmethod
    def reset_counters(cls):
        """
        Reset the counters when needed.
        """

        for string in ["up", "down", "invalid", "tested"]:
            PyFunceble.CONFIGURATION["counter"]["number"].update({string: 0})
        return

    @classmethod
    def colored_logo(cls):
        """
        This method print the colored logo based on global results.
        """

        if not PyFunceble.CONFIGURATION["quiet"]:
            if PyFunceble.CONFIGURATION["counter"]["percentage"]["up"] >= 50:
                print(Fore.GREEN + PyFunceble.ASCII_PYFUNCEBLE)
            else:
                print(Fore.RED + PyFunceble.ASCII_PYFUNCEBLE)

    @classmethod
    def _format_domain(cls, extracted_domain):
        """
        Format the extracted domain before passing it to the system.

        Argument:
            extracted_domain: str
                The extracted domain from the file.

        Returns: str
            The domain to test.
        """

        if not extracted_domain.startswith("#"):

            if "#" in extracted_domain:
                extracted_domain = extracted_domain[:extracted_domain.find("#")].strip()

            if " " in extracted_domain or "\t" in extracted_domain:
                splited_line = extracted_domain.split()

                index = 1
                while index < len(splited_line):
                    if splited_line[index]:
                        break

                    index += 1

                return splited_line[index]

            return extracted_domain

        return ""

    @classmethod
    def _format_adblock_decoded(cls, to_format, result=None):
        """
        Format the exctracted adblock line before passing it to the system.

        Arguments:
            - to_format: str
                The extracted line from the file.
            - result: None or list
                The list of extracted domain.

        Returns: list
            The list of extracted domains.
        """

        if not result:
            result = []

        for data in List(to_format).format():
            if data:
                if "#" in data:
                    return cls._format_adblock_decoded(data.split("#"), result)

                elif "," in data:
                    return cls._format_adblock_decoded(data.split(","), result)

                elif "~" in data:
                    return cls._format_adblock_decoded(data.split("~"), result)

                elif "!" in data:
                    return cls._format_adblock_decoded(data.split("!"), result)

                elif "|" in data:
                    return cls._format_adblock_decoded(data.split("|"), result)

                elif data and (
                    ExpirationDate.is_domain_valid(data)
                    or ExpirationDate.is_ip_valid(data)
                ):
                    result.append(data)

        return result

    def adblock_decode(self, list_to_test):
        """
        Convert the adblock format into a readable format which is understood
        by the system.

        Argument:
            - list_to_test: list
                The read content of the given file.

        Returns: list
            The list of domain to test.
        """

        result = []
        regex = r"^(?:.*\|\|)([^\/\$\^]{1,}).*$"
        regex_v2 = r"(.*\..*)(?:#{1,}.*)"

        for line in list_to_test:
            rematch = Regex(
                line, regex, return_data=True, rematch=True, group=0
            ).match()

            rematch_v2 = Regex(
                line, regex_v2, return_data=True, rematch=True, group=0
            ).match()

            if rematch:
                result.extend(rematch)

            if rematch_v2:
                result.extend(List(self._format_adblock_decoded(rematch_v2)).format())

        return result

    @classmethod
    def _extract_domain_from_file(cls):
        """
        This method extract all non commented lines.

        Returns: list
            Each line of the file == an element of the list.
        """

        result = []

        if path.isfile(PyFunceble.CONFIGURATION["file_to_test"]):
            with open(PyFunceble.CONFIGURATION["file_to_test"]) as file:
                for line in file:
                    if not line.startswith("#"):
                        result.append(line.rstrip("\n").strip())
        else:
            raise FileNotFoundError(PyFunceble.CONFIGURATION["file_to_test"])

        return result

    def file(self):
        """
        Manage the case that need to test each domain of a given file path.
        Note: 1 domain per line.
        """

        list_to_test = self._extract_domain_from_file()

        AutoContinue().restore()

        if PyFunceble.CONFIGURATION["adblock"]:
            list_to_test = self.adblock_decode(list_to_test)
        else:
            list_to_test = list(map(self._format_domain, list_to_test))

        PyFunceble.Clean(list_to_test)

        if PyFunceble.CONFIGURATION["inactive_database"]:
            Database().to_test()

            if PyFunceble.CONFIGURATION["file_to_test"] in PyFunceble.CONFIGURATION[
                "inactive_db"
            ] and "to_test" in PyFunceble.CONFIGURATION[
                "inactive_db"
            ][
                PyFunceble.CONFIGURATION["file_to_test"]
            ] and PyFunceble.CONFIGURATION[
                "inactive_db"
            ][
                PyFunceble.CONFIGURATION["file_to_test"]
            ][
                "to_test"
            ]:
                list_to_test.extend(
                    PyFunceble.CONFIGURATION["inactive_db"][
                        PyFunceble.CONFIGURATION["file_to_test"]
                    ][
                        "to_test"
                    ]
                )

        regex_delete = r"localhost$|localdomain$|local$|broadcasthost$|0\.0\.0\.0$|allhosts$|allnodes$|allrouters$|localnet$|loopback$|mcastprefix$"  # pylint: disable=line-too-long

        list_to_test = List(
            Regex(list_to_test, regex_delete).not_matching_list()
        ).format()

        if PyFunceble.CONFIGURATION["filter"]:
            list_to_test = List(
                Regex(
                    list_to_test, PyFunceble.CONFIGURATION["filter"], escape=True
                ).matching_list()
            ).format()

        list(
            map(
                self.domain,
                list_to_test[PyFunceble.CONFIGURATION["counter"]["number"]["tested"]:],
                repeat(list_to_test[-1]),
            )
        )

    def url(self, url_to_test=None, last_url=None):
        """
        Manage the case that we want to test only a given url.

        Arguments:
            - url_to_test: str
                The url to test.
            - last_url: str
                The last url of the file we are testing.
        """

        if url_to_test:
            PyFunceble.CONFIGURATION["URL"] = url_to_test
        self.print_header()

        if __name__ == "PyFunceble.core":
            if PyFunceble.CONFIGURATION["simple"]:
                print(URL().get())
            else:
                status = URL().get()

            self._file_decision(url_to_test, last_url, status)
        else:
            URL().get()
            return

    def url_file(self):
        """
        Manage the case that we have to test a file
        Note: 1 URL per line.
        """

        list_to_test = self._extract_domain_from_file()

        AutoContinue().restore()

        PyFunceble.Clean(list_to_test)

        if PyFunceble.CONFIGURATION["inactive_database"]:
            Database().to_test()

            if PyFunceble.CONFIGURATION["file_to_test"] in PyFunceble.CONFIGURATION[
                "inactive_db"
            ] and "to_test" in PyFunceble.CONFIGURATION[
                "inactive_db"
            ][
                PyFunceble.CONFIGURATION["file_to_test"]
            ] and PyFunceble.CONFIGURATION[
                "inactive_db"
            ][
                PyFunceble.CONFIGURATION["file_to_test"]
            ][
                "to_test"
            ]:
                list_to_test.extend(
                    PyFunceble.CONFIGURATION["inactive_db"][
                        PyFunceble.CONFIGURATION["file_to_test"]
                    ][
                        "to_test"
                    ]
                )

        if PyFunceble.CONFIGURATION["filter"]:
            list_to_test = List(
                Regex(
                    list_to_test, PyFunceble.CONFIGURATION["filter"], escape=True
                ).matching_list()
            ).format()

        list(
            map(
                self.url,
                list_to_test[PyFunceble.CONFIGURATION["counter"]["number"]["tested"]:],
                repeat(list_to_test[-1]),
            )
        )

    @classmethod
    def switch(
        cls, variable, custom=False
    ):  # pylint: disable=inconsistent-return-statements
        """
        Switch PyFunceble.CONFIGURATION variables to their opposite.

        Arguments:
            - variable: str
                The PyFunceble.CONFIGURATION[variable_name] to switch.
            - custom: bool
                Tell the system if we want to switch a specific variable different
                from PyFunceble.CONFIGURATION

        Returns: bool
            The opposite of the installed value of Settings.variable_name.

        Raise:
            - Exception: When the configuration is not valid. In other words,
                if the PyFunceble.CONFIGURATION[variable_name] is not a bool.
        """

        if not custom:
            current_state = dict.get(PyFunceble.CONFIGURATION, variable)
        else:
            current_state = variable

        if isinstance(current_state, bool):
            if current_state:
                return False

            return True

        to_print = "Impossible to switch %s. Please post an issue to %s"

        raise Exception(
            to_print % (repr(variable), PyFunceble.LINKS["repo"] + "/issues.")
        )
