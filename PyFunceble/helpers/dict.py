"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the dict helpers.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import copy
import json
from json import decoder, dump, dumps, loads
from typing import Any, List, Optional, Union

from yaml import dump as yaml_dump
from yaml import safe_load as yaml_load

from PyFunceble.helpers.file import FileHelper


class DictHelper:
    """
    Simplify some :code:`dict` manipulation.

    :param dict main: The main :code:`dict` to work with.
    :raise TypeError: When :code:`main` is not a dict nor a list (tolarated).
    """

    _subject: Optional[Union[Any, dict]] = None

    def __init__(self, subject: Optional[Union[Any, dict]] = None) -> None:
        if subject is not None:
            self.subject = subject

    @property
    def subject(self) -> Optional[Union[Any, dict]]:
        """
        Provides the current state of the :code:`_subject` attribute.
        """

        return self._subject

    @subject.setter
    def subject(self, value: Any) -> None:
        """
        Sets the subject to work with.

        :param value:
            The value to set.
        """

        self._subject = copy.deepcopy(value)

    def set_subject(self, value: Any) -> "DictHelper":
        """
        Sets the subject to work with.

        :param value:
            The value to set.
        """

        self.subject = value

        return self

    def has_same_keys_as(self, to_check: dict, loop: bool = False) -> bool:
        """
        Checks if keys are presents in both given :py:class:`dict`.

        :param to_check:
            The dict to compare with.
        :param loop:
            DO NOT USE, only used to tell us wen to return the list of dataset
            or the final result.
        """

        result = []

        for key, value in to_check.items():
            if key in self.subject:
                if isinstance(value, dict) and isinstance(self.subject[key], dict):
                    result.extend(
                        DictHelper(self.subject[key]).has_same_keys_as(value, loop=True)
                    )
                else:
                    result.append(True)
            else:
                result.append(False)
        if loop:
            return result
        return False not in result

    def remove_key(
        self, key_to_remove: Union[str, List[str]]
    ) -> Optional[Union[Any, dict]]:
        """
        Remove a given key from a given dictionary.

        :param key_to_remove: The key(s) to delete.

        :return: The dict without the given key(s).
        """

        if isinstance(self.subject, dict):
            if isinstance(key_to_remove, list):
                for key in key_to_remove:
                    self.remove_key(key)
            else:
                try:
                    del self.subject[key_to_remove]
                except KeyError:
                    pass
        return self.subject

    def rename_key(self, key_to_rename: dict, strict: bool = True) -> dict:
        """
        Rename the given keys from the given dictionary.

        :param key_to_rename:
            The key(s) to rename.

            Expected format: :code:`{old:new}`

        :param strict:
            Tell us if we have to rename the exact index or
            the index which looks like the given key(s)

        :return: The well formatted dict.
        """

        if isinstance(self.subject, dict) and isinstance(key_to_rename, dict):
            for old, new in key_to_rename.items():
                if strict:
                    if old in self.subject:
                        self.subject[new] = self.subject.pop(old)
                else:
                    to_rename = {}

                    for index in self.subject:
                        if old in index:
                            to_rename.update({index: new[:-1] + index.split(old)[-1]})

                    self.subject = DictHelper(self.subject).rename_key(to_rename, True)
        return self.subject

    def to_json_file(
        self,
        file_path: str,
        ensure_ascii: bool = False,
        indent: int = 4,
        sort_keys: bool = True,
        encoding: str = "utf-8",
        own_class: Optional[json.JSONEncoder] = None,
    ) -> None:
        """
        Converts the given :code:`dict` to JSON and save the result
        into a given file path.

        :param file_path: The file path.
        :param ensure_ascii: Avoids unicode.
        :param indent: The indentation to apply.
        :param sortkeys: Sorts the keys.
        :param encoding: The encoding to apply.
        :param own_class: A class to use for the conversion to json.
        """

        with open(file_path, "w", encoding=encoding) as file_stream:
            dump(
                self.subject,
                file_stream,
                ensure_ascii=ensure_ascii,
                indent=indent,
                sort_keys=sort_keys,
                cls=own_class,
            )

    @staticmethod
    def from_json_file(
        file_path: str, encoding: str = "utf-8", return_dict_on_error: bool = True
    ) -> Optional[Union[List[Any], dict]]:
        """
        Reads the given file path and convert it's content to
        dict/list (tolarated).

        :param file_path: The file path.
        :param return_dict_on_error: Return a dict instead of a NoneType.
        :parma encoding: The encoding to use.
        """

        try:
            return loads(FileHelper(path=file_path).read(encoding=encoding))
        except (decoder.JSONDecodeError, TypeError):
            return None if not return_dict_on_error else {}

    def to_json(
        self,
        ensure_ascii: bool = False,
        indent: int = 4,
        sort_keys: bool = True,
        own_class: Optional[json.JSONEncoder] = None,
    ) -> str:
        """
        Converts a given dict to JSON and return the json string.

        :param ensure_ascii: Avoids unicode.
        :param indent: The indentation to apply.
        :param sort_keys: Sort the keys.
        :param own_class: A class to use for the conversion to json.
        """

        return dumps(
            self.subject,
            ensure_ascii=ensure_ascii,
            indent=indent,
            sort_keys=sort_keys,
            cls=own_class,
        )

    @staticmethod
    def from_json(
        json_str: str, return_dict_on_error: bool = True
    ) -> Optional[Union[List[Any], dict]]:
        """
        Converts a given JSON string to dict/list.

        :param json_str: The JSON string ot convert.
        :param return_dict_on_error:
            Returns a :py:class:`dict` instead of a :py:class:`None`.
        """

        try:
            return loads(json_str)
        except (decoder.JSONDecodeError, TypeError):
            return None if not return_dict_on_error else {}

    @staticmethod
    def from_yaml_file(
        file_path: str, encoding: str = "utf-8"
    ) -> Union[List[Any], dict]:
        """
        Converts a given YAML formatted file, into dict/list.

        :param file_path: The file path.
        :param encoding: The encoding to use.
        """

        with open(file_path, "r", encoding=encoding) as file_stream:
            data = yaml_load(file_stream)

        return data

    def to_yaml_file(
        self,
        file_path: str,
        encoding: str = "utf-8",
        default_flow_style: bool = False,
        indent: int = 4,
        allow_unicode: bool = True,
        sort_keys: bool = True,
    ) -> None:
        """
        Converts the given dict/list to YAML and save the result into a file.

        :param file_path: The file path.
        :param encoding: The encoding.
        :param default_flow_style: Uses the default flow style.
        :param indent: The indentation to apply.
        :param allow_unicode: Allows the  decoding of unicode chars.
        :param sort_keys: Sorts the keys.
        """

        with open(file_path, "w", encoding=encoding) as file_stream:
            yaml_dump(
                self.subject,
                stream=file_stream,
                default_flow_style=default_flow_style,
                indent=indent,
                allow_unicode=allow_unicode,
                encoding=encoding,
                sort_keys=sort_keys,
            )

    @staticmethod
    def from_yaml(yaml_str) -> Union[List[Any], dict]:
        """
        Converts the given YAML string to dict/list.

        :param str yaml_str: The YAML string to convert.
        """

        return yaml_load(yaml_str)

    def to_yaml(
        self,
        encoding: str = "utf-8",
        default_flow_style: bool = False,
        indent: int = 4,
        allow_unicode: bool = True,
        sort_keys: bool = True,
    ) -> str:
        """
        Converts the given dict/list to the YAML format and return
        the result.

        :param str encoding: The encoding to use.
        :param bool default_flow_style: Uses the default flow style.
        :param int indent: The indentation to apply.
        :param bool allow_unicode: Allows the decoding of unicode chars.
        :param bool sort_keys: Sors the keys.

        :rtype: dict|list
        """

        return yaml_dump(
            self.subject,
            default_flow_style=default_flow_style,
            indent=indent,
            allow_unicode=allow_unicode,
            encoding=encoding,
            sort_keys=sort_keys,
        ).decode()

    def flatten(
        self,
        *,
        separator: str = ".",
        previous: Optional[str] = None,
        data: Optional[Any] = None,
    ) -> dict:
        """
        Flatten the current dictionnary.

        :param separator:
            The separator to apply.
        :param previous:
            The previous key we are working with.
        :param data:
            The data to work with. If not given, we fallback to :code:`self.subject`.
        """

        if data is None:
            data = self.subject

        result = {}

        if isinstance(data, dict):
            for key, value in data.items():
                for yek, eulav in (
                    DictHelper(value).flatten(separator=separator, previous=key).items()
                ):
                    if previous is not None:
                        result[f"{previous}{separator}{yek}"] = eulav
                    else:
                        result[yek] = eulav
        else:
            if previous:
                result[previous] = data
            else:
                result[separator] = data

        return result

    def unflatten(self, *, separator: str = ".", data: Optional[Any] = None):
        """
        Unflatten a previously flatten dictionnary.

        :param separator:
            The separator to split.
        """

        if data is None:
            data = self.subject

        result = {}

        for key, value in data.items():
            local_result = result

            if separator in key:
                splitted_sep = key.replace(separator + separator, separator).split(
                    separator
                )

                for yek in splitted_sep[:-1]:
                    if yek not in local_result:
                        local_result[yek] = {}

                    local_result = local_result[yek]
                local_result[splitted_sep[-1]] = value
            else:
                local_result[key] = value

        return result
