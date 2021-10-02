"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the schema of our "status" table.

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

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, Text

from PyFunceble.database.sqlalchemy.base_schema import SchemaBase


class Status(SchemaBase):
    """
    Provides the schema our status table.
    """

    file_id = Column(
        Integer,
        nullable=True,
    )

    tested = Column(Text, nullable=False, index=True)
    _status = Column(Text, nullable=True)
    status = Column(Text, nullable=True)
    _status_source = Column(Text, nullable=True)
    status_source = Column(Text, nullable=True)
    domain_syntax_validation = Column(Boolean(), default=False, nullable=True)
    expiration_date = Column(Text, nullable=True)
    http_status_code = Column(Integer, nullable=True)
    ipv4_range_syntax_validation = Column(Boolean(), default=False, nullable=True)
    ipv4_syntax_validation = Column(Boolean(), default=False, nullable=True)
    ipv6_range_syntax_validation = Column(Boolean(), default=False, nullable=True)
    ipv6_syntax_validation = Column(Boolean(), default=False, nullable=True)
    subdomain_syntax_validation = Column(Boolean(), default=False, nullable=True)
    url_syntax_validation = Column(Boolean(), default=False, nullable=True)
    is_complement = Column(Boolean(), default=False, nullable=True)
    test_completed = Column(Boolean(), default=False, nullable=False)
    tested_at = Column(DateTime(), default=datetime.utcnow, nullable=False)
