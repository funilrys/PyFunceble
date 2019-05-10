# pylint: disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provide the logic for a file test from the CLI.

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

from itertools import chain

from domain2idna import get as domain2idna

import PyFunceble
from PyFunceble.adblock import AdBlock
from PyFunceble.auto_continue import AutoContinue
from PyFunceble.auto_save import AutoSave
from PyFunceble.generate import Generate
from PyFunceble.helpers import Download, List, Regex
from PyFunceble.inactive_db import InactiveDB
from PyFunceble.mining import Mining
from PyFunceble.sort import Sort
from PyFunceble.status import Status, SyntaxStatus, URLStatus
from PyFunceble.whois_db import WhoisDB


class FileCore:  # pylint: disable=too-many-instance-attributes
    """
    Brain of PyFunceble for file testing.

    :param str file: The file we are testing.

    :param str file_type:
        The file type.
        Should be one of the following.

            - :code:`domain`

            - :code:`url`
    """

    # We set a regex of element to delete.
    # Understand with this variable that we don't want to test those.
    regex_ignore = r"localhost$|localdomain$|local$|broadcasthost$|0\.0\.0\.0$|allhosts$|allnodes$|allrouters$|localnet$|loopback$|mcastprefix$|ip6-mcastprefix$|ip6-localhost$|ip6-loopback$|ip6-allnodes$|ip6-allrouters$|ip6-localnet$"  # pylint: disable=line-too-long

    def __init__(self, file, file_type="domain"):
        # We share the file we are working with.
        self.file = file
        # We share the file/test type.
        self.file_type = file_type

        # We construct the list of UP statuses.
        self.list_of_up_statuses = PyFunceble.STATUS["list"]["up"]
        self.list_of_up_statuses.extend(PyFunceble.STATUS["list"]["valid"])

        # We get/initiate the preset class.
        self.preset = PyFunceble.Preset()
        # We get/initiate the autosave database/subsyste..
        self.autosave = AutoSave(start_time=PyFunceble.INTERN["start"])
        # We get/initiate the inactive database.
        self.inactive_db = InactiveDB(self.file)
        # We get/initiate the whois database.
        self.whois_db = WhoisDB()
        # We get/initiate the mining subsystem.
        self.mining = Mining(self.file)
        # We get/initiate the autocontinue subsystem.
        self.autocontinue = AutoContinue(self.file)

        # We initiate a variable which will tell us when
        # we start testing for complements.
        self.complements_test_started = False

        # We download the file if it is a list.
        self.download_link()

        # We generate the directory structure.
        PyFunceble.DirectoryStructure()

    @classmethod
    def get_simple_coloration(cls, status):
        """
        Given a status we give the coloration for the simple mode.

        :param str status: An official status output.
        """

        if status in [
            PyFunceble.STATUS["official"]["up"],
            PyFunceble.STATUS["official"]["valid"],
        ]:
            # The status is in the list of UP status.

            # We return the green coloration.
            return PyFunceble.Fore.GREEN + PyFunceble.Style.BRIGHT

        if status == PyFunceble.STATUS["official"]["down"]:
            # The status is in the list of DOWN status.

            # We return the red coloration.
            return PyFunceble.Fore.RED + PyFunceble.Style.BRIGHT

        # The status is not in the list of UP nor DOWN status.

        # We return the cyam coloration.
        return PyFunceble.Fore.CYAN + PyFunceble.Style.BRIGHT

    def download_link(self):  # pragma: no cover
        """
        Download the file if it is an URL.
        """

        if (
            self.file
            and self.autocontinue.is_empty()
            and PyFunceble.Check(self.file).is_url()
        ):
            # The given file is an URL.

            # We get the destination.
            destination = self.file.split("/")[-1]

            if (
                not PyFunceble.path.isfile(destination)
                or PyFunceble.INTERN["counter"]["number"]["tested"] == 0
            ):
                # The filename does not exist in the current directory
                # or the currently number of tested is equal to 0.

                # We download the content of the link.
                Download(self.file, destination).text()

            # We update the global file with the destination.
            self.file = destination

    def domain(self, subject):  # pragma: no cover
        """
        Handle the test of a single domain.

        :param str subject: The subject we are testing.
        """

        if subject:
            # The given subject is not empty nor None.

            if PyFunceble.CONFIGURATION["syntax"]:
                # The syntax mode is activated.

                # We get the status from SyntaxStatus.
                status = SyntaxStatus(
                    subject, subject_type="file_domain", filename=self.file
                ).get()["status"]
            else:
                # We test and get the status of the domain.
                status = Status(
                    subject,
                    subject_type="file_domain",
                    filename=self.file,
                    whois_db=self.whois_db,
                ).get()["status"]

            if PyFunceble.CONFIGURATION["simple"]:
                # The simple mode is activated.

                # We print the domain and the status.
                print(
                    "{0} {1}".format(
                        self.get_simple_coloration(status) + subject, status
                    )
                )

            if self.complements_test_started:
                # We started to test the complements.

                # We generate the complement file(s).
                Generate(subject, "file_domain", status).complements_file()

            # We return the status.
            return status

        # We return None, there is nothing to test.
        return None

    def url(self, subject):  # pragma: no cover
        """
        Handle the simple URL testing.

        :param str subject: The subject we are testing.
        """

        if subject:
            # The given subject is not empty nor None.

            if PyFunceble.CONFIGURATION["syntax"]:
                # The syntax mode is activated.

                # We get the status from SyntaxStatus.
                status = SyntaxStatus(
                    subject, subject_type="file_url", filename=self.file
                ).get()["status"]
            else:
                # We test and get the status of the domain.
                status = URLStatus(
                    subject, subject_type="file_url", filename=self.file
                ).get()["status"]

            if PyFunceble.CONFIGURATION["simple"]:
                # The simple mode is activated.

                # We print the domain and the status.
                print(
                    "{0} {1}".format(
                        self.get_simple_coloration(status) + subject, status
                    )
                )

            if self.complements_test_started:
                # We started to test the complements.

                # We generate the complement file(s).
                Generate(subject, "file_url", status).complements_file()

            # We retunr the status.
            return status

        # We return None, there is nothing to test.
        return None

    @classmethod
    def _format_line(cls, line):
        """
        Format the extracted line before passing it to the system.

        :param str line: The extracted line.

        :return: The formatted line with only the element to test.
        :rtype: str

        .. note:
            Understand by formating the fact that we get rid
            of all the noises around the element we want to test.
        """

        if not line.startswith("#"):
            # The line is not a commented line.

            if "#" in line:
                # There is a comment at the end of the line.

                # We delete the comment from the line.
                line = line[: line.find("#")].strip()

            if " " in line or "\t" in line:
                # A space or a tabs is in the line.

                # We remove all whitestring from the extracted line.
                splited_line = line.split()

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
                    index += 1  # pragma: no cover

                # We return the last read element.
                return splited_line[index]

            # We return the extracted line.
            return line

        # The extracted line is a comment line.

        # We return an empty string as we do not want to work with commented line.
        return ""

    def __process_test(self, subject):  # pragma: no cover
        """
        Given a subject, we perform its test.

        :param str subject: The subjet we have to test.
        """

        if self.file_type == "domain":
            # We are testing for domains.

            if PyFunceble.CONFIGURATION["idna_conversion"]:
                # We have to convert to IDNA:

                # We get and return the status of the IDNA
                # domain.
                return self.domain(domain2idna(subject))

            # We get and return the status of the domain.
            return self.domain(subject)

        if self.file_type == "url":
            # We are testing for urls.

            # We get and return the status of the URL.
            return self.url(subject)

        # We raise an exception, we could not understand the
        # given file type.
        raise Exception("Unknown file type.")

    def get_complements(self):  # pragma: no cover
        """
        Generate a list of complements to test.
        """

        # We initiate an empty list of complements.
        complements = []

        if (
            PyFunceble.CONFIGURATION["generate_complements"]
            and self.autocontinue.authorized
        ):
            # * The user want us to generate and test the list
            # of all complements.
            # and
            # * The autocontinue subsystem is activated.

            # We inform all subsystem that we are testing for complements.
            self.complements_test_started = True

            if "complements" not in self.autocontinue.database[self.file].keys():
                # The complements are not saved,

                # We get the list of domains we are going to work with.
                complements = [
                    z
                    for x, y in self.autocontinue.database[self.file].items()
                    for z in y
                    if not PyFunceble.Check(z).is_subdomain()
                    and PyFunceble.Check(z).is_domain()
                ]

                # We generate the one without "www." if "www." is given.
                complements.extend([x[4:] for x in complements if x.startswith("www.")])
                # We generate the one with "www." if "www." is not given.
                complements.extend(
                    [
                        "www.{0}".format(x)
                        for x in complements
                        if not x.startswith("www.")
                    ]
                )

                # We remove the already tested subjects.
                complements = set(List(complements).format()) - set(
                    self.autocontinue.database[self.file].keys()
                )

                # We save the constructed list of complements
                self.autocontinue.database[self.file]["complements"] = list(complements)
                self.autocontinue.save()
            else:
                # We get the complements we still have to test.
                complements = self.autocontinue.database[self.file]["complements"]

        return complements

    def _test_line(
        self, line, manager_data=None
    ):  # pylint: disable=too-many-branches  # pragma: no cover
        """
        Given a line, we test it.

        :param str line: A line to work with.
        :param multiprocessing.Manager.list manager_data: A Server process.
        """

        if manager_data is not None:
            # We are in a mulitiprocess environment.

            # We create a new autocontinue instance.
            autocontinue = AutoContinue(self.file)
            # We create a new inactive database instance.
            inactive_db = InactiveDB(self.file)
            # We create a new mining instance.
            mining = Mining(self.file)
        else:
            # We are not in a multiprocess environment.

            # We use the previously initiated autocontinue instance.
            autocontinue = self.autocontinue
            # We use the previously initiated inactive database instance.
            inactive_db = self.inactive_db
            # We use the previously initiated mining instance.
            mining = self.mining

        # We remove cariage from the given line.
        line = line.strip()

        if line[0] == "#":
            # We line is a comment line.

            # We return None, there is nothing to test.
            return None

        if Regex(line, self.regex_ignore, escape=False, return_data=False).match():
            # The line match our list of elemenet
            # to ignore.

            # We return None, there is nothing to test.
            return None

        # We format the line, it's the last
        # rush before starting to filter and test.
        subject = self._format_line(line)

        if subject in autocontinue or subject in inactive_db:
            # * The subject is in the autocontinue database.
            # or
            # * The subject is in the inactive database.

            # We return None, thre is nothing to test.
            return None

        if (
            not PyFunceble.CONFIGURATION["local"]
            and PyFunceble.Check(subject).is_reserved_ipv4()
        ):
            # * We are not testing for local components.
            # and
            # * The subject is a reserved IPv4.

            # We return None, there is nothing to test.
            return None

        if PyFunceble.CONFIGURATION["filter"]:
            # We have to filter.

            if Regex(
                subject, PyFunceble.CONFIGURATION["filter"], return_data=False
            ).match():
                # The line match the given filter.

                # We get the status of the current line.
                status = self.__process_test(subject)
            else:
                # The line does not match the given filter.

                # We return None.
                return None
        else:
            # We do not have to filter.

            # We get the status of the current line.
            status = self.__process_test(subject)

        # We add the line into the auto continue database.
        autocontinue.add(subject, status)

        if status.lower() in self.list_of_up_statuses:
            # The status is in the list of UP status.

            # We mine if necessary.
            mining.mine(subject, self.file_type)

            if subject in inactive_db:
                # The subject is in the inactive database.

                # We generate the suspicous file.
                Generate(
                    subject, "file_domain", PyFunceble.STATUS["official"]["up"]
                ).analytic_file("suspicious")

                # And we remove the current subject from
                # the inactive database.
                inactive_db.remove(subject)
        else:
            # The status is not in the list of UP status.

            # We add the current subject into the
            # inactive database.
            inactive_db.add(subject)

        if self.complements_test_started:
            # We started the test of the complements.

            if "complements" in autocontinue.database:
                # The complement index is present.

                while subject in autocontinue.database["complements"]:
                    # We loop untill the line is not present into the
                    # database.

                    # We remove the currently tested element.
                    autocontinue.database["complements"].remove(subject)

                    # We save the current state.
                    autocontinue.save()

        if manager_data is None:
            # We are not in a multiprocess environment.

            # We process the autosaving if it is necessary.
            self.autosave.process(test_completed=False)
        else:
            # We are in a multiprocess environment.

            # We save everything we initiated into the server process
            manager_data.append(
                {
                    "autocontinue": autocontinue.database,
                    "inactive_db": inactive_db.database,
                    "mining": mining.database,
                }
            )

        # We return None.
        return None

    def read_and_test_file_content(self):  # pragma: no cover
        """
        Read a file block by block and test its content.
        """

        # We print the CLI header.
        PyFunceble.CLICore.print_header()

        with open(self.file, "r", encoding="utf-8") as file:
            # We open the file we have to test.

            if not PyFunceble.CONFIGURATION["hierarchical_sorting"]:
                # We do not have to sort hierarchicaly.

                # We sort the lines standarly.
                file = List(file).custom_format(Sort.standard)
            else:
                # We do have to sort hierarchicaly.

                # We sort the lines hierarchicaly.
                file = List(file).custom_format(Sort.hierarchical)

            if not PyFunceble.CONFIGURATION["adblock"]:
                # We do not have to adblock decode the content
                # of the file.

                for line in chain(file, self.inactive_db["to_test"]):
                    # We loop through the file content and the
                    # inactive dataset to retest.

                    # We test the line.
                    self._test_line(line)
            else:
                # We do have to decode the content of the file.

                for line in chain(AdBlock(file).decode(), self.inactive_db["to_test"]):
                    # We loop through the file decoded file
                    # content.

                    # We test the line.
                    self._test_line(line)

        for index, line in self.mining.list_of_mined():
            # We loop through the list of mined domains
            # (if the mining subystem is activated.)

            # We test the line.
            self._test_line(line)
            # and remove the currently tested line
            # from the mining database.
            self.mining.remove(index, line)

            # We get the list of complements.
            complements = self.get_complements()

            for subject in complements:
                # We loop through the list of complements.

                # We test the complement.
                self._test_line(subject)

            # We inform all subsystem that we are not testing for complements anymore.
            self.complements_test_started = False

        # We clean the autocontinue subsystem, we finished
        # the test.
        self.autocontinue.clean()
        # We process the autosaving if necessary.
        self.autosave.process(test_completed=True)
