#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check domains or IP availability.

::


    :::::::::  :::   ::: :::::::::: :::    ::: ::::    :::  ::::::::  :::::::::: :::::::::  :::        ::::::::::
    :+:    :+: :+:   :+: :+:        :+:    :+: :+:+:   :+: :+:    :+: :+:        :+:    :+: :+:        :+:
    +:+    +:+  +:+ +:+  +:+        +:+    +:+ :+:+:+  +:+ +:+        +:+        +:+    +:+ +:+        +:+
    +#++:++#+    +#++:   :#::+::#   +#+    +:+ +#+ +:+ +#+ +#+        +#++:++#   +#++:++#+  +#+        +#++:++#
    +#+           +#+    +#+        +#+    +#+ +#+  +#+#+# +#+        +#+        +#+    +#+ +#+        +#+
    #+#           #+#    #+#        #+#    #+# #+#   #+#+# #+#    #+# #+#        #+#    #+# #+#        #+#
    ###           ###    ###         ########  ###    ####  ########  ########## #########  ########## ##########

This submodule will provide the class related to the directory structure.

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
import PyFunceble
from PyFunceble import directory_separator, mkdir, path, rename, requests, walk
from PyFunceble.auto_save import AutoSave
from PyFunceble.helpers import Command, Dict, File, Hash, Regex


