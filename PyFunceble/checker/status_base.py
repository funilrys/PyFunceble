"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all our status classes.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022 Nissar Chababy

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

import dataclasses
import datetime
from typing import Optional

from PyFunceble.checker.complex_json_encoder import ComplexJsonEncoder
from PyFunceble.checker.params_base import CheckerParamsBase
from PyFunceble.helpers.dict import DictHelper


@dataclasses.dataclass
class CheckerStatusBase:
    """
    Provides the base of all status classes.
    """

    subject: Optional[str] = None
    idna_subject: Optional[str] = None
    netloc: Optional[str] = None

    status: Optional[str] = None
    status_source: Optional[str] = None

    tested_at: Optional[datetime.datetime] = None

    params: Optional[CheckerParamsBase] = None

    def to_dict(self) -> dict:
        """
        Converts the current object to dict.
        """

        return {
            x: y if not hasattr(y, "to_dict") else y.to_dict()
            for x, y in self.__dict__.items()
            if not x.startswith("__")
        }

    def to_json(self) -> str:
        """
        Converts the current object to JSON.
        """

        return DictHelper(self.to_dict()).to_json(own_class=ComplexJsonEncoder)
