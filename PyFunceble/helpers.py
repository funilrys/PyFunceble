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

This submodule will provide the helpers.

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
import hashlib
from json import decoder, dump, loads
from os import remove
from re import compile as comp
from re import escape
from re import sub as substrings
from subprocess import PIPE, Popen

from yaml import dump as dump_yaml
from yaml import load as load_yaml

from PyFunceble import copy as shutil_copy
from PyFunceble import directory_separator, path, requests


class Hash:  # pylint: disable=too-few-public-methods
    """
    Get and return the hash a file with the given algorithm.

    Arguments:
        - file_path: str
            - The path to the file we have to hash.
        - algorithm: str
            The algoritm to use.
        - only_hash: bool
            True: Return only the desired algorithm

    Note:
        Original version : https://git.io/vFQrK
    """

    def __init__(
        self, file_path, algorithm="sha512", only_hash=False
    ):  # pragma: no cover

        # We initiate the list of allowed algorithms.
        self.valid_algorithms = ["all", "md5", "sha1", "sha224", "sha384", "sha512"]

        # We get the parsed file path.
        self.path = file_path

        # We get the parsed algorithm.
        self.algorithm = algorithm

        # We get the parsed decision about the only hash arguments.
        self.only_hash = only_hash

    def hash_data(self, algo):
        """Get the hash of the given file

        :param algo: A string, the algorithm to use.
        """

        # We het the algorithm function.
        hash_data = getattr(hashlib, algo)()

        with open(self.path, "rb") as file:
            # We open an read the parsed path.

            # We read the content.
            content = file.read()

            # We parse the content to the hash algorithm.
            hash_data.update(content)

        # And we extract and return the hash.
        return hash_data.hexdigest()

    def get(self):
        """
        Return the hash of the given file
        """

        # We initiate a variable which will save the result we are going
        # to return.
        result = {}

        if path.isfile(self.path) and self.algorithm in self.valid_algorithms:
            # * The parsed path exist.
            # and
            # * The parsed algorithm is in the list of valid algorithms.

            if self.algorithm == "all":
                # The parsed algorithm is `all`.

                # We remove `all` (the first element of the list) from
                # the list of valid algorithms because we are going to
                # loop through the list of valid algorithms.
                del self.valid_algorithms[0]

                for algo in self.valid_algorithms:
                    # We loop through the list of valid algorithms.

                    # We save the hash into the result variable.
                    result[algo] = self.hash_data(algo)
            else:
                # The parsed algorithm is a specific one.

                # We save the hash into the result variable.
                result[self.algorithm] = self.hash_data(self.algorithm)
        else:
            # * The parsed path does not exist.
            # or
            # * The parsed algorithm is nor in the list of valid algorithms.
            return None

        if self.algorithm != "all" and self.only_hash:
            # * The parsed algorithm is not equal to `all`.
            # and
            # * We only have to return the selected hash.

            # We return the selected algorithm.
            return result[self.algorithm]

        # * The parsed algorithm is equal to `all`.
        # or
        # * We do not have to return the selected hash.

        # We return all hashes.
        return result


class Command:  # pylint: disable=too-few-public-methods
    """
    Shell command execution.
    """

    def __init__(self, command):  # pragma: no cover
        # We set the default decoding type.
        self.decode_type = "utf-8"

        # We get the command to run.
        self.command = command

    def _decode_output(self, to_decode):
        """
        Decode the output of a shell command in order to be readable.

        Argument:
            - to_decode: byte
                Output of a command to decode.

        Retunes: str
            The decoded output.
        """

        return to_decode.decode(self.decode_type)

    def execute(self):
        """
        Execute the given command.

        Returns: byte
            The output in byte format.
        """

        # We initiate a process and parse the command to it.
        process = Popen(self.command, stdout=PIPE, stderr=PIPE, shell=True)

        # We communicate the command and get the output and the error.
        (output, error) = process.communicate()

        if process.returncode != 0:  # pragma: no cover
            # The return code is different to 0.

            # We return the decoded error.
            return self._decode_output(error)

        # The return code (or exit code if you prefer) if equal to 0.

        # We return the decoded output of the executed command.
        return self._decode_output(output)


