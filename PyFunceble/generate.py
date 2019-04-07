# pylint:disable=line-too-long, too-many-lines
"""
The tool to check the availability or syntax of domains, IPv4 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This submodule will create the generation interface/logic.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://funilrys.github.io/PyFunceble/

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
from PyFunceble import directory_separator
from PyFunceble.inactive_db import InactiveDB
from PyFunceble.percentage import Percentage
from PyFunceble.prints import Prints


class Generate:  # pragma: no cover pylint:disable=too-many-instance-attributes, too-many-arguments
    """
    Generate different sort of files.

    :param subject: The subject we are working with.
    :type subject: str

    :param subject_type: The type of the subject.
    :type subject_type: str

    :param status: The catched status.
    :type status: str

    :param source: The source of the given status.
    :type source: str

    :param expiration_date: The expiration date of the domain (if catched).
    :type expiration_date: str

    :param http_status_code: The HTTP status code.
    :type http_status_code: str|int

    :param whois_server: The whois server.
    :type whois_server: str

    :param filename: The name of the file we are testing.
    :type filename: str
    """

    def __init__(
        self,
        subject,
        subject_type,
        status,
        source=None,
        expiration_date=None,
        http_status_code="***",
        whois_server="Unknown",
        filename=None,
    ):
        # We share the subject.
        self.subject = subject
        # We share the subject type.
        self.subject_type = subject_type
        # We share the status
        self.status = status
        # We get the source.
        self.source = source
        # We share the status code.
        self.status_code = http_status_code
        # We share the file name.
        self.filename = filename

        if not whois_server:
            whois_server = "Unknown"
        else:
            # We share the whois server.
            self.whois_server = whois_server

        if not expiration_date:
            # The expiration date is not give or is empty.

            # We set the expiration date.
            self.expiration_date = "Unknown"
        else:
            # The expiration date is given.

            # We get the expiration date.
            self.expiration_date = expiration_date

        # We construct the output parent directory.
        self.output_parent_dir = (
            PyFunceble.OUTPUT_DIRECTORY + PyFunceble.OUTPUTS["parent_directory"]
        )

        if PyFunceble.CONFIGURATION["user_agent"]:
            # The user-agent (from the configuration file) is not empty.

            # We initiate the header to use with our request.
            self.headers = {"User-Agent": PyFunceble.CONFIGURATION["user_agent"]}
        else:
            # The user-agent (from the configuration file) is empty.

            # We initiate an empty header to use with our request.
            self.headers = {}

    def _analytic_host_file_directory(self):
        """
        Return the analytic directory to write depending of the matched
        status.
        """

        # We construct the path to the analytic directory.
        output_dir = (
            self.output_parent_dir
            + PyFunceble.OUTPUTS["analytic"]["directories"]["parent"]
        )

        if self.status.lower() in PyFunceble.STATUS["list"]["potentially_up"]:
            # The status is in the list of analytic up status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS["analytic"]["directories"][
                "potentially_up"
            ]
        elif self.status.lower() in PyFunceble.STATUS["list"]["potentially_down"]:
            # The status is in the list of analytic down status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS["analytic"]["directories"][
                "potentially_down"
            ]
        elif self.status.lower() in PyFunceble.STATUS["list"]["suspicious"]:
            # The status is in the list of analytic suspicious status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS["analytic"]["directories"]["suspicious"]
        else:
            # The status is not in the list of analytic down or up status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS["analytic"]["directories"]["up"]

        return output_dir

    def ___info_files_authorization(self):
        """
        Provide the authorization for the generation
        of info files.

        Basicaly here is what we check:

        * We are not testing as an imported module.

        and

        * The hosts file generation is activated.

        or

        * The plain list generation is activated.
        or

        * The "api_file_generation" was set into the CONFIGURATION.
        """

        return (
            self.subject_type.startswith("file_")
            and (
                PyFunceble.CONFIGURATION["generate_hosts"]
                or PyFunceble.CONFIGURATION["plain_list_domain"]
                or PyFunceble.CONFIGURATION["generate_json"]
            )
            or "api_file_generation" in PyFunceble.CONFIGURATION
            and PyFunceble.CONFIGURATION["api_file_generation"]
        )

    def info_files(self):  # pylint: disable=inconsistent-return-statements
        """
        Generate the hosts file, the plain list and the splitted lists.
        """

        if self._do_not_produce_file():
            # We do not have to produce file.

            # We return false.
            return False

        if self.___info_files_authorization():
            # We initiate a variable which whill save the splited testination.
            splited_destination = ""

            # We initiate the list of all analytic related statuses.
            http_list = []
            http_list.extend(PyFunceble.STATUS["list"]["potentially_up"])
            http_list.extend(PyFunceble.STATUS["list"]["potentially_down"])
            http_list.extend(PyFunceble.STATUS["list"]["http_active"])
            http_list.extend(PyFunceble.STATUS["list"]["suspicious"])

            # We partially initiate the path to the hosts file.
            output_hosts = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS["hosts"]["directory"]
                + "%s"
                + directory_separator
                + PyFunceble.OUTPUTS["hosts"]["filename"]
            )

            # We partially initiate the path to the plain list file.
            output_domains = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS["domains"]["directory"]
                + "%s"
                + directory_separator
                + PyFunceble.OUTPUTS["domains"]["filename"]
            )

            # We partially intiate the path to the json list file.
            output_json = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS["json"]["directory"]
                + "%s"
                + directory_separator
                + PyFunceble.OUTPUTS["json"]["filename"]
            )

            if self.status.lower() in PyFunceble.STATUS["list"]["up"]:
                # The status is in the list of up list.

                # We complete the path to the hosts file.
                hosts_destination = output_hosts % PyFunceble.STATUS["official"]["up"]

                # We complete the path to the plain list file.
                plain_destination = output_domains % PyFunceble.STATUS["official"]["up"]

                # We complete the path to the json list file.
                json_destination = output_json % PyFunceble.STATUS["official"]["up"]
            elif self.status.lower() in PyFunceble.STATUS["list"]["valid"]:
                # The status is in the list of valid list.

                # We complete the path to the hosts file.
                hosts_destination = (
                    output_hosts % PyFunceble.STATUS["official"]["valid"]
                )

                # We complete the path to the plain list file.
                plain_destination = (
                    output_domains % PyFunceble.STATUS["official"]["valid"]
                )

                # We complete the path to the json list file.
                json_destination = output_json % PyFunceble.STATUS["official"]["valid"]
            elif self.status.lower() in PyFunceble.STATUS["list"]["down"]:
                # The status is in the list of down list.

                # We complete the path to the hosts file.
                hosts_destination = output_hosts % PyFunceble.STATUS["official"]["down"]

                # We complete the path to the plain list file.
                plain_destination = (
                    output_domains % PyFunceble.STATUS["official"]["down"]
                )

                # We complete the path to the json list file.
                json_destination = output_json % PyFunceble.STATUS["official"]["down"]
            elif self.status.lower() in PyFunceble.STATUS["list"]["invalid"]:
                # The status is in the list of invalid list.

                # We complete the path to the hosts file.
                hosts_destination = (
                    output_hosts % PyFunceble.STATUS["official"]["invalid"]
                )

                # We complete the path to the plain list file.
                plain_destination = (
                    output_domains % PyFunceble.STATUS["official"]["invalid"]
                )

                # We complete the path to the json list file.
                json_destination = (
                    output_json % PyFunceble.STATUS["official"]["invalid"]
                )
            elif self.status.lower() in http_list:
                # The status is in the list of analytic status.

                # We construct the path to the analytic directory.
                output_dir = self._analytic_host_file_directory()

                if not output_dir.endswith(directory_separator):
                    # The output directory does not ends with the directory separator.

                    # We append the directory separator at the end of the output directory.
                    output_dir += directory_separator

                # We initiate the hosts file path.
                hosts_destination = output_dir + PyFunceble.OUTPUTS["hosts"]["filename"]

                # We initiate the plain list file path.
                plain_destination = (
                    output_dir + PyFunceble.OUTPUTS["domains"]["filename"]
                )

                # We complete the path to the json list file.
                json_destination = output_dir + PyFunceble.OUTPUTS["json"]["filename"]

                # We initiate the path to the http code file.
                # Note: We generate the http code file so that
                # we can have each domain in a file which is the
                # extracted http code.
                splited_destination = output_dir + str(self.status_code)

            if PyFunceble.CONFIGURATION["generate_hosts"]:
                # The hosts file generation is activated.

                # We generate/append the currently tested element in its
                # final location. (hosts file format)
                # We print on screen and on file.
                Prints(
                    [PyFunceble.CONFIGURATION["custom_ip"], self.subject],
                    "FullHosts",
                    hosts_destination,
                ).data()

            if PyFunceble.CONFIGURATION["plain_list_domain"]:
                # The plain list generation is activated.

                # We generate/append the currently tested element in its
                # final location. (the plain list format)
                # We print on file.
                Prints([self.subject], "PlainDomain", plain_destination).data()

            if PyFunceble.CONFIGURATION["split"] and splited_destination:
                # The splited list generation is activated.

                # We generate/append the currently tested element in its
                # final location. (the split list format)
                # We print on file.
                Prints([self.subject], "PlainDomain", splited_destination).data()

            if PyFunceble.CONFIGURATION["generate_json"]:
                # The jsaon list generation is activated.

                # We generate/append the currently tested element in its
                # final location. (the json format)
                # We print on file.
                Prints([self.subject], "JSON", json_destination).data()

    def unified_file(self):
        """
        Generate unified file. Understand by that that we use an unified table
        instead of a separate table for each status which could result into a
        misunderstanding.
        """

        if (
            self.subject_type.startswith("file_")
            and PyFunceble.CONFIGURATION["unified"]
        ):
            # * We are not testing as an imported module.
            # and
            # * The unified file generation is activated.

            # We construct the path of the unified file.
            output = (
                self.output_parent_dir + PyFunceble.OUTPUTS["default_files"]["results"]
            )

            if PyFunceble.CONFIGURATION["less"]:
                # We have to print less information.

                if PyFunceble.HTTP_CODE["active"]:
                    # The http status code request is activated.

                    # We construct what we have to print.
                    to_print = [self.subject, self.status, self.status_code]
                else:
                    # The http status code request is not activated.

                    # We construct what we have to print.
                    to_print = [self.subject, self.status, self.source]

                # And we print the informations on file.
                Prints(to_print, "Less", output, True).data()
            else:
                # The unified file generation is not activated.

                # We construct what we have to print.
                to_print = [
                    self.subject,
                    self.status,
                    self.expiration_date,
                    self.source,
                    self.status_code,
                    PyFunceble.CURRENT_TIME,
                ]

                # And we print the information on file.
                Prints(to_print, "Generic_File", output, True).data()

    def analytic_file(self, new_status, old_status=None):
        """
        Generate :code:`Analytic/*` files based on the given old and
        new statuses.

        :param new_status: The new status of the domain.
        :type new_status: str

        :param old_status: The old status of the domain.
        :type old_status: str
        """

        if not old_status:
            # The old status is not given.

            # We set the old status as the one given globally.
            old_status = self.status

        if self.subject_type.startswith("file_"):
            # We are not testing as an imported module.

            # We partially construct the path to the file to write/print.
            output = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS["analytic"]["directories"]["parent"]
                + "%s%s"
            )

            if new_status.lower() in PyFunceble.STATUS["list"]["up"]:
                # The new status is in the list of up status.

                # We complete the output directory.
                output = output % (
                    PyFunceble.OUTPUTS["analytic"]["directories"]["up"],
                    PyFunceble.OUTPUTS["analytic"]["filenames"]["up"],
                )

                # We generate the hosts file.
                Generate(
                    self.subject,
                    self.subject_type,
                    "HTTP_Active",
                    source=self.source,
                    expiration_date=self.expiration_date,
                    http_status_code=self.status_code,
                    whois_server=self.whois_server,
                    filename=self.filename,
                ).info_files()
            elif new_status.lower() in PyFunceble.STATUS["list"]["potentially_up"]:
                # The new status is in the list of down status.

                # We complete the output directory.
                output = output % (
                    PyFunceble.OUTPUTS["analytic"]["directories"]["potentially_up"],
                    PyFunceble.OUTPUTS["analytic"]["filenames"]["potentially_up"],
                )

                # We generate the hosts file.
                Generate(
                    self.subject,
                    self.subject_type,
                    "potentially_up",
                    source=self.source,
                    expiration_date=self.expiration_date,
                    http_status_code=self.status_code,
                    whois_server=self.whois_server,
                    filename=self.filename,
                ).info_files()
            elif new_status.lower() in PyFunceble.STATUS["list"]["suspicious"]:
                # The new status is in the list of suspicious status.

                # We complete the output directory.
                output = output % (
                    PyFunceble.OUTPUTS["analytic"]["directories"]["suspicious"],
                    PyFunceble.OUTPUTS["analytic"]["filenames"]["suspicious"],
                )

                # We generate the hosts file.
                Generate(
                    self.subject,
                    self.subject_type,
                    "suspicious",
                    source=self.source,
                    expiration_date=self.expiration_date,
                    http_status_code=self.status_code,
                    whois_server=self.whois_server,
                    filename=self.filename,
                ).info_files()
            else:
                # The new status is in the list of up and down status.

                # We complete the output directory.
                output = output % (
                    PyFunceble.OUTPUTS["analytic"]["directories"]["potentially_down"],
                    PyFunceble.OUTPUTS["analytic"]["filenames"]["potentially_down"],
                )

                # We generate the hosts files.
                Generate(
                    self.subject,
                    self.subject_type,
                    "potentially_down",
                    source=self.source,
                    expiration_date=self.expiration_date,
                    http_status_code=self.status_code,
                    whois_server=self.whois_server,
                    filename=self.filename,
                ).info_files()

            # We print the information on file.
            Prints(
                [self.subject, old_status, self.status_code, PyFunceble.CURRENT_TIME],
                "HTTP",
                output,
                True,
            ).data()

    def _prints_status_file(self):  # pylint: disable=too-many-branches
        """
        Logic behind the printing (in file) when generating status file.
        """

        if self.subject_type.startswith("file_"):
            # We are testing a file.

            output = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS["splited"]["directory"]
                + self.status
            )

            if PyFunceble.CONFIGURATION["less"]:
                # We have to print less information.

                # We print the information on file.
                Prints(
                    [self.subject, self.status, self.source], "Less", output, True
                ).data()
            elif PyFunceble.CONFIGURATION["split"]:
                # We have to split the information we print on file.

                if self.status.lower() in PyFunceble.STATUS["list"]["up"]:
                    # The status is in the list of up status.

                    if PyFunceble.HTTP_CODE["active"]:
                        # The http code extraction is activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.subject,
                            self.expiration_date,
                            self.source,
                            self.status_code,
                            PyFunceble.CURRENT_TIME,
                        ]
                    else:
                        # The http code extraction is not activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.subject,
                            self.expiration_date,
                            self.source,
                            PyFunceble.CURRENT_TIME,
                        ]

                    # We print the informations to print on file.
                    Prints(
                        data_to_print, PyFunceble.STATUS["official"]["up"], output, True
                    ).data()
                elif self.status.lower() in PyFunceble.STATUS["list"]["valid"]:
                    # The status is in the list of valid status.

                    # We initiate the data to print.
                    data_to_print = [self.subject, self.source, PyFunceble.CURRENT_TIME]

                    # We print the informations to print on file.
                    Prints(
                        data_to_print,
                        PyFunceble.STATUS["official"]["valid"],
                        output,
                        True,
                    ).data()
                elif self.status.lower() in PyFunceble.STATUS["list"]["down"]:
                    # The status is in the list of down status.

                    if PyFunceble.HTTP_CODE["active"]:
                        # The http statuc code extraction is activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.subject,
                            self.whois_server,
                            self.status,
                            self.source,
                            self.status_code,
                            PyFunceble.CURRENT_TIME,
                        ]
                    else:
                        # The http status code extraction is not activated.

                        # We initate the data to print.
                        data_to_print = [
                            self.subject,
                            self.whois_server,
                            self.status,
                            self.source,
                            PyFunceble.CURRENT_TIME,
                        ]

                    # We print the information on file.
                    Prints(
                        data_to_print,
                        PyFunceble.STATUS["official"]["down"],
                        output,
                        True,
                    ).data()
                elif self.status.lower() in PyFunceble.STATUS["list"]["invalid"]:
                    # The status is in the list of invalid status.

                    if PyFunceble.HTTP_CODE["active"]:
                        # The http status code extraction is activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.subject,
                            self.source,
                            self.status_code,
                            PyFunceble.CURRENT_TIME,
                        ]
                    else:
                        # The http status code extraction is not activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.subject,
                            self.source,
                            PyFunceble.CURRENT_TIME,
                        ]

                    # We print the information to print on file.
                    Prints(
                        data_to_print,
                        PyFunceble.STATUS["official"]["invalid"],
                        output,
                        True,
                    ).data()

    def _prints_status_screen(self):
        """
        Logic behind the printing (on screen) when generating status file.
        """

        if not PyFunceble.CONFIGURATION["quiet"]:
            # The quiet mode is not activated.

            if PyFunceble.CONFIGURATION["less"]:
                # We have to print less information.

                # We initiate the data to print.
                to_print = [self.subject, self.status, self.status_code]

                if not PyFunceble.HTTP_CODE["active"]:
                    # The http status code is not activated.

                    # We replace the last element to print with
                    # the source.
                    to_print[-1] = self.source

                # We print the informations on screen.
                Prints(to_print, "Less").data()
            else:
                # We have to print all informations on screen.

                if PyFunceble.HTTP_CODE["active"]:
                    # The http status code extraction is activated.

                    # We initiate the data to print.
                    data_to_print = [
                        self.subject,
                        self.status,
                        self.expiration_date,
                        self.source,
                        self.status_code,
                    ]
                else:
                    # The http status code extraction is not activated.

                    # We initiate the data to print.
                    data_to_print = [
                        self.subject,
                        self.status,
                        self.expiration_date,
                        self.source,
                        PyFunceble.CURRENT_TIME,
                    ]

                # We print the information on screen.
                Prints(data_to_print, "Generic").data()

    def status_file(self):  # pylint: disable=inconsistent-return-statements
        """
        Generate a file according to the domain status.
        """

        # We generate the hosts file.
        self.info_files()

        # We are testing a file content.

        # We increase the percentage count.
        Percentage(self.status).count()

        # We print on screen if needed.
        self._prints_status_screen()

        if self._do_not_produce_file():
            return None

        if (
            not PyFunceble.CONFIGURATION["no_files"]
            and PyFunceble.CONFIGURATION["split"]
        ):
            # * The file non-generation of file is globaly deactivated.
            # and
            # * We have to split the outputs.

            # We print or generate the files.
            self._prints_status_file()
        else:
            # * The file non-generation of file is globaly activated.
            # or
            # * We do not have to split the outputs.

            # We print or generate the unified files.
            self.unified_file()

    def _do_not_produce_file(self):
        """
        Check if we are allowed to produce a file based from the given
        information.

        :return:
            The state of the production.
            True: We do not produce file.
            False: We do produce file.
        :rtype: bool
        """

        if PyFunceble.CONFIGURATION["no_files"]:
            return True

        if self.filename:
            inactive_db = InactiveDB(self.filename)
        else:
            inactive_db = []

        if self.subject in inactive_db and self.status in [
            PyFunceble.STATUS["official"]["down"],
            PyFunceble.STATUS["official"]["invalid"],
        ]:
            return True
        return False
