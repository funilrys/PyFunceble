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

from datetime import datetime, timedelta

import PyFunceble


class InactiveDB:  # pylint: disable=too-many-instance-attributes
    """
    Provides the inactive database logic and interface.

    :param str filename: The name of the file we are processing.
    """

    is_present_cache = {}
    database = {}
    authorized = False
    filename = None

    def __init__(self, filename, parent_process=False):
        self.one_day = timedelta(days=1)
        self.database_file = ""

        self.authorized = self.authorization()
        self.parent = parent_process

        PyFunceble.LOGGER.debug(f"Authorization: {self.authorized}")

        if self.authorized:
            self.days = timedelta(days=PyFunceble.CONFIGURATION.days_between_db_retest)
            self.days_between_clean = timedelta(
                days=PyFunceble.CONFIGURATION.days_between_inactive_db_clean
            )

            if PyFunceble.CONFIGURATION.db_type == "json":
                self.database_file = "{0}{1}".format(
                    PyFunceble.CONFIG_DIRECTORY,
                    PyFunceble.OUTPUTS.default_files.inactive_db,
                )

            self.filename = filename

            self.table_name = self.get_table_name()
            self.to_retest = self.get_to_retest()

            PyFunceble.LOGGER.debug(f"Table Name: {self.table_name}")
            PyFunceble.LOGGER.debug(f"DB (File): {self.database_file}")

            self.initiate()

    def __contains__(self, subject):
        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                if subject not in self.is_present_cache:
                    self.is_present_cache[subject] = False
                    if self[subject]:
                        self.is_present_cache[subject] = True

                return self.is_present_cache[subject]

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                query = (
                    "SELECT COUNT(*) "
                    "FROM {0} "
                    "WHERE subject = %(subject)s AND file_path = %(file)s"
                ).format(self.table_name)

                with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
                    cursor.execute(query, {"subject": subject, "file": self.filename})

                    fetched = cursor.fetchone()

                return fetched["COUNT(*)"]

        return False  # pragma: no cover

    def __getitem__(self, subject):
        if (
            self.authorized
            and PyFunceble.CONFIGURATION.db_type == "json"
            and self.filename in self.database
            and subject in self.database[self.filename]
        ):
            return self.database[self.filename][subject]
        return {}

    def __setitem__(self, subject, data):
        if PyFunceble.CONFIGURATION.db_type == "json":
            actual_state = self[subject]

            if actual_state:
                if isinstance(actual_state, dict):  # pragma: no cover
                    if isinstance(data, dict):
                        self.database[self.filename][
                            subject
                        ] = PyFunceble.helpers.Merge(data).into(
                            self.database[self.filename][subject]
                        )
                    else:  # pragma: no cover
                        self.database[self.filename][subject] = data
                elif isinstance(actual_state, list):  # pragma: no cover
                    if isinstance(data, list):
                        PyFunceble.helpers.Merge(data).into(
                            self.database[self.filename][subject], strict=False
                        )
                    else:  # pragma: no cover
                        self.database[self.filename][subject].append(data)

                    self.database[self.filename][subject] = PyFunceble.helpers.List(
                        self.database[self.filename][subject]
                    ).format()
                else:  # pragma: no cover
                    self.database[self.filename][subject] = data
            else:
                if self.filename not in self.database:
                    self.database[self.filename] = {subject: data}
                else:
                    self.database[self.filename][subject] = data

    def __delitem__(self, subject):
        if PyFunceble.CONFIGURATION.db_type == "json" and self[subject]:
            del self.database[self.filename][subject]

    @classmethod
    def authorization(cls):
        """
        Provides the execution authorization.
        """

        return PyFunceble.CONFIGURATION.inactive_database

    @classmethod
    def get_table_name(cls):
        """
        Returns the name of the table to use.
        """

        if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
            return PyFunceble.engine.MySQL.tables["inactive"]
        return "inactive"

    def _merge(self):
        """
        Merges the database with the older one which
        has already been set into the database.
        """

        if self.authorized and PyFunceble.CONFIGURATION.db_type == "json":
            database_content = PyFunceble.helpers.Dict().from_json_file(
                self.database_file
            )

            for database_top_key in [
                x for x in database_content.keys() if database_content[x]
            ]:

                for database_low_key, data in database_content[
                    database_top_key
                ].items():
                    to_set = {}

                    if database_low_key.isdigit():
                        last_test_date = datetime.fromtimestamp(float(database_low_key))

                        for subject, status in data.items():
                            to_set[subject] = {
                                "included_at_epoch": last_test_date.timestamp(),
                                "included_at_iso": last_test_date.isoformat(),
                                "last_retested_at_epoch": last_test_date.timestamp(),
                                "last_retested_at_iso": last_test_date.isoformat(),
                                "status": status,
                            }
                    else:
                        to_set[database_low_key] = data

                    if database_top_key not in self.database:
                        self.database[database_top_key] = to_set
                    else:
                        self.database[database_top_key].update(to_set)

            PyFunceble.LOGGER.info("Merged possible old to the new format")

    def load(self):
        """
        Loads the content of the database file.
        """

        if self.authorized and PyFunceble.CONFIGURATION.db_type == "json":
            if PyFunceble.helpers.File(self.database_file).exists():
                self._merge()
            else:
                self.database = {self.filename: {}}

            if self.filename not in self.database:  # pragma: no cover
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
            PyFunceble.helpers.Dict(self.database).to_json_file(self.database_file)

            PyFunceble.LOGGER.info(f"Saved database into {repr(self.database_file)}.")

    def clean(self):
        """
        Cleans everything which is not needed anymore.
        """

        if self.authorized and self.parent:
            PyFunceble.LOGGER.info("Started to clean old entry from the database.")
            for subject in self.get_to_clean():
                self.remove(subject)
            PyFunceble.LOGGER.info("Finished to clean old entry from the database.")

    def initiate(self):
        """
        Initiates the databsse.
        """

        if self.authorized:
            self.load()
            self.clean()
            self.save()

    @classmethod
    def datetime(cls):
        """
        Gets the timestamp where we are going to save our current list.

        :return: The timestamp to append with the currently tested element.
        :rtype: int|str
        """

        return datetime.now()

    def add(self, subject, status):
        """
        Adds the given subject into the database.

        :param str subject: The subject we are working with.
        :param str status: The status of the given subject.
        """

        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                current_datetime = self.datetime()

                if self[subject]:
                    self[subject] = {
                        "status": status,
                        "last_retested_at_iso": current_datetime.isoformat(),
                        "last_retested_at_epoch": current_datetime.timestamp(),
                    }
                else:
                    self[subject] = {
                        "status": status,
                        "included_at_iso": current_datetime.isoformat(),
                        "last_retested_at_iso": current_datetime.isoformat(),
                        "included_at_epoch": current_datetime.timestamp(),
                        "last_retested_at_epoch": current_datetime.timestamp(),
                    }

                PyFunceble.LOGGER.info(
                    f"Indexed {repr(subject)} with the status "
                    f"{repr(status)} into {repr(self.filename)} database's."
                )

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

                with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
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
                    except PyFunceble.engine.MySQL.errors:
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
            if PyFunceble.CONFIGURATION.db_type == "json":
                if self[subject]:
                    del self[subject]

                    PyFunceble.LOGGER.info(
                        "Cleaned the data related to " f"{repr(subject)}."
                    )
                    self.save()
            elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                query = (
                    "DELETE FROM {0} "
                    "WHERE file_path = %(file)s "
                    "AND subject = %(subject)s"
                ).format(self.table_name)

                with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
                    cursor.execute(query, {"file": self.filename, "subject": subject})

                    PyFunceble.LOGGER.info(
                        "Cleaned the data related to "
                        f"{repr(subject)} and {repr(self.filename)} from "
                        f"the {repr(self.table_name)} table."
                    )

    def __execute_query(self, query):  # pragma: no cover
        """
        Executes the query to get the list to retest or already tested.
        """

        with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
            cursor.execute(
                query,
                {
                    "file": self.filename,
                    "days": self.days,
                    "days_between_clean": self.days_between_clean,
                },
            )
            fetched = cursor.fetchall()

            if fetched:
                return {x["subject"] for x in fetched}

        return set()

    def get_to_retest(self):
        """
        Returns a set of subject to restest.
        """

        PyFunceble.LOGGER.info(
            "Getting the list of subjects to retest (DATASET WONT BE LOGGED)"
        )

        if (
            self.authorized
            and PyFunceble.CONFIGURATION.days_between_db_retest >= 0
            and self.filename in self.database
        ):
            if PyFunceble.CONFIGURATION.db_type == "json":
                result = set()

                for subject, info in self.database[self.filename].items():
                    if (
                        "last_retested_at_epoch" in info
                        and info["last_retested_at_epoch"]
                    ):
                        if (
                            datetime.now()
                            > datetime.fromtimestamp(info["last_retested_at_epoch"])
                            + self.days
                        ):
                            result.add(subject)
                    else:
                        result.add(subject)

                return result

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                query = (
                    "SELECT * FROM {0} WHERE file_path = %(file)s "
                    "AND CAST(UNIX_TIMESTAMP() AS {1}) "
                    "> (CAST(UNIX_TIMESTAMP(modified) AS {1}) + CAST(%(days)s AS {1}))"
                ).format(self.table_name, PyFunceble.engine.MySQL.get_int_cast_type())

                return self.__execute_query(query)
        return set()

    def get_already_tested(self):
        """
        Returns a set of already tested subjects.
        """

        PyFunceble.LOGGER.info(
            "Getting the list of already tested (DATASET WONT BE LOGGED)"
        )

        if (
            self.authorized
            and PyFunceble.CONFIGURATION.days_between_db_retest >= 0
            and self.filename in self.database
        ):
            if PyFunceble.CONFIGURATION.db_type == "json":
                result = set()

                for subject, info in self.database[self.filename].items():
                    if (
                        "last_retested_at_epoch" in info
                        and info["last_retested_at_epoch"]
                    ):
                        if (
                            datetime.now()
                            < datetime.fromtimestamp(info["last_retested_at_epoch"])
                            + self.days
                        ):
                            result.add(subject)
                    else:
                        result.add(subject)
                return result

            if PyFunceble.CONFIGURATION.db_type in [
                "mariadb",
                "mysql",
            ]:  # pragma: no cover
                query = (
                    "SELECT * FROM {0} WHERE file_path= %(file)s "
                    "AND CAST(UNIX_TIMESTAMP() AS {1}) "
                    "< (CAST(UNIX_TIMESTAMP(modified) AS {1}) + CAST(%(days)s AS {1}))"
                ).format(self.table_name, PyFunceble.engine.MySQL.get_int_cast_type())

                return self.__execute_query(query)
        return set()

    def get_to_clean(self):
        """
        Returns a set of subject to clean from the database.
        """

        PyFunceble.LOGGER.info(
            "Getting the list of subject to clean (DATASET WONT BE LOGGED)"
        )

        if (
            self.authorized
            and PyFunceble.CONFIGURATION.days_between_inactive_db_clean >= 0
            and self.filename in self.database
        ):
            if PyFunceble.CONFIGURATION.db_type == "json":
                result = set()

                for subject, info in self.database[self.filename].items():
                    if "included_at_epoch" in info and info["included_at_epoch"]:
                        if (
                            datetime.now()
                            > datetime.fromtimestamp(info["included_at_epoch"])
                            + self.days_between_clean
                        ):
                            result.add(subject)
                    else:
                        result.add(subject)

                return result

            if PyFunceble.CONFIGURATION.db_type in [
                "mariadb",
                "mysql",
            ]:  # pragma: no cover

                query = (
                    "SELECT * FROM {0} WHERE file_path= %(file)s "
                    "AND CAST(UNIX_TIMESTAMP() AS {1}) "
                    "> (CAST(UNIX_TIMESTAMP(created) AS {1}) + CAST(%(days_between_clean)s AS {1}))"
                ).format(self.table_name, PyFunceble.engine.MySQL.get_int_cast_type())

                return self.__execute_query(query)
        return set()
