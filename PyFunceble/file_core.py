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

from hashlib import sha256
from itertools import chain
from multiprocessing import Pool

from domain2idna import get as domain2idna

import PyFunceble
from PyFunceble.adblock import AdBlock
from PyFunceble.auto_continue import AutoContinue
from PyFunceble.auto_save import AutoSave
from PyFunceble.generate import Generate
from PyFunceble.helpers import Dict, Download, List, Regex
from PyFunceble.inactive_db import InactiveDB
from PyFunceble.mining import Mining
from PyFunceble.mysql import MySQL
from PyFunceble.percentage import Percentage
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
        self.list_of_up_statuses = PyFunceble.STATUS.list.up
        self.list_of_up_statuses.extend(PyFunceble.STATUS.list.valid)

        # We get/initiate the db.
        self.mysql_db = MySQL()

        # We get/initiate the preset class.
        self.preset = PyFunceble.Preset()
        # We get/initiate the autosave database/subsyste..
        self.autosave = AutoSave(start_time=PyFunceble.INTERN["start"])
        # We get/initiate the inactive database.
        self.inactive_db = InactiveDB(self.file, mysql_db=self.mysql_db)
        # We get/initiate the whois database.
        self.whois_db = WhoisDB(mysql_db=self.mysql_db)
        # We get/initiate the mining subsystem.
        self.mining = Mining(self.file, mysql_db=self.mysql_db)
        # We get/initiate the autocontinue subsystem.
        self.autocontinue = AutoContinue(
            self.file, parent_process=True, mysql_db=self.mysql_db
        )

        # We initiate a variable which will tell us when
        # we start testing for complements.
        self.complements_test_started = False

        # We download the file if it is a list.
        self.download_link()

    @classmethod
    def save_into_database(cls, output, filename, mysql_db):
        """
        Saves the current status inside the database.
        """

        if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
            table_name = mysql_db.tables["tested"]

            if not filename:
                filename = ""

            to_insert = (
                "INSERT INTO {0} "
                "(tested, file_path, _status, status, _status_source, status_source, "
                "domain_syntax_validation, expiration_date, http_status_code, "
                "ipv4_range_syntax_validation, ipv4_syntax_validation, "
                "subdomain_syntax_validation, url_syntax_validation, whois_server, digest) "
                "VALUES (%(tested)s, %(file_path)s, %(_status)s, %(status)s, %(_status_source)s, "
                "%(status_source)s, %(domain_syntax_validation)s, "
                "%(expiration_date)s, %(http_status_code)s, "
                "%(ipv4_range_syntax_validation)s, %(ipv4_syntax_validation)s, "
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
                "subdomain_syntax_validation = %(subdomain_syntax_validation)s, "
                "url_syntax_validation = %(url_syntax_validation)s, "
                "whois_server = %(whois_server)s "
                "WHERE digest = %(digest)s"
            ).format(table_name)

            with mysql_db.get_connection() as cursor:
                to_set = Dict(output).merge({"file_path": filename})

                to_set["digest"] = sha256(
                    bytes(to_set["file_path"] + to_set["tested"], "utf-8")
                ).hexdigest()

                if (
                    isinstance(to_set["http_status_code"], str)
                    and not to_set["http_status_code"].isdigit()
                ):
                    to_set["http_status_code"] = None

                try:
                    cursor.execute(to_insert, to_set)
                except mysql_db.errors:
                    cursor.execute(to_update, to_set)

                PyFunceble.Logger().debug(
                    f"Saved into the {repr(table_name)} table:\n{to_set}"
                )

    @classmethod
    def get_simple_coloration(cls, status):
        """
        Given a status we give the coloration for the simple mode.

        :param str status: An official status output.
        """

        if status in [PyFunceble.STATUS.official.up, PyFunceble.STATUS.official.valid]:
            # The status is in the list of UP status.

            # We return the green coloration.
            return PyFunceble.Fore.GREEN + PyFunceble.Style.BRIGHT

        if status == PyFunceble.STATUS.official.down:
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

        if PyFunceble.Check(self.file).is_url():
            # We get the destination.
            destination = self.file.split("/")[-1]

            if self.file and self.autocontinue.is_empty():
                # The given file is an URL.

                if (
                    not PyFunceble.path.isfile(destination)
                    or PyFunceble.INTERN["counter"]["number"]["tested"] == 0
                ):
                    # The filename does not exist in the current directory
                    # or the currently number of tested is equal to 0.

                    # We download the content of the link.
                    Download(self.file, destination).text()

                    PyFunceble.Logger().info(
                        f"Downloaded {repr(self.file)} into {repr(destination)}"
                    )

            # We update the global file with the destination.
            self.file = destination

            PyFunceble.Logger().info(f"Set file to test to {repr(self.file)}")

    def domain(self, subject):  # pragma: no cover
        """
        Handle the test of a single domain.

        :param str subject: The subject we are testing.
        """

        if subject:
            # The given subject is not empty nor None.

            if PyFunceble.CONFIGURATION.syntax:
                # The syntax mode is activated.

                data = SyntaxStatus(
                    subject, subject_type="file_domain", filename=self.file
                ).get()

                # We get the status from SyntaxStatus.
                status = data["status"]
            else:
                # We test and get the status of the domain.
                data = Status(
                    subject,
                    subject_type="file_domain",
                    filename=self.file,
                    whois_db=self.whois_db,
                    inactive_db=self.inactive_db,
                ).get()
                status = data["status"]

            if PyFunceble.CONFIGURATION.simple:
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

            self.save_into_database(data, self.file, self.mysql_db)

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

            if PyFunceble.CONFIGURATION.syntax:
                # The syntax mode is activated.

                # We get the status from SyntaxStatus.
                data = SyntaxStatus(
                    subject, subject_type="file_url", filename=self.file
                ).get()
                status = data["status"]
            else:
                # We test and get the status of the domain.
                data = URLStatus(
                    subject,
                    subject_type="file_url",
                    filename=self.file,
                    inactive_db=self.inactive_db,
                ).get()
                status = data["status"]

            if PyFunceble.CONFIGURATION.simple:
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

            self.save_into_database(data, self.file, self.mysql_db)

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

        line = line.strip()

        if line and not line.startswith("#"):
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

            if PyFunceble.CONFIGURATION.idna_conversion:
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
            PyFunceble.CONFIGURATION.generate_complements
            and self.autocontinue.authorized
        ):
            # * The user want us to generate and test the list
            # of all complements.
            # and
            # * The autocontinue subsystem is activated.

            # We inform all subsystem that we are testing for complements.
            self.complements_test_started = True

            # We get/generate the complements.
            complements = self.autocontinue.get_or_generate_complements()

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
            autocontinue = AutoContinue(self.file, parent_process=False)
            inactive_db = InactiveDB(self.file)
            mining = Mining(self.file)
        else:
            # We use the previously initiated autocontinue instance.
            autocontinue = self.autocontinue

            # We use the previously initiated inactive database instance.
            inactive_db = self.inactive_db

            # We use the previously initiated mining instance.
            mining = self.mining

        # We remove cariage from the given line.
        line = line.strip()

        if not line or line[0] == "#":
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

        if (
            not PyFunceble.CONFIGURATION.local
            and PyFunceble.Check(subject).is_reserved_ipv4()
        ):
            # * We are not testing for local components.
            # and
            # * The subject is a reserved IPv4.

            # We return None, there is nothing to test.
            return None

        if PyFunceble.CONFIGURATION.filter:
            # We have to filter.

            if Regex(
                subject, PyFunceble.CONFIGURATION.filter, return_data=False
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
                    subject, "file_domain", PyFunceble.STATUS.official.up
                ).analytic_file("suspicious")

                # And we remove the current subject from
                # the inactive database.
                inactive_db.remove(subject)
        else:
            # The status is not in the list of UP status.

            # We add the current subject into the
            # inactive database.
            inactive_db.add(subject, status)

        if self.complements_test_started and PyFunceble.CONFIGURATION.db_type == "json":
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

            if self.autosave.is_time_exceed():
                autocontinue.update_counters()

                # We process the autosaving if it is necessary.
                self.autosave.process(test_completed=False)
        elif PyFunceble.CONFIGURATION.db_type == "json":
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

    def _get_list_to_of_subjects_to_test_from_file(
        self, file_object
    ):  # pragma: no cover
        """
        Give a file object, we construct/get the list of subject to test.
        """

        if hasattr(self.inactive_db, "to_retest"):
            to_retest_inactive_db = self.inactive_db.to_retest
        else:
            to_retest_inactive_db = set()

        if PyFunceble.CONFIGURATION.multiprocess:
            with Pool(PyFunceble.CONFIGURATION.maximal_processes) as pool:
                if not PyFunceble.CONFIGURATION.adblock:
                    formatted_subjects = set(pool.map(self._format_line, file_object))
                else:
                    formatted_subjects = {
                        x
                        for x in AdBlock(
                            file_object, aggressive=PyFunceble.CONFIGURATION.aggressive
                        ).decode()
                    }
        else:
            if not PyFunceble.CONFIGURATION.adblock:
                formatted_subjects = {self._format_line(x) for x in file_object}
            else:
                formatted_subjects = {
                    x
                    for x in AdBlock(
                        file_object, aggressive=PyFunceble.CONFIGURATION.aggressive
                    ).decode()
                }

        subjects_to_test = (
            formatted_subjects
            - self.autocontinue.get_already_tested()
            - self.inactive_db.get_already_tested()
            - to_retest_inactive_db
        )

        if not subjects_to_test:
            subjects_to_test = list(formatted_subjects)
        else:
            subjects_to_test = list(subjects_to_test)

        if not PyFunceble.CONFIGURATION.multiprocess:
            if not PyFunceble.CONFIGURATION.hierarchical_sorting:
                subjects_to_test = List(subjects_to_test).custom_format(Sort.standard)
            else:
                subjects_to_test = List(subjects_to_test).custom_format(
                    Sort.hierarchical
                )

        return chain(subjects_to_test, to_retest_inactive_db)

    def generate_files_of_status(self, status):  # pragma: no cover
        """
        Generate the status file of all subjects of the given status.

        :param str status: A status to filter.
        """

        to_select = (
            "SELECT tested as subject, status, status_source, expiration_date, "
            "http_status_code, whois_server, file_path, ipv4_syntax_validation "
            "FROM {0} WHERE status = %(official_status)s "
            "AND file_path = %(file_path)s ORDER BY subject ASC"
        ).format(self.mysql_db.tables["tested"])

        if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
            with self.mysql_db.get_connection() as cursor:
                cursor.execute(
                    to_select, {"official_status": status, "file_path": self.file}
                )

                fetched = cursor.fetchall()

                if fetched:
                    for data in fetched:
                        generate = Generate(
                            data["subject"],
                            f"file_{self.file_type}",
                            data["status"],
                            source=data["status_source"],
                            expiration_date=data["expiration_date"],
                            http_status_code=data["http_status_code"],
                            whois_server=data["whois_server"],
                            filename=self.file,
                            end=True,
                        )

                        generate.status_file(
                            exclude_file_generation=self.inactive_db.authorized
                            and data["status"] not in self.list_of_up_statuses
                            and data["subject"] in self.inactive_db.to_retest
                        )
                        generate.prints_status_file()
                        generate.unified_file()

    def generate_files(self):  # pragma: no cover
        """
        Generate all needed files.
        """

        Percentage({})

        if PyFunceble.CONFIGURATION.syntax:
            self.generate_files_of_status(PyFunceble.STATUS.official.valid)
        else:
            self.generate_files_of_status(PyFunceble.STATUS.official.up)

        self.generate_files_of_status(PyFunceble.STATUS.official.down)
        self.generate_files_of_status(PyFunceble.STATUS.official.invalid)

    def read_and_test_file_content(self):  # pragma: no cover
        """
        Read a file block by block and test its content.
        """

        # We print the CLI header.
        PyFunceble.CLICore.print_header()

        with open(self.file, "r", encoding="utf-8") as file:
            # We open the file we have to test.

            for line in self._get_list_to_of_subjects_to_test_from_file(file):
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

        for subject in self.get_complements():
            # We loop through the list of complements.

            # We test the complement.
            self._test_line(subject)

        # We inform all subsystem that we are not testing for complements anymore.
        self.complements_test_started = False

        # We generate the files if they were not previously generated.
        self.generate_files()

        # We update the counters
        self.autocontinue.update_counters()

        # We clean the autocontinue subsystem, we finished
        # the test.
        self.autocontinue.clean()
        # We process the autosaving if necessary.
        self.autosave.process(test_completed=True)
