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

This submodule will provide the auto-continue logic.

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
import PyFunceble
from PyFunceble.helpers import Dict, File


class AutoContinue:
    """
    Provide the auto-continue subsystem.
    """

    def __init__(self):
        if PyFunceble.CONFIGURATION["auto_continue"]:
            # The auto_continue subsystem is activated.

            # We set the log file location.
            self.autocontinue_log_file = (
                PyFunceble.OUTPUT_DIRECTORY
                + PyFunceble.OUTPUTS["parent_directory"]
                + PyFunceble.OUTPUTS["logs"]["filenames"]["auto_continue"]
            )

            if PyFunceble.path.isfile(self.autocontinue_log_file):
                # The log file already exist.

                # We get its content and save it inside backup_content.
                self.backup_content = Dict().from_json(
                    File(self.autocontinue_log_file).read()
                )
            else:
                # The log file does not exist.

                # We initiate the backup content.
                self.backup_content = {}
                # And we save our empty backup_content to the log file.
                File(self.autocontinue_log_file).write(str(self.backup_content))

    def backup(self):
        """
        Backup the current execution state.
        """

        if PyFunceble.CONFIGURATION["auto_continue"]:
            # The auto_continue subsystem is activated.

            # We initiate the location where we are going to save the data to backup.
            data_to_backup = {}
            # We get the current counter states.
            configuration_counter = PyFunceble.CONFIGURATION["counter"]["number"]

            # We initiate the data we have to backup.
            data_to_backup[PyFunceble.CONFIGURATION["file_to_test"]] = {
                # We backup the number of tested.
                "tested": configuration_counter["tested"],
                # We backup the number of up.
                "up": configuration_counter["up"],
                # We backup the number of down.
                "down": configuration_counter["down"],
                # We backup the number of invalid.
                "invalid": configuration_counter["invalid"],
            }

            # We initiate the final data we have to save.
            # We initiate this variable instead of updating backup_content because
            # we do not want to touch the backup_content.
            to_save = {}

            # We add the backup_content into to_save.
            to_save.update(self.backup_content)
            # And we overwrite with the newly data to backup.
            to_save.update(data_to_backup)

            # Finaly, we save our informations into the log file.
            Dict(to_save).to_json(self.autocontinue_log_file)

    def restore(self):
        """
        Restore data from the given path.
        """

        if PyFunceble.CONFIGURATION["auto_continue"] and self.backup_content:
            # The auto_continue subsystem is activated and the backup_content
            # is not empty.

            # We get the file we have to restore.
            file_to_restore = PyFunceble.CONFIGURATION["file_to_test"]

            if file_to_restore in self.backup_content:
                # The file we are working with is already into the backup content.

                # We initiate the different status to set.
                to_initiate = ["up", "down", "invalid", "tested"]

                # Because at some time it was not the current status, we have to map
                # the new with the old. This way, if someone is running the latest
                # version but with old data, we still continue like nothing happend.
                alternatives = {
                    "up": "number_of_up",
                    "down": "number_of_down",
                    "invalid": "number_of_invalid",
                    "tested": "number_of_tested",
                }

                for string in to_initiate:
                    # We loop over the status we have to initiate.

                    try:
                        # We try to update the counters by using the currently read status.
                        PyFunceble.CONFIGURATION["counter"]["number"].update(
                            {string: self.backup_content[file_to_restore][string]}
                        )
                    except KeyError:
                        # But if the status is not present, we try with the older index
                        # we mapped previously.
                        PyFunceble.CONFIGURATION["counter"]["number"].update(
                            {
                                string: self.backup_content[file_to_restore][
                                    alternatives[string]
                                ]
                            }
                        )
