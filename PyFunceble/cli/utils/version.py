"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the version comparison tool.

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
import sys
from datetime import datetime

import colorama
from box import Box

import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.cli.utils.stdout import print_single_line
from PyFunceble.converter.internal_url import InternalUrlConverter
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.utils.version import VersionUtility


def get_upstream_version() -> Box:
    """
    Provides the state of the upstream version.
    """

    return Box(
        DictHelper().from_yaml(
            DownloadHelper(
                InternalUrlConverter(
                    PyFunceble.cli.storage.VERSION_DUMP_LINK
                ).get_converted()
            ).download_text()
        ),
        frozen_box=True,
    )


def get_local_version() -> Box:
    """
    Provides the state of the local version file.
    """

    return Box(
        DictHelper().from_yaml_file(
            os.path.join(
                PyFunceble.storage.CONFIG_DIRECTORY,
                PyFunceble.cli.storage.DISTRIBUTED_VERSION_FILENAME,
            )
        ),
        frozen_box=True,
    )


def handle_force_update(upstream_version: Box) -> None:
    """
    Checks if we should force the end-user to update.
    """

    version_utility = VersionUtility(PyFunceble.storage.PROJECT_VERSION)

    if (
        PyFunceble.facility.ConfigLoader.is_already_loaded()
        and PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.colour
    ):
        message = (
            f"{colorama.Style.BRIGHT}{colorama.Fore.RED}A critical issue has "
            f"been fixed.{colorama.Style.RESET_ALL}\n"
            f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}Please take the time to"
            f"update {PyFunceble.storage.PROJECT_NAME}!{colorama.Style.RESET_ALL}"
        )
    else:
        message = (
            "A critical issue has been fixed.\nPlease take the time to "
            f"update {PyFunceble.storage.PROJECT_NAME}!"
        )

    if upstream_version.force_update.status:
        for minimal in upstream_version.force_update.minimal_version:
            if version_utility.is_older_than(minimal):
                print(message)

                sys.exit(1)


def handle_deprecated_version(upstream_version: Box) -> bool:
    """
    Checks if the current version (local) is deprecated and provides a message
    to the end-user.

    :return:
        :py:class:`True` if local is deprecated. :py:class:`False` otherwise.
    """

    version_utility = VersionUtility(PyFunceble.storage.PROJECT_VERSION)

    if PyFunceble.facility.ConfigLoader.is_already_loaded():
        if PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet:
            message = "Version deprecated."
        elif PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.colour:
            message = (
                f"{colorama.Style.BRIGHT}{colorama.Fore.RED}Your current version "
                f"is considered as deprecated.{colorama.Style.RESET_ALL}\n"
                f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}Please take the "
                "time to "
                f"update {PyFunceble.storage.PROJECT_NAME}!{colorama.Style.RESET_ALL}"
            )
        else:
            message = (
                "Your current version is considered as deprecated.\nPlease take "
                "the time to "
                f"update {PyFunceble.storage.PROJECT_NAME}!"
            )
    else:
        message = (
            "Your current version is considered as deprecated.\nPlease take the "
            "time to "
            f"update {PyFunceble.storage.PROJECT_NAME}!"
        )

    for version in reversed(upstream_version.deprecated):
        if version_utility.is_older_than(version):
            print(message)
            return True

    return False


def handle_greater_version(upstream_version: Box) -> None:
    """
    Checks if the current version (local) is more recent than the upstream one
    and provides a message.

    :return:
        :py:class:`True` if local is greater. :py:class:`False` otherwise.
    """

    version_utility = VersionUtility(PyFunceble.storage.PROJECT_VERSION)

    if PyFunceble.facility.ConfigLoader.is_already_loaded():
        if PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet:
            message = ""
        elif PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.colour:
            message = (
                f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}Your current version "
                f"is more recent!{colorama.Style.RESET_ALL}\n"
                f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}You should "
                "really consider to submit a Pull Request to "
                f"{PyFunceble.storage.PROJECT_NAME}!"
                f"{colorama.Style.RESET_ALL}\n"
                f"{colorama.Style.BRIGHT}Your version:{colorama.Style.RESET_ALL} "
                f"{PyFunceble.storage.PROJECT_VERSION}\n"
                f"{colorama.Style.BRIGHT}Upstream version:{colorama.Style.RESET_ALL} "
                f"{upstream_version.current_version}\n"
            )
        else:
            message = (
                "Your current version is more recent!\nYou should really "
                "consider to submit a Pull Request to  "
                f"{PyFunceble.storage.PROJECT_NAME}!\n"
                f"Your version: {PyFunceble.storage.PROJECT_VERSION}\n"
                f"Upstream version: {upstream_version.current_version}"
            )
    else:
        message = (
            "Your current version is more recent!\nYou should really "
            "consider to submit a Pull Request to  "
            f"{PyFunceble.storage.PROJECT_NAME}!\n"
            f"Your version: {PyFunceble.storage.PROJECT_VERSION}\n"
            f"Upstream version: {upstream_version.current_version}"
        )

    if version_utility.is_recent(upstream_version.current_version):
        print(message)
        return True

    return False


