"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the custom logs interface.

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

from datetime import datetime

import PyFunceble


class Logs:
    """
    Provide a clean and unique way to work with logs.
    Indeed, it's not good to have logs spread around the code :smile:

    :param str output: A path to the JSON file we are going to write.
    """

    def __init__(self, output=None):
        self.output = output
        self.current_time = str(datetime.now().timestamp())

    @classmethod
    def _get_content(cls, file):
        """
        Get and return the content of the given log file.

        :param str file: The file we have to get the content from.

        :return The content of the given file.
        :rtype: dict
        """

        if PyFunceble.helpers.File(file).exists():
            return PyFunceble.helpers.Dict().from_json_file(file)

        return {}

    @classmethod
    def _write_content(cls, content, file):
        """
        Write the content into the given file.

        :param str content: The dict to write.

        :param str file: The file to write.
        """

        if not PyFunceble.CONFIGURATION.no_files:
            if not isinstance(content, dict):
                content = {}

            PyFunceble.helpers.Dict(content).to_json_file(file)

    def whois(self, subject, record):
        """
        Logs the WHOIS record if needed.

        :param str subject: The currently tested subject.
        :param str record: The record to log.
        """

        if PyFunceble.CONFIGURATION.debug and PyFunceble.CONFIGURATION.logs:
            # The debug and the logs subsystem are activated.

            to_write = {self.current_time: {"domain": subject, "record": record}}

            if self.output:
                output = self.output
            else:
                output = PyFunceble.OUTPUT_DIRECTORY
                output += PyFunceble.OUTPUTS.parent_directory
                output += PyFunceble.OUTPUTS.logs.directories.parent
                output += PyFunceble.OUTPUTS.logs.filenames.whois

            current_content = self._get_content(output)
            current_content.update(to_write)

            PyFunceble.LOGGER.debug(f"WHOIS Record of {repr(subject)}:\n{to_write}")

            self._write_content(current_content, output)

    def expiration_date(self, subject, extracted):
        """
        Logs the extracted expiration date.

        :param str subject: The currently tested subject.
        :param str extracted: The extracted expiration date (from WHOIS record).
        """

        if PyFunceble.CONFIGURATION.logs:
            # The logs subsystem is activated.

            if PyFunceble.INTERN["referer"]:
                referer = PyFunceble.INTERN["referer"]
            else:
                referer = None

            to_write = {
                self.current_time: {
                    "domain": subject,
                    "expiration_date": extracted,
                    "whois_server": referer,
                }
            }

            if self.output:
                output = self.output
            else:
                output = PyFunceble.OUTPUT_DIRECTORY
                output += PyFunceble.OUTPUTS.parent_directory
                output += PyFunceble.OUTPUTS.logs.directories.parent
                output += PyFunceble.OUTPUTS.logs.filenames.date_format

            current_content = self._get_content(output)
            current_content.update(to_write)

            PyFunceble.LOGGER.critical(
                f"Wrong date format for {repr(subject)}:\n{to_write}"
            )

            self._write_content(current_content, output)

            if PyFunceble.CONFIGURATION.share_logs:
                # The logs sharing is activated.

                # And we share the logs with the api.
                PyFunceble.REQUESTS.post(
                    PyFunceble.LINKS.api_date_format,
                    data=to_write[self.current_time],
                    timeout=PyFunceble.CONFIGURATION.timeout,
                    verify=PyFunceble.CONFIGURATION.verify_ssl_certificate,
                    allow_redirects=False,
                )

    def referer_not_found(self, subject, extension):
        """
        Logs the case that the referer was not found.

        :param str subject: The currently tested subject.
        :param str extension: The extension of the domain we are testing.
        """

        if PyFunceble.CONFIGURATION.logs:
            # The logs subsystem is activated.

            to_write = {self.current_time: {"domain": subject, "extension": extension}}

            if self.output:
                output = self.output
            else:
                output = PyFunceble.OUTPUT_DIRECTORY
                output += PyFunceble.OUTPUTS.parent_directory
                output += PyFunceble.OUTPUTS.logs.directories.parent
                output += PyFunceble.OUTPUTS.logs.filenames.no_referer

            current_content = self._get_content(output)
            current_content.update(to_write)

            PyFunceble.LOGGER.critical(
                f"Referer not found for {repr(subject)}:\n{to_write}"
            )

            self._write_content(current_content, output)

            if PyFunceble.CONFIGURATION.share_logs:
                # The logs sharing is activated.

                # And we share the logs with the api.
                PyFunceble.REQUESTS.post(
                    PyFunceble.LINKS.api_no_referer,
                    data=to_write[self.current_time],
                    timeout=PyFunceble.CONFIGURATION.timeout,
                    verify=PyFunceble.CONFIGURATION.verify_ssl_certificate,
                    allow_redirects=False,
                )
