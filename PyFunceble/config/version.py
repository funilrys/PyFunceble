"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provide our version controller.

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

import PyFunceble
from PyFunceble.helpers import Dict, Download


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
            upstream_link = self.right_url_from_version(upstream_link)

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
            else:
                # The local version is eqal to the upstream version.

                # We initiate its status to None which means that we are in
                # the same version (for the current version part).
                status[index] = None

            # Otherwise the status stay None which means that there is no change
            # between both local and upstream.

        # We consider that the version is the same.
        result = None

        for data in status:
            # We loop through the list of status.
            # The purpose of this loop is only to
            # get the first not None value.

            if result is None:
                # The result is None (no changes).
                # We set the currently read one as the result.
                result = data

        # We return the result.
        return result

    def __check_force_update(self):
        """
        Check if we need to force the user to update.
        """

        for minimal in self.upstream_data["force_update"]["minimal_version"]:
            # We loop through the list of minimal version which trigger the
            # the force update message.

            # We compare the local with the currently read minimal version.
            checked = self.check_versions(
                self.local_splited, self.split_versions(minimal)
            )

            if not PyFunceble.CONFIGURATION.quiet:
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

    def __check_deprecated(self):
        """
        Checks if the local version is deprecated.
        """

        for version in self.upstream_data["deprecated"]:
            # We loop through the list of deprecated versions.

            # We compare the local with the currently read deprecated version.
            checked = self.check_versions(
                self.local_splited, self.split_versions(version)
            )

            if (
                not PyFunceble.CONFIGURATION.quiet
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
                return False

            # The quiet mode is activated.

            if checked or checked is not False and not checked:
                # The local version is  less or equal to the currently
                # read deprecated version.
                print("Version deprecated.")

                # And we continue to the next logic. There is no need to
                # shutdown PyFunceble as it's just for information.
                return False
        return True

    def print_message(self):
        """
        Prints some message if needed.
        """

        if (
            "messages" in self.upstream_data
            and not PyFunceble.CONFIGURATION.simple
            and not PyFunceble.CONFIGURATION.quiet
        ):
            messages = self.upstream_data["messages"]

            for minimal_version, data in messages.items():
                comparison = self.check_versions(
                    self.local_splited, self.split_versions(minimal_version)
                )

                for single_message in data:
                    if "until" in single_message:
                        until_comparison = self.check_versions(
                            self.local_splited,
                            self.split_versions(single_message["until"]),
                        )
                    else:
                        until_comparison = True

                    if "type" in single_message:
                        if single_message["type"] == "info":
                            coloration = (
                                PyFunceble.Fore.YELLOW + PyFunceble.Style.BRIGHT
                            )
                        elif single_message["type"] == "warning":
                            coloration = (
                                PyFunceble.Fore.MAGENTA + PyFunceble.Style.BRIGHT
                            )
                        else:
                            coloration = PyFunceble.Fore.BLUE + PyFunceble.Style.BRIGHT
                    else:
                        coloration = PyFunceble.Fore.CYAN + PyFunceble.Style.BRIGHT

                    if (
                        comparison is False or comparison is None
                    ) and until_comparison is True:

                        print(f"{coloration}{single_message['message']}")

    def compare(self):
        """
        Compare the current version with the upstream saved version.
        """

        if self.upstream_data["force_update"]["status"]:
            # The force_update status is set to True.
            self.__check_force_update()

        if self.__check_deprecated():
            # We compare the local version with the upstream version.
            status = self.check_versions(
                self.local_splited,
                self.split_versions(self.upstream_data["current_version"]),
            )

            if status is not None and not status and not PyFunceble.CONFIGURATION.quiet:
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

                if not PyFunceble.CONFIGURATION.quiet:
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