class DirectoryStructure(object):  # pragma: no cover
    """
    Consider this class as a backup/reconstructor of desired directory.
    (By default, the output direcctory)
    """

    def __init__(self, production=False):
        if PyFunceble.OUTPUTS["main"]:
            self.base = PyFunceble.OUTPUTS["main"]
        else:
            self.base = PyFunceble.CURRENT_DIRECTORY

        if not self.base.endswith(directory_separator):
            self.base += directory_separator

        self.structure = self.base + PyFunceble.OUTPUTS["default_files"][
            "dir_structure"
        ]

        if production:
            self.backup()
        else:
            self.restore()

    @classmethod
    def backup(cls):
        """
        Backup the developer state of `output/` in order to make it restorable
            and portable for user.
        """

        output_path = PyFunceble.CURRENT_DIRECTORY + PyFunceble.OUTPUTS[
            "parent_directory"
        ]
        result = {PyFunceble.OUTPUTS["parent_directory"]: {}}

        for root, _, files in walk(output_path):
            directories = root.split(output_path)[1]

            local_result = result[PyFunceble.OUTPUTS["parent_directory"]]

            for file in files:
                file_path = root + directory_separator + file
                file_hash = Hash(file_path, "sha512", True).get()

                lines_in_list = [line.rstrip("\n") for line in open(file_path)]

                formated_content = "@@@".join(lines_in_list)

                local_result = local_result.setdefault(
                    directories,
                    {file: {"sha512": file_hash, "content": formated_content}},
                )

        Dict(result).to_json(
            PyFunceble.CURRENT_DIRECTORY + "dir_structure_production.json"
        )

    def _restore_replace(self):
        """
        Check if we need to replace ".gitignore" to ".keep".
        """

        if path.isdir(self.base + ".git"):
            if "PyFunceble" not in Command("git remote show origin").execute():
                return True

            return False

        return True

    def _update_structure_from_config(self, structure):
        """
        This method update the paths according to configs.

        Argument:
            - structure: dict
                The readed structure.
        """

        to_replace_base = {"output/": PyFunceble.OUTPUTS["parent_directory"]}

        to_replace = {
            "HTTP_Analytic": PyFunceble.OUTPUTS["http_analytic"]["directories"][
                "parent"
            ],
            "HTTP_Analytic/ACTIVE": PyFunceble.OUTPUTS["http_analytic"]["directories"][
                "parent"
            ]
            + PyFunceble.OUTPUTS["http_analytic"]["directories"]["up"],
            "HTTP_Analytic/POTENTIALLY_ACTIVE": PyFunceble.OUTPUTS["http_analytic"][
                "directories"
            ][
                "parent"
            ]
            + PyFunceble.OUTPUTS["http_analytic"]["directories"]["potentially_up"],
            "HTTP_Analytic/POTENTIALLY_INACTIVE": PyFunceble.OUTPUTS["http_analytic"][
                "directories"
            ][
                "parent"
            ]
            + PyFunceble.OUTPUTS["http_analytic"]["directories"]["potentially_down"],
            "domains": PyFunceble.OUTPUTS["domains"]["directory"],
            "domains/ACTIVE": PyFunceble.OUTPUTS["domains"]["directory"]
            + PyFunceble.STATUS["official"]["up"]
            + directory_separator,
            "domains/INACTIVE": PyFunceble.OUTPUTS["domains"]["directory"]
            + PyFunceble.STATUS["official"]["down"]
            + directory_separator,
            "domains/INVALID": PyFunceble.OUTPUTS["domains"]["directory"]
            + PyFunceble.STATUS["official"]["invalid"]
            + directory_separator,
            "hosts": PyFunceble.OUTPUTS["hosts"]["directory"],
            "hosts/ACTIVE": PyFunceble.OUTPUTS["hosts"]["directory"]
            + PyFunceble.STATUS["official"]["up"]
            + directory_separator,
            "hosts/INACTIVE": PyFunceble.OUTPUTS["hosts"]["directory"]
            + PyFunceble.STATUS["official"]["down"]
            + directory_separator,
            "hosts/INVALID": PyFunceble.OUTPUTS["hosts"]["directory"]
            + PyFunceble.STATUS["official"]["invalid"]
            + directory_separator,
            "logs": PyFunceble.OUTPUTS["logs"]["directories"]["parent"],
            "logs/date_format": PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
            + PyFunceble.OUTPUTS["logs"]["directories"]["date_format"],
            "logs/no_referer": PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
            + PyFunceble.OUTPUTS["logs"]["directories"]["no_referer"],
            "logs/percentage": PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
            + PyFunceble.OUTPUTS["logs"]["directories"]["percentage"],
            "logs/whois": PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
            + PyFunceble.OUTPUTS["logs"]["directories"]["whois"],
            "splited": PyFunceble.OUTPUTS["splited"]["directory"],
        }

        structure = Dict(structure).rename_key(to_replace_base)
        structure[PyFunceble.OUTPUTS["parent_directory"]] = Dict(
            structure[PyFunceble.OUTPUTS["parent_directory"]]
        ).rename_key(
            to_replace
        )

        try:
            Dict(structure).to_json(self.structure)
        except FileNotFoundError:
            mkdir(
                directory_separator.join(self.structure.split(directory_separator)[:-1])
            )
            Dict(structure).to_json(self.structure)

        return structure

    def _get_structure(self):
        """
        This method return the structure we are goinng to work with.
        """

        structure_file = ""
        req = ""

        if path.isfile(self.structure):
            structure_file = self.structure
        elif path.isfile(self.base + "dir_structure_production.json"):
            structure_file = self.base + "dir_structure_production.json"
        else:
            if "dev" not in PyFunceble.VERSION:
                req = requests.get(PyFunceble.LINKS["dir_structure"])
            else:
                req = requests.get(
                    PyFunceble.LINKS["dir_structure"].replace("master", "dev")
                )

        if structure_file.endswith("_production.json"):
            structure = Dict().from_json(File(structure_file).read())

            return self._update_structure_from_config(structure)

        elif structure_file.endswith(".json"):
            return Dict().from_json(File(structure_file).read())

        return self._update_structure_from_config(Dict().from_json(req.text))

    @classmethod
    def _create_directory(cls, directory):
        """
        This method create the given directory if it does not exists.
        """

        if not path.isdir(directory):
            AutoSave.travis_permissions()
            mkdir(directory)
            AutoSave.travis_permissions()

    def restore(self):
        """
        Restore the 'output/' directory structure based on the `dir_structure.json` file.
        """

        structure = self._get_structure()

        list_of_key = list(structure.keys())
        structure = structure[list_of_key[0]]
        parent_path = list_of_key[0] + directory_separator

        for directory in structure:
            base = self.base + parent_path + directory + directory_separator

            self._create_directory(base)

            for file in structure[directory]:
                file_path = base + file

                content_to_write = structure[directory][file]["content"]
                online_sha = structure[directory][file]["sha512"]

                content_to_write = Regex(
                    content_to_write, "@@@", escape=True, replace_with="\\n"
                ).replace()

                git_to_keep = file_path.replace("gitignore", "keep")
                keep_to_git = file_path.replace("keep", "gitignore")

                if self._restore_replace():
                    if path.isfile(file_path) and Hash(
                        file_path, "sha512", True
                    ).get() == online_sha:
                        rename(file_path, git_to_keep)
                        write = False
                    else:
                        File(file_path).delete()
                        file_path = git_to_keep
                        write = True
                else:
                    if path.isfile(keep_to_git) and Hash(
                        file_path, "sha512", True
                    ).get() == online_sha:
                        rename(file_path, keep_to_git)
                        write = False
                    else:
                        File(keep_to_git).delete()
                        file_path = keep_to_git
                        write = True

                if write:
                    File(file_path).write(content_to_write + "\n", True)
