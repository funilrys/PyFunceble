"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the base of all datasets classes.

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

import functools
from typing import Any, Optional

import PyFunceble.storage
from PyFunceble.downloader.base import DownloaderBase
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.file import FileHelper


class DatasetBase:
    """
    Provides the base of all dataset.
    """

    STORAGE_INDEX: Optional[str] = None
    DOWNLOADER: Optional[DownloaderBase] = None

    source_file: Optional[str] = None

    def __contains__(self, value: Any):  # pragma: no cover
        raise NotImplementedError()

    def __getattr__(self, value: Any):  # pragma: no cover
        raise AttributeError(value)

    def __getitem__(self, value: Any):  # pragma: no cover
        raise KeyError(value)

    def __getstate__(self):  # pragma: no cover
        return vars(self)

    def __setstate__(self, state):  # pragma: no cover
        vars(self).update(state)

    def ensure_source_file_exists(func):  # pylint: disable=no-self-argument
        """
        Ensures that the source file exists before running the decorated
        method.

        :raise TypeError:
            When :code:`self.source_file` is not a :py:class:`str`.
        :raise ValueError:
            When :code:`self.source_file` is empty.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self.source_file, str):
                raise TypeError(
                    f"<self.source_file> should be {str}, "
                    f"{type(self.source_file)} given."
                )

            if not self.source_file:
                raise ValueError("<self.source_file> should not be empty.")

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @ensure_source_file_exists
    def get_content(self) -> Optional[dict]:
        """
        Provides the cached or the real contend of the dataset (after caching)

        :raise FileNotFoundError:
            When the declared file does not exists.
        """

        if (
            bool(self.STORAGE_INDEX)
            and hasattr(PyFunceble.storage, self.STORAGE_INDEX)
            and bool(getattr(PyFunceble.storage, self.STORAGE_INDEX))
        ):
            return getattr(PyFunceble.storage, self.STORAGE_INDEX)

        file_helper = FileHelper(self.source_file)

        if not file_helper.exists() and bool(
            self.DOWNLOADER
        ):  # pragma: no cover ## This is just a safety endpoint.
            self.DOWNLOADER.start()

            if not file_helper.exists():
                raise FileNotFoundError(file_helper.path)

        content = DictHelper().from_json_file(
            self.source_file, return_dict_on_error=False
        )

        setattr(PyFunceble.storage, self.STORAGE_INDEX, content)

        return content
