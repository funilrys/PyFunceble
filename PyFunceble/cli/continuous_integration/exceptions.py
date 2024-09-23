# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the exception related to the CI integration.

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

import PyFunceble.exceptions


class ContinuousIntegrationException(PyFunceble.exceptions.PyFuncebleException):
    """
    Describes an exception related to the continuous integration.
    """


class TokenNotFound(ContinuousIntegrationException):
    """
    Describes a missing (Git?(lab|hub)) Token.
    """


class RemoteURLNotFound(ContinuousIntegrationException):
    """
    Describes a missing or unknown remote URL.
    """


class GitBranchNotFound(ContinuousIntegrationException):
    """
    Describes a missing git branch.
    """


class GitDistributionBranchNotFound(ContinuousIntegrationException):
    """
    Describes a missing git distribution branch.
    """


class GitEmailNotFound(ContinuousIntegrationException):
    """
    Describes a missing Git Email.
    """


class GitNameNotFound(ContinuousIntegrationException):
    """
    Describes a missing Git Name.
    """


class StopExecution(ContinuousIntegrationException):
    """
    Informs upstream - or interacting interface - that we pushed the changes
    and that they need stop everything they plan to do with PyFunceble.
    """


class StartTimeNotFound(ContinuousIntegrationException):
    """
    Describes a missing start time.
    """
