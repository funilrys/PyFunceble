"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the common storage location for all entry points.

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
import sys
from typing import List, Optional

import colorama
from box import Box

import PyFunceble.cli.storage_facility
from PyFunceble.helpers.merge import Merge
from PyFunceble.utils.platform import PlatformUtility

if PlatformUtility.is_unix() and sys.stdin.encoding == "utf-8":
    STD_EPILOG: str = (
        f"Crafted with {colorama.Fore.RED}♥{colorama.Fore.RESET} by "
        f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}Nissar Chababy (@funilrys)"
        f"{colorama.Style.RESET_ALL} "
        f"with the help of\n{colorama.Style.BRIGHT}{colorama.Fore.GREEN}"
        f"https://pyfunceble.github.io/#/contributors{colorama.Style.RESET_ALL} "
        f"&& {colorama.Style.BRIGHT}{colorama.Fore.GREEN}"
        f"https://pyfunceble.github.io/#/special-thanks{colorama.Style.RESET_ALL}"
    )

    ASCII_PYFUNCEBLE = """
    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝
    """

    ASCII_PYUNCEBLE_RESULT = """
                          █
                        ████    ██
                     ███ ██   █████   ███
               ███ █████    █████   █████
             ██████████   █████   █████
           ██████████   █████   ██████   ██
         ██████████   █████   ██████   ████
       ███████████████████████████   █████
      ██████████████████████████   ████
     ████████ █████ ██████████   █████
     ███████   ███   ███████   █████
     █████████████████████   █████
     ████████████████████  █████
     ███████         █████████
      ████████     █████████
        ██████████████████
          ██████████████
               ████

    """
    DONE: str = f"{colorama.Fore.GREEN}✔"
    ERROR: str = f"{colorama.Fore.RED}✘"
else:
    STD_EPILOG: str = (
        f"Crafted with {colorama.Fore.RED}HEART{colorama.Fore.RESET} by "
        f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}Nissar Chababy (@funilrys)"
        f"{colorama.Style.RESET_ALL} "
        f"with the help of\n{colorama.Style.BRIGHT}{colorama.Fore.GREEN}"
        f"https://pyfunceble.github.io/#/contributors{colorama.Style.RESET_ALL} "
        f"&& {colorama.Style.BRIGHT}{colorama.Fore.GREEN}"
        f"https://pyfunceble.github.io/#/special-thanks{colorama.Style.RESET_ALL}"
    )
    ASCII_PYFUNCEBLE = """
    ########  ##    ## ######## ##     ## ##    ##  ######  ######## ########  ##       ########
    ##     ##  ##  ##  ##       ##     ## ###   ## ##    ## ##       ##     ## ##       ##
    ##     ##   ####   ##       ##     ## ####  ## ##       ##       ##     ## ##       ##
    ########     ##    ######   ##     ## ## ## ## ##       ######   ########  ##       ######
    ##           ##    ##       ##     ## ##  #### ##       ##       ##     ## ##       ##
    ##           ##    ##       ##     ## ##   ### ##    ## ##       ##     ## ##       ##
    ##           ##    ##        #######  ##    ##  ######  ######## ########  ######## ########
    """
    ASCII_PYUNCEBLE_RESULT = """
                          .
                        :==:    ::
                     .:. ..   :-=-.   .:.
               .:. .-==-    :-=-:   .-==:
             .-==--==-.   :-=-:   .-==:
           .-===-==-.   :-=-:   .-==:.   ..
         .-==-====:   :-==.   .-==:.   :==-
       .-==--=====-::-==-=:..-==:.   ..--.
      :===============-=======:.   :-=:
     :=-===:  .-=-. .-======:.   :==-.
     -=====.   --:   -====-.   :==-.
     =======--=====-====:.   :==-.
     -=====---:::::---==.  :==-.
     .==--=.         -===-==-.
      .-==--:      .-=-===-.
        :-====-----=====-.
          .:-=======--:.
               ....
    """
    DONE: str = f"{colorama.Fore.GREEN}DONE"
    ERROR: str = f"{colorama.Fore.RED}ERROR"

VERSION_DUMP_LINK: str = (
    "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/version.yaml"
)

