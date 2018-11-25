#!/usr/bin/env python3


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

This submodule will provide the database logic and interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

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
# pylint: disable=bad-continuation
import PyFunceble
from PyFunceble.generate import Generate
from PyFunceble.helpers import Dict, File, List


class Inactive:
    """
    Logic behind the generation and the usage of a database system.
    The main idea behind this is to provide an inactive-db.json and test all
    inactive domain which are into to it regularly
    """

    def __init__(self):
        # We get the file path we are working with.
        self.file_path = PyFunceble.CONFIGURATION["file_to_test"]

        # We set the equivalent of one day in seconds.
        self.one_day_in_seconds = 1 * 24 * 3600

        # We convert the number of days between the database retest
        # to seconds.
        self.days_in_seconds = (
            PyFunceble.CONFIGURATION["days_between_db_retest"] * 24 * 3600
        )

        # We set the path to the inactive database file.
        self.inactive_db_path = (
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.OUTPUTS["default_files"]["inactive_db"]
        )

        if (
            "to_test" in PyFunceble.CONFIGURATION
            and PyFunceble.CONFIGURATION["to_test"]
        ):
            # We are testing something.

            # We set a variable which will save the actual element we are working with.
            self.element = PyFunceble.CONFIGURATION["to_test"]

        if "inactive_db" not in PyFunceble.CONFIGURATION:
            # The database is empty or equal to None.

            # We initiate it with an empty dictionnary.
            PyFunceble.CONFIGURATION["inactive_db"] = {}

    def _reformat_historical_formating_error(self):  # pragma: no cover
        """
        Format the old format so it can be merged into the newer format.
        """

        # We construct the possible path to an older version of the database.
        historical_formating_error = PyFunceble.CURRENT_DIRECTORY + "inactive-db.json"

        if PyFunceble.path.isfile(historical_formating_error):
            # The histortical file already exists.

            # We get its content.
            data = Dict().from_json(File(historical_formating_error).read())

            # We initiate a variable which will save the data that is going
            # to be merged.
            data_to_parse = {}

            # We get the database keybase.
            top_keys = data.keys()

            for top_key in top_keys:
                # We loop through the list of upper keys.

                # We get the lowest keys.
                low_keys = data[top_key].keys()

                # We initiate the data to parse.
                data_to_parse[top_key] = {}

                for low_key in low_keys:
                    # We loop through the list of lower keys.

                    if low_key.isdigit():
                        # The current low key is a digit.

                        # We parse its content (from the old) into the new format.
                        # In between, we remove 30 days from the low_key so that
                        # it become in the past. This way they will be retested
                        # automatically.
                        data_to_parse[top_key][
                            int(low_key) - (self.one_day_in_seconds * 30)
                        ] = data[top_key][low_key]
                    else:
                        # The current low key is not a digit.

                        # We parse its content (from the old) into the new format.
                        # In between, we remove 30 days from the current time so that
                        # it become in the past. This way they will be retested
                        # automatically.
                        data_to_parse[top_key][
                            int(PyFunceble.time()) - (self.one_day_in_seconds * 30)
                        ] = data[top_key][low_key]

            if "inactive_db" in PyFunceble.CONFIGURATION:
                # The current (new) database is not empty.

                # We update add the content of the old into the current database.
                PyFunceble.CONFIGURATION["inactive_db"].update(data_to_parse)
            else:
                # The current (new) database is empty.

                # We replace the content with the data_to_parse as it is complient
                # with the new format.
                PyFunceble.CONFIGURATION["inactive_db"] = data_to_parse

            # We delete the old database file.
            File(historical_formating_error).delete()

    def _merge(self):
        """
        Merge the real database with the older one which
        has already been set into :code:`PyFunceble.CONFIGURATION["inactive_db"]`
        """

        # We get the content of the database.
        database_content = Dict().from_json(File(self.inactive_db_path).read())

        # We get the database top keys.
        database_top_keys = database_content.keys()

        for database_top_key in database_top_keys:
            # We loop through the list of database top keys.

            if database_top_key not in PyFunceble.CONFIGURATION["inactive_db"]:
                # The currently read top key is not already into the database.

                # We initiate the currently read key with the same key from
                # our database file.
                PyFunceble.CONFIGURATION["inactive_db"][
                    database_top_key
                ] = database_content[database_top_key]
            else:
                # The currently read top key is already into the database.

                # We get the list of lower indexes.
                database_low_keys = database_content[database_top_key].keys()

                for database_low_key in database_low_keys:
                    # We loop through the lower keys.

                    if (
                        database_low_key
                        not in PyFunceble.CONFIGURATION["inactive_db"][database_top_key]
                    ):  # pragma: no cover
                        # The lower key is not already into the database.

                        # We initiate the currently read low and top key with the
                        # same combinaison from our database file.
                        PyFunceble.CONFIGURATION["inactive_db"][database_top_key][
                            database_low_key
                        ] = database_content[database_top_key][database_low_key]
                    else:
                        # The lower key is not already into the database.

                        # We exted the currently read low and top key combinaison
                        # with the same combinaison from our database file.
                        PyFunceble.CONFIGURATION["inactive_db"][database_top_key][
                            database_low_key
                        ].extend(database_content[database_top_key][database_low_key])

                        # And we format the list of element to ensure that there is no
                        # duplicate into the database content.
                        PyFunceble.CONFIGURATION["inactive_db"][database_top_key][
                            database_low_key
                        ] = List(
                            PyFunceble.CONFIGURATION["inactive_db"][database_top_key][
                                database_low_key
                            ]
                        ).format()

    def _retrieve(self):
        """
        Return the current content of the inactive-db.json file.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            # We get, format and initiate the historical database file.
            self._reformat_historical_formating_error()

            if PyFunceble.path.isfile(self.inactive_db_path):
                # The database file exist.

                # We merge our current database into already initiated one.
                self._merge()

    def _backup(self):
        """
        Save the current database into the inactive-db.json file.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            # We save the current database state into the database file.
            Dict(PyFunceble.CONFIGURATION["inactive_db"]).to_json(self.inactive_db_path)

    def _add_to_test(self, to_add):
        """
        Add an element or a list of element into
        :code:`PyFunceble.CONFIGURATION['inactive_db'][self.file_path]['to_test']`.

        :param to_add: The domain, IP or URL to add.
        :type to_add: str|list
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            if not isinstance(to_add, list):
                # The element to add is not a list.

                # We set it into a list.
                to_add = [to_add]

            if self.file_path in PyFunceble.CONFIGURATION["inactive_db"]:
                # The file we are testing is into the database.

                if "to_test" in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                    # The `to_test` index is into the database related to the file
                    # we are testing.

                    # We extend the `to_test` element with the list we have to restest.
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                        "to_test"
                    ].extend(to_add)
                else:
                    # The `to_test` index is not into the database related to the file
                    # we are testing.

                    # We initiate the `to_test` element with the list we have to retest.
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                        "to_test"
                    ] = to_add
            else:
                # The file we are testing is not into the database.

                # We add the file and its to_test information into the database.
                PyFunceble.CONFIGURATION["inactive_db"].update(
                    {self.file_path: {"to_test": to_add}}
                )

            # We format the list to test in order to avoid duplicate.
            PyFunceble.CONFIGURATION["inactive_db"][self.file_path]["to_test"] = List(
                PyFunceble.CONFIGURATION["inactive_db"][self.file_path]["to_test"]
            ).format()

            # And we finally backup the database.
            self._backup()

    def to_test(self):
        """
        Get the list to test for the next session.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            # We initiate a variable which is going to save what we are going
            # to return.
            result = []

            # We initiate a variable which is going to save the key to remove
            # once they are merged into the `to_test` index.
            to_delete = []

            # We retrieve the database informations.
            self._retrieve()

            if self.file_path in PyFunceble.CONFIGURATION["inactive_db"]:
                # The file we are testing is into the database.

                for data in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                    # We loop through the database content related to the file we
                    # are testing.

                    if data != "to_test":
                        # The currently read index is not `to_test`.

                        if int(PyFunceble.time()) > int(data) + self.days_in_seconds:
                            # The currently read index is older than the excepted time
                            # for retesting.

                            # We extend our result variable with the content from the
                            # currently read index.
                            result.extend(
                                PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                                    data
                                ]
                            )

                            # And we append the currently read index into the list of
                            # index to delete.
                            to_delete.append(data)

                # We remove all indexes which are present into the list of index to delete.
                Dict(
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path]
                ).remove_key(to_delete)

                # And we append our list of element to retest into the `to_test` index.s
                self._add_to_test(result)
            else:
                # The file we are testing is not into the database.

                # We add the file we are testing into the database.
                PyFunceble.CONFIGURATION["inactive_db"].update({self.file_path: {}})

            # And we finally backup the database.
            self._backup()

    def _timestamp(self):
        """
        Get the timestamp where we are going to save our current list.

        :return: The timestamp to append with the currently tested element.
        :rtype: int|str
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            if (
                "inactive_db" in PyFunceble.CONFIGURATION
                and self.file_path in PyFunceble.CONFIGURATION["inactive_db"]
                and PyFunceble.CONFIGURATION["inactive_db"][self.file_path]
            ):
                # The file we are testing is into the database and its content
                # is not empty.

                # We get the indexes of the current file (in the dabase).
                database_keys = list(
                    filter(
                        lambda x: x.isdigit(),
                        PyFunceble.CONFIGURATION["inactive_db"][self.file_path].keys(),
                    )
                )

                if database_keys:
                    # The list of keys is not empty.

                    # We get the most recent date.
                    recent_date = max(database_keys)
                else:  # pragma: no cover
                    # The list of keys is empty.

                    # We return the current time.
                    return int(PyFunceble.time())

                if int(PyFunceble.time()) > int(recent_date) + self.one_day_in_seconds:
                    # The most recent time was in more than one day.

                    # We return the current time.
                    return int(PyFunceble.time())

                # The most recent time was in less than one day.

                if int(PyFunceble.time()) < int(recent_date) + self.days_in_seconds:
                    # The most recent time was in less than the expected number of day for
                    # retesting.

                    # We return the most recent data.
                    return int(recent_date)

        # The database subsystem is not activated.

        # We return the current time.
        return int(PyFunceble.time())

    def add(self):
        """
        Save the current :code.`PyFunceble.CONFIGURATION['to_test']`
        into the current timestamp.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            # We get the timestamp to use as index.
            timestamp = str(self._timestamp())

            if (
                "inactive_db" in PyFunceble.CONFIGURATION
                and self.file_path in PyFunceble.CONFIGURATION["inactive_db"]
            ):
                # * The file path is not into the database.

                if timestamp in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                    # The timetamp is already into the database related to the file we
                    # are testing.

                    if (
                        self.element
                        not in PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                            timestamp
                        ]
                    ):
                        # The currently tested element is not into the database related
                        # to the file we are testing.

                        # We append the currently tested element into the database.
                        PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                            timestamp
                        ].append(self.element)
                else:
                    # The timetamp is not into the database related to the file we
                    # are testing.

                    # We append the index and the database element into the databse
                    # related to the file we are testing.
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path].update(
                        {timestamp: [self.element]}
                    )

                if (
                    "to_test" in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]
                    and self.element
                    in PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                        "to_test"
                    ]
                ):
                    # * The `to_test` index is into the database related to the file we
                    #   are testing.
                    # and
                    # * The element we are testing is into the `to_test` index related to
                    #   the file we are testing.

                    # We remove the element from the list of element to test.
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                        "to_test"
                    ].remove(self.element)
            else:
                # The file path is not into the database.

                # We initiate the file path and its content into the database.
                PyFunceble.CONFIGURATION["inactive_db"] = {
                    self.file_path: {timestamp: [self.element]}
                }

            # And we save the data into the database.
            self._backup()

    def remove(self):
        """
        Remove all occurence of :code:`PyFunceble.CONFIGURATION['to_test']`
        from the database.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            if self.file_path in PyFunceble.CONFIGURATION["inactive_db"]:
                #  The file path is into the database.

                for data in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                    # We loop through the index of the file database.

                    if (
                        self.element
                        in PyFunceble.CONFIGURATION["inactive_db"][self.file_path][data]
                    ):
                        # The currently tested element into the currently read index.

                        # We generate the suspicious file(s).
                        Generate("strange").analytic_file(
                            "suspicious", PyFunceble.STATUS["official"]["up"]
                        )

                        # We remove the currently tested element from the read index.
                        PyFunceble.CONFIGURATION["inactive_db"][self.file_path][
                            data
                        ].remove(self.element)

            # And we save the data into the database.
            self._backup()

    def content(self):
        """
        Get the content of the database.

        :return: The content of the database.
        :rtype: list
        """

        # We initiate a variable which will save what we are going to return.
        result = []

        if (
            PyFunceble.CONFIGURATION["inactive_database"]
            and PyFunceble.CONFIGURATION["inactive_db"]
        ):
            # * The database subsystem is activated.
            # and
            # * The database is not empty.

            for key in PyFunceble.CONFIGURATION["inactive_db"][self.file_path]:
                # We loop through the index of the current file database.

                if key == "to_test":
                    # The current key is `to_test`.

                    # We continue to the next element.
                    continue

                # We extend the result with the content of the currently read index.
                result.extend(
                    PyFunceble.CONFIGURATION["inactive_db"][self.file_path][key]
                )

        # We return the content of the database.
        return result


class Whois:
    """
    Logic behind the whois database. Indeed, the idea is to implement #2.

    :param expiration_date: The extracted expiration date.
    :type expiration_date: str
    """

    def __init__(self, expiration_date=None):
        # We get the extracted expiration date.
        self.expiration_date = expiration_date

        if self.expiration_date:
            # We get the epoch of the expiration date.
            self.epoch = int(
                PyFunceble.mktime(PyFunceble.strptime(self.expiration_date, "%d-%b-%Y"))
            )

        if (
            "file_to_test" in PyFunceble.CONFIGURATION
            and PyFunceble.CONFIGURATION["file_to_test"]
        ):
            # The file path was given previously.
            self.file_path = PyFunceble.CONFIGURATION["file_to_test"]
        else:
            # The file path was not given previously.

            # We set a dummy index.
            self.file_path = "single_testing"

        # We set the path to the whois database file.
        self.whois_db_path = (
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.OUTPUTS["default_files"]["whois_db"]
        )

        if (
            "to_test" in PyFunceble.CONFIGURATION
            and PyFunceble.CONFIGURATION["to_test"]
        ):
            # We are testing something.

            # We set a variable which will save the actual element we are working with.
            self.element = PyFunceble.CONFIGURATION["to_test"]

        # We try to retrieve the information from the database file.
        self._retrieve()

    @classmethod
    def _authorization(cls):
        """
        Check if we are authorized to work with our database.
        """

        if (
            not PyFunceble.CONFIGURATION["no_whois"]
            and PyFunceble.CONFIGURATION["whois_database"]
        ):
            # * The usage of whois lookup is activated.
            # and
            # * The usage of the whois database is activated.

            # We return True, we are authorized to work.
            return True

        # * The usage of whois lookup is not activated.
        # or
        # * The usage of the whois database is not activated.

        # We return False, we are not authorized to work.
        return False

    def _retrieve(self):
        """
        Retrieve the data from the database.
        """

        if self._authorization() and "whois_db" not in PyFunceble.CONFIGURATION:
            # The usage of the whois database is activated.

            if PyFunceble.path.isfile(self.whois_db_path):
                # The database file exist.

                # We merge our current database into already initiated one.
                PyFunceble.CONFIGURATION["whois_db"] = Dict().from_json(
                    File(self.whois_db_path).read()
                )
            else:
                # The database file does not exist.

                # We initiate an empty database.
                PyFunceble.CONFIGURATION["whois_db"] = {}

    def _backup(self):
        """
        Backup the database into its file.
        """

        if self._authorization():
            # We are authorized to work.

            # We backup the current state of the datbase.
            Dict(PyFunceble.CONFIGURATION["whois_db"]).to_json(self.whois_db_path)

    def is_in_database(self):
        """
        Check if the element is into the database.
        """

        if (
            self._authorization()
            and self.file_path in PyFunceble.CONFIGURATION["whois_db"]
            and self.element in PyFunceble.CONFIGURATION["whois_db"][self.file_path]
        ):
            # * We are authorized to work.
            # and
            # * The given file path exist in the database.
            # and
            # * The element we are testing is in the database related to the
            # given file path.

            # We return True, the element we are testing is into the database.
            return True

        # * We are not authorized to work.
        # or
        # * The given file path does not exist in the database.
        # or
        # * The element we are testing is not in the database related to the
        # given file path.

        # We return False,the element we are testing is not into the database.
        return False

    def is_time_older(self):
        """
        Check if the current time is older than the one in the database.
        """

        if (
            self._authorization()
            and self.is_in_database()
            and int(
                PyFunceble.CONFIGURATION["whois_db"][self.file_path][self.element][
                    "epoch"
                ]
            )
            < int(PyFunceble.time())
        ):
            # * We are authorized to work.
            # and
            # * The element we are testing is in the database.
            # and
            # * The epoch of the expiration date is less than our current epoch.

            # The expiration date is in the past, we return True.
            return True

        # The expiration date is in the future, we return False.
        return False

    def get_expiration_date(self):
        """
        Get the expiration date from the database.

        :return: The expiration date from the database.
        :rtype: str|None
        """

        if self._authorization() and self.is_in_database() and not self.is_time_older():
            # * We are authorized to work.
            # and
            # * The element we are testing is in the database.
            # and
            # * The expiration date is in the future.

            # We get the expiration date from the database.
            result = PyFunceble.CONFIGURATION["whois_db"][self.file_path][self.element][
                "expiration_date"
            ]

            if result:
                # The expiration date from the database is not empty nor
                # equal to None.

                # We return it.
                return result

        # We return None, there is no data to work with.
        return None

    def add(self):
        """
        Add the currently tested element into the database.
        """

        if self._authorization():
            # We are authorized to work.

            if self.epoch < int(PyFunceble.time()):
                state = "past"
            else:
                state = "future"

            if self.is_in_database():
                # The element we are working with is in the database.

                if (
                    str(self.epoch)
                    != PyFunceble.CONFIGURATION["whois_db"][self.file_path][
                        self.element
                    ]["epoch"]
                ):
                    # The given epoch is diffent from the one saved.

                    # We update it.
                    PyFunceble.CONFIGURATION["whois_db"][self.file_path][
                        self.element
                    ].update(
                        {
                            "epoch": str(self.epoch),
                            "state": state,
                            "expiration_date": self.expiration_date,
                        }
                    )

                elif self.is_time_older():
                    # The expiration date from the database is in the past.

                    if (
                        PyFunceble.CONFIGURATION["whois_db"][self.file_path][
                            self.element
                        ]["state"]
                        != "past"
                    ):  # pragma: no cover
                        # The state of the element in the datbase is not
                        # equal to `past`.

                        # We update it to `past`.
                        PyFunceble.CONFIGURATION["whois_db"][self.file_path][
                            self.element
                        ].update({"state": "past"})
                elif (
                    PyFunceble.CONFIGURATION["whois_db"][self.file_path][self.element][
                        "state"
                    ]
                    != "future"
                ):
                    # * The expiration date from the database is in the future.
                    # and
                    # * The state of the element in the database is not
                    # equal to `future`.

                    # We update it to `future`.
                    PyFunceble.CONFIGURATION["whois_db"][self.file_path][
                        self.element
                    ].update({"state": "future"})
            else:
                # The element we are working with is not in the database.

                if not self.file_path in PyFunceble.CONFIGURATION["whois_db"]:
                    # The file path is not in the database.

                    # We initiate it.
                    PyFunceble.CONFIGURATION["whois_db"][self.file_path] = {}

                # We create the first dataset.
                PyFunceble.CONFIGURATION["whois_db"][self.file_path].update(
                    {
                        self.element: {
                            "epoch": str(self.epoch),
                            "state": state,
                            "expiration_date": self.expiration_date,
                        }
                    }
                )

            # We do a safety backup of our database.
            self._backup()
