"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides everything related to the PyFunceble infrastructure.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/master/

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


class Infrastructure:
    """
    Provides some infrastructure related abstractions.
    """

    DEFAULT_CONFIGURATION_FILENAME = ".PyFunceble_production.yaml"
    """
    Sets the name of the default configuration file.

    :type: str
    """

    CONFIGURATION_FILENAME = ".PyFunceble.yaml"
    """
    Sets the name of the user editable configuration file.

    :type: str
    """

    ENV_FILENAME = ".pyfunceble-env"
    """
    Sets the name of our own environment file.

    :type: str
    """

    DOWN_FILENAME = ".pyfunceble_intern_downtime.json"
    """
    Sets the name of our own download time record
    file.

    :type: str
    """

    USER_AGENT_FILENAME = "user_agents.json"
    """
    Sets the name of our own copy of the user agents file.
    """

    HASHES_FILENAME = "hashes_tracker.json"
    """
    Sets the name of the file which will save the hashes of the
    files we are testing.
    """

    IPV4_REPUTATION_FILENAME = "ipv4_reputation.data"
    """
    Sets the name of our own copy of the IPv4 reputation data file.

    :type: str
    """

    PROD_CONFIG_LINK = "https://raw.githubusercontent.com/funilrys/PyFunceble/master/.PyFunceble_production.yaml"  # pylint: disable=line-too-long
    """
    Sets the link to the production configuration file.

    :type: str
    """

    REPO_LINK = "https://git.io/vpZoI"
    """
    Sets the link to the repository.

    :type: str
    """

    ALEMBIC_DIRECTORY_NAME = "alembic"
    """
    Sets the name of the alembic related directory.

    :type: str
    """

    CI_MIGRATION_TRIGGER_FILE = ".trigger"
    """
    Sets the name of the file to write into for the case that
    we are migrating to sqlalchemy from inside a CI engine.

    :type: str
    """
