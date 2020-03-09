"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the configuration loader.

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
# pylint: disable=import-error

from os import sep as directory_separator

from box import Box
from colorama import Fore, Style

import PyFunceble


class Load:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Loads the configuration(s) file(s).

    :param str path_to_config:
        The possible path to the configuration to load.

    :param dict custom:
        The custom index, this is what we overwrite.
    """

    def __init__(self, path_to_config, custom=None):
        # We initiate the vairable which will provides the configuration content.
        self.data = Box({}, default_box=True, default_box_attr=None)

        self.__path_to_config = path_to_config

        if not path_to_config.endswith(directory_separator):
            path_to_config += directory_separator

        # We initiate 2 variables:
        #   * One with the path to the config file
        #   * The second one is the path to the default configuration file which is
        #   used only if the first one is not found.
        self.path_to_config, self.path_to_default_config = self._set_path_to_configs(
            path_to_config
        )

        # We download the latest production configuration file.
        PyFunceble.downloader.Config()

        if "config_loaded" not in PyFunceble.INTERN:
            self.__load_it()

        self.__set_it(custom)
        self.__download_them_all()

    def __load_it(self):
        """
        Loads the configuration and everything needed around it.

        .. note::
            "Everything needed around it" is meant to be all files
            which are needed by other part of the project.
        """

        try:
            # We try to load the configuration.
            self._load_config_file()
        except PyFunceble.exceptions.ConfigurationFileNotFound:
            # We got a FileNotFoundError

            if not PyFunceble.helpers.EnvironmentVariable(
                "PYFUNCEBLE_AUTO_CONFIGURATION"
            ).exists():
                # `PYFUNCEBLE_AUTO_CONFIGURATION` is not into the environments variables.

                while True:
                    # We infinitely loop until we get a response which is `y|Y` or `n|N`.

                    # We ask the user if we should install and load the default configuration.
                    response = input(
                        "%s was not found.\n\
Install and load the default configuration at the mentioned location? [y/n] "
                        % (Style.BRIGHT + self.path_to_config + Style.RESET_ALL)
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

                        if response.lower() == "n":
                            # The response is a `n` or `N`.

                            # We inform the user that something went wrong.
                            raise PyFunceble.exceptions.ConfigurationFileNotFound()

            else:
                # `PYFUNCEBLE_AUTO_CONFIGURATION` is not into the environment variables.

                # We install the production configuration.
                self._install_production_config()

                # We load the installed configuration.
                self._load_config_file()

    def __fix_paths(self):
        """
        Fixes all paths.
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
                self.data["outputs"][main_key][
                    "directory"
                ] = PyFunceble.helpers.Directory(
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
                self.data["outputs"][main_key]["directories"][
                    key
                ] = PyFunceble.helpers.Directory(value).fix_path()

        # We fix the path.
        # Which means: If they do not end with the directory separator, we append
        # it to the end.
        self.data["outputs"]["parent_directory"] = PyFunceble.helpers.Directory(
            self.data["outputs"]["parent_directory"]
        ).fix_path()

    @classmethod
    def __download_them_all(cls):
        """
        Download everything that needs to be downloaded.
        """

        # We install the latest directory structure file.
        PyFunceble.downloader.DirectoryStructure()

        # We install the lated user agents file.
        PyFunceble.downloader.UserAgents()

    def __set_it(self, custom):
        """
        Sets the configuration at its final location and load the complementary infos.

        :param dict custom:
            The custom index, this is what we overwrite.
        """

        if "config_loaded" not in PyFunceble.INTERN:
            PyFunceble.CONFIGURATION = self.data

        if custom and isinstance(custom, dict):
            PyFunceble.CONFIGURATION.update(custom)

            if "custom_config_loaded" in PyFunceble.INTERN:
                PyFunceble.INTERN["custom_config_loaded"] = PyFunceble.helpers.Merge(
                    custom
                ).into(PyFunceble.INTERN["custom_config_loaded"])
            else:
                PyFunceble.INTERN["custom_config_loaded"] = custom

            # We save the fact the the custom was loaded.
            PyFunceble.INTERN["custom_loaded"] = True

        try:
            # We install the latest iana configuration file.
            PyFunceble.downloader.IANA()
        except Exception as exception:  # pylint: disable=broad-except
            if "Unable to download" in str(exception):
                PyFunceble.cconfig.Merge(PyFunceble.CONFIG_DIRECTORY)
                self._load_config_file()
            else:
                raise exception

        try:
            # We install the latest public suffix configuration file.
            PyFunceble.downloader.PublicSuffix()
        except Exception as exception:  # pylint: disable=broad-except
            if "Unable to download" in str(exception):
                PyFunceble.cconfig.Merge(PyFunceble.CONFIG_DIRECTORY)
                self._load_config_file()
            else:
                raise exception

        if "config_loaded" not in PyFunceble.INTERN:
            PyFunceble.STATUS = PyFunceble.CONFIGURATION.status
            PyFunceble.OUTPUTS = PyFunceble.CONFIGURATION.outputs
            PyFunceble.HTTP_CODE = PyFunceble.CONFIGURATION.http_codes
            PyFunceble.LINKS = PyFunceble.CONFIGURATION.links

            # Those 2 strings are used to say if something like the cleaning went right (done)
            # or wrong (error).
            PyFunceble.INTERN.update(
                {"done": Fore.GREEN + "✔", "error": Fore.RED + "✘"}
            )

            PyFunceble.LOGGER = PyFunceble.engine.Logger(
                debug=PyFunceble.CONFIGURATION.debug
            )
            PyFunceble.REQUESTS = PyFunceble.lookup.Requests()
            PyFunceble.PSLOOOKUP = PyFunceble.lookup.PublicSuffix()
            PyFunceble.IANALOOKUP = PyFunceble.lookup.Iana()
            PyFunceble.DNSLOOKUP = PyFunceble.lookup.Dns(
                dns_server=PyFunceble.CONFIGURATION.dns_server,
                lifetime=PyFunceble.CONFIGURATION.timeout,
                tcp=PyFunceble.CONFIGURATION.dns_lookup_over_tcp,
            )

            PyFunceble.INTERN.update({"config_loaded": True})

    @classmethod
    def _set_path_to_configs(cls, path_to_config):
        """
        Sets the paths to the configuration files.

        :param str path_to_config:
            The possible path to the config to load.

        :return:
            The path to the config to read (0), the path to the default
            configuration to read as fallback.(1)
        :rtype: tuple
        """

        if not path_to_config.endswith(directory_separator):
            # The path to the config does not ends with the directory separator.

            # We initiate the default and the parsed variable with the directory separator.
            default = parsed = path_to_config + directory_separator
        else:
            # The path to the config does ends with the directory separator.

            # We initiate the default and the parsed variable.
            default = parsed = path_to_config

        # We append the `CONFIGURATION_FILENAME` to the parsed variable.
        parsed += PyFunceble.abstracts.Infrastructure.CONFIGURATION_FILENAME
        # And we append the `DEFAULT_CONFIGURATION_FILENAME` to the default variable.
        default += PyFunceble.abstracts.Infrastructure.DEFAULT_CONFIGURATION_FILENAME

        # We finally return a tuple which contain both information.
        return (parsed, default)

    def _load_config_file(self):
        """
        Loads :code.`.PyFunceble.yaml` into the system.
        """

        try:
            # We try to load the configuration file.

            file_instance = PyFunceble.helpers.File(self.path_to_config)

            if not file_instance.exists() or file_instance.is_empty():

                # We force the regeneration of the configuration file.
                raise FileNotFoundError(self.path_to_config)

            self.data.update(
                PyFunceble.helpers.Dict.from_yaml_file(self.path_to_config)
            )
        except (FileNotFoundError, TypeError):
            # *  But if the configuration file is not found.
            # Or
            # * A configuration index is not found.

            # We raise the exception we were handling.
            raise PyFunceble.exceptions.ConfigurationFileNotFound()

        self.__fix_paths()

    def _install_production_config(self):
        """
        Downloads the production configuration and install it in the
        given configuration directory.
        """

        # We copy the previously downloaded production file.
        PyFunceble.helpers.File(self.path_to_default_config).copy(self.path_to_config)

    def get(self):
        """
        Returns the loaded config
        """

        return self.data
