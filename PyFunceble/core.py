#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This module is half of the brain of PyFunceble.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

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
# pylint: disable=bad-continuation, too-many-lines

from domain2idna import get as domain2idna

import PyFunceble
from PyFunceble.auto_continue import AutoContinue
from PyFunceble.auto_save import AutoSave
from PyFunceble.check import Check
from PyFunceble.database import Inactive
from PyFunceble.directory_structure import DirectoryStructure
from PyFunceble.execution_time import ExecutionTime
from PyFunceble.expiration_date import ExpirationDate
from PyFunceble.helpers import Command, Download, List, Regex
from PyFunceble.mining import Mining
from PyFunceble.percentage import Percentage
from PyFunceble.prints import Prints
from PyFunceble.sort import Sort
from PyFunceble.syntax import Syntax
from PyFunceble.url import URL
from PyFunceble.adblock import AdBlock


class Core:  # pragma: no cover
    """
    Main entry to PyFunceble. Brain of the program. Also known as "put everything
    together to make the system works".

    :param domain_or_ip_to_test: A domain or IP to test.
    :type domain_or_ip_to_test: str

    :param file_path: A path to a file to read and test.
    :type file_path: str

    :param url_to_test: A URL to test.
    :type url_to_test: str

    :param url_file: A path to a file which contains URL to test.
    :type url_file: str

    :param link_to_test: A link to a file to download and test.
    :type link_to_test: str

    :param modulo_test:
        If set to True, it will tell the system that we are working as an
        exported module.
    :param modulo_test: bool
    """

    def __init__(self, **args):
        # We initiate our list of optional arguments with their default values.
        optional_arguments = {
            "domain_or_ip_to_test": None,
            "file_path": None,
            "url_to_test": None,
            "url_file": None,
            "modulo_test": False,
            "link_to_test": None,
        }

        # We initiate our optional_arguments in order to be usable all over the
        # class.
        for (arg, default) in optional_arguments.items():
            setattr(self, arg, args.get(arg, default))

        # We manage the entries.
        self._entry_management()

    @classmethod
    def _entry_management_url_download(cls, passed):
        """
        Check if the given information is a URL.
        If it is the case, it download and update the location of file to test.

        :param passed: The url passed to the system.
        :type passed: str

        :return: The state of the check.
        :rtype: bool
        """

        if passed and Check().is_url_valid(passed):
            # The passed string is an URL.

            # We get the file name based on the URL.
            # We actually just get the  string after the last `/` in the URL.
            file_to_test = passed.split("/")[-1]

            if (
                not PyFunceble.path.isfile(file_to_test)
                or PyFunceble.CONFIGURATION["counter"]["number"]["tested"] == 0
            ):
                # The filename does not exist in the current directory
                # or the currently number of tested is equal to 0.

                # We download the content of the link.
                Download(passed, file_to_test).text()

            # The files does exist or the currently number of tested is greater than
            # 0.

            # We initiate the file we have to test.
            PyFunceble.CONFIGURATION["file_to_test"] = file_to_test

            # We return true to say that everything goes right.
            return True

        # The passed string is not an URL.

        # We do not need to do anything else.
        return False

    def _entry_management_url(self):
        """
        Manage the loading of the url system.
        """

        if (
            self.url_file  # pylint: disable=no-member
            and not self._entry_management_url_download(
                self.url_file  # pylint: disable=no-member
            )
        ):  # pylint: disable=no-member
            # The current url_file is not a URL.

            # We initiate the filename as the file we have to test.
            PyFunceble.CONFIGURATION[
                "file_to_test"
            ] = self.url_file  # pylint: disable=no-member

    def _entry_management(self):  # pylint: disable=too-many-branches
        """
        Avoid to have 1 millions line into self.__init__()
        """

        if not self.modulo_test:  # pylint: disable=no-member
            # We are not in a module usage.

            # We set the file_path as the file we have to test.
            PyFunceble.CONFIGURATION[
                "file_to_test"
            ] = self.file_path  # pylint: disable=no-member

            # We check if the given file_path is an url.
            # If it is an URL we update the file to test and download
            # the given URL.
            self._entry_management_url()

            # We fix the environnement permissions.
            AutoSave().travis_permissions()

            # We check if we need to bypass the execution of PyFunceble.
            self.bypass()

            # We set the start time.
            ExecutionTime("start")

            if PyFunceble.CONFIGURATION["syntax"]:
                # We are checking for syntax.

                # We deactivate the http status code.
                PyFunceble.HTTP_CODE["active"] = False

            if self.domain_or_ip_to_test:  # pylint: disable=no-member
                # The given domain is not empty or None.

                # We initiate a variable which will tell the system the type
                # of the tested element.
                PyFunceble.CONFIGURATION["to_test_type"] = "domain"

                # We set the start time.
                ExecutionTime("start")

                # We deactivate the showing of percentage as we are in a single
                # test run.
                PyFunceble.CONFIGURATION["show_percentage"] = False

                # We deactivate the whois database as it is not needed.
                PyFunceble.CONFIGURATION["whois_database"] = False

                if PyFunceble.CONFIGURATION["idna_conversion"]:
                    domain_or_ip_to_test = domain2idna(
                        self.domain_or_ip_to_test.lower()  # pylint: disable=no-member
                    )
                else:
                    domain_or_ip_to_test = (
                        self.domain_or_ip_to_test.lower()  # pylint: disable=no-member
                    )  # pylint: disable=no-member

                # We test the domain after converting it to lower case.
                self.domain(domain_or_ip_to_test)
            elif self.url_to_test and not self.file_path:  # pylint: disable=no-member
                # An url to test is given and the file path is empty.

                # We initiate a variable which will tell the system the type
                # of the tested element.
                PyFunceble.CONFIGURATION["to_test_type"] = "url"

                # We set the start time.
                ExecutionTime("start")

                # We deactivate the showing of percentage as we are in a single
                # test run.
                PyFunceble.CONFIGURATION["show_percentage"] = False

                # We test the url to test after converting it if needed (IDNA).
                self.url(
                    Check().is_url_valid(
                        self.url_to_test,  # pylint: disable=no-member
                        return_formatted=True,
                    )
                )
            elif (
                self._entry_management_url_download(
                    self.url_file  # pylint: disable=no-member
                )
                or self.url_file  # pylint: disable=no-member
            ):
                # * A file full of URL is given.
                # or
                # * the given file full of URL is a URL.

                # * We deactivate the whois subsystem as it is not needed for url testing.
                # * We activate the generation of plain list element.
                # * We activate the generation of splited data instead of unified data.
                PyFunceble.CONFIGURATION["no_whois"] = PyFunceble.CONFIGURATION[
                    "plain_list_domain"
                ] = PyFunceble.CONFIGURATION["split"] = True

                # We deactivate the generation of hosts file as it is not relevant for
                # url testing.
                PyFunceble.CONFIGURATION["generate_hosts"] = False

                # We initiate a variable which will tell the system the type
                # of the tested element.
                PyFunceble.CONFIGURATION["to_test_type"] = "url"

                # And we test the given or the downloaded file.
                self.file_url()
            elif (
                self._entry_management_url_download(
                    self.link_to_test  # pylint: disable=no-member
                )
                or self._entry_management_url_download(
                    self.file_path  # pylint: disable=no-member
                )  # pylint: disable=no-member
                or self.file_path  # pylint: disable=no-member
            ):
                # * A file path is given.
                # or
                # * The given file path is an URL.
                # or
                # * A link to test is given.

                # We initiate a variable which will tell the system the type
                # of the tested element.
                PyFunceble.CONFIGURATION["to_test_type"] = "domain"

                # We test the given or the downloaded file.
                self.file()
            else:
                # No file, domain, single url or file or url is given.

                # We print a message on screen.
                print(
                    PyFunceble.Fore.CYAN + PyFunceble.Style.BRIGHT + "Nothing to test."
                )

            # We stop and log the execution time.
            ExecutionTime("stop", last=True)

            # We log the current percentage state.
            Percentage().log()

            if (
                self.domain_or_ip_to_test  # pylint: disable=no-member
                or self.url_to_test  # pylint: disable=no-member
            ):
                # We are testing a domain.

                # We show the colored logo.
                self.colorify_logo()

            # We print our friendly message :)
            PyFunceble.stay_safe()
        else:
            # We are used as an imported module.

            # We activate the simple mode as the table or any full
            # details on screen are irrelevant.
            PyFunceble.CONFIGURATION["simple"] = True

            # We activate the quiet mode.
            PyFunceble.CONFIGURATION["quiet"] = True

            # We deactivate the whois database as it is not needed.
            PyFunceble.CONFIGURATION["whois_database"] = False

            # And we deactivate the generation of files.
            PyFunceble.CONFIGURATION["no_files"] = True

            if self.domain_or_ip_to_test:  # pylint: disable=no-member
                # A domain is given.

                # We initiate a variable which will tell the system the type
                # of the tested element.
                PyFunceble.CONFIGURATION["to_test_type"] = "domain"

                # We set the domain to test.
                PyFunceble.CONFIGURATION[
                    "to_test"
                ] = self.domain_or_ip_to_test.lower()  # pylint: disable=no-member
            elif self.url_to_test:  # pylint: disable=no-member
                # A url is given,

                # We initiate a variable which will tell the system the type
                # of the tested element.
                PyFunceble.CONFIGURATION["to_test_type"] = "url"

                # We set the url to test.
                PyFunceble.CONFIGURATION[
                    "to_test"
                ] = self.url_to_test  # pylint: disable=no-member

    def test(self, complete=False):
        """
        Avoid confusion between self.domain which is called into
        __main__ and test() which should be called out of PyFunceble's scope.

        :param complete:
            Activate the return of a dictionnary with signigican data about
            the test.
        :type complete: bool

        :return: ACTIVE INACTIVE or INVALID.
        :rtype: str|list

        :raises:
            :code:`Exception`
                When this method is called under
                :code:`__name__ == '__main__'`

        .. note::
            This method should never be called in a
            :code:`__name__ == '__main__'` context.
        """

        if not self.modulo_test:  # pylint: disable=no-member
            # We are not used as an imported module.

            # We inform the user that they should not use this method.
            raise Exception(
                "You should not use this method. Please prefer self.domain()"
            )

        else:
            # We are used as an imported module.

            if complete:
                # We have to return much more information into our result.

                # We initiate the location and the information we have to return.
                PyFunceble.CONFIGURATION["current_test_data"] = {
                    "tested": None,
                    "expiration_date": None,
                    "domain_syntax_validation": None,
                    "http_status_code": None,
                    "ip4_syntax_validation": None,
                    "nslookup": [],
                    "status": None,
                    "url_syntax_validation": None,
                    "whois_server": None,
                    "whois_record": None,
                }

                if (
                    "to_test" in PyFunceble.CONFIGURATION
                    and PyFunceble.CONFIGURATION["to_test"]
                ):
                    # We are testing something.

                    # We update the tested index.
                    PyFunceble.CONFIGURATION["current_test_data"][
                        "tested"
                    ] = PyFunceble.CONFIGURATION["to_test"]

                    if PyFunceble.CONFIGURATION["to_test_type"] == "domain":
                        # We are testing a domain.

                        # We get the status of the domain.
                        PyFunceble.CONFIGURATION["current_test_data"][
                            "status"
                        ] = ExpirationDate().get()
                    elif PyFunceble.CONFIGURATION["to_test_type"] == "url":
                        # We are testing a url.

                        # We get the status of the url.
                        PyFunceble.CONFIGURATION["current_test_data"][
                            "status"
                        ] = URL().get()
                    else:
                        raise Exception("Unknow test type.")

                if "http_code" in PyFunceble.CONFIGURATION:
                    # The http status code exist into the configuration.

                    # We update the tested index.
                    PyFunceble.CONFIGURATION["current_test_data"][
                        "http_status_code"
                    ] = PyFunceble.CONFIGURATION["http_code"]

                # We finaly return our dataset.
                return PyFunceble.CONFIGURATION["current_test_data"]

            if PyFunceble.CONFIGURATION["to_test_type"] == "domain":
                # We are testing a domain.

                # We return the status of the parsed domain.
                return ExpirationDate().get()

            if PyFunceble.CONFIGURATION["to_test_type"] == "url":
                # We are testing a url.

                # We return the status of the parsed url.
                return URL().get()

            # We raise an exception because that means that something wrong
            # happened because of the developer not the user.
            raise Exception("Unknown to_test_type. Please report issue.")

    @classmethod
    def bypass(cls):
        """
        Exit the script if :code:`[PyFunceble skip]` is matched into the latest
        commit message.
        """

        # We set the regex to match in order to bypass the execution of
        # PyFunceble.
        regex_bypass = r"\[PyFunceble\sskip\]"

        if (
            PyFunceble.CONFIGURATION["travis"]
            and Regex(
                Command("git log -1").execute(), regex_bypass, return_data=False
            ).match()
        ):
            # * We are under Travis CI.
            # and
            # * The bypass marker is matched into the latest commit.

            # We save everything and stop PyFunceble.
            AutoSave(True, is_bypass=True)

    @classmethod
    def _print_header(cls):
        """
        Decide if we print or not the header.
        """

        if (
            not PyFunceble.CONFIGURATION["quiet"]
            and not PyFunceble.CONFIGURATION["header_printed"]
        ):
            # * The quiet mode is not activated.
            # and
            # * The header has not been already printed.

            # We print a new line.
            print("\n")

            if PyFunceble.CONFIGURATION["less"]:
                # We have to show less informations on screen.

                # We print the `Less` header.
                Prints(None, "Less").header()
            else:
                # We have to show every informations on screen.

                # We print the `Generic` header.
                Prints(None, "Generic").header()

            # The header was printed.

            # We initiate the variable which say that the header has been printed to True.
            PyFunceble.CONFIGURATION["header_printed"] = True

    def _file_decision(self, current, last, status=None):
        """
        Manage the database, autosave and autocontinue systems for the case that we are reading
        a file.

        :param current: The currently tested element.
        :type current: str

        :param last: The last element of the list.
        :type last: str

        :param status: The status of the currently tested element.
        :type status: str
        """

        if (
            status
            and not PyFunceble.CONFIGURATION["simple"]
            and PyFunceble.CONFIGURATION["file_to_test"]
        ):
            # * The status is given.
            # and
            # * The simple mode is deactivated.
            # and
            # * A file to test is set.

            # We run the mining logic.
            Mining().process()

            # We delete the currently tested element from the mining
            # database.
            # Indeed, as it is tested, it is already in our
            # testing process which means that we don't need it into
            # the mining database.
            Mining().remove()

            if (
                status.lower() in PyFunceble.STATUS["list"]["up"]
                or status.lower() in PyFunceble.STATUS["list"]["valid"]
            ):
                # The status is in the list of up status.

                # We remove the currently tested element from the
                # database.
                Inactive().remove()
            else:
                # The status is not in the list of up status.

                # We add the currently tested element to the
                # database.
                Inactive().add()

            # We backup the current state of the file reading
            # for the case that we need to continue later.
            AutoContinue().backup()

            if current != last:
                # The current element is not the last one.

                # We run the autosave logic.
                AutoSave()
            else:
                # The current element is the last one.

                # We stop and log the execution time.
                ExecutionTime("stop", True)

                # We show/log the percentage.
                Percentage().log()

                # We reset the counters as we end the process.
                self.reset_counters()

                # We backup the current state of the file reading
                # for the case that we need to continue later.
                AutoContinue().backup()

                # We show the colored logo.
                self.colorify_logo()

                # We save and stop the script if we are under
                # Travis CI.
                AutoSave(True)

        for index in ["http_code", "referer"]:
            # We loop through some configuration index we have to empty.

            if index in PyFunceble.CONFIGURATION:
                # The index is in the configuration.

                # We empty the configuration index.
                PyFunceble.CONFIGURATION[index] = ""

    def domain(self, domain=None, last_domain=None):
        """
        Manage the case that we want to test only a domain.

        :param domain: The domain or IP to test.
        :type domain: str

        :param last_domain:
            The last domain to test if we are testing a file.
        :type last_domain: str

        :param return_status: Tell us if we need to return the status.
        :type return_status: bool
        """

        # We print the header.
        self._print_header()

        if domain:
            # A domain is given.

            # We format and set the domain we are testing and treating.
            PyFunceble.CONFIGURATION["to_test"] = self._format_domain(domain)
        else:
            # A domain is not given.

            # We set the domain we are testing and treating to None.
            PyFunceble.CONFIGURATION["to_test"] = None

        if PyFunceble.CONFIGURATION["to_test"]:
            # The domain is given (Not None).

            if PyFunceble.CONFIGURATION["syntax"]:
                # The syntax mode is activated.

                # We get the status from Syntax.
                status = Syntax().get()
            else:
                # We test and get the status of the domain.
                status = ExpirationDate().get()

            # We run the file decision logic.
            self._file_decision(domain, last_domain, status)

            if PyFunceble.CONFIGURATION["simple"]:
                # The simple mode is activated.

                # We print the domain and the status.
                print(domain, status)

    def url(self, url_to_test=None, last_url=None):
        """
        Manage the case that we want to test only a given url.

        :param url_to_test: The url to test.
        :type url_to_test: str

        :param last_url:
            The last url of the file we are testing
            (if exist)
        :type last_url: str
        """

        # We print the header.
        self._print_header()

        if url_to_test:
            # An url to test is given.

            # We set the url we are going to test.
            PyFunceble.CONFIGURATION["to_test"] = url_to_test
        else:
            # An URL to test is not given.

            # We set the url we are going to test to None.
            PyFunceble.CONFIGURATION["to_test"] = None

        if PyFunceble.CONFIGURATION["to_test"]:
            # An URL to test is given.

            if PyFunceble.CONFIGURATION["syntax"]:
                # The syntax mode is activated.

                # We get the status from Syntax.
                status = Syntax().get()
            else:
                # The syntax mode is not activated.

                # We get the status from URL.
                status = URL().get()

            # We run the file decision logic.
            self._file_decision(url_to_test, last_url, status)

            if PyFunceble.CONFIGURATION["simple"]:
                # The simple mode is activated.

                # We print the URL informations.
                print(PyFunceble.CONFIGURATION["to_test"], status)

    @classmethod
    def reset_counters(cls):
        """
        Reset the counters when needed.
        """

        for string in ["up", "down", "invalid", "tested"]:
            # We loop through to the index of the autoContinue subsystem.

            # And we set their counter to 0.
            PyFunceble.CONFIGURATION["counter"]["number"].update({string: 0})

    @classmethod
    def colorify_logo(cls):
        """
        Print the colored logo based on global results.
        """

        if not PyFunceble.CONFIGURATION["quiet"]:
            # The quiet mode is not activated.

            if PyFunceble.CONFIGURATION["counter"]["percentage"]["up"] >= 50:
                # The percentage of up is greater or equal to 50%.

                # We print the CLI logo in green.
                print(PyFunceble.Fore.GREEN + PyFunceble.ASCII_PYFUNCEBLE)
            else:
                # The percentage of up is less than 50%.

                # We print the CLI logo in red.
                print(PyFunceble.Fore.RED + PyFunceble.ASCII_PYFUNCEBLE)

    @classmethod
    def _format_domain(cls, extracted_domain):
        """
        Format the extracted domain before passing it to the system.

        :param extracted_domain: The extracted domain.
        :type extracted_domain: str

        :return: The formatted domain or IP to test.
        :rtype: str

        .. note:
            Understand by formating the fact that we get rid
            of all the noises around the domain we want to test.
        """

        if not extracted_domain.startswith("#"):
            # The line is not a commented line.

            if "#" in extracted_domain:
                # There is a comment at the end of the line.

                # We delete the comment from the line.
                extracted_domain = extracted_domain[
                    : extracted_domain.find("#")
                ].strip()

            if " " in extracted_domain or "\t" in extracted_domain:
                # A space or a tabs is in the line.

                # We remove all whitestring from the extracted line.
                splited_line = extracted_domain.split()

                # As there was a space or a tab in the string, we consider
                # that we are working with the hosts file format which means
                # that the domain we have to test is after the first string.
                # So we set the index to 1.
                index = 1

                while index < len(splited_line):
                    # We loop until the index is greater than the length of
                    #  the splited line.

                    if splited_line[index]:
                        # The element at the current index is not an empty string.

                        # We break the loop.
                        break

                    # The element at the current index is an empty string.

                    # We increase the index number.
                    index += 1

                # We return the last read element.
                return splited_line[index]

            # We return the extracted line.
            return extracted_domain

        # The extracted line is a comment line.

        # We return an empty string as we do not want to work with commented line.
        return ""

    @classmethod
    def _extract_domain_from_file(cls):
        """
        Extract all non commented lines from the file we are testing.

        :return: The elements to test.
        :rtype: list
        """

        # We initiate the variable which will save what we are going to return.
        result = []

        if PyFunceble.path.isfile(PyFunceble.CONFIGURATION["file_to_test"]):
            # The give file to test exist.

            with open(PyFunceble.CONFIGURATION["file_to_test"]) as file:
                # We open and read the file.

                for line in file:
                    # We loop through each lines.

                    if not line.startswith("#"):
                        # The currently read line is not a commented line.

                        # We append the current read line to the result.
                        result.append(line.rstrip("\n").strip())
        else:
            # The given file to test does not exist.

            # We raise a FileNotFoundError exception.
            raise FileNotFoundError(PyFunceble.CONFIGURATION["file_to_test"])

        # We return the result.
        return result

    def _file_list_to_test_filtering(self):
        """
        Unify the way we work before testing file contents.
        """

        # We get the list to test from the file we have to test.
        list_to_test = self._extract_domain_from_file()

        # We get the list of mined.
        mined_list = Mining().list_of_mined()

        if mined_list:
            list_to_test.extend(mined_list)

        # We generate the directory structure.
        DirectoryStructure()

        # We restore the data from the last session if it does exist.
        AutoContinue().restore()

        if PyFunceble.CONFIGURATION["adblock"]:
            # The adblock decoder is activated.

            # We get the list of domain to test (decoded).
            list_to_test = AdBlock(list_to_test).decode()
        else:
            # The adblock decoder is not activated.

            # We get the formatted list of domain to test.
            list_to_test = list(map(self._format_domain, list_to_test))

        # We clean the output directory if it is needed.
        PyFunceble.Clean(list_to_test)

        # We set the start time.
        ExecutionTime("start")

        # We get the list we have to test in the current session (from the database).
        Inactive().to_test()

        if (
            PyFunceble.CONFIGURATION["file_to_test"]
            in PyFunceble.CONFIGURATION["inactive_db"]
            and "to_test"
            in PyFunceble.CONFIGURATION["inactive_db"][
                PyFunceble.CONFIGURATION["file_to_test"]
            ]
            and PyFunceble.CONFIGURATION["inactive_db"][
                PyFunceble.CONFIGURATION["file_to_test"]
            ]["to_test"]
        ):
            # * The current file to test in into the database.
            # and
            # * The `to_test` index is present into the database
            #   related to the file we are testing.
            # and
            # * The `to_test` index content is not empty.

            # We extend our list to test with the content of the `to_test` index
            # of the current file database.
            list_to_test.extend(
                PyFunceble.CONFIGURATION["inactive_db"][
                    PyFunceble.CONFIGURATION["file_to_test"]
                ]["to_test"]
            )

        # We set a regex of element to delete.
        # Understand with this variable that we don't want to test those.
        regex_delete = r"localhost$|localdomain$|local$|broadcasthost$|0\.0\.0\.0$|allhosts$|allnodes$|allrouters$|localnet$|loopback$|mcastprefix$|ip6-mcastprefix$|ip6-localhost$|ip6-loopback$|ip6-allnodes$|ip6-allrouters$|ip6-localnet$"  # pylint: disable=line-too-long

        # We get the database content.
        database_content = Inactive().content()

        # We remove the element which are in the database from the
        # current list to test.
        list_to_test = List(
            list(
                set(Regex(list_to_test, regex_delete).not_matching_list())
                - set(database_content)
            )
        ).format()

        if PyFunceble.CONFIGURATION["filter"]:
            # The filter is not empty.

            # We get update our list to test. Indeed we only keep the elements which
            # matches the given filter.
            list_to_test = List(
                Regex(
                    list_to_test, PyFunceble.CONFIGURATION["filter"], escape=True
                ).matching_list()
            ).format()

        list_to_test = List(list(list_to_test)).custom_format(Sort.standard)

        if PyFunceble.CONFIGURATION["hierarchical_sorting"]:
            # The hierarchical sorting is desired by the user.

            # We format the list.
            list_to_test = List(list(list_to_test)).custom_format(Sort.hierarchical)

        # We return the final list to test.
        return list_to_test

    def file(self):
        """
        Manage the case that need to test each domain of a given file path.

        .. note::
            1 domain per line.
        """

        # We get, format, filter, clean the list to test.
        list_to_test = self._file_list_to_test_filtering()

        if PyFunceble.CONFIGURATION["idna_conversion"]:
            # We have to convert domains to idna.

            # We convert if we need to convert.
            list_to_test = domain2idna(list_to_test)

            if PyFunceble.CONFIGURATION["hierarchical_sorting"]:
                # The hierarchical sorting is desired by the user.

                # We format the list.
                list_to_test = List(list_to_test).custom_format(Sort.hierarchical)
            else:
                # The hierarchical sorting is not desired by the user.

                # We format the list.
                list_to_test = List(list_to_test).custom_format(Sort.standard)

        # We test each element of the list to test.
        list(
            map(
                self.domain,
                list_to_test[PyFunceble.CONFIGURATION["counter"]["number"]["tested"] :],
                PyFunceble.repeat(list_to_test[-1]),
            )
        )

    def file_url(self):
        """
        Manage the case that we have to test a file

        .. note::
            1 URL per line.
        """

        # We get, format, clean the list of URL to test.
        list_to_test = self._file_list_to_test_filtering()

        # We test each URL from the list to test.
        list(
            map(
                self.url,
                list_to_test[PyFunceble.CONFIGURATION["counter"]["number"]["tested"] :],
                PyFunceble.repeat(list_to_test[-1]),
            )
        )

    @classmethod
    def switch(
        cls, variable, custom=False
    ):  # pylint: disable=inconsistent-return-statements
        """
        Switch PyFunceble.CONFIGURATION variables to their opposite.

        :param variable:
            The variable name to switch.
            The variable should be an index our configuration system.
            If we want to switch a bool variable, we should parse
            it here.
        :type variable: str|bool

        :param custom:
            Let us know if have to switch the parsed variable instead
            of our configuration index.
        :type custom: bool

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
        raise Exception(
            to_print % (repr(variable), PyFunceble.LINKS["repo"] + "/issues.")
        )