class Dict:
    """
    Dictionary manipulations.
    """

    def __init__(self, main_dictionnary=None):  # pragma: no cover

        if main_dictionnary is None:
            # A dictionnary is not parsed.

            # We set the main dictionnary as an empty dictionnary.
            self.main_dictionnary = {}
        else:
            # A dictionnary is parsed.

            # We set the main dictionnary as the parsed dictionnary.
            self.main_dictionnary = main_dictionnary

    def remove_key(self, key_to_remove):
        """
        Remove a given key from a given dictionary.

        Argument:
            - key_to_remove: str or list
                The key(s) to delete.

        Returns: None or dict
            - None: no dict passed to the class.
            - dict: The dict without the removed key(s).
        """

        if isinstance(self.main_dictionnary, dict):
            # The main dictionnary is a dictionnary

            if isinstance(key_to_remove, list):
                # The parsed key to remove is a list.

                for key in key_to_remove:
                    # We loop through the list of key to remove.

                    # We delete the key from the dictionnary.
                    del self.main_dictionnary[key]
            else:
                # The parsed key to remove is not a list.

                # We delete the given key from the dictionnary.
                del self.main_dictionnary[key_to_remove]

            # We return the final dictionnary.
            return self.main_dictionnary

        # The main dictionnary is not a dictionnary.

        # We return None.
        return None

    def rename_key(self, key_to_rename, strict=True):
        """
        Rename the given keys from the given dictionary.

        Argument:
            - key_to_remove: dict
                The key(s) to rename.
                Format: {old:new}
            - strict: bool
                True: We replace the exact string
                False: We replace if the string is like.
        """

        if isinstance(self.main_dictionnary, dict) and isinstance(key_to_rename, dict):
            # * The given main directory is a dictionnary.
            # and
            # * The given key to rename is a dictionnary.

            for old, new in key_to_rename.items():
                # We loop through the key to raname.

                if strict:
                    # The strict method is activated.
                    if old in self.main_dictionnary:
                        # The old key is in the main dictionnary.

                        # We initiate the new with the old and remove the old content.
                        self.main_dictionnary[new] = self.main_dictionnary.pop(old)
                else:
                    # The strict method is not activated.

                    # We initiate the elements to rename.
                    to_rename = {}

                    for index in self.main_dictionnary:
                        # We loop throught the indexes of the main dictionnary.

                        if old in index:
                            # The old key is into the index name.

                            # We append the index name and the new index to our
                            # local list to rename.
                            to_rename.update({index: new[:-1] + index.split(old)[-1]})

                    # We run this method against the local list to rename in order
                    # to rename the element.
                    self.main_dictionnary = Dict(self.main_dictionnary).rename_key(
                        to_rename, True
                    )

            # We return the final list.
            return self.main_dictionnary

        # * The given main directory is not a dictionnary.
        # or
        # * The given key to rename is not a dictionnary.

        # We return None.
        return None

    def to_json(self, destination):
        """
        Save a dictionnary into a JSON file.

        Argument:
            - destination: str
                A path to a file where we're going to
                write the converted dict into a JSON format.
        """

        with open(destination, "w") as file:
            # We open the file we are going to write.
            # Note: We always overwrite the destination.

            # We save the current dictionnary into a json format.
            dump(
                self.main_dictionnary,
                file,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
            )

    def to_yaml(self, destination):
        """
        Save a dictionnary into a YAML file.

        Argument:
            - destination: str
                A path to a file where we're going to write the converted dict into a JSON format.
        """

        with open(destination, "w") as file:
            # We open the file we are going to write.
            # Note: We always overwrite the destination.

            # We save the current dictionnary into a json format.
            dump_yaml(self.main_dictionnary, file, indent=4)

    @classmethod
    def from_json(cls, data):
        """
        Convert a JSON formated string into a dictionary.

        Argument:
            - data: str
                A JSON formated string to convert to dict format.
        """

        try:
            # Read a json string and convert it to dictionnary.
            return loads(data)

        except decoder.JSONDecodeError:  # pragma: no cover
            # In case the decoder return an error,
            # we return and empty dictionnary.
            return {}

    @classmethod
    def from_yaml(cls, data):
        """
        Convert a YAML formated string into a dictionary.

        Argument:
            - data: str
                A YAML formated string to convert to dict format.
        """

        # We read a YAML string and convert it into a dictionnary.
        return load_yaml(data)


