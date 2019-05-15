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

This submodule will provide the whois database logic and interface.

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
# pylint: disable=line-too-long

import PyFunceble
from PyFunceble.helpers import Dict, File


class WhoisDB:
    """
    Provide the WHOIS database interface and logic.
    """

    database = {}

    database_file = None
    authorized = False

    def __init__(self):
        # Get the authorization.
        self.authorized = self.authorization()

        # We set the location of the database file.
        self.database_file = "{0}{1}".format(
            PyFunceble.CURRENT_DIRECTORY,
            PyFunceble.OUTPUTS["default_files"]["whois_db"],
        )

        # We load the configuration.
        self.load()

    def __contains__(self, index):
        if index in self.database:
            return True
        return False

    def __getitem__(self, index):
        if index in self.database:
            return self.database[index]

        return None

    def __setitem__(self, index, value):
        actual_value = self[index]

        if isinstance(actual_value, dict):
            if isinstance(value, dict):
                self.database[index].update(value)
            else:  # pragma: no cover
                self.database[index] = value
        elif isinstance(actual_value, list):
            if isinstance(value, list):  # pragma: no cover
                self.database[index].extend(value)
            else:  # pragma: no cover
                self.database[index].append(value)
        else:
            self.database[index] = value

    @classmethod
    def authorization(cls):
        """
        Provide the operation authorization.
        """

        return (
            not PyFunceble.CONFIGURATION["no_whois"]
            and PyFunceble.CONFIGURATION["whois_database"]
        )

    @classmethod
    def merge(cls, old):  # pragma: no cover
        """
        Merge the older version of the database into the new version.

        :param dict old: The old version of the database.


        :return: The database in the new format.
        :rtype: dict
        """

        # We initiate a local place to save our results.
        result = {}

        for index, data in old.items():
            # We loop through all indexes and data of the database.

            if isinstance(data, dict) and "epoch" in data:
                # The epoch index is present into the currently
                # read dataset.

                # We create the copy of the dataset for our result.
                result[index] = data

                continue
            elif isinstance(data, dict):
                # The read data is a dict.

                # We save the content of of the currently read dataset
                # into the upstream index.
                result.update(data)

        # We return the result.
        return result

    def load(self):
        """
        Load the database file into the database.
        """

        if self.authorized and PyFunceble.path.isfile(self.database_file):
            # * We are authorized to operate.
            # and
            # * The database file exists.

            # We merge our current database into already initiated one.
            self.database.update(
                self.merge(Dict().from_json(File(self.database_file).read()))
            )

            # As changes can happen because of the merging, we directly saved
            # the loaded data.
            self.save()

    def save(self):
        """
        Save the database into the database file.
        """

        if self.authorized:
            # We are authorized to operate.

            # We save the current state of the datbase.
            Dict(self.database).to_json(self.database_file)

    def is_time_older(self, subject):
        """
        Check if the expiration time of the given subject is
        older.

        :param str subject: The subject we are working with.

        .. note::
            Of course, we imply that the subject is in the database.
        """

        data = self[subject]

        return (
            self.authorized
            and data
            and "epoch" in data
            and int(data["epoch"]) < int(PyFunceble.time())
        )

    def get_expiration_date(self, subject):
        """
        Get the expiration date of the given subject.

        :param str subject: The subject we are working with.

        :return: The expiration date from the database.
        :rtype: str|None
        """

        if self.authorized and self[subject] and not self.is_time_older(subject):
            # * We are authorized to work.
            # and
            # * The element we are testing is in the database.
            # and
            # * The expiration date is in the future.

            try:
                # We return the expiration date.
                return self[subject]["expiration_date"]
            except KeyError:  # pragma: no cover
                pass

        # We return None, there is no data to work with.
        return None

    def add(self, subject, expiration_date):
        """
        Add the given subject and expiration date to the database.

        :param str subject: The subject we are working with.
        :param str expiration_date: The extracted expiration date.
        """

        if self.authorized and expiration_date:
            # * We are authorized to operate.
            # and
            # * The expiration date is not empty nor None.

            # We initiate what we are going to save into the database
            data = {
                "epoch": int(
                    PyFunceble.mktime(PyFunceble.strptime(expiration_date, "%d-%b-%Y"))
                ),
                "expiration_date": expiration_date,
            }

            if data["epoch"] < int(PyFunceble.time()):
                # We compare the epoch with the current time.

                # We set the state.
                data["state"] = "past"
            else:
                # We set the state.
                data["state"] = "future"

            # We save everything into the database.
            self[subject] = data

            # We save everything.
            self.save()
