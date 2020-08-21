"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the migrator. It migrated the data from old to the new structure.

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

from os import sep as directory_separator

import pymysql
import pymysql.cursors
from colorama import Fore, Style
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

import PyFunceble

from ..schemas.file import File
from ..schemas.status import Status
from ..schemas.whois_record import WhoisRecord


class CleanupOldTables:
    """
    Provides the interface which is in charge of cleaning the database.

    :param credentials:
        A credentials object.
    """

    old_tables = [
        "pyfunceble_auto_continue",
        "pyfunceble_inactive",
        "pyfunceble_mining",
        "pyfunceble_tested",
        "pyfunceble_whois",
    ]

    def __init__(self, credentials, db_session):
        self.credentials = credentials
        self.db_session = db_session

        self.autosave_authorized = PyFunceble.engine.AutoSave().authorized

    @property
    def authorized(self):
        """
        Provides the authorization to run.
        """

        return PyFunceble.CONFIGURATION.db_type in ["mysql", "mariadb"] and any(
            [self.does_table_exists(x) for x in self.old_tables]
        )

    def get_old_connection(self):
        """
        Provides a connection, the old way.
        """

        if (
            directory_separator not in self.credentials["host"]
            or "/" not in self.credentials["host"]
        ):
            return pymysql.connect(
                host=self.credentials["host"],
                port=self.credentials["port"],
                user=self.credentials["username"],
                password=self.credentials["password"],
                db=self.credentials["name"],
                charset=self.credentials["charset"],
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )

        return pymysql.connect(
            unix_socket=self.credentials["host"],
            user=self.credentials["username"],
            password=self.credentials["password"],
            db=self.credentials["name"],
            charset=self.credentials["charset"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def does_table_exists(self, table_name):
        """
        Checks if the table exists.

        :param str table_name:
            The name of the table to check.
        """

        old_connection = self.get_old_connection()
        with old_connection.cursor() as cursor:
            statement = (
                "SELECT COUNT(*) "
                "FROM information_schema.tables "
                "WHERE table_schema = %(database_name)s "
                "AND table_name = %(table_name)s "
            )

            cursor.execute(
                statement,
                {"database_name": self.credentials["name"], "table_name": table_name,},
            )

            result = cursor.fetchone()

            if result["COUNT(*)"] != 1:
                old_connection.close()
                return False
        old_connection.close()
        return True

    def __start_tested_migration(self):
        """
        Starts the migration of the tested data.
        """

        if self.does_table_exists("pyfunceble_tested"):
            old_connection = self.get_old_connection()
            with old_connection.cursor() as cursor:
                statement = "SELECT * FROM pyfunceble_tested"
                cursor.execute(statement)

                result = cursor.fetchall()
            old_connection.close()

            for data in result:
                try:
                    self.db_session.rollback()
                    file = (
                        self.db_session.query(File)
                        .filter(File.path == data["file_path"])
                        .one()
                    )
                except NoResultFound:
                    file = File(path=data["file_path"])

                    self.db_session.add(file)
                    self.db_session.commit()
                    self.db_session.refresh(file)

                status = Status(
                    file_id=file.id,
                    created=data["created"],
                    modified=data["modified"],
                    tested=data["tested"],
                    _status=data["_status"],
                    status=data["status"],
                    _status_source=data["_status_source"],
                    status_source=data["status_source"],
                    domain_syntax_validation=data["domain_syntax_validation"],
                    expiration_date=data["expiration_date"],
                    http_status_code=data["http_status_code"],
                    ipv4_range_syntax_validation=data["ipv4_range_syntax_validation"],
                    ipv4_syntax_validation=data["ipv4_syntax_validation"],
                    ipv6_range_syntax_validation=data["ipv6_range_syntax_validation"],
                    ipv6_syntax_validation=data["ipv6_syntax_validation"],
                    subdomain_syntax_validation=data["subdomain_syntax_validation"],
                    url_syntax_validation=data["url_syntax_validation"],
                    is_complement=False,
                    test_completed=True,
                )

                try:
                    self.db_session.add(status)
                    self.db_session.commit()
                    self.db_session.refresh(status)
                except IntegrityError:
                    pass

                old_connection = self.get_old_connection()
                with old_connection.cursor() as cursor:
                    statement = "DELETE FROM pyfunceble_tested WHERE id = %(status_id)s"
                    # pylint: disable=no-member
                    cursor.execute(statement, {"status_id": status.id})
                old_connection.close()

                if self.autosave_authorized or PyFunceble.CONFIGURATION.print_dots:
                    PyFunceble.LOGGER.info(f'Switched {data["tested"]} to SQLAlchemy.')
                    print(".", end="")

    def __start_autocontinue_migration(self):
        """
        Starts the migration of the autocontinue data.
        """

        if self.does_table_exists("pyfunceble_auto_continue"):
            old_connection = self.get_old_connection()
            with old_connection.cursor() as cursor:
                statement = "SELECT * FROM pyfunceble_auto_continue"
                cursor.execute(statement)

                result = cursor.fetchall()
            old_connection.close()

            for data in result:
                try:
                    self.db_session.rollback()
                    file = (
                        self.db_session.query(File)
                        .filter(File.path == data["file_path"])
                        .one()
                    )
                except NoResultFound:
                    file = File(path=data["file_path"])

                    self.db_session.add(file)
                    self.db_session.commit()
                    self.db_session.refresh(file)

                try:
                    status = (
                        self.db_session.query(Status)
                        .join(File)
                        .filter(File.path == data["file_path"])
                        .filter(Status.tested == data["subject"])
                        .one()
                    )
                except NoResultFound:
                    status = Status(
                        tested=data["subject"], status=data["subject"], file_id=file.id
                    )

                status.is_complement = data["is_complement"]

                try:
                    self.db_session.add(status)
                    self.db_session.commit()
                except IntegrityError:
                    pass

                old_connection = self.get_old_connection()
                with old_connection.cursor() as cursor:
                    statement = "DELETE FROM pyfunceble_auto_continue WHERE id = %(id)s"
                    cursor.execute(statement, {"id": data["id"]})
                old_connection.close()

                if self.autosave_authorized or PyFunceble.CONFIGURATION.print_dots:
                    PyFunceble.LOGGER.info(
                        f'Switched {data["subject"]} (AUTOCONTINUE) to SQLAlchemy.'
                    )
                    print(".", end="")

    def __start_whois_migration(self):
        """
        Starts the migration of the whois data.
        """

        if self.does_table_exists("pyfunceble_whois"):
            old_connection = self.get_old_connection()
            with old_connection.cursor() as cursor:
                statement = "SELECT * FROM pyfunceble_whois"
                cursor.execute(statement)

                result = cursor.fetchall()
            old_connection.close()

            for data in result:

                try:
                    self.db_session.rollback()
                    _ = (
                        self.db_session.query(Status)
                        .filter(Status.tested == data["subject"])
                        .one()
                    )
                except NoResultFound:
                    continue
                except MultipleResultsFound:
                    pass

                whois_record = WhoisRecord(
                    subject=data["subject"],
                    modified=data["modified"],
                    created=data["created"],
                    expiration_date=data["expiration_date"],
                    epoch=data["expiration_date_epoch"],
                    record=data["record"],
                    state=data["state"],
                )

                try:
                    self.db_session.add(whois_record)
                    self.db_session.commit()
                except IntegrityError:
                    pass

                old_connection = self.get_old_connection()
                with old_connection.cursor() as cursor:
                    statement = "DELETE FROM pyfunceble_whois WHERE id = %(id)s"
                    cursor.execute(statement, {"id": data["id"]})
                old_connection.close()

                if self.autosave_authorized or PyFunceble.CONFIGURATION.print_dots:
                    PyFunceble.LOGGER.info(
                        f'Switched {data["subject"]} (WHOIS) to SQLAlchemy.'
                    )
                    print(".", end="")

    def __delete_old_tables(self):
        """
        Deletes all the tables which we don't need.
        """

        for table in self.old_tables:
            if self.does_table_exists(table):
                old_connection = self.get_old_connection()
                with old_connection.cursor() as cursor:
                    statement = f"DROP TABLE {table}"
                    cursor.execute(statement)
                old_connection.close()

            if self.autosave_authorized or PyFunceble.CONFIGURATION.print_dots:
                PyFunceble.LOGGER.info(f"Deleted {table} from the database.")
                print(".", end="")

    def start(self):
        """
        Starts the migration of old data into the new structure.
        """

        if self.authorized:
            print(f"{Fore.MAGENTA}{Style.BRIGHT}Starting switch to SQLAlchemy ...")
            self.__start_tested_migration()
            self.__start_autocontinue_migration()
            self.__start_whois_migration()

            self.__delete_old_tables()
            print(f"{Fore.MAGENTA}{Style.BRIGHT}Finished switch to SQLAlchemy!")
