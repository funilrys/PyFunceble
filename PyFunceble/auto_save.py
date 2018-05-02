#!/usr/bin/env python3

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will create the auto-save logic.


PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on March 13th, 2018.
At the end of 2017, PyFunceble was described by one of its most active user as:
"[an] excellent script for checking ACTIVE and INACTIVE domain names."

Our main objective is to test domains and IP availability
by generating an accurate result based on results from WHOIS, NSLOOKUP and
HTTP status codes.
As result, PyFunceble returns 3 status: ACTIVE, INACTIVE and INVALID.
The denomination of those statuses can be changed under your personal
`config.yaml`.

At the time we write this, PyFunceble is running actively and daily under 50+
Travis CI repository or process to test the availability of domains which are
present into hosts files, AdBlock filter lists, list of IP, list of domains or
blocklists.

An up to date explanation of all status can be found at https://git.io/vxieo.
You can also find a simple representation of the logic behind PyFunceble at
https://git.io/vxifw.

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
from PyFunceble import directory_separator, strftime
from PyFunceble.helpers import Command
from PyFunceble.percentage import Percentage


class AutoSave(object):  # pragma: no cover  # pylint: disable=too-few-public-methods
    """
    Logic behind autosave.

    Arguments:
        - is_last_domain: bool
            Tell the autosave logic if we are at the end.
        - is_bypass: bool
            Tell the autosave logic if we are in bypass mode.
    """

    def __init__(self, is_last_domain=False, is_bypass=False):
        if PyFunceble.CONFIGURATION["travis"]:
            self.last = is_last_domain
            self.bypass = is_bypass
            self._travis()

    @classmethod
    def travis_permissions(cls):
        """
        Set permissions in order to avoid issues before commiting.
        """
        try:
            build_dir = PyFunceble.environ["TRAVIS_BUILD_DIR"]
            commands = [
                "sudo chown -R travis:travis %s" % (build_dir),
                "sudo chgrp -R travis %s" % (build_dir),
                "sudo chmod -R g+rwX %s" % (build_dir),
                "sudo chmod 777 -Rf %s.git" % (build_dir + directory_separator),
                r"sudo find %s -type d -exec chmod g+x '{}' \;" % (build_dir),
            ]

            for command in commands:
                Command(command).execute()

            if Command("git config core.sharedRepository").execute() == "":
                Command("git config core.sharedRepository group").execute()
        except KeyError:
            pass

    def _travis(self):
        """
        Logic behind travis autosave.
        """

        current_time = int(strftime("%s"))
        time_autorisation = False

        try:
            time_autorisation = current_time >= int(
                PyFunceble.CONFIGURATION["start"]
            ) + (
                int(PyFunceble.CONFIGURATION["travis_autosave_minutes"]) * 60
            )
        except KeyError:
            if self.last and not self.bypass:
                raise Exception("Please review the way `ExecutionTime()` is called.")

        if self.last or time_autorisation or self.bypass:
            Percentage().log()
            self.travis_permissions()

            command = 'git add --all && git commit -a -m "%s"'

            if self.last or self.bypass:
                if PyFunceble.CONFIGURATION["command_before_end"]:
                    Command(PyFunceble.CONFIGURATION["command_before_end"]).execute()

                message = PyFunceble.CONFIGURATION[
                    "travis_autosave_final_commit"
                ] + " [ci skip]"

                Command(command % message).execute()
            else:
                Command(
                    command % PyFunceble.CONFIGURATION["travis_autosave_commit"]
                ).execute()

            Command(
                "git push origin %s" % PyFunceble.CONFIGURATION["travis_branch"]
            ).execute()
            exit(0)
