"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our hashes and position tracker.

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

import PyFunceble


class HashesTracker:
    """
    Provides our hashes and position tracker.
    """

    tracker = dict()

    def __init__(self, filename):
        self.filename = filename

        self.tracker[filename] = dict()

        if self.authorized:
            self.hashes_file = (
                PyFunceble.CONFIG_DIRECTORY
                + PyFunceble.abstracts.Infrastructure.HASHES_FILENAME
            )

            PyFunceble.LOGGER.debug(f"Hashes file: {self.hashes_file}")

            self.load()
            self.__set_current_hash()
            self.__reset_if_changed()

    @property
    def authorized(self):
        """
        Provides the execution authorization.
        """

        return PyFunceble.CONFIGURATION.auto_continue

    def load(self):
        """
        Loads the hash file content.
        """

        file_destination = PyFunceble.helpers.File(self.hashes_file)

        if self.authorized and file_destination.exists():
            self.tracker = PyFunceble.helpers.Dict.from_json_file(file_destination.path)

            if self.filename not in self.tracker:
                self.tracker[self.filename] = dict()

            PyFunceble.LOGGER.info(f"Loaded {self.hashes_file!r} in memory.")

    def save(self):
        """
        Saves the current tracker into its file.
        """

        if self.authorized:
            PyFunceble.helpers.Dict(self.tracker).to_json_file(self.hashes_file)

            PyFunceble.LOGGER.info(f"Saved tracked into {self.hashes_file!r}.")

    def __set_current_hash(self):
        """
        Provides the hash of the current file.

        :rtype: str
        """

        if self.authorized:
            hash_datetime = datetime.utcnow().isoformat()

            hashes = PyFunceble.helpers.Hash().file(self.filename)

            self.tracker[self.filename]["latest"] = {
                "datetime_iso": hash_datetime,
                "hash": hashes,
            }

            if "base" not in self.tracker[self.filename]:
                self.tracker[self.filename]["base"] = {
                    "datetime_iso": hash_datetime,
                    "hash": hashes,
                }

            self.save()

            return hashes
        return None

    def hash_changed(self):
        """
        Checks if the current hash is different than our base one.

        :rtype: bool
        """

        if self.authorized:
            return (
                self.tracker[self.filename]["base"]["hash"]
                != self.tracker[self.filename]["latest"]["hash"]
            )
        return False

    def add_position(self, position):
        """
        Adds the given position to the previous one.
        """

        if self.authorized:
            try:
                self.tracker[self.filename]["position"] += position
            except KeyError:
                self.tracker[self.filename]["position"] = position

            self.save()

    def set_position(self, position):
        """
        Sets the position.
        """

        if self.authorized:
            self.tracker[self.filename]["position"] = position

            self.save()

    def get_position(self):
        """
        Provides the saved position.
        """

        try:
            return self.tracker[self.filename]["position"]
        except KeyError:
            return 0

    def reset_position(self):
        """
        Resets the position.
        """

        if self.authorized:
            self.set_position(0)

    def __reset_if_changed(self):
        """
        Resets the hashes.
        """

        if self.authorized and self.hash_changed():
            self.tracker[self.filename]["base"] = self.tracker[self.filename][
                "latest"
            ].copy()

            self.reset_position()

            self.save()
