"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the auto-continue engine.

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


import PyFunceble


class AutoContinue:  # pylint: disable=too-many-instance-attributes
    """
    Provides the auto-continue subsystem.
    """

    # Save the content of the database.
    database = {}
    # Save the database file
    database_file = None
    # Save the operation authorization.
    authorized = False

    # Save the filename we are working with.
    filename = None

    def __init__(self, filename, parent_process=False):
        # We get the operation authorization.
        self.authorized = self.authorization()
        self.database_file = ""
        # We share the filename.
        self.filename = filename
        # We preset the filename namespace.
        self.database[self.filename] = {}

        self.table_name = self.get_table_name()

        # We share if we are under the parent process.
        self.parent = parent_process

        PyFunceble.LOGGER.debug(f"Authorization: {self.authorized}")
        PyFunceble.LOGGER.debug(f"Table Name: {self.table_name}")

        if self.authorized:
            # We are authorized to operate.

            PyFunceble.LOGGER.info("Process authorized.")

            if PyFunceble.CONFIGURATION.db_type == "json":
                # We set the location of the database file.
                self.database_file = (
                    PyFunceble.OUTPUT_DIRECTORY
                    + PyFunceble.OUTPUTS.parent_directory
                    + PyFunceble.OUTPUTS.logs.filenames.auto_continue
                )

            PyFunceble.LOGGER.debug(f"DB (File): {self.database_file}")

            # We load the backup (if existant).
            self.load()

            if self.parent and (
                self.filename not in self.database or not self.database[self.filename]
            ):
                # The database of the file we are
                # currently testing is empty.

                PyFunceble.LOGGER.info(
                    "Process authorized, is the parent process and the file "
                    "to test not indexed. Cleaning directory structure."
                )

                # We clean the output directory.
                PyFunceble.output.Clean(file_path=self.filename)
        elif self.parent:
            # We are not authorized to operate.

            PyFunceble.LOGGER.info(
                "Process not authorized but is the parent process. "
                "Cleaning directory structure."
            )

            # We clean the output directory.
            PyFunceble.output.Clean(file_path=self.filename)

    def __contains__(self, index):  # pragma: no cover
        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                if self.filename in self.database:
                    for status, status_data in self.database[self.filename].items():
                        if status == "complements":
                            continue

                        if index in status_data:
                            PyFunceble.LOGGER.info(
                                f"{index} is present into the database."
                            )
                            return True

                PyFunceble.LOGGER.info(f"{index} is not present into the database.")
                return False

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                query = (
                    "SELECT COUNT(*) "
                    "FROM {0} "
                    "WHERE subject = %(subject)s AND file_path = %(file)s"
                ).format(self.table_name)

                with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
                    cursor.execute(query, {"subject": index, "file": self.filename})

                    fetched = cursor.fetchone()

                if fetched["COUNT(*)"] != 0:
                    PyFunceble.LOGGER.info(f"{index} is present into the database.")
                    return True

                PyFunceble.LOGGER.info(f"{index} is not present into the database.")
                return False

        PyFunceble.LOGGER.info(
            f"Could not check if {index} is present into the database. "
            "Unauthorized action."
        )
        return False

    @classmethod
    def authorization(cls):
        """
        Provides the execution authorization.
        """

        return (
            PyFunceble.CONFIGURATION.auto_continue
            and not PyFunceble.CONFIGURATION.no_files
        )

    @classmethod
    def get_table_name(cls):
        """
        Returns the name of the table to use.
        """

        if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
            return PyFunceble.engine.MySQL.tables["auto_continue"]
        return None

    def is_empty(self):
        """
        Checks if the database related to the currently tested
        file is empty.
        """

        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                if (
                    self.filename not in self.database
                    or not self.database[self.filename]
                ):
                    PyFunceble.LOGGER.info("File to test was not previously indexed.")
                    return True

                PyFunceble.LOGGER.info("File to test was previously indexed.")
                return False

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                query = "SELECT COUNT(*) FROM {0} WHERE file_path = %(file)s".format(
                    self.table_name
                )

                with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
                    cursor.execute(query, {"file": self.filename})

                    fetched = cursor.fetchone()

                if fetched["COUNT(*)"] == 0:
                    PyFunceble.LOGGER.info("File to test was not previously indexed.")
                    return True

                PyFunceble.LOGGER.info("File to test was previously indexed.")
                return False

        PyFunceble.LOGGER.info(  # pragma: no cover
            "Could not check if the file to test "
            "was previously indexed. Unauthorized action."
        )
        return False  # pragma: no cover

    def add(self, subject, status):
        """
        Adds the given subject into the database.
        """

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION.db_type == "json":
                if self.filename in self.database:
                    # We already have something related
                    # to the file we are testing.

                    if status in self.database[self.filename]:
                        # The status is already registered.

                        # We set the new data.
                        self.database[self.filename][status].append(subject)
                    else:
                        # We set the new data.
                        self.database[self.filename][status] = [subject]
                else:
                    # We have nothing related to the file
                    # we are testing.

                    # We initiate the file index.
                    self.database[self.filename] = {status: [subject]}

                PyFunceble.LOGGER.info(
                    f"Indexed {repr(subject)} with the status "
                    f"{repr(status)} into {repr(self.filename)} database's."
                )

                # We save everything.
                self.save()
            elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                # We construct the query string.

                digest = PyFunceble.helpers.Hash(algo="sha256").data(
                    bytes(self.filename + subject + status, "utf-8")
                )

                with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:

                    query = (
                        "INSERT INTO {0} "
                        "(file_path, subject, status, is_complement, digest) "
                        "VALUES (%(file)s, %(subject)s, %(status)s, %(is_complement)s, %(digest)s)"
                    ).format(self.table_name)

                    try:
                        playload = {
                            "file": self.filename,
                            "subject": subject,
                            "status": status,
                            "is_complement": int(False),
                            "digest": digest,
                        }
                        cursor.execute(query, playload)

                        PyFunceble.LOGGER.info(
                            f"Inserted into the database: \n {playload}"
                        )
                    except PyFunceble.engine.MySQL.errors:
                        query = (
                            "UPDATE {0} "
                            "SET subject = %(subject)s "
                            "WHERE digest = %(digest)s"
                        ).format(self.table_name)

                        cursor.execute(query, {"subject": subject, "digest": digest})

                        PyFunceble.LOGGER.info(
                            "Data already indexed, updated the modified "
                            f"column of the row related to {repr(subject)}."
                        )

    def save(self):
        """
        Saves the current state of the database.
        """

        if (
            self.authorized
            and self.parent
            and PyFunceble.CONFIGURATION.db_type == "json"
        ):
            # We are authoried to operate.

            # We save the current database state.
            PyFunceble.helpers.Dict(self.database).to_json_file(self.database_file)

            PyFunceble.LOGGER.info(f"Saved database into {repr(self.database_file)}.")

    def load(self):
        """
        Loads previously saved database.
        """

        if self.authorized and PyFunceble.CONFIGURATION.db_type == "json":
            # We are authorized to operate.

            if PyFunceble.helpers.File(self.database_file).exists():
                # The database file exists.

                # We get its content and save it inside backup_content.
                self.database = PyFunceble.helpers.Dict().from_json_file(
                    self.database_file
                )
            else:
                # The database file do not exists.

                # We initiate an empty database.
                self.database = {self.filename: {}}

            PyFunceble.LOGGER.info(f"Loaded {repr(self.database_file)} in memory.")

    def clean(self):
        """
        Cleans the database.
        """

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION.db_type == "json":
                # We empty the database.
                self.database[self.filename] = {}

                # And we save the current database state.
                PyFunceble.helpers.Dict(self.database).to_json_file(self.database_file)

                PyFunceble.LOGGER.info(
                    "Cleaned the data related to "
                    f"{repr(self.filename)} from {repr(self.database_file)}."
                )
            elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                # We construct the query we are going to execute.
                query = "DELETE FROM {0} WHERE file_path = %(file)s".format(
                    self.table_name
                )

                with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
                    cursor.execute(query, {"file": self.filename})

                    PyFunceble.LOGGER.info(
                        "Cleaned the data related to "
                        f"{repr(self.filename)} from the {repr(self.table_name)} table."
                    )

    def update_counters(self):  # pragma: no cover
        """
        Updates the counters.
        """

        if self.authorized and self.parent:
            # We are authorized to operate.

            # We create a list of all status we are working with.
            statuses = PyFunceble.STATUS.official.keys()

            # We preset the number of tested.
            tested = 0

            for status in statuses:
                # We loop through the list of status.

                if PyFunceble.CONFIGURATION.db_type == "json":
                    try:
                        # We get the number of tested of the currently read
                        # status.
                        tested_for_status = len(
                            self.database[self.filename][
                                PyFunceble.STATUS.official[status]
                            ]
                        )

                        # We then update/transfert it to its global place.
                        PyFunceble.INTERN["counter"]["number"][
                            status
                        ] = tested_for_status

                        PyFunceble.LOGGER.debug(
                            f"Counter of {repr(status)} set to {tested_for_status}."
                        )

                        # We finally increate the number of tested.
                        tested += tested_for_status
                    except KeyError:
                        PyFunceble.INTERN["counter"]["number"][status] = 0
                        continue
                elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                    query = (
                        "SELECT COUNT(*) "
                        "FROM {0} "
                        "WHERE status = %(status)s "
                        "AND file_path = %(file)s "
                    ).format(self.table_name)

                    with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
                        cursor.execute(
                            query,
                            {
                                "status": PyFunceble.STATUS.official[status],
                                "file": self.filename,
                            },
                        )

                        fetched = cursor.fetchone()["COUNT(*)"]

                        PyFunceble.INTERN["counter"]["number"][status] = fetched

                        PyFunceble.LOGGER.debug(
                            f"Counter of {repr(status)} set to {fetched}."
                        )

                        # We then update/transfert it to its global place.
                        tested += fetched

            # We update/transfert the number of tested globally.
            PyFunceble.INTERN["counter"]["number"]["tested"] = tested
            PyFunceble.LOGGER.debug(f"Totally tested set to {repr(tested)}.")

    def get_already_tested(self):
        """
        Returns the list of subjects which were already tested as a set.
        """

        PyFunceble.LOGGER.info(
            "Getting the list of already tested (DATASET WONT BE LOGGED)"
        )

        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                try:
                    return {
                        y
                        for state, x in self.database[self.filename].items()
                        for y in x
                        if state not in ["complements"]
                    }
                except KeyError:  # pragma: no cover
                    pass
            elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                query = "SELECT * FROM {0} WHERE file_path = %(file)s".format(
                    self.table_name
                )

                with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
                    cursor.execute(query, {"file": self.filename})

                    fetched = cursor.fetchall()

                    if fetched:
                        return {x["subject"] for x in fetched}
        return set()  # pragma: no cover

    def __generate_complements(self):  # pragma: no cover
        """
        Generates the complements from the given list of tested.
        """

        # We get the list of domains we are going to work with.
        already_tested = self.get_already_tested()
        result = PyFunceble.get_complements(already_tested)

        # We remove the already tested subjects.
        return set(PyFunceble.helpers.List(result).format()) - already_tested

    def __get_or_generate_complements_json(self):  # pragma: no cover
        """
        Gets or generates the complements while working with
        as JSON formatted database.
        """

        result = []

        if "complements" not in self.database[self.filename].keys():
            # The complements are not saved,

            already_tested = self.get_already_tested()
            result = PyFunceble.get_complements(already_tested)

            # We remove the already tested subjects.
            result = set(PyFunceble.helpers.List(result).format()) - already_tested

            # We save the constructed list of complements
            self.database[self.filename]["complements"] = list(result)

            self.save()
        else:
            # We get the complements we still have to test.
            result = self.database[self.filename]["complements"]

        return result

    def __get_or_generate_complements_mysql(self):  # pragma: no cover
        """
        Gets or generates the complements while working with
        as MySQL/MariaDB formatted database.
        """

        result = []

        query = (
            "SELECT * "
            "FROM {0} "
            "WHERE file_path = %(file)s "
            "AND is_complement = %(is_complement)s".format(self.table_name)
        )

        with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
            cursor.execute(query, {"file": self.filename, "is_complement": int(True)})
            fetched = cursor.fetchall()

            if fetched:
                result = [x["subject"] for x in fetched]
            else:
                result = self.__generate_complements()

        query = (
            "INSERT INTO {0} "
            "(file_path, subject, status, is_complement, digest) "
            "VALUES (%(file)s, %(subject)s, %(status)s, %(is_complement)s, %(digest)s)".format(
                self.table_name
            )
        )

        to_execute = [
            {
                "file": self.filename,
                "subject": subject,
                "status": "",
                "is_complement": int(True),
                "digest": PyFunceble.helpers.Hash(algo="sha256").data(
                    bytes(self.filename + subject, "utf-8")
                ),
            }
            for subject in result
        ]

        with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
            try:
                cursor.executemany(query, to_execute)
            except PyFunceble.engine.MySQL.errors:
                pass

        return result

    def get_or_generate_complements(self):  # pragma: no cover
        """
        Gets or generates the complements.
        """

        PyFunceble.LOGGER.info("Generate/Get complements (DATASET WONT BE LOGGED)")

        if self.authorized and PyFunceble.CONFIGURATION.generate_complements:
            # We aer authorized to operate.

            if PyFunceble.CONFIGURATION.db_type == "json":
                return self.__get_or_generate_complements_json()
            if PyFunceble.CONFIGURATION.db_type in ["mysql", "mariadb"]:
                return self.__get_or_generate_complements_mysql()

        return list()
