"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the content/output generator.

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

from datetime import datetime
from os import sep as directory_separator

import PyFunceble


class Generate:  # pylint:disable=too-many-instance-attributes, too-many-arguments
    """
    Generate different sort of files.

    :param str subject: The subject we are working with.

    :param str subject_type: The type of the subject.

    :param str status: The catched status.

    :param str source: The source of the given status.

    :param str expiration_date:
        The expiration date of the domain (if catched).

    :param http_status_code: The HTTP status code.
    :type http_status_code: str|int

    :param str whois_server: The whois server.

    :param str filename:
        The name of the file we are testing.

    :param bool ip_validation:
        The IP validation check of the currently written subject.
    """

    def __init__(
        self,
        subject,
        subject_type,
        status,
        source=None,
        expiration_date=None,
        http_status_code=None,
        whois_server="Unknown",
        filename=None,
        ip_validation=False,
        end=False,
    ):
        # We share the subject.
        self.subject = subject
        # We share the subject type.
        self.subject_type = subject_type
        # We share the status
        self.status = status
        # We get the source.
        self.source = source
        # We share the file name.
        self.filename = filename
        # We share the IP validation.
        self.ip_validation = ip_validation
        # We share the end state.
        self.end = end

        if not http_status_code:
            self.status_code = PyFunceble.HTTP_CODE.not_found_default
        else:
            self.status_code = http_status_code

        if not whois_server:
            self.whois_server = "Unknown"
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
            PyFunceble.OUTPUT_DIRECTORY + PyFunceble.OUTPUTS.parent_directory
        )

        user_agent = PyFunceble.engine.UserAgent().get()

        if user_agent:
            # The user-agent (from the configuration file) is not empty.

            # We initiate the header to use with our request.
            self.headers = {"User-Agent": user_agent}
        else:
            # The user-agent (from the configuration file) is empty.

            # We initiate an empty header to use with our request.
            self.headers = {}

        self.file_production = not self._do_not_produce_file()

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

        # pylint: disable=unsupported-membership-test
        if "api_file_generation" in PyFunceble.CONFIGURATION:
            return not PyFunceble.CONFIGURATION.api_file_generation

        if PyFunceble.CONFIGURATION.db_type in ["mariadb", "mysql"]:
            return not self.end

        return PyFunceble.CONFIGURATION.no_files

    def _analytic_host_file_directory(self):
        """
        Return the analytic directory to write depending of the matched
        status.
        """

        # We construct the path to the analytic directory.
        output_dir = (
            self.output_parent_dir + PyFunceble.OUTPUTS.analytic.directories.parent
        )

        if self.status.lower() in PyFunceble.STATUS.list.potentially_up:
            # The status is in the list of analytic up status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS.analytic.directories.potentially_up
        elif self.status.lower() in PyFunceble.STATUS.list.potentially_down:
            # The status is in the list of analytic down status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS.analytic.directories.potentially_down
        elif self.status.lower() in PyFunceble.STATUS.list.suspicious:
            # The status is in the list of analytic suspicious status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS.analytic.directories.suspicious
        else:
            # The status is not in the list of analytic down or up status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS.analytic.directories.up

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
            self.file_production
            and self.subject_type.startswith("file_")
            and (
                PyFunceble.CONFIGURATION.generate_hosts
                or PyFunceble.CONFIGURATION.plain_list_domain
                or PyFunceble.CONFIGURATION.generate_json
            )
            or PyFunceble.CONFIGURATION.api_file_generation
        )

    def ___get_info_files_destinations(self, output_hosts, output_domains, output_json):
        """
        Given the output directory, this method return several paths.

        .. note::
            The given output directories have to be partially completed.

            Indeed, we only do :code:`output % final_location`.

        :return:
            The following paths:

            ::

                (
                    hosts_destination,
                    plain_destination,
                    json_destination,
                    splited_destination
                )

        :rtype: tuple
        """

        # We present the splited destination.
        splited_destination = None

        # We initiate the list of all analytic related statuses.
        http_list = []
        http_list.extend(PyFunceble.STATUS.list.potentially_up)
        http_list.extend(PyFunceble.STATUS.list.potentially_down)
        http_list.extend(PyFunceble.STATUS.list.http_active)
        http_list.extend(PyFunceble.STATUS.list.suspicious)

        if self.status.lower() in PyFunceble.STATUS.list.valid:
            # The status is in the list of valid list.

            # We complete the path to the hosts file.
            hosts_destination = output_hosts % PyFunceble.STATUS.official.valid

            # We complete the path to the plain list file.
            plain_destination = output_domains % PyFunceble.STATUS.official.valid

            # We complete the path to the json list file.
            json_destination = output_json % PyFunceble.STATUS.official.valid
        elif self.status.lower() in PyFunceble.STATUS.list.sane:
            # The status is in the list of sane list.

            # We complete the path to the hosts file.
            hosts_destination = output_hosts % PyFunceble.STATUS.official.sane

            # We complete the path to the plain list file.
            plain_destination = output_domains % PyFunceble.STATUS.official.sane

            # We complete the path to the json list file.
            json_destination = output_json % PyFunceble.STATUS.official.sane
        elif self.status.lower() in PyFunceble.STATUS.list.up:
            # The status is in the list of up list.

            # We complete the path to the hosts file.
            hosts_destination = output_hosts % PyFunceble.STATUS.official.up

            # We complete the path to the plain list file.
            plain_destination = output_domains % PyFunceble.STATUS.official.up

            # We complete the path to the json list file.
            json_destination = output_json % PyFunceble.STATUS.official.up
        elif self.status.lower() in PyFunceble.STATUS.list.malicious:
            # The status is in the list of malicious list.

            # We complete the path to the hosts file.
            hosts_destination = output_hosts % PyFunceble.STATUS.official.malicious

            # We complete the path to the plain list file.
            plain_destination = output_domains % PyFunceble.STATUS.official.malicious

            # We complete the path to the json list file.
            json_destination = output_json % PyFunceble.STATUS.official.malicious
        elif self.status.lower() in PyFunceble.STATUS.list.down:
            # The status is in the list of down list.

            # We complete the path to the hosts file.
            hosts_destination = output_hosts % PyFunceble.STATUS.official.down

            # We complete the path to the plain list file.
            plain_destination = output_domains % PyFunceble.STATUS.official.down

            # We complete the path to the json list file.
            json_destination = output_json % PyFunceble.STATUS.official.down
        elif self.status.lower() in PyFunceble.STATUS.list.invalid:
            # The status is in the list of invalid list.

            # We complete the path to the hosts file.
            hosts_destination = output_hosts % PyFunceble.STATUS.official.invalid

            # We complete the path to the plain list file.
            plain_destination = output_domains % PyFunceble.STATUS.official.invalid

            # We complete the path to the json list file.
            json_destination = output_json % PyFunceble.STATUS.official.invalid
        elif self.status.lower() in http_list:
            # The status is in the list of analytic status.

            # We construct the path to the analytic directory.
            output_dir = self._analytic_host_file_directory()

            if not output_dir.endswith(directory_separator):
                # The output directory does not ends with the directory separator.

                # We append the directory separator at the end of the output directory.
                output_dir += directory_separator

            # We initiate the hosts file path.
            hosts_destination = output_dir + PyFunceble.OUTPUTS.hosts.filename

            # We initiate the plain list file path.
            plain_destination = output_dir + PyFunceble.OUTPUTS.domains.filename

            # We complete the path to the json list file.
            json_destination = output_dir + PyFunceble.OUTPUTS.json.filename

            # We initiate the path to the http code file.
            # Note: We generate the http code file so that
            # we can have each domain in a file which is the
            # extracted http code.
            splited_destination = output_dir + str(self.status_code)
        elif self.status.lower().startswith("complements_"):
            # The status is in the list of complements status.

            # We convert the status to lower case.
            status = self.status.lower()
            # We get the status type.
            status_type = status[status.find("_") + 1 :]

            # We construct the path to the complements directory.
            output_dir = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS.complements.directory
                + PyFunceble.STATUS.official[status_type]
            )

            if not output_dir.endswith(directory_separator):
                # The output directory does not ends with the directory separator.

                # We append the directory separator at the end of the output directory.
                output_dir += directory_separator

            # We initiate the hosts file path.
            hosts_destination = output_dir + PyFunceble.OUTPUTS.hosts.filename

            # We initiate the plain list file path.
            plain_destination = output_dir + PyFunceble.OUTPUTS.domains.filename

            # We complete the path to the json list file.
            json_destination = output_dir + PyFunceble.OUTPUTS.json.filename

        return (
            hosts_destination,
            plain_destination,
            json_destination,
            splited_destination,
        )

    # pylint: disable=inconsistent-return-statements,too-many-branches
    def info_files(self):
        """
        Generate the hosts file, the plain list, the JSON file and the splitted files.
        """

        if self.___info_files_authorization():
            # We initiate a variable which whill save the splited testination.
            splited_destination = ""

            # We partially initiate the path to the hosts file.
            output_hosts = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS.hosts.directory
                + "%s"
                + directory_separator
                + PyFunceble.OUTPUTS.hosts.filename
            )

            # We partially initiate the path to the plain list file.
            output_domains = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS.domains.directory
                + "%s"
                + directory_separator
                + PyFunceble.OUTPUTS.domains.filename
            )

            # We partially intiate the path to the json list file.
            output_json = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS.json.directory
                + "%s"
                + directory_separator
                + PyFunceble.OUTPUTS.json.filename
            )

            if self.ip_validation:
                # The element is an IP.

                # We construct the output file.
                output_hosts = (
                    self.output_parent_dir
                    + PyFunceble.OUTPUTS.hosts.directory
                    + "%s"
                    + directory_separator
                    + PyFunceble.OUTPUTS.hosts.ip_filename
                )

            # We get the destination of the different files.
            (
                hosts_destination,
                plain_destination,
                json_destination,
                splited_destination,
            ) = self.___get_info_files_destinations(
                output_hosts, output_domains, output_json
            )

            if PyFunceble.CONFIGURATION.generate_hosts:
                # The hosts file generation is activated.

                # We generate/append the currently tested element in its
                # final location. (hosts file format)
                # We print on screen and on file.
                PyFunceble.output.Prints(
                    [PyFunceble.CONFIGURATION.custom_ip, self.subject],
                    "FullHosts",
                    hosts_destination,
                ).data()

            if PyFunceble.CONFIGURATION.plain_list_domain:
                # The plain list generation is activated.

                # We generate/append the currently tested element in its
                # final location. (the plain list format)
                # We print on file.
                PyFunceble.output.Prints(
                    [self.subject], "PlainDomain", plain_destination
                ).data()

            if PyFunceble.CONFIGURATION.split and splited_destination:
                # The splited list generation is activated.

                # We generate/append the currently tested element in its
                # final location. (the split list format)
                # We print on file.
                PyFunceble.output.Prints(
                    [self.subject], "PlainDomain", splited_destination
                ).data()

            if PyFunceble.CONFIGURATION.generate_json:
                # The json list generation is activated.

                # We generate/append the currently tested element in its
                # final location. (the json format)
                # We print on file.
                PyFunceble.output.Prints(
                    [self.subject], "JSON", json_destination
                ).data()

    def unified_file(self):
        """
        Generate unified file. Understand by that that we use an unified table
        instead of a separate table for each status which could result into a
        misunderstanding.
        """

        if (
            self.file_production
            and self.subject_type.startswith("file_")
            and PyFunceble.CONFIGURATION.unified
            and not PyFunceble.CONFIGURATION.split
        ):
            # * We are not testing as an imported module.
            # and
            # * The unified file generation is activated.

            # We construct the path of the unified file.
            output = self.output_parent_dir + PyFunceble.OUTPUTS.default_files.results

            if PyFunceble.CONFIGURATION.simple:
                to_print = [self.subject, self.status]

                PyFunceble.output.Prints(to_print, "Simple", output, True).data()
            elif PyFunceble.CONFIGURATION.less:
                # We have to print less information.

                if PyFunceble.HTTP_CODE.active:
                    # The http status code request is activated.

                    # We construct what we have to print.
                    to_print = [self.subject, self.status, self.status_code]
                else:
                    # The http status code request is not activated.

                    # We construct what we have to print.
                    to_print = [self.subject, self.status, self.source]

                # And we print the informations on file.
                PyFunceble.output.Prints(to_print, "Less", output, True).data()
            else:
                # The unified file generation is not activated.

                # We construct what we have to print.
                to_print = [
                    self.subject,
                    self.status,
                    self.expiration_date,
                    self.source,
                    self.status_code,
                    datetime.now().isoformat(),
                ]

                # And we print the information on file.
                PyFunceble.output.Prints(to_print, "Generic_File", output, True).data()

    def complements_file(self):
        """
        Generate :code:`complements` files base on the current status.
        """

        if self.subject_type.startswith("file_"):
            # We are testing files.

            # We map the way we are going to work.
            status_map = {
                "up": "complements_UP",
                "down": "complements_DOWN",
                "invalid": "complements_INVALID",
                "valid": "complements_VALID",
            }

            for status, generate_status in status_map.items():
                # We loop through the list of status.

                if self.status.lower() in PyFunceble.STATUS.list[status]:
                    # The status is found.

                    # We generate the different files.
                    Generate(
                        self.subject,
                        self.subject_type,
                        generate_status,
                        source=self.source,
                        expiration_date=self.expiration_date,
                        http_status_code=self.status_code,
                        whois_server=self.whois_server,
                        filename=self.filename,
                        ip_validation=self.ip_validation,
                    ).info_files()

                    # We break the loop.
                    break

    def analytic_file(self, new_status, old_status=None):
        """
        Generate :code:`Analytic/*` files based on the given old and
        new statuses.

        :param str new_status: The new status of the domain.

        :param str old_status: The old status of the domain.
        """

        if not old_status:
            # The old status is not given.

            # We set the old status as the one given globally.
            old_status = self.status

        if self.subject_type.startswith("file_"):
            # We are testing files.

            # We map the way we are going to work with the status.
            status_map = {
                "up": "HTTP_Active",
                "potentially_up": "potentially_up",
                "suspicious": "suspicious",
            }

            # We keep a track of the map usage.
            map_used = False

            # We partially construct the path to the file to write/print.
            output = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS.analytic.directories.parent
                + "%s%s"
            )

            for status, generate_status in status_map.items():
                # We loop through our map.

                if new_status.lower() in PyFunceble.STATUS.list[status]:
                    # The status is found into our map.

                    # We conmplete the output directory.
                    output = output % (
                        PyFunceble.OUTPUTS.analytic.directories.status,
                        PyFunceble.OUTPUTS.analytic.filenames.status,
                    )

                    # We generate the different file(s).
                    Generate(
                        self.subject,
                        self.subject_type,
                        generate_status,
                        source=self.source,
                        expiration_date=self.expiration_date,
                        http_status_code=self.status_code,
                        whois_server=self.whois_server,
                        filename=self.filename,
                        ip_validation=self.ip_validation,
                    ).info_files()

                    # We update the map usage.
                    map_used = True

                    # And we break the loop.
                    break

            if not map_used:
                # The map was not user, that means that
                # we are working with potentially inactive domains.

                # We complete the output directory.
                output = output % (
                    PyFunceble.OUTPUTS.analytic.directories.potentially_down,
                    PyFunceble.OUTPUTS.analytic.filenames.potentially_down,
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
                    ip_validation=self.ip_validation,
                ).info_files()

            # We print the information on file.
            PyFunceble.output.Prints(
                [
                    self.subject,
                    old_status,
                    self.status_code,
                    datetime.now().isoformat(),
                ],
                "HTTP",
                output,
                True,
            ).data()

    def prints_status_file(self):  # pylint: disable=too-many-branches
        """
        Logic behind the printing (in file) when generating status file.
        """

        if (
            self.file_production
            and self.subject_type.startswith("file_")
            and PyFunceble.CONFIGURATION.split
        ):
            # We are testing a file.

            output = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS.splited.directory
                + self.status
            )

            if PyFunceble.CONFIGURATION.simple:
                PyFunceble.output.Prints(
                    [self.subject, self.status], "Simple", output, True
                ).data()
            elif PyFunceble.CONFIGURATION.less:
                # We have to print less information.

                # We print the information on file.
                PyFunceble.output.Prints(
                    [self.subject, self.status, self.source], "Less", output, True
                ).data()
            elif PyFunceble.CONFIGURATION.split:
                # We have to split the information we print on file.

                if self.status.lower() in PyFunceble.STATUS.list.up:
                    # The status is in the list of up status.

                    if PyFunceble.HTTP_CODE.active:
                        # The http code extraction is activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.subject,
                            self.expiration_date,
                            self.source,
                            self.status_code,
                            datetime.now().isoformat(),
                        ]
                    else:
                        # The http code extraction is not activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.subject,
                            self.expiration_date,
                            self.source,
                            datetime.now().isoformat(),
                        ]

                    # We print the informations to print on file.
                    PyFunceble.output.Prints(
                        data_to_print, PyFunceble.STATUS.official.up, output, True
                    ).data()
                elif self.status.lower() in PyFunceble.STATUS.list.valid:
                    # The status is in the list of valid status.

                    # We initiate the data to print.
                    data_to_print = [
                        self.subject,
                        self.source,
                        datetime.now().isoformat(),
                    ]

                    # We print the informations to print on file.
                    PyFunceble.output.Prints(
                        data_to_print, PyFunceble.STATUS.official.valid, output, True
                    ).data()
                elif self.status.lower() in PyFunceble.STATUS.list.sane:
                    # The status is in the list of sane status.

                    # We initiate the data to print.
                    data_to_print = [
                        self.subject,
                        self.source,
                        datetime.now().isoformat(),
                    ]

                    # We print the informations to print on file.
                    PyFunceble.output.Prints(
                        data_to_print, PyFunceble.STATUS.official.sane, output, True
                    ).data()
                elif self.status.lower() in PyFunceble.STATUS.list.malicious:
                    # The status is in the list of malicious status.

                    # We initiate the data to print.
                    data_to_print = [
                        self.subject,
                        self.source,
                        datetime.now().isoformat(),
                    ]

                    # We print the informations to print on file.
                    PyFunceble.output.Prints(
                        data_to_print,
                        PyFunceble.STATUS.official.malicious,
                        output,
                        True,
                    ).data()
                elif self.status.lower() in PyFunceble.STATUS.list.down:
                    # The status is in the list of down status.

                    if PyFunceble.HTTP_CODE.active:
                        # The http statuc code extraction is activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.subject,
                            self.whois_server,
                            self.status,
                            self.source,
                            self.status_code,
                            datetime.now().isoformat(),
                        ]
                    else:
                        # The http status code extraction is not activated.

                        # We initate the data to print.
                        data_to_print = [
                            self.subject,
                            self.whois_server,
                            self.status,
                            self.source,
                            datetime.now().isoformat(),
                        ]

                    # We print the information on file.
                    PyFunceble.output.Prints(
                        data_to_print, PyFunceble.STATUS.official.down, output, True
                    ).data()
                elif self.status.lower() in PyFunceble.STATUS.list.invalid:
                    # The status is in the list of invalid status.

                    if PyFunceble.HTTP_CODE.active:
                        # The http status code extraction is activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.subject,
                            self.source,
                            self.status_code,
                            datetime.now().isoformat(),
                        ]
                    else:
                        # The http status code extraction is not activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.subject,
                            self.source,
                            datetime.now().isoformat(),
                        ]

                    # We print the information to print on file.
                    PyFunceble.output.Prints(
                        data_to_print, PyFunceble.STATUS.official.invalid, output, True
                    ).data()

    def _prints_status_screen(self):
        """
        Logic behind the printing (on screen) when generating status file.
        """

        if not PyFunceble.CONFIGURATION.quiet:
            # The quiet mode is not activated.

            if PyFunceble.CONFIGURATION.simple:
                # We have to print simple infomation.

                # We initiate the data to print.
                to_print = [self.subject, self.status]

                PyFunceble.output.Prints(to_print, "Simple").data()
            elif PyFunceble.CONFIGURATION.less:
                # We have to print less information.

                # We initiate the data to print.
                to_print = [self.subject, self.status, self.status_code]

                if not PyFunceble.HTTP_CODE.active:
                    # The http status code is not activated.

                    # We replace the last element to print with
                    # the source.
                    to_print[-1] = self.source

                # We print the informations on screen.
                PyFunceble.output.Prints(to_print, "Less").data()
            else:
                # We have to print all informations on screen.

                if PyFunceble.HTTP_CODE.active:
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
                        datetime.now().isoformat(),
                    ]

                # We print the information on screen.
                PyFunceble.output.Prints(data_to_print, "Generic").data()
        elif "ci_initiated" in PyFunceble.INTERN or PyFunceble.CONFIGURATION.print_dots:
            # We are under a CI/CD environment.

            PyFunceble.LOGGER.info(f"Generation of output file for {self.subject!r}.")

            # We print a dot.
            print(".", end="")

    def status_file(
        self, exclude_file_generation=False
    ):  # pylint: disable=inconsistent-return-statements
        """
        Generate a file according to the domain status.

        :param bool exclude_file_generation:
            A shorthand to disable any file generation.
        """

        if exclude_file_generation:
            self.file_production = False

        # We generate the hosts file.
        self.info_files()

        if not self.end:
            # We print on screen if needed.
            self._prints_status_screen()

        # We increase the percentage count.
        PyFunceble.output.Percentage(self.status).count()

        if self.file_production:

            # We print or generate the  splitted files.
            self.prints_status_file()
            # We print or generate the unified files.
            self.unified_file()
