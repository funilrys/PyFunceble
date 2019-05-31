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

This submodule will give us the mining interface and logic.

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
from hashlib import sha256

# pylint: enable=line-too-long
import urllib3.exceptions as urllib3_exceptions

import PyFunceble
from PyFunceble.helpers import Dict, File


class Mining:  # pylint: disable=too-many-instance-attributes
    """
    Manage the minig subsystem.
    """

    database = {}
    is_subject_present_cache = {}
    database_file = None

    authorized = False
    filename = None
    headers = {}

    def __init__(self, filename, sqlite_db=None, mysql_db=None):  # pragma: no cover
        # We get the authorization to operate.
        self.authorized = self.authorization()
        # We save the file we are working with.
        self.filename = filename
        # Se create the current file namespace.
        self.database[self.filename] = {}

        self.sqlite_db = sqlite_db
        self.mysql_db = mysql_db

        self.table_name = self.get_table_name()

        if PyFunceble.CONFIGURATION["user_agent"]:
            # The user-agent is given.

            # We append the user agent to the header we are going to parse with
            # the request.
            self.headers = {"User-Agent": PyFunceble.CONFIGURATION["user_agent"]}

        if self.authorized:
            # We are authorized to operate.

            # We get the file we are going to save our data.
            self.database_file = (
                PyFunceble.CONFIG_DIRECTORY
                + PyFunceble.OUTPUTS["default_files"]["mining"]
            )

            self.load()

    def __getitem__(self, index):
        if PyFunceble.CONFIGURATION["db_type"] == "json":
            if index in self.database[self.filename]:
                return self.database[self.filename][index]
        if PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            query = (
                "SELECT * "
                "FROM {0} "
                "WHERE file_path = :file "
                "AND subject = :subject "
            ).format(self.table_name)

            output = self.sqlite_db.cursor.execute(
                query, {"file": self.filename, "subject": index}
            )
            fetched = output.fetchall()

            if fetched:
                return [x["mined"] for x in fetched]

        if PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
            query = (
                "SELECT * "
                "FROM {0} "
                "WHERE file_path = %(file)s "
                "AND subject = %(subject)s "
            ).format(self.table_name)

            with self.mysql_db.get_connection() as cursor:
                cursor.execute(query, {"file": self.filename, "subject": index})

                fetched = cursor.fetchall()

                if fetched:
                    return [x["mined"] for x in fetched]

        return None

    def __setitem__(self, index, value):  # pylint: disable=too-many-branches
        if PyFunceble.CONFIGURATION["db_type"] == "json":
            actual_value = self[index]

            if actual_value:
                if isinstance(actual_value, dict):
                    if isinstance(value, dict):  # pragma: no cover
                        self.database[self.filename][index].update(value)
                    else:  # pragma: no cover
                        self.database[self.filename][index] = value
                elif isinstance(actual_value, list):
                    if isinstance(value, list):
                        self.database[self.filename][index].extend(value)
                    else:  # pragma: no cover
                        self.database[self.filename][index].append(value)
                else:  # pragma: no cover
                    self.database[self.filename][index] = value
            else:
                if self.filename not in self.database:  # pragma: no cover
                    self.database[self.filename] = {}

                self.database[self.filename][index] = value
        elif PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            query = (
                "INSERT INTO {0} "
                "(file_path, subject, mined) "
                "VALUES (:file, :subject, :mined)"
            ).format(self.table_name)

            for val in value:
                try:
                    # We execute the query.
                    self.sqlite_db.cursor.execute(
                        query, {"file": self.filename, "subject": index, "mined": val}
                    )
                    # And we commit the changes.
                    self.sqlite_db.connection.commit()
                except self.sqlite_db.errors:
                    pass
        elif PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
            query = (
                "INSERT INTO {0} "
                "(file_path, subject, mined, digest) "
                "VALUES (%(file)s, %(subject)s, %(mined)s, %(digest)s)"
            ).format(self.table_name)

            with self.mysql_db.get_connection() as cursor:
                digest = sha256(bytes(self.filename + index + val, "utf-8")).hexdigest()

                for val in value:
                    try:
                        cursor.execute(
                            query,
                            {
                                "file": self.filename,
                                "subject": index,
                                "mined": val,
                                "digest": digest,
                            },
                        )
                    except self.mysql_db.errors:
                        pass

    def __delitem__(self, index):  # pragma: no cover
        if PyFunceble.CONFIGURATION["db_type"] == "json":
            actual_value = self[index]

            if actual_value:
                del self.database[self.filename][index]
        elif PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            query = "DELETE FROM {0} WHERE file_path = :file AND subject = :subject ".format(
                self.table_name
            )

            # We execute the query.
            self.sqlite_db.cursor.execute(
                query, {"file": self.filename, "subject": index}
            )
            # And we commit the changes.
            self.sqlite_db.connection.commit()
        elif PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
            query = "DELETE FROM {0} WHERE file_path = %(file)s AND subject = %(subject)s ".format(
                self.table_name
            )

            with self.mysql_db.get_connection() as cursor:
                cursor.execute(query, {"file": self.filename, "subject": index})

    @classmethod
    def authorization(cls):
        """
        Provide the operation authorization.
        """

        return PyFunceble.CONFIGURATION["mining"]

    @classmethod
    def get_history(cls, url):  # pragma: no cover
        """
        Get the history of the given url.

        :param str url: An URL to call.

        :return: The list of links.
        :rtype: list
        """

        try:
            return PyFunceble.requests.get(
                url,
                timeout=PyFunceble.CONFIGURATION["seconds_before_http_timeout"],
                headers=cls.headers,
            ).history
        except (
            PyFunceble.requests.ConnectionError,
            PyFunceble.requests.exceptions.Timeout,
            PyFunceble.requests.exceptions.InvalidURL,
            PyFunceble.socket.timeout,
            urllib3_exceptions.InvalidHeader,
            UnicodeDecodeError,  # The probability that this happend in production is minimal.
        ):
            return []

    def get_table_name(self):
        """
        Return the name of the table to use.
        """

        if PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            return self.sqlite_db.tables["mining"]
        if PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
            return self.mysql_db.tables["mining"]
        return "mining"

    def list_of_mined(self):
        """
        Provide the list of mined domains so that they can
        be tested.

        :return:
            The list of mined domains.

            The returned format is the following:

                ::

                    [
                        (index_to_delete_after_test, mined),
                        (index_to_delete_after_test, mined),
                        (index_to_delete_after_test, mined)
                    ]
        :rtype: list
        """

        # We initiate a variable which will return the result.
        result = []

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION["db_type"] == "json":

                for subject in self.database[self.filename].keys():
                    # We loop through the available list of status
                    # from the database.

                    for element in self[subject]:
                        # We then loop through the data associatied to
                        # the currently read status.

                        result.append((subject, element))
            elif PyFunceble.CONFIGURATION["db_type"] == "sqlite":
                query = "SELECT * FROM {0} WHERE file_path = :file ".format(
                    self.table_name
                )

                output = self.sqlite_db.cursor.execute(query, {"file": self.filename})
                fetched = output.fetchall()

                if fetched:
                    result = [(x["subject"], x["mined"]) for x in fetched]
            elif PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
                query = "SELECT * FROM {0} WHERE file_path = %(file)s".format(
                    self.table_name
                )

                with self.mysql_db.get_connection() as cursor:
                    cursor.execute(query, {"file": self.filename})

        # We return the result.
        return result

    def load(self):
        """
        Load the content of the database file.
        """

        if self.authorized and PyFunceble.CONFIGURATION["db_type"] == "json":
            # We are authorized to operate.

            if PyFunceble.path.isfile(self.database_file):
                # The database file exists.

                # We update the database with the content of the file.
                self.database.update(Dict().from_json(File(self.database_file).read()))

    def save(self):
        """
        Save the content of the database into the database file.
        """

        if self.authorized and PyFunceble.CONFIGURATION["db_type"] == "json":
            # We are authorized to operate.

            # We save the database into the file.
            Dict(self.database).to_json(self.database_file)

    def mine(self, subject, subject_type):  # pragma: no cover
        """
        Search for domain or URL related to the original URL or domain.
        If some are found, we add them into the database.

        :param str subject: The subject we are working with.

        :param str subject_typ:
            The type of the subject.

            Can me one of the following:

                - :code:`url`

                - :code:`domain`
        """

        if self.authorized and not self[subject]:
            # We are authorized to operate.

            if subject_type == "domain":
                to_get = "http://{0}:80".format(subject)
            elif subject_type == "url":
                to_get = subject
            else:
                raise ValueError("Unknown subject type {0}".format(repr(subject_type)))

            history = self.get_history(to_get)

            for element in history:
                # We loop through the list of requests history.

                # We get the url from the currently read
                # request.
                url = element.url

                # We create a variable which will save the
                # local result.
                local_result = None

                if subject_type == "domain":
                    # We are working with domains.

                    # We validate and get the base of the URL we
                    # are working with.
                    local_result = PyFunceble.Check(url).is_url(return_base=True)
                elif subject_type == "url":
                    # We are working with URLs.

                    # We validate and get the full URL.
                    local_result = PyFunceble.Check(url).is_url(
                        return_base=False, return_formatted=True
                    )

                if local_result:
                    # The subject type is domain.

                    if subject_type == "domain":
                        # We are working with domain.

                        if local_result.endswith(":80"):
                            # The 80 port is present.

                            # We remove it.
                            local_result = local_result[: local_result.find(":80")]
                        elif local_result.endswith(":443"):
                            # The 443 port is present.

                            # We remove it.
                            local_result = local_result[: local_result.find(":443")]

                    if local_result != subject:
                        # The local result is differnt from the
                        # subject we are working with.

                        # We save into the database.
                        self[subject] = [local_result]

            # We save the database.
            self.save()

    def remove(self, subject, history_member):
        """
        Remove the given subject from the database assigned to the
        currently tested file.

        :param str subject: The subject we are working with.
        :param str history_member: The history member to delete.
        """

        while True:
            actual_value = self[subject]

            if isinstance(actual_value, list) and history_member in actual_value:

                if PyFunceble.CONFIGURATION["db_type"] == "json":
                    try:
                        actual_value.remove(history_member)
                    except ValueError:  # pragma: no cover
                        pass
                elif PyFunceble.CONFIGURATION["db_type"] == "sqlite":
                    # We construct the query string.
                    query = (
                        "DELETE FROM {0} "
                        "WHERE file_path = :file AND subject = :subject AND mined = :mined"
                    ).format(self.table_name)

                    # We execute the query.
                    self.sqlite_db.cursor.execute(
                        query,
                        {
                            "file": self.filename,
                            "subject": subject,
                            "mined": history_member,
                        },
                    )
                    # And we commit the changes.
                    self.sqlite_db.connection.commit()
                elif PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]:
                    # We construct the query string.
                    query = (
                        "DELETE FROM {0} "
                        "WHERE file_path = %(file)s AND subject = %(subject)s AND mined = %(mined)s"
                    ).format(self.table_name)

                    with self.mysql_db.get_connection() as cursor:
                        cursor.execute(
                            query,
                            {
                                "file": self.filename,
                                "subject": subject,
                                "mined": history_member,
                            },
                        )
            else:
                break

        if not self[subject]:  # pragma: no cover
            del self[subject]

        self.save()
