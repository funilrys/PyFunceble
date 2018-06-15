#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check domains or IP availability.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

This submodule will give us the cleaning interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: enable=line-too-long
# pylint: disable=bad-continuation
import PyFunceble
from PyFunceble import directory_separator, walk
from PyFunceble.core import Core
from PyFunceble.helpers import File


class Clean(object):
    """
    Directory cleaning logic.
    This class clean the output/ directory.

    Argument:
        - list_to_test: list
            The list of domains to test.
    """

    def __init__(self, list_to_test):
        if list_to_test:
            try:
                number_of_tested = PyFunceble.CONFIGURATION["counter"]["number"][
                    "tested"
                ]

                if number_of_tested == 0 or list_to_test[
                    number_of_tested - 1
                ] == list_to_test[
                    -1
                ] or number_of_tested == len(
                    list_to_test
                ):
                    Core.reset_counters()

                    self.all()
            except IndexError:
                Core.reset_counters()

                self.all()
        else:
            self.all()

    @classmethod
    def file_to_delete(cls):
        """
        Return the list of file to delete.
        """

        directory = PyFunceble.CURRENT_DIRECTORY + PyFunceble.OUTPUTS[
            "parent_directory"
        ]

        if not directory.endswith(directory_separator):  # pragma: no cover
            directory += directory_separator

        result = []

        for root, _, files in walk(directory):
            for file in files:
                if file not in [".gitignore", ".keep"]:
                    if root.endswith(directory_separator):
                        result.append(root + file)
                    else:
                        result.append(
                            root + directory_separator + file
                        )  # pragma: no cover

        return result

    def all(self):
        """
        Delete all discovered files.
        """

        to_delete = self.file_to_delete()

        for file in to_delete:
            File(file).delete()
