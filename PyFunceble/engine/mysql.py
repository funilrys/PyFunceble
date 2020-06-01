"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the MariaDB/MySQL communication engine.

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


import warnings
from getpass import getpass
from os import sep as directory_separator

import pymysql

import PyFunceble


class MySQL:
    """
    Provides our way to work with our mysql/mariadb database.
    """

    # pylint: disable=no-member,too-many-instance-attributes

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
        "tested": "pyfunceble_tested",
    }

    errors = pymysql.err.IntegrityError
    connection = None

    def __init__(self):
        warnings.simplefilter("ignore")

        self.authorized = self.authorization()

        if self.authorized:
            self.pyfunceble_env_location = (
                PyFunceble.CONFIG_DIRECTORY
                + PyFunceble.abstracts.Infrastructure.ENV_FILENAME
            )
            self.env_content = self.parse_env_file(self.pyfunceble_env_location)

            self.pre_initiated = False
            self.post_initiated = False
            self.db_tables_initiated = False

    def __enter__(self):
        self.init_pre_connection()

        if directory_separator not in self._host or "/" not in self._host:
            self.connection = pymysql.connect(
                host=self._host,
                port=self._port,
                user=self._username,
                password=self._password,
                db=self._name,
                charset=self._charset,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
        else:
            self.connection = pymysql.connect(
                unix_socket=self._host,
                user=self._username,
                password=self._password,
                db=self._name,
                charset=self._charset,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )

        self.init_post_connection()

        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    @classmethod
    def get_int_cast_type(cls):
        """
        Provides the right integer casting.
        """

        if PyFunceble.CONFIGURATION.db_type == "mariadb":
            return "INTEGER"
        return "SIGNED"

    @classmethod
    def authorization(cls):
        """
        Provides the authorization to operate.
        """

        return PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]

    @classmethod
    def parse_mysql_sql_file(cls):
        """
        Parses our mysql.sql file into something we understand.
        """

        source = PyFunceble.CONFIG_DIRECTORY + PyFunceble.OUTPUTS.db_type.directory

        if PyFunceble.CONFIGURATION.db_type == "mariadb":
            source += PyFunceble.OUTPUTS.db_type.files.mariadb
        elif PyFunceble.CONFIGURATION.db_type == "mysql":
            source += PyFunceble.OUTPUTS.db_type.files.mysql

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
        Parses the environment file into something we understand.

        :param str env_file_location: The location of the file we have to parse.
        """

        result = {}
        content = ""

        file_instance = PyFunceble.helpers.File(env_file_location)

        if file_instance.exists():
            content = file_instance.read()

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

    def save_to_env_file(self, envs, env_file_location):
        """
        Saves the given dict of environment variable into our environment file.

        :param dict envs: A dict of environment variables to save.
        :param str env_file_location: The location of the file we have to update.
        """

        if not self.pre_initiated and envs:
            file_instance = PyFunceble.helpers.File(env_file_location)

            try:
                content = file_instance.read()
            except FileNotFoundError:
                content = ""

            for environment_variable, value in envs.items():
                to_write = "{0}={1}".format(environment_variable, value)
                regex = r"{0}=.*".format(environment_variable)

                if content:
                    if PyFunceble.helpers.Regex(f"^{regex}").get_matching_list(
                        content.splitlines()
                    ):
                        content = PyFunceble.helpers.Regex(regex).replace_match(
                            content, to_write
                        )
                    else:
                        if not content.endswith("\n"):
                            content += "\n{0}\n".format(to_write)
                        else:
                            content += "{0}\n".format(to_write)
                else:
                    content += "{0}\n".format(to_write)

            file_instance.write(content, overwrite=True)

    def init_pre_connection(self):
        """
        Initiate everything needed before the connection.
        """

        if "mysql" in PyFunceble.INTERN:
            self.__dict__.update(PyFunceble.INTERN["mysql"].copy())

        if self.authorized and not self.pre_initiated:
            for (description, data) in self.variables.items():
                environment_var = PyFunceble.helpers.EnvironmentVariable(data["env"])
                if environment_var.exists():
                    setattr(
                        self, "_{0}".format(description), environment_var.get_value(),
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

            # pylint: disable = attribute-defined-outside-init
            self._port = int(self._port)
            self.save_to_env_file(self.env_content, self.pyfunceble_env_location)
            self.pre_initiated = True

    def init_post_connection(self):
        """
        Initiate everything needed after the connection.
        """

        if self.authorized and not self.post_initiated:
            self.create_tables_and_apply_patches()
            self.post_initiated = True

            PyFunceble.INTERN["mysql"] = self.__dict__.copy()

    def are_tables_present(self):
        """
        Checks if all our tables are present.
        """

        if self.authorized:
            for _, table_name in self.tables.items():
                with self.get_connection() as cursor:
                    query = (
                        "SELECT COUNT(*) "
                        "FROM information_schema.tables "
                        "WHERE table_schema = %(database_name)s "
                        "AND table_name = %(table_name)s "
                    )
                    cursor.execute(
                        query, {"database_name": self._name, "table_name": table_name,},
                    )

                    result = cursor.fetchone()

                    if result["COUNT(*)"] != 1:
                        return False

        return True

    def create_tables_and_apply_patches(self):
        """
        Creates the tables of the database and apply the patches.
        """

        if self.authorized and not self.db_tables_initiated:
            with self.connection.cursor() as cursor:
                for statement in self.parse_mysql_sql_file():
                    cursor.execute(statement)

                PyFunceble.LOGGER.info(
                    "Created the missing tables. Applied all patched"
                )

            self.db_tables_initiated = True
