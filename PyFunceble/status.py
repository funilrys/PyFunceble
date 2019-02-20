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

This submodule will manage the status.

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

    Copyright (c) 2017-2019 Nissar Chababy

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
from PyFunceble import requests
from PyFunceble.check import Check
from PyFunceble.expiration_date import ExpirationDate
from PyFunceble.generate import Generate
from PyFunceble.helpers import Regex
from PyFunceble.lookup import Lookup


class Status:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Hanle the research of domain status in case we don't use
    WHOIS or in case that WHOIS record is not readable nor exploitable.

    :param matched_result: The previously catched status.
    :type matched_result: str
    """

    @classmethod
    def __init__(cls):
        # We initiate an instance of the ExtraRules class.
        cls.extra_rules = cls.ExtraRules()

    @classmethod
    def get(cls):
        """
        Get the status while testing for an IP or domain.

        .. note::
            We consider that the domain or IP we are currently testing
            is into :code:`PyFunceble.INTERN["to_test"]`.
        """

        if "to_test" in PyFunceble.INTERN and PyFunceble.INTERN["to_test"]:
            expiration_date = ExpirationDate().get()

            if expiration_date is False:
                return cls.handle(status="invalid")

            if expiration_date == PyFunceble.STATUS["official"]["up"]:
                return expiration_date, "WHOIS"

            return cls.handle(status="inactive")

        raise NotImplementedError("We expect `INTERN['to_test']` to be set.")

    @classmethod
    def handle(cls, status, invalid_source="IANA"):
        """
        Handle the lack of WHOIS and expiration date. :smile_cat:

        :param matched_status: The status that we have to handle.
        :type status: str

        :param invalid_source:
            The source to set when we handle INVALID element.
        :type invalid_source: str

        :return:
            The strus of the domain after generating the files desired
            by the user.
        :rtype: str
        """

        if status.lower() not in PyFunceble.STATUS["list"]["invalid"]:
            # The matched status is not in the list of invalid status.

            # We initiate the source we are going to parse to the Generate class.
            source = "NSLOOKUP"

            if Lookup().nslookup():
                # We could execute the nslookup logic.

                # We get the status and source after extra rules check.
                status, source = cls.extra_rules.handle(
                    PyFunceble.STATUS["official"]["up"], source
                )

                # We generate the status files with the up status.
                Generate(status, source).status_file()

                # We return the up status.
                return status, source

            # We could not execute the nslookup logic.

            # We get the status and source after extra rules check.
            status, source = cls.extra_rules.handle(
                PyFunceble.STATUS["official"]["down"], source
            )

            # We generate the status file with the down status.
            Generate(status, source).status_file()

            # We return the down status.
            return status, source

        # The matched status is in the list of invalid status.

        # We get the status and source after extra rules check.
        status, source = cls.extra_rules.handle(
            PyFunceble.STATUS["official"]["invalid"], invalid_source
        )

        # We generate the status file with the invalid status.
        Generate(status, source).status_file()

        # We return the status.
        return status, source

    class ExtraRules:
        """
        Manage some extra rules.
        """

        def __init__(self):
            # We set the header that we will send when communicating with webservers.
            self.headers = {"User-Agent": PyFunceble.CONFIGURATION["user_agent"]}

            # We set a list of regex and methods to call if matched.
            self.regexes_active_to_inactive_potentially_down = {
                r"\.blogspot\.": self.__blogspot,
                r"\.canalblog\.com$": self.__special_down,
                r"\.doubleclick\.net$": self.__special_down,
                r"\.liveadvert\.com$": self.__special_down,
                r"\.skyrock\.com$": self.__special_down,
                r"\.tumblr\.com$": self.__special_down,
            }

            # We set a list of regex and methods to call if matched.
            self.regexes_active_to_inactive_potentially_up = {
                r"\.blogspot\.": self.__blogspot,
                r"\.wordpress\.com$": self.__wordpress_dot_com,
            }

        @classmethod
        def __special_down(cls):
            """
            Set what we return for the SPECIAL status de-escalation.

            :return: :code:`(new status, new source)`
            :rtype: tuple
            """

            return PyFunceble.STATUS["official"]["down"], "SPECIAL"

        @classmethod
        def __special_up(cls):
            """
            Set what we return for the SPECIAL status escalation.

            :return: :code:`(new status, new source)`
            :rtype: tuple
            """

            return PyFunceble.STATUS["official"]["up"], "SPECIAL"

        @classmethod
        def __http_status_code_up(cls):
            """
            Set what we return for the HTTP Code status escalation.

            :return: :code:`(new status, new source)`
            :rtype: tuple
            """

            return PyFunceble.STATUS["official"]["up"], "HTTP Code"

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

            if PyFunceble.INTERN["to_test_type"] == "domain":
                # The element we are testing is a domain.

                # We construct the url to get.
                url_to_get = "http://%s" % PyFunceble.INTERN["to_test"]
            elif PyFunceble.INTERN["to_test_type"] == "url":
                # The element we are testing is a URL.

                # We construct the url to get.
                url_to_get = PyFunceble.INTERN["to_test"]
            else:
                raise NotImplementedError(
                    "to_test_type not implemented: `{}`".format(
                        PyFunceble.INTERN["to_test_type"]
                    )
                )

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
                    # * The currently read regex is present into the docuement.
                    # or
                    # * Something in the document match the currently read regex.

                    # We update the status and source.
                    return self.__special_down()

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

            # We get the content of the page.
            wordpress_com_content = requests.get(
                "http://%s:80" % PyFunceble.INTERN["to_test"], headers=self.headers
            )

            if does_not_exist in wordpress_com_content.text:
                # The marker is into the page content.

                # We return the new status and source.
                return self.__special_down()

            # We return None, there is no changes.
            return None

        def __handle_potentially_inactive(self, previous_state):
            """
            Handle the potentially inactive case.

            :param previous_state: The previously catched status.
            :type previous_state: str

            :return:
                :code:`(new status, new source)` or :code:`None` if there is any
                change to apply.
            :rtype: tuple|None
            """

            if (
                PyFunceble.HTTP_CODE["active"]
                and PyFunceble.INTERN["http_code"]
                in PyFunceble.HTTP_CODE["list"]["potentially_down"]
            ):
                # * The http status request is activated.
                # and
                # * The extracted http status code is in the list of
                #   potentially down list.

                # We generate the analytics files.
                Generate(domain_status=previous_state).analytic_file("potentially_down")

                if not PyFunceble.CONFIGURATION["no_special"]:
                    # We are authorized to play with the SPEICIAL rules.

                    for regx in self.regexes_active_to_inactive_potentially_down:
                        # We loop through the list of available regex.

                        if Regex(
                            data=PyFunceble.INTERN["to_test"],
                            regex=regx,
                            return_data=False,
                            escape=False,
                        ).match():
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
                PyFunceble.HTTP_CODE["active"]
                and PyFunceble.INTERN["http_code"]
                in PyFunceble.HTTP_CODE["list"]["potentially_up"]
            ):
                # * The http status code request is activated.
                # and
                # * The extracted http status code is into the list of potentially up codes.

                if not PyFunceble.CONFIGURATION["no_special"]:
                    # We are authorized to play with the SPEICIAL rules.

                    for regx in self.regexes_active_to_inactive_potentially_up:
                        # We loop through the list of available regex.

                        if Regex(
                            data=PyFunceble.INTERN["to_test"],
                            regex=regx,
                            return_data=False,
                            escape=False,
                        ).match():
                            # The element we are currently testing match the
                            # regex we are currently reading.

                            # We get the output of the function associated
                            # with the regex.
                            output = self.regexes_active_to_inactive_potentially_up[
                                regx
                            ]()

                            if output is not None:
                                # The output is not None.

                                # We return the new source and state.
                                return output

            # We return None, there is no changes.
            return None

        def __handle_http_code(self, previous_state):
            """
            Handle the HTTP Code status escalation.

            :param previous_state: The previously catched status.
            :type previous_state: str

            :return:
                :code:`(new status, new source)` or :code:`None` if there is any
                change to apply.
            :rtype: tuple|None
            """

            try:
                if PyFunceble.INTERN["http_code"] in PyFunceble.HTTP_CODE["list"]["up"]:
                    # The extracted http code is in the list of up codes.

                    # We generate the analytics files.
                    Generate(domain_status=previous_state).analytic_file(
                        PyFunceble.STATUS["official"]["up"]
                    )

                    # And we return the new status and source
                    return self.__http_status_code_up()

                if (
                    PyFunceble.INTERN["http_code"]
                    in PyFunceble.HTTP_CODE["list"]["potentially_up"]
                ):
                    # The extracted http status code is in the list of potentially up status.

                    # We generate the analytics files.
                    Generate(domain_status=previous_state).analytic_file(
                        "potentially_up"
                    )

                if (
                    previous_state.lower() in PyFunceble.STATUS["list"]["invalid"]
                    and PyFunceble.INTERN["http_code"]
                    in PyFunceble.HTTP_CODE["list"]["potentially_down"]
                ):
                    # The extracted http code is in the list of potentially down status code.

                    # We generate the analytics files.
                    Generate(domain_status=previous_state).analytic_file(
                        "potentially_down"
                    )
            except KeyError:
                pass

            # We return None, there is no changes.
            return None

        def __handle_ipv4_range(self):
            """
            Handle the IP range status escalation.

            :return:
                :code:`(new status, new source)` or :code:`None` if there is any
                change to apply.
            :rtype: tuple|None
            """

            if not PyFunceble.CONFIGURATION["no_special"] and Check().is_ip_range():
                # * We can run/check the special rule.
                # and
                # * The element we are currently testing is an IPv4 with range.

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

            if previous_state_modified in PyFunceble.STATUS["list"]["up"]:
                # The previous state is in the list of up status.

                try:
                    # We try to get the new status and source from another handler.

                    new_status, source = self.__handle_potentially_inactive(
                        previous_state
                    )

                    if "current_test_data" in PyFunceble.INTERN:
                        # The end-user want more informations.

                        # We share the previous status and source.
                        PyFunceble.INTERN["current_test_data"][
                            "_status"
                        ], PyFunceble.INTERN["current_test_data"]["_status_source"] = (
                            previous_state,
                            previous_source,
                        )
                    return new_status, source
                except TypeError:
                    pass

                try:
                    # We try to get the new status and source from another handler.

                    new_status, source = self.__handle_potentially_up()
                    return new_status, source
                except TypeError:
                    pass

            if previous_state_modified in PyFunceble.STATUS["list"]["valid"]:
                # The previous state is in the list of valid status.

                # We return the given state and source, nothing changes.
                return previous_state, previous_source

            if previous_state_modified in PyFunceble.STATUS["list"]["down"]:
                # The previous state is in the list of down status.

                try:
                    # We try to get the new status and source from another handler.

                    new_status, source = self.__handle_ipv4_range()

                    return new_status, source
                except TypeError:
                    pass

                if PyFunceble.HTTP_CODE["active"]:
                    # The http status code request is activated.

                    try:
                        # We try to get the new status and source from another handler.

                        new_status, source = self.__handle_http_code(previous_state)

                        return new_status, source
                    except TypeError:
                        pass

            if previous_state_modified in PyFunceble.STATUS["list"]["invalid"]:
                # The previous state is in the list of invalid status.

                if PyFunceble.HTTP_CODE["active"]:
                    # The http status code request is activated.

                    try:
                        # We try to get the new status and source from another handler.

                        new_status, source = self.__handle_http_code(previous_state)

                        return new_status, source
                    except TypeError:
                        pass

            # We return the given state and source, nothing changes.
            return previous_state, previous_source


class URLStatus:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Generate everything around the catched status when testing for URL.

    :param catched_status: THe catched status.
    :type catched_status: str
    """

    def __init__(self, catched_status):
        # We get the parsed status.
        self.catched = catched_status

    def handle(self):
        """
        Handle the backend of the given status.
        """

        # We initiate the source we are going to parse to the Generate class.
        source = "URL"

        if self.catched.lower() not in PyFunceble.STATUS["list"]["invalid"]:
            # The parsed status is not in the list of invalid.

            # We generate the status file with the catched status.
            Generate(self.catched, source).status_file()
        else:
            # The parsed status is in the list of invalid.

            # We generate the status file with the parsed status.
            Generate(self.catched, "SYNTAX").status_file()

        # We return the parsed status.
        return self.catched


class SyntaxStatus:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Generate everything around the catched status when testing for Syntax.

    :param catched_status: THe catched status.
    :type catched_status: str
    """

    def __init__(self, catched_status):
        # We get the parsed status.
        self.catched = catched_status

    def handle(self):
        """
        Handle the backend of the given status.
        """

        # We generate the status file with the catched status.
        Generate(self.catched, "SYNTAX").status_file()

        # We return the parsed status.
        return self.catched
