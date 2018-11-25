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

This submodule will create the generation interface/logic.

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
# pylint: disable=bad-continuation, too-many-lines
import PyFunceble
from PyFunceble import directory_separator, requests
from PyFunceble.check import Check
from PyFunceble.helpers import Regex
from PyFunceble.percentage import Percentage
from PyFunceble.prints import Prints


class Generate:  # pragma: no cover pylint:disable=too-many-instance-attributes
    """
    Generate different sort of files.

    :param domain_status: The domain status.
    :type domain_status: str

    :param source: The source of the given status.
    :type source: str

    :param expiration_date: The expiration date of the domain (if catched).
    :type expiration_date: str
    """

    def __init__(self, domain_status, source=None, expiration_date=None):
        # We get the domain status.
        self.domain_status = domain_status

        # We get the source.
        self.source = source

        # We get the expiration date.
        self.expiration_date = expiration_date

        # We construct the output parent directory.
        self.output_parent_dir = (
            PyFunceble.OUTPUT_DIRECTORY + PyFunceble.OUTPUTS["parent_directory"]
        )

        # We set a variable which will save the referer status.
        self.refer_status = ""

        # We set a variable which will save the output.
        self.output = ""

        if (
            "to_test" in PyFunceble.CONFIGURATION
            and PyFunceble.CONFIGURATION["to_test"]
        ):
            # We are testing something.

            # We save it into an unified variable.
            self.tested = PyFunceble.CONFIGURATION["to_test"]

        if PyFunceble.CONFIGURATION["user_agent"]:
            # The user-agent (from the configuration file) is not empty.

            # We initiate the header to use with our request.
            self.headers = {"User-Agent": PyFunceble.CONFIGURATION["user_agent"]}
        else:
            # The user-agent (from the configuration file) is empty.

            # We initiate an empty header to use with our request.
            self.headers = {}

        # We handle possible non existant index.
        self._handle_non_existant_index()

    @classmethod
    def _handle_non_existant_index(cls):
        """
        Handle and check that some configuration index exists.
        """

        try:
            # We try to call the http code.
            PyFunceble.CONFIGURATION["http_code"]
        except KeyError:
            # If it is not found.

            # We initiate an empty http code.
            PyFunceble.CONFIGURATION["http_code"] = "*" * 3

        try:
            # We try to call the referer.
            PyFunceble.CONFIGURATION["referer"]
        except KeyError:
            # If it is not found.

            # We initate an `Unknown` referer.
            PyFunceble.CONFIGURATION["referer"] = "Unknown"

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

        if self.domain_status.lower() in PyFunceble.STATUS["list"]["potentially_up"]:
            # The status is in the list of analytic up status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS["analytic"]["directories"][
                "potentially_up"
            ]
        elif (
            self.domain_status.lower() in PyFunceble.STATUS["list"]["potentially_down"]
        ):
            # The status is in the list of analytic down status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS["analytic"]["directories"][
                "potentially_down"
            ]
        elif self.domain_status.lower() in PyFunceble.STATUS["list"]["suspicious"]:
            # The status is in the list of analytic suspicious status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS["analytic"]["directories"]["suspicious"]
        else:
            # The status is not in the list of analytic down or up status.

            # We complete the output directory.
            output_dir += PyFunceble.OUTPUTS["analytic"]["directories"]["up"]

        return output_dir

    def info_files(self):
        """
        Generate the hosts file, the plain list and the splitted lists.
        """

        if (
            "file_to_test" in PyFunceble.CONFIGURATION
            and PyFunceble.CONFIGURATION["file_to_test"]
            and (
                PyFunceble.CONFIGURATION["generate_hosts"]
                or PyFunceble.CONFIGURATION["plain_list_domain"]
                or PyFunceble.CONFIGURATION["generate_json"]
            )
        ):
            # * We are testing a file.
            # and
            # * The hosts file generation is activated.
            # or
            # * The plain list generation is activated.

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

            if self.domain_status.lower() in PyFunceble.STATUS["list"]["up"]:
                # The status is in the list of up list.

                # We complete the path to the hosts file.
                hosts_destination = output_hosts % PyFunceble.STATUS["official"]["up"]

                # We complete the path to the plain list file.
                plain_destination = output_domains % PyFunceble.STATUS["official"]["up"]

                # We complete the path to the json list file.
                json_destination = output_json % PyFunceble.STATUS["official"]["up"]
            elif self.domain_status.lower() in PyFunceble.STATUS["list"]["valid"]:
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
            elif self.domain_status.lower() in PyFunceble.STATUS["list"]["down"]:
                # The status is in the list of down list.

                # We complete the path to the hosts file.
                hosts_destination = output_hosts % PyFunceble.STATUS["official"]["down"]

                # We complete the path to the plain list file.
                plain_destination = (
                    output_domains % PyFunceble.STATUS["official"]["down"]
                )

                # We complete the path to the json list file.
                json_destination = output_json % PyFunceble.STATUS["official"]["down"]
            elif self.domain_status.lower() in PyFunceble.STATUS["list"]["invalid"]:
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
            elif self.domain_status.lower() in http_list:
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
                splited_destination = output_dir + str(
                    PyFunceble.CONFIGURATION["http_code"]
                )

            if PyFunceble.CONFIGURATION["generate_hosts"]:
                # The hosts file generation is activated.

                # We generate/append the currently tested element in its
                # final location. (hosts file format)
                # We print on screen and on file.
                Prints(
                    [PyFunceble.CONFIGURATION["custom_ip"], self.tested],
                    "FullHosts",
                    hosts_destination,
                ).data()

            if PyFunceble.CONFIGURATION["plain_list_domain"]:
                # The plain list generation is activated.

                # We generate/append the currently tested element in its
                # final location. (the plain list format)
                # We print on file.
                Prints([self.tested], "PlainDomain", plain_destination).data()

            if PyFunceble.CONFIGURATION["split"] and splited_destination:
                # The splited list generation is activated.

                # We generate/append the currently tested element in its
                # final location. (the split list format)
                # We print on file.
                Prints([self.tested], "PlainDomain", splited_destination).data()

            if PyFunceble.CONFIGURATION["generate_json"]:
                # The jsaon list generation is activated.

                # We generate/append the currently tested element in its
                # final location. (the json format)
                # We print on file.
                Prints([self.tested], "JSON", json_destination).data()

    def unified_file(self):
        """
        Generate unified file. Understand by that that we use an unified table
        instead of a separate table for each status which could result into a
        misunderstanding.
        """

        if (
            "file_to_test" in PyFunceble.CONFIGURATION
            and PyFunceble.CONFIGURATION["file_to_test"]
            and PyFunceble.CONFIGURATION["unified"]
        ):
            # * We are testing a file.
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
                    to_print = [
                        self.tested,
                        self.domain_status,
                        PyFunceble.CONFIGURATION["http_code"],
                    ]
                else:
                    # The http status code request is not activated.

                    # We construct what we have to print.
                    to_print = [self.tested, self.domain_status, self.source]

                # And we print the informations on file.
                Prints(to_print, "Less", output, True).data()
            else:
                # The unified file generation is not activated.

                # We construct what we have to print.
                to_print = [
                    self.tested,
                    self.domain_status,
                    self.expiration_date,
                    self.source,
                    PyFunceble.CONFIGURATION["http_code"],
                    PyFunceble.CURRENT_TIME,
                ]

                # And we print the information on file.
                Prints(to_print, "Generic_File", output, True).data()

    def analytic_file(self, new_status, old_status):
        """
        Generate :code:`Analytic/*` files based on the given old and
        new statuses.

        :param new_status: The new status of the domain.
        :type new_status: str

        :param old_status: The old status of the domain.
        :type old_status: str
        """

        if PyFunceble.CONFIGURATION["file_to_test"]:
            # We are testing a file.

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
                Generate("HTTP_Active").info_files()
            elif new_status.lower() in PyFunceble.STATUS["list"]["potentially_up"]:
                # The new status is in the list of down status.

                # We complete the output directory.
                output = output % (
                    PyFunceble.OUTPUTS["analytic"]["directories"]["potentially_up"],
                    PyFunceble.OUTPUTS["analytic"]["filenames"]["potentially_up"],
                )

                # We generate the hosts file.
                Generate("potentially_up").info_files()
            elif new_status.lower() in PyFunceble.STATUS["list"]["suspicious"]:
                # The new status is in the list of suspicious status.

                # We complete the output directory.
                output = output % (
                    PyFunceble.OUTPUTS["analytic"]["directories"]["suspicious"],
                    PyFunceble.OUTPUTS["analytic"]["filenames"]["suspicious"],
                )

                # We generate the hosts file.
                Generate("suspicious").info_files()
            else:
                # The new status is in the list of up and down status.

                # We complete the output directory.
                output = output % (
                    PyFunceble.OUTPUTS["analytic"]["directories"]["potentially_down"],
                    PyFunceble.OUTPUTS["analytic"]["filenames"]["potentially_down"],
                )

                # We generate the hosts files.
                Generate("potentially_down").info_files()

            # We print the information on file.
            Prints(
                [
                    self.tested,
                    old_status,
                    PyFunceble.CONFIGURATION["http_code"],
                    PyFunceble.CURRENT_TIME,
                ],
                "HTTP",
                output,
                True,
            ).data()

    def _special_blogspot(self):
        """
        Handle the blogspot SPECIAL case.
        """

        # We initate a variable whith a regex which will match all blogpost domain.
        regex_blogspot = ".blogspot."

        # We iniate a list of elements in the HTML which will tell us more about
        # the status of the domain.
        regex_blogger = ["create-blog.g?", "87065", "doesn&#8217;t&nbsp;exist"]

        if PyFunceble.CONFIGURATION["to_test_type"] == "domain":
            # The element we are testing is a domain.

            # We construct the url to get.
            url_to_get = "http://%s" % self.tested
        elif PyFunceble.CONFIGURATION["to_test_type"] == "url":
            # The element we are testing is a URL.

            # We construct the url to get.
            url_to_get = self.tested
        else:
            raise Exception("Unknow test type.")

        if Regex(self.tested, regex_blogspot, return_data=False, escape=True).match():
            # The element we are testing is a blogspot subdomain.

            # We get the HTML of the home page.
            blogger_content_request = requests.get(url_to_get, headers=self.headers)

            for regx in regex_blogger:
                # We loop through the list of regex to match.

                if (
                    regx in blogger_content_request.text
                    or Regex(
                        blogger_content_request.text,
                        regx,
                        return_data=False,
                        escape=False,
                    ).match()
                ):
                    # The content match the currently read regex.

                    # We update the source.
                    self.source = "SPECIAL"

                    # We update the domain status.
                    self.domain_status = PyFunceble.STATUS["official"]["down"]

                    # We update the output file.
                    self.output = (
                        self.output_parent_dir
                        + PyFunceble.OUTPUTS["splited"]["directory"]
                        + self.domain_status
                    )

                    # And we break the loop as we matched something.
                    break

    def _special_wordpress_com(self):
        """
        Handle the wordpress.com special case.
        """

        # We initiate the domain to match.
        wordpress_com = ".wordpress.com"

        # We initiate a variable which whill have to be into the HTML
        # in order to be considered as inactive.
        does_not_exist = "doesn&#8217;t&nbsp;exist"

        if self.tested.endswith(wordpress_com):
            # The currently tested element ends with wordpress.com.

            # We get the content of the page.
            wordpress_com_content = requests.get(
                "http://%s:80" % self.tested, headers=self.headers
            )

            if does_not_exist in wordpress_com_content.text:
                # The marker is into the page content.

                # We update the source.
                self.source = "SPECIAL"

                # We update the status.
                self.domain_status = PyFunceble.STATUS["official"]["down"]

                # We update the output file.
                self.output = (
                    self.output_parent_dir
                    + PyFunceble.OUTPUTS["splited"]["directory"]
                    + self.domain_status
                )

    def up_status_file(self):
        """
        Logic behind the up status when generating the status file.
        """

        if not self.expiration_date:
            # The expiration date is not given.

            # We update the expiration date.
            self.expiration_date = "Unknown"

        if (
            PyFunceble.HTTP_CODE["active"]
            and PyFunceble.CONFIGURATION["http_code"]
            in PyFunceble.HTTP_CODE["list"]["potentially_down"]
        ):
            # * The http status request is activated.
            # and
            # * The extracted http status code is in the list of
            #   potentially down list.

            # We generate the analytics files.
            self.analytic_file("potentially_down", self.domain_status)

            # We initiate a list of domain which are actually.
            # down if they return for example 404 as status code.
            domain_to_match = [
                ".canalblog.com",
                ".doubleclick.net",
                ".liveadvert.com",
                ".skyrock.com",
                ".tumblr.com",
            ]

            for domain_to_handle in domain_to_match:
                # We loop through the list of of domain to handle.

                if self.tested.endswith(domain_to_handle):
                    # The currently tested domain is endswith
                    # the curerntly read domain to handle.

                    # We update the source.
                    self.source = "SPECIAL"

                    # We update the status.
                    self.domain_status = PyFunceble.STATUS["official"]["down"]

                    # We update the output file.s
                    self.output = (
                        self.output_parent_dir
                        + PyFunceble.OUTPUTS["splited"]["directory"]
                        + self.domain_status
                    )

            # We check again the special blogspot case.
            self._special_blogspot()
        elif (
            PyFunceble.HTTP_CODE["active"]
            and PyFunceble.CONFIGURATION["http_code"]
            in PyFunceble.HTTP_CODE["list"]["potentially_up"]
        ):
            # * The http status code request is activated.
            # and
            # * The extracted http status code is into the list of potentially up codes.

            # We handle the blogpost special case.
            self._special_blogspot()

            # And we handle the wordpress special case.
            self._special_wordpress_com()

        if self.source != "SPECIAL":
            # The source is not equal to `SPECIAL`.

            # We update the domain status.
            self.domain_status = PyFunceble.STATUS["official"]["up"]

            # We update the output file.
            self.output = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS["splited"]["directory"]
                + self.domain_status
            )

    def valid_status_file(self):
        """
        Logic behind the valis status when generating the status file.
        """

        # We update the expiration date.
        self.expiration_date = "Unknown"

        # We update the domain status.
        self.domain_status = PyFunceble.STATUS["official"]["valid"]

        # We update the output file.
        self.output = (
            self.output_parent_dir
            + PyFunceble.OUTPUTS["splited"]["directory"]
            + self.domain_status
        )

    def down_status_file(self):
        """
        Logic behind the down status when generating the status file.
        """

        # We update the referer status.
        self.refer_status = "Not Found"

        # We update the expiration date.
        self.expiration_date = "Unknown"

        if PyFunceble.HTTP_CODE["active"]:
            # The http status code request is activated.

            if (
                PyFunceble.CONFIGURATION["http_code"]
                in PyFunceble.HTTP_CODE["list"]["up"]
            ):
                # The extracted http code in in the list of up codes.

                # We generate the analytic file(s).
                self.analytic_file(
                    PyFunceble.STATUS["official"]["up"], self.domain_status
                )

                # We update the source.
                self.source = "HTTP Code"

                # We update the status.
                self.domain_status = PyFunceble.STATUS["official"]["up"]

                # We update the output file.
                self.output = (
                    self.output_parent_dir
                    + PyFunceble.OUTPUTS["splited"]["directory"]
                    + self.domain_status
                )
            elif (
                PyFunceble.CONFIGURATION["http_code"]
                in PyFunceble.HTTP_CODE["list"]["potentially_up"]
            ):
                # The extracted http status code is in the list of potentially up status.

                # We generate the analytic file(s).
                self.analytic_file("potentially_up", self.domain_status)

        if Check(self.tested).is_ip_range():
            # The element we are currently testing is an IPv4 with range.

            # We update the source.
            self.source = "SPECIAL"

            # We update the status.
            self.domain_status = PyFunceble.STATUS["official"]["up"]

            # We update the output file.
            self.output = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS["splited"]["directory"]
                + self.domain_status
            )

        if self.source != "HTTP Code" and self.source != "SPECIAL":
            # * The source is not equal to `HTTP Code`.
            # and
            # * The source is not equal to `SPECIAL`.

            # We update the status.
            self.domain_status = PyFunceble.STATUS["official"]["down"]

            # We update the output file.
            self.output = (
                self.output_parent_dir
                + PyFunceble.OUTPUTS["splited"]["directory"]
                + self.domain_status
            )

    def invalid_status_file(self):
        """
        Logic behind the invalid status when generating the status file.
        """

        # We update the expiration date.
        self.expiration_date = "Unknown"

        if PyFunceble.HTTP_CODE["active"]:
            # The http code request/extraction is activated.

            try:
                if (
                    PyFunceble.CONFIGURATION["http_code"]
                    in PyFunceble.HTTP_CODE["list"]["up"]
                ):
                    # The extracted http code is in the list of up status.

                    # We generate the analytic file(s).
                    self.analytic_file(
                        PyFunceble.STATUS["official"]["up"], self.domain_status
                    )

                    # We update the source.
                    self.source = "HTTP Code"

                    # We update the status.
                    self.domain_status = PyFunceble.STATUS["official"]["up"]

                    # We update the output file(s).
                    self.output = (
                        self.output_parent_dir
                        + PyFunceble.OUTPUTS["splited"]["directory"]
                        + self.domain_status
                    )
                elif (
                    PyFunceble.CONFIGURATION["http_code"]
                    in PyFunceble.HTTP_CODE["list"]["potentially_up"]
                ):
                    # The extracted http code is in the list of potentially up status code.

                    # We generate the analytic file(s).
                    self.analytic_file("potentially_up", self.domain_status)
                elif (
                    PyFunceble.CONFIGURATION["http_code"]
                    in PyFunceble.HTTP_CODE["list"]["potentially_down"]
                ):
                    # The extracted http code is in the list of potentially down status code.

                    # We generate the analytic file(s).
                    self.analytic_file("potentially_down", self.domain_status)
            except KeyError:
                # In case we match a key error, we ignore it.

                pass

            if self.source != "HTTP Code":
                # The source is not equal to `HTTP Code`.

                # We update the status.
                self.domain_status = PyFunceble.STATUS["official"]["invalid"]

                # We update the output file.
                self.output = (
                    self.output_parent_dir
                    + PyFunceble.OUTPUTS["splited"]["directory"]
                    + self.domain_status
                )

    def _prints_status_file(self):  # pylint: disable=too-many-branches
        """
        Logic behind the printing (in file) when generating status file.
        """

        if PyFunceble.CONFIGURATION["file_to_test"]:
            # We are testing a file.

            if PyFunceble.CONFIGURATION["less"]:
                # We have to print less information.

                # We print the information on file.
                Prints(
                    [self.tested, self.domain_status, self.source],
                    "Less",
                    self.output,
                    True,
                ).data()
            elif PyFunceble.CONFIGURATION["split"]:
                # We have to split the information we print on file.

                if self.domain_status.lower() in PyFunceble.STATUS["list"]["up"]:
                    # The status is in the list of up status.

                    if PyFunceble.HTTP_CODE["active"]:
                        # The http code extraction is activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.tested,
                            self.expiration_date,
                            self.source,
                            PyFunceble.CONFIGURATION["http_code"],
                            PyFunceble.CURRENT_TIME,
                        ]
                    else:
                        # The http code extraction is not activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.tested,
                            self.expiration_date,
                            self.source,
                            PyFunceble.CURRENT_TIME,
                        ]

                    # We print the informations to print on file.
                    Prints(
                        data_to_print,
                        PyFunceble.STATUS["official"]["up"],
                        self.output,
                        True,
                    ).data()
                elif self.domain_status.lower() in PyFunceble.STATUS["list"]["valid"]:
                    # The status is in the list of valid status.

                    # We initiate the data to print.
                    data_to_print = [self.tested, self.source, PyFunceble.CURRENT_TIME]

                    # We print the informations to print on file.
                    Prints(
                        data_to_print,
                        PyFunceble.STATUS["official"]["valid"],
                        self.output,
                        True,
                    ).data()
                elif self.domain_status.lower() in PyFunceble.STATUS["list"]["down"]:
                    # The status is in the list of down status.

                    if PyFunceble.HTTP_CODE["active"]:
                        # The http statuc code extraction is activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.tested,
                            PyFunceble.CONFIGURATION["referer"],
                            self.domain_status,
                            self.source,
                            PyFunceble.CONFIGURATION["http_code"],
                            PyFunceble.CURRENT_TIME,
                        ]
                    else:
                        # The http status code extraction is not activated.

                        # We initate the data to print.
                        data_to_print = [
                            self.tested,
                            PyFunceble.CONFIGURATION["referer"],
                            self.domain_status,
                            self.source,
                            PyFunceble.CURRENT_TIME,
                        ]

                    # We print the information on file.
                    Prints(
                        data_to_print,
                        PyFunceble.STATUS["official"]["down"],
                        self.output,
                        True,
                    ).data()
                elif self.domain_status.lower() in PyFunceble.STATUS["list"]["invalid"]:
                    # The status is in the list of invalid status.

                    if PyFunceble.HTTP_CODE["active"]:
                        # The http status code extraction is activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.tested,
                            self.source,
                            PyFunceble.CONFIGURATION["http_code"],
                            PyFunceble.CURRENT_TIME,
                        ]
                    else:
                        # The http status code extraction is not activated.

                        # We initiate the data to print.
                        data_to_print = [
                            self.tested,
                            self.source,
                            PyFunceble.CURRENT_TIME,
                        ]

                    # We print the information to print on file.
                    Prints(
                        data_to_print,
                        PyFunceble.STATUS["official"]["invalid"],
                        self.output,
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
                to_print = [
                    self.tested,
                    self.domain_status,
                    PyFunceble.CONFIGURATION["http_code"],
                ]

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
                        self.tested,
                        self.domain_status,
                        self.expiration_date,
                        self.source,
                        PyFunceble.CONFIGURATION["http_code"],
                    ]
                else:
                    # The http status code extraction is not activated.

                    # We initiate the data to print.
                    data_to_print = [
                        self.tested,
                        self.domain_status,
                        self.expiration_date,
                        self.source,
                        PyFunceble.CURRENT_TIME,
                    ]

                # We print the information on screen.
                Prints(data_to_print, "Generic").data()

    def status_file(self):
        """
        Generate a file according to the domain status.
        """

        if not PyFunceble.CONFIGURATION["http_code"]:
            # The http code is equal to None.

            # We initiate an empty http code.
            PyFunceble.CONFIGURATION["http_code"] = "*" * 3

        if self.domain_status.lower() in PyFunceble.STATUS["list"]["up"]:
            # The status is in the list of up status.

            # We generate the status file(s).
            self.up_status_file()
        elif self.domain_status.lower() in PyFunceble.STATUS["list"]["valid"]:
            # The status is in the list of valid status.

            # We generate the status file(s).
            self.valid_status_file()
        elif self.domain_status.lower() in PyFunceble.STATUS["list"]["down"]:
            # The status is in the list of down status.

            # We generate the status file(s).
            self.down_status_file()
        elif self.domain_status.lower() in PyFunceble.STATUS["list"]["invalid"]:
            # The status is in the list of invalid status.

            # We generate the status file(s).
            self.invalid_status_file()

        # We generate the hosts file.
        Generate(self.domain_status, self.source, self.expiration_date).info_files()

        # We increase the percentage count.
        Percentage(self.domain_status).count()

        # We print on screen if needed.
        self._prints_status_screen()

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
