"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the hashing helpers.

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

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from .file import File


class Hash:
    """
    Simplify the hashing of data or file content.

    :param str algo:
        The algorithm to use for hashing.

    :raise ValueError: When the given algo is not known.
    """

    def __init__(self, algo="sha512_224"):
        self.algo = algo.upper()

        if not hasattr(hashes, self.algo):
            raise ValueError(f"Unknown <algo> ({self.algo})")

    def file(self, file_path, encoding="utf-8"):
        """
        Open the given file, and it's content.

        :param str file_path:
            The file to hash.

        :rtype: str
        """

        digest = hashes.Hash(getattr(hashes, self.algo)(), backend=default_backend())

        content = File(file_path).read(encoding=encoding)

        if content:
            digest.update(content.encode(encoding))
            return digest.finalize().hex()

        return None

    def data(self, data):
        """
        Hash the given data.

        :param data:
            The data to hash.
        :type data: str, bytes

        :rtype: str
        """

        if not isinstance(data, (bytes, str)):  # pragma: no cover
            raise ValueError(f"<data> must be {bytes} or {str}, {type(data)}, given.")

        if isinstance(data, str):
            data = data.encode()

        digest = hashes.Hash(getattr(hashes, self.algo)(), backend=default_backend())
        digest.update(data)

        return digest.finalize().hex()
