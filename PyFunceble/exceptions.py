# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our exceptions.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

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


class PyFuncebleException(Exception):
    """
    Describes our own exceptions.
    """


class PyFuncebleExternalException(PyFuncebleException):
    """
    Describes an exception which is caused by an external input.
    """


class PyFuncebleInternalException(PyFuncebleException):
    """
    Describes an exception which is caused by our own logic.
    """


class WrongParameterType(PyFuncebleInternalException):
    """
    Describes a wrong parameter type.
    """


class WrongParameterValue(PyFuncebleInternalException):
    """
    Describes a wrong parameter value.
    """


class NoInternetConnection(PyFuncebleExternalException):
    """
    Describes a missing connection.
    """


class ConfigurationFileNotFound(PyFuncebleExternalException):
    """
    Describes a missing configuration file.
    """


class GitHubTokenNotFound(PyFuncebleExternalException):
    """
    Describes a missing GitHub token.
    """


class GitLabTokenNotFound(PyFuncebleExternalException):
    """
    Describes a missing GitLab token.
    """


class GitEmailNotFound(PyFuncebleExternalException):
    """
    Describes a missing Git Email.
    """


class GitNameNotFound(PyFuncebleExternalException):
    """
    Describes a missing Git Name.
    """


class PleaseUpdatePyFunceble(PyFuncebleInternalException):
    """
    Describes the impossiblity to continue with an older version.
    """


class NoConversionMade(PyFuncebleInternalException):
    """
    Describes the fact that a conversion was expected but none
    was made.
    """


class NoExtractionMade(PyFuncebleInternalException):
    """
    Describes the fact that an extraction was expected but none
    was made.
    """


class UnknownSubject(PyFuncebleInternalException):
    """
    Describes the fact that an unknown subject is inputed.
    """


class NoDownloadDestinationGiven(PyFuncebleInternalException):
    """
    Describes the fact that the download destination was not declared.
    """


class NoDownloadLinkGiven(PyFuncebleInternalException):
    """
    Describes the fact that no download link was declared.
    """


class UserAgentNotFound(PyFuncebleInternalException):
    """
    Describes the fact that we could not find a user
    agent to work with.
    """


class UserAgentBrowserNotFound(PyFuncebleInternalException):
    """
    Describes the fact that we could not find a valid
    browser to work with.
    """


class UserAgentPlatformNotFound(PyFuncebleInternalException):
    """
    Describes the fact that we could not find a valid
    browser to work with.
    """
