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

This submodule will provide the inactive database logic and interface.

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

import PyFunceble
from PyFunceble.helpers import Dict, File, List


class InactiveDB:  # pylint: disable=too-many-instance-attributes
    """
    Provide the inactive database logic and interface.

    :param str filename: The name of the file we are processing.
    """

    # We initiate a variable which will save the
    # cache about who are present or not into the database.
    is_present_cache = {}

    # Saves the whole database content.
    database = {}

    # Save the operation authorization.
    authorized = False

    one_day_in_seconds = 1 * 24 * 3600

    # Save the filename we are operating.
    filename = None

    def __init__(self, filename, sqlite_db=None, mysql_db=None):
        # We get the authorization status.
        self.authorized = self.authorization()

        # We convert the number of days between the database retest
        # to seconds.
        self.days_in_seconds = (
            PyFunceble.CONFIGURATION["days_between_db_retest"] * 24 * 3600
        )

        # We set the path to the inactive database file.
        self.database_file = "{0}{1}".format(
            PyFunceble.CONFIG_DIRECTORY,
            PyFunceble.OUTPUTS["default_files"]["inactive_db"],
        )

        # We share the filename.
        self.filename = filename

        # We get the db instance.
        self.sqlite_db = sqlite_db
        self.mysql_db = mysql_db

        self.table_name = self.get_table_name()

        # We initiate the database.
        self.initiate()

    def __contains__(self, subject):
        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION["db_type"] == "json":
                if subject not in self.is_present_cache:
                    for element in [
                        x for x in self.database[self.filename].keys() if x.isdigit()
                    ]:
                        if subject in self[element]:
                            self.is_present_cache[subject] = True
                            break
                        else:  # pragma: no cover
                            self.is_present_cache[subject] = False
                            continue

                    if subject not in self.is_present_cache:
                        self.is_present_cache[subject] = False

                return self.is_present_cache[subject]

            if PyFunceble.CONFIGURATION["db_type"] == "sqlite":
                query = (
                    "SELECT COUNT(*) "
                    "FROM {0} "
                    "WHERE subject = :subject AND file_path = :file"
                ).format(self.table_name)

                try:
                    output = self.sqlite_db.cursor.execute(
                        query, {"subject": subject, "file": self.filename}
                    )
                except self.sqlite_db.locked_errors:
                    PyFunceble.sleep(0.3)
                    output = self.sqlite_db.cursor.execute(
                        query, {"subject": subject, "file": self.filename}
                    )
                fetched = output.fetchone()

                return fetched[0] != 0

            if PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
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
        if self.authorized and PyFunceble.CONFIGURATION["db_type"] == "json":
            if self.filename in self.database and index in self.database[self.filename]:
                return self.database[self.filename][index]
        return []

    def __setitem__(self, index, value):
        if PyFunceble.CONFIGURATION["db_type"] == "json":
            actual_state = self[index]

            if actual_state:
                if isinstance(actual_state, dict):
                    if isinstance(value, dict):  # pragma: no cover
                        self.database[self.filename][index].update(value)
                    else:  # pragma: no cover
                        self.database[self.filename][index] = value
                elif isinstance(actual_state, list):
                    if isinstance(value, list):
                        self.database[self.filename][index].extend(value)
                    else:  # pragma: no cover
                        self.database[self.filename][index].append(value)
                else:  # pragma: no cover
                    self.database[self.filename][index] = value
            else:
                if self.filename not in self.database:
                    self.database[self.filename] = {index: value}
                self.database[self.filename][index] = value

            self.database[self.filename][index] = List(
                self.database[self.filename][index]
            ).format()

    @classmethod
    def authorization(cls):
        """
        Provide the execution authorization.
        """

        return PyFunceble.CONFIGURATION["inactive_database"]

    def get_table_name(self):
        """
        Return the name of the table to use.
        """

        if PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            return self.sqlite_db.tables["inactive"]
        if PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
            return self.mysql_db.tables["inactive"]
        return "inactive"

    def _merge(self):
        """
        Merge the database with the older one which
        has already been set into the database.
        """

        if self.authorized and PyFunceble.CONFIGURATION["db_type"] == "json":
            # We are authorized to operate.

            # We get the content of the database.
            database_content = Dict().from_json(File(self.database_file).read())

            # We get the database top keys.
            database_top_keys = database_content.keys()

            for database_top_key in database_top_keys:
                # We loop through the list of database top keys.

                if database_top_key not in self.database:
                    # The currently read top key is not already into the database.

                    # We initiate the currently read key with the same key from
                    # our database file.
                    self.database[database_top_key] = database_content[database_top_key]
                else:
                    # The currently read top key is already into the database.

                    # We get the list of lower indexes.
                    database_low_keys = database_content[database_top_key].keys()

                    for database_low_key in database_low_keys:
                        # We loop through the lower keys.

                        if (
                            database_low_key not in self.database[database_top_key]
                        ):  # pragma: no cover
                            # The lower key is not already into the database.

                            # We initiate the currently read low and top key with the
                            # same combinaison from our database file.
                            self.database[database_top_key][
                                database_low_key
                            ] = database_content[database_top_key][database_low_key]
                        else:
                            # The lower key is not already into the database.

                            # We exted the currently read low and top key combinaison
                            # with the same combinaison from our database file.
                            self.database[database_top_key][database_low_key].extend(
                                database_content[database_top_key][database_low_key]
                            )

                            # And we format the list of element to ensure that there is no
                            # duplicate into the database content.
                            self.database[database_top_key][database_low_key] = List(
                                self.database[database_top_key][database_low_key]
                            ).format()

    def load(self):
        """
        Load the content of the database file.
        """

        if self.authorized and PyFunceble.CONFIGURATION["db_type"] == "json":
            # We are authorized to operate.

            if PyFunceble.path.isfile(self.database_file):
                # The database file exists.

                self._merge()
            else:
                # The database file do not exists.

                # We initiate an empty database.
                self.database = {self.filename: {"to_test": []}}

    def save(self):
        """
        Save the current database into the database file.
        """

        if self.authorized and PyFunceble.CONFIGURATION["db_type"] == "json":
            # We are authorized to operate.

            # We save the current database state into the database file.
            Dict(self.database).to_json(self.database_file)

    def _add_to_test(self, to_add):
        """
        Add an element or a list of element into the list of element
        to test on the next session.

        :param to_add: The domain, IP or URL to add.
        :type to_add: str|list
        """

        if self.authorized and PyFunceble.CONFIGURATION["db_type"] == "json":
            # We are authorized to operate.

            if not isinstance(to_add, list):
                # The element to add is not a list.

                # We set it into a list.
                to_add = [to_add]

            # We set the list to test
            self["to_test"] = to_add

            # We format the list to test in order to avoid duplicate.
            self.database[self.filename]["to_test"] = List(self["to_test"]).format()

            # And we finally save the database.
            self.save()

    def initiate(self):
        """
        Initiate the databse.
        """

        if self.authorized:
            # * We are authorized to operate.
            # and
            # * The filename is already in the database.

            # We initiate a variable which is going to save what we are going
            # to return.
            result = []

            # We initiate a variable which is going to save the key to remove
            # once they are merged into the `to_test` index.
            to_delete = []

            # We load the database.
            self.load()

            if PyFunceble.CONFIGURATION["db_type"] == "json":
                if self.filename in self.database:
                    for data in [
                        x for x in self.database[self.filename] if x.isdigit()
                    ]:
                        # We loop through the database content related to the file we
                        # are testing.

                        if int(PyFunceble.time()) > int(data) + self.days_in_seconds:
                            # The currently read index is older than the excepted time
                            # for retesting.

                            # We extend our result variable with the content from the
                            # currently read index.
                            result.extend(self.database[self.filename][data])

                            # And we append the currently read index into the list of
                            # index to delete.
                            to_delete.append(data)

                    # We remove all indexes which are present into the list of index to delete.
                    Dict(self.database[self.filename]).remove_key(to_delete)

                    # And we append our list of element to retest into the `to_test` index.s
                    self._add_to_test(result)

                    # And we finally save the database.
                    self.save()
                else:  # pragma: no cover
                    # We create the current file namepace
                    self.database[self.filename] = {"to_test": []}

    def _timestamp(self):
        """
        Get the timestamp where we are going to save our current list.

        :return: The timestamp to append with the currently tested element.
        :rtype: int|str
        """

        if (
            PyFunceble.CONFIGURATION["db_type"] == "json"
            and self.authorized
            and self.filename in self.database
        ):
            # * We are authorized to operate.
            # and
            # * The currently tested file is already in the database.

            if self.database[self.filename]:
                # The file we are testing is into the database and its content
                # is not empty.

                # We get the indexes of the current file (in the dabase).
                database_keys = [
                    x for x in self.database[self.filename].keys() if x.isdigit()
                ]

                if database_keys:
                    # The list of keys is not empty.

                    # We get the most recent date.
                    recent_date = max(database_keys)
                else:  # pragma: no cover
                    # The list of keys is empty.

                    # We return the current time.
                    return int(PyFunceble.time())

                if int(PyFunceble.time()) > int(recent_date) + self.one_day_in_seconds:
                    # The most recent time was in more than one day.

                    # We return the current time.
                    return int(PyFunceble.time())

                # The most recent time was in less than one day.

                if int(PyFunceble.time()) < int(recent_date) + self.days_in_seconds:
                    # The most recent time was in less than the expected number of day for
                    # retesting.

                    # We return the most recent data.
                    return int(recent_date)

        # The database subsystem is not activated.

        # We return the current time.
        return int(PyFunceble.time())

    def add(self, subject):
        """
        Add the given subject into the database.

        :param str subject: The subject we are working with.
        """

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION["db_type"] == "json":
                # We get the timestamp to use as index.
                timestamp = str(self._timestamp())

                if self.filename in self.database:
                    # * The file path is not into the database.

                    # We append the index and the database element into the databse
                    # related to the file we are testing.
                    self[timestamp] = [subject]

                    if self["to_test"] and subject in self["to_test"]:
                        # * The `to_test` index is into the database related to the file we
                        #   are testing.
                        # and
                        # * The element we are testing is into the `to_test` index related to
                        #   the file we are testing.

                        # We remove the element from the list of element to test.
                        self["to_test"].remove(subject)
                else:
                    # The file path is not into the database.

                    # We initiate the file path and its content into the database.
                    self[timestamp] = [subject]
                # And we save the database.
                self.save()
            elif PyFunceble.CONFIGURATION["db_type"] == "sqlite":
                query = (
                    "INSERT INTO {0} "
                    "(file_path, subject) "
                    "VALUES (:file, :subject)"
                ).format(self.table_name)

                try:
                    # We execute the query.
                    self.sqlite_db.cursor.execute(
                        query, {"file": self.filename, "subject": subject}
                    )
                except self.sqlite_db.errors:
                    query = (
                        "UPDATE {0} "
                        "SET subject = :subject "
                        "WHERE file_path = :file AND subject = :subject"
                    ).format(self.table_name)

                    # We execute the query.
                    self.sqlite_db.cursor.execute(
                        query, {"subject": subject, "file": self.filename}
                    )

                # And we commit the changes.
                self.sqlite_db.connection.commit()
            elif PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
                digest = sha256(bytes(self.filename + subject, "utf-8")).hexdigest()

                query = (
                    "INSERT INTO {0} "
                    "(file_path, subject, digest) "
                    "VALUES (%(file)s, %(subject)s, %(digest)s)"
                ).format(self.table_name)

                with self.mysql_db.get_connection() as cursor:

                    try:
                        cursor.execute(
                            query,
                            {
                                "file": self.filename,
                                "subject": subject,
                                "digest": digest,
                            },
                        )
                    except self.mysql_db.errors:
                        query = (
                            "UPDATE {0} "
                            "SET subject = %(subject)s "
                            "WHERE file_path = %(file)s "
                            "AND %(subject)s = %(subject)s "
                            "AND digest = %(digest)s"
                        ).format(self.table_name)

                        cursor.execute(
                            query,
                            {
                                "subject": subject,
                                "file": self.filename,
                                "digest": digest,
                            },
                        )

    def remove(self, subject):
        """
        Remove all occurence of the given subject from the database.

        :param str subject: The subject we are working with.
        """

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION["db_type"] == "json":
                for data in self.database[self.filename]:
                    # We loop through the index of the file database.

                    if subject in self[data]:
                        # The currently tested element into the currently read index.

                        # We remove the currently tested element from the read index.
                        self[data].remove(subject)

                # And we save the data into the database.
                self.save()
            elif PyFunceble.CONFIGURATION["db_type"] == "sqlite":
                # We construct the query we are going to execute.
                query = (
                    "DELETE FROM {0} "
                    "WHERE file_path = :file "
                    "AND subject = :subject"
                ).format(self.table_name)

                # We execute it.
                self.sqlite_db.cursor.execute(
                    query, {"file": self.filename, "subject": subject}
                )
                # We commit everything.
                self.sqlite_db.connection.commit()
            elif PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
                # We construct the query we are going to execute.
                query = (
                    "DELETE FROM {0} "
                    "WHERE file_path = %(file)s "
                    "AND subject = %(subject)s"
                ).format(self.table_name)

                with self.mysql_db.get_connection() as cursor:
                    cursor.execute(query, {"file": self.filename, "subject": subject})

    def get_to_retest(self):  # pylint: pragma: no cover
        """
        Return a set of subject to restest.
        """

        if PyFunceble.CONFIGURATION["db_type"] == "json":
            try:
                return [
                    z
                    for x, y in self.database[self.filename].items()
                    if x.isdigit()
                    and int(PyFunceble.time()) > int(x) + self.days_in_seconds
                    for z in y
                ]
            except KeyError:
                return []

        if PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            query = (
                "SELECT * FROM {0} WHERE file_path = :file "
                "AND CAST(strftime('%s', 'now') AS INTEGER) "
                "> (CAST(strftime('%s', modified) AS INTEGER) + CAST(:days AS INTEGER))"
            ).format(self.table_name)

            output = self.sqlite_db.cursor.execute(
                query, {"file": self.filename, "days": self.days_in_seconds}
            )
            fetched = output.fetchall()

            if fetched:
                return [x["subject"] for x in fetched]

        if PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
            if PyFunceble.CONFIGURATION["db_type"] == "mariadb":
                cast_type = "INTEGER"
            else:
                cast_type = "UNSIGNED"

            query = (
                "SELECT * FROM {0} WHERE file_path = %(file)s "
                "AND CAST(UNIX_TIMESTAMP() AS {1}) "
                "> (CAST(UNIX_TIMESTAMP(modified) AS {1}) + CAST(%(days)s AS {1}))"
            ).format(self.table_name, cast_type)

            with self.mysql_db.get_connection() as cursor:
                cursor.execute(
                    query, {"file": self.filename, "days": self.days_in_seconds}
                )
                fetched = cursor.fetchall()

                if fetched:
                    return [x["subject"] for x in fetched]

        return []

    def get_already_tested(self):  # pragma: no cover
        """
        Return a set of already tested subjects.
        """

        if PyFunceble.CONFIGURATION["db_type"] == "json":
            try:
                return {
                    z
                    for x, y in self.database[self.filename].items()
                    if x.isdigit()
                    and int(PyFunceble.time()) < int(x) + self.days_in_seconds
                    for z in y
                }
            except KeyError:
                return set()

        if PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            query = (
                "SELECT * FROM {0} WHERE file_path = :file "
                "AND CAST(strftime('%s', 'now') AS INTEGER) "
                "< (CAST(strftime('%s', modified) AS INTEGER) + CAST(:days AS INTEGER))"
            ).format(self.table_name)

            output = self.sqlite_db.cursor.execute(
                query, {"file": self.filename, "days": self.days_in_seconds}
            )
            fetched = output.fetchall()

            if fetched:
                return {x["subject"] for x in fetched}

        if PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
            if PyFunceble.CONFIGURATION["db_type"] == "mariadb":
                cast_type = "INTEGER"
            else:
                cast_type = "UNSIGNED"

            query = (
                "SELECT * FROM {0} WHERE file_path= %(file)s "
                "AND CAST(UNIX_TIMESTAMP() AS {1}) "
                "< (CAST(UNIX_TIMESTAMP(modified) AS {1}) + CAST(%(days)s AS {1}))"
            ).format(self.table_name, cast_type)

            with self.mysql_db.get_connection() as cursor:
                cursor.execute(
                    query, {"file": self.filename, "days": self.days_in_seconds}
                )
                fetched = cursor.fetchall()

                if fetched:
                    return {x["subject"] for x in fetched}
        return set()
