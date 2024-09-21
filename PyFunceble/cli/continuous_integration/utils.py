"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some utilities related to the CI.

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

import PyFunceble.facility
from PyFunceble.cli.continuous_integration.base import ContinuousIntegrationBase
from PyFunceble.cli.continuous_integration.github_actions import GitHubActions
from PyFunceble.cli.continuous_integration.gitlab_ci import GitLabCI
from PyFunceble.cli.continuous_integration.jenkins import Jenkins
from PyFunceble.cli.continuous_integration.standalone import Standalone
from PyFunceble.cli.continuous_integration.travis_ci import TravisCI


def ci_object(*args, **kwargs) -> ContinuousIntegrationBase:
    """
    A placeholder which provides the CI object to use.
    """

    known_objects = [Jenkins, GitHubActions, TravisCI, GitLabCI, Standalone]
    result = None

    for known in known_objects:
        result = known(*args, **kwargs)
        result.guess_all_settings()

        PyFunceble.facility.Logger.debug("Checking if %r is authorized.", result)

        if result.is_authorized():
            PyFunceble.facility.Logger.debug(
                "%r is authorized. Using it as CI object.", result
            )
            return result

    PyFunceble.facility.Logger.debug(
        "No known CI object authorized. Using: %r", known_objects[0]
    )

    return known_objects[0](*args, **kwargs)
