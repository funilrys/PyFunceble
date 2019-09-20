# pylint:disable=line-too-long
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Dispatch between the diferrent cores from the CLI.

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
from PyFunceble.cli_core import CLICore
from PyFunceble.execution_time import ExecutionTime
from PyFunceble.file_core import FileCore
from PyFunceble.file_multiprocess_core import FileMultiprocessCore
from PyFunceble.percentage import Percentage
from PyFunceble.simple_core import SimpleCore


class Dispatcher:  # pylint: disable=too-few-public-methods, too-many-arguments
    """
    Dispatch to the right brain side.

    .. note::
        The purpose of this is to not loose compatibility with
        the old (v1.x.x) :code:`PyFunceble.core.Core`.

    .. warning::
        This is the replacement of the old (v1.x.x) :code:`PyFunceble.core.Core`.
    """

    def __init__(
        self,
        preset,
        domain_or_ip=None,
        file_path=None,
        link_to_test=None,
        url_file_path=None,
        url_to_test=None,
    ):
        PyFunceble.Logger().debug(f"CONFIGURATION:\n{PyFunceble.CONFIGURATION}")
        self.preset = preset

        if domain_or_ip or file_path or link_to_test or url_file_path or url_to_test:

            CLICore.logs_sharing()
            ExecutionTime("start")

            if domain_or_ip:
                SimpleCore(domain_or_ip).domain()
            elif file_path:
                self.dispatch_file_test(file_path)
            elif link_to_test:
                self.dispatch_link_test(link_to_test)
            elif url_file_path:
                self.dispatch_url_file_test(url_file_path)
            elif url_to_test:
                SimpleCore(url_to_test).url()

            Percentage().log()
            ExecutionTime("stop")
            PyFunceble.CLICore.stay_safe()
        else:
            PyFunceble.CLICore.print_nothing_to_test()

    @classmethod
    def dispatch_file_test(cls, file_path):
        """
        Dispatch to the right file testing logic.

        :param str file_path: The file path to test.
        """

        PyFunceble.DirectoryStructure()

        if PyFunceble.CONFIGURATION.multiprocess:
            FileMultiprocessCore(file_path, "domain").read_and_test_file_content()
        else:
            FileCore(file_path, "domain").read_and_test_file_content()

    @classmethod
    def dispatch_link_test(cls, link_to_test):
        """
        Dispatch to the right link testing logic.

        :param str link_to_test: The link to test.
        """

        PyFunceble.DirectoryStructure()

        if PyFunceble.CONFIGURATION.multiprocess:
            FileMultiprocessCore(link_to_test, "domain").read_and_test_file_content()
        else:
            FileCore(link_to_test, "domain").read_and_test_file_content()

    def dispatch_url_file_test(self, url_file_path):
        """
        Dispatch to the right url file path testing logic.

        :param str url_file_path: The file to test.
        """

        PyFunceble.DirectoryStructure()
        self.preset.file_url()

        if PyFunceble.CONFIGURATION.multiprocess:
            FileMultiprocessCore(url_file_path, "url").read_and_test_file_content()
        else:
            FileCore(url_file_path, "url").read_and_test_file_content()
