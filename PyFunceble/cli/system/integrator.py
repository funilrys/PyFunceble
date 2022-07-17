"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our very own argument parser. Take this as a splitter which runs
some actions against other resource before returning the arguments.

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

import colorama

import PyFunceble.cli.facility
import PyFunceble.cli.factory
import PyFunceble.cli.storage
import PyFunceble.facility
import PyFunceble.storage
from PyFunceble.cli.system.base import SystemBase
from PyFunceble.helpers.dict import DictHelper


class SystemIntegrator(SystemBase):
    """
    Provides our system integrator. The idea is that we given an argparse
    Namespace, we should be able to parse it into our system.

    To simplify the trick and headache in the CLI management, I explicitely
    mapped the :code:`dest` argument to what we are supposed to have in the
    flatten version of the configuration. That way, we only need to compare
    against the flatten version instead of looping over all possible levels
    of the configuration tree.
    """

    @SystemBase.ensure_args_is_given
    def init_logger(self) -> "SystemIntegrator":
        """
        Initiate the loggers. In fact, before this moment, in a normal case
        the logger was not properly initiated.
        To avoid multiple management place, I took it to the essential.

        .. warning::
            If you plan to play with the logger on your own, be sure to
            follow the same procedure.
        """

        PyFunceble.facility.Logger.set_output_directory(
            os.path.join(
                PyFunceble.cli.storage.OUTPUT_DIRECTORY,
                PyFunceble.cli.storage.STD_LOGGING_DIRNAME,
            )
        )

        if hasattr(self.args, "debug__active") and self.args.debug__active:
            PyFunceble.facility.Logger.set_activated(True)

        if hasattr(self.args, "debug__level") and self.args.debug__level:
            PyFunceble.facility.Logger.set_min_level(self.args.debug__level)
            PyFunceble.facility.Logger.set_activated(True)

        if not PyFunceble.facility.Logger.activated:
            PyFunceble.facility.Logger.guess_all_settings()

        # We do this because the starting point is here under the CLI :-)
        PyFunceble.facility.Logger.init_loggers()

    @SystemBase.ensure_args_is_given
    def inject_into_config(self) -> "SystemIntegrator":
        """
        Injects the configuration variables into the configuration after
        comparing each value with the current one.
        """

        PyFunceble.facility.Logger.info(
            "Started to inject arguments info configuration."
        )

        dict_helper = DictHelper(PyFunceble.storage.CONFIGURATION)
        flatten_config = dict_helper.flatten()

        to_update = {}
        reserved_lookup_mode = []

        for key, value in vars(self.args).items():
            if value in (False, None):
                continue

            if "__" in key:
                key = key.replace("__", ".")

            if key in flatten_config:
                if isinstance(flatten_config[key], bool) and isinstance(value, bool):
                    to_update[key] = not flatten_config[key]
                else:
                    to_update[key] = value
            elif key.startswith("self_contained") and "lookup" in key:
                reserved_lookup_mode.append(key[key.rfind(".") + 1 :])

        if reserved_lookup_mode:
            for lookup_key in PyFunceble.storage.CONFIGURATION.lookup.keys():
                if lookup_key in {"timeout"}:
                    continue

                if lookup_key not in reserved_lookup_mode:
                    to_update[f"lookup.{lookup_key}"] = False
                else:
                    to_update[f"lookup.{lookup_key}"] = True

        dict_helper.set_subject(to_update)
        unflatten_to_update = dict_helper.unflatten()

        # We assume that the configuration was already loaded.
        PyFunceble.facility.ConfigLoader.custom_config = unflatten_to_update

        PyFunceble.facility.Logger.debug(
            "Injected into config: %r", unflatten_to_update
        )

        PyFunceble.facility.Logger.info(
            "Finished to inject arguments info configuration."
        )

        return self

    @SystemBase.ensure_args_is_given
    def check_config(self) -> "SystemIntegrator":
        """
        Checks or do some sanity check of the configuration.

        This method will basically check that the common mistakes while mixing
        configuration and CLI arguments are not found.

        .. warning::
            The messages are not directly printed, but rather stored in the
            PyFunceble.cli.storage.EXTRA_MESSAGES list.
        """

        if (
            not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.hosts
            and not PyFunceble.storage.CONFIGURATION.cli_testing.file_generation.plain
        ):
            PyFunceble.cli.storage.EXTRA_MESSAGES.append(
                f"{colorama.Style.BRIGHT}{colorama.Fore.MAGENTA}Your setup won't "
                "generate any output! "
                "Reason: file_generation.hosts and file_generation.plain are "
                "both disabled."
            )

    @SystemBase.ensure_args_is_given
    def start(self) -> "SystemIntegrator":
        """
        Starts a group of actions provided by this interface.
        """

        if hasattr(self.args, "output_location") and self.args.output_location:
            PyFunceble.cli.storage.OUTPUT_DIRECTORY = os.path.realpath(
                os.path.join(
                    self.args.output_location,
                    PyFunceble.cli.storage.OUTPUTS.parent_directory,
                )
            )

        self.init_logger()

        PyFunceble.facility.Logger.debug("Given arguments:\n%r", self.args)

        self.inject_into_config()
        self.check_config()

        PyFunceble.cli.facility.CredentialLoader.start()
        PyFunceble.cli.factory.DBSession.init_db_sessions()

        return self
