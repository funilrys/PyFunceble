"""
The tool to check the availability or syntax of domain, IP or URL.

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

import datetime
import os
from typing import Optional

import PyFunceble.downloader.exceptions
import PyFunceble.exceptions
import PyFunceble.storage
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.file import FileHelper


class DownloaderBase:
    """
    Provides the base of all downloader classes.

    The interface is actually simple, but the part which may be hard to
    understand is the "downtime" part. What we do, is that we save the
    download time inside a JSON file, so this class provides the base around
    the download mechanism but also the generation or update of that JSON file.
    """

    DOWNTIME_INDEX: Optional[str] = None
    """
    Used to set/track the download time of the current file.
    """

    DOWNLOAD_FREQUENCY: int = 1
    """
    The download frequency (in day).

    Example:
        if 1 is given, it's once every 24 hours.

    .. warning::
        A frequency of :code:`0` or a negative number will force the download
        every hour.
    """

    all_downtimes: Optional[dict] = dict()
    """
    Stores the download time of all files (self managed).
    """

    _destination: Optional[str] = None
    _download_link: Optional[str] = None

    dict_helper: DictHelper = DictHelper()

    def __init__(self) -> None:
        self.downtimes_file = FileHelper(
            os.path.join(
                PyFunceble.storage.CONFIG_DIRECTORY, PyFunceble.storage.DOWN_FILENAME
            )
        )

        self.all_downtimes.update(self.get_all_downtimes())

    @property
    def authorized(self) -> bool:
        """
        Provides the authorization to start the download.
        """

        raise NotImplementedError()

    @property
    def destination(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_destination` attribute.
        """

        return self._destination

    @destination.setter
    def destination(self, value: str) -> None:
        """
        Sets the destination.

        :param value:
            The value to set.

        :raise TypeError:
            When value is not a :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._destination = value

    def set_destination(self, value: str) -> "DownloaderBase":
        """
        Sets the destination.

        :param value:
            The value to set.
        """

        self.destination = value

        return self

    @property
    def download_link(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_download_link` attribute.
        """

        return self._download_link

    @download_link.setter
    def download_link(self, value: str) -> None:
        """
        Sets the link to download.

        :param value:
            The value to set.

        :raise TypeError:
            When value is not a :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        self._download_link = value

    def set_download_link(self, value: str) -> "DownloaderBase":
        """
        Sets the link to download.

        :param value:
            The value to set.
        """

        self.download_link = value

        return self

    def get_all_downtimes(self) -> dict:
        """
        Provides the downloadtime of all files.
        """

        return self.dict_helper.from_json_file(self.downtimes_file.path)

    def is_downtime_set(self) -> bool:
        """
        Checks if the download time of the current object exists.
        """

        return (
            self.DOWNTIME_INDEX in self.all_downtimes
            and self.all_downtimes[self.DOWNTIME_INDEX]
            and all(
                x in self.all_downtimes[self.DOWNTIME_INDEX]
                and self.all_downtimes[self.DOWNTIME_INDEX][x]
                for x in ["iso", "timestamp"]
            )
        )

    def get_current_downtime(self):
        """
        Provides the download times of the current :code:`DOWN_TIME_INDEX`.
        """

        if self.is_downtime_set():
            return self.all_downtimes[self.DOWNTIME_INDEX]
        return None

    def set_current_downtime(self) -> "DownloaderBase":
        """
        Sets the current datetime into our registry.
        """

        current_datetime = datetime.datetime.utcnow()

        self.all_downtimes[self.DOWNTIME_INDEX] = {
            "iso": current_datetime.isoformat(),
            "timestamp": current_datetime.timestamp(),
        }

        return self

    def save_all_downtimes(self) -> None:
        """
        Saves the current state of the all downtimes.
        """

        self.dict_helper.set_subject(self.all_downtimes).to_json_file(
            self.downtimes_file.path
        )

    def is_last_download_expired(self) -> bool:
        """
        Checks if the last downloaded file is expired (if exists).
        """

        if not FileHelper(self.destination).exists() or not self.is_downtime_set():
            return True

        last_downloaded_time = datetime.datetime.fromtimestamp(
            self.get_current_downtime()["timestamp"]
        )

        if (
            self.DOWNLOAD_FREQUENCY <= 0
            and (datetime.datetime.utcnow() - last_downloaded_time).seconds < 3600
        ):
            return False

        if (
            last_downloaded_time + datetime.timedelta(days=self.DOWNLOAD_FREQUENCY)
            <= datetime.datetime.utcnow()
        ):
            return True

        return False

    def start(self) -> None:
        """
        Starts the download process.
        """

        if self.authorized and self.is_last_download_expired():
            if not hasattr(self, "destination") or not self.destination:
                raise PyFunceble.downloader.exceptions.NoDownloadDestinationGiven()

            if not hasattr(self, "download_link") or not self.download_link:
                raise PyFunceble.downloader.exceptions.NoDownloadLinkGiven()

            if DownloadHelper(self.download_link).download_text(
                destination=self.destination
            ):
                self.set_current_downtime()
                self.save_all_downtimes()
