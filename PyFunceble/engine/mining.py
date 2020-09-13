"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the mining engine.

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
import socket

from sqlalchemy.orm.exc import NoResultFound
from urllib3 import exceptions as urllib3_exceptions

import PyFunceble
from PyFunceble.engine.database.loader import session
from PyFunceble.engine.database.schemas import File, Mined, Status


class Mining:  # pylint: disable=too-many-instance-attributes
    """
    Manages the minig subsystem.
    """

    database = {}
    is_subject_present_cache = {}
    database_file = None

    filename = None
    headers = {}

    def __init__(self, filename, parent_process=False):  # pragma: no cover
        self.database_file = ""
        # We save the file we are working with.
        self.filename = filename
        # Se create the current file namespace.
        self.database[self.filename] = {}
        # We share the state.
        self.parent = parent_process

        self.authorized = self.authorization()

        PyFunceble.LOGGER.debug(f"Authorization: {self.authorized}")

        user_agent = PyFunceble.engine.UserAgent().get()

        if user_agent:
            # The user-agent is given.

            # We append the user agent to the header we are going to parse with
            # the request.
            self.headers = {"User-Agent": user_agent}

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION.db_type == "json":
                # We get the file we are going to save our data.
                self.database_file = (
                    PyFunceble.CONFIG_DIRECTORY
                    + PyFunceble.OUTPUTS.default_files.mining
                )

            PyFunceble.LOGGER.debug(f"DB (File): {self.database_file}")

            self.load()

    def __getitem__(self, index):
        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                if index in self.database[self.filename]:
                    return self.database[self.filename][index]

            if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                with session.Session() as db_session:
                    # pylint: disable=no-member
                    fetched = (
                        db_session.query(Mined)
                        .join(Status)
                        .filter(Status.id == Mined.subject_id)
                        .all()
                    )

                    if fetched:
                        return {x.mined for x in fetched}
        return None

    def __setitem__(self, index, value):  # pylint: disable=too-many-branches
        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
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

                        self.database[self.filename][index] = PyFunceble.helpers.List(
                            self.database[self.filename][index]
                        ).format()
                    else:  # pragma: no cover
                        self.database[self.filename][index] = value
                else:
                    if self.filename not in self.database:  # pragma: no cover
                        self.database[self.filename] = {}

                    self.database[self.filename][index] = value

                PyFunceble.LOGGER.info(
                    f"Inserted {repr(value)} into the subset of {repr(index)}"
                )
            elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                with session.Session() as db_session:
                    try:
                        # pylint: disable=no-member
                        status = (
                            db_session.query(Status)
                            .filter(Status.tested == index)
                            .one()
                        )
                    except NoResultFound:
                        pass

                with session.Session() as db_session:
                    # pylint: disable=no-member, singleton-comparison
                    in_db = (
                        db_session.query(Mined)
                        .filter(Mined.mined == value)
                        .filter(Mined.subject_id == status.id)
                        .all()
                    )

                if not in_db:
                    mined = Mined(
                        subject_id=status.id,
                        mined=value,
                        file_id=status.file_id,
                    )

                    with session.Session() as db_session:
                        # pylint: disable=no-member, singleton-comparison
                        db_session.add(mined)
                        db_session.commit()
                        db_session.refresh(mined)

    def __delitem__(self, index):
        if self.authorized:
            if PyFunceble.CONFIGURATION.db_type == "json":
                actual_value = self[index]

                if actual_value:
                    del self.database[self.filename][index]

                    PyFunceble.LOGGER.info(
                        "Cleaned the data related to "
                        f"{repr(index)} and {repr(self.filename)} "
                        f"from the database."
                    )
            elif PyFunceble.CONFIGURATION.db_type in [
                "mariadb",
                "mysql",
            ]:  # pragma: no cover
                with session.Session() as db_session:
                    # pylint: disable=no-member
                    to_delete = (
                        db_session.query(Mined)
                        .join(Status)
                        .filter(Status.tested == index)
                        .all()
                    )

                for row in to_delete:
                    # pylint: disable=no-member

                    with session.Session() as db_session:
                        # pylint: disable=no-member, singleton-comparison
                        delete_query = Mined.__table__.delete().where(
                            Mined.id == row.id
                        )
                        db_session.execute(delete_query)
                        db_session.commit()

                PyFunceble.LOGGER.info(
                    "Cleaned the data related to "
                    f"{repr(index)} and {repr(self.filename)} "
                    f"from the database."
                )

    @classmethod
    def authorization(cls):
        """
        Provides the operation authorization.
        """

        return PyFunceble.CONFIGURATION.mining

    @classmethod
    def get_history(cls, url, verify=None):  # pragma: no cover
        """
        Gets the history of the given url.

        :param str url: An URL to call.

        :return: The list of links.
        :rtype: list
        """

        if verify is None:
            verify = PyFunceble.CONFIGURATION.verify_ssl_certificate

        try:
            result = PyFunceble.REQUESTS.get(
                url,
                headers=cls.headers,
                timeout=PyFunceble.CONFIGURATION.timeout,
                verify=verify,
                allow_redirects=True,
            ).history

            for element in result.copy():
                if "location" in element.headers:
                    result.append(element.headers["location"])

            return result
        except (
            PyFunceble.REQUESTS.exceptions.ConnectionError,
            PyFunceble.REQUESTS.exceptions.Timeout,
            PyFunceble.REQUESTS.exceptions.InvalidURL,
            socket.timeout,
            urllib3_exceptions.InvalidHeader,
            UnicodeDecodeError,  # The probability that this happend in production is minimal.
        ):
            PyFunceble.LOGGER.exception()

        return []

    def list_of_mined(self):
        """
        Provides the list of mined domains so that they can
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

        PyFunceble.LOGGER.info(
            "Getting the list of previously mined data. (DATASET WONT BE LOGGED)"
        )

        # We initiate a variable which will return the result.
        result = []

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.CONFIGURATION.db_type == "json":

                for subject in self.database[self.filename].keys():
                    # We loop through the available list of status
                    # from the database.

                    for element in self[subject]:
                        # We then loop through the data associatied to
                        # the currently read status.

                        result.append((subject, element))
            elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                with session.Session() as db_session:
                    # pylint: disable=no-member
                    fetched = (
                        db_session.query(Mined)
                        .join(File)
                        .join(Status)
                        .filter(File.id == Mined.file_id)
                        .filter(Status.id == Mined.subject_id)
                        .all()
                    )

                    if fetched:
                        result = [(x.subject.tested, x.mined) for x in fetched]

        # We return the result.
        return result

    def load(self):
        """
        Loads the content of the database file.
        """

        if self.authorized and PyFunceble.CONFIGURATION.db_type == "json":
            # We are authorized to operate.

            if PyFunceble.helpers.File(self.database_file).exists():
                # The database file exists.

                # We update the database with the content of the file.
                self.database.update(
                    PyFunceble.helpers.Dict().from_json_file(self.database_file)
                )

                PyFunceble.LOGGER.info(
                    "Database content loaded in memory. (DATASET WONT BE LOGGED)"
                )

    def save(self):
        """
        Saves the content of the database into the database file.
        """

        if (
            self.authorized
            and self.parent
            and PyFunceble.CONFIGURATION.db_type == "json"
        ):
            # We are authorized to operate.

            # We save the database into the file.
            PyFunceble.helpers.Dict(self.database).to_json_file(self.database_file)

            PyFunceble.LOGGER.info(f"Saved database into {repr(self.database_file)}.")

    # pylint: disable=too-many-branches
    def mine(self, subject, subject_type):  # pragma: no cover
        """
        Searches for domain or URL related to the original URL or domain.
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

            PyFunceble.LOGGER.info("Starting mining logic..")

            if subject_type == "domain":
                to_get = "http://{0}:80".format(subject)
            elif subject_type == "url":
                to_get = subject

            else:
                raise ValueError("Unknown subject type {0}".format(repr(subject_type)))

            history = self.get_history(to_get)

            PyFunceble.LOGGER.debug(f"(Not processed) Mined:\n{history}")

            for element in history:
                # We loop through the list of requests history.

                try:
                    # We get the url from the currently read
                    # request.
                    url = element.url
                except AttributeError:
                    url = element

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

                    PyFunceble.LOGGER.debug(
                        f"{local_result} was successfully validated. "
                        "Removing possible Ports."
                    )

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
                    elif subject_type == "url" and local_result.endswith("/"):
                        local_result = local_result[:-1]

                    if local_result != subject:
                        # The local result is differnt from the
                        # subject we are working with.

                        PyFunceble.LOGGER.debug(
                            f"Saving {repr(local_result)} into the subset of {repr(subject)}."
                        )

                        # We save into the database.
                        self[subject] = [local_result]

            # We save the database.
            self.save()

    def remove(self, subject, history_member):
        """
        Removes the given subject from the database assigned to the
        currently tested file.

        :param str subject: The subject we are working with.
        :param str history_member: The history member to delete.
        """

        if self.authorized:
            while True:
                actual_value = self[subject]

                if (
                    isinstance(actual_value, (list, set))
                    and history_member in actual_value
                ):

                    if PyFunceble.CONFIGURATION.db_type == "json":
                        try:
                            actual_value.remove(history_member)

                            PyFunceble.LOGGER.info(
                                f"Removed {repr(history_member)} (mined) "
                                f"From the subset of {repr(subject)}."
                            )
                        except ValueError:  # pragma: no cover
                            pass
                    elif PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
                        # We construct the query string.

                        with session.Session() as db_session:
                            # pylint: disable=no-member
                            to_delete = (
                                db_session.query(Mined)
                                .join(Status)
                                .join(File)
                                .filter(File.id == Mined.file_id)
                                .filter(Status.tested == subject)
                                .filter(Mined.mined == history_member)
                                .all()
                            )

                        for row in to_delete:
                            with session.Session() as db_session:
                                # pylint: disable=no-member, singleton-comparison
                                delete_query = Mined.__table__.delete().where(
                                    Mined.id == row.id
                                )
                                db_session.execute(delete_query)
                                db_session.commit()

                        PyFunceble.LOGGER.info(
                            "Cleaned the data related to "
                            f"{repr(subject)}, {repr(history_member)} (mined) and "
                            f"{repr(self.filename)} and from "
                            f"the database."
                        )
                else:  # pragma: no cover
                    break

            if not self[subject]:  # pragma: no cover
                del self[subject]

            self.save()
