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

This submodule will provide the logs interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

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
from PyFunceble.helpers import Dict, File


class Logs:  # pragma: no cover
    """
    Provide a clean and unique way to work with logs.
    Indeed, it's not good to have logs spread around the code :smile:

    :param output: A path to the JSON file we are going to write.
    :type output: str
    """

    def __init__(self, output=None):
        self.output = output
        self.current_time = str(PyFunceble.time())

    @classmethod
    def _get_content(cls, file):
        """
        Get and return the content of the given log file.

        :param file: The file we have to get the content from.
        :type file: str

        :return The content of the given file.
        :rtype: dict
        """

        if PyFunceble.path.isfile(file):
            return Dict().from_json(File(file).read())

        return {}

    @classmethod
    def _write_content(cls, content, file):
        """
        Write the content into the given file.

        :param content: The dict to write.
        :type content: dict

        :param file: The file to write.
        :type file: str
        """

        if not isinstance(content, dict):
            content = {}

        Dict(content).to_json(file)

    def whois(self, record):
        """
        Logs the WHOIS record if needed.

        :param record: The record to log.
        :type record: str
        """

        if PyFunceble.CONFIGURATION["debug"] and PyFunceble.CONFIGURATION["logs"]:
            # The debug and the logs subsystem are activated.

            if PyFunceble.CONFIGURATION["referer"]:
                referer = PyFunceble.CONFIGURATION["referer"]
            else:
                referer = None

            to_write = {
                self.current_time: {
                    "domain": PyFunceble.CONFIGURATION["to_test"],
                    "record": record,
                    "referer": referer,
                }
            }

            if self.output:
                output = self.output
            else:
                output = PyFunceble.OUTPUT_DIRECTORY
                output += PyFunceble.OUTPUTS["parent_directory"]
                output += PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
                output += PyFunceble.OUTPUTS["logs"]["filenames"]["whois"]

            current_content = self._get_content(output)
            current_content.update(to_write)

            self._write_content(current_content, output)

    def expiration_date(self, extracted):
        """
        Logs the extracted expiration date.

        :param extracted: The extracted expiration date (from WHOIS record).
        :type extracted: str
        """

        if PyFunceble.CONFIGURATION["logs"]:
            # The logs subsystem is activated.

            if PyFunceble.CONFIGURATION["referer"]:
                referer = PyFunceble.CONFIGURATION["referer"]
            else:
                referer = None

            to_write = {
                self.current_time: {
                    "domain": PyFunceble.CONFIGURATION["to_test"],
                    "expiration_date": extracted,
                    "whois_server": referer,
                }
            }

            if self.output:
                output = self.output
            else:
                output = PyFunceble.OUTPUT_DIRECTORY
                output += PyFunceble.OUTPUTS["parent_directory"]
                output += PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
                output += PyFunceble.OUTPUTS["logs"]["filenames"]["date_format"]

            current_content = self._get_content(output)
            current_content.update(to_write)

            self._write_content(current_content, output)

            if PyFunceble.CONFIGURATION["share_logs"]:
                # The logs sharing is activated.

                # And we share the logs with the api.
                PyFunceble.requests.post(
                    PyFunceble.LINKS["api_date_format"],
                    data=to_write[self.current_time],
                )

    def referer_not_found(self, extension):
        """
        Logs the case that the referer was not found.

        :param extension: The extension of the domain we are testing.
        :type extension: str
        """

        if PyFunceble.CONFIGURATION["logs"]:
            # The logs subsystem is activated.

            to_write = {
                self.current_time: {
                    "domain": PyFunceble.CONFIGURATION["to_test"],
                    "extension": extension,
                }
            }

            if self.output:
                output = self.output
            else:
                output = PyFunceble.OUTPUT_DIRECTORY
                output += PyFunceble.OUTPUTS["parent_directory"]
                output += PyFunceble.OUTPUTS["logs"]["directories"]["parent"]
                output += PyFunceble.OUTPUTS["logs"]["filenames"]["no_referer"]

            current_content = self._get_content(output)
            current_content.update(to_write)

            self._write_content(current_content, output)

            if PyFunceble.CONFIGURATION["share_logs"]:
                # The logs sharing is activated.

                # And we share the logs with the api.
                PyFunceble.requests.post(
                    PyFunceble.LINKS["api_no_referer"], data=to_write[self.current_time]
                )
