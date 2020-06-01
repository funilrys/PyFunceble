"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the file testing core interface.

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

from tempfile import NamedTemporaryFile

from domain2idna import get as domain2idna

import PyFunceble

from .cli import CLICore


class FileCore(CLICore):  # pylint: disable=too-many-instance-attributes
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

    accepted_file_content_types = ["url", "domain"]

    def __init__(self, file, file_content_type="domain"):
        super().__init__()

        if file_content_type.lower() not in self.accepted_file_content_types:
            raise PyFunceble.exceptions.WrongParameterValue(
                f"<file_content_type> ({file_content_type}) "
                "not in {self.accepted_file_content_types}."
            )

        self.file = self.download_link(file)
        self.file_type = file_content_type.lower()

        self.inactive_db = PyFunceble.database.Inactive(self.file, parent_process=True)
        self.mining = PyFunceble.engine.Mining(self.file)
        self.autocontinue = PyFunceble.engine.AutoContinue(
            self.file, parent_process=True
        )

    @classmethod
    def download_link(cls, input_file):  # pragma: no cover
        """
        Downloads the file if it is an URL and return the name of the new file to test.
        """

        if PyFunceble.Check(input_file).is_url():
            # We get the destination.
            destination = input_file.split("/")[-1]

            if input_file and PyFunceble.engine.AutoContinue(destination).is_empty():
                # The given file is an URL.

                if (
                    not PyFunceble.helpers.File(destination).exists()
                    or PyFunceble.INTERN["counter"]["number"]["tested"] == 0
                ):
                    # The filename does not exist in the current directory
                    # or the currently number of tested is equal to 0.

                    # We download the content of the link.
                    PyFunceble.helpers.Download(input_file).text(
                        destination=destination
                    )

                    PyFunceble.LOGGER.info(
                        f"Downloaded {repr(input_file)} into {repr(destination)}"
                    )

            return destination
        return input_file

    def generate_complement_status_file(self, subject, status):
        """
        Generate the complements status files.
        """

        if self.complements_test_started:
            PyFunceble.output.Generate(
                subject, f"file_{self.file_type}", status
            ).complements_file()

    @classmethod
    def get_complements(cls, auto_continue_db):
        """
        Generate a list of complements to test.
        """

        if (
            PyFunceble.CONFIGURATION.generate_complements
            and auto_continue_db
            and auto_continue_db.authorized
        ):
            # * The user want us to generate and test the list
            # of all complements.
            # and
            # * The autocontinue subsystem is activated.

            # We get/generate the complements.
            for complement in auto_continue_db.get_or_generate_complements():
                yield complement

    def generate_files_of_status(
        self, status, include_entries_without_changes=False
    ):  # pragma: no cover
        """
        Generates the status file of all subjects of the given status.

        :param str status: A status to filter.
        :param bool include_entries_without_changes: Descriptive enough.
        """

        if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:

            to_select = (
                "SELECT tested as subject, status, status_source, expiration_date, "
                "http_status_code, whois_server, file_path "
                "FROM {0} WHERE status = %(official_status)s "
                "AND file_path = %(file_path)s ORDER BY subject ASC"
            ).format(PyFunceble.engine.MySQL.tables["tested"])

            with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
                cursor.execute(
                    to_select, {"official_status": status, "file_path": self.file}
                )

                fetched = cursor.fetchall()

                if fetched:
                    for data in fetched:
                        generate = PyFunceble.output.Generate(
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

                        if include_entries_without_changes:
                            generate.status_file(exclude_file_generation=False)
                        else:
                            generate.status_file(
                                exclude_file_generation=self.inactive_db.authorized
                                and data["status"] not in self.list_of_up_statuses
                                and data["subject"] in self.inactive_db.to_retest
                            )

    def generate_files(self, include_entries_without_changes=False):  # pragma: no cover
        """
        Generates all needed files.
        """

        if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
            self.preset.reset_counters()

            if PyFunceble.CONFIGURATION.syntax:
                self.generate_files_of_status(
                    PyFunceble.STATUS.official.valid,
                    include_entries_without_changes=include_entries_without_changes,
                )
            elif PyFunceble.CONFIGURATION.reputation:
                self.generate_files_of_status(
                    PyFunceble.STATUS.official.sane,
                    include_entries_without_changes=include_entries_without_changes,
                )
            else:
                self.generate_files_of_status(
                    PyFunceble.STATUS.official.up,
                    include_entries_without_changes=include_entries_without_changes,
                )

            if PyFunceble.CONFIGURATION.reputation:
                self.generate_files_of_status(
                    PyFunceble.STATUS.official.malicious,
                    include_entries_without_changes=include_entries_without_changes,
                )
            else:
                self.generate_files_of_status(
                    PyFunceble.STATUS.official.down,
                    include_entries_without_changes=include_entries_without_changes,
                )

            self.generate_files_of_status(
                PyFunceble.STATUS.official.invalid,
                include_entries_without_changes=include_entries_without_changes,
            )

    def test(self, subject):
        """
        Tests the given subject and return it's results.
        """

        if PyFunceble.CONFIGURATION.idna_conversion:
            subject = domain2idna(subject)

        if isinstance(PyFunceble.CONFIGURATION.cooldown_time, (float, int)):
            PyFunceble.sleep(PyFunceble.CONFIGURATION.cooldown_time)

        if PyFunceble.CONFIGURATION.syntax:
            if "url" in self.file_type:
                result = PyFunceble.status.UrlSyntax(
                    subject,
                    whois_db=self.whois_db,
                    inactive_db=self.inactive_db,
                    filename=self.file,
                ).get()
            else:
                result = PyFunceble.status.DomainAndIpSyntax(
                    subject.lower(),
                    whois_db=self.whois_db,
                    inactive_db=self.inactive_db,
                    filename=self.file,
                ).get()
        elif PyFunceble.CONFIGURATION.reputation:
            if "url" in self.file_type:
                result = PyFunceble.status.UrlReputation(
                    subject,
                    whois_db=self.whois_db,
                    inactive_db=self.inactive_db,
                    filename=self.file,
                ).get()
            else:
                result = PyFunceble.status.DomainAndIPReputation(
                    subject.lower(),
                    whois_db=self.whois_db,
                    inactive_db=self.inactive_db,
                    filename=self.file,
                ).get()
        elif "url" in self.file_type:
            result = PyFunceble.status.UrlAvailability(
                subject,
                whois_db=self.whois_db,
                inactive_db=self.inactive_db,
                filename=self.file,
            ).get()
        else:
            result = PyFunceble.status.DomainAndIpAvailability(
                subject.lower(),
                whois_db=self.whois_db,
                inactive_db=self.inactive_db,
                filename=self.file,
            ).get()

        self.generate_complement_status_file(result["tested"], result["status"])
        self.save_into_database(result, self.file)

        return result

    # pylint: disable=too-many-return-statements
    @classmethod
    def should_be_ignored(
        cls, subject, auto_continue_db, inactive_db, ignore_inactive_db_check=False
    ):
        """
        Given a subject which is supposed to be tested,
        we check if we should ignore it.
        """

        if not subject:
            PyFunceble.LOGGER.debug(f"Ignored {subject} because not true.")
            return True

        if subject.startswith(PyFunceble.converter.File.comment_sign):
            PyFunceble.LOGGER.debug(
                f"Ignored {subject} because it starts with comment sign."
            )
            return True

        if auto_continue_db and subject in auto_continue_db.get_already_tested():
            PyFunceble.LOGGER.debug(
                f"Ignored {subject} because it is into the list of already tested (autocontinue)."
            )
            return True

        if (
            not ignore_inactive_db_check
            and inactive_db
            and subject in inactive_db.get_already_tested()
        ):
            PyFunceble.LOGGER.debug(
                f"Ignored {subject} because it is into the list of already tested (inactive_db)."
            )
            return True

        if PyFunceble.helpers.Regex(cls.regex_ignore).match(
            subject, return_match=False
        ):
            PyFunceble.LOGGER.debug(f"Ignored {subject} because it match our regex.")
            return True

        if (
            not PyFunceble.CONFIGURATION.local
            and PyFunceble.Check(subject).is_reserved_ip()
        ):
            PyFunceble.LOGGER.debug(
                f"Ignored {subject} because it is a reserved IP and we are not in local test."
            )
            return True

        if PyFunceble.CONFIGURATION.filter and not PyFunceble.helpers.Regex(
            PyFunceble.CONFIGURATION.filter
        ).match(subject, return_match=False):
            PyFunceble.LOGGER.debug(
                f"Ignored {subject} because it does not "
                f"match the given filter ({PyFunceble.CONFIGURATION.fileter})"
            )
            return True

        return False

    def post_test_treatment(
        self,
        test_output,
        file_content_type,
        complements_test_started=False,
        auto_continue_db=None,
        inactive_db=None,
        mining=None,
        whois_db=None,
    ):
        """
        Do the post test treatment.
        """

        if auto_continue_db:
            auto_continue_db.add(test_output["tested"], test_output["status"])

        if test_output["status"].lower() in self.list_of_up_statuses:
            if mining:
                mining.mine(test_output["tested"], file_content_type)

            if inactive_db and test_output["tested"] in inactive_db:
                PyFunceble.output.Generate(
                    test_output["tested"],
                    f"file_{file_content_type}",
                    PyFunceble.STATUS.official.up,
                ).analytic_file("suspicious")

                inactive_db.remove(test_output["tested"])
        elif inactive_db:
            inactive_db.add(test_output["tested"], test_output["status"])

        if (
            auto_continue_db
            and complements_test_started
            and PyFunceble.CONFIGURATION.db_type == "json"
        ):
            if "complements" in auto_continue_db.database:

                while test_output["tested"] in auto_continue_db.database["complements"]:
                    auto_continue_db.database["complements"].remove(
                        test_output["tested"]
                    )
                    auto_continue_db.save()

        if (
            whois_db
            and test_output["expiration_date"]
            and test_output["whois_record"]
            and test_output["tested"]
        ):
            whois_db.add(
                test_output["tested"],
                test_output["expiration_date"],
                test_output["whois_record"],
            )

        if (
            PyFunceble.CONFIGURATION.db_type == "json"
            and PyFunceble.CONFIGURATION.multiprocess
        ):
            generate = PyFunceble.output.Generate(
                test_output["tested"],
                f"file_{self.file_type}",
                test_output["status"],
                source=test_output["status_source"],
                expiration_date=test_output["expiration_date"],
                http_status_code=test_output["http_status_code"],
                whois_server=test_output["whois_server"],
                filename=self.file,
                end=True,
            )

            generate.prints_status_file()
            generate.unified_file()

    def cleanup(self, auto_continue_db, auto_save, test_completed=False):
        """
        Runs the logic to run at the end of all test.
        """

        if test_completed:
            auto_continue_db.update_counters()
            self.generate_files()
            self.sort_generated_files()
            auto_continue_db.clean()
            auto_save.process(test_completed=test_completed)
        elif auto_save.is_time_exceed():
            auto_continue_db.update_counters()
            self.generate_files()
            self.sort_generated_files()
            auto_save.process(test_completed=test_completed)

    def __run_single_test(self, subject, ignore_inactive_db_check=False):
        """
        Run a test for a single subject.
        """

        self.print_header()

        if not self.should_be_ignored(
            subject,
            auto_continue_db=self.autocontinue,
            inactive_db=self.inactive_db,
            ignore_inactive_db_check=ignore_inactive_db_check,
        ):
            result = self.test(subject)

            self.post_test_treatment(
                result,
                self.file_type,
                complements_test_started=self.complements_test_started,
                auto_continue_db=self.autocontinue,
                inactive_db=self.inactive_db,
                mining=self.mining,
                whois_db=self.whois_db,
            )
        elif self.autosave.authorized or PyFunceble.CONFIGURATION.print_dots:
            # We are under a CI/CD environment.

            PyFunceble.LOGGER.info(f"Skipped {subject!r}.")

            # We print a dot.
            print(".", end="")

        self.cleanup(self.autocontinue, self.autosave, test_completed=False)

    @classmethod
    def get_subjects(cls, line):
        """
        Given a line, we give the list of subjects
        to test.
        """

        if PyFunceble.CONFIGURATION.adblock:
            subjects = PyFunceble.converter.AdBlock(
                line, aggressive=PyFunceble.CONFIGURATION.aggressive
            ).get_converted()
        else:
            subjects = PyFunceble.converter.File(line).get_converted()

        return subjects

    def __test_line(self, line, ignore_inactive_db_check=False):
        """
        Tests a given line.
        """

        subjects = self.get_subjects(line)

        if isinstance(subjects, list):
            for subject in subjects:
                self.__run_single_test(
                    subject, ignore_inactive_db_check=ignore_inactive_db_check
                )
        else:
            self.__run_single_test(
                subjects, ignore_inactive_db_check=ignore_inactive_db_check
            )

    def construct_and_get_shadow_file(
        self, file_stream, ignore_inactive_db_check=False
    ):
        """
        Provides a path to a file which contain the list to file.

        The idea is to do a comparison between what we already tested
        and what we still have to test.
        """

        with NamedTemporaryFile(delete=False) as temp_file:
            if self.autosave.authorized or PyFunceble.CONFIGURATION.print_dots:
                print("")

            for line in file_stream:
                subjects = self.get_subjects(line)

                if isinstance(subjects, list):
                    comparison = [
                        self.should_be_ignored(
                            x,
                            auto_continue_db=self.autocontinue,
                            inactive_db=self.inactive_db,
                            ignore_inactive_db_check=ignore_inactive_db_check,
                        )
                        for x in subjects
                    ]
                else:
                    comparison = [
                        self.should_be_ignored(
                            subjects,
                            auto_continue_db=self.autocontinue,
                            inactive_db=self.inactive_db,
                            ignore_inactive_db_check=ignore_inactive_db_check,
                        )
                    ]

                if all(comparison):
                    if self.autosave.authorized or PyFunceble.CONFIGURATION.print_dots:
                        print("I", end="")

                    continue

                if self.autosave.authorized or PyFunceble.CONFIGURATION.print_dots:
                    print("S", end="")

                temp_file.write(line.encode("utf-8"))

            if self.autosave.authorized or PyFunceble.CONFIGURATION.print_dots:
                print("")

            return temp_file.name

    def run_test(self):
        """
        Run the test of the content of the given file.
        """

        with open(self.file, "r", encoding="utf-8") as file_stream, open(
            self.construct_and_get_shadow_file(file_stream), "r"
        ) as shadow_file:
            for subject in shadow_file:
                self.__test_line(subject)

            shadow_file_name = shadow_file.name

        PyFunceble.helpers.File(shadow_file_name).delete()

        if self.autocontinue.is_empty():
            with open(self.file, "r", encoding="utf-8") as file_stream, open(
                self.construct_and_get_shadow_file(
                    file_stream, ignore_inactive_db_check=True
                ),
                "r",
                encoding="utf-8",
            ) as shadow_file:
                for subject in shadow_file:
                    self.__test_line(subject, ignore_inactive_db_check=True)

                shadow_file_name = shadow_file.name

        PyFunceble.helpers.File(shadow_file_name).delete()

        for subject in self.inactive_db.get_to_retest():
            self.__test_line(subject)

        self.complements_test_started = True

        for subject in self.get_complements(self.autocontinue):
            self.__test_line(subject)

        self.complements_test_started = False

        for index, subject in self.mining.list_of_mined():
            self.__test_line(subject)
            self.mining.remove(index, subject)

        self.cleanup(self.autocontinue, self.autosave, test_completed=True)
