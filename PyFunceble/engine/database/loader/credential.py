"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a simple and retro-compatible way to get access to the database credentials

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/master/

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

from getpass import getpass

import PyFunceble


class Credential:
    """
    Provides the credential loader.
    """

    var2env = {
        "host": {"env": "PYFUNCEBLE_DB_HOST", "default": "localhost"},
        "port": {"env": "PYFUNCEBLE_DB_PORT", "default": 3306},
        "name": {"env": "PYFUNCEBLE_DB_NAME", "default": "pyfunceble"},
        "username": {"env": "PYFUNCEBLE_DB_USERNAME", "default": "pyfunceble"},
        "password": {"env": "PYFUNCEBLE_DB_PASSWORD", "default": "PyFunceble:15_93le"},
        "charset": {"env": "PYFUNCEBLE_DB_CHARSET", "default": "utf8mb4"},
    }

    credentials = {}

    def __init__(self, db_type="mariadb") -> None:
        if PyFunceble.CONFIGURATION is None:
            PyFunceble.load_config()
            PyFunceble.CONFIGURATION.db_type = db_type

        if self.authorized:
            self.env_file_path = (
                PyFunceble.CONFIG_DIRECTORY
                + PyFunceble.abstracts.Infrastructure.ENV_FILENAME
            )
            self.decoded_env_file_content = self.parse_env_file(self.env_file_path)

    def __getitem__(self, index):
        if index in self.credentials:
            return self.credentials[index]

        raise KeyError(index)

    @property
    def authorized(self):
        """
        Provides the authorization to load the credentials.
        """

        return PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]

    @classmethod
    def parse_env_file(cls, env_file_path):
        """
        Parses the environment file into something we understand.

        :param str env_file_path:
            The location of the file we have to parse.
        """

        result = {}
        content = ""

        file_instance = PyFunceble.helpers.File(env_file_path)

        if file_instance.exists():
            content = file_instance.read()

            for line in content.splitlines():
                line = line.strip()

                if line.startswith("#"):
                    continue

                if "#" in line:
                    line = line[: line.find("#")]

                if "=" in line:
                    splitted = line.split("=")
                    result[splitted[0]] = splitted[1]

        return result

    @classmethod
    def save_to_env_file(cls, environment_variables, env_file_path):
        """
        Saves the given environment variabels into the given
        environment file.

        :param dict environment_variables:
            A dict of environment variables to save.
        :param str env_file_path:
            The location of the file we have to write/update.
        """

        if environment_variables:
            file_instance = PyFunceble.helpers.File(env_file_path)

            try:
                content = file_instance.read()
            except FileNotFoundError:
                content = ""

            for name, value in environment_variables.items():
                to_write = f"{name}={value}"
                regex = f"{name}=.*"

                if not content:
                    content = f"{to_write}\n"
                    continue

                if PyFunceble.helpers.Regex(f"^{regex}").get_matching_list(
                    content.splitlines()
                ):
                    content = PyFunceble.helpers.Regex(regex).replace_match(
                        content, to_write
                    )
                    continue

                if not content.endswith("\n"):
                    content += f"\n{to_write}\n"
                    continue

                content += f"{to_write}\n"

            file_instance.write(content, overwrite=True)

    def ask_for_them(self):
        """
        Ask the credentials to the end-user.
        """

        if self.authorized:
            for internal, data in self.var2env.items():
                environment_var = PyFunceble.helpers.EnvironmentVariable(data["env"])

                if environment_var.exists():
                    self.credentials[internal] = environment_var.get_value()
                else:
                    message = (
                        "[MySQL/MariaDB] Please give us your DB "
                        f"{internal} ({data['default']!r}): "
                    )

                    if internal != "password":
                        user_input = input(message)
                    else:
                        user_input = getpass(message)

                    if user_input:
                        self.credentials[internal] = user_input
                        self.decoded_env_file_content[environment_var.name] = user_input
                    else:
                        self.credentials[internal] = data["default"]
                        self.decoded_env_file_content[environment_var.name] = data[
                            "default"
                        ]

            self.credentials["port"] = int(self.credentials["port"])
            PyFunceble.INTERN["db_credentials"] = self.credentials.copy()
            self.save_to_env_file(self.decoded_env_file_content, self.env_file_path)

    def load(self):
        """
        Try to load the credentials. If they are not available, ask the end-user for it.
        """

        if "db_credentials" in PyFunceble.INTERN:
            self.credentials.update(PyFunceble.INTERN["db_credentials"])
        else:
            self.ask_for_them()

    def get(self):
        """
        Provides all the credentials.

        :rtype: dict
        """

        return self.credentials

    def get_uri(self):
        """
        Provides the sqlalchemy URI.
        """

        if not self.credentials:
            self.load()

        if PyFunceble.CONFIGURATION.db_type in ["mysql", "mariadb"]:
            protocol = "mysql+pymysql"
        else:
            raise Exception("Unknown protocol.")

        if self.credentials["host"].startswith("/"):
            return (
                f"{protocol}://"
                f"{self.credentials['username']}:{self.credentials['password']}"
                f"@localhost/{self.credentials['name']}"
                f"?unix_socket={self.credentials['host']}"
                f"&charset={self.credentials['charset']}"
            )

        return (
            f"{protocol}://"
            f"{self.credentials['username']}:{self.credentials['password']}"
            f"@{self.credentials['host']}/{self.credentials['name']}"
            f"?charset={self.credentials['charset']}"
        )
