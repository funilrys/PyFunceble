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

This submodule will provide the auto-continue logic.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/contributors.html

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

import PyFunceble
from PyFunceble.helpers import Dict, File


class AutoContinue:
    """
    Provide the auto-continue subsystem.
    """

    # Save the content of the database.
    database = {}
    # Save the database file
    database_file = None
    # Save the operation authorization.
    authorized = False

    # Save the filename we are working with.
    filename = None

    def __init__(self, filename):
        # We get the operation authorization.
        self.authorized = self.authorization()
        # We share the filename.
        self.filename = filename
        # We preset the filename namespace.
        self.database[self.filename] = {}

        if self.authorized:
            # We are authorized to operate.

            # We set the location of the database file.
            self.database_file = (
                PyFunceble.OUTPUT_DIRECTORY
                + PyFunceble.OUTPUTS["parent_directory"]
                + PyFunceble.OUTPUTS["logs"]["filenames"]["auto_continue"]
            )

            # We load the backup (if existant).
            self.load()

    def __contains__(self, index):
        if index in self.database[self.filename]:
            if self.database[self.filename][index] in [
                PyFunceble.STATUS["official"]["up"],
                PyFunceble.STATUS["official"]["valid"],
            ]:
                PyFunceble.INTERN["counter"]["number"]["up"] += 1
            elif self.database[self.filename][index] in [
                PyFunceble.STATUS["official"]["down"]
            ]:
                PyFunceble.INTERN["counter"]["number"]["down"] += 1
            elif self.database[self.filename][index] in [
                PyFunceble.STATUS["official"]["invalid"]
            ]:
                PyFunceble.INTERN["counter"]["number"]["invalid"] += 1

            PyFunceble.INTERN["counter"]["number"]["tested"] += 1
            return True

        return False

    @classmethod
    def authorization(cls):
        """
        Provide the execution authorization.
        """

        return (
            PyFunceble.CONFIGURATION["auto_continue"]
            and not PyFunceble.CONFIGURATION["no_files"]
        )

    def is_empty(self):
        """
        Check if the database related to the currently tested
        file is emtpy.
        """

        if self.filename not in self.database or not self.database[self.filename]:
            return True
        return False

    def add(self, element, status):
        """
        Add the given element into the database.
        """

        if self.authorized:
            # We are authorized to operate.

            if self.filename in self.database:
                # We already have something related
                # to the file we are testing.

                # We set the new data.
                self.database[self.filename][element] = status
            else:
                # We set the new data.
                self.database[self.filename] = {element: status}

            # We save everything.
            self.save()

    def save(self):
        """
        Save the current state of the database.
        """

        if self.authorized:
            # We are authoried to operate.

            if PyFunceble.path.isfile(self.database_file):
                # The database file exists.

                # We merge the current content of the
                # database file with the current state
                # of the database.
                Dict(
                    Dict(self.database).merge(
                        Dict.from_json(File(self.database_file).read())
                    )
                ).to_json(self.database_file)
            else:
                # The database file do not exists.

                # We save the current database state.
                Dict(self.database).to_json(self.database_file)

    def load(self):
        """
        Load previously saved database.
        """

        if self.authorized:
            # We are authorized to operate.

            if PyFunceble.path.isfile(self.database_file):
                # The database file exists.

                # We get its content and save it inside backup_content.
                self.database = Dict().from_json(File(self.database_file).read())
            else:
                # The database file do not exists.

                # We initiate an empty database.
                self.database = {self.filename: {}}

    def clean(self):
        """
        Clean the database.
        """

        if self.authorized:
            # We are authorized to operate.

            # We empty the database.
            self.database[self.filename] = {}

            # And we save the current database state.
            Dict(self.database).to_json(self.database_file)
