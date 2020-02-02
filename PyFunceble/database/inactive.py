"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the inactive database interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

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

from datetime import datetime, timedelta

import PyFunceble


class InactiveDB:  # pylint: disable=too-many-instance-attributes
    """
    Provides the inactive database logic and interface.

    :param str filename: The name of the file we are processing.
    """

    # We initiate a variable which will save the
    # cache about who are present or not into the database.
    is_present_cache = {}

    # Saves the whole database content.
    database = {}

    # Save the operation authorization.
    authorized = False

    # Save the filename we are operating.
    filename = None

    def __init__(self, filename, mysql_db=None, parent_process=False):
        self.one_day = timedelta(days=1)
        self.database_file = ""

        # We get the authorization status.
        self.authorized = self.authorization()
        # We share the parent state.
        self.parent = parent_process

        PyFunceble.LOGGER.debug(f"Authorization: {self.authorized}")

        if self.authorized:
            # We convert the number of days between the database retest
            # to seconds.
            self.days = timedelta(days=PyFunceble.CONFIGURATION.days_between_db_retest)

            if PyFunceble.CONFIGURATION.db_type == "json":
                # We set the path to the inactive database file.
                self.database_file = "{0}{1}".format(
                    PyFunceble.CONFIG_DIRECTORY,
                    PyFunceble.OUTPUTS.default_files.inactive_db,
                )

            # We share the filename.
            self.filename = filename

            # We get the db instance.
            self.mysql_db = mysql_db

            self.table_name = self.get_table_name()
            self.to_retest = self.get_to_retest()

            PyFunceble.LOGGER.debug(f"DB: {self.mysql_db}")
            PyFunceble.LOGGER.debug(f"Table Name: {self.table_name}")
            PyFunceble.LOGGER.debug(f"DB (File): {self.database_file}")

            # We initiate the database.
            self.initiate()

    def __contains__(self, subject):
        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION.db_type == "json":
                if subject not in self.is_present_cache:
                    self.is_present_cache[subject] = False

                    for element in [
                        x for x in self.database[self.filename].keys() if x.isdigit()
                    ]:
                        if subject in self[element]:
                            self.is_present_cache[subject] = True
                            break

                return self.is_present_cache[subject]

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                query = (
                    "SELECT COUNT(*) "
                    "FROM {0} "
                    "WHERE subject = %(subject)s AND file_path = %(file)s"
                ).format(self.table_name)

                with self.mysql_db.get_connection() as cursor:
                    cursor.execute(query, {"subject": subject, "file": self.filename})

                    fetched = cursor.fetchone()

                return fetched["COUNT(*)"]

        return False  # pragma: no cover

    def __getitem__(self, index):
        if (
            self.authorized
            and PyFunceble.CONFIGURATION.db_type == "json"
            and self.filename in self.database
            and index in self.database[self.filename]
        ):
            return self.database[self.filename][index]
        return []

    def __setitem__(self, index, value):
        if PyFunceble.CONFIGURATION.db_type == "json":
            actual_state = self[index]

            if actual_state:
                if isinstance(actual_state, dict):
                    if isinstance(value, dict):  # pragma: no cover
                        self.database[self.filename][index] = PyFunceble.helpers.Merge(
                            value
                        ).into(self.database[self.filename][index])
                    else:  # pragma: no cover
                        self.database[self.filename][index] = value
                elif isinstance(actual_state, list):  # pragma: no cover
                    if isinstance(value, list):
                        PyFunceble.helpers.Merge(value).into(
                            self.database[self.filename][index], strict=False
                        )
                    else:  # pragma: no cover
                        self.database[self.filename][index].append(value)

                    self.database[self.filename][index] = PyFunceble.helpers.List(
                        self.database[self.filename][index]
                    ).format()
                else:  # pragma: no cover
                    self.database[self.filename][index] = value
            else:
                if self.filename not in self.database:
                    self.database[self.filename] = {index: value}
                else:
                    self.database[self.filename][index] = value

    @classmethod
    def authorization(cls):
        """
        Provides the execution authorization.
        """

        return PyFunceble.CONFIGURATION.inactive_database

    def get_table_name(self):
        """
        Returns the name of the table to use.
        """

        if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
            return self.mysql_db.tables["inactive"]
        return "inactive"

    def _merge(self):
        """
        Merges the database with the older one which
        has already been set into the database.
        """

        if self.authorized and PyFunceble.CONFIGURATION.db_type == "json":
            # We are authorized to operate.

            # We get the content of the database.
            database_content = PyFunceble.helpers.Dict().from_json_file(
                self.database_file
            )

            # We get the database top keys.
            database_top_keys = [
                x for x in database_content.keys() if database_content[x]
            ]

            for database_top_key in database_top_keys:
                # We loop through the list of database top keys.

                # We get the list of lower indexes.
                database_low_keys = database_content[database_top_key].keys()

                for database_low_key in database_low_keys:
                    # We loop through the lower keys.

                    if isinstance(
                        database_content[database_top_key][database_low_key], list
                    ):  # pragma: no cover
                        to_set = {
                            x: ""
                            for x in database_content[database_top_key][
                                database_low_key
                            ]
                        }
                    else:
                        to_set = database_content[database_top_key][database_low_key]

                    if database_top_key not in self.database:
                        self.database[database_top_key] = {database_low_key: to_set}
                    else:
                        if database_low_key in self.database[database_top_key]:
                            self.database[database_top_key][
                                database_low_key
                            ] = PyFunceble.helpers.Merge(to_set).into(
                                self.database[database_top_key][database_low_key],
                                strict=False,
                            )
                        else:  # pragma: no cover
                            self.database[database_top_key][database_low_key] = to_set

            PyFunceble.LOGGER.info("Merged possible old to the new format")

    def load(self):
        """
        Loads the content of the database file.
        """

        if self.authorized and PyFunceble.CONFIGURATION.db_type == "json":
            # We are authorized to operate.

            if PyFunceble.helpers.File(self.database_file).exists():
                # The database file exists.

                self._merge()

                if (
                    self.filename in self.database
                    and "to_test" in self.database[self.filename]
                ):
                    new_time = str(
                        int(
                            (
                                datetime.now() - self.one_day - timedelta(seconds=100)
                            ).timestamp()
                        )
                    )
                    self.database[self.filename][new_time] = self.database[
                        self.filename
                    ]["to_test"]

                    del self.database[self.filename]["to_test"]
            else:
                # The database file do not exists.

                # We initiate an empty database.
                self.database = {self.filename: {}}

            if self.filename not in self.database:  # pragma: no cover
                # We create the current file namepace
                self.database[self.filename] = {}

            PyFunceble.LOGGER.info(
                "Database content loaded in memory. (DATASET WONT BE LOGGED)"
            )

    def save(self):
        """
        Saves the current database into the database file.
        """

        if (
            self.authorized
            and self.parent
            and PyFunceble.CONFIGURATION.db_type == "json"
        ):
            # We are authorized to operate.

            # We save the current database state into the database file.
            PyFunceble.helpers.Dict(self.database).to_json_file(self.database_file)

            PyFunceble.LOGGER.info(f"Saved database into {repr(self.database_file)}.")

    def initiate(self):
        """
        Initiates the databsse.
        """

        if self.authorized:
            # * We are authorized to operate.
            # and
            # * The filename is already in the database.

            # We load the database.
            self.load()

            self.save()

    @classmethod
    def timestamp(cls):
        """
        Gets the timestamp where we are going to save our current list.

        :return: The timestamp to append with the currently tested element.
        :rtype: int|str
        """

        # We return the current time.
        return int(datetime.now().timestamp())

    def add(self, subject, status):
        """
        Adds the given subject into the database.

        :param str subject: The subject we are working with.
        :param str status: The status of the given subject.
        """

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION.db_type == "json":
                # We get the timestamp to use as index.
                timestamp = str(self.timestamp())

                if self.filename in self.database:
                    # * The file path is not into the database.

                    self.remove(subject)

                # We initiate the file path and its content into the database.
                self[timestamp] = {subject: status}

                PyFunceble.LOGGER.info(
                    f"Indexed {repr(subject)} with the status "
                    f"{repr(status)} into {repr(self.filename)} database's."
                )

                # And we save the database.
                self.save()
            elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                digest = PyFunceble.helpers.Hash(algo="sha256").data(
                    bytes(self.filename + subject, "utf-8")
                )

                query = (
                    "INSERT INTO {0} "
                    "(file_path, subject, status, digest) "
                    "VALUES (%(file)s, %(subject)s, %(status)s, %(digest)s)"
                ).format(self.table_name)

                with self.mysql_db.get_connection() as cursor:

                    playload = {
                        "file": self.filename,
                        "subject": subject,
                        "status": status,
                        "digest": digest,
                    }

                    try:
                        cursor.execute(query, playload)

                        PyFunceble.LOGGER.info(
                            f"Inserted into the database: \n {playload}"
                        )
                    except self.mysql_db.errors:
                        query = (
                            "UPDATE {0} "
                            "SET subject = %(subject)s, status = %(status)s "
                            "WHERE digest = %(digest)s"
                        ).format(self.table_name)

                        cursor.execute(
                            query,
                            {"subject": subject, "status": status, "digest": digest},
                        )

                        PyFunceble.LOGGER.info(
                            "Data already indexed, updated the modified "
                            f"column of the row related to {repr(subject)}."
                        )

    def remove(self, subject):
        """
        Removes all occurrences of the given subject from the database.

        :param str subject: The subject we are working with.
        """

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION.db_type == "json":
                for data in self.database[self.filename]:
                    # We loop through the index of the file database.

                    if subject in self[data]:
                        # The currently tested element into the currently read index.

                        self[data] = PyFunceble.helpers.Dict(self[data]).remove_key(
                            subject
                        )

                        PyFunceble.LOGGER.info(
                            "Cleaned the data related to " f"{repr(subject)}."
                        )

                to_delete = [
                    x for x, y in self.database[self.filename].items() if not y
                ]

                for index in to_delete:
                    del self.database[self.filename][index]

                # And we save the data into the database.
                self.save()
            elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                # We construct the query we are going to execute.
                query = (
                    "DELETE FROM {0} "
                    "WHERE file_path = %(file)s "
                    "AND subject = %(subject)s"
                ).format(self.table_name)

                with self.mysql_db.get_connection() as cursor:
                    cursor.execute(query, {"file": self.filename, "subject": subject})

                    PyFunceble.LOGGER.info(
                        "Cleaned the data related to "
                        f"{repr(subject)} and {repr(self.filename)} from "
                        "the {repr(self.table_name)} table."
                    )

    def __execute_query_retest_already_tested(self, query):  # pragma: no cover
        """
        Executes the query to get the list to retest or already tested.
        """

        with self.mysql_db.get_connection() as cursor:
            cursor.execute(query, {"file": self.filename, "days": self.days})
            fetched = cursor.fetchall()

            if fetched:
                return {x["subject"] for x in fetched}

        return set()

    def get_to_retest(self):  # pylint: pragma: no cover
        """
        Returns a set of subject to restest.
        """

        PyFunceble.LOGGER.info(
            "Getting the list of subjects to retest (DATASET WONT BE LOGGED)"
        )

        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                try:
                    return {
                        z
                        for x, y in self.database[self.filename].items()
                        if x.isdigit()
                        and datetime.now()
                        > datetime.fromtimestamp(float(x)) + self.days
                        for z in y.keys()
                    }
                except KeyError:
                    return set()

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                query = (
                    "SELECT * FROM {0} WHERE file_path = %(file)s "
                    "AND CAST(UNIX_TIMESTAMP() AS {1}) "
                    "> (CAST(UNIX_TIMESTAMP(modified) AS {1}) + CAST(%(days)s AS {1}))"
                ).format(self.table_name, self.mysql_db.int_cast_type)

                return self.__execute_query_retest_already_tested(query)
        return set()

    def get_already_tested(self):  # pragma: no cover
        """
        Returns a set of already tested subjects.
        """

        PyFunceble.LOGGER.info(
            "Getting the list of already tested (DATASET WONT BE LOGGED)"
        )

        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                try:
                    return {
                        z
                        for x, y in self.database[self.filename].items()
                        if x.isdigit()
                        and datetime.now()
                        < datetime.fromtimestamp(float(x)) + self.days
                        for z in y.keys()
                    }
                except KeyError:
                    return set()

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                query = (
                    "SELECT * FROM {0} WHERE file_path= %(file)s "
                    "AND CAST(UNIX_TIMESTAMP() AS {1}) "
                    "< (CAST(UNIX_TIMESTAMP(modified) AS {1}) + CAST(%(days)s AS {1}))"
                ).format(self.table_name, self.mysql_db.int_cast_type)

                return self.__execute_query_retest_already_tested(query)
        return set()
