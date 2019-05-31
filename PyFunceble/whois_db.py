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

This submodule will provide the whois database logic and interface.

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
# pylint: disable=line-too-long

from hashlib import sha256

import PyFunceble
from PyFunceble.helpers import Dict, File


class WhoisDB:
    """
    Provide the WHOIS database interface and logic.
    """

    database = {}

    database_file = None
    authorized = False

    def __init__(self, sqlite_db=None, mysql_db=None):
        # Get the authorization.
        self.authorized = self.authorization()

        # We set the location of the database file.
        self.database_file = "{0}{1}".format(
            PyFunceble.CONFIG_DIRECTORY, PyFunceble.OUTPUTS["default_files"]["whois_db"]
        )

        self.sqlite_db = sqlite_db
        self.mysql_db = mysql_db

        self.table_name = self.get_table_name()

        # We load the configuration.
        self.load()

    def __contains__(self, index):
        if PyFunceble.CONFIGURATION["db_type"] == "json":
            if index in self.database:
                return True
            return False

        if PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            query = "SELECT COUNT(*) FROM {0} WHERE subject = :subject".format(
                self.table_name
            )

            output = self.sqlite_db.cursor.execute(query, {"subject": index})
            fetched = output.fetchone()

            return fetched[0] != 0

        if PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
            query = "SELECT COUNT(*) FROM {0} WHERE subject = %(subject)s".format(
                self.table_name
            )

            with self.mysql_db.get_connection() as cursor:
                cursor.execute(query, {"subject": index})

                fetched = cursor.fetchone()

                return fetched["COUNT(*)"] != 0

        return False  # pragma: no cover

    def __getitem__(self, index):
        if PyFunceble.CONFIGURATION["db_type"] == "json":
            if index in self.database:
                return self.database[index]

            return None

        if PyFunceble.CONFIGURATION["db_type"] in ["sqlite", "mariadb", "mysql"]:
            fetched = None

            if PyFunceble.CONFIGURATION["db_type"] == "sqlite":
                query = "SELECT * FROM {0} WHERE subject = :subject".format(
                    self.table_name
                )

                output = self.sqlite_db.cursor.execute(query, {"subject": index})
                fetched = output.fetchone()

            if PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
                query = "SELECT * FROM {0} WHERE subject = %(subject)s".format(
                    self.table_name
                )

                with self.mysql_db.get_connection() as cursor:
                    cursor.execute(query, {"subject": index})

                    fetched = cursor.fetchone()

            if fetched:
                return {
                    "epoch": fetched["expiration_date_epoch"],
                    "expiration_date": fetched["expiration_date"],
                    "state": fetched["state"],
                }

        return None  # pragma: no cover

    def __setitem__(self, index, value):
        if PyFunceble.CONFIGURATION["db_type"] == "json":
            actual_value = self[index]

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
        elif PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            query = (
                "INSERT INTO {0} "
                "(subject, expiration_date, expiration_date_epoch, state) "
                "VALUES (:subject, :expiration_date, :epoch, :state)"
            ).format(self.table_name)

            try:
                # We execute the query.
                self.sqlite_db.cursor.execute(
                    query,
                    {
                        "subject": index,
                        "expiration_date": value["expiration_date"],
                        "epoch": value["epoch"],
                        "state": value["state"],
                    },
                )
                # And we commit the changes.
                self.sqlite_db.connection.commit()
            except self.sqlite_db.errors:
                pass
        elif PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
            query = (
                "INSERT INTO {0} "
                "(subject, expiration_date, expiration_date_epoch, state, digest) "
                "VALUES  (%(subject)s, %(expiration_date)s, %(epoch)s, %(state)s, %(digest)s)"
            ).format(self.table_name)

            digest = sha256(
                bytes(
                    index
                    + value["expiration_date"]
                    + str(value["epoch"])
                    + value["state"],
                    "utf-8",
                )
            ).hexdigest()

            with self.mysql_db.get_connection() as cursor:
                try:
                    cursor.execute(
                        query,
                        {
                            "subject": index,
                            "expiration_date": value["expiration_date"],
                            "epoch": value["epoch"],
                            "state": value["state"],
                            "digest": digest,
                        },
                    )
                except self.mysql_db.errors:
                    pass

    @classmethod
    def authorization(cls):
        """
        Provide the operation authorization.
        """

        return (
            not PyFunceble.CONFIGURATION["no_whois"]
            and PyFunceble.CONFIGURATION["whois_database"]
        )

    @classmethod
    def merge(cls, old):  # pragma: no cover
        """
        Merge the older version of the database into the new version.

        :param dict old: The old version of the database.


        :return: The database in the new format.
        :rtype: dict
        """

        # We initiate a local place to save our results.
        result = {}

        if PyFunceble.CONFIGURATION["db_type"] == "json":
            for index, data in old.items():
                # We loop through all indexes and data of the database.

                if isinstance(data, dict) and "epoch" in data:
                    # The epoch index is present into the currently
                    # read dataset.

                    # We create the copy of the dataset for our result.
                    result[index] = data

                    continue
                elif isinstance(data, dict):
                    # The read data is a dict.

                    # We save the content of of the currently read dataset
                    # into the upstream index.
                    result.update(data)

        # We return the result.
        return result

    def get_table_name(self):
        """
        Return the name of the table to use.
        """

        if PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            return self.sqlite_db.tables["whois"]
        if PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
            return self.mysql_db.tables["whois"]
        return "whois"

    def load(self):
        """
        Load the database file into the database.
        """

        if (
            self.authorized
            and PyFunceble.path.isfile(self.database_file)
            and PyFunceble.CONFIGURATION["db_type"] == "json"
        ):
            # * We are authorized to operate.
            # and
            # * The database file exists.

            # We merge our current database into already initiated one.
            self.database.update(
                self.merge(Dict().from_json(File(self.database_file).read()))
            )

            # As changes can happen because of the merging, we directly saved
            # the loaded data.
            self.save()

    def save(self):
        """
        Save the database into the database file.
        """

        if self.authorized and PyFunceble.CONFIGURATION["db_type"] == "json":
            # We are authorized to operate.

            # We save the current state of the datbase.
            Dict(self.database).to_json(self.database_file)

    def is_time_older(self, subject):
        """
        Check if the expiration time of the given subject is
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
            and int(data["epoch"]) < int(PyFunceble.time())
        )

    def get_expiration_date(self, subject):
        """
        Get the expiration date of the given subject.

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

    def add(self, subject, expiration_date):
        """
        Add the given subject and expiration date to the database.

        :param str subject: The subject we are working with.
        :param str expiration_date: The extracted expiration date.
        """

        if self.authorized and expiration_date:
            # * We are authorized to operate.
            # and
            # * The expiration date is not empty nor None.

            # We initiate what we are going to save into the database
            data = {
                "epoch": int(
                    PyFunceble.mktime(PyFunceble.strptime(expiration_date, "%d-%b-%Y"))
                ),
                "expiration_date": expiration_date,
            }

            if data["epoch"] < int(PyFunceble.time()):
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
