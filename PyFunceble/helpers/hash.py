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
