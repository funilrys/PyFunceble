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

This submodule will provide the configuration.

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
from PyFunceble import Fore, Style, directory_separator, environ, path
from PyFunceble.helpers import Dict, Directory, Download, File


class Load(object):  # pylint: disable=too-few-public-methods
    """
    This class will help to load the configurations.

    Argument:
        - path_to_config: str
            The path to the config to load.
    """

    def __init__(self, path_to_config):
        self.path_to_config = path_to_config

        if path_to_config.endswith(directory_separator):
            self.path_to_config += directory_separator

        self.path_to_config += PyFunceble.CONFIGURATION_FILENAME

        try:
            self._load_config_file()
            self._install_iana_config()
        except FileNotFoundError:

            if "PYFUNCEBLE_AUTO_CONFIGURATION" not in environ:
                while True:
                    response = input(
                        "%s was not found.\n\
Install the default configuration in the current directory ? [y/n] "
                        % (Style.BRIGHT + path_to_config + Style.RESET_ALL)
                    )

                    if isinstance(response, str):
                        if response.lower() == "y":
                            self._install_production_config()
                            self._load_config_file()
                            self._install_iana_config()
                            break

                        elif response.lower() == "n":
                            raise Exception("Unable to find the configuration file.")

            else:
                self._install_production_config()
                self._load_config_file()
                self._install_iana_config()

        for main_key in ["domains", "hosts", "splited"]:
            PyFunceble.CONFIGURATION["outputs"][main_key]["directory"] = Directory(
                PyFunceble.CONFIGURATION["outputs"][main_key]["directory"]
            ).fix_path()

        for main_key in ["http_analytic", "logs"]:
            for key, value in PyFunceble.CONFIGURATION["outputs"][main_key][
                "directories"
            ].items():
                PyFunceble.CONFIGURATION["outputs"][main_key]["directories"][
                    key
                ] = Directory(
                    value
                ).fix_path()

        PyFunceble.CONFIGURATION["outputs"]["main"] = Directory(
            PyFunceble.CONFIGURATION["outputs"]["main"]
        ).fix_path()

        PyFunceble.STATUS.update(PyFunceble.CONFIGURATION["status"])
        PyFunceble.OUTPUTS.update(PyFunceble.CONFIGURATION["outputs"])
        PyFunceble.HTTP_CODE.update(PyFunceble.CONFIGURATION["http_codes"])
        PyFunceble.LINKS.update(PyFunceble.CONFIGURATION["links"])

        PyFunceble.CONFIGURATION.update(
            {"done": Fore.GREEN + "✔", "error": Fore.RED + "✘"}
        )

    def _load_config_file(self):
        """
        This method will load .PyFunceble.yaml.
        """

        PyFunceble.CONFIGURATION.update(
            Dict.from_yaml(File(self.path_to_config).read())
        )

    def _install_production_config(self):
        """
        This method download the production configuration and install it in the
        current directory.

        Argument:
            - path_to_config: str
                The path were we have to install the configuration file.
        """

        production_config_link = "https://raw.githubusercontent.com/funilrys/PyFunceble/master/.PyFunceble_production.yaml"  # pylint: disable=line-too-long

        if "dev" in PyFunceble.VERSION:
            production_config_link = production_config_link.replace("master", "dev")
        else:
            production_config_link = production_config_link.replace("dev", "master")

        return Download(production_config_link, self.path_to_config).text()

    @classmethod
    def _install_iana_config(cls):
        """
        This method download `iana-domains-db.json` if not present.
        """

        iana_link = "https://raw.githubusercontent.com/funilrys/PyFunceble/master/iana-domains-db.json"  # pylint: disable=line-too-long
        destination = PyFunceble.CURRENT_DIRECTORY + "iana-domains-db.json"

        if "dev" in PyFunceble.VERSION:
            iana_link = iana_link.replace("master", "dev")
        else:
            iana_link = iana_link.replace("dev", "master")

        if not path.isfile(destination):
            return Download(iana_link, destination).text()

        return True


