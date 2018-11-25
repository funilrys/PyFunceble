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

This submodule will give us the mining interface and logic.

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
import urllib3.exceptions as urllib3_exceptions

import PyFunceble
from PyFunceble.check import Check
from PyFunceble.helpers import Dict, File, List


class Mining:
    """
    Manage the minig subsystem.
    """

    def __init__(self):  # pragma: no cover
        if (
            "to_test" in PyFunceble.CONFIGURATION
            and PyFunceble.CONFIGURATION["to_test"]
        ):
            # There is something to test.

            if PyFunceble.CONFIGURATION["to_test_type"] == "domain":
                # We are testing a domain.

                # We set a variable which will save the actual element we are working with.
                self.to_get = "http://%s:80" % PyFunceble.CONFIGURATION["to_test"]
                self.to_get_bare = PyFunceble.CONFIGURATION["to_test"]
            elif PyFunceble.CONFIGURATION["to_test_type"] == "url":
                # We are testing an URL.

                # We set a variable which will save the actual element we are working with.
                self.to_get = PyFunceble.CONFIGURATION["to_test"]
                self.to_get_bare = PyFunceble.CONFIGURATION["to_test"]
            else:
                raise Exception("Unknow test type.")

        if PyFunceble.CONFIGURATION["user_agent"]:
            # The user-agent is given.

            # We append the user agent to the header we are going to parse with
            # the request.
            self.headers = {"User-Agent": PyFunceble.CONFIGURATION["user_agent"]}
        else:
            # The user-agent is not given or is empty.

            # We return an empty header.
            self.headers = {}

        # We get the file we are going to save our data.
        self.file = (
            PyFunceble.CURRENT_DIRECTORY + PyFunceble.OUTPUTS["default_files"]["mining"]
        )

        # We get the file path of the list we are testing.
        self.tested_file_path = PyFunceble.CONFIGURATION["file_to_test"]

        if "mined" not in PyFunceble.CONFIGURATION:
            # The mined index is not into the configuration informations.

            # We initiate it.
            self._retrieve()

            # We backup everything.
            self._backup()

    def mine(self):  # pragma: no cover
        """
        Search for domain or URL related to the original URL or domain.

        :return: The mined domains or URL.
        :rtype: dict
        """

        if PyFunceble.CONFIGURATION["mining"]:
            # The mining is activated.

            try:
                # We get the history.
                history = PyFunceble.requests.get(
                    self.to_get,
                    timeout=PyFunceble.CONFIGURATION["seconds_before_http_timeout"],
                    headers=self.headers,
                ).history

                # We initiate a dictionnary which will save the
                # list of mined links.
                mined = {self.to_get_bare: []}

                for element in history:
                    # We loop through the history.

                    # We update the element.
                    element = element.url

                    if PyFunceble.CONFIGURATION["to_test_type"] == "url":
                        # We are testing a full url.

                        # We get the element to append.
                        to_append = Check().is_url_valid(element, return_base=False)
                    elif PyFunceble.CONFIGURATION["to_test_type"] == "domain":
                        # We are testing a domain.

                        # We get the element to append.
                        to_append = Check().is_url_valid(element, return_base=True)
                    else:
                        raise Exception("Unknown tested.")

                    if to_append:
                        # There is something to append.

                        if to_append.endswith(":80"):
                            # The port is present.

                            # We get rid of it.
                            to_append = to_append[:-3]

                        if to_append != self.to_get_bare:
                            # The element to append is different as
                            # the element we are globally testing.

                            # We append the element to append to the
                            # list of mined links.
                            mined[self.to_get_bare].append(to_append)

                if mined[self.to_get_bare]:
                    # There is something in the list of mined links.

                    # We return the whole element.
                    return mined

                # There is nothing in the list of mined links.

                # We return None.
                return None

            except (
                PyFunceble.requests.ConnectionError,
                PyFunceble.requests.exceptions.Timeout,
                PyFunceble.requests.exceptions.InvalidURL,
                PyFunceble.socket.timeout,
                urllib3_exceptions.InvalidHeader,
                UnicodeDecodeError,  # The probability that this happend in production is minimal.
            ):
                # Something went wrong.

                # We return None.
                return None
        return None

    def _retrieve(self):
        """
        Retrieve the mining informations.
        """

        if PyFunceble.CONFIGURATION["mining"]:
            # The mining is activated.

            if "mined" not in PyFunceble.CONFIGURATION:
                PyFunceble.CONFIGURATION["mined"] = {}

            if PyFunceble.path.isfile(self.file):
                # Our backup file exist.

                # We return the information from our backup.
                data = Dict().from_json(File(self.file).read())

                # We clean the empty elements.
                for file_path in data:
                    PyFunceble.CONFIGURATION["mined"][file_path] = {}

                    for element in data[file_path]:
                        if data[file_path][element]:
                            PyFunceble.CONFIGURATION["mined"][file_path][
                                element
                            ] = data[file_path][element]

                return
        # * The mining is not activated.
        # or
        # * Our backup file does not exist.

        # We return nothing.
        PyFunceble.CONFIGURATION["mined"] = {}

        return

    def _backup(self):
        """
        Backup the mined informations.
        """

        if PyFunceble.CONFIGURATION["mining"]:
            # The mining is activated.

            # We backup our mined informations.
            Dict(PyFunceble.CONFIGURATION["mined"]).to_json(self.file)

    def _add(self, to_add):
        """
        Add the currently mined information to the
        mined "database".

        :param to_add: The element to add.
        :type to_add: dict
        """

        if PyFunceble.CONFIGURATION["mining"]:
            # The mining is activated.

            if self.tested_file_path not in PyFunceble.CONFIGURATION["mined"]:
                # Our tested file path is not into our mined database.

                # We initiate it.
                PyFunceble.CONFIGURATION["mined"][self.tested_file_path] = {}

            for element in to_add:
                # We loop through the element to add.

                if element in PyFunceble.CONFIGURATION["mined"][self.tested_file_path]:
                    # The element is already into the tested file path database.

                    # We extent it with our element to add.
                    PyFunceble.CONFIGURATION["mined"][self.tested_file_path][
                        element
                    ].extend(to_add[element])
                else:
                    # The element is already into the tested file path database.

                    # We initiate it.
                    PyFunceble.CONFIGURATION["mined"][self.tested_file_path][
                        element
                    ] = to_add[element]

                # We format the added information in order to avoid duplicate.
                PyFunceble.CONFIGURATION["mined"][self.tested_file_path][
                    element
                ] = List(
                    PyFunceble.CONFIGURATION["mined"][self.tested_file_path][element]
                ).format()

            # We backup everything.
            self._backup()

    def remove(self):
        """
        Remove the currently tested element from the mining
        data.
        """

        if PyFunceble.CONFIGURATION["mining"]:
            # The mining is activated.

            if self.tested_file_path in PyFunceble.CONFIGURATION["mined"]:
                # The currently tested file is in our mined database.

                for element in PyFunceble.CONFIGURATION["mined"][self.tested_file_path]:
                    # We loop through the mined index.

                    if (
                        self.to_get_bare
                        in PyFunceble.CONFIGURATION["mined"][self.tested_file_path][
                            element
                        ]
                    ):
                        # The currently read element content.

                        # We remove the globally tested element from the currently
                        # read element content.
                        PyFunceble.CONFIGURATION["mined"][self.tested_file_path][
                            element
                        ].remove(self.to_get_bare)

                # We backup everything.
                self._backup()

    def list_of_mined(self):
        """
        Provide the list of mined so they can be added to the list
        queue.

        :return: The list of mined domains or URL.
        :rtype: list
        """

        # We initiate a variable which will return the result.
        result = []

        if PyFunceble.CONFIGURATION["mining"]:
            # The mining is activated.

            if self.tested_file_path in PyFunceble.CONFIGURATION["mined"]:
                # The file we are testing is into our mining database.

                for element in PyFunceble.CONFIGURATION["mined"][self.tested_file_path]:
                    # We loop through the list of index of the file we are testing.

                    # We append the element of the currently read index to our result.
                    result.extend(
                        PyFunceble.CONFIGURATION["mined"][self.tested_file_path][
                            element
                        ]
                    )

                # We format our result.
                result = List(result).format()

        # We return the result.
        return result

    def process(self):  # pragma: no cover
        """
        Process the logic and structuration of the mining database.
        """

        if PyFunceble.CONFIGURATION["mining"]:
            # The mining is activated.

            # We load the mining logic.
            mined = self.mine()

            if mined:
                # The mined data is not empty or None.

                # We add the mined data to the global database.
                self._add(mined)

                # And we finally backup everything.
                self._backup()
