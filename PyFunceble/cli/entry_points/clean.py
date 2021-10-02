"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the endpoints related to the cleanup of the data we produce.

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
import os
import sys
import traceback

import colorama

import PyFunceble.cli.facility
import PyFunceble.cli.storage
import PyFunceble.cli.utils.ascii_logo
import PyFunceble.facility
from PyFunceble.cli.filesystem.cleanup import FilesystemCleanup
from PyFunceble.cli.system.integrator import SystemIntegrator
from PyFunceble.cli.utils.testing import get_destination_from_origin
from PyFunceble.helpers.directory import DirectoryHelper


def cleaner() -> None:
    """
    Provides the CLI for the public file generation.
    """

    PyFunceble.facility.ConfigLoader.start()

    colorama.init(autoreset=True)

    description = (
        f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}PyFunceble Cleaner"
        f"{colorama.Style.RESET_ALL} - "
        "The cleaner of PyFunceble."
    )

    parser = argparse.ArgumentParser(
        description=description,
        epilog=PyFunceble.cli.storage.STD_EPILOG,
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-f", "--file", type=str, help="Sets the file to cleanup the information for."
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Authorizes the cleanup of everything that is not useful anymore.",
        default=False,
    )

    args = parser.parse_args()

    SystemIntegrator(args).start()

    directories_to_ignore = ["__pyfunceble_origin__"]

    utility = FilesystemCleanup()

    print(PyFunceble.cli.utils.ascii_logo.get_home_representation())

    to_cleanup = []
    directory_helper = DirectoryHelper()

    if args.file:
        to_cleanup.append(get_destination_from_origin(args.file))

    if (
        args.all
        and directory_helper.set_path(PyFunceble.cli.storage.OUTPUT_DIRECTORY).exists()
    ):
        to_cleanup.extend(
            [
                x
                for x in os.listdir(PyFunceble.cli.storage.OUTPUT_DIRECTORY)
                if directory_helper.set_path(
                    os.path.join(PyFunceble.cli.storage.OUTPUT_DIRECTORY, x)
                ).exists()
            ]
        )

    for directory in to_cleanup:
        if directory in directories_to_ignore:
            continue

        utility.set_parent_dirname(directory)

        print(f"Started cleanup of {utility.get_output_basedir()}.", end=" ")

        try:
            utility.clean_output_files()
            print(PyFunceble.cli.storage.DONE)
        except:  # pylint: disable=bare-except
            print(PyFunceble.cli.storage.ERROR)
            print(traceback.format_exc())
            sys.exit(1)

    if args.all:
        utility.clean_database()
