from os import path, remove
from shutil import copy as shutil_copy
from shutil import move as shutil_move


class File:
    """
    Simplify the file manipulations.

    :param str file_path: The file path to work with.
    """

    def __init__(self, file_path=None):
        self.path = file_path

    def exists(self, file_path=None):
        """
        Checks if the given file path exists.

        :param str file_path:
            The file path to check.

            .. note::
                If :code:`None` is given, we
                report to the globally given file path.
        :rtype: bool
        """
        if not file_path:
            file_path = self.path

        return path.isfile(file_path)

    def delete(self, file_path=None):
        """
        Deletes the given file path if it exists.

        :param str file_path:
            The file path to check.

            .. note::
                If :code:`None` is given, we
                report to the globally given file path.

        :return: The non existance state of the file.
        :rtype: bool
        """
        if not file_path:
            file_path = self.path

        if self.exists(file_path=file_path):
            remove(file_path)
        return not self.exists(file_path=file_path)

    def write(
        self, data, overwrite=False, encoding="utf-8", newline="\n", file_path=None
    ):
        """
        Write the given data into the given file path.

        :param str data: The data to write.
        :param str encoding: The encoding to use while opening the file.
        :param str newline: The new line char to use.
        :param str file_path:
            The file path to check.

            .. note::
                If :code:`None` is given, we
                report to the globally given file path.
        """

        if not file_path:
            file_path = self.path

        if data and isinstance(data, str):
            if overwrite or not self.exists(file_path=file_path):
                with open(
                    file_path, "w", encoding=encoding, newline=newline
                ) as file_stream:
                    file_stream.write(data)
            else:
                with open(
                    file_path, "a", encoding=encoding, newline=newline
                ) as file_stream:
                    file_stream.write(data)

    def read(self, file_path=None, encoding="utf-8", newline="\n"):
        """
        Read the given file path and return it's content.

        :param str file_path:
            The file path to check.

            .. note::
                If :code:`None` is given, we
                report to the globally given file path.
        :param str encoding: The encoding to use.
        :param str newline: The new line char to use.
        :rtype: str
        """

        if not file_path:
            file_path = self.path

        data = None

        if self.exists(file_path):
            with open(
                self.path, "r", encoding=encoding, newline=newline
            ) as file_stream:
                data = file_stream.read()

        return data

    def copy(self, destination):
        """
        Copy the globaly given file path to the given destination.

        :param str destination: The destination of the copy.
        """

        if self.exists(self.path):
            shutil_copy(self.path, destination)

    def move(self, destination):  # pragma: no cover
        """
        Move the globally given file path to the given destination.

        :param str destination: The destination of the file.
        """

        if self.exists(self.path):
            shutil_move(self.path, destination)