class Version(object):
    """
    This class will compare the local with the upstream version.

    Argument:
        - used: bool
            True: Version is configured for simple usage.
            False: Version compare local with upstream.
    """

    def __init__(self, used=False):
        if not used:
            self.local_splited = self.split_versions(PyFunceble.VERSION)

            upstream_link = "https://raw.githubusercontent.com/funilrys/PyFunceble/master/version.yaml"  # pylint: disable=line-too-long

            if "dev" in PyFunceble.VERSION:
                upstream_link = upstream_link.replace("master", "dev")
            else:
                upstream_link = upstream_link.replace("dev", "master")

            self.upstream_data = Dict().from_yaml(
                Download(upstream_link, return_data=True).text()
            )

    @classmethod
    def split_versions(cls, version, return_non_digits=False):
        """
        This method will convert the versions to a shorter one.

        Arguments:
            - version: str
                The version to split.
            - return_non_digits: bool
                Return the non digit part of the splited version.

        Returns: list
        """

        digits = list(filter(lambda x: x.isdigit(), version.split(".")))

        if not return_non_digits:
            return digits

        non_digits = list(filter(lambda x: not x.isdigit(), version.split(".")))

        return (digits, non_digits[0])

    @classmethod
    def check_versions(cls, local, upstream):
        """
        This method will compare the given versions.

        Arguments:
            - local: list
                The local version converted by split_versions().
            - upstream: list
                The upstream version converted by split_versions().

        Returns:
            - True: local < upstream
            - None: local == upstream
            - False: local > upstream
        """

        status = [None, None, None]

        for index, version_number in enumerate(local):
            if int(version_number) < int(upstream[index]):
                status[index] = True
            elif int(version_number) > int(upstream[index]):
                status[index] = False

        if False in status:
            return False

        elif True in status:
            return True

        return None

    def compare(self):
        """
        This method will compare the current version with the upstream saved version.
        """

        if self.upstream_data["force_update"]["status"]:
            for minimal in self.upstream_data["force_update"]["minimal_version"]:
                checked = self.check_versions(
                    self.local_splited, self.split_versions(minimal)
                )

                if not PyFunceble.CONFIGURATION["quiet"]:
                    if checked or checked != False and not checked:
                        message = Style.BRIGHT + Fore.RED + "A critical issue has been fixed.\n" + Style.RESET_ALL  # pylint:disable=line-too-long
                        message += Style.BRIGHT + Fore.GREEN + "Please take the time to update PyFunceble!\n" + Style.RESET_ALL  # pylint:disable=line-too-long

                        print(message)
                        exit(1)
                elif checked or checked != False and not checked:
                    raise Exception(
                        "A critical issue has been fixed. Please take the time to update PyFunceble!"  # pylint:disable=line-too-long
                    )

        for version in self.upstream_data["deprecated"]:
            checked = self.check_versions(
                self.local_splited, self.split_versions(version)
            )

            if not PyFunceble.CONFIGURATION[
                "quiet"
            ] and checked or checked != False and not checked:
                message = Style.BRIGHT + Fore.RED + "Your current version is considered as deprecated.\n" + Style.RESET_ALL  # pylint:disable=line-too-long
                message += Style.BRIGHT + Fore.GREEN + "Please take the time to update PyFunceble!\n" + Style.RESET_ALL  # pylint:disable=line-too-long

                print(message)
                return

            elif checked or checked != False and not checked:
                print("Version deprecated.")
                return

        status = self.check_versions(
            self.local_splited,
            self.split_versions(self.upstream_data["current_version"]),
        )

        if status != None and not status and not PyFunceble.CONFIGURATION["quiet"]:
            message = Style.BRIGHT + Fore.CYAN + "Your version is more recent!\nYou should really think about sharing your changes with the community!\n" + Style.RESET_ALL  # pylint:disable=line-too-long
            message += Style.BRIGHT + "Your version: " + Style.RESET_ALL + PyFunceble.VERSION + "\n"
            message += Style.BRIGHT + "Upstream version: " + Style.RESET_ALL + self.upstream_data[
                "current_version"
            ] + "\n"

            print(message)
        elif status:
            if not PyFunceble.CONFIGURATION["quiet"]:
                message = Style.BRIGHT + Fore.YELLOW + "Please take the time to update PyFunceble!\n" + Style.RESET_ALL  # pylint:disable=line-too-long
                message += Style.BRIGHT + "Your version: " + Style.RESET_ALL + PyFunceble.VERSION + "\n"  # pylint:disable=line-too-long
                message += Style.BRIGHT + "Upstream version: " + Style.RESET_ALL + self.upstream_data[  # pylint:disable=line-too-long
                    "current_version"
                ] + "\n"

                print(message)
            else:
                print("New version available.")

        return
