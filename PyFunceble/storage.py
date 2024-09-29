# pylint:disable=invalid-name, cyclic-import
"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides a central storage place.

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

import os
import secrets
from typing import Optional

from box import Box
from dotenv import load_dotenv

from PyFunceble.storage_facility import get_config_directory

PROJECT_NAME: str = "PyFunceble"
PROJECT_VERSION: str = "4.2.29.dev (Blue Duckling: Tulip)"

DISTRIBUTED_CONFIGURATION_FILENAME: str = ".PyFunceble_production.yaml"

CONFIGURATION_FILENAME: str = ".PyFunceble.yaml"
CONFIGURATION_REMOTE_FILENAME: str = ".PyFunceble.remote.yaml"
ENV_FILENAME: str = ".pyfunceble-env"

# pylint: disable=line-too-long

SHORT_REPO_LINK: str = "https://pyfunceble.github.io"
REPO_LINK: str = "https://github.com/funilrys/PyFunceble"

NOT_RESOLVED_STD_HOSTNAME: str = f"{secrets.token_hex(12)}.mock-resolver.pyfunceble.com"

IANA: Optional[dict] = {}
PUBLIC_SUFFIX: Optional[dict] = {}
USER_AGENTS: Optional[dict] = {}

load_dotenv(".env")
load_dotenv(ENV_FILENAME)

CONFIG_DIRECTORY: str = get_config_directory(
    project_name=PROJECT_NAME, project_version=PROJECT_VERSION
)
load_dotenv(os.path.join(CONFIG_DIRECTORY, ".env"))
load_dotenv(os.path.join(CONFIG_DIRECTORY, ENV_FILENAME))

# This is for the case that the environment variable are telling us something
# else.
CONFIG_DIRECTORY: str = get_config_directory(
    project_name=PROJECT_NAME, project_version=PROJECT_VERSION
)


CONFIGURATION: Optional[Box] = Box({})
FLATTEN_CONFIGURATION: Optional[dict] = {}
STATUS: Optional[Box] = Box(
    {
        "up": "ACTIVE",
        "down": "INACTIVE",
        "valid": "VALID",
        "invalid": "INVALID",
        "malicious": "MALICIOUS",
        "sane": "SANE",
    },
    frozen_box=True,
)
HTTP_CODES: Optional[Box] = Box({})
PLATFORM: Optional[Box] = Box({})
LINKS: Optional[Box] = Box({})
PROXY: Optional[Box] = Box({})


STD_HTTP_CODES: Optional[Box] = Box(
    {
        "list": {
            "up": [
                100,
                101,
                102,
                200,
                201,
                202,
                203,
                204,
                205,
                206,
                207,
                208,
                226,
                429,
            ],
            "potentially_up": [
                300,
                301,
                302,
                303,
                304,
                305,
                307,
                308,
                403,
                405,
                406,
                407,
                408,
                411,
                413,
                417,
                418,
                421,
                422,
                423,
                424,
                426,
                428,
                431,
                500,
                501,
                502,
                503,
                504,
                505,
                506,
                507,
                508,
                510,
                511,
            ],
            "potentially_down": [400, 402, 404, 409, 410, 412, 414, 415, 416, 451],
        },
    },
    frozen_box=True,
)
