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

This submodule will provide the auto-continue logic.

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

import PyFunceble
from PyFunceble.helpers import Dict, File


class AutoContinue:
    """
    Provide the auto-continue subsystem.
    """

    # Save the content of the database.
    database = {}
    # Save the database file
    database_file = None
    # Save the operation authorization.
    authorized = False

    # Save the filename we are working with.
    filename = None

    def __init__(self, filename, parent_process=False, sqlite_db=None):
        # We get the operation authorization.
        self.authorized = self.authorization()
        # We share the filename.
        self.filename = filename
        # We preset the filename namespace.
        self.database[self.filename] = {}
        # We preset the sqlite connetion.
        self.sqlite_db = sqlite_db

        # We share if we are under the parent process.
        self.parent = parent_process

        if self.authorized:
            # We are authorized to operate.

            # We set the location of the database file.
            self.database_file = (
                PyFunceble.OUTPUT_DIRECTORY
                + PyFunceble.OUTPUTS["parent_directory"]
                + PyFunceble.OUTPUTS["logs"]["filenames"]["auto_continue"]
            )

            # We load the backup (if existant).
            self.load()

            if self.parent and (
                self.filename not in self.database or not self.database[self.filename]
            ):
                # The database of the file we are
                # currently testing is empty.

                # We clean the output directory.
                PyFunceble.Clean(None)
        elif self.parent:
            # We are not authorized to operate.

            # We clean the output directory.
            PyFunceble.Clean(None)

    def __contains__(self, index):  # pragma: no cover
        if self.authorized:
            if PyFunceble.CONFIGURATION["db_type"] == "json":
                if self.filename in self.database:
                    for _, status_data in self.database[self.filename].items():
                        if index in status_data:
                            return True
                return False

            if PyFunceble.CONFIGURATION["db_type"] == "sqlite":
                query = (
                    "SELECT COUNT(*) "
                    "FROM auto_continue "
                    "WHERE subject = :subject AND file_path = :file"
                )
                output = self.sqlite_db.cursor.execute(
                    query, {"subject": index, "file": self.filename}
                )
                fetched = output.fetchone()

                return fetched[0] != 0
        return False

    @classmethod
    def authorization(cls):
        """
        Provide the execution authorization.
        """

        return (
            PyFunceble.CONFIGURATION["auto_continue"]
            and not PyFunceble.CONFIGURATION["no_files"]
        )

    def is_empty(self):
        """
        Check if the database related to the currently tested
        file is emtpy.
        """

        if PyFunceble.CONFIGURATION["db_type"] == "json":
            if self.filename not in self.database or not self.database[self.filename]:
                return True
            return False

        if PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            query = "SELECT COUNT(*) from auto_continue where file_path = :file"
            output = self.sqlite_db.cursor.execute(query, {"file": self.filename})
            fetched = output.fetchone()

            return fetched[0] == 0
        return False  # pragma: no cover

    def add(self, subject, status):
        """
        Add the given subject into the database.
        """

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION["db_type"] == "json":
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

                # We save everything.
                self.save()
            elif PyFunceble.CONFIGURATION["db_type"] == "sqlite":
                # We construct the query string.
                query = (
                    "INSERT INTO auto_continue "
                    "(file_path, subject, status) "
                    "VALUES (:file, :subject, :status)"
                )
                try:
                    try:
                        # We execute the query.
                        self.sqlite_db.cursor.execute(
                            query,
                            {
                                "subject": subject,
                                "status": status,
                                "file": self.filename,
                            },
                        )
                    except self.sqlite_db.locked_errors:
                        PyFunceble.sleep(0.3)
                        # We execute the query.
                        self.sqlite_db.cursor.execute(
                            query,
                            {
                                "subject": subject,
                                "status": status,
                                "file": self.filename,
                            },
                        )
                except self.sqlite_db.errors:
                    query = (
                        "UPDATE auto_continue "
                        "SET status = :status "
                        "WHERE file_path = :file AND subject = :subject"
                    )

                    # We execute the query.
                    self.sqlite_db.cursor.execute(
                        query,
                        {"subject": subject, "status": status, "file": self.filename},
                    )
                # And we commit the changes.
                self.sqlite_db.connection.commit()

    def save(self):
        """
        Save the current state of the database.
        """

        if self.authorized and PyFunceble.CONFIGURATION["db_type"] == "json":
            # We are authoried to operate.

            # We save the current database state.
            Dict(self.database).to_json(self.database_file)

    def load(self):
        """
        Load previously saved database.
        """

        if self.authorized and PyFunceble.CONFIGURATION["db_type"] == "json":
            # We are authorized to operate.

            if PyFunceble.path.isfile(self.database_file):
                # The database file exists.

                # We get its content and save it inside backup_content.
                self.database = Dict().from_json(File(self.database_file).read())
            else:
                # The database file do not exists.

                # We initiate an empty database.
                self.database = {self.filename: {}}

    def clean(self):
        """
        Clean the database.
        """

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION["db_type"] == "json":
                # We empty the database.
                self.database[self.filename] = {}

                # And we save the current database state.
                Dict(self.database).to_json(self.database_file)
            elif PyFunceble.CONFIGURATION["db_type"] == "sqlite":
                # We construct the query we are going to execute.
                query = "DELETE FROM auto_continue WHERE file_path=:file"
                # We execute it.
                self.sqlite_db.cursor.execute(query, {"file": self.filename})
                # We commit everything.
                self.sqlite_db.connection.commit()

    def update_counters(self):  # pragma: no cover
        """
        Update the counters.
        """

        if self.authorized and self.parent:
            # We are authorized to operate.

            # We create a list of all status we are working with.
            statuses = ["up", "down", "invalid"]
            # We preset the number of tested.
            tested = 0

            for status in statuses:
                # We loop through the list of status.

                if PyFunceble.CONFIGURATION["db_type"] == "json":
                    try:
                        # We get the number of tested of the currently read
                        # status.
                        tested_for_status = len(
                            self.database[self.filename][
                                PyFunceble.STATUS["official"][status]
                            ]
                        )

                        # We then update/transfert it to its global place.
                        PyFunceble.INTERN["counter"]["number"][
                            status
                        ] = tested_for_status

                        # We finally increate the number of tested.
                        tested += tested_for_status
                    except KeyError:
                        PyFunceble.INTERN["counter"]["number"][status] = 0
                        continue
                elif PyFunceble.CONFIGURATION["db_type"] == "sqlite":
                    query = (
                        "SELECT COUNT(*) "
                        "FROM auto_continue "
                        "WHERE status=:status and file_path=:file "
                        "AND subject "
                        "NOT IN ("
                        "SELECT subject "
                        "FROM inactive "
                        "WHERE created != modified "
                        "AND file_path = :file "
                        ")"
                    )

                    output = self.sqlite_db.cursor.execute(
                        query,
                        {
                            "file": self.filename,
                            "status": PyFunceble.STATUS["official"][status],
                        },
                    )
                    fetched = output.fetchone()

                    PyFunceble.INTERN["counter"]["number"][status] = fetched[0]

                    # We then update/transfert it to its global place.
                    tested += fetched[0]

            # We update/transfert the number of tested globally.
            PyFunceble.INTERN["counter"]["number"]["tested"] = tested

    def get_already_tested(self):
        """
        Return the list of subjects which were already tested as a set.
        """

        if PyFunceble.CONFIGURATION["db_type"] == "json":
            try:
                return {y for _, x in self.database[self.filename].items() for y in x}
            except KeyError:  # pragma: no cover
                pass
        elif PyFunceble.CONFIGURATION["db_type"] == "sqlite":
            query = "SELECT * FROM auto_continue WHERE file_path=:file"

            output = self.sqlite_db.cursor.execute(query, {"file": self.filename})
            fetched = output.fetchall()

            if fetched:
                return {x["subject"] for x in fetched}
        return set()  # pragma: no cover
