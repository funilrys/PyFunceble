"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the endpoints related to our production preparation.

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

import colorama

import PyFunceble.cli.storage
import PyFunceble.cli.utils.ascii_logo
from PyFunceble.cli.scripts.production import ProductionPrep


def producer() -> None:  # pylint: disable=too-many-statements
    """
    Provides the CLI for the production preparator.
    """

    colorama.init(autoreset=True)

    description = (
        f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}PyFunceble Production Preparator"
        f"{colorama.Style.RESET_ALL} - "
        "The Production peparator for PyFunceble."
    )

    parser = argparse.ArgumentParser(
        description=description,
        epilog=PyFunceble.cli.storage.STD_EPILOG,
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "branch", type=str, help="Sets the branch to acts as.", default=None
    )

    args = parser.parse_args()

    utility = ProductionPrep()

    try:
        utility.branch = args.branch
    except (TypeError, ValueError) as exception:
        print(f"{colorama.Fore.RED}{colorama.Style.BRIGHT}{str(exception)}")
        sys.exit(1)

    print(PyFunceble.cli.utils.ascii_logo.get_home_representation())

    print("Update setup.py", end=" ")
    try:
        utility.update_setup_py()
        print(PyFunceble.cli.storage.DONE)
    except:  # pylint: disable=bare-except
        print(PyFunceble.cli.storage.ERROR)
        print(traceback.format_exc())
        sys.exit(1)

    print("Update URL in source code and tests", end=" ")
    try:
        utility.update_code_urls()
        print(PyFunceble.cli.storage.DONE)
    except:  # pylint: disable=bare-except
        print(PyFunceble.cli.storage.ERROR)
        print(traceback.format_exc())
        sys.exit(1)

    print("Update URL in documentation", end=" ")
    try:
        utility.update_docs_urls()
        print(PyFunceble.cli.storage.DONE)
    except:  # pylint: disable=bare-except
        print(PyFunceble.cli.storage.ERROR)
        print(traceback.format_exc())
        sys.exit(1)

    print("Update source code and tests format", end=" ")
    try:
        utility.update_code_format()
        print(PyFunceble.cli.storage.DONE)
    except:  # pylint: disable=bare-except
        print(PyFunceble.cli.storage.ERROR)
        print(traceback.format_exc())
        sys.exit(1)

    print("Update version file", end=" ")
    try:
        utility.update_version_file()
        print(PyFunceble.cli.storage.DONE)
    except:  # pylint: disable=bare-except
        print(PyFunceble.cli.storage.ERROR)
        print(traceback.format_exc())
        sys.exit(1)

    print("Update dir structure file", end=" ")
    try:
        utility.update_dir_structure_file()
        print(PyFunceble.cli.storage.DONE)
    except:  # pylint: disable=bare-except
        print(PyFunceble.cli.storage.ERROR)
        print(traceback.format_exc())
        sys.exit(1)

    print("Update documentation", end=" ")
    try:
        utility.update_documentation()
        print(PyFunceble.cli.storage.DONE)
    except:  # pylint: disable=bare-except
        print(PyFunceble.cli.storage.ERROR)
        print(traceback.format_exc())
        sys.exit(1)