class Directory:  # pylint: disable=too-few-public-methods
    """
    Directory manipulation.

    Argument:
        - directory:str
            A path to the directory to manipulate.
    """

    def __init__(self, directory):  # pragma: no cover
        # We get the directory.
        self.directory = directory

    def fix_path(self, splited_path=None):
        """
        This method fix the path of the given path.

        Argument:
            - splited_path: list
                A list to convert to the right path
        """

        if not splited_path:
            # A splited path is parsed.

            # We initate a variable which will save the splited path.
            split_path = []

            if self.directory:
                # The parsed directory is not empty or equal to None.

                if "/" in self.directory:
                    # We split the separator.
                    split_path = self.directory.split("/")
                elif "\\" in self.directory:
                    # We split the separator.
                    split_path = self.directory.split("\\")

                # We run the same function with the splited_path argument filled.
                return self.fix_path(splited_path=filter(lambda dir: dir, split_path))

            # We return the directory.
            return self.directory

        # We join the splited element with the directory separator as glue.
        return directory_separator.join(splited_path) + directory_separator


class File:
    """
    File treatment/manipulations.

    Argument:
        file: str
            A path to the file to manipulate.
    """

    def __init__(self, file):
        # We get the parsed file.
        self.file = file

    def write(self, data_to_write, overwrite=False):
        """
        Write or append data into the given file path.

        Argument:
            - data_to_write: str
                The data to write.
        """

        if overwrite or not path.isfile(self.file):
            # * We have to overwrite the file data.
            # or
            # * The file path does not already exist.

            with open(self.file, "w", encoding="utf-8") as file:
                # We prepare the file for writting.

                if data_to_write and isinstance(data_to_write, str):
                    # * A data  to write is given.
                    # and
                    # * The data to write is a string

                    # We write the string into the file.
                    file.write(data_to_write)
        else:
            # * We do not have to overwrite the file data.
            # or
            # * The file path does already exist.

            with open(self.file, "a", encoding="utf-8") as file:
                # We prepare the file for append writting.

                if data_to_write and isinstance(data_to_write, str):
                    # * A data  to write is given.
                    # and
                    # * The data to write is a string

                    # We append the string into the file.
                    file.write(data_to_write)

    def read(self):
        """
        Read a given file path and return its content.

        Returns: str
            The content of the given file path.
        """

        with open(self.file, "r", encoding="utf-8") as file:
            # We open and read a file.

            # We get the file content.
            funilrys = file.read()

        # We return the file content.
        return funilrys

    def delete(self):
        """
        Delete a given file path.
        """

        try:
            # We try to remove the existing file.
            remove(self.file)
        except OSError:
            # If the path is not found, we ignore the error.
            pass

    def copy(self, destination):
        """
        Copy the givven file to the destination.

        Argument:
            - destination: str
                The destination of the copy
        """

        shutil_copy(self.file, destination)


class List:  # pylint: disable=too-few-public-methods
    """
    List manipulation.

    Argument:
        - main_list: list
            The list to manipulate.
    """

    def __init__(self, main_list=None):  # pragma: no cover
        if main_list is None:
            # The main list is not given.

            # We initiate an empty list.
            self.main_list = []
        else:
            # The main list is given.

            # We get the given list.
            self.main_list = list(filter(lambda x: x is None or x, main_list))

    def format(self):
        """
        Return a well formated list. Basicaly, it's sort a list and remove duplicate.

        Returns: list
            A sorted, without duplicate, list.
        """

        try:
            return sorted(list(set(self.main_list)), key=str.lower)

        except TypeError:  # pragma: no cover
            return self.main_list

    def custom_format(self, key_method, reverse=False):
        """
        Return a well formated list. With the key_method as a function/method to format
        the elements before sorting.

        Arguments:
            - key_method: function
                A function to use to format the readed element before sorting.
            - reverse: bool
                True: Reverse the returned list.

        Returns: list
            A sorted list.
        """

        try:
            return sorted(list(set(self.main_list)), key=key_method, reverse=reverse)
        except TypeError:  # pragma: no cover
            return self.main_list


