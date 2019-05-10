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

This submodule will provide the configuration loading and construction logic.

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
# pylint: enable=line-too-long
import PyFunceble
from PyFunceble.helpers import Dict, Directory, Download, File


class Load:  # pylint: disable=too-few-public-methods
    """
    Help us load the configuration(s) file(s).

    :param str path_to_config: The possible path to the configuration to load.
    """

    def __init__(self, path_to_config):
        # We initiate 2 variables:
        #   * One with the path to the config file
        #   * The second one is the path to the default configuration file which is
        #   used only if the first one is not found.
        self.path_to_config, self.path_to_default_config = self._set_path_to_configs(
            path_to_config
        )

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

        for main_key in ["domains", "hosts", "splited", "json", "complements"]:
            # We loop through the key which contain paths under the `outputs` index.

            # And we fix the path.
            # Which means: If they do not end with the directory separator, we append
            # it to the end.
            PyFunceble.CONFIGURATION["outputs"][main_key]["directory"] = Directory(
                PyFunceble.CONFIGURATION["outputs"][main_key]["directory"]
            ).fix_path()

        for main_key in ["analytic", "logs"]:
            # We loop through the key which are more deeper under the `outputs` index.

            for key, value in PyFunceble.CONFIGURATION["outputs"][main_key][
                "directories"
            ].items():
                # We loop through the more deeper indexes.

                # And we fix the path.
                # Which means: If they do not end with the directory separator, we append
                # it to the end.
                PyFunceble.CONFIGURATION["outputs"][main_key]["directories"][
                    key
                ] = Directory(value).fix_path()

        # We fix the path.
        # Which means: If they do not end with the directory separator, we append
        # it to the end.
        PyFunceble.CONFIGURATION["outputs"]["parent_directory"] = Directory(
            PyFunceble.CONFIGURATION["outputs"]["parent_directory"]
        ).fix_path()

        # We update the STATUS variable with the status from the configuration.
        PyFunceble.STATUS.update(PyFunceble.CONFIGURATION["status"])
        # We update the OUTPUTS variable with the outputs from the configuration.
        PyFunceble.OUTPUTS.update(PyFunceble.CONFIGURATION["outputs"])
        # We update the HTTP_CODE variable with the http_codes from the configuration.
        PyFunceble.HTTP_CODE.update(PyFunceble.CONFIGURATION["http_codes"])
        # We update the LINKS variable with the links from the configuration.
        PyFunceble.LINKS.update(PyFunceble.CONFIGURATION["links"])

        # Those 2 strings are used to say if something like the cleaning went right (done)
        # or wrong (error).
        PyFunceble.INTERN.update(
            {"done": PyFunceble.Fore.GREEN + "✔", "error": PyFunceble.Fore.RED + "✘"}
        )

        # We load the PSL database.
        PyFunceble.PublicSuffix().load()

        # We load the IANA database.
        PyFunceble.IANA().load()

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

            PyFunceble.CONFIGURATION.update(
                Dict.from_yaml(File(self.path_to_config).read())
            )

            # We install the latest iana configuration file.
            self._install_iana_config()

            # We install the latest public suffix configuration file.
            self._install_psl_config()

            # We install the latest directory structure file.
            self._install_directory_structure_file()
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
        production_config_link = Version(True).right_url_from_version(
            production_config_link
        )

        if not Version(True).is_cloned():
            # The current version is not the cloned one.

            # We download the link content and save it inside the default location.
            #
            # Note: We add this one in order to allow the enduser to always have
            # a copy of our upstream configuration file.
            Download(production_config_link, self.path_to_default_config).text()

        # And we download the link content and return the download status.
        return Download(production_config_link, self.path_to_config).text()

    @classmethod
    def _install_iana_config(cls):
        """
        Download `iana-domains-db.json` if not present.
        """

        # We initiate the link to the iana configuration.
        # It is not hard coded because this method is called only if we
        # are sure that the configuration file exist.
        iana_link = PyFunceble.CONFIGURATION["links"]["iana"]

        # We update the link according to our current version.
        iana_link = Version(True).right_url_from_version(iana_link)

        # We set the destination of the downloaded file.
        destination = PyFunceble.CURRENT_DIRECTORY + "iana-domains-db.json"

        if not Version(True).is_cloned() or not PyFunceble.path.isfile(destination):
            # The current version is not the cloned version.

            # We Download the link content and return the download status.
            return Download(iana_link, destination).text()

        # We are in the cloned version.

        # We do not need to download the file, so we are returning None.
        return None

    @classmethod
    def _install_psl_config(cls):
        """
        Download `public-suffix.json` if not present.
        """

        # We initiate the link to the public suffix configuration.
        # It is not hard coded because this method is called only if we
        # are sure that the configuration file exist.
        psl_link = PyFunceble.CONFIGURATION["links"]["psl"]

        # We update the link according to our current version.
        psl_link = Version(True).right_url_from_version(psl_link)

        # We set the destination of the downloaded file.
        destination = (
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.CONFIGURATION["outputs"]["default_files"]["public_suffix"]
        )

        if not Version(True).is_cloned() or not PyFunceble.path.isfile(destination):
            # The current version is not the cloned version.

            # We Download the link content and return the download status.
            return Download(psl_link, destination).text()

        # We are in the cloned version.

        # We do not need to download the file, so we are returning None.
        return None

    @classmethod
    def _install_directory_structure_file(cls):
        """
        Download the latest version of `dir_structure_production.json`.
        """

        # We initiate the link to the public suffix configuration.
        # It is not hard coded because this method is called only if we
        # are sure that the configuration file exist.
        dir_structure_link = PyFunceble.CONFIGURATION["links"]["dir_structure"]

        # We update the link according to our current version.
        dir_structure_link = Version(True).right_url_from_version(dir_structure_link)

        # We set the destination of the downloaded file.
        destination = (
            PyFunceble.CURRENT_DIRECTORY
            + PyFunceble.CONFIGURATION["outputs"]["default_files"]["dir_structure"]
        )

        if not Version(True).is_cloned() or not PyFunceble.path.isfile(destination):
            # The current version is not the cloned version.

            # We Download the link content and return the download status.
            data = Download(dir_structure_link, destination, return_data=True).text()

            File(destination).write(data, overwrite=True)
            return True

        # We are in the cloned version.

        # We do not need to download the file, so we are returning None.
        return None


