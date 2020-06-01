"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the output directory constructor.

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

from os import sep as directory_separator
from os import walk

import PyFunceble


class Constructor:
    """
    Basically a backup/reconstructor of our :code:`output` directory.

    :param bool production:
        Tell the subsystem if we are preparing for production which
        imply the execution of the backup insteam of of the
        "reconstructore" mode.
    """

    def __init__(self, production=False):
        # We set the base directory where we are going to replicate
        # the directory structure.
        self.base = PyFunceble.OUTPUT_DIRECTORY

        if not self.base.endswith(directory_separator):
            # The base path does not ends wiith a directory separator.

            # We append the directory separator to the ends.
            self.base += directory_separator

        # We set the structure base.
        self.structure = self.base + PyFunceble.OUTPUTS.default_files.dir_structure

        if production and PyFunceble.abstracts.Version.is_local_cloned():
            # We are preparing the repository for production.

            # We backup the directory structure.
            self.backup()
        elif "structure_already_generated" not in PyFunceble.INTERN:
            # We are not preparing the repository for production.

            # We restore the directory structure.
            self.restore()

            # We inform all future logic that the generation was
            # already done in the current session.
            PyFunceble.INTERN["structure_already_generated"] = True

    def backup(self):
        """
        Backup the developer state of `output/` in order to make it restorable
        and portable for user.
        """

        PyFunceble.LOGGER.info("Backing up the directory structure..")

        # We set the current output directory path.
        output_path = self.base + PyFunceble.OUTPUTS.parent_directory

        # We initiate the structure base.
        result = {PyFunceble.OUTPUTS.parent_directory: {}}

        for root, _, files in walk(output_path):
            # We loop through the current output directory structure.

            # We get the currently read directory name.
            directories = PyFunceble.helpers.Directory(
                root.split(output_path)[1]
            ).fix_path()

            # We initiate a local variable which will get the structure of the subdirectory.
            local_result = result[PyFunceble.OUTPUTS.parent_directory]

            for file in files:
                # We loop through the list of files.

                # We construct the file path.
                file_path = root + directory_separator + file

                # We get the hash of the file.
                file_hash = PyFunceble.helpers.Hash().file(file_path)

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

                PyFunceble.LOGGER.info(f"{file_path} backed up.")

        # We finally save the directory structure into the production file.
        PyFunceble.helpers.Dict(result).to_json_file(
            self.base + "dir_structure_production.json"
        )

        PyFunceble.LOGGER.info("Backup saved into dir_structure_production.json")

    def _restore_replace(self):
        """
        Check if we need to replace ".gitignore" to ".keep".

        :return: The replacement status.
        :rtype: bool
        """

        if PyFunceble.helpers.Directory(self.base + ".git").exists():
            # The `.git` directory exist.

            if (
                "PyFunceble"
                not in PyFunceble.helpers.Command("git remote show origin").execute()
            ):
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

        :param dict structure: The read structure.
        """

        # We initiate a variable which will map what we have to replace `ouput` to.
        # Indeed, as we allow the user to change directory names directly from the
        # configuration, here we initiate what we have to replace `output/` with.
        to_replace_base_map = {"output/": PyFunceble.OUTPUTS.parent_directory}

        # We map the replacement of other directories.
        to_replace_map = {
            #########################################################################
            #            The following part is there for historical reason.         #
            #########################################################################
            # We get the replacement of the HTTP_Analytic directory from the
            # configuration file.
            "HTTP_Analytic/": PyFunceble.OUTPUTS.analytic.directories.parent,
            # We get the replacement of the HTTP_Analytic/ACTIVE directory from the
            # configuration file.
            "HTTP_Analytic/ACTIVE/": PyFunceble.OUTPUTS.analytic.directories.parent
            + PyFunceble.OUTPUTS.analytic.directories.up,
            "HTTP_Analytic/POTENTIALLY_ACTIVE/": PyFunceble.OUTPUTS.analytic.directories.parent
            + PyFunceble.OUTPUTS.analytic.directories.potentially_up,
            # We get the replacement of the HTTP_Analytic/POTENTIALLY_INACTIVE directory
            # from the configuration file.
            "HTTP_Analytic/POTENTIALLY_INACTIVE/": PyFunceble.OUTPUTS.analytic.directories.parent  # pylint: disable=line-too-long
            + PyFunceble.OUTPUTS.analytic.directories.potentially_down,
            #########################################################################
            #             The previous part is there for historical reason.         #
            #########################################################################
            # We get the replacement of the Analytic directory from the
            # configuration file.
            "Analytic/": PyFunceble.OUTPUTS.analytic.directories.parent,
            # We get the replacement of the Analytic/ACTIVE directory from the
            # configuration file.
            "Analytic/ACTIVE/": PyFunceble.OUTPUTS.analytic.directories.parent
            + PyFunceble.OUTPUTS.analytic.directories.up,
            "Analytic/POTENTIALLY_ACTIVE/": PyFunceble.OUTPUTS.analytic.directories.parent
            + PyFunceble.OUTPUTS.analytic.directories.potentially_up,
            # We get the replacement of the Analytic/POTENTIALLY_INACTIVE directory
            # from the configuration file.
            "Analytic/POTENTIALLY_INACTIVE/": PyFunceble.OUTPUTS.analytic.directories.parent
            + PyFunceble.OUTPUTS.analytic.directories.potentially_down,
            # We get the replacement of the Analytic/SUSPICIOUS directory
            # from the configuration file.
            "Analytic/SUSPICIOUS/": PyFunceble.OUTPUTS.analytic.directories.parent
            + PyFunceble.OUTPUTS.analytic.directories.suspicious,
            # We get the replacement of the complements directory from the
            # configuration file.
            "complements/": PyFunceble.OUTPUTS.complements.directory,
            # We get the replacement of the complements/ACTIVE directory from the
            # configuration file.
            "complements/ACTIVE/": PyFunceble.OUTPUTS.complements.directory
            + PyFunceble.STATUS.official.up,
            # We get the replacement of the complements/INACTIVE directory from the
            # configuration file.
            "complements/INACTIVE/": PyFunceble.OUTPUTS.complements.directory
            + PyFunceble.STATUS.official.down,
            # We get the replacement of the complements/INVALID directory from the
            # configuration file.
            "complements/INVALID/": PyFunceble.OUTPUTS.complements.directory
            + PyFunceble.STATUS.official.invalid,
            # We get the replacement of the complements/VALID directory from the
            # configuration file.
            "complements/VALID/": PyFunceble.OUTPUTS.complements.directory
            + PyFunceble.STATUS.official.valid,
            # We get the replacement of the complements/MALICIOUS directory from the
            # configuration file.
            "complements/MALICIOUS/": PyFunceble.OUTPUTS.complements.directory
            + PyFunceble.STATUS.official.malicious,
            # We get the replacement of the complements/SANE directory from the
            # configuration file.
            "complements/SANE/": PyFunceble.OUTPUTS.complements.directory
            + PyFunceble.STATUS.official.sane,
            # We get the replacement of the domains directory from the
            # configuration file.
            "domains/": PyFunceble.OUTPUTS.domains.directory,
            # We get the replacement of the domains/ACTIVE directory from the
            # configuration file.
            "domains/ACTIVE/": PyFunceble.OUTPUTS.domains.directory
            + PyFunceble.STATUS.official.up,
            # We get the replacement of the domains/INACTIVE directory from the
            # configuration file.
            "domains/INACTIVE/": PyFunceble.OUTPUTS.domains.directory
            + PyFunceble.STATUS.official.down,
            # We get the replacement of the domains/INVALID directory from the
            # configuration file.
            "domains/INVALID/": PyFunceble.OUTPUTS.domains.directory
            + PyFunceble.STATUS.official.invalid,
            # We get the replacement of the domains/VALID directory from the
            # configuration file.
            "domains/VALID/": PyFunceble.OUTPUTS.domains.directory
            + PyFunceble.STATUS.official.valid,
            # We get the replacement of the domains/MALICIOUS directory from the
            # configuration file.
            "domains/MALICIOUS/": PyFunceble.OUTPUTS.domains.directory
            + PyFunceble.STATUS.official.malicious,
            # We get the replacement of the domains/SANE directory from the
            # configuration file.
            "domains/SANE/": PyFunceble.OUTPUTS.domains.directory
            + PyFunceble.STATUS.official.sane,
            # We get the replacement of the hosts directory from the
            # configuration file.
            "hosts/": PyFunceble.OUTPUTS.hosts.directory,
            # We get the replacement of the hosts/ACTIVE directory from the
            # configuration file.
            "hosts/ACTIVE/": PyFunceble.OUTPUTS.hosts.directory
            + PyFunceble.STATUS.official.up,
            # We get the replacement of the hosts/INACTIVE directory from the
            # configuration file.
            "hosts/INACTIVE/": PyFunceble.OUTPUTS.hosts.directory
            + PyFunceble.STATUS.official.down,
            # We get the replacement of the hosts/INVALID directory from the
            # configuration file.
            "hosts/INVALID/": PyFunceble.OUTPUTS.hosts.directory
            + PyFunceble.STATUS.official.invalid,
            # We get the replacement of the hosts/VALID directory from the
            # configuration file.
            "hosts/VALID/": PyFunceble.OUTPUTS.hosts.directory
            + PyFunceble.STATUS.official.valid,
            # We get the replacement of the hosts/MALICIOUS directory from the
            # configuration file.
            "hosts/MALICIOUS/": PyFunceble.OUTPUTS.hosts.directory
            + PyFunceble.STATUS.official.malicious,
            # We get the replacement of the hosts/SANE directory from the
            # configuration file.
            "hosts/SANE/": PyFunceble.OUTPUTS.hosts.directory
            + PyFunceble.STATUS.official.sane,
            # We get the replacement of the json directory from the
            # configuration file.
            "json/": PyFunceble.OUTPUTS.json.directory,
            # We get the replacement of the json/ACTIVE directory from the
            # configuration file.
            "json/ACTIVE/": PyFunceble.OUTPUTS.json.directory
            + PyFunceble.STATUS.official.up,
            # We get the replacement of the json/INACTIVE directory from the
            # configuration file.
            "json/INACTIVE/": PyFunceble.OUTPUTS.json.directory
            + PyFunceble.STATUS.official.down,
            # We get the replacement of the json/INVALID directory from the
            # configuration file.
            "json/INVALID/": PyFunceble.OUTPUTS.json.directory
            + PyFunceble.STATUS.official.invalid,
            # We get the replacement of the json/VALID directory from the
            # configuration file.
            "json/VALID/": PyFunceble.OUTPUTS.json.directory
            + PyFunceble.STATUS.official.valid,
            # We get the replacement of the json/MALICIOUS directory from the
            # configuration file.
            "json/MALICIOUS/": PyFunceble.OUTPUTS.json.directory
            + PyFunceble.STATUS.official.malicious,
            # We get the replacement of the json/SANE directory from the
            # configuration file.
            "json/SANE/": PyFunceble.OUTPUTS.json.directory
            + PyFunceble.STATUS.official.sane,
            # We get the replacement of the logs directory from the
            # configuration file.
            "logs/": PyFunceble.OUTPUTS.logs.directories.parent,
            # We get the replacement of the logs/percentage directory from the
            # configuration file.
            "logs/percentage/": PyFunceble.OUTPUTS.logs.directories.parent
            + PyFunceble.OUTPUTS.logs.directories.percentage,
            # We get the replacement of the splited directory from the
            # configuration file.
            "splited/": PyFunceble.OUTPUTS.splited.directory,
        }

        # We initiate the variable which will be used for the structure
        # update.
        to_replace = {}

        for mapped, declared in to_replace_map.items():
            # We loop through the declared mad.

            # We fix the path of the declared.
            declared = PyFunceble.helpers.Directory(declared).fix_path()

            # And we update our data.
            to_replace.update({mapped: declared})

        to_replace_base = {}
        for mapped, declared in to_replace_base_map.items():
            # We loop through the declared mad.

            # We fix the path of the declared.
            declared = PyFunceble.helpers.Directory(declared).fix_path()

            # And we update our data.
            to_replace_base.update({mapped: declared})

        # We perform the replacement of the base directory.
        structure = PyFunceble.helpers.Dict(structure).rename_key(to_replace_base)

        # We perform the replacement of every subdirectories.
        structure[PyFunceble.OUTPUTS.parent_directory] = PyFunceble.helpers.Dict(
            structure[PyFunceble.OUTPUTS.parent_directory]
        ).rename_key(to_replace)

        try:
            # We try to save the structure into the right path.

            PyFunceble.helpers.Dict(structure).to_json_file(self.structure)
        except FileNotFoundError:
            # But if we get a FileNotFoundError exception,

            to_create = directory_separator.join(
                self.structure.split(directory_separator)[:-1]
            )

            # We create the directory where the directory structure should be saved.
            PyFunceble.helpers.Directory(to_create).create()

            # And we retry to save the structure into the right path.
            PyFunceble.helpers.Dict(structure).to_json_file(self.structure)

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

        if PyFunceble.helpers.File(self.structure).exists():
            # The structure path file exist.

            # We set it as the destination file.
            structure_file = self.structure
        elif PyFunceble.helpers.File(
            self.base + "dir_structure_production.json"
        ).exists():
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
                req = PyFunceble.REQUESTS.get(
                    PyFunceble.LINKS.dir_structure.replace("dev", "master")
                )
            else:
                # `dev` is into the local version name.

                # We get the production file from the dev branch.
                req = PyFunceble.REQUESTS.get(
                    PyFunceble.LINKS.dir_structure.replace("master", "dev")
                )

        if structure_file.endswith("_production.json"):
            # The destination is the production file.

            # And we return the updated the structure from the last read file.
            # (with the names from the configuration file).
            return self._update_structure_from_config(
                PyFunceble.helpers.Dict().from_json_file(structure_file)
            )

        # The destination is not the production file.

        if structure_file.endswith(".json"):
            # The destination ends with `.json`.

            # And we return the updated the structure from the given file.
            # (with the names from the configuration file).
            return self._update_structure_from_config(
                PyFunceble.helpers.Dict().from_json_file(structure_file)
            )

        # The destination does not ends with `.json`.

        # We return the updated the structure from the link we previously got.
        # (with the names from the configuration file).
        return self._update_structure_from_config(
            PyFunceble.helpers.Dict().from_json(req.text)
        )

    @classmethod
    def _create_directory(cls, directory, loop=False):
        """
        Creates the given directory if it does not exists.

        :param str directory: The directory to create.

        :param bool loop: Tell us if we are in the creation loop or not.
        """

        if not loop and directory_separator in directory:
            # * We are not in the loop.
            # and
            # * The directory separator in the given directory.

            # We split the directories separator.
            splited_directory = directory.split(directory_separator)

            # We initiate a variable which will save the full path to create.
            full_path_to_create = ""

            for single_directory in splited_directory:
                # We loop through each directory.

                # We append the currently read directory to the full path.
                full_path_to_create += single_directory + directory_separator

                # And we create the directory if it does not exist.
                cls._create_directory(full_path_to_create, True)

        if not PyFunceble.helpers.Directory(directory).exists():
            # The given directory does not exist.

            ci_engine = PyFunceble.engine.AutoSave.get_current_ci()

            if ci_engine:
                # We update the permission.
                # (Only if we are under CI.)
                ci_engine.permissions()

            # We create the directory.
            PyFunceble.helpers.Directory(directory).create()

            if ci_engine:
                # We update the permission.
                # (Only if we are under CI.)
                ci_engine.permissions()

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

        if not parent_path.endswith(directory_separator):
            parent_path += directory_separator

        # We get if we have to replace `.gitignore` to `.keep` and versa.
        replacement_status = self._restore_replace()

        for directory in structure:
            # We loop through the list of directory to create.

            # We construct the full path.
            base = self.base + parent_path + directory

            if not base.endswith(directory_separator):
                base += directory_separator

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
                content_to_write = PyFunceble.helpers.Regex(
                    "@@@", escape=True
                ).replace_match(content_to_write, "\\n")

                # We get the file path as .keep.
                git_to_keep = file_path.replace("gitignore", "keep")

                # We get the file path as .gitignore.
                keep_to_git = file_path.replace("keep", "gitignore")

                if replacement_status:
                    # We have to replace every .gitignore to .keep.

                    if (
                        PyFunceble.helpers.File(file_path).exists()
                        and PyFunceble.helpers.Hash().file(file_path) == online_sha
                    ):
                        # * The currently read file exist.
                        # and
                        # * Its sha512sum is equal to the one we have in our structure.

                        # We rename the file.
                        PyFunceble.helpers.File(file_path).move(git_to_keep)

                        # And we disallow the file writing.
                        write = False
                    else:
                        # * The currently read file does not exist.
                        # or
                        # * Its sha512sum is not equal to the one we have in our structure.

                        # We delere the file if it does exist.
                        PyFunceble.helpers.File(file_path).delete()

                        # We update the file path.
                        file_path = git_to_keep

                        # And we allow the file writing.
                        write = True
                else:
                    # We have to replace every .keep to .gitignore.
                    if (
                        PyFunceble.helpers.File(keep_to_git).exists()
                        and PyFunceble.helpers.Hash().file(file_path) == online_sha
                    ):
                        # * The .keep file exist.
                        # and
                        # * Its sha512sum is equal to the one we have in our structure.

                        # We rename the file.
                        PyFunceble.helpers.File(file_path).move(keep_to_git)

                        # And we disallow the file writing.
                        write = False
                    else:
                        # * The .keep file does not exist.
                        # or
                        # * Its sha512sum is not equal to the one we have in our structure.

                        # We delete the file if it exist.
                        PyFunceble.helpers.File(keep_to_git).delete()

                        # We update the file path
                        file_path = keep_to_git

                        # And we allow the file writing.
                        write = True

                if write:
                    # The file writing is allowed.

                    # We write our file content into the file path.
                    PyFunceble.helpers.File(file_path).write(
                        content_to_write + "\n", True
                    )

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

        if not parent_path.endswith(directory_separator):
            parent_path += directory_separator

        for root, _, _ in walk(parent_path):
            # We loop through each directories of the parent path.

            # We fix the path in order to avoid issues.
            root = PyFunceble.helpers.Directory(root).fix_path()

            if root.replace(parent_path, "") not in structure:
                # The currently read directory is not in our structure.

                # We delete it.
                PyFunceble.helpers.Directory(root).delete()

                PyFunceble.LOGGER.info(f"Deleted {repr(root)}.")
