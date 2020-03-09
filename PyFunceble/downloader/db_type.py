"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the downloader of the desired database type file.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io//en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    MIT License

    Copyright (c) 2017, 2018, 2019, 2020 Nissar Chababy

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

from os import sep as directory_separator

import PyFunceble

from .base import DownloaderBase


class DBTypeDownloader(DownloaderBase):
    """
    Provides the downloader of the desired database type file.
    """

    DOWNTIME_INDEX = f"db_type"
    REDOWNLOAD_AFTER = 0

    def __init__(self):
        is_cloned_version = PyFunceble.abstracts.Version.is_local_cloned()
        destination_directory = (
            f"{PyFunceble.CONFIG_DIRECTORY}"
            f"{PyFunceble.CONFIGURATION.outputs.db_type.directory}"
            f"{directory_separator}"
        )
        destination_dir_instance = PyFunceble.helpers.Directory(destination_directory)

        not_supported_db_types = ["json"]

        self.destination = (
            f"{destination_directory}"
            f"{PyFunceble.CONFIGURATION.outputs.db_type.files[PyFunceble.CONFIGURATION.db_type]}"
        )

        if not is_cloned_version and (
            PyFunceble.CONFIGURATION.db_type not in not_supported_db_types
        ):
            destination_dir_instance.delete()

            if PyFunceble.CONFIGURATION.db_type not in not_supported_db_types:
                destination_dir_instance.create()

                self.DOWNTIME_INDEX += f"_{PyFunceble.CONFIGURATION.db_type}"  # pylint: disable=invalid-name

                self.download_link = PyFunceble.converter.InternalUrl(
                    PyFunceble.CONFIGURATION.links[PyFunceble.CONFIGURATION.db_type]
                ).get_converted()

                super().__init__()

                self.process()
