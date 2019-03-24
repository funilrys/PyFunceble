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
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://funilrys.github.io/PyFunceble/

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
# pylint: disable=bad-continuation
import PyFunceble
from PyFunceble.helpers import Dict, File, List


class Inactive:
    """
    Logic behind the generation and the usage of a database system.
    The main idea behind this is to provide an inactive-db.json and test all
    inactive domain which are into to it regularly.

    :param subject: The subject we are working with.
    :type subject: str

    :param filename: The name of the file we are processing.
    :type filename: str
    """

    is_subject_present_cache = {}

    def __init__(self, filename):
        # We share the filename.
        self.filename = filename

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

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

            # We create the database content.
            self.database_content = {}

    def _reformat_historical_formating_error(self):  # pragma: no cover
        """
        Format the old format so it can be merged into the newer format.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            # We construct the possible path to an older version of the database.
            historical_formating_error = (
                PyFunceble.CURRENT_DIRECTORY + "inactive-db.json"
            )

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

                self.database_content.update(data_to_parse)

                # We delete the old database file.
                File(historical_formating_error).delete()

    def _merge(self):
        """
        Merge the real database with the older one which
        has already been set into the database.
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            # We get the content of the database.
            database_content = Dict().from_json(File(self.inactive_db_path).read())

            # We get the database top keys.
            database_top_keys = database_content.keys()

            for database_top_key in database_top_keys:
                # We loop through the list of database top keys.

                if database_top_key not in self.database_content:
                    # The currently read top key is not already into the database.

                    # We initiate the currently read key with the same key from
                    # our database file.
                    self.database_content[database_top_key] = database_content[
                        database_top_key
                    ]
                else:
                    # The currently read top key is already into the database.

                    # We get the list of lower indexes.
                    database_low_keys = database_content[database_top_key].keys()

                    for database_low_key in database_low_keys:
                        # We loop through the lower keys.

                        if (
                            database_low_key
                            not in self.database_content[database_top_key]
                        ):  # pragma: no cover
                            # The lower key is not already into the database.

                            # We initiate the currently read low and top key with the
                            # same combinaison from our database file.
                            self.database_content[database_top_key][
                                database_low_key
                            ] = database_content[database_top_key][database_low_key]
                        else:
                            # The lower key is not already into the database.

                            # We exted the currently read low and top key combinaison
                            # with the same combinaison from our database file.
                            self.database_content[database_top_key][
                                database_low_key
                            ].extend(
                                database_content[database_top_key][database_low_key]
                            )

                            # And we format the list of element to ensure that there is no
                            # duplicate into the database content.
                            self.database_content[database_top_key][
                                database_low_key
                            ] = List(
                                self.database_content[database_top_key][
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
            Dict(self.database_content).to_json(self.inactive_db_path)

    def _add_to_test(self, to_add):
        """
        Add an element or a list of element into
        :code:`PyFunceble.INTERN['inactive_db'][self.filename]['to_test']`.

        :param to_add: The domain, IP or URL to add.
        :type to_add: str|list
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            if not isinstance(to_add, list):
                # The element to add is not a list.

                # We set it into a list.
                to_add = [to_add]

            if self.filename in self.database_content:
                # The file we are testing is into the database.

                if "to_test" in self.database_content[self.filename]:
                    # The `to_test` index is into the database related to the file
                    # we are testing.

                    # We extend the `to_test` element with the list we have to restest.
                    self.database_content[self.filename]["to_test"].extend(to_add)
                else:
                    # The `to_test` index is not into the database related to the file
                    # we are testing.

                    # We initiate the `to_test` element with the list we have to retest.
                    self.database_content[self.filename]["to_test"] = to_add
            else:
                # The file we are testing is not into the database.

                # We add the file and its to_test information into the database.
                self.database_content.update({self.filename: {"to_test": to_add}})

            # We format the list to test in order to avoid duplicate.
            self.database_content[self.filename]["to_test"] = List(
                self.database_content[self.filename]["to_test"]
            ).format()

            # And we finally backup the database.
            self._backup()

    def initiate(self):
        """
        Initiate the databse.
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

            if self.filename in self.database_content:
                # The file we are testing is into the database.

                for data in self.database_content[self.filename]:
                    # We loop through the database content related to the file we
                    # are testing.

                    if data != "to_test":
                        # The currently read index is not `to_test`.

                        if int(PyFunceble.time()) > int(data) + self.days_in_seconds:
                            # The currently read index is older than the excepted time
                            # for retesting.

                            # We extend our result variable with the content from the
                            # currently read index.
                            result.extend(self.database_content[self.filename][data])

                            # And we append the currently read index into the list of
                            # index to delete.
                            to_delete.append(data)

                # We remove all indexes which are present into the list of index to delete.
                Dict(self.database_content[self.filename]).remove_key(to_delete)

                # And we append our list of element to retest into the `to_test` index.s
                self._add_to_test(result)
            else:
                # The file we are testing is not into the database.

                # We add the file we are testing into the database.
                self.database_content.update({self.filename: {}})

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
                self.filename in self.database_content
                and self.database_content[self.filename]
            ):
                # The file we are testing is into the database and its content
                # is not empty.

                # We get the indexes of the current file (in the dabase).
                database_keys = [
                    x
                    for x in self.database_content[self.filename].keys()
                    if x.isdigit()
                ]

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

    def add(self, subject):
        """
        Add the given subject into the database.

        :param subject: The subject we are working with.
        :type subject: str
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            # We get the timestamp to use as index.
            timestamp = str(self._timestamp())

            if self.filename in self.database_content:
                # * The file path is not into the database.

                if timestamp in self.database_content[self.filename]:
                    # The timetamp is already into the database related to the file we
                    # are testing.

                    if subject not in self.database_content[self.filename][timestamp]:
                        # The currently tested element is not into the database related
                        # to the file we are testing.

                        # We append the currently tested element into the database.
                        self.database_content[self.filename][timestamp].append(subject)
                else:
                    # The timetamp is not into the database related to the file we
                    # are testing.

                    # We append the index and the database element into the databse
                    # related to the file we are testing.
                    self.database_content[self.filename].update({timestamp: [subject]})

                if (
                    "to_test" in self.database_content[self.filename]
                    and subject in self.database_content[self.filename]["to_test"]
                ):
                    # * The `to_test` index is into the database related to the file we
                    #   are testing.
                    # and
                    # * The element we are testing is into the `to_test` index related to
                    #   the file we are testing.

                    # We remove the element from the list of element to test.
                    self.database_content[self.filename]["to_test"].remove(subject)
            else:
                # The file path is not into the database.

                # We initiate the file path and its content into the database.
                self.database_content = {self.filename: {timestamp: [subject]}}

            # And we save the data into the database.
            self._backup()

    def remove(self, subject):
        """
        Remove all occurence of the given subject from the database.

        :param subject: The subject we are working with.
        :type subject: str
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            if self.filename in self.database_content:
                #  The file path is into the database.

                for data in self.database_content[self.filename]:
                    # We loop through the index of the file database.

                    if subject in self.database_content[self.filename][data]:
                        # The currently tested element into the currently read index.

                        # We remove the currently tested element from the read index.
                        self.database_content[self.filename][data].remove(subject)

            # And we save the data into the database.
            self._backup()

    def is_present(self, subject):
        """
        Check if the currently tested element is into the database.

        :param subject: The subject we are working with.
        :type subject: str
        """

        if PyFunceble.CONFIGURATION["inactive_database"]:
            # The database subsystem is activated.

            if (
                subject not in self.is_subject_present_cache
                and self.filename in self.database_content
            ):

                for element in [
                    x
                    for x in self.database_content[self.filename].keys()
                    if x.isdigit()
                ]:
                    if (
                        subject in self.database_content[self.filename][element]
                        or subject in self.database_content[self.filename]["to_test"]
                    ):
                        self.is_subject_present_cache[subject] = True
                        break
                    else:
                        self.is_subject_present_cache[subject] = False
                        continue

            if subject not in self.is_subject_present_cache:
                self.is_subject_present_cache[subject] = False

            return self.is_subject_present_cache[subject]
        return False


class Whois:
    """
    Logic behind the whois database. Indeed, the idea is to implement #2.

    :param subject: The subject we are working with.
    :type subject: str

    :param expiration_date: The extracted expiration date.
    :type expiration_date: str

    :param filename: The name of the file we are working with.
    :type filename: str
    """

    def __init__(self, subject, expiration_date=None, filename=None):
        # We share the subject.
        self.subject = subject
        # We share the filename.
        self.filename = filename

        if self._authorization():
            # We are authorized to run this submodule.

            # We get the extracted expiration date.
            self.expiration_date = expiration_date

            if self.expiration_date:
                # We get the epoch of the expiration date.
                self.epoch = int(
                    PyFunceble.mktime(
                        PyFunceble.strptime(self.expiration_date, "%d-%b-%Y")
                    )
                )

            if not self.filename:
                self.filename = "single_testing"

            # We set the path to the whois database file.
            self.whois_db_path = (
                PyFunceble.CURRENT_DIRECTORY
                + PyFunceble.OUTPUTS["default_files"]["whois_db"]
            )

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

        if self._authorization() and "whois_db" not in PyFunceble.INTERN:
            # The usage of the whois database is activated.

            if PyFunceble.path.isfile(self.whois_db_path):
                # The database file exist.

                # We merge our current database into already initiated one.
                PyFunceble.INTERN["whois_db"] = Dict().from_json(
                    File(self.whois_db_path).read()
                )
            else:
                # The database file does not exist.

                # We initiate an empty database.
                PyFunceble.INTERN["whois_db"] = {}

    def _backup(self):
        """
        Backup the database into its file.
        """

        if self._authorization():
            # We are authorized to work.

            # We backup the current state of the datbase.
            Dict(PyFunceble.INTERN["whois_db"]).to_json(self.whois_db_path)

    def is_in_database(self):
        """
        Check if the element is into the database.
        """

        if (
            self._authorization()
            and self.filename in PyFunceble.INTERN["whois_db"]
            and self.subject in PyFunceble.INTERN["whois_db"][self.filename]
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
            and int(PyFunceble.INTERN["whois_db"][self.filename][self.subject]["epoch"])
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
            result = PyFunceble.INTERN["whois_db"][self.filename][self.subject][
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
                    != PyFunceble.INTERN["whois_db"][self.filename][self.subject][
                        "epoch"
                    ]
                ):
                    # The given epoch is diffent from the one saved.

                    # We update it.
                    PyFunceble.INTERN["whois_db"][self.filename][self.subject].update(
                        {
                            "epoch": str(self.epoch),
                            "state": state,
                            "expiration_date": self.expiration_date,
                        }
                    )

                elif self.is_time_older():
                    # The expiration date from the database is in the past.

                    if (
                        PyFunceble.INTERN["whois_db"][self.filename][self.subject][
                            "state"
                        ]
                        != "past"
                    ):  # pragma: no cover
                        # The state of the element in the datbase is not
                        # equal to `past`.

                        # We update it to `past`.
                        PyFunceble.INTERN["whois_db"][self.filename][
                            self.subject
                        ].update({"state": "past"})
                elif (
                    PyFunceble.INTERN["whois_db"][self.filename][self.subject]["state"]
                    != "future"
                ):
                    # * The expiration date from the database is in the future.
                    # and
                    # * The state of the element in the database is not
                    # equal to `future`.

                    # We update it to `future`.
                    PyFunceble.INTERN["whois_db"][self.filename][self.subject].update(
                        {"state": "future"}
                    )
            else:
                # The element we are working with is not in the database.

                if not self.filename in PyFunceble.INTERN["whois_db"]:
                    # The file path is not in the database.

                    # We initiate it.
                    PyFunceble.INTERN["whois_db"][self.filename] = {}

                # We create the first dataset.
                PyFunceble.INTERN["whois_db"][self.filename].update(
                    {
                        self.subject: {
                            "epoch": str(self.epoch),
                            "state": state,
                            "expiration_date": self.expiration_date,
                        }
                    }
                )

            # We do a safety backup of our database.
            self._backup()
