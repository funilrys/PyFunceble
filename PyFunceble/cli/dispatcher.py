"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Dispatches between the diferrent cores (from the CLI.)

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

import PyFunceble

from .execution_time import ExecutionTime


class Dispatcher:  # pylint: disable=too-few-public-methods, too-many-arguments
    """
    Dispatches to one of the other brain.

    .. note::
        We are talking about :code:`brain` because,
        each :code:`PyFunceble.core.*` is a unique brain
        which has it's own function ;-)

        Sometimes, 2 brains depends from the other one.
        But that's great because working together is always
        great ;-)

    :param preset:
        An instance of the configuration preset.
    :type preset: :py:class:`~PyFunceble.config.preset.Preset`
    :param list domain_or_ip:
        A list of subject to test.
    :param str file_path:
        A file path or a link.

        .. note::
            If a file path is given, we read and test its content.

        .. note::
            If a link is given, we download it's content and test
            it.

        .. warning::
            If given, we consider each line to be an adblock filter,
            a host file format or a subject to test.

    :param str url_file_path:
        A file path or a link.

        .. note::
            If a file path is given, we read and test its content.

        .. note::
            If a link is given, we download it's content and test
            it.

        .. warning::
            If given, we consider each line to be a URL to test.
    :param str url_to_test:
        A list of URL to test.
    """

    def __init__(
        self,
        preset,
        domain_or_ip=None,
        file_path=None,
        url_file_path=None,
        url_to_test=None,
        generate_results_only=False,
        generate_all_results_only=False,
    ):
        self.preset = preset
        self.preset.init_all()
        PyFunceble.LOGGER.debug(f"CONFIGURATION:\n{PyFunceble.CONFIGURATION}")

        if domain_or_ip or file_path or url_file_path or url_to_test:

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
        Dispatches to the brain in charge of file testing.

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

    def dispatch_url_file_test(
        self, url_file_path, generate_results_only, generate_all_results_only
    ):
        """
        Dispatches to the brain in charge of url file testing.

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
