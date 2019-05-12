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
from PyFunceble.expiration_date import ExpirationDate
from PyFunceble.generate import Generate
from PyFunceble.helpers import Regex
from PyFunceble.http_code import HTTPCode, urllib3_exceptions
from PyFunceble.referer import Referer


class Status:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Handle the research of the domain status.

    :param str subject: The subject we are working with.

    :param str subject_type:
        The type of the subject.
        Should be one of the following.

            - :code:`domain`

            - :code:`file_domain`

    :param whois_db:
        An instance of the whois database.
    :type whois_db: :func:`PyFunceble.whois_db.WhoisDB`


    :param str filename: The name of the file we are working with.
    """

    output = {}

    def __init__(self, subject, subject_type="domain", filename=None, whois_db=None):
        self.subject = subject
        self.subject_type = subject_type.lower()
        self.filename = filename

        self.whois_db = whois_db
        self.checker = PyFunceble.Check(self.subject)

    def get(self):
        """
        Get the status while testing for an IP or domain.
        """

        if self.subject:
            self.output.update(
                {
                    "domain_syntax_validation": self.checker.is_domain(),
                    "expiration_date": None,
                    "http_status_code": "***",
                    "ipv4_range_syntax_validation": self.checker.is_ipv4_range(),
                    "ipv4_syntax_validation": self.checker.is_ipv4(),
                    "subdomain_syntax_validation": self.checker.is_subdomain(),
                    "tested": self.subject,
                    "url_syntax_validation": self.checker.is_url(),
                    "whois_server": Referer(self.subject).get(),
                }
            )

            if PyFunceble.CONFIGURATION["local"] or (
                self.output["domain_syntax_validation"]
                or self.output["ipv4_syntax_validation"]
            ):
                self.output["http_status_code"] = HTTPCode(
                    self.subject, self.subject_type
                ).get()

                if not self.output["subdomain_syntax_validation"]:
                    self.output["expiration_date"], self.output[
                        "whois_record"
                    ] = ExpirationDate(
                        self.subject,
                        self.output["whois_server"],
                        whois_db=self.whois_db,
                    ).get()

                    if isinstance(self.output["expiration_date"], str):
                        self.output["_status_source"] = self.output[
                            "status_source"
                        ] = "WHOIS"
                        self.output["_status"] = self.output[
                            "status"
                        ] = PyFunceble.STATUS["official"]["up"]

                        Generate(
                            self.subject,
                            self.subject_type,
                            self.output["status"],
                            source=self.output["status_source"],
                            expiration_date=self.output["expiration_date"],
                            http_status_code=self.output["http_status_code"],
                            whois_server=self.output["whois_server"],
                            filename=self.filename,
                            ip_validation=self.output["ipv4_syntax_validation"],
                        ).status_file()
                    else:
                        self.output["_status_source"] = "DNSLOOKUP"
                        self.handle(
                            status="inactive",
                            ip_validation_status=self.output["ipv4_syntax_validation"],
                        )
                else:
                    self.output["_status_source"] = "DNSLOOKUP"
                    self.handle(
                        status="inactive",
                        ip_validation_status=self.output["ipv4_syntax_validation"],
                    )
            else:
                self.output["_status_source"] = "IANA"
                self.output["_status"] = PyFunceble.STATUS["official"]["invalid"]

                self.handle(
                    status="invalid",
                    ip_validation_status=self.output["ipv4_syntax_validation"],
                )

            return self.output

        raise ValueError("Subject should be given.")

    def handle(self, status, ip_validation_status):
        """
        Handle the lack of WHOIS and expiration date. :smile_cat:

        :param str matched_status: The status that we have to handle.

        :param str ip_validation_status:
            The IP syntax validation.

        :return:
            The status of the domain after generating the files desired
            by the user.
        :rtype: str
        """

        # We get the dns_lookup state.
        self.output["dns_lookup"] = PyFunceble.DNSLookup(
            self.subject, dns_server=PyFunceble.CONFIGURATION["dns_server"]
        ).request()

        if status.lower() not in PyFunceble.STATUS["list"]["invalid"]:
            # The matched status is not in the list of invalid status.

            if self.output["dns_lookup"]:
                # We could execute the dns_lookup logic.

                # We set the status we got.
                self.output["_status"] = PyFunceble.STATUS["official"]["up"]
            else:
                # We could not get something.

                # We set the status we got.
                self.output["_status"] = PyFunceble.STATUS["official"]["down"]

            # We get the status and source after extra rules check.
            self.output["status"], self.output["status_source"] = ExtraRules(
                self.subject, self.subject_type, self.output["http_status_code"]
            ).handle(self.output["_status"], self.output["_status_source"])
        else:
            if self.output["dns_lookup"]:
                # We could execute the dns_lookup logic.

                # We set the status we got.
                self.output["_status"] = PyFunceble.STATUS["official"]["up"]
                # We set the status source.
                self.output["_status_source"] = "DNSLOOKUP"

            self.output["status"], self.output["status_source"] = (
                self.output["_status"],
                self.output["_status_source"],
            )

        # We generate the status file with the invalid status.
        Generate(
            self.subject,
            self.subject_type,
            self.output["status"],
            source=self.output["status_source"],
            expiration_date=self.output["expiration_date"],
            http_status_code=self.output["http_status_code"],
            whois_server=self.output["whois_server"],
            filename=self.filename,
            ip_validation=ip_validation_status,
        ).status_file()


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
            blogger_content_request = PyFunceble.requests.get(
                url_to_get, headers=self.headers
            )

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
        except (
            PyFunceble.requests.exceptions.InvalidURL,
            PyFunceble.socket.timeout,
            PyFunceble.requests.exceptions.Timeout,
            PyFunceble.requests.ConnectionError,
            urllib3_exceptions.InvalidHeader,
            UnicodeDecodeError,  # The probability that this happend in production is minimal.
        ):
            pass

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
        wordpress_com_content = PyFunceble.requests.get(
            "http://{}:80".format(self.subject), headers=self.headers
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

        :param str previous_state: The previously catched status.

        :return:
            :code:`(new status, new source)` or :code:`None` if there is any
            change to apply.
        :rtype: tuple|None
        """

        if (
            PyFunceble.HTTP_CODE["active"]
            and self.status_code in PyFunceble.HTTP_CODE["list"]["potentially_down"]
        ):
            # * The http status request is activated.
            # and
            # * The extracted http status code is in the list of
            #   potentially down list.

            # We generate the analytics files.
            Generate(self.subject, self.subject_type, previous_state).analytic_file(
                "potentially_down"
            )

            if not PyFunceble.CONFIGURATION["no_special"]:
                # We are authorized to play with the SPEICIAL rules.

                for regx in self.regexes_active_to_inactive_potentially_down:
                    # We loop through the list of available regex.

                    if Regex(
                        data=self.subject, regex=regx, return_data=False, escape=False
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
            and self.status_code in PyFunceble.HTTP_CODE["list"]["potentially_up"]
        ):
            # * The http status code request is activated.
            # and
            # * The extracted http status code is into the list of potentially up codes.

            if not PyFunceble.CONFIGURATION["no_special"]:
                # We are authorized to play with the SPEICIAL rules.

                for regx in self.regexes_active_to_inactive_potentially_up:
                    # We loop through the list of available regex.

                    if Regex(
                        data=self.subject, regex=regx, return_data=False, escape=False
                    ).match():
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
            if self.status_code in PyFunceble.HTTP_CODE["list"]["up"]:
                # The extracted http code is in the list of up codes.

                # We generate the analytics files.
                Generate(self.subject, self.subject_type, previous_state).analytic_file(
                    PyFunceble.STATUS["official"]["up"]
                )

                # And we return the new status and source
                return self.__http_status_code_up()

            if self.status_code in PyFunceble.HTTP_CODE["list"]["potentially_up"]:
                # The extracted http status code is in the list of potentially up status.

                # We generate the analytics files.
                Generate(self.subject, self.subject_type, previous_state).analytic_file(
                    "potentially_up"
                )

            if (
                previous_state.lower() in PyFunceble.STATUS["list"]["invalid"]
                and self.status_code in PyFunceble.HTTP_CODE["list"]["potentially_down"]
            ):
                # The extracted http code is in the list of potentially down status code.

                # We generate the analytics files.
                Generate(self.subject, self.subject_type, previous_state).analytic_file(
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

        if (
            not PyFunceble.CONFIGURATION["no_special"]
            and PyFunceble.Check(self.subject).is_ipv4_range()
        ):
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

    :param str subject: The subject we are working with.

    :param str subject_type: The type of the subject.

    :param str filename: The name of the file we are working with.
    """

    def __init__(self, subject, subject_type="url", filename=None):
        # We share the subject.
        self.subject = subject
        # We share the subject type.
        self.subject_type = subject_type
        # We share the filename.
        self.filename = filename

        self.checker = PyFunceble.Check(self.subject)

        # We initiate what we are going to return.
        self.output = {
            "domain_syntax_validation": None,
            "expiration_date": None,
            "ipv4_range_syntax_validation": None,
            "ipv4_syntax_validation": None,
            "subdomain_syntax_validation": None,
            "tested": self.subject,
            "url_syntax_validation": self.checker.is_url(),
            "whois_server": None,
            "http_status_code": HTTPCode(self.subject, "url").get(),
            "dns_lookup": None,
        }

    def get(self):
        """
        Get the status of the subject.
        """

        # We set the status source.
        self.output["_status_source"] = self.output["status_source"] = "URL"

        if self.output["url_syntax_validation"] or PyFunceble.CONFIGURATION["local"]:
            # * The URL syntax is valid.
            # or
            # * We are testing in/for a local or private network URL.

            # We initiate the list of active status code.
            active_list = []
            active_list.extend(PyFunceble.HTTP_CODE["list"]["potentially_up"])
            active_list.extend(PyFunceble.HTTP_CODE["list"]["up"])

            # We initiate the list of inactive status code.
            inactive_list = []
            inactive_list.extend(PyFunceble.HTTP_CODE["list"]["potentially_down"])
            inactive_list.append("*" * 3)

            if self.output["http_status_code"] in active_list:
                self.output["_status"] = self.output["status"] = PyFunceble.STATUS[
                    "official"
                ]["up"]
            elif self.output["http_status_code"] in inactive_list:
                self.output["_status"] = self.output["status"] = PyFunceble.STATUS[
                    "official"
                ]["down"]
        else:
            self.output["_status_source"] = self.output["status_source"] = "SYNTAX"
            self.output["_status"] = self.output["status"] = PyFunceble.STATUS[
                "official"
            ]["invalid"]

        self.handle()

        return self.output

    def handle(self):
        """
        Handle the backend of the given status.
        """

        # We generate the status file with the catched status.
        Generate(
            self.subject,
            self.subject_type,
            self.output["status"],
            source=self.output["status_source"],
            http_status_code=self.output["http_status_code"],
            filename=self.filename,
        ).status_file()


class SyntaxStatus:  # pragma: no cover pylint: disable=too-few-public-methods
    """
    Generate everything around the catched status when testing for Syntax.

    :param str subject: The subject we are working with.

    :param str subject_type: The type of the subject.

    :param str filename: The name of the file we are working with.
    """

    def __init__(self, subject, subject_type="domain", filename=None):
        # We share the subject
        self.subject = subject
        # We share the subject type.
        self.subject_type = subject_type
        # We share the filename.
        self.filename = filename

        self.checker = PyFunceble.Check(self.subject)

        # We initiate what we are going to return.
        self.output = {
            "domain_syntax_validation": self.checker.is_domain(),
            "expiration_date": None,
            "http_status_code": None,
            "ipv4_range_syntax_validation": self.checker.is_ipv4_range(),
            "ipv4_syntax_validation": self.checker.is_ipv4(),
            "subdomain_syntax_validation": self.checker.is_subdomain(),
            "tested": self.subject,
            "url_syntax_validation": self.checker.is_url(),
            "whois_server": None,
        }

    def get(self):
        """
        Get the status of the subject.
        """
        # We set the status source.
        self.output["_status_source"] = self.output["status_source"] = "SYNTAX"

        if self.subject_type in ["url", "file_url"]:
            # We are testing for URL syntax.

            print(self.output)
            if self.output["url_syntax_validation"]:
                self.output["_status"] = self.output["status"] = PyFunceble.STATUS[
                    "official"
                ]["valid"]
            else:
                self.output["_status"] = self.output["status"] = PyFunceble.STATUS[
                    "official"
                ]["invalid"]
        elif self.subject_type in ["domain", "file_domain"]:
            # We are testing for domain or IP.

            if (
                self.output["domain_syntax_validation"]
                or self.output["ipv4_syntax_validation"]
            ):
                self.output["_status"] = self.output["status"] = PyFunceble.STATUS[
                    "official"
                ]["valid"]
            else:
                self.output["_status"] = self.output["status"] = PyFunceble.STATUS[
                    "official"
                ]["invalid"]
        else:
            raise ValueError("Please register the subject type.")

        self.handle()

        return self.output

    def handle(self):
        """
        Handle the backend of the found status.
        """

        # We generate the status file with the catched status.
        Generate(
            self.subject,
            self.subject_type,
            self.output["status"],
            source=self.output["status_source"],
            filename=self.filename,
            ip_validation=self.output["ipv4_syntax_validation"],
        ).status_file()