class Merge:  # pylint: disable=too-few-public-methods
    """
    Merge the old into the new configuration file.

    :param str configuration_path: The path to the configuration file to update.
    """

    def __init__(self, configuration_path):
        self.path_to_config = configuration_path

        if not self.path_to_config.endswith(PyFunceble.directory_separator):
            self.path_to_config += PyFunceble.directory_separator

        self.path_to_config += PyFunceble.CONFIGURATION_FILENAME

        self.upstream_config = Dict().from_yaml(
            Download(PyFunceble.LINKS["config"], return_data=True).text()
        )

        if self.upstream_config["links"]["config"] != PyFunceble.LINKS["config"]:
            self.upstream_config = Dict().from_yaml(
                Download(self.upstream_config["links"]["repo"], return_data=True).text()
            )

        self.new_config = {}

        self._load()

    def _merge_values(self):
        """
        Simply merge the older into the new one.
        """

        to_remove = []

        self.new_config = Dict(
            Dict(self.upstream_config).merge(PyFunceble.CONFIGURATION)
        ).remove_key(to_remove)

    def _save(self):
        """
        Save the new configuration inside the configuration file.
        """

        Dict(self.new_config).to_yaml(self.path_to_config)

    def _load(self):
        """
        Execute the logic behind the merging.
        """

        if "PYFUNCEBLE_AUTO_CONFIGURATION" not in PyFunceble.environ:
            # The auto configuration environment variable is not set.

            while True:
                # We infinitly loop until we get a reponse which is `y|Y` or `n|N`.

                # We ask the user if we should install and load the default configuration.
                response = input(
                    PyFunceble.Style.BRIGHT
                    + PyFunceble.Fore.RED
                    + "A configuration key is missing.\n"
                    + PyFunceble.Fore.RESET
                    + "Try to merge upstream configuration file into %s ? [y/n] "
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

                        # We merge the old values inside the new one.
                        self._merge_values()

                        # And we save.
                        self._save()

                        print(
                            PyFunceble.Style.BRIGHT + PyFunceble.Fore.GREEN + "Done!\n"
                            "Please try again, if it happens again,"
                            " please fill a new issue."
                        )

                        # And we break the loop as we got a satisfied response.
                        break

                    elif response.lower() == "n":
                        # The response is a `n` or `N`.

                        # We inform the user that something went wrong.
                        raise Exception("Configuration key still missing.")
        else:
            # The auto configuration environment variable is set.

            # We merge the old values inside the new one.
            self._merge_values()

            # And we save.
            self._save()


class Version:
    """
    Compare the local with the upstream version.

    :param bool used:
        True: Version is configured for simple usage.
        False: Version compare local with upstream.
    """

    def __init__(self, used=False):
        if not used:
            # A method of this class is not called directly.

            # We split the local version.
            self.local_splited = self.split_versions(PyFunceble.VERSION)

            # We initiate the link to the upstream version file.
            # It is hard coded because we may not have the chance to have the
            # configuration file everytime we need it.
            upstream_link = (
                "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/version.yaml"
            )  # pylint: disable=line-too-long

            # We update the link according to our current version.
            upstream_link = Version(True).right_url_from_version(upstream_link)

            # We get the link content and convert it to a dict which is more
            # usable.
            self.upstream_data = Dict().from_yaml(
                Download(upstream_link, return_data=True).text()
            )

    @classmethod
    def split_versions(cls, version, return_non_digits=False):
        """
        Convert the versions to a shorter one.

        :param str version: The version to split.

        :param bool return_non_digits:
            Activate the return of the non-digits parts of the splitted
            version.

        :return: The splitted version name/numbers.
        :rtype: list
        """

        # We split the version.
        splited_version = version.split(".")

        # We split the parsed version and keep the digits.
        digits = [x for x in splited_version if x.isdigit()]

        if not return_non_digits:
            # We do not have to return the non digits part of the version.

            # We return the digits part of the version.
            return digits

        # We have to return the non digit parts of the version.

        # We split the parsed version and keep the non digits.
        non_digits = [x for x in splited_version if not x.isdigit()]

        # We return a tuple with first the digits part and finally the non digit parts.
        return (digits, non_digits[0])

    @classmethod
    def check_versions_literally(cls, local, upstream):
        """
        Compare the given versions literally.

        :param str local: The local version converted by split_versions().

        :param str upstream: The upstream version converted by split_versions().

        :return:
            - True: local == upstream
            - False: local != upstream
        :rtype: bool
        """

        return local == upstream

    @classmethod
    def check_versions(cls, local, upstream):
        """
        Compare the given versions.

        :param list local: The local version converted by split_versions().

        :param list upstream: The upstream version converted by split_versions().

        :return:
            - True: local < upstream
            - None: local == upstream
            - False: local > upstream
        :rtype: bool|None
        """

        # A version should be in format [1,2,3] which is actually the version `1.2.3`
        # So as we only have 3 elements in the versioning,
        # we initiate the following variable in order to get the status of each parts.
        status = [None, None, None]

        for index, version_number in enumerate(local):
            # We loop through the local version.

            if int(version_number) < int(upstream[index]):
                # The local version is less than the upstream version.

                # We initiate its status to True which means that we are in
                # an old version (for the current version part).
                status[index] = True
            elif int(version_number) > int(upstream[index]):
                # The local version is greater then the upstream version.

                # We initiate its status to False which means that we are in
                # a more recent version (for the current version part).
                status[index] = False

            # Otherwise the status stay None which means that there is no change
            # between both local and upstream.

        if False in status:
            # There is a False in the status.

            # We return False which means that we are in a more recent version.
            return False

        if True in status:
            # There is a True in the status.

            # We return True which means that we are in a older version.
            return True

        # There is no True or False in the status.

        # We return None which means that we are in the same version as upstream.
        return None

    def compare(self):
        """
        Compare the current version with the upstream saved version.
        """

        if self.upstream_data["force_update"]["status"]:
            # The force_update status is set to True.

            for minimal in self.upstream_data["force_update"]["minimal_version"]:
                # We loop through the list of minimal version which trigger the
                # the force update message.

                # We compare the local with the currently read minimal version.
                checked = self.check_versions(
                    self.local_splited, self.split_versions(minimal)
                )

                if not PyFunceble.CONFIGURATION["quiet"]:
                    # The quiet mode is not activated.

                    if checked or checked is not False and not checked:
                        # The current version is less or equal to
                        # the minimal version.

                        # We initiate the message we are going to return to
                        # the user.
                        message = (
                            PyFunceble.Style.BRIGHT
                            + PyFunceble.Fore.RED
                            + "A critical issue has been fixed.\n"
                            + PyFunceble.Style.RESET_ALL
                        )  # pylint:disable=line-too-long
                        message += (
                            PyFunceble.Style.BRIGHT
                            + PyFunceble.Fore.GREEN
                            + "Please take the time to update PyFunceble!\n"
                            + PyFunceble.Style.RESET_ALL
                        )  # pylint:disable=line-too-long

                        # We print the message on screen.
                        print(message)

                        # We exit PyFunceble with the code 1.
                        exit(1)
                elif checked or checked is not False and not checked:
                    # The quiet mode is activated and the current version
                    # is less or equal to the minimal version.

                    # We raise an exception telling the user to update their
                    # instance of PyFunceble.
                    raise Exception(
                        "A critical issue has been fixed. Please take the time to update PyFunceble!"  # pylint:disable=line-too-long
                    )

        for version in self.upstream_data["deprecated"]:
            # We loop through the list of deprecated versions.

            # We compare the local with the currently read deprecated version.
            checked = self.check_versions(
                self.local_splited, self.split_versions(version)
            )

            if (
                not PyFunceble.CONFIGURATION["quiet"]
                and checked
                or checked is not False
                and not checked
            ):
                # The quiet mode is not activated and the local version is
                # less or equal to the currently read deprecated version.

                # We initiate the message we are going to return to the user.
                message = (
                    PyFunceble.Style.BRIGHT
                    + PyFunceble.Fore.RED
                    + "Your current version is considered as deprecated.\n"
                    + PyFunceble.Style.RESET_ALL
                )  # pylint:disable=line-too-long
                message += (
                    PyFunceble.Style.BRIGHT
                    + PyFunceble.Fore.GREEN
                    + "Please take the time to update PyFunceble!\n"
                    + PyFunceble.Style.RESET_ALL
                )  # pylint:disable=line-too-long

                # We print the message.
                print(message)

                # And we continue to the next logic. There is no need to
                # shutdown PyFunceble as it's just for information.
                return

            # The quiet mode is activated.

            if checked or checked is not False and not checked:
                # The local version is  less or equal to the currently
                # read deprecated version.
                print("Version deprecated.")

                # And we continue to the next logic. There is no need to
                # shutdown PyFunceble as it's just for information.
                return

        # We compare the local version with the upstream version.
        status = self.check_versions(
            self.local_splited,
            self.split_versions(self.upstream_data["current_version"]),
        )

        if status is not None and not status and not PyFunceble.CONFIGURATION["quiet"]:
            # The quiet mode is not activate and the current version is greater than
            # the upstream version.

            # We initiate the message we are going to return to the user.
            message = (
                PyFunceble.Style.BRIGHT
                + PyFunceble.Fore.CYAN
                + "Your version is more recent!\nYou should really think about sharing your changes with the community!\n"  # pylint:disable=line-too-long
                + PyFunceble.Style.RESET_ALL
            )
            message += (
                PyFunceble.Style.BRIGHT
                + "Your version: "
                + PyFunceble.Style.RESET_ALL
                + PyFunceble.VERSION
                + "\n"
            )
            message += (
                PyFunceble.Style.BRIGHT
                + "Upstream version: "
                + PyFunceble.Style.RESET_ALL
                + self.upstream_data["current_version"]
                + "\n"
            )

            # We print the message.
            print(message)
        elif status:
            # The current version is less that the upstream version.

            if not PyFunceble.CONFIGURATION["quiet"]:
                # The quiet mode is not activated.

                # We initiate the message we are going to return to the user.
                message = (
                    PyFunceble.Style.BRIGHT
                    + PyFunceble.Fore.YELLOW
                    + "Please take the time to update PyFunceble!\n"
                    + PyFunceble.Style.RESET_ALL
                )  # pylint:disable=line-too-long
                message += (
                    PyFunceble.Style.BRIGHT
                    + "Your version: "
                    + PyFunceble.Style.RESET_ALL
                    + PyFunceble.VERSION
                    + "\n"
                )  # pylint:disable=line-too-long
                message += (
                    PyFunceble.Style.BRIGHT
                    + "Upstream version: "
                    + PyFunceble.Style.RESET_ALL
                    + self.upstream_data[  # pylint:disable=line-too-long
                        "current_version"
                    ]
                    + "\n"
                )

                # We print the message.
                print(message)
            else:
                # The quiet mode is activated.

                # We print the message.
                print("New version available.")

        # And we continue to the next app logic. There is no need to
        # shutdown PyFunceble as it's just for information.
        return

    @classmethod
    def is_cloned(cls):
        """
        Let us know if we are currently in the cloned version of
        PyFunceble which implicitly mean that we are in developement mode.
        """

        if not PyFunceble.path.isdir(".git"):
            # The git directory does not exist.

            # We return False, the current version is not the cloned version.
            return False

        # We list the list of file which can be found only in a cloned version.
        list_of_file = [
            ".coveragerc",
            ".coveralls.yml",
            ".gitignore",
            ".PyFunceble_production.yaml",
            ".travis.yml",
            "CODE_OF_CONDUCT.md",
            "CONTRIBUTING.md",
            "dir_structure_production.json",
            "MANIFEST.in",
            "README.rst",
            "requirements.txt",
            "setup.py",
            "version.yaml",
        ]

        # We list the list of directory which can be found only in a cloned
        # version.
        list_of_dir = ["docs", "PyFunceble", "tests"]

        for file in list_of_file:
            # We loop through the list of file.

            if not PyFunceble.path.isfile(file):
                # The file does not exist in the current directory.

                # We return False, the current version is not the cloned version.
                return False

        # All required files exist in the current directory.

        for directory in list_of_dir:
            # We loop through the list of directory.

            if not PyFunceble.path.isdir(directory):
                # The directory does not exist in the current directory.

                # We return False, the current version is not the cloned version.
                return False

        # All required directories exist in the current directory.

        # We return True, the current version is a cloned version.
        return True

    @classmethod
    def right_url_from_version(cls, url):
        """
        Convert the GitHub URL to the right one depending of the
        branch or version we are working with.

        :param str url: The URL to convert.

        :return: The converted URL.
        :rtype: str
        """

        if "dev" in PyFunceble.VERSION:
            # `dev` is in the current version.

            # We update and return the url in order to point to the dev branch.
            return url.replace("master", "dev")

        # `dev` is not in the current version.

        # We update and return the url in order to point to the master branch.
        return url.replace("dev", "master")
