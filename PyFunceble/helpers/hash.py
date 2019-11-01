from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


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

    def file(self, file_path):
        """
        Open the given file, and it's content.

        :param str file_path:
            The file to hash.

        :rtype: str
        """

        digest = hashes.Hash(getattr(hashes, self.algo)(), backend=default_backend())

        try:
            with open(file_path, "rb") as file_stream:
                digest.update(file_stream.read())

            return digest.finalize().hex()
        except FileNotFoundError:
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