HASHES_FILENAME: str = "hashes_tracker.json"
ALEMBIC_DIRECTORY_NAME = "alembic"
CI_TRIGGER_FILE = ".trigger"
DISTRIBUTED_VERSION_FILENAME: str = "version.yaml"

AUTOCONTINUE_OLD_FILE: str = "continue.json"
INACTIVE_DB_OLD_FILE: str = "inactive_db.json"
MINING_OLD_FILE = "mining.json"
WHOIS_DB_OLD_FILE = "whois_db.json"

AUTOCONTINUE_FILE: str = "continue.csv"
INACTIVE_DB_FILE = "inactive.csv"
RESULTS_RAW_FILE = "results.txt"
WHOIS_DB_FILE = "whois.csv"
EXECUTION_TIME_FILE = "execution_time.json"
COUNTER_FILE = "counter.json"
REGISTRAR_COUNTER_FILE = "registrar_counter.json"
TEST_RUNNING_FILE = ".running"

PRE_LOADER_FILE = "preload.json"

STD_PARENT_DIRNAME: str = "__pyfunceble_origin__"
STD_LOGGING_DIRNAME: str = "__pyfunceble_loggging__"

UNIX_OUTPUTS: dict = {
    "domains": {"filename": "list"},
    "ips": {"filename": "list"},
    "hosts": {"filename": "hosts", "ip_filename": "ips"},
    "analytic": {
        "filenames": {
            "potentially_down": "down_or_potentially_down",
            "potentially_up": "potentially_up",
            "up": "active_and_merged_in_results",
            "suspicious": "suspicious_and_merged_in_results",
        }
    },
    "logs": {
        "filenames": {
            "inactive_not_retested": "inactive_not_retested",
        },
    },
}

WIN_OUTPUTS: dict = {
    "domains": {"filename": "list.txt"},
    "ips": {"filename": "list.txt"},
    "hosts": {"filename": "hosts.txt", "ip_filename": "ips.txt"},
    "analytic": {
        "filenames": {
            "potentially_down": "down_or_potentially_down.txt",
            "potentially_up": "potentially_up.txt",
            "up": "active_and_merged_in_results.txt",
            "suspicious": "suspicious_and_merged_in_results.txt",
        }
    },
    "logs": {
        "filenames": {
            "inactive_not_retested": "inactive_not_retested.txt",
        },
    },
}

UNIVERSAL_OUTPUTS: dict = {
    "domains": {"directory": "domains", "filename": "list"},
    "ips": {"directory": "ips", "filename": "list"},
    "hosts": {"directory": "hosts", "filename": "hosts", "ip_filename": "ips"},
    "analytic": {
        "directories": {
            "parent": "Analytic",
            "potentially_down": "POTENTIALLY_INACTIVE",
            "potentially_up": "POTENTIALLY_ACTIVE",
            "up": "ACTIVE",
            "suspicious": "SUSPICIOUS",
        },
        "filenames": {
            "potentially_down": "down_or_potentially_down",
            "potentially_up": "potentially_up",
            "up": "active_and_merged_in_results",
            "suspicious": "suspicious_and_merged_in_results",
        },
    },
    "logs": {
        "directories": {
            "parent": "logs",
            "percentage": "percentage",
        },
        "filenames": {
            "auto_continue": "continue.json",
            "execution_time": "execution_time.json",
            "percentage": "percentage.txt",
            "registrar": "registrar.txt",
            "whois": "whois.json",
            "date_format": "date_format.json",
            "no_referrer": "no_referrer.json",
            "inactive_not_retested": "inactive_not_retested",
        },
    },
    "parent_directory": "output",
    "merged_directory": "merged_results",
    "splitted": {"directory": "splitted"},
}

OUTPUTS: Optional[Box] = Box(
    (
        Merge(UNIX_OUTPUTS).into(UNIVERSAL_OUTPUTS)
        if PlatformUtility.is_unix()
        else Merge(WIN_OUTPUTS).into(UNIVERSAL_OUTPUTS)
    ),
    frozen_box=True,
)

OUTPUT_DIRECTORY: str = os.path.join(
    PyFunceble.cli.storage_facility.get_output_directory(),
    OUTPUTS.parent_directory,
)

# This one will store some extra messages to print to the user.
EXTRA_MESSAGES: Optional[List[str]] = []
