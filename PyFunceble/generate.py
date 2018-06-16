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
# pylint: disable=bad-continuation
import PyFunceble
from PyFunceble import directory_separator, requests
from PyFunceble.helpers import Regex
from PyFunceble.percentage import Percentage
from PyFunceble.prints import Prints


class Generate(object):  # pragma: no cover
    """
    Generate different sort of files.

    Arguments:
        - domain_status: str
            The domain status.
        - source: str
            The source of the given status.
        - expiration_date: str
            The expiration date of the domain if catched.
    """

    def __init__(self, domain_status, source=None, expiration_date=None):
        self.domain_status = domain_status
        self.source = source
        self.expiration_date = expiration_date

        self.output_parent_dir = PyFunceble.CURRENT_DIRECTORY + PyFunceble.OUTPUTS[
            "parent_directory"
        ]

        self.refer_status = ""
        self.output = ""

        if "domain" in PyFunceble.CONFIGURATION and PyFunceble.CONFIGURATION["domain"]:
            self.tested = PyFunceble.CONFIGURATION["domain"]
        elif "URL" in PyFunceble.CONFIGURATION and PyFunceble.CONFIGURATION["URL"]:
            self.tested = PyFunceble.CONFIGURATION["URL"]

    def hosts_file(self):
        """
        Generate a hosts file.
        """

        if PyFunceble.CONFIGURATION["generate_hosts"] or PyFunceble.CONFIGURATION[
            "plain_list_domain"
        ]:
            splited_destination = ""
            http_list = []
            http_list.extend(PyFunceble.STATUS["list"]["potentially_up"])
            http_list.extend(PyFunceble.STATUS["list"]["potentially_down"])
            http_list.extend(PyFunceble.STATUS["list"]["http_active"])

            output_hosts = self.output_parent_dir + PyFunceble.OUTPUTS["hosts"][
                "directory"
            ] + "%s" + directory_separator + PyFunceble.OUTPUTS[
                "hosts"
            ][
                "filename"
            ]

            output_domains = self.output_parent_dir + PyFunceble.OUTPUTS["domains"][
                "directory"
            ] + "%s" + directory_separator + PyFunceble.OUTPUTS[
                "domains"
            ][
                "filename"
            ]

            if self.domain_status.lower() in PyFunceble.STATUS["list"]["up"]:
                hosts_destination = output_hosts % PyFunceble.STATUS["official"]["up"]
                plain_destination = output_domains % PyFunceble.STATUS["official"]["up"]
            elif self.domain_status.lower() in PyFunceble.STATUS["list"]["down"]:
                hosts_destination = output_hosts % PyFunceble.STATUS["official"]["down"]
                plain_destination = output_domains % PyFunceble.STATUS["official"][
                    "down"
                ]
            elif self.domain_status.lower() in PyFunceble.STATUS["list"]["invalid"]:
                hosts_destination = output_hosts % PyFunceble.STATUS["official"][
                    "invalid"
                ]
                plain_destination = output_domains % PyFunceble.STATUS["official"][
                    "invalid"
                ]
            elif self.domain_status.lower() in http_list:

                output_dir = self.output_parent_dir + PyFunceble.OUTPUTS[
                    "http_analytic"
                ][
                    "directories"
                ][
                    "parent"
                ]
                if self.domain_status.lower() in PyFunceble.STATUS["list"][
                    "potentially_up"
                ]:
                    output_dir += PyFunceble.OUTPUTS["http_analytic"]["directories"][
                        "potentially_up"
                    ]
                elif self.domain_status.lower() in PyFunceble.STATUS["list"][
                    "potentially_down"
                ]:
                    output_dir += PyFunceble.OUTPUTS["http_analytic"]["directories"][
                        "potentially_down"
                    ]
                else:
                    output_dir += PyFunceble.OUTPUTS["http_analytic"]["directories"][
                        "up"
                    ]

                if not output_dir.endswith(directory_separator):
                    output_dir += directory_separator

                hosts_destination = output_dir + PyFunceble.OUTPUTS["hosts"]["filename"]
                plain_destination = output_dir + PyFunceble.OUTPUTS["domains"][
                    "filename"
                ]
                splited_destination = output_dir + str(
                    PyFunceble.CONFIGURATION["http_code"]
                )

            if PyFunceble.CONFIGURATION["generate_hosts"]:
                Prints(
                    [PyFunceble.CONFIGURATION["custom_ip"], self.tested],
                    "FullHosts",
                    hosts_destination,
                ).data()

            if PyFunceble.CONFIGURATION["plain_list_domain"]:
                Prints([self.tested], "PlainDomain", plain_destination).data()

            if PyFunceble.CONFIGURATION["split"] and splited_destination:
                Prints([self.tested], "PlainDomain", splited_destination).data()

    def unified_file(self):
        """
        Generate unified file. Understand by that that we use an unified table
        instead of a separate table for each status which could result into a
        misunderstanding.
        """

        if PyFunceble.CONFIGURATION["unified"]:
            output = self.output_parent_dir + PyFunceble.OUTPUTS["default_files"][
                "results"
            ]
            if PyFunceble.CONFIGURATION["less"]:
                if PyFunceble.HTTP_CODE["active"]:
                    to_print = [
                        self.tested,
                        self.domain_status,
                        PyFunceble.CONFIGURATION["http_code"],
                    ]
                else:
                    to_print = [self.tested, self.domain_status, self.source]

                Prints(to_print, "Less", output, True).data()
            else:
                to_print = [
                    self.tested,
                    self.domain_status,
                    self.expiration_date,
                    self.source,
                    PyFunceble.CONFIGURATION["http_code"],
                    PyFunceble.CURRENT_TIME,
                ]

                Prints(to_print, "Generic_File", output, True).data()

    def _analytic_file(self, new_status, old_status):
        """
        Generate HTTP_Analytic/* files.

        Arguments:
            - new_status: str
                The new status of the domain.
            - old_status: str
                The old status of the domain.
        """

        output = self.output_parent_dir + PyFunceble.OUTPUTS["http_analytic"][
            "directories"
        ][
            "parent"
        ] + "%s%s"
        if new_status.lower() in PyFunceble.STATUS["list"]["up"]:
            output = output % (
                PyFunceble.OUTPUTS["http_analytic"]["directories"]["up"],
                PyFunceble.OUTPUTS["http_analytic"]["filenames"]["up"],
            )
            Generate("HTTP_Active").hosts_file()
        elif new_status.lower() in PyFunceble.STATUS["list"]["potentially_up"]:
            output = output % (
                PyFunceble.OUTPUTS["http_analytic"]["directories"]["potentially_up"],
                PyFunceble.OUTPUTS["http_analytic"]["filenames"]["potentially_up"],
            )
            Generate("potentially_up").hosts_file()
        else:
            output = output % (
                PyFunceble.OUTPUTS["http_analytic"]["directories"]["potentially_down"],
                PyFunceble.OUTPUTS["http_analytic"]["filenames"]["potentially_down"],
            )
            Generate("potentially_down").hosts_file()

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

        regex_blogspot = ".blogspot."
        regex_blogger = ["create-blog.g?", "87065", "doesn&#8217;t&nbsp;exist"]

        if self.tested == PyFunceble.CONFIGURATION["domain"]:
            url_to_get = "http://%s" % self.tested
        else:
            url_to_get = self.tested

        if Regex(self.tested, regex_blogspot, return_data=False, escape=True).match():
            blogger_content_request = requests.get(url_to_get)

            for regx in regex_blogger:
                if regx in blogger_content_request.text or Regex(
                    blogger_content_request.text, regx, return_data=False, escape=False
                ).match():
                    self.source = "SPECIAL"
                    self.domain_status = PyFunceble.STATUS["official"]["down"]
                    self.output = self.output_parent_dir + PyFunceble.OUTPUTS[
                        "splited"
                    ][
                        "directory"
                    ] + self.domain_status
                    break

    def _special_wordpress_com(self):
        """
        Handle the wordpress.com special case.
        """

        wordpress_com = ".wordpress.com"
        does_not_exist = "doesn&#8217;t&nbsp;exist"

        if self.tested.endswith(wordpress_com):
            wordpress_com_content = requests.get("http://%s:80" % self.tested)

            if does_not_exist in wordpress_com_content.text:
                self.source = "SPECIAL"
                self.domain_status = PyFunceble.STATUS["official"]["down"]
                self.output = self.output_parent_dir + PyFunceble.OUTPUTS["splited"][
                    "directory"
                ] + self.domain_status

    def up_status_file(self):
        """
        Logic behind the up status when generating the status file.
        """

        if not self.expiration_date:
            self.expiration_date = "Unknown"

        if PyFunceble.HTTP_CODE["active"] and PyFunceble.CONFIGURATION[
            "http_code"
        ] in PyFunceble.HTTP_CODE[
            "list"
        ][
            "potentially_down"
        ]:
            self._analytic_file("potentially_down", self.domain_status)

            regex_to_match = [
                ".canalblog.com",
                ".doubleclick.net",
                ".liveadvert.com",
                ".skyrock.com",
                ".tumblr.com",
            ]

            for regx in regex_to_match:
                if Regex(self.tested, regx, return_data=False, escape=True).match():
                    self.source = "SPECIAL"
                    self.domain_status = PyFunceble.STATUS["official"]["down"]
                    self.output = self.output_parent_dir + PyFunceble.OUTPUTS[
                        "splited"
                    ][
                        "directory"
                    ] + self.domain_status

            self._special_blogspot()
        elif PyFunceble.HTTP_CODE["active"] and PyFunceble.CONFIGURATION[
            "http_code"
        ] in PyFunceble.HTTP_CODE[
            "list"
        ][
            "potentially_up"
        ]:
            self._special_blogspot()
            self._special_wordpress_com()

        if self.source != "SPECIAL":
            self.domain_status = PyFunceble.STATUS["official"]["up"]
            self.output = self.output_parent_dir + PyFunceble.OUTPUTS["splited"][
                "directory"
            ] + self.domain_status

    def down_status_file(self):
        """
        Logic behind the down status when generating the status file.
        """

        self.refer_status = "Not Found"
        self.expiration_date = "Unknown"

        if PyFunceble.HTTP_CODE["active"]:
            if PyFunceble.CONFIGURATION["http_code"] in PyFunceble.HTTP_CODE["list"][
                "up"
            ]:
                self._analytic_file(
                    PyFunceble.STATUS["official"]["up"], self.domain_status
                )
                self.source = "HTTP Code"
                self.domain_status = PyFunceble.STATUS["official"]["up"]
                self.output = self.output_parent_dir + PyFunceble.OUTPUTS["splited"][
                    "directory"
                ] + self.domain_status
            elif PyFunceble.CONFIGURATION["http_code"] in PyFunceble.HTTP_CODE["list"][
                "potentially_up"
            ]:
                self._analytic_file("potentially_up", self.domain_status)

        if Regex(
            self.tested,
            r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,})$",  # pylint: disable=line-too-long
            return_data=False,
        ).match():
            self.source = "SPECIAL"
            self.domain_status = PyFunceble.STATUS["official"]["up"]
            self.output = self.output_parent_dir + PyFunceble.OUTPUTS["splited"][
                "directory"
            ] + self.domain_status

        if self.source != "HTTP Code" and self.source != "SPECIAL":
            self.domain_status = PyFunceble.STATUS["official"]["down"]
            self.output = self.output_parent_dir + PyFunceble.OUTPUTS["splited"][
                "directory"
            ] + self.domain_status

    def invalid_status_file(self):
        """
        Logic behind the invalid status when generating the status file.
        """

        self.expiration_date = "Unknown"

        if PyFunceble.HTTP_CODE["active"]:
            try:
                if PyFunceble.CONFIGURATION["http_code"] in PyFunceble.HTTP_CODE[
                    "list"
                ][
                    "up"
                ]:
                    self._analytic_file(
                        PyFunceble.STATUS["official"]["up"], self.domain_status
                    )
                    self.source = "HTTP Code"
                    self.domain_status = PyFunceble.STATUS["official"]["up"]
                    self.output = self.output_parent_dir + PyFunceble.OUTPUTS[
                        "splited"
                    ][
                        "directory"
                    ] + self.domain_status
                elif PyFunceble.CONFIGURATION["http_code"] in PyFunceble.HTTP_CODE[
                    "list"
                ][
                    "potentially_up"
                ]:
                    self._analytic_file("potentially_up", self.domain_status)
                elif PyFunceble.CONFIGURATION["http_code"] in PyFunceble.HTTP_CODE[
                    "list"
                ][
                    "potentially_down"
                ]:
                    self._analytic_file("potentially_down", self.domain_status)
            except KeyError:
                pass

            if self.source != "HTTP Code":
                self.domain_status = PyFunceble.STATUS["official"]["invalid"]
                self.output = self.output_parent_dir + PyFunceble.OUTPUTS["splited"][
                    "directory"
                ] + self.domain_status

    def _prints_status_file(self):
        """
        Logic behind the printing when generating status file.
        """

        if PyFunceble.CONFIGURATION["less"]:
            Prints(
                [self.tested, self.domain_status, self.source],
                "Less",
                self.output,
                True,
            ).data()
        elif PyFunceble.CONFIGURATION["split"]:
            if self.domain_status.lower() in PyFunceble.STATUS["list"]["up"]:
                if PyFunceble.HTTP_CODE["active"]:
                    data_to_print = [
                        self.tested,
                        self.expiration_date,
                        self.source,
                        PyFunceble.CONFIGURATION["http_code"],
                        PyFunceble.CURRENT_TIME,
                    ]
                else:
                    data_to_print = [
                        self.tested,
                        self.expiration_date,
                        self.source,
                        PyFunceble.CURRENT_TIME,
                    ]

                Prints(
                    data_to_print,
                    PyFunceble.STATUS["official"]["up"],
                    self.output,
                    True,
                ).data()
            elif self.domain_status.lower() in PyFunceble.STATUS["list"]["down"]:
                if PyFunceble.HTTP_CODE["active"]:
                    data_to_print = [
                        self.tested,
                        PyFunceble.CONFIGURATION["referer"],
                        self.domain_status,
                        self.source,
                        PyFunceble.CONFIGURATION["http_code"],
                        PyFunceble.CURRENT_TIME,
                    ]
                else:
                    data_to_print = [
                        self.tested,
                        PyFunceble.CONFIGURATION["referer"],
                        self.domain_status,
                        self.source,
                        PyFunceble.CURRENT_TIME,
                    ]

                Prints(
                    data_to_print,
                    PyFunceble.STATUS["official"]["down"],
                    self.output,
                    True,
                ).data()
            elif self.domain_status.lower() in PyFunceble.STATUS["list"]["invalid"]:
                if PyFunceble.HTTP_CODE["active"]:
                    data_to_print = [
                        self.tested,
                        self.source,
                        PyFunceble.CONFIGURATION["http_code"],
                        PyFunceble.CURRENT_TIME,
                    ]
                else:
                    data_to_print = [self.tested, self.source, PyFunceble.CURRENT_TIME]

                Prints(
                    data_to_print,
                    PyFunceble.STATUS["official"]["invalid"],
                    self.output,
                    True,
                ).data()

    def status_file(self):
        """
        Generate a file according to the domain status.
        """

        try:
            PyFunceble.CONFIGURATION["http_code"]
        except KeyError:
            PyFunceble.CONFIGURATION["http_code"] = "*" * 3

        if not PyFunceble.CONFIGURATION["http_code"]:
            PyFunceble.CONFIGURATION["http_code"] = "*" * 3

        if self.domain_status.lower() in PyFunceble.STATUS["list"]["up"]:
            self.up_status_file()
        elif self.domain_status.lower() in PyFunceble.STATUS["list"]["down"]:
            self.down_status_file()
        elif self.domain_status.lower() in PyFunceble.STATUS["list"]["invalid"]:
            self.invalid_status_file()

        Generate(self.domain_status, self.source, self.expiration_date).hosts_file()
        Percentage(self.domain_status).count()

        if not PyFunceble.CONFIGURATION["quiet"]:
            if PyFunceble.CONFIGURATION["less"]:
                Prints(
                    [
                        self.tested,
                        self.domain_status,
                        PyFunceble.CONFIGURATION["http_code"],
                    ],
                    "Less",
                ).data()
            else:
                if PyFunceble.HTTP_CODE["active"]:
                    data_to_print = [
                        self.tested,
                        self.domain_status,
                        self.expiration_date,
                        self.source,
                        PyFunceble.CONFIGURATION["http_code"],
                    ]
                else:
                    data_to_print = [
                        self.tested,
                        self.domain_status,
                        self.expiration_date,
                        self.source,
                        PyFunceble.CURRENT_TIME,
                    ]

                Prints(data_to_print, "Generic").data()

        if not PyFunceble.CONFIGURATION["no_files"] and PyFunceble.CONFIGURATION[
            "split"
        ]:
            self._prints_status_file()
        else:
            self.unified_file()
