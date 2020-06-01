"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the WHOIS database interface.

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

from datetime import datetime

import PyFunceble


class WhoisDB:
    """
    Provides the WHOIS database interface and logic.
    """

    database = {}

    database_file = None
    authorized = False

    def __init__(self, parent_process=False):
        # Get the authorization.
        self.authorized = self.authorization()
        self.database_file = ""

        if PyFunceble.CONFIGURATION.db_type == "json":
            # We set the location of the database file.
            self.database_file = "{0}{1}".format(
                PyFunceble.CONFIG_DIRECTORY, PyFunceble.OUTPUTS.default_files.whois_db
            )

        self.parent = parent_process
        self.table_name = self.get_table_name()

        PyFunceble.LOGGER.debug(f"Table Name: {self.table_name}")
        PyFunceble.LOGGER.debug(f"DB (File): {self.database_file}")

        # We load the configuration.
        self.load()

    def __contains__(self, index):
        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                if index in self.database:
                    PyFunceble.LOGGER.info(f"{index} is present into the database.")
                    return True

                PyFunceble.LOGGER.info(f"{index} is not present into the database.")
                return False

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                query = "SELECT COUNT(*) FROM {0} WHERE subject = %(subject)s".format(
                    self.table_name
                )

                with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
                    cursor.execute(query, {"subject": index})

                    fetched = cursor.fetchone()

                    if fetched["COUNT(*)"] != 0:
                        PyFunceble.LOGGER.info(f"{index} is present into the database.")
                        return True

                    PyFunceble.LOGGER.info(f"{index} is not present into the database.")

        return False  # pragma: no cover

    def __getitem__(self, index):
        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                if index in self.database:
                    return self.database[index]

                return None

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                fetched = None

                if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                    query = "SELECT * FROM {0} WHERE subject = %(subject)s".format(
                        self.table_name
                    )

                    with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
                        cursor.execute(query, {"subject": index})

                        fetched = cursor.fetchone()

                if fetched:
                    return {
                        "epoch": fetched["expiration_date_epoch"],
                        "expiration_date": fetched["expiration_date"],
                        "state": fetched["state"],
                    }

        return None  # pragma: no cover

    def __setitem_json(self, index, value):
        actual_value = self[index]

        if "record" in value:
            del value["record"]

        if isinstance(actual_value, dict):
            if isinstance(value, dict):
                self.database[index].update(value)
            else:  # pragma: no cover
                self.database[index] = value
        elif isinstance(actual_value, list):
            if isinstance(value, list):  # pragma: no cover
                self.database[index].extend(value)
            else:  # pragma: no cover
                self.database[index].append(value)
        else:
            self.database[index] = value

        PyFunceble.LOGGER.info(
            f"Inserted {repr(value)} into the subset of {repr(index)}"
        )

    def __setitem_mysql(self, index, value):
        query = (
            "INSERT INTO {0} "
            "(subject, expiration_date, expiration_date_epoch, state, record, digest) "
            "VALUES  (%(subject)s, %(expiration_date)s, %(epoch)s, %(state)s, %(record)s, %(digest)s)"  # pylint: disable=line-too-long
        ).format(self.table_name)

        digest = PyFunceble.helpers.Hash(algo="sha256").data(
            bytes(
                index + value["expiration_date"] + str(value["epoch"]) + value["state"],
                "utf-8",
            )
        )

        with PyFunceble.engine.MySQL() as connection, connection.cursor() as cursor:
            playload = {
                "subject": index,
                "expiration_date": value["expiration_date"],
                "epoch": value["epoch"],
                "state": value["state"],
                "record": value["record"],
                "digest": digest,
            }
            try:
                cursor.execute(query, playload)
                PyFunceble.LOGGER.info(f"Inserted into the database: \n {playload}")
            except PyFunceble.engine.MySQL.errors:
                pass

    def __setitem__(self, index, value):
        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                self.__setitem_json(index, value)
            elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                self.__setitem_mysql(index, value)

    @classmethod
    def authorization(cls):
        """
        Provides the operation authorization.
        """

        return (
            not PyFunceble.CONFIGURATION.no_whois
            and PyFunceble.CONFIGURATION.whois_database
        )

    @classmethod
    def merge(cls, old):  # pragma: no cover
        """
        Merges the older version of the database into the new version.

        :param dict old: The old version of the database.


        :return: The database in the new format.
        :rtype: dict
        """

        # We initiate a local place to save our results.
        result = {}

        if PyFunceble.CONFIGURATION.db_type == "json":
            for index, data in old.items():
                # We loop through all indexes and data of the database.

                if isinstance(data, dict) and "epoch" in data:
                    # The epoch index is present into the currently
                    # read dataset.

                    # We create the copy of the dataset for our result.
                    result[index] = data

                    continue

                if isinstance(data, dict):
                    # The read data is a dict.

                    # We save the content of of the currently read dataset
                    # into the upstream index.
                    result.update(data)

        # We return the result.
        return result

    @classmethod
    def get_table_name(cls):
        """
        Returns the name of the table to use.
        """

        if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
            return PyFunceble.engine.MySQL.tables["whois"]
        return "whois"

    def load(self):
        """
        Loads the database file into the database.
        """

        if (
            self.authorized
            and PyFunceble.helpers.File(self.database_file).exists()
            and PyFunceble.CONFIGURATION.db_type == "json"
        ):
            # * We are authorized to operate.
            # and
            # * The database file exists.

            # We merge our current database into already initiated one.
            self.database.update(
                self.merge(PyFunceble.helpers.Dict().from_json_file(self.database_file))
            )

            PyFunceble.LOGGER.info(
                "Database content loaded in memory. (DATASET WONT BE LOGGED)"
            )

            # As changes can happen because of the merging, we directly saved
            # the loaded data.
            self.save()

    def save(self):
        """
        Saves the database into the database file.
        """

        if (
            self.authorized
            and self.parent
            and PyFunceble.CONFIGURATION.db_type == "json"
        ):
            # We are authorized to operate.

            # We save the current state of the datbase.
            PyFunceble.helpers.Dict(self.database).to_json_file(self.database_file)

            PyFunceble.LOGGER.info(f"Saved database into {repr(self.database_file)}.")

    def is_time_older(self, subject):
        """
        Checks if the expiration time of the given subject is
        older.

        :param str subject: The subject we are working with.

        .. note::
            Of course, we imply that the subject is in the database.
        """

        data = self[subject]

        return (
            self.authorized
            and data
            and "epoch" in data
            and datetime.fromtimestamp(float(data["epoch"])) < datetime.now()
        )

    def get_expiration_date(self, subject):
        """
        Gets the expiration date of the given subject.

        :param str subject: The subject we are working with.

        :return: The expiration date from the database.
        :rtype: str|None
        """

        if self.authorized and self[subject] and not self.is_time_older(subject):
            # * We are authorized to work.
            # and
            # * The element we are testing is in the database.
            # and
            # * The expiration date is in the future.

            try:
                # We return the expiration date.
                return self[subject]["expiration_date"]
            except KeyError:  # pragma: no cover
                pass

        # We return None, there is no data to work with.
        return None

    def add(self, subject, expiration_date, record=None):
        """
        Adds the given subject and expiration date to the database.

        :param str subject: The subject we are working with.
        :param str expiration_date: The extracted expiration date.
        :param str record: The WHOIS record.
        """

        if self.authorized and expiration_date:
            # * We are authorized to operate.
            # and
            # * The expiration date is not empty nor None.

            # We initiate what we are going to save into the database
            data = {
                "epoch": datetime.strptime(expiration_date, "%d-%b-%Y").timestamp(),
                "expiration_date": expiration_date,
            }

            if record:  # pragma: no cover
                data["record"] = str(record)
            else:
                data["record"] = str(None)

            if data["epoch"] < datetime.now().timestamp():
                # We compare the epoch with the current time.

                # We set the state.
                data["state"] = "past"
            else:
                # We set the state.
                data["state"] = "future"

            # We save everything into the database.
            self[subject] = data

            # We save everything.
            self.save()
