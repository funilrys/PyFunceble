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

from .execution_time import ExecutionTime


class Dispatcher:  # pragma: no cover pylint: disable=too-few-public-methods, too-many-arguments
    """
    Dispatch to the right brain side.

    .. note::
        The purpose of this is to not loose compatibility with
        the old (v1.x.x) :code:`PyFunceble.PyFunceble.core.Core`.

    .. warning::
        This is the replacement of the old (v1.x.x) :code:`PyFunceble.PyFunceble.core.Core`.
    """

    def __init__(
        self,
        preset,
        domain_or_ip=None,
        file_path=None,
        link_to_test=None,
        url_file_path=None,
        url_to_test=None,
        generate_results_only=False,
        generate_all_results_only=False,
    ):
        self.preset = preset
        PyFunceble.LOGGER.debug(f"CONFIGURATION:\n{PyFunceble.CONFIGURATION}")

        if domain_or_ip or file_path or link_to_test or url_file_path or url_to_test:

            PyFunceble.core.CLI.logs_sharing()
            ExecutionTime("start")

            if generate_results_only or generate_all_results_only:
                PyFunceble.INTERN["do_not_clean"] = True

            if domain_or_ip:
                PyFunceble.core.Simple(domain_or_ip).domain()
            elif file_path:
                self.dispatch_file_test(
                    file_path, generate_results_only, generate_all_results_only
                )
            elif link_to_test:
                self.dispatch_link_test(
                    link_to_test, generate_results_only, generate_all_results_only
                )
            elif url_file_path:
                self.dispatch_url_file_test(
                    url_file_path, generate_results_only, generate_all_results_only
                )
            elif url_to_test:
                PyFunceble.core.Simple(url_to_test).url()

            PyFunceble.output.Percentage().log()

            PyFunceble.core.CLI.colorify_logo()
            ExecutionTime("stop")

            PyFunceble.core.CLI.stay_safe()
        else:
            PyFunceble.core.CLI.print_nothing_to_test()

    @classmethod
    def dispatch_file_test(
        cls, file_path, generate_results_only, generate_all_results_only
    ):
        """
        Dispatch to the right file testing logic.

        :param str file_path: The file path to test.
        :param bool generate_results_only:
            Tell us to only regenerate from the data stored into the
            MariaDB/MySQL databases.
        :param bool generate_all_results_only:
            Tell us to only regenerate from the data stored into the
            MariaDB/MySQL databases.

            .. note::
                The difference with :code:`generate_results_only` is that
                it includes the retested which status didn't changed.
        """

        PyFunceble.output.Constructor()

        if PyFunceble.CONFIGURATION.multiprocess:
            if not generate_results_only and not generate_all_results_only:
                PyFunceble.core.Multiprocess(file_path, "domain").run_test()
            elif generate_all_results_only:
                PyFunceble.core.Multiprocess(file_path, "domain").generate_files(
                    include_entries_without_changes=True
                )
            else:
                PyFunceble.core.Multiprocess(file_path, "domain").generate_files()
        else:
            if not generate_results_only and not generate_all_results_only:
                PyFunceble.core.File(file_path, "domain").run_test()
            elif generate_all_results_only:
                PyFunceble.core.File(file_path, "domain").generate_files(
                    include_entries_without_changes=True
                )
            else:
                PyFunceble.core.File(file_path, "domain").generate_files()

    @classmethod
    def dispatch_link_test(
        cls, link_to_test, generate_results_only, generate_all_results_only
    ):
        """
        Dispatch to the right link testing logic.

        :param str link_to_test: The link to test.
        :param bool generate_results_only:
            Tell us to only regenerate from the data stored into the
            MariaDB/MySQL databases.
        """

        PyFunceble.output.Constructor()

        if PyFunceble.CONFIGURATION.multiprocess:
            if not generate_results_only and not generate_all_results_only:
                PyFunceble.core.Multiprocess(link_to_test, "domain").run_test()
            elif generate_all_results_only:
                PyFunceble.core.Multiprocess(link_to_test, "domain").generate_files(
                    include_entries_without_changes=True
                )
            else:
                PyFunceble.core.Multiprocess(link_to_test, "domain").generate_files()
        else:
            if not generate_results_only and not generate_all_results_only:
                PyFunceble.core.File(link_to_test, "domain").run_test()
            elif generate_all_results_only:
                PyFunceble.core.File(link_to_test, "domain").generate_files(
                    include_entries_without_changes=True
                )
            else:
                PyFunceble.core.File(link_to_test, "domain").generate_files()

    def dispatch_url_file_test(
        self, url_file_path, generate_results_only, generate_all_results_only
    ):
        """
        Dispatch to the right url file path testing logic.

        :param str url_file_path: The file to test.
        :param bool generate_results_only:
            Tell us to only regenerate from the data stored into the
            MariaDB/MySQL databases.
        """

        PyFunceble.output.Constructor()
        self.preset.file_url()

        if PyFunceble.CONFIGURATION.multiprocess:
            if not generate_results_only and not generate_all_results_only:
                PyFunceble.core.Multiprocess(url_file_path, "url").run_test()
            elif generate_all_results_only:
                PyFunceble.core.Multiprocess(url_file_path, "url").generate_files(
                    include_entries_without_changes=True
                )
            else:
                PyFunceble.core.Multiprocess(url_file_path, "url").generate_files()
        else:
            if not generate_results_only and not generate_all_results_only:
                PyFunceble.core.File(url_file_path, "url").run_test()
            elif generate_all_results_only:
                PyFunceble.core.File(url_file_path, "url").generate_files(
                    include_entries_without_changes=True
                )
            else:
                PyFunceble.core.File(url_file_path, "url").generate_files()