def handle_older_version(upstream_version: Box) -> bool:
    """
    Checks if the current version (local) is older than the upstream one
    and provides a message to the end-user.

    :return:
        :py:class:`True` if local is older. :py:class:`False` otherwise.
    """

    version_utility = VersionUtility(PyFunceble.storage.PROJECT_VERSION)

    if PyFunceble.facility.ConfigLoader.is_already_loaded():
        if PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet:
            message = "New version available."
        elif PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.colour:
            message = (
                f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}Please take the "
                "time to "
                f"update {PyFunceble.storage.PROJECT_NAME}!"
                f"{colorama.Style.RESET_ALL}\n"
                f"{colorama.Style.BRIGHT}Your version:{colorama.Style.RESET_ALL} "
                f"{PyFunceble.storage.PROJECT_VERSION}\n"
                f"{colorama.Style.BRIGHT}Upstream version:{colorama.Style.RESET_ALL} "
                f"{upstream_version.current_version}\n"
            )
        else:
            message = (
                f"Please take the time to update "
                f"{PyFunceble.storage.PROJECT_NAME}!\n"
                f"Your version: {PyFunceble.storage.PROJECT_VERSION}\n"
                f"Upstream version: {upstream_version.current_version}"
            )
    else:
        message = (
            "Please take the time to "
            f"update {PyFunceble.storage.PROJECT_NAME}!\n"
            f"Your version: {PyFunceble.storage.PROJECT_VERSION}\n"
            f"Upstream version: {upstream_version.current_version}"
        )

    if version_utility.is_older_than(upstream_version.current_version):
        print(message)
        return True

    return False


def handle_messages(upstream_version: Box) -> None:
    """
    Handles and prints the upstream messages.
    """

    version_utility = VersionUtility(PyFunceble.storage.PROJECT_VERSION)
    iso_dateformat = "%Y-%m-%dT%H:%M:%S%z"

    if PyFunceble.facility.ConfigLoader.is_already_loaded():
        if (
            PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.quiet
            or PyFunceble.storage.CONFIGURATION.cli_testing.display_mode.simple
        ):
            authorized = False
        else:
            authorized = True
    else:
        authorized = True

    if authorized:
        local_timezone = datetime.utcnow().astimezone().tzinfo

        for minimal_version, data in upstream_version.messages.items():
            if not version_utility.is_equal_to(
                minimal_version
            ) and not version_utility.is_recent(minimal_version):
                continue

            remaining_days = None

            for single_message in data:
                if "until_date" in single_message:
                    try:
                        remaining_days = (
                            datetime.strptime(single_message.until_date, iso_dateformat)
                            - datetime.now(tz=local_timezone)
                        ).days
                    except ValueError:
                        remaining_days = 0

                if remaining_days is not None and remaining_days <= 0:
                    continue

                if "until" in single_message and (
                    version_utility.is_recent(single_message.until)
                    or version_utility.is_equal_to(single_message.until)
                ):
                    continue

                if "type" in single_message:
                    if single_message.type == "info":
                        coloration = colorama.Fore.YELLOW
                    elif single_message.type == "warning":
                        coloration = colorama.Fore.MAGENTA
                    else:
                        coloration = colorama.Fore.BLUE
                else:
                    coloration = colorama.Fore.CYAN

                coloration += colorama.Style.BRIGHT

                print(
                    f"{coloration}{single_message.message}"
                    f"{colorama.Style.RESET_ALL}\n"
                )


def print_central_messages(check_force_update: bool = False) -> None:
    """
    Collect all possible messages from upstream and downstream and print them.
    """

    upstream_version = get_upstream_version()

    if check_force_update:
        handle_force_update(upstream_version)

    _ = (
        not handle_deprecated_version(upstream_version)
        and not handle_greater_version(upstream_version)
        and not handle_older_version(upstream_version)
    )

    handle_messages(upstream_version)

    for extra_message in PyFunceble.cli.storage.EXTRA_MESSAGES:
        print_single_line(extra_message, force=True)
