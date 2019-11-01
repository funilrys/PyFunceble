from json import decoder, dump, dumps, loads

from yaml import dump as yaml_dump
from yaml import safe_load as yaml_load

from .file import File


class Dict:
    """
    Simplify some :code:`dict` manipulation.

    :param dict main: The main :code:`dict` to work with.
    :raise TypeError: When :code:`main` is not a dict nor a list (tolarated).
    """

    def __init__(self, main=None):

        if main is not None and not isinstance(main, (dict, list)):
            raise TypeError(
                f"<main> must be {dict} or {list} (tolarated), {type(main)} given."
            )

        self.main = main

    def has_same_keys_as(self, to_check, loop=False):
        """
        A dirty solution which checks keys are presents in both
        given :code:`dict`.

        :param dict to_check: The dict to check.
        :param bool loop:
            DO NOT USE, only used to tell us wen to return the list of dataset
            or the final result.

        :rtype: bool
        """

        result = []

        for key, value in to_check.items():
            if key in self.main:
                if isinstance(value, dict) and isinstance(self.main[key], dict):
                    result.extend(
                        Dict(self.main[key]).has_same_keys_as(value, loop=True)
                    )
                else:
                    result.append(True)
            else:
                result.append(False)
        if loop:
            return result
        return False not in result

    def remove_key(self, key_to_remove):
        """
        Remove a given key from a given dictionary.

        :param key_to_remove: The key(s) to delete.
        :type key_to_remove: list|str

        :return: The dict without the given key(s).
        :rtype: dict|None
        """

        if isinstance(self.main, dict):
            # The main dictionnary is a dictionnary

            if isinstance(key_to_remove, list):
                # The parsed key to remove is a list.

                for key in key_to_remove:
                    # We loop through the list of key to remove.

                    # We delete the key from the dictionnary.
                    del self.main[key]
            else:
                # The parsed key to remove is not a list.

                try:
                    # We delete the given key from the dictionnary.
                    del self.main[key_to_remove]
                except KeyError:
                    pass

            # We return the final dictionnary.
            return self.main

        # The main dictionnary is not a dictionnary.

        # We return None.
        return None

    def rename_key(self, key_to_rename, strict=True):
        """
        Rename the given keys from the given dictionary.

        :param dict key_to_rename:
            The key(s) to rename.

            Expected format: :code:`{old:new}`

        :param bool strict:
            Tell us if we have to rename the exact index or
            the index which looks like the given key(s)

        :return: The well formatted dict.
        :rtype: dict|None
        """

        if isinstance(self.main, dict) and isinstance(key_to_rename, dict):
            # * The given main directory is a dictionnary.
            # and
            # * The given key to rename is a dictionnary.

            for old, new in key_to_rename.items():
                # We loop through the key to raname.

                if strict:
                    # The strict method is activated.
                    if old in self.main:
                        # The old key is in the main dictionnary.

                        # We initiate the new with the old and remove the old content.
                        self.main[new] = self.main.pop(old)
                else:
                    # The strict method is not activated.

                    # We initiate the elements to rename.
                    to_rename = {}

                    for index in self.main:
                        # We loop throught the indexes of the main dictionnary.

                        if old in index:
                            # The old key is into the index name.

                            # We append the index name and the new index to our
                            # local list to rename.
                            to_rename.update({index: new[:-1] + index.split(old)[-1]})

                    # We run this method against the local list to rename in order
                    # to rename the element.
                    self.main = Dict(self.main).rename_key(to_rename, True)

            # We return the final list.
            return self.main

        # * The given main directory is not a dictionnary.
        # or
        # * The given key to rename is not a dictionnary.

        # We return None.
        return None

    def to_json_file(
        self,
        file_path,
        ensure_ascii=False,
        indent=4,
        sort_keys=True,
        encoding="utf-8",
        newline="\n",
    ):
        """
        Converts the given :code:`dict` to JSON and save the result
        into a given file path.

        :param str file_path: The file path.
        :param bool ensure_ascii: Avoids unicode.
        :param int indent: The indentation to apply.
        :param bool sortkeys: Sorts the keys.
        :param str newline: The default newline to use.
        """

        with open(file_path, "w", encoding=encoding, newline=newline) as file_stream:
            dump(
                self.main,
                file_stream,
                ensure_ascii=ensure_ascii,
                indent=indent,
                sort_keys=sort_keys,
            )

    @classmethod
    def from_json_file(
        cls, file_path, encoding="utf-8", newline="\n", return_dict_on_error=True
    ):
        """
        Reads the given file path and convert it's content to
        dict/list (tolarated).

        :param str file_path: The file path.
        :param str newline: The default newline to use.
        :param bool return_dict_on_error: Return a dict instead of a NoneType.

        :rtype: dict|list
        """

        try:
            return loads(
                File(file_path=file_path).read(encoding=encoding, newline=newline)
            )
        except decoder.JSONDecodeError:  # pragma: no cover
            return None if not return_dict_on_error else {}

    def to_json(self, ensure_ascii=False, indent=4, sort_keys=True):
        """
        Converts a given dict to JSON and return the json string.

        :param bool ensure_ascii: Avoids unicode.
        :param int indent: The indentation to apply.
        :param sort_keys: Sort the keys.

        :rtype: str
        """

        return dumps(
            self.main, ensure_ascii=ensure_ascii, indent=indent, sort_keys=sort_keys,
        )

    @classmethod
    def from_json(cls, json_str, return_dict_on_error=True):
        """
        Converts a given JSON string to dict/list.

        :param bool return_dict_on_error: Return a dict instead of a NoneType.

        :rtype: dict|list
        """

        try:
            return loads(json_str)
        except decoder.JSONDecodeError:  # pragma: no cover
            return None if not return_dict_on_error else {}

    @classmethod
    def from_yaml_file(cls, file_path, encoding="utf-8", newline="\n"):
        """
        Converts a given YAML formatted file, into dict/list.

        :param str file_path: The file path.
        :param str encoding: The encoding to use.
        :param str newline: The newline char string.

        :rtype: dict|list
        """

        with open(file_path, "r", encoding=encoding, newline=newline) as file_stream:
            data = yaml_load(file_stream)

        return data

    def to_yaml_file(
        self,
        file_path,
        encoding="utf-8",
        newline="\n",
        default_flow_style=False,
        indent=4,
        allow_unicode=True,
        sort_keys=True,
    ):
        """
        Converts the given dict/list to YAML and save the result into a file.

        :param str file_path: The file path.
        :param str encoding: The encoding.
        :param str newline: The newline char string.
        :param bool default_flow_style: Uses the default flow style.
        :param int indent: The indentation to apply.
        :param bool allow_unicode: Allows the  decoding of unicode chars.
        :param bool sort_keys: Sorts the keys.
        """

        with open(file_path, "w", encoding=encoding, newline=newline) as file_stream:
            yaml_dump(
                self.main,
                stream=file_stream,
                default_flow_style=default_flow_style,
                indent=indent,
                allow_unicode=allow_unicode,
                line_break=newline,
                encoding=encoding,
                sort_keys=sort_keys,
            )

    @classmethod
    def from_yaml(cls, yaml_str):  # pragma: no cover
        """
        Converts the given YAML string to dict/list.

        :param str yaml_str: The YAML string to convert.

        :rtype: dict|list
        """
        return yaml_load(yaml_str)

    def to_yaml(
        self,
        encoding="utf-8",
        newline="\n",
        default_flow_style=False,
        indent=4,
        allow_unicode=True,
        sort_keys=True,
    ):  # pragma: no cover
        """
        Converts the given dict/list to the YAML format and return
        the result.

        :param str encoding: The encoding to use.
        :param str newline: The newline char string.
        :param bool default_flow_style: Uses the default flow style.
        :param int indent: The indentation to apply.
        :param bool allow_unicode: Allows the decoding of unicode chars.
        :param bool sort_keys: Sors the keys.

        :rtype: dict|list
        """

        return yaml_dump(
            self.main,
            default_flow_style=default_flow_style,
            indent=indent,
            allow_unicode=allow_unicode,
            line_break=newline,
            encoding=encoding,
            sort_keys=sort_keys,
        ).decode()
