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

import os
import secrets
from typing import Optional

from box import Box
from dotenv import load_dotenv

from PyFunceble.storage_facility import get_config_directory

PROJECT_NAME: str = "PyFunceble"
PROJECT_VERSION: str = "4.2.0a2.dev (Blue Duckling: Ixora)"

DISTRIBUTED_CONFIGURATION_FILENAME: str = ".PyFunceble_production.yaml"
DISTRIBUTED_DIR_STRUCTURE_FILENAME: str = "dir_structure_production.json"

IANA_DUMP_FILENAME: str = "iana-domains-db.json"
PUBLIC_SUFFIX_DUMP_FILENAME: str = "public-suffix.json"
CONFIGURATION_FILENAME: str = ".PyFunceble.yaml"
CONFIGURATION_OVERWRITE_FILENAME: str = ".PyFunceble.overwrite.yaml"
ENV_FILENAME: str = ".pyfunceble-env"
DOWN_FILENAME: str = ".pyfunceble_intern_downtime.json"
USER_AGENT_FILENAME: str = "user_agents.json"
IPV4_REPUTATION_FILENAME: str = "ipv4_reputation.data"

# pylint: disable=line-too-long
IANA_DUMP_LINK: str = (
    "https://raw.githubusercontent.com/PyFunceble/iana/master/iana-domains-db.json"
)
PUBLIC_SUFFIX_DUMP_LINK: str = "https://raw.githubusercontent.com/PyFunceble/public-suffix/master/public-suffix.json"
USER_AGENT_DUMP_LINK: str = (
    "https://raw.githubusercontent.com/PyFunceble/user_agents/master/user_agents.json"
)
IPV4_REPUTATION_DUMP_LINK: str = "https://reputation.alienvault.com/reputation.data"

SHORT_REPO_LINK: str = "https://git.io/vpZoI"
REPO_LINK: str = "https://github.com/funilrys/PyFunceble"

NOT_RESOLVED_STD_HOSTNAME: str = f"pyfunceble-{secrets.token_hex(12)}.com"

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
COLLECTION: Optional[Box] = Box({})
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
