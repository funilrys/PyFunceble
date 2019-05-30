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

This submodule will provide the interface to our sqlite db.

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
import sqlite3

import PyFunceble
from PyFunceble.helpers import File


class SQLite:
    """
    Provide our way to work with our sqlite database.
    """

    errors = sqlite3.IntegrityError
    locked_errors = sqlite3.OperationalError

    tables = {
        "auto_continue": "auto_continue",
        "inactive": "inactive",
        "mining": "mining",
        "whois": "whois",
    }

    def __init__(self):
        self.authorized = self.authorization()

        if self.authorized:
            self.connection = self.get_connection()
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()

            if self.is_empty():
                self.create_database()

    @classmethod
    def authorization(cls):
        """
        Provide the authorization to operate.
        """

        return PyFunceble.CONFIGURATION["db_type"] == "sqlite"

    def get_connection(self):
        """
        Provide the connection to the database.
        """

        if self.authorized:
            return sqlite3.connect(
                PyFunceble.CONFIG_DIRECTORY
                + PyFunceble.OUTPUTS["default_files"]["sqlite"]
            )

        return None

    def is_empty(self):
        """
        Check if our database is emtpy.
        """

        if self.authorized:
            output = self.cursor.execute("SELECT name from sqlite_master")
            fetched = output.fetchall()

            if not fetched:
                return True
        return False

    def create_database(self):
        """
        Create the tables of the database.
        """

        if self.authorized:
            self.cursor.executescript(
                File(
                    PyFunceble.CONFIG_DIRECTORY
                    + PyFunceble.OUTPUTS["db_type"]["directory"]
                    + PyFunceble.OUTPUTS["db_type"]["files"]["sqlite"]
                ).read()
            )
