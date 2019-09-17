# pylint: disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provide the configuration loader.

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


    MIT License

    Copyright (c) 2017, 2018, 2019 Nissar Chababy

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

from box import Box

import PyFunceble
from PyFunceble.helpers import Dict, Directory, Download, File

from .version import Version


class Load:  # pylint: disable=too-few-public-methods
    """
    Help us load the configuration(s) file(s).

    :param str path_to_config: The possible path to the configuration to load.
    """

    def __init__(self, path_to_config, custom=None):
        # We initiate the vairable which will provides the configuration content.
        self.data = Box({}, default_box=True, default_box_attr=None)

        # We initiate 2 variables:
        #   * One with the path to the config file
        #   * The second one is the path to the default configuration file which is
        #   used only if the first one is not found.
        self.path_to_config, self.path_to_default_config = self._set_path_to_configs(
            path_to_config
        )

        self.version = Version(True)

        if "config_loaded" not in PyFunceble.INTERN:
            self.__load_it()
            self.__fix_paths()
        self.__set_it(custom)

    def __load_it(self):
        """
        Load the configuration and everything needed aroud it.
        """

        try:
            # We try to load the configuration.
            self._load_config_file()
        except FileNotFoundError:
            # We got a FileNotFoundError

            if "PYFUNCEBLE_AUTO_CONFIGURATION" not in PyFunceble.environ:
                # `PYFUNCEBLE_AUTO_CONFIGURATION` is not into the environnements variables.

                while True:
                    # We infinitly loop until we get a reponse which is `y|Y` or `n|N`.

                    # We ask the user if we should install and load the default configuration.
                    response = input(
                        "%s was not found.\n\
Install and load the default configuration at the mentioned location? [y/n] "
                        % (
                            PyFunceble.Style.BRIGHT
                            + self.path_to_config
                            + PyFunceble.Style.RESET_ALL
                        )
                    )

                    if isinstance(response, str):
                        # The response is a string

                        if response.lower() == "y":
                            # The response is a `y` or `Y`.

                            # We install the production configuration.
                            self._install_production_config()

                            # We load the installed configuration.
                            self._load_config_file()

                            # And we break the loop as we got a satisfied response.
                            break

                        elif response.lower() == "n":
                            # The response is a `n` or `N`.

                            # We inform the user that something went wrong.
                            raise Exception("Unable to find the configuration file.")

            else:
                # `PYFUNCEBLE_AUTO_CONFIGURATION` is not into the environnements variables.

                # We install the production configuration.
                self._install_production_config()

                # We load the installed configuration.
                self._load_config_file()

    def __fix_paths(self):
        """
        Fix all paths.
        """

        for main_key in [
            "domains",
            "hosts",
            "splited",
            "json",
            "complements",
            "db_type",
        ]:
            # We loop through the key which contain paths under the `outputs` index.

            try:
                # And we fix the path.
                # Which means: If they do not end with the directory separator, we append
                # it to the end.
                self.data["outputs"][main_key]["directory"] = Directory(
                    self.data["outputs"][main_key]["directory"]
                ).fix_path()
            except KeyError:
                pass

        for main_key in ["analytic", "logs"]:
            # We loop through the key which are more deeper under the `outputs` index.

            for key, value in self.data["outputs"][main_key]["directories"].items():
                # We loop through the more deeper indexes.

                # And we fix the path.
                # Which means: If they do not end with the directory separator, we append
                # it to the end.
                self.data["outputs"][main_key]["directories"][key] = Directory(
                    value
                ).fix_path()

        # We fix the path.
        # Which means: If they do not end with the directory separator, we append
        # it to the end.
        self.data["outputs"]["parent_directory"] = Directory(
            self.data["outputs"]["parent_directory"]
        ).fix_path()

    def __set_it(self, custom):
        """
        Set the configuration at its final location and load the complementary infos.
        """

        if "config_loaded" not in PyFunceble.INTERN:
            PyFunceble.CONFIGURATION = self.data

        if custom and isinstance(custom, dict):
            # @TODO: Delete this in the future.
            # We update the index which was renamed.
            if "seconds_before_http_timeout" in custom:
                custom["timeout"] = custom["seconds_before_http_timeout"]
                del custom["seconds_before_http_timeout"]

            PyFunceble.CONFIGURATION.update(custom)

            # We save the fact the the custom was loaded.
            PyFunceble.INTERN.update(
                {"custom_loaded": True, "custom_config_loaded": custom}
            )

        if "config_loaded" not in PyFunceble.INTERN:
            PyFunceble.STATUS = PyFunceble.CONFIGURATION.status
            PyFunceble.OUTPUTS = PyFunceble.CONFIGURATION.outputs
            PyFunceble.HTTP_CODE = PyFunceble.CONFIGURATION.http_codes
            PyFunceble.LINKS = PyFunceble.CONFIGURATION.links

            # Those 2 strings are used to say if something like the cleaning went right (done)
            # or wrong (error).
            PyFunceble.INTERN.update(
                {
                    "done": PyFunceble.Fore.GREEN + "✔",
                    "error": PyFunceble.Fore.RED + "✘",
                }
            )

            # We load the PSL database.
            PyFunceble.PublicSuffix().load()

            # We load the IANA database.
            PyFunceble.IANA().load()

            PyFunceble.INTERN.update({"config_loaded": True})

    @classmethod
    def _set_path_to_configs(cls, path_to_config):
        """
        Set the paths to the configuration files.

        :param str path_to_config: The possible path to the config to load.

        :return:
            The path to the config to read (0), the path to the default
            configuration to read as fallback.(1)
        :rtype: tuple
        """

        if not path_to_config.endswith(PyFunceble.directory_separator):
            # The path to the config does not ends with the directory separator.

            # We initiate the default and the parsed variable with the directory separator.
            default = parsed = path_to_config + PyFunceble.directory_separator
        else:
            # The path to the config does ends with the directory separator.

            # We initiate the default and the parsed variable.
            default = parsed = path_to_config

        # We append the `CONFIGURATION_FILENAME` to the parsed variable.
        parsed += PyFunceble.CONFIGURATION_FILENAME
        # And we append the `DEFAULT_CONFIGURATION_FILENAME` to the default variable.
        default += PyFunceble.DEFAULT_CONFIGURATION_FILENAME

        # We finaly return a tuple which contain both informations.
        return (parsed, default)

    def _load_config_file(self):
        """
        Load .PyFunceble.yaml into the system.
        """

        try:
            # We try to load the configuration file.

            self.data.update(Dict.from_yaml(File(self.path_to_config).read()))

            # We install the latest iana configuration file.
            self._install_iana_config()

            # We install the latest public suffix configuration file.
            self._install_psl_config()

            # We install the latest directory structure file.
            self._install_directory_structure_file()

            # We install the db types files.
            self._install_db_type_files()
        except FileNotFoundError as exception:
            # But if the configuration file is not found.

            if PyFunceble.path.isfile(self.path_to_default_config):
                # The `DEFAULT_CONFIGURATION_FILENAME` file exists.

                # We copy it as the configuration file.
                File(self.path_to_default_config).copy(self.path_to_config)

                # And we load the configuration file as it does exist (yet).
                self._load_config_file()
            else:
                # The `DEFAULT_CONFIGURATION_FILENAME` file does not exists.

                # We raise the exception we were handling.
                raise exception

    def _install_production_config(self):
        """
        Download the production configuration and install it in the
        current directory.
        """

        # We initiate the link to the production configuration.
        # It is not hard coded because this method is called only if we
        # are sure that the configuration file exist.
        production_config_link = "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/.PyFunceble_production.yaml"  # pylint: disable=line-too-long

        # We update the link according to our current version.
        production_config_link = self.version.right_url_from_version(
            production_config_link
        )

        if not self.version.is_cloned():
            # The current version is not the cloned one.

            # We download the link content and save it inside the default location.
            #
            # Note: We add this one in order to allow the enduser to always have
            # a copy of our upstream configuration file.
            Download(production_config_link, self.path_to_default_config).text()

        # And we download the link content and return the download status.
        return Download(production_config_link, self.path_to_config).text()

    def _install_db_type_files(self):
        """
        Create the .db_type directory if it does not exists and update
        its content.
        """

        if not self.version.is_cloned():
            # * The current version is not the cloned version.
            # and
            # * The database type is not JSON.

            destination_dir = (
                PyFunceble.CONFIG_DIRECTORY
                + self.data["outputs"]["db_type"]["directory"]
                + PyFunceble.directory_separator
            )

            if not PyFunceble.path.isdir(destination_dir):
                PyFunceble.mkdir(destination_dir)

            # We set the list of index to download.
            index_to_download = ["mariadb", "mysql"]

            for index in index_to_download:
                # We loop through the list of indexes.

                # We create the right link.
                link_to_download = self.version.right_url_from_version(
                    self.data["links"][index]
                )

                # We create the destination.
                destination = (
                    destination_dir + self.data["outputs"]["db_type"]["files"][index]
                )

                # We finally download the file.
                Download(link_to_download, destination).text()

    def _install_iana_config(self):
        """
        Download `iana-domains-db.json` if not present.
        """

        # We initiate the link to the iana configuration.
        # It is not hard coded because this method is called only if we
        # are sure that the configuration file exist.
        iana_link = self.data["links"]["iana"]

        # We update the link according to our current version.
        iana_link = self.version.right_url_from_version(iana_link)

        # We set the destination of the downloaded file.
        destination = PyFunceble.CONFIG_DIRECTORY + "iana-domains-db.json"

        if not self.version.is_cloned() or not PyFunceble.path.isfile(destination):
            # The current version is not the cloned version.

            # We Download the link content and return the download status.
            return Download(iana_link, destination).text()

        # We are in the cloned version.

        # We do not need to download the file, so we are returning None.
        return None

    def _install_psl_config(self):
        """
        Download `public-suffix.json` if not present.
        """

        # We initiate the link to the public suffix configuration.
        # It is not hard coded because this method is called only if we
        # are sure that the configuration file exist.
        psl_link = self.data["links"]["psl"]

        # We update the link according to our current version.
        psl_link = self.version.right_url_from_version(psl_link)

        # We set the destination of the downloaded file.
        destination = (
            PyFunceble.CONFIG_DIRECTORY
            + self.data["outputs"]["default_files"]["public_suffix"]
        )

        if not self.version.is_cloned() or not PyFunceble.path.isfile(destination):
            # The current version is not the cloned version.

            # We Download the link content and return the download status.
            return Download(psl_link, destination).text()

        # We are in the cloned version.

        # We do not need to download the file, so we are returning None.
        return None

    def _install_directory_structure_file(self):
        """
        Download the latest version of `dir_structure_production.json`.
        """

        # We initiate the link to the public suffix configuration.
        # It is not hard coded because this method is called only if we
        # are sure that the configuration file exist.
        dir_structure_link = self.data["links"]["dir_structure"]

        # We update the link according to our current version.
        dir_structure_link = self.version.right_url_from_version(dir_structure_link)

        # We set the destination of the downloaded file.
        destination = (
            PyFunceble.CONFIG_DIRECTORY
            + self.data["outputs"]["default_files"]["dir_structure"]
        )

        if not self.version.is_cloned() or not PyFunceble.path.isfile(destination):
            # The current version is not the cloned version.

            # We Download the link content and return the download status.
            data = Download(dir_structure_link, destination, return_data=True).text()

            File(destination).write(data, overwrite=True)
            return True

        # We are in the cloned version.

        # We do not need to download the file, so we are returning None.
        return None

    def get(self):
        """
        Return the loaded config
        """

        return self.data
