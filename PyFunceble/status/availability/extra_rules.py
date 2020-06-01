"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides availability special rules interfaces.

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

import socket

from urllib3 import exceptions as urllib3_exceptions

import PyFunceble


class ExtraRules:  # pylint: disable=too-few-public-methods # pragma: no cover
    """
    Manage some extra rules.,

    :param str subject: The subject we are working with.

    :param str subject_type:
        The type of the subject we are working with.
        Should be one of the following.

            - :code:`domain`
            - :code:`url`

    :param http_status_code: The extracted status code.
    :type http_status_code: str|int
    """

    def __init__(self, subject, subject_type, http_status_code):
        # We share the subject we are working with.
        self.subject = subject
        # We share the subject type.
        self.subject_type = subject_type
        # We share the status code.
        self.status_code = http_status_code

        user_agent = PyFunceble.engine.UserAgent().get()

        if user_agent:
            # We set the header that we will send when communicating with webservers.
            self.headers = {"User-Agent": user_agent}
        else:
            self.headers = {}

        # We set a list of regex and methods to call if matched.
        self.regexes_active_to_inactive_potentially_down = {
            r"\.blogspot\.": self.__blogspot,
            r"\.canalblog\.com$": self.__special_down_404,
            r"\.github\.io$": self.__special_down_404,
            r"\.liveadvert\.com$": self.__special_down_404,
            r"\.skyrock\.com$": self.__special_down_404,
            r"\.tumblr\.com$": self.__special_down_404,
        }

        # We set a list of regex and methods to call if matched.
        self.regexes_active_to_inactive_potentially_up = {
            r"\.blogspot\.": self.__blogspot,
            r"\.wordpress\.com$": self.__wordpress_dot_com,
        }

        PyFunceble.LOGGER.debug(f"[{self.subject}] Headers:\n{self.headers}")

    @classmethod
    def __special_down(cls):
        """
        Set what we return for the SPECIAL status de-escalation.

        :return: :code:`(new status, new source)`
        :rtype: tuple
        """

        return PyFunceble.STATUS.official.down, "SPECIAL"

    def __special_down_404(self):
        """
        Set what we return for the SPECIAL status de-escalation
        when the 404 status code is caught.

        :return: :code:`(new status, new source)`
        :rtype: tuple
        """

        if self.status_code == 404:
            return PyFunceble.STATUS.official.down, "SPECIAL"
        return None

    @classmethod
    def __special_up(cls):
        """
        Set what we return for the SPECIAL status escalation.

        :return: :code:`(new status, new source)`
        :rtype: tuple
        """

        return PyFunceble.STATUS.official.up, "SPECIAL"

    @classmethod
    def __http_status_code_up(cls):
        """
        Set what we return for the HTTP Code status escalation.

        :return: :code:`(new status, new source)`
        :rtype: tuple
        """

        return PyFunceble.STATUS.official.up, "HTTP Code"

    def __blogspot(self):
        """
        Handle the blogspot SPECIAL case.

        :return:
            :code:`(new status, new source)` or :code:`None` if there is any
            change to apply.
        :rtype: tuple|None
        """

        # We iniate a list of elements in the HTML which will tell us more about
        # the status of the domain.
        regex_blogger = ["create-blog.g?", "87065", "doesn&#8217;t&nbsp;exist"]

        if self.subject_type in ["domain", "file_domain"]:
            # The element we are testing is a domain.

            # We construct the url to get.
            url_to_get = "http://%s" % self.subject
        elif self.subject_type in ["url", "file_url"]:
            # The element we are testing is a URL.

            # We construct the url to get.
            url_to_get = self.subject
        else:
            raise ValueError("Given subject type not registered.")

        try:
            # We get the HTML of the home page.
            blogger_content_request = PyFunceble.REQUESTS.get(
                url_to_get,
                headers=self.headers,
                timeout=PyFunceble.CONFIGURATION.timeout,
                verify=PyFunceble.CONFIGURATION.verify_ssl_certificate,
                allow_redirects=True,
            )

            for regx in regex_blogger:
                # We loop through the list of regex to match.

                if regx in blogger_content_request.text or PyFunceble.helpers.Regex(
                    regx
                ).match(blogger_content_request.text, return_match=False):
                    # * The currently read regex is present into the docuement.
                    # or
                    # * Something in the document match the currently read regex.

                    PyFunceble.LOGGER.info(
                        "[{self.subject}] Switching status according to blogspot rule."
                    )

                    # We update the status and source.
                    return self.__special_down()
        except (
            PyFunceble.REQUESTS.exceptions.InvalidURL,
            socket.timeout,
            PyFunceble.REQUESTS.exceptions.Timeout,
            PyFunceble.REQUESTS.exceptions.ConnectionError,
            urllib3_exceptions.InvalidHeader,
            UnicodeDecodeError,  # The probability that this happend in production is minimal.
        ):
            PyFunceble.LOGGER.exception()

        # We return None, there is no changes.
        return None

    def __wordpress_dot_com(self):
        """
        Handle the wordpress.com SPECIAL case.

        :return:
            :code:`(new status, new source)` or :code:`None` if there is any
            change to apply.
        :rtype: tuple|None
        """

        # We initiate a variable which whill have to be into the HTML
        # in order to be considered as inactive.
        does_not_exist = "doesn&#8217;t&nbsp;exist"

        try:
            # We get the content of the page.
            wordpress_com_content = PyFunceble.REQUESTS.get(
                "http://{}:80".format(self.subject),
                headers=self.headers,
                timeout=PyFunceble.CONFIGURATION.timeout,
                verify=PyFunceble.CONFIGURATION.verify_ssl_certificate,
                allow_redirects=True,
            )

            if does_not_exist in wordpress_com_content.text:
                # The marker is into the page content.

                PyFunceble.LOGGER.info(
                    "[{self.subject}] Switching status according to wordpress_dot_com rule."
                )

                # We return the new status and source.
                return self.__special_down()
        except PyFunceble.REQUESTS.exceptions.SSLError:
            pass

        # We return None, there is no changes.
        return None

    def __handle_potentially_inactive(self, previous_state):
        """
        Handle the potentially inactive case.

        :param str previous_state: The previously catched status.

        :return:
            :code:`(new status, new source)` or :code:`None` if there is any
            change to apply.
        :rtype: tuple|None
        """

        if (
            PyFunceble.HTTP_CODE.active
            and self.status_code in PyFunceble.HTTP_CODE.list.potentially_down
        ):
            # * The http status request is activated.
            # and
            # * The extracted http status code is in the list of
            #   potentially down list.

            # We generate the analytics files.
            PyFunceble.output.Generate(
                self.subject, self.subject_type, previous_state
            ).analytic_file("potentially_down")

            if not PyFunceble.CONFIGURATION.no_special:
                # We are authorized to play with the SPEICIAL rules.

                for regx in self.regexes_active_to_inactive_potentially_down:
                    # We loop through the list of available regex.

                    if PyFunceble.helpers.Regex(regx).match(
                        self.subject, return_match=False
                    ):
                        # The element we are currently testing match the
                        # regex we are currently reading.

                        # We get the output of the function associated
                        # with the regex.
                        output = self.regexes_active_to_inactive_potentially_down[
                            regx
                        ]()

                        if output is not None:
                            # The output is not None.

                            # We return the new source and state.
                            return output

        # We return None, there is no changes.
        return None

    def __handle_potentially_up(self):
        """
        Handle the potentially up  case.

        :return:
            :code:`(new status, new source)` or :code:`None` if there is any
            change to apply.
        :rtype: tuple|None
        """

        if (
            PyFunceble.HTTP_CODE.active
            and self.status_code in PyFunceble.HTTP_CODE.list.potentially_up
        ):
            # * The http status code request is activated.
            # and
            # * The extracted http status code is into the list of potentially up codes.

            if not PyFunceble.CONFIGURATION.no_special:
                # We are authorized to play with the SPEICIAL rules.

                for regx in self.regexes_active_to_inactive_potentially_up:
                    # We loop through the list of available regex.

                    if PyFunceble.helpers.Regex(regex=regx).match(
                        self.subject, return_match=False
                    ):
                        # The element we are currently testing match the
                        # regex we are currently reading.

                        # We get the output of the function associated
                        # with the regex.
                        output = self.regexes_active_to_inactive_potentially_up[regx]()

                        if output is not None:
                            # The output is not None.

                            # We return the new source and state.
                            return output

        # We return None, there is no changes.
        return None

    def __handle_http_code(self, previous_state):
        """
        Handle the HTTP Code status escalation.

        :param str previous_state: The previously catched status.

        :return:
            :code:`(new status, new source)` or :code:`None` if there is any
            change to apply.
        :rtype: tuple|None
        """

        try:

            if self.status_code in PyFunceble.HTTP_CODE.list.up:
                # The extracted http code is in the list of up codes.

                # We generate the analytics files.
                PyFunceble.output.Generate(
                    self.subject, self.subject_type, previous_state
                ).analytic_file(PyFunceble.STATUS.official.up)

                if previous_state.lower() not in PyFunceble.STATUS.list.up:
                    # And we return the new status and source

                    PyFunceble.LOGGER.info(
                        "[{self.subject}] Switching status according to status code rule."
                    )

                    return self.__http_status_code_up()

            if self.status_code in PyFunceble.HTTP_CODE.list.potentially_up:
                # The extracted http status code is in the list of potentially up status.

                # We generate the analytics files.
                PyFunceble.output.Generate(
                    self.subject, self.subject_type, previous_state
                ).analytic_file("potentially_up")

                if previous_state.lower() not in PyFunceble.STATUS.list.up:

                    PyFunceble.LOGGER.info(
                        "[{self.subject}] Switching status according to status code rule."
                    )

                    # And we return the new status and source
                    return self.__http_status_code_up()

            if (
                previous_state.lower() in PyFunceble.STATUS.list.down
                and self.status_code != PyFunceble.HTTP_CODE.not_found_default
            ):
                # We generate the analytics files.
                PyFunceble.output.Generate(
                    self.subject, self.subject_type, previous_state
                ).analytic_file("potentially_up")

                PyFunceble.LOGGER.info(
                    "[{self.subject}] Switching status according to status code rule."
                )

                # And we return the new status and source
                return self.__http_status_code_up()

            if (
                previous_state.lower() not in PyFunceble.STATUS.list.down
                or previous_state.lower() not in PyFunceble.STATUS.list.invalid
            ) and self.status_code in PyFunceble.HTTP_CODE.list.potentially_down:
                # The extracted http code is in the list of potentially down status code.

                # We generate the analytics files.
                PyFunceble.output.Generate(
                    self.subject, self.subject_type, previous_state
                ).analytic_file("potentially_down")
        except KeyError:
            PyFunceble.LOGGER.exception()

        # We return None, there is no changes.
        return None

    def __handle_reputation(self):
        """
        Handle the reputation escalation.

        :return:
            :code:`(new status, new source)` or :code:`None` if there is any
            change to apply.
        :rtype: tuple|None
        """

        if (
            not PyFunceble.CONFIGURATION.no_special
            and PyFunceble.CONFIGURATION.use_reputation_data
            and self.subject in PyFunceble.lookup.IPv4Reputation()
        ):
            PyFunceble.LOGGER.info(
                "[{self.subject}] Switching status according to reputation rule."
            )

            return self.__special_up()
        return None

    def __handle_ip_range(self):
        """
        Handle the IP range status escalation.

        :return:
            :code:`(new status, new source)` or :code:`None` if there is any
            change to apply.
        :rtype: tuple|None
        """

        if (
            not PyFunceble.CONFIGURATION.no_special
            and PyFunceble.Check(self.subject).is_ip_range()
        ):
            # * We can run/check the special rule.
            # and
            # * The element we are currently testing is an IP range.

            PyFunceble.LOGGER.info(
                "[{self.subject}] Switching status according to IP range rule."
            )

            # We return the new status and source.
            return self.__special_up()

        # We return None, there is no changes.
        return None

    def handle(
        self, previous_state, previous_source
    ):  # pylint:disable= too-many-return-statements
        """
        Globally handle the case of the currently tested domain.
        """

        # We preset the new status and the source to None.
        new_status = None
        source = None

        # We convert the given previous state to lower case.
        previous_state_modified = previous_state.lower()

        if previous_state_modified in PyFunceble.STATUS.list.up:
            # The previous state is in the list of up status.

            try:
                # We try to get the new status and source from another handler.

                new_status, source = self.__handle_potentially_inactive(previous_state)

                return new_status, source
            except TypeError:
                pass

            try:
                # We try to get the new status and source from another handler.

                new_status, source = self.__handle_potentially_up()
                return new_status, source
            except TypeError:
                pass

        if previous_state_modified in PyFunceble.STATUS.list.valid:
            # The previous state is in the list of valid status.

            # We return the given state and source, nothing changes.
            return previous_state, previous_source

        if previous_state_modified in PyFunceble.STATUS.list.down:
            # The previous state is in the list of down status.

            try:
                # We try to get the new status and source from another handler.

                new_status, source = self.__handle_ip_range()

                return new_status, source
            except TypeError:
                pass

            if PyFunceble.HTTP_CODE.active:
                # The http status code request is activated.

                try:
                    # We try to get the new status and source from another handler.

                    new_status, source = self.__handle_http_code(previous_state)

                    return new_status, source
                except TypeError:
                    pass

        if previous_state_modified in PyFunceble.STATUS.list.invalid:
            # The previous state is in the list of invalid status.

            if PyFunceble.HTTP_CODE.active:
                # The http status code request is activated.

                try:
                    # We try to get the new status and source from another handler.

                    new_status, source = self.__handle_http_code(previous_state)

                    return new_status, source
                except TypeError:
                    pass

        # We return the given state and source, nothing changes.
        return previous_state, previous_source