class Regex:  # pylint: disable=too-few-public-methods

    """A simple implementation ot the python.re package

    Arguments:
        - data: str
            The data to regex check.
        - regex: str
            The regex to match.
        - group: int
            The group to return
        - rematch: bool
            True: return the matched groups into a formated list.
                (implementation of Bash ${BASH_REMATCH})
        - replace_with: str
            The value to replace the matched regex with.
        - occurences: int
            The number of occurence(s) to replace.
    """

    def __init__(self, data, regex, **args):  # pragma: no cover
        # We initiate the needed variable in order to be usable all over
        # class
        self.data = data

        # We assign the default value of our optional arguments
        optional_arguments = {
            "escape": False,
            "group": 0,
            "occurences": 0,
            "rematch": False,
            "replace_with": None,
            "return_data": True,
        }

        # We initiate our optional_arguments in order to be usable all over the
        # class
        for (arg, default) in optional_arguments.items():
            setattr(self, arg, args.get(arg, default))

        if self.escape:  # pylint: disable=no-member
            self.regex = escape(regex)
        else:
            self.regex = regex

    def not_matching_list(self):
        """
        This method return a list of string which don't match the
        given regex.
        """

        pre_result = comp(self.regex)

        return list(
            filter(lambda element: not pre_result.search(str(element)), self.data)
        )

    def matching_list(self):
        """
        This method return a list of the string which match the given
        regex.
        """

        pre_result = comp(self.regex)

        return list(filter(lambda element: pre_result.search(str(element)), self.data))

    def match(self):
        """
        Used to get exploitable result of re.search
        """

        # We initate this variable which gonna contain the returned data
        result = []

        # We compile the regex string
        to_match = comp(self.regex)

        # In case we have to use the implementation of ${BASH_REMATCH} we use
        # re.findall otherwise, we use re.search
        if self.rematch:  # pylint: disable=no-member
            pre_result = to_match.findall(self.data)
        else:
            pre_result = to_match.search(self.data)

        if self.return_data and pre_result:  # pylint: disable=no-member
            if self.rematch:  # pylint: disable=no-member
                for data in pre_result:
                    if isinstance(data, tuple):
                        result.extend(list(data))
                    else:
                        result.append(data)

                if self.group != 0:  # pylint: disable=no-member
                    return result[self.group]  # pylint: disable=no-member

            else:
                result = pre_result.group(
                    self.group  # pylint: disable=no-member
                ).strip()

            return result

        elif not self.return_data and pre_result:  # pylint: disable=no-member
            return True

        return False

    def replace(self):
        """
        Used to replace a matched string with another.
        """

        if self.replace_with:  # pylint: disable=no-member
            return substrings(
                self.regex,
                self.replace_with,  # pylint: disable=no-member
                self.data,
                self.occurences,  # pylint: disable=no-member
            )

        return self.data


class Download:  # pragma: no cover pylint:disable=too-few-public-methods
    """
    This class will download all given file.

    Argument:
        - link: str
            The link to download
        - destination: str
            The location where we should save the downloaded content.
        - return_data: bool
            True: We return data
            False: We save into destination
    """

    def __init__(self, link, destination=None, return_data=False):
        # We get the parsed link.
        self.link = link

        # We get the parsed destination.
        self.destination = destination

        # We get the parsed return data.
        self.return_data = return_data

    def text(self):
        """
        This method download the given link and return its requests.text.
        """

        # We request the link.
        req = requests.get(self.link)

        if req.status_code == 200:
            # The request http status code is equal to 200.

            if self.return_data:
                # We have to return the data.

                # We return the link content.
                return req.text

            # We save the link content to the parsed destination.
            File(self.destination).write(req.text, overwrite=True)

            # We return True.
            return True

        # The request http status code is not equal to 200.

        # We raise an exception saying that we were unable to download.
        raise Exception("Unable to download %s." % repr(self.link))
