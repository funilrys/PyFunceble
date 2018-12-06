#!/usr/bin/env python3

# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will provide the directory structure management subsystem.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

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
from PyFunceble.auto_save import AutoSave
from PyFunceble.config import Version
from PyFunceble.helpers import Command, Dict, Directory, File, Hash, Regex


class DirectoryStructure:  # pragma: no cover
    """
    Basically a backup/reconstructor of our :code:`output` directory.

    :param production:
        Tell the subsystem if we are preparing for production which
        imply the execution of the backup insteam of of the
        "reconstructore" mode.
    :type production: bool
    """

    def __init__(self, production=False):
        # We set the base directory where we are going to replicate
        # the directory structure.
        self.base = PyFunceble.OUTPUT_DIRECTORY

        if not self.base.endswith(PyFunceble.directory_separator):
            # The base path does not ends wiith a directory separator.

            # We append the directory separator to the ends.
            self.base += PyFunceble.directory_separator

        # We set the structure base.
        self.structure = (
            self.base + PyFunceble.OUTPUTS["default_files"]["dir_structure"]
        )

        if production and Version(True).is_cloned():
            # We are preparing the repository for production.

            # We backup the directory structure.
            self.backup()
        else:
            # We are not preparing the repository for production.

            # We restore the directory structure.
            self.restore()

    def backup(self):
        """
        Backup the developer state of `output/` in order to make it restorable
            and portable for user.
        """

        # We set the current output directory path.
        output_path = self.base + PyFunceble.OUTPUTS["parent_directory"]

        # We initiate the structure base.
        result = {PyFunceble.OUTPUTS["parent_directory"]: {}}

        for root, _, files in PyFunceble.walk(output_path):
            # We loop through the current output directory structure.

            # We get the currently read directory name.
            directories = Directory(root.split(output_path)[1]).fix_path()

            # We initiate a local variable which will get the structure of the subdirectory.
            local_result = result[PyFunceble.OUTPUTS["parent_directory"]]

            for file in files:
                # We loop through the list of files.

                # We construct the file path.
                file_path = root + PyFunceble.directory_separator + file

                # We get the hash of the file.
                file_hash = Hash(file_path, "sha512", True).get()

                # We convert the file content to a list.
                lines_in_list = [line.rstrip("\n") for line in open(file_path)]

                # We convert the file content into a more flat format.
                # We use `@@@` as glue and implicitly replacement for `\n`.
                formatted_content = "@@@".join(lines_in_list)

                # We update the local result (and implicitly the global result)
                # with the files and directory informations/structure.
                local_result = local_result.setdefault(
                    directories,
                    {file: {"sha512": file_hash, "content": formatted_content}},
                )

        # We finally save the directory structure into the production file.
        Dict(result).to_json(self.base + "dir_structure_production.json")

    def _restore_replace(self):
        """
        Check if we need to replace ".gitignore" to ".keep".

        :return: The replacement status.
        :rtype: bool
        """

        if PyFunceble.path.isdir(self.base + ".git"):
            # The `.git` directory exist.

            if "PyFunceble" not in Command("git remote show origin").execute():
                # PyFunceble is not in the origin.

                # We return True.
                return True

            # We return False.
            return False

        # The `.git` directory does not exist.

        # We return True.
        return True

    def _update_structure_from_config(self, structure):
        """
        Update the paths according to configs.

        :param structure: The read structure.
        :type structure: dict
        """

        # We initiate a variable which will map what we have to replace `ouput` to.
        # Indeed, as we allow the user to change directory names directly from the
        # configuration, here we initiate what we have to replace `output/` with.
        to_replace_base_map = {"output/": PyFunceble.OUTPUTS["parent_directory"]}

        # We map the replacement of other directories.
        to_replace_map = {
            #########################################################################
            #            The following part is there for historical reason.         #
            #########################################################################
            # We get the replacement of the HTTP_Analytic directory from the
            # configuration file.
            "HTTP_Analytic": PyFunceble.OUTPUTS["analytic"]["directories"]["parent"],
            # We get the replacement of the HTTP_Analytic/ACTIVE directory from the
            # configuration file.
            "HTTP_Analytic/ACTIVE": PyFunceble.OUTPUTS["analytic"]["directories"][
                "parent"
            ]
            + PyFunceble.OUTPUTS["analytic"]["directories"]["up"],
            "HTTP_Analytic/POTENTIALLY_ACTIVE": PyFunceble.OUTPUTS["analytic"][
                "directories"
            ]["parent"]
            + PyFunceble.OUTPUTS["analytic"]["directories"]["potentially_up"],
            # We get the replacement of the HTTP_Analytic/POTENTIALLY_INACTIVE directory
            # from the configuration file.
            "HTTP_Analytic/POTENTIALLY_INACTIVE": PyFunceble.OUTPUTS["analytic"][
                "directories"
            ]["parent"]
            + PyFunceble.OUTPUTS["analytic"]["directories"]["potentially_down"],
            #########################################################################
            #             The previous part is there for historical reason.         #
            #########################################################################
            # We get the replacement of the Analytic directory from the
            # configuration file.
            "Analytic": PyFunceble.OUTPUTS["analytic"]["directories"]["parent"],
            # We get the replacement of the Analytic/ACTIVE directory from the
            # configuration file.
            "Analytic/ACTIVE": PyFunceble.OUTPUTS["analytic"]["directories"]["parent"]
            + PyFunceble.OUTPUTS["analytic"]["directories"]["up"],
            "Analytic/POTENTIALLY_ACTIVE": PyFunceble.OUTPUTS["analytic"][
                "directories"
            ]["parent"]
            + PyFunceble.OUTPUTS["analytic"]["directories"]["potentially_up"],
            # We get the replacement of the Analytic/POTENTIALLY_INACTIVE directory
            # from the configuration file.
            "Analytic/POTENTIALLY_INACTIVE": PyFunceble.OUTPUTS["analytic"][
                "directories"
            ]["parent"]
            + PyFunceble.OUTPUTS["analytic"]["directories"]["potentially_down"],
            # We get the replacement of the domains directory from the
            # configuration file.
            "domains": PyFunceble.OUTPUTS["domains"]["directory"],
            # We get the replacement of the domains/ACTIVE directory from the
            # configuration file.
            "domains/ACTIVE": PyFunceble.OUTPUTS["domains"]["directory"]
            + PyFunceble.STATUS["official"]["up"],
            # We get the replacement of the domains/INACTIVE directory from the
            # configuration file.
            "domains/INACTIVE": PyFunceble.OUTPUTS["domains"]["directory"]
            + PyFunceble.STATUS["official"]["down"],
            # We get the replacement of the domains/INVALID directory from the
            # configuration file.
            "domains/INVALID": PyFunceble.OUTPUTS["domains"]["directory"]
            + PyFunceble.STATUS["official"]["invalid"],
            # We get the replacement of the domains/VALID directory from the
            # configuration file.
            "domains/VALID": PyFunceble.OUTPUTS["domains"]["directory"]
            + PyFunceble.STATUS["official"]["valid"],
            # We get the replacement of the hosts directory from the
            # configuration file.
            "hosts": PyFunceble.OUTPUTS["hosts"]["directory"],
            # We get the replacement of the hosts/ACTIVE directory from the
            # configuration file.
            "hosts/ACTIVE": PyFunceble.OUTPUTS["hosts"]["directory"]
            + PyFunceble.STATUS["official"]["up"],
            # We get the replacement of the hosts/INACTIVE directory from the
            # configuration file.
            "hosts/INACTIVE": PyFunceble.OUTPUTS["hosts"]["directory"]
            + PyFunceble.STATUS["official"]["down"],
            # We get the replacement of the hosts/INVALID directory from the
            # configuration file.
            "hosts/INVALID": PyFunceble.OUTPUTS["hosts"]["directory"]
            + PyFunceble.STATUS["official"]["invalid"],
            # We get the replacement of the hosts/VALID directory from the
            # configuration file.
            "hosts/VALID": PyFunceble.OUTPUTS["hosts"]["directory"]
            + PyFunceble.STATUS["official"]["valid"],
            # We get the replacement of the json directory from the
            # configuration file.
            "json": PyFunceble.OUTPUTS["json"]["directory"],
            # We get the replacement of the json/ACTIVE directory from the
            # configuration file.
            "json/ACTIVE": PyFunceble.OUTPUTS["json"]["directory"]
            + PyFunceble.STATUS["official"]["up"],
            # We get the replacement of the json/INACTIVE directory from the
            # configuration file.
            "json/INACTIVE": PyFunceble.OUTPUTS["json"]["directory"]
            + PyFunceble.STATUS["official"]["down"],
            # We get the replacement of the json/INVALID directory from the
            # configuration file.
            "json/INVALID": PyFunceble.OUTPUTS["json"]["directory"]
            + PyFunceble.STATUS["official"]["invalid"],
            # We get the replacement of the json/VALID directory from the
            # configuration file.
            "json/VALID": PyFunceble.OUTPUTS["json"]["directory"]
            + PyFunceble.STATUS["official"]["valid"],
            # We get the replacement of the logs directory from the
            # configuration file.
            "logs": PyFunceble.OUTPUTS["logs"]["directories"]["parent"],
            # We get the replacement of the logs/percentage directory from the
            # configuration file.
            "logs/percentage": PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
            + PyFunceble.OUTPUTS["logs"]["directories"]["percentage"],
            # We get the replacement of the splited directory from the
            # configuration file.
            "splited": PyFunceble.OUTPUTS["splited"]["directory"],
        }

        # We initiate the variable which will be used for the structure
        # update.
        to_replace = {}

        for mapped, declared in to_replace_map.items():
            # We loop through the declared mad.

            # We fix the path of the index.
            mapped = Directory(mapped).fix_path()

            # We fix the path of the declared.
            declared = Directory(declared).fix_path()
            # print('dec', declared, 'map', mapped)

            # And we update our data.
            to_replace.update({mapped: declared})

        to_replace_base = {}
        for mapped, declared in to_replace_base_map.items():
            # We loop through the declared mad.

            # We fix the path of the index.
            mapped = Directory(mapped).fix_path()

            # We fix the path of the declared.
            declared = Directory(declared).fix_path()
            # print('dec', declared, 'map', mapped)

            # And we update our data.
            to_replace_base_map.update({mapped: declared})

        # We perform the replacement of the base directory.
        structure = Dict(structure).rename_key(to_replace_base)

        # We perform the replacement of every subdirectories.
        structure[PyFunceble.OUTPUTS["parent_directory"]] = Dict(
            structure[PyFunceble.OUTPUTS["parent_directory"]]
        ).rename_key(to_replace)

        try:
            # We try to save the structure into the right path.

            Dict(structure).to_json(self.structure)
        except FileNotFoundError:
            # But if we get a FileNotFoundError exception,

            # We create the directory where the directory structure should be saved.
            PyFunceble.mkdir(
                PyFunceble.directory_separator.join(
                    self.structure.split(PyFunceble.directory_separator)[:-1]
                )
            )

            # And we retry to save the structure into the right path.
            Dict(structure).to_json(self.structure)

        # We finaly return the new structure in case it's needed for other logic.
        return structure

    def _get_structure(self):
        """
        Get the structure we are going to work with.

        :return: The structure we have to work with.
        :rtype: dict
        """

        # We initiate an empty variable which is going to save the location of
        # file we are going to download.
        structure_file = ""

        # We initiate the variable which will save the request instance.
        req = ""

        if PyFunceble.path.isfile(self.structure):
            # The structure path file exist.

            # We set it as the destination file.
            structure_file = self.structure
        elif PyFunceble.path.isfile(self.base + "dir_structure_production.json"):
            # * The structure path file does not exist.
            # but
            # * The production structure path file exist.

            # We set it as the destination file
            structure_file = self.base + "dir_structure_production.json"
        else:
            # * The structure path file does not exist.
            # and
            # * The production structure path file does not exist.

            if "dev" not in PyFunceble.VERSION:
                # `dev` is not into the local version name.

                # We get the production file from the master branch.
                req = PyFunceble.requests.get(
                    PyFunceble.LINKS["dir_structure"].replace("dev", "master")
                )
            else:
                # `dev` is into the local version name.

                # We get the production file from the dev branch.
                req = PyFunceble.requests.get(
                    PyFunceble.LINKS["dir_structure"].replace("master", "dev")
                )

        if structure_file.endswith("_production.json"):
            # The destination is the production file.

            # And we return the updated the structure from the last read file.
            # (with the names from the configuration file).
            return self._update_structure_from_config(
                Dict().from_json(File(structure_file).read())
            )

        # The destination is not the production file.

        if structure_file.endswith(".json"):
            # The destination ends with `.json`.

            # And we return the updated the structure from the given file.
            # (with the names from the configuration file).
            return self._update_structure_from_config(
                Dict().from_json(File(structure_file).read())
            )

        # The destination does not ends with `.json`.

        # We return the updated the structure from the link we previously got.
        # (with the names from the configuration file).
        return self._update_structure_from_config(Dict().from_json(req.text))

    @classmethod
    def _create_directory(cls, directory, loop=False):
        """
        Creates the given directory if it does not exists.

        :param directory: The directory to create.
        :type directory: str

        :param loop: Tell us if we are in the creation loop or not.
        :type loop: bool
        """

        if not loop and PyFunceble.directory_separator in directory:
            # * We are not in the loop.
            # and
            # * The directory separator in the given directory.

            # We split the directories separator.
            splited_directory = directory.split(PyFunceble.directory_separator)

            # We initiate a variable which will save the full path to create.
            full_path_to_create = ""

            for single_directory in splited_directory:
                # We loop through each directory.

                # We append the currently read directory to the full path.
                full_path_to_create += single_directory + PyFunceble.directory_separator

                # And we create the directory if it does not exist.
                cls._create_directory(full_path_to_create, True)

        if not PyFunceble.path.isdir(directory):
            # The given directory does not exist.

            # We update the permission.
            # (Only if we are under Travis CI.)
            AutoSave.travis_permissions()

            # We create the directory.
            PyFunceble.mkdir(directory)

            # We update the permission.
            # (Only if we are under Travis CI.)
            AutoSave.travis_permissions()

    def restore(self):
        """
        Restore the 'output/' directory structure based on the `dir_structure.json` file.
        """

        # We get the structure we have to create/apply.
        structure = self._get_structure()

        # We get the list of key which is implicitly the list of directory to recreate.
        list_of_key = list(structure.keys())

        # We move to the content of the parent as we know that we are creating only one directory.
        # Note: if one day we will have to create multiple directory, we will have to change
        # the following.
        structure = structure[list_of_key[0]]

        # We also set the parent directory as we are going to construct its childen.
        parent_path = list_of_key[0]

        if not parent_path.endswith(PyFunceble.directory_separator):
            parent_path += PyFunceble.directory_separator

        # We get if we have to replace `.gitignore` to `.keep` and versa.
        replacement_status = self._restore_replace()

        for directory in structure:
            # We loop through the list of directory to create.

            # We construct the full path.
            base = self.base + parent_path + directory

            if not base.endswith(PyFunceble.directory_separator):
                base += PyFunceble.directory_separator

            # We create the constructed path if it does not exist.
            self._create_directory(base)

            for file in structure[directory]:
                # We loop through the list of files in the currently read directory.

                # We construct the full file path.s
                file_path = base + file

                # We get the file content.
                content_to_write = structure[directory][file]["content"]

                # And its sha512 checksum.
                online_sha = structure[directory][file]["sha512"]

                # We update the content to write by replacing our glue with `\n`.
                content_to_write = Regex(
                    content_to_write, "@@@", escape=True, replace_with="\\n"
                ).replace()

                # We get the file path as .keep.
                git_to_keep = file_path.replace("gitignore", "keep")

                # We get the file path as .gitignore.
                keep_to_git = file_path.replace("keep", "gitignore")

                if replacement_status:
                    # We have to replace every .gitignore to .keep.

                    if (
                        PyFunceble.path.isfile(file_path)
                        and Hash(file_path, "sha512", True).get() == online_sha
                    ):
                        # * The currently read file exist.
                        # and
                        # * Its sha512sum is equal to the one we have in our structure.

                        # We rename the file.
                        PyFunceble.rename(file_path, git_to_keep)

                        # And we disallow the file writing.
                        write = False
                    else:
                        # * The currently read file does not exist.
                        # or
                        # * Its sha512sum is not equal to the one we have in our structure.

                        # We delere the file if it does exist.
                        File(file_path).delete()

                        # We update the file path.
                        file_path = git_to_keep

                        # And we allow the file writing.
                        write = True
                else:
                    # We have to replace every .keep to .gitignore.
                    if (
                        PyFunceble.path.isfile(keep_to_git)
                        and Hash(file_path, "sha512", True).get() == online_sha
                    ):
                        # * The .keep file exist.
                        # and
                        # * Its sha512sum is equal to the one we have in our structure.

                        # We rename the file.
                        PyFunceble.rename(file_path, keep_to_git)

                        # And we disallow the file writing.
                        write = False
                    else:
                        # * The .keep file does not exist.
                        # or
                        # * Its sha512sum is not equal to the one we have in our structure.

                        # We delete the file if it exist.
                        File(keep_to_git).delete()

                        # We update the file path
                        file_path = keep_to_git

                        # And we allow the file writing.
                        write = True

                if write:
                    # The file writing is allowed.

                    # We write our file content into the file path.
                    File(file_path).write(content_to_write + "\n", True)
        self.delete_uneeded()

    def delete_uneeded(self):
        """
        Delete the directory which are not registered into our structure.
        """

        # We get the structure we have to apply.
        structure = self._get_structure()

        # We get the list of key which is implicitly the list of directory we do not bave to delete.
        list_of_key = list(structure.keys())

        # We move to the content of the parent as we know that we are creating only one directory.
        # Note: if one day we will have to create multiple directory, we will have to change
        # the following.
        structure = structure[list_of_key[0]]

        # We also set the parent directory as we are going to construct its childen.
        parent_path = list_of_key[0]

        if not parent_path.endswith(PyFunceble.directory_separator):
            parent_path += PyFunceble.directory_separator

        for root, _, _ in PyFunceble.walk(parent_path):
            # We loop through each directories of the parent path.

            # We fix the path in order to avoid issues.
            root = Directory(root).fix_path()

            if root.replace(parent_path, "") not in structure:
                # The currently read directory is not in our structure.

                # We delete it.
                PyFunceble.rmtree(root)
