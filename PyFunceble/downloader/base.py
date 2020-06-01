"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all our downloader.

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

from datetime import datetime, timedelta

import PyFunceble


class DownloaderBase:
    """
    Provides the downloader base.
    """

    # pylint: disable=no-member

    DOWNTIME_INDEX = None
    """
    Used to set/track the download time of the current file.

    :rtype: str
    """

    REDOWNLOAD_AFTER = 1
    """
    Used to set the redownload frequency in day.

    :rtype: int
    """

    def __init__(self):
        self.downtimes_file = PyFunceble.helpers.File(
            f"{PyFunceble.CONFIG_DIRECTORY}{PyFunceble.abstracts.Infrastructure.DOWN_FILENAME}"
        )

        self.all_downtimes = self.get_all_downtimes()

        if not hasattr(self, "destination"):
            raise PyFunceble.exceptions.NoDownloadDestinationGiven()

        if not hasattr(self, "download_link"):
            raise PyFunceble.exceptions.NoDownloadLinkGiven()

    def get_all_downtimes(self):
        """
        Provides all download times.

        :rtype: dict
        """

        return PyFunceble.helpers.Dict().from_json_file(self.downtimes_file.path)

    def get_downtime(self):
        """
        Provides the download timestamp of the current :code:`DOWN_TIME_INDEX`.

        :rtype: dict, None
        """

        if self.is_downtime_set():
            return self.all_downtimes[self.DOWNTIME_INDEX]

        return None

    def update_downtime(self):
        """
        Updates the current download time.
        """

        current_datetime = datetime.now()

        self.all_downtimes[self.DOWNTIME_INDEX] = {
            "iso": current_datetime.isoformat(),
            "timestamp": current_datetime.timestamp(),
        }

    def save_downtimes(self):
        """
        Saves all downtimes.
        """

        PyFunceble.helpers.Dict(self.all_downtimes).to_json_file(
            self.downtimes_file.path
        )

    def is_downtime_set(self):
        """
        Checks if the downtime is set for the current :code:`DOWNTIME_INDEX`.

        :rtype: bool
        """

        return (
            self.DOWNTIME_INDEX in self.all_downtimes
            and self.all_downtimes[self.DOWNTIME_INDEX]
            and all(
                [
                    x in self.all_downtimes[self.DOWNTIME_INDEX]
                    and self.all_downtimes[self.DOWNTIME_INDEX][x]
                    for x in ["iso", "timestamp"]
                ]
            )
        )

    def is_last_download_expired(self):
        """
        Checks if the last downloaded file is expired.
        """

        if (
            not PyFunceble.helpers.File(self.destination).exists()
            or not self.is_downtime_set()
        ):
            return True

        last_download = datetime.fromtimestamp(self.get_downtime()["timestamp"])

        if (
            self.REDOWNLOAD_AFTER <= 0
            and (datetime.now() - last_download).seconds < 3600
        ):
            return False

        if last_download + timedelta(days=self.REDOWNLOAD_AFTER) <= datetime.now():
            return True

        return False

    def process(self):
        """
        Process the download and returns the downloaded text.

        :rtype: str, None
        """

        if self.is_last_download_expired() and PyFunceble.helpers.Download(
            self.download_link
        ).text(destination=self.destination):
            self.update_downtime()
            self.save_downtimes()
