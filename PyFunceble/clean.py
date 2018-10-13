#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check the availability of domains, IPv4 or URL.

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


class Clean:
    """
    Directory cleaning logic.
    This class clean the output/ directory.

    Argument:
        - list_to_test: list
            The list of domains to test.
    """

    def __init__(self, list_to_test):
        if list_to_test:
            # The list to test is not empty.

            try:
                # We try to see if we have to reset counters and clean the output directory.

                # We get the number of tested.
                number_of_tested = PyFunceble.CONFIGURATION["counter"]["number"][
                    "tested"
                ]

                if (
                    number_of_tested == 0
                    or list_to_test[number_of_tested - 1] == list_to_test[-1]
                    or number_of_tested == len(list_to_test)
                ):
                    # * If the number of tested is null,
                    # or
                    # * the last tested element is the same as the last element in the
                    #   sequence,
                    # or
                    # * The number of tested is equal to the number of elements in the
                    #   sequence,

                    # We reset the counters.
                    Core.reset_counters()

                    # We clean the output directory.
                    self.all()
            except IndexError:
                # But if at any time in the conditionnal an Index Error occurs,

                # We reset the counters.
                Core.reset_counters()

                # We clean the output directory.
                self.all()
        else:
            # The list to test is empty.

            # We clean the output directory.
            self.all()

    @classmethod
    def file_to_delete(cls):
        """
        Return the list of file to delete.
        """

        # We initiate the directory we have to look for.
        directory = PyFunceble.OUTPUT_DIRECTORY + PyFunceble.OUTPUTS["parent_directory"]

        if not directory.endswith(directory_separator):  # pragma: no cover
            # For safety, if it does not ends with the directory separator, we append it
            # to its end.
            directory += directory_separator

        # We initiate a variable which will save the list of file to delete.
        result = []

        for root, _, files in walk(directory):
            # We walk in the directory and get all files and sub-directories.

            for file in files:
                # If there is files in the current sub-directory, we loop
                # through the list of files.

                if file not in [".gitignore", ".keep"]:
                    # The file is not into our list of file we do not have to delete.

                    if root.endswith(directory_separator):
                        # The root ends with the directory separator.

                        # We construct the path and append the full path to the result.
                        result.append(root + file)
                    else:
                        # The root directory does not ends with the directory separator.

                        # We construct the path by appending the directory separator
                        # between the root and the filename and append the full path to
                        # the result.
                        result.append(
                            root + directory_separator + file
                        )  # pragma: no cover

        # We return our list of file to delete.
        return result

    def all(self):
        """
        Delete all discovered files.
        """

        # We get the list of file to delete.
        to_delete = self.file_to_delete()

        for file in to_delete:
            # We loop through the list of file to delete.

            # And we delete the currently read file.
            File(file).delete()
