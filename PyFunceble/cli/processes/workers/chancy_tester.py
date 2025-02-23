"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our chancy tester worker. The chancy tester worker is a worker that
abstract from the standard tester worker. It just get rid of the walls between
some of the component of our data workflow.

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


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024, 2025 Nissar Chababy

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

from PyFunceble.cli.processes.workers.producer import ProducerWorker
from PyFunceble.cli.processes.workers.tester import TesterWorker


class ChancyTesterWorker(TesterWorker):
    """
    Provides our chancy tester worker. The chancy worker breaks the walls
    between some of the core component of our data workflow.

    .. warning::
        This chancy tester does not provide any guarantee. The flow that keep
        PyFunceble safe are here unleashed.

        USE AT YOUR OWN RISK. GOOD LUCK!
    """

    def __post_init__(self) -> None:
        self.producer_worker = ProducerWorker(**self._all_args)
        self.producer_worker.name = f"{self.name}.producer"
        self.producer_worker.perform_external_poweron_checks()

        return super().__post_init__()

    def target(self, consumed: dict) -> Optional[Tuple[Any, ...]]:
        """
        The actually wall destructor.

        :param consumed:
            The data that needs to be tested.
        """

        return self.producer_worker.target(super().target(consumed))
