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

Provides the conversion of the an RPZ input line into testable subjects.

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
# pylint: enable=line-too-long

from typing import List

from PyFunceble.converter.input_line2subject import InputLine2Subject


class RPZInputLine2Subject(InputLine2Subject):
    """
    Converts/Extracts the subject from the given RPZ inputline.
    """

    COMMENT: list = [";", "//", "#"]
    SPECIAL: list = ["$", "@"]

    def get_converted(self) -> List[str]:
        """
        Provides the converted data.
        """

        result = []
        subject = self.data_to_convert.strip()

        if (
            subject
            and not any(subject.startswith(x) for x in self.COMMENT)
            and not any(subject.startswith(x) for x in self.SPECIAL)
        ):
            for comment_sign in self.COMMENT:
                if comment_sign in subject:
                    subject = subject[: subject.find(comment_sign)].strip()

            if self.SPACE in subject or self.TAB in subject:
                subject = subject.split()[0]

                if not subject.isdigit():
                    result.append(subject)
            elif not subject.isdigit():
                result.append(subject)

        return result
