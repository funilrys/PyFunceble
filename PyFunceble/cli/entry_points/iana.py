"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the endpoints related to our own version of the iana database.

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

import argparse
import sys
import traceback
from os import cpu_count

import colorama

import PyFunceble.cli.storage
import PyFunceble.cli.utils.ascii_logo
from PyFunceble.cli.scripts.iana import IanaDBGenerator


def generator() -> None:
    """
    Provides the CLI for the IANA file generation.
    """

    colorama.init(autoreset=True)

    description = (
        f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}PyFunceble IANA Generator"
        f"{colorama.Style.RESET_ALL} - "
        "The IANA database file generator for PyFunceble."
    )

    parser = argparse.ArgumentParser(
        description=description,
        epilog=PyFunceble.cli.storage.STD_EPILOG,
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-d",
        "--destination",
        type=str,
        help="Sets the path to the file to write.",
        default=None,
    )

    parser.add_argument(
        "-w",
        "--max-workers",
        type=int,
        help=f"Sets the maximum number of worker to use. "
        f"(Default: {cpu_count() * 5})",
        default=None,
    )

    args = parser.parse_args()

    utility = IanaDBGenerator()

    if args.destination:
        utility.destination = args.destination

    print(PyFunceble.cli.utils.ascii_logo.get_home_representation())

    print(f"Generation of IANA database into {utility.destination!r}", end=" ")
    try:
        utility.start(max_workers=args.max_workers)
        print(PyFunceble.cli.storage.DONE)
    except:  # pylint: disable=bare-except
        print(PyFunceble.cli.storage.ERROR)
        print(traceback.format_exc())
        sys.exit(1)
