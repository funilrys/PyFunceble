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

This submodule will provide the interface to the mysql/mariadb database.

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
from getpass import getpass

import pymysql

import PyFunceble


class MySQL:
    """
    Provide our way to work with our sqlite database.
    """

    environment_variables = {
        "host": "PYFUNCEBLE_DB_HOST",
        "port": "PYFUNCEBLE_DB_PORT",
        "name": "PYFUNCEBLE_DB_NAME",
        "username": "PYFUNCEBLE_DB_USERNAME",
        "password": "PYFUNCEBLE_DB_PASSWORD",
        "charset": "PYFUNCEBLE_DB_CHARSET",
    }

    tables = {
        "auto_continue": "pyfunceble_auto_continue",
        "inactive": "pyfunceble_inactive",
        "mining": "pyfunceble_mining",
        "whois": "pyfunceble_whois",
    }

    errors = pymysql.err.IntegrityError

    def __init__(self):
        self.authorized = self.authorization()

        if self.authorized:
            self.initiated = False
            self.connection = self.get_connection()
            self.initiated = True

            if not self.are_tables_present():
                self.create_tables()

    @classmethod
    def authorization(cls):
        """
        Provide the authorization to operate.
        """

        return PyFunceble.CONFIGURATION["db_type"] == "mysql"

    @classmethod
    def parse_mysql_sql_file(cls):
        """
        Parse our mysql.sql file into something we understand.
        """

        source = (
            PyFunceble.CONFIG_DIRECTORY
            + PyFunceble.OUTPUTS["db_type"]["directory"]
            + PyFunceble.OUTPUTS["db_type"]["files"]["mysql"]
        )

        statements = []
        delimiter = ";"
        statement = ""

        with open(source, "r", encoding="utf-8") as file_stream:
            source_content = file_stream.readlines()

            for line in source_content:
                line = line.strip()

                if not line or line.startswith("--"):
                    continue

                if "delimiter" in line.lower():
                    delimiter = line.split()[-1]
                    continue

                if "--" in line:
                    statement += line.split("--")[0] + " "
                    continue

                if delimiter not in line:
                    statement += line + " "
                    continue

                if statement:
                    statement += line.replace(delimiter, ";") + " "
                    statements.append(statement)
                    statement = ""
                else:
                    statements.append(line)

        return statements

    def get_connection(self):
        """
        Provide the connection to the database.
        """

        if self.authorized:
            if not self.initiated:
                for (
                    description,
                    environment_variable,
                ) in self.environment_variables.items():
                    if environment_variable in PyFunceble.environ:
                        setattr(
                            self,
                            "_{0}".format(description),
                            PyFunceble.environ[environment_variable],
                        )
                    else:
                        message = "[MySQL/MariaDB] Please give us your DB {0}: ".format(
                            description.capitalize()
                        )

                        if description != "password":
                            setattr(self, "_{0}".format(description), input(message))
                        else:
                            setattr(self, "_{0}".format(description), getpass(message))

                self._port = int(self._port)

            return pymysql.connect(
                host=self._host,  # pylint: disable=no-member
                port=self._port,  # pylint: disable=no-member
                user=self._username,  # pylint: disable=no-member
                password=self._password,  # pylint: disable=no-member
                db=self._name,  # pylint: disable=no-member
                charset=self._charset,  # pylint: disable=no-member
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )

        return None

    def are_tables_present(self):
        """
        Check if all our tables are present.
        """

        if self.authorized:
            for _, table_name in self.tables.items():
                with self.connection.cursor() as cursor:
                    query = (
                        "SELECT COUNT(*) "
                        "FROM information_schema.tables "
                        "WHERE table_schema = %(database_name)s "
                        "AND table_name = %(table_name)s "
                    )
                    cursor.execute(
                        query,
                        {
                            "database_name": self._name,  # pylint: disable=no-member
                            "table_name": table_name,
                        },
                    )

                    result = cursor.fetchone()

                    if result["COUNT(*)"] != 1:
                        return False

        return True

    def create_tables(self):
        """
        Create the tables of the database.
        """

        if self.authorized:
            with self.connection.cursor() as cursor:
                for statement in self.parse_mysql_sql_file():
                    cursor.execute(statement)
