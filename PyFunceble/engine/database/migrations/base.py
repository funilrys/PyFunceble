"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of our very own migration logic.

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


from datetime import datetime
from multiprocessing import active_children

import PyFunceble


class MigrationaBase:
    """
    Provides the base of all our (own) migration logic.
    """

    def __init__(self):
        self.autosave = PyFunceble.engine.AutoSave()

    def write_file_for_autocontinue(self):
        """
        Writes a file in order to force the CI engine to continue.
        """

        if self.autosave.authorized:
            # Ensure that the output directory exist.
            PyFunceble.output.Constructor()
            with open(
                f"{PyFunceble.OUTPUT_DIRECTORY}"
                f"{PyFunceble.abstracts.Infrastructure.CI_MIGRATION_TRIGGER_FILE}",
                "w",
                encoding="utf-8",
            ) as file_stream:
                file_stream.write(datetime.utcnow().isoformat())

    @classmethod
    def wait_for_all_process_to_finish(cls):
        """
        Wait until all migration process finished.
        """

        if PyFunceble.CONFIGURATION.multiprocess:
            while "Migration" in " ".join(
                [x.name for x in reversed(active_children())]
            ):
                continue

    def handle_autosaving(self):
        """
        Handles the autosaving.
        """

        if self.autosave.is_time_exceed():
            self.wait_for_all_process_to_finish()
            self.write_file_for_autocontinue()
            self.autosave.process()
