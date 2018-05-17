#!/usr/bin/env python3

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the autosave logic and interface.


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on 13th March, 2018.

Its main objective is to get and the return domains and IPs availability by
generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

In its daily usage, PyFunceble is mostly used to clean `hosts` files or blocklist.
Indeed, it is possible because PyFunceble generates a list of all `ACTIVE` domains
or IPs but in the same time, it creates by default a database of the `INACTIVE`
domains or IPs so we can retest them overtime automatically at the next execution.

PyFunceble is running actively and daily with the help of Travis CI under 60+
repositories. It is used to clean or test the availability of data which are
present in hosts files, list of IP, list of domains, blocklists or even AdBlock
filter lists.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
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
