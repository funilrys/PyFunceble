"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our producer worker.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from typing import Any, Optional, Tuple

import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.checker.status_base import CheckerStatusBase
from PyFunceble.cli.processes.workers.producer import ProducerWorker


class ChancyProducerWorker(ProducerWorker):
    """
    Provides our chancy producer worker.

    .. warning::
        This chancy producer does not provide any guarantee. The flow that keep
        PyFunceble safe are here unleashed.

        USE AT YOUR OWN RISK. GOOD LUCK!
    """

    STD_NAME: str = "pyfunceble_chancy_producer_worker"

    def target(self, consumed: Any) -> Optional[Tuple[Any, ...]]:
        if not isinstance(consumed, tuple):
            PyFunceble.facility.Logger.info(
                "Skipping latest dataset because consumed data was not a tuple."
            )
            return None

        # Just for human brain.
        test_dataset, test_result = consumed

        if not isinstance(test_dataset, dict):
            PyFunceble.facility.Logger.info(
                "Skipping because test dataset is not a dictionnary."
            )
            return None

        if self.should_we_ignore(test_result):
            PyFunceble.facility.Logger.info(
                "Ignored test dataset. Reason: No output wanted."
            )
            return None

        if not isinstance(test_result, CheckerStatusBase):
            PyFunceble.facility.Logger.info(
                "Skipping latest dataset because consumed status is not "
                "a status object.."
            )
            return None

        self.run_whois_backup(test_result)
        self.run_inactive_backup(test_dataset, test_result)
        self.run_continue_backup(test_dataset, test_result)

        if not self.should_we_block_status_file_printer(test_dataset, test_result):
            self.run_counter(test_dataset, test_result)

        test_dataset["from_chancy_producer"] = True

        return test_dataset, test_result
