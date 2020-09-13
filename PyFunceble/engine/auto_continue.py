"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the auto-continue engine.

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

from datetime import datetime
from multiprocessing import get_start_method

from sqlalchemy.orm.exc import NoResultFound

import PyFunceble
from PyFunceble.engine.database.loader import session
from PyFunceble.engine.database.schemas import File, Status


class AutoContinue:  # pylint: disable=too-many-instance-attributes
    """
    Provides the auto-continue subsystem.
    """

    # Save the content of the database.
    database = {}
    # Save the database file
    database_file = None
    # Save the filename we are working with.
    filename = None

    def __init__(self, filename, parent_process=False):
        # We get the operation authorization.
        self.database_file = ""
        # We share the filename.
        self.filename = filename
        # We preset the filename namespace.
        self.database[self.filename] = {}

        # We share if we are under the parent process.
        self.parent = parent_process

        self.authorized = self.authorization()

        PyFunceble.LOGGER.debug(f"Authorization: {self.authorized}")

        if self.authorized:
            # We are authorized to operate.

            PyFunceble.LOGGER.info("Process authorized.")

            if PyFunceble.CONFIGURATION.db_type == "json":
                # We set the location of the database file.
                self.database_file = (
                    PyFunceble.OUTPUT_DIRECTORY
                    + PyFunceble.OUTPUTS.parent_directory
                    + PyFunceble.OUTPUTS.logs.filenames.auto_continue
                )

            PyFunceble.LOGGER.debug(f"DB (File): {self.database_file}")

            # We load the backup (if existant).
            self.load()

            if self.parent and self.is_empty():
                # The database of the file we are
                # currently testing is empty.

                PyFunceble.LOGGER.info(
                    "Process authorized, is the parent process and the file "
                    "to test not indexed. Cleaning directory structure."
                )

                # We clean the output directory.
                PyFunceble.output.Clean(file_path=self.filename)
        elif self.parent:
            # We are not authorized to operate.

            PyFunceble.LOGGER.info(
                "Process not authorized but is the parent process. "
                "Cleaning directory structure."
            )

            # We clean the output directory.
            PyFunceble.output.Clean(file_path=self.filename)

    def __contains__(self, index):  # pragma: no cover
        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                if self.filename in self.database:
                    for status, status_data in self.database[self.filename].items():
                        if status == "complements":
                            continue

                        if index in status_data:
                            PyFunceble.LOGGER.info(
                                f"{index} is present into the database."
                            )
                            return True

                PyFunceble.LOGGER.info(f"{index} is not present into the database.")
                return False

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                with session.Session() as db_session:
                    try:
                        # pylint: disable=no-member, singleton-comparison
                        _ = (
                            db_session.query(Status)
                            .join(File)
                            .filter(Status.tested == index)
                            .filter(File.path == self.filename)
                            .one()
                        )
                    except NoResultFound:
                        PyFunceble.LOGGER.info(
                            f"{index} is not present into the database."
                        )
                        return False

                    PyFunceble.LOGGER.info(f"{index} is present into the database.")
                    return True

        PyFunceble.LOGGER.info(
            f"Could not check if {index} is present into the database. "
            "Unauthorized action."
        )
        return False

    @classmethod
    def authorization(cls):
        """
        Provides the execution authorization.
        """

        return (
            PyFunceble.CONFIGURATION.auto_continue
            and not PyFunceble.CONFIGURATION.no_files
        )

    def is_empty(self):
        """
        Checks if the database related to the currently tested
        file is empty.
        """

        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                if (
                    self.filename not in self.database
                    or not self.database[self.filename]
                ):
                    PyFunceble.LOGGER.info("File to test was not previously indexed.")
                    return True

                PyFunceble.LOGGER.info("File to test was previously indexed.")
                return False

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                # Here we don't really check if it is empty.
                # What we do, is that we check that everything was
                # tested.

                with session.Session() as db_session:
                    # pylint: disable=no-member, singleton-comparison
                    try:
                        result = (
                            db_session.query(File)
                            .filter(File.path == self.filename)
                            .one()
                        )

                        PyFunceble.LOGGER.info(
                            f"File was completely tested: {not result.test_completed}"
                        )
                        return result.test_completed
                    except NoResultFound:
                        pass

        PyFunceble.LOGGER.info(  # pragma: no cover
            "Could not check if the file to test "
            "was previously indexed. Unauthorized action."
        )
        return False  # pragma: no cover

    def add(self, subject, status):
        """
        Adds the given subject into the database.
        """

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION.db_type == "json":
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

                PyFunceble.LOGGER.info(
                    f"Indexed {repr(subject)} with the status "
                    f"{repr(status)} into {repr(self.filename)} database's."
                )

                # We save everything.
                self.save()

    def save(self):
        """
        Saves the current state of the database.
        """

        if (
            self.authorized
            and self.parent
            and PyFunceble.CONFIGURATION.db_type == "json"
        ):
            # We are authoried to operate.

            # We save the current database state.
            PyFunceble.helpers.Dict(self.database).to_json_file(self.database_file)

            PyFunceble.LOGGER.info(f"Saved database into {repr(self.database_file)}.")

    def load(self):
        """
        Loads previously saved database.
        """

        if self.authorized and PyFunceble.CONFIGURATION.db_type == "json":
            # We are authorized to operate.

            if PyFunceble.helpers.File(self.database_file).exists():
                # The database file exists.

                # We get its content and save it inside backup_content.
                self.database = PyFunceble.helpers.Dict().from_json_file(
                    self.database_file
                )
            else:
                # The database file do not exists.

                # We initiate an empty database.
                self.database = {self.filename: {}}

            PyFunceble.LOGGER.info(f"Loaded {repr(self.database_file)} in memory.")

    def clean(self):
        """
        Cleans the database.
        """

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION.db_type == "json":
                # We empty the database.
                self.database[self.filename] = {}

                # And we save the current database state.
                PyFunceble.helpers.Dict(self.database).to_json_file(self.database_file)

                PyFunceble.LOGGER.info(
                    "Cleaned the data related to "
                    f"{repr(self.filename)} from {repr(self.database_file)}."
                )
            elif PyFunceble.CONFIGURATION.db_type in [
                "mysql",
                "mariadb",
            ]:  # pragma: no cover
                with session.Session() as db_session:
                    # pylint: disable=no-member, singleton-comparison
                    try:
                        file_object = (
                            db_session.query(File)
                            .filter(File.path == self.filename)
                            .one()
                        )

                        file_object.test_completed = True

                        db_session.add(file_object)
                        db_session.commit()
                    except NoResultFound:
                        pass

                with session.Session() as db_session:
                    # pylint: disable=no-member, singleton-comparison

                    # Now we only replace the test_completed
                    # flag for the inactive/invalid one.
                    to_update = (
                        db_session.query(Status)
                        .join(File)
                        .filter(File.path == self.filename)
                        .filter(
                            Status.status.notin_(PyFunceble.core.CLI.get_up_statuses())
                        )
                        .filter(Status.test_completed == True)
                        .all()
                    )

                for status_object in to_update:
                    status_object.test_completed = False

                    with session.Session() as db_session:
                        # pylint: disable=no-member, singleton-comparison
                        db_session.add(status_object)
                        db_session.commit()

    def update_counters(self):  # pragma: no cover
        """
        Updates the counters.
        """

        if self.authorized and self.parent:
            # We are authorized to operate.

            # We create a list of all status we are working with.
            statuses = PyFunceble.STATUS.official.keys()

            # We preset the number of tested.
            tested = 0

            for status in statuses:
                # We loop through the list of status.

                if PyFunceble.CONFIGURATION.db_type == "json":
                    try:
                        # We get the number of tested of the currently read
                        # status.
                        tested_for_status = len(
                            self.database[self.filename][
                                PyFunceble.STATUS.official[status]
                            ]
                        )

                        # We then update/transfert it to its global place.
                        PyFunceble.INTERN["counter"]["number"][
                            status
                        ] = tested_for_status

                        PyFunceble.LOGGER.debug(
                            f"Counter of {repr(status)} set to {tested_for_status}."
                        )

                        # We finally increate the number of tested.
                        tested += tested_for_status
                    except KeyError:
                        PyFunceble.INTERN["counter"]["number"][status] = 0
                        continue
                elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                    with session.Session() as db_session:
                        # pylint: disable=no-member, singleton-comparison
                        result = (
                            db_session.query(Status)
                            .join(File)
                            .filter(File.path == self.filename)
                            .filter(Status.status == PyFunceble.STATUS.official[status])
                            .filter(Status.test_completed == True)
                            .all()
                        )

                        fetched = len(result)
                        PyFunceble.INTERN["counter"]["number"][status] = fetched

                        PyFunceble.LOGGER.debug(
                            f"Counter of {repr(status)} set to {fetched}."
                        )

                        # We then update/transfer it to its global place.
                        tested += fetched

            # We update/transfert the number of tested globally.
            PyFunceble.INTERN["counter"]["number"]["tested"] = tested
            PyFunceble.LOGGER.debug(f"Totally tested set to {repr(tested)}.")

    def get_already_tested(self):
        """
        Returns the list of subjects which were already tested as a set.
        """

        PyFunceble.LOGGER.info(
            "Getting the list of already tested (DATASET WONT BE LOGGED)"
        )

        # raise Exception("AUTHORIZED", self.authorized)

        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                if (
                    PyFunceble.CONFIGURATION.multiprocess
                    and get_start_method() == "spawn"
                ):  # pragma: no cover
                    self.load()

                try:
                    return {
                        y
                        for state, x in self.database[self.filename].items()
                        for y in x
                        if state not in ["complements"]
                    }
                except KeyError:  # pragma: no cover
                    pass
            elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                with session.Session() as db_session:
                    # pylint: disable=no-member, singleton-comparison
                    result = (
                        db_session.query(Status)
                        .join(File)
                        .filter(File.path == self.filename)
                        .filter(Status.test_completed == True)
                        .all()
                    )

                    if result:
                        return {x.tested for x in result}

        return set()  # pragma: no cover

    def __generate_complements(self):  # pragma: no cover
        """
        Generates the complements from the given list of tested.
        """

        # We get the list of domains we are going to work with.
        already_tested = self.get_already_tested()
        result = PyFunceble.get_complements(already_tested)

        # We remove the already tested subjects.
        return set(PyFunceble.helpers.List(result).format()) - already_tested

    def __get_or_generate_complements_json(self):  # pragma: no cover
        """
        Gets or generates the complements while working with
        as JSON formatted database.
        """

        result = []

        if "complements" not in self.database[self.filename].keys():
            # The complements are not saved,

            already_tested = self.get_already_tested()
            result = PyFunceble.get_complements(already_tested)

            # We remove the already tested subjects.
            result = set(PyFunceble.helpers.List(result).format()) - already_tested

            # We save the constructed list of complements
            self.database[self.filename]["complements"] = list(result)

            self.save()
        else:
            # We get the complements we still have to test.
            result = self.database[self.filename]["complements"]

        return result

    def __get_or_generate_complements_mysql(self):  # pragma: no cover
        """
        Gets or generates the complements while working with
        as MySQL/MariaDB formatted database.
        """

        result = []

        with session.Session() as db_session:
            # pylint: disable=singleton-comparison,no-member
            result = (
                db_session.query(Status)
                .join(File)
                .filter(File.path == self.filename)
                .filter(Status.is_complement == True)
                .all()
            )

            if result:
                result = [x.tested for x in result]
            else:
                result = self.__generate_complements()

        for subject in result:
            with session.Session() as db_session:
                try:
                    file = (
                        db_session.query(File).filter(File.path == self.filename).one()
                    )
                except NoResultFound:
                    file = File(path=self.filename)

                    db_session.add(file)
                    db_session.commit()
                    db_session.refresh(file)

            with session.Session() as db_session:
                # pylint: disable=no-member, singleton-comparison
                try:
                    status = (
                        db_session.query(Status).filter(Status.tested == subject).one()
                    )
                except NoResultFound:
                    status = Status(
                        file_id=file.id,
                        is_complement=True,
                        tested=subject,
                        tested_at=datetime.fromtimestamp(10),
                        test_completed=False,
                    )

                    db_session.add(status)
                    db_session.commit()

        return result

    def get_or_generate_complements(self):  # pragma: no cover
        """
        Gets or generates the complements.
        """

        PyFunceble.LOGGER.info("Generate/Get complements (DATASET WONT BE LOGGED)")

        if self.authorized and PyFunceble.CONFIGURATION.generate_complements:
            # We aer authorized to operate.

            if PyFunceble.CONFIGURATION.db_type == "json":
                return self.__get_or_generate_complements_json()
            if PyFunceble.CONFIGURATION.db_type in ["mysql", "mariadb"]:
                return self.__get_or_generate_complements_mysql()

        return list()
