"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the auto-save engine.

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

from datetime import datetime, timedelta

import PyFunceble

from .ci import GitLabCI, TravisCI


class AutoSave:  # pragma: no cover  pylint: disable=too-few-public-methods
    """
    Provides the autosave interface.
    """

    # We set the varible which will save the global authorization to operate.
    authorized = None
    # We set the variable which will save the starting time.
    start_time = None
    # We set the variable which will save the end time.
    endtime = None
    # We set the variable which will process as a chache for the
    # time exceeed value.
    time_exceed = False

    def __init__(self, start_time=None):
        self.current_ci_engine = self.get_current_ci()
        PyFunceble.LOGGER.debug(f"Current CI engine: {self.current_ci_engine}")

        if self.current_ci_engine:
            self.authorized = True

            PyFunceble.LOGGER.debug(
                "CI (already) Initiated: %s" % "ci_initiated" not in PyFunceble.INTERN
            )
            if "ci_initiated" not in PyFunceble.INTERN:
                self.current_ci_engine.init()
                self.current_ci_engine.bypass()

                if start_time is None:
                    self.start_time = datetime.now()
                else:
                    self.start_time = datetime.fromtimestamp(int(start_time))

                self.end_time = self.start_time + timedelta(
                    minutes=int(PyFunceble.CONFIGURATION.ci_autosave_minutes)
                )

                PyFunceble.INTERN["auto_save"] = {
                    "start_time": self.start_time.timestamp(),
                    "end_time": self.end_time.timestamp(),
                }

                PyFunceble.LOGGER.debug(f"Start Time: {self.start_time}")
                PyFunceble.LOGGER.debug(f"End Time:  {self.end_time}")

                PyFunceble.INTERN["ci_initiated"] = True
            elif "auto_save" in PyFunceble.INTERN:
                self.start_time = datetime.fromtimestamp(
                    PyFunceble.INTERN["auto_save"]["start_time"]
                )
                self.end_time = datetime.fromtimestamp(
                    PyFunceble.INTERN["auto_save"]["end_time"]
                )

                PyFunceble.LOGGER.debug(f"Start Time (Shared): {self.start_time}")
                PyFunceble.LOGGER.debug(f"End Time (Shared):  {self.end_time}")

    @classmethod
    def get_current_ci(cls):
        """
        Provides the current CI to use.
        """

        for ci_engine in [TravisCI(), GitLabCI()]:
            if ci_engine.authorized:
                return ci_engine

        return None

    def is_time_exceed(self):
        """
        Checks if the end time is exceed.
        """

        if self.authorized and hasattr(self, "end_time"):
            # We are authorized to operate.

            if not self.time_exceed and datetime.now() >= self.end_time:
                # * We did not tested previously if the time exceed.
                # and
                # * The time exceed.

                # We update the time exceed marker.
                self.time_exceed = True
        else:
            self.time_exceed = False

            PyFunceble.LOGGER.debug(f"Time exceed: {self.time_exceed}")

        return self.time_exceed

    def process(self, test_completed=False):
        """
        Processes the autosave base on the current state of the test.

        :param bool test_completed: Tell us if we finished the test.
        """

        if self.authorized:
            # We are authorized to operate.

            if test_completed:
                # The test was completed.

                # We run the end commit.
                self.current_ci_engine.end_commit()
            elif self.is_time_exceed():
                # The current time excessed the minimal time for autosaving.

                # We run the not end commit.
                self.current_ci_engine.not_end_commit()
