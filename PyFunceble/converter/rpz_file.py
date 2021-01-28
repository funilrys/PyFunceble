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

Provides the conversion of the RPZ file format.

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
# pylint: enable=line-too-long

from .file import File


class RPZFile(File):
    """
    Converts an RPZ line to a subject to test.
    """

    comment_sign = [";", "//", "#"]
    special_chars = ["$", "@"]

    def get_converted(self):
        """
        Provides the converted data.

        .. warning::
            This method returns return None if no subject
            of interest was found.

        :rtype: None, str, list
        """

        if isinstance(self.data_to_convert, list):
            return [RPZFile(x).get_converted() for x in self.data_to_convert]

        subject = self.data_to_convert.strip()

        if (
            subject
            and not any(subject.startswith(x) for x in self.comment_sign)
            and not any(subject.startswith(x) for x in self.special_chars)
        ):
            for comment_sign in self.comment_sign:
                if comment_sign in subject:
                    subject = subject[: subject.find(comment_sign)].strip()

            if self.space_sign in subject or self.tab_sign in subject:
                subject = subject.split()[0]

                if subject.isdigit():
                    return None
                return subject

            if subject.isdigit():
                return None
            return subject
        return None
