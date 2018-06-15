#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check domains or IP availability.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

This submodule will provide the autosave logic and interface.

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
from PyFunceble import path
from PyFunceble.helpers import Dict, File


class AutoContinue(object):
    """
    Autocontinue logic/subsystem.
    """

    def __init__(self):
        if PyFunceble.CONFIGURATION["auto_continue"]:
            self.autocontinue_log_file = PyFunceble.CURRENT_DIRECTORY + PyFunceble.OUTPUTS[
                "parent_directory"
            ] + PyFunceble.OUTPUTS[
                "logs"
            ][
                "filenames"
            ][
                "auto_continue"
            ]

            if path.isfile(self.autocontinue_log_file):
                self.backup_content = Dict().from_json(
                    File(self.autocontinue_log_file).read()
                )
            else:
                self.backup_content = {}
                File(self.autocontinue_log_file).write(str(self.backup_content))

    def backup(self):
        """
        Backup the current execution state.
        """

        if PyFunceble.CONFIGURATION["auto_continue"]:
            data_to_backup = {}
            configuration_counter = PyFunceble.CONFIGURATION["counter"]["number"]

            data_to_backup[PyFunceble.CONFIGURATION["file_to_test"]] = {
                "tested": configuration_counter["tested"],
                "up": configuration_counter["up"],
                "down": configuration_counter["down"],
                "invalid": configuration_counter["invalid"],
            }

            to_save = {}

            to_save.update(self.backup_content)
            to_save.update(data_to_backup)

            Dict(to_save).to_json(self.autocontinue_log_file)

    def restore(self):
        """
        Restore data from the given path.
        """

        file_to_restore = PyFunceble.CONFIGURATION["file_to_test"]

        if PyFunceble.CONFIGURATION["auto_continue"] and self.backup_content:
            if file_to_restore in self.backup_content:
                to_initiate = ["up", "down", "invalid", "tested"]

                alternatives = {
                    "up": "number_of_up",
                    "down": "number_of_down",
                    "invalid": "number_of_invalid",
                    "tested": "number_of_tested",
                }

                for string in to_initiate:
                    try:
                        PyFunceble.CONFIGURATION["counter"]["number"].update(
                            {string: self.backup_content[file_to_restore][string]}
                        )
                    except KeyError:
                        PyFunceble.CONFIGURATION["counter"]["number"].update(
                            {
                                string: self.backup_content[file_to_restore][
                                    alternatives[string]
                                ]
                            }
                        )
