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
from PyFunceble.helpers import File, Regex


class MySQL:
    """
    Provide our way to work with our sqlite database.
    """

    variables = {
        "host": {"env": "PYFUNCEBLE_DB_HOST", "default": "localhost"},
        "port": {"env": "PYFUNCEBLE_DB_PORT", "default": 3306},
        "name": {"env": "PYFUNCEBLE_DB_NAME", "default": "pyfunceble"},
        "username": {"env": "PYFUNCEBLE_DB_USERNAME", "default": "pyfunceble"},
        "password": {"env": "PYFUNCEBLE_DB_PASSWORD", "default": "PyFunceble:15_93le"},
        "charset": {"env": "PYFUNCEBLE_DB_CHARSET", "default": "utf8mb4"},
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

        pyfunceble_env_location = PyFunceble.CONFIG_DIRECTORY + PyFunceble.ENV_FILENAME
        self.env_content = self.parse_env_file(pyfunceble_env_location)

        if self.authorized:
            self.initiated = False
            self.connection = self.get_connection()

            self.save_to_env_file(self.env_content, pyfunceble_env_location)

            self.initiated = True

            if not self.are_tables_present():
                self.create_tables()

    @classmethod
    def authorization(cls):
        """
        Provide the authorization to operate.
        """

        return PyFunceble.CONFIGURATION["db_type"] in ["mariadb", "mysql"]

    @classmethod
    def parse_mysql_sql_file(cls):
        """
        Parse our mysql.sql file into something we understand.
        """

        source = (
            PyFunceble.CONFIG_DIRECTORY + PyFunceble.OUTPUTS["db_type"]["directory"]
        )

        if PyFunceble.CONFIGURATION["db_type"] == "mariadb":
            source += PyFunceble.OUTPUTS["db_type"]["files"]["mariadb"]
        elif PyFunceble.CONFIGURATION["db_type"] == "mysql":
            source += PyFunceble.OUTPUTS["db_type"]["files"]["mysql"]

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

    @classmethod
    def parse_env_file(cls, env_file_location):
        """
        Parse the environment file into something we understand.

        :param str env_file_location: The location of the file we have to parse.
        """

        result = {}
        content = ""

        if PyFunceble.path.isfile(env_file_location):
            content = File(env_file_location).read()

            for line in content.splitlines():
                line = line.strip()

                if line.startswith("#"):
                    continue

                if "#" in line:
                    line = line[: line.find("#")]

                if "=" in line:
                    splited = line.split("=")
                    result[splited[0]] = splited[1]

        return result

    @classmethod
    def save_to_env_file(cls, envs, env_file_location):
        """
        Save the given dict of environment variable into our environment file.

        :param dict envs: A dict of environment variables to save.
        :param str env_file_location: The location of the file we have to update.
        """

        file_instance = File(env_file_location)

        try:
            content = file_instance.read()
        except FileNotFoundError:
            content = ""

        if content:
            for environment_variable, value in envs.items():
                to_write = "{0}={1}".format(environment_variable, value)

                regex = r"{0}=.*".format(environment_variable)

                if Regex(content, regex, return_data=False).match():
                    content = Regex(content, regex, replace_with=to_write).replace()
                else:
                    if not content.endswith("\n"):
                        content += "\n{0}\n".format(to_write)
                    else:
                        content += "{0}\n".format(to_write)
        else:
            for environment_variable, value in envs.items():
                to_write = "{0}={1}".format(environment_variable, value)
                content += "{0}\n".format(to_write)

        file_instance.write(content, overwrite=True)

    def get_connection(self):
        """
        Provide the connection to the database.
        """

        if self.authorized:
            if not self.initiated:
                for (description, data) in self.variables.items():
                    if data["env"] in PyFunceble.environ:
                        setattr(
                            self,
                            "_{0}".format(description),
                            PyFunceble.environ[data["env"]],
                        )
                    else:
                        message = "[MySQL/MariaDB] Please give us your DB {0} ({1}): ".format(
                            description.capitalize(), repr(data["default"])
                        )

                        if description != "password":
                            user_input = input(message)
                        else:
                            user_input = getpass(message)

                        if user_input:
                            setattr(self, "_{0}".format(description), user_input)
                            self.env_content[data["env"]] = user_input
                        else:
                            setattr(self, "_{0}".format(description), data["default"])
                            self.env_content[data["env"]] = data["default"]

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
