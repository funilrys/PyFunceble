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

Provides the default file content converter.

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
# pylint: enable=line-too-long

from PyFunceble.exceptions import WrongParameterType

from .base import ConverterBase


class File(ConverterBase):
    """
    Converts a line to a subject to test.
    """

    comment_sign = "#"
    space_sign = " "
    tab_sign = "\t"

    def __init__(self, data_to_convert):
        if not isinstance(data_to_convert, (str, list)):
            raise WrongParameterType(
                f"<data_to_convert> should be {str} or {list}, {type(data_to_convert)} given."
            )

        super().__init__(data_to_convert)

    def get_converted(self):
        """
        Provides the converted data.

        .. warning::
            This method returns return None if no subject
            of interest was found.

        :rtype: None, str, list
        """

        if isinstance(self.data_to_convert, list):
            return [File(x).get_converted() for x in self.data_to_convert]

        subject = self.data_to_convert.strip()

        if subject and not subject.startswith(self.comment_sign):
            if self.comment_sign in subject:
                subject = subject[: subject.find(self.comment_sign)].strip()

            if self.space_sign in subject or self.tab_sign in subject:
                # As there was a space or a tab in the string, we consider
                # that we are working with the hosts file format which means
                # that the domain we have to test is after the first string.

                splited = subject.split()

                if len(splited[1:]) > 1:
                    return splited[1:]
                return splited[1]
            return subject
        return None
