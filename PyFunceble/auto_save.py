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

This submodule will create the autosave logic.

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
from PyFunceble.helpers import Command
from PyFunceble.percentage import Percentage


class AutoSave:  # pragma: no cover  pylint: disable=too-few-public-methods
    """
    Provide the autosave logic.

    :param is_last_domain:
        Tell this subsystem if we are at the very end of the file testing.
    :type is_last_domain: bool

    :param is_bypass:
        Tell this subsystem if we are in bypassing mode.
    :type is_bypass: bool
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

        if PyFunceble.CONFIGURATION["travis"]:
            try:
                build_dir = PyFunceble.environ["TRAVIS_BUILD_DIR"]
                commands = [
                    "sudo chown -R travis:travis %s" % (build_dir),
                    "sudo chgrp -R travis %s" % (build_dir),
                    "sudo chmod -R g+rwX %s" % (build_dir),
                    "sudo chmod 777 -Rf %s.git"
                    % (build_dir + PyFunceble.directory_separator),
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
        Logic behind autosave under Travis CI.
        """

        if PyFunceble.CONFIGURATION["travis"]:
            try:
                _ = PyFunceble.environ["TRAVIS_BUILD_DIR"]
                time_autorisation = False

                try:
                    time_autorisation = int(PyFunceble.time()) >= int(
                        PyFunceble.CONFIGURATION["start"]
                    ) + (int(PyFunceble.CONFIGURATION["travis_autosave_minutes"]) * 60)
                except KeyError:
                    if self.last and not self.bypass:
                        raise Exception(
                            "Please review the way `ExecutionTime()` is called."
                        )

                if self.last or time_autorisation or self.bypass:
                    Percentage().log()
                    self.travis_permissions()

                    command = 'git add --all && git commit -a -m "%s"'

                    if self.last or self.bypass:
                        if PyFunceble.CONFIGURATION["command_before_end"]:
                            print(
                                Command(
                                    PyFunceble.CONFIGURATION["command_before_end"]
                                ).execute()
                            )

                            self.travis_permissions()

                        message = (
                            PyFunceble.CONFIGURATION["travis_autosave_final_commit"]
                            + " [ci skip]"
                        )

                        Command(command % message).execute()
                    else:
                        if PyFunceble.CONFIGURATION["command"]:
                            print(
                                Command(PyFunceble.CONFIGURATION["command"]).execute()
                            )

                            self.travis_permissions()

                        Command(
                            command % PyFunceble.CONFIGURATION["travis_autosave_commit"]
                        ).execute()

                    Command(
                        "git push origin %s" % PyFunceble.CONFIGURATION["travis_branch"]
                    ).execute()
                    exit(0)
            except KeyError:
                pass
