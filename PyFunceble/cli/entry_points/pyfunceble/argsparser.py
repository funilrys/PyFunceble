"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our very own argument parser

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

import argparse
from typing import Optional, Sequence

# pylint: disable=raising-bad-type


class OurArgumentParser(argparse.ArgumentParser):
    """
    Overwrites some behavior of the default argument parser.
    """

    def parse_args(
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[argparse.Namespace] = None,
    ) -> argparse.Namespace:
        namespace = super().parse_args(args, namespace)

        if namespace.lookup__timeout is not None and namespace.lookup__timeout < 0:
            raise self.error("--timeout must be a positive digit.")

        if (
            namespace.cli_testing__cooldown_time is not None
            and namespace.cli_testing__cooldown_time < 0
        ):
            raise self.error("--cooldown-time must be zero or a positive digit.")

        if (
            namespace.cli_testing__max_workers is not None
            and namespace.cli_testing__max_workers <= 0
        ):
            raise self.error("--max-workers must be a positive digit.")

        if (
            namespace.cli_testing__display_mode__max_registrar is not None
            and namespace.cli_testing__display_mode__max_registrar <= 0
        ):
            raise self.error("--max-registrar must be a positive digit.")

        if namespace.dns__delay is not None and namespace.dns__delay < 0:
            raise self.error("--dns-delay must be zero or a positive digit.")

        if namespace.max_http_retries is not None and namespace.max_http_retries < 0:
            raise self.error("--max-http-retries must be zero or a positive digit.")

        if namespace.cli_decoding__adblock and namespace.cli_decoding__wildcard:
            raise self.error("--adblock and --wildcard are incompatible.")

        if namespace.cli_decoding__adblock and namespace.cli_decoding__rpz:
            raise self.error("--adblock and --rpz are incompatible.")

        if namespace.cli_decoding__wildcard and namespace.cli_decoding__rpz:
            raise self.error("--rpz and --wildcard are incompatible.")

        if (
            namespace.cli_testing__testing_mode__syntax
            and namespace.cli_testing__testing_mode__reputation
        ):
            raise self.error("--syntax and --reputation are incompatible.")

        return namespace
