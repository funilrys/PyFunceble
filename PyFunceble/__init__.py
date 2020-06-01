# pylint:disable=invalid-name, cyclic-import
"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

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

import warnings
from datetime import datetime
from os import path
from os import sep as directory_separator
from time import sleep

from colorama import Fore
from dotenv import load_dotenv

import PyFunceble.abstracts as abstracts
import PyFunceble.config as cconfig
import PyFunceble.converter as converter
import PyFunceble.core as core
import PyFunceble.database as database
import PyFunceble.downloader as downloader
import PyFunceble.engine as engine
import PyFunceble.exceptions as exceptions
import PyFunceble.extractor as extractor
import PyFunceble.helpers as helpers
import PyFunceble.lookup as lookup
import PyFunceble.output as output
import PyFunceble.status as status
from PyFunceble.check import Check

# We set our project name.
NAME = abstracts.Package.NAME
# We set out project version.
VERSION = abstracts.Package.VERSION


if helpers.EnvironmentVariable("PYFUNCEBLE_CONFIG_DIR").exists():  # pragma: no cover
    # We handle the case that the `PYFUNCEBLE_CONFIG_DIR` environnement variable is set.
    CONFIG_DIRECTORY = helpers.EnvironmentVariable("PYFUNCEBLE_CONFIG_DIR").get_value()
elif helpers.EnvironmentVariable("PYFUNCEBLE_OUTPUT_DIR").exists():  # pragma: no cover
    # We hande the retro compatibility.
    CONFIG_DIRECTORY = helpers.EnvironmentVariable("PYFUNCEBLE_OUTPUT_DIR").get_value()
elif abstracts.Version.is_local_cloned():  # pragma: no cover
    # We handle the case that we are in a cloned.
    CONFIG_DIRECTORY = helpers.Directory.get_current(with_end_sep=True)
elif helpers.EnvironmentVariable("TRAVIS_BUILD_DIR").exists():  # pragma: no cover
    # We handle the case that we are under Travis CI.
    CONFIG_DIRECTORY = helpers.Directory.get_current(with_end_sep=True)
elif (
    helpers.EnvironmentVariable("CI_PROJECT_DIR").exists()
    and helpers.EnvironmentVariable("GITLAB_CI").exists()
):  # pragma: no cover
    # We handle the case that we are under GitLab CI/CD.
    CONFIG_DIRECTORY = helpers.Directory.get_current(with_end_sep=True)
else:  # pragma: no cover
    # We handle all other case and distributions specific cases.

    if abstracts.Platform.is_unix():
        # We are under a Linux distribution.

        # We set the default configuration location path.
        config_dir_path = (
            path.expanduser("~" + directory_separator + ".config") + directory_separator
        )

        if helpers.Directory(config_dir_path).exists():
            # Everything went right:
            #   * `~/.config` exists.
            # We set our configuration location path as the directory we are working with.
            CONFIG_DIRECTORY = config_dir_path
        elif helpers.Directory(path.expanduser("~")).exists():
            # Something went wrong:
            #   * `~/.config` does not exists.
            #   * `~` exists.
            # We set `~/` as the directory we are working with.
            #
            # Note: The `.` at the end is because we want to hide the directory we are
            # going to create.
            CONFIG_DIRECTORY = (
                path.expanduser("~") + directory_separator + "."
            )  # pylint: disable=line-too-long
        else:
            # Everything went wrong:
            #   * `~/.config` does not exists.
            #   * `~` soes not exists.
            # We set the current directory as the directory we are working with.
            CONFIG_DIRECTORY = helpers.Directory.get_current(with_end_sep=True)
    elif abstracts.Platform.is_windows():
        # We are under Windows or CygWin.

        if helpers.EnvironmentVariable("APPDATA").exists():
            # Everything went right:
            #   * `APPDATA` is into the environnement variables.
            # We set it as the directory we are working with.
            CONFIG_DIRECTORY = helpers.EnvironmentVariable("APPDATA").get_value()
        else:
            # Everything went wrong:
            #   * `APPDATA` is not into the environnement variables.
            # We set the current directory as the directory we are working with.
            CONFIG_DIRECTORY = helpers.Directory.get_current(with_end_sep=True)

    if not CONFIG_DIRECTORY.endswith(directory_separator):
        # If the directory we are working with does not ends with the directory
        # separator, we append it to the end.
        CONFIG_DIRECTORY += directory_separator

    # We append the name of the project to the directory we are working with.
    CONFIG_DIRECTORY += NAME + directory_separator

    if not helpers.Directory(CONFIG_DIRECTORY).exists():
        # If the directory does not exist we create it.
        helpers.Directory(CONFIG_DIRECTORY).create()

if not CONFIG_DIRECTORY.endswith(directory_separator):  # pragma: no cover
    # Again for safety, if the directory we are working with does not ends with
    # the directory separator, we append it to the end.
    CONFIG_DIRECTORY += directory_separator

# We set the location of the `output` directory which should always be in the current
# directory.
OUTPUT_DIRECTORY = helpers.Directory.get_current(with_end_sep=True)

# We initiate the location where we are going to save our whole configuration content.
CONFIGURATION = None
# We initiate the location where we are going to get all statuses.
STATUS = None
# We initiate the location where we are going to get all outputs.
OUTPUTS = None
# We initiate the location where we are going to get the map of the classification
# of each status codes for the analytic part.
HTTP_CODE = None
# We initiate the location where we are going to get all links.
LINKS = None
# We initiate a location which will have all internal data.
INTERN = None
# We initiate the location of the Logger.
LOGGER = None
# We initiate the location of the HTTP requests.
REQUESTS = None
# We initiate the DNS resolver.
DNSLOOKUP = None
# We initiate the PSL lookup.
PSLOOOKUP = None
# We initiate the IANA lookup.
IANALOOKUP = None
# We initate the loader.
LOADER = None

load_dotenv()
load_dotenv(CONFIG_DIRECTORY + ".env")
load_dotenv(CONFIG_DIRECTORY + abstracts.Infrastructure.ENV_FILENAME)

# We initiate the CLI logo of PyFunceble.
ASCII_PYFUNCEBLE = """
██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝
"""


def test(subject, complete=False, config=None):  # pragma: no cover
    """
    Test the availability of the given subject (domain or IP).

    :param subject: The subject (IP or domain) to test.
    :type subject: str|list

    :param bool complete:
        Activate the return of a dict with some significant data from
        the test.

    :param dict config:
        A dict with the configuration index (from .PyFunceble.yaml) to update.

    :return: The status or the informations of the domain.
    :rtype: str|dict

    .. note::
        If :code:`config` is given, the given :code:`dict` overwrite
        the last value of the given indexes in the configuration.

        It's actually something like following:

        ::

            pyfunceble.configuration.update(config_given_by_user)

    .. note::
        If :code:`complete` is set to :code:`True`, we return the following indexes.

        ::

            {
                "_status_source": None,
                "_status": None,
                "dns_lookup": [],
                "domain_syntax_validation": None,
                "expiration_date": None,
                "http_status_code": None,
                "ipv4_range_syntax_validation": None,
                "ipv4_syntax_validation": None,
                "ipv6_range_syntax_validation": None,
                "ipv6_syntax_validation": None,
                "status": None,
                "status_source": None,
                "subdomain_syntax_validation": None,
                "tested": None,
                "url_syntax_validation": None,
                "whois_record": None,
                "whois_server": None,
            }
    """

    if subject:
        # The subject is not empty nor None.

        # We return the status of the given subject.
        return core.API(
            subject, complete=complete, configuration=config
        ).domain_and_ip()

    # We return None, there is nothing to test.
    return None


def url_test(subject, complete=False, config=None):  # pragma: no covere
    """
    Test the availability of the given subject (URL).

    :param subject: The subject (URL) to test.
    :type subject: str|list

    :param bool complete:
        Activate the return of a dict with some significant data from
        the test.

    :param dict config:
        A dict with the configuration index (from .PyFunceble.yaml) to update.

    :return: The status or the informations of the URL.
    :rtype: str|dict

    .. note::
        If :code:`config` is given, the given :code:`dict` overwrite
        the last value of the given indexes in the configuration.

        It's actually something like following:

        ::

            pyfunceble.configuration.update(config_given_by_user)

    .. note::
        If :code:`complete` is set to :code:`True`, we return the following indexes.

        ::

            {
                "_status_source": None,
                "_status": None,
                "dns_lookup": [],
                "domain_syntax_validation": None,
                "expiration_date": None,
                "http_status_code": None,
                "ipv4_range_syntax_validation": None,
                "ipv4_syntax_validation": None,
                "ipv6_range_syntax_validation": None,
                "ipv6_syntax_validation": None,
                "status": None,
                "status_source": None,
                "subdomain_syntax_validation": None,
                "tested": None,
                "url_syntax_validation": None,
                "whois_record": None,
                "whois_server": None,
            }
    """

    if subject:
        # The given URL is not empty nor None.

        # We retunr the status of the the url.
        return core.API(subject, complete=complete, configuration=config).url()

    # We return None, there is nothing to test.
    return None


def dns_lookup(
    subject, dns_server=None, complete=False, lifetime=3
):  # pragma: no cover
    """
    Make a DNS lookup of the given subject.

    :param str subject: The subject we are working with.
    :param dns_server: A (or list of) DNS server to use while resolving.
    :type dns_server: str|int
    :param bool complete:
        Tell us to look for everything instead of :code:`NS` only.
    :param int lifetime: The query lifetime.

    :return:
        A dict with following index if the given subject is not registered into the
        given DNS server. (More likely local subjects).

            ::

                {
                    "hostname": "",
                    "aliases": [],
                    "ips": []
                }

        A dict with following index for everything else (and if found).

            ::

                {
                    "A": [],
                    "AAAA": [],
                    "CNAME": [],
                    "MX": [],
                    "NS": [],
                    "TXT": [],
                    "PTR": []
                }

    :rtype: dict
    """

    if subject:
        # The subject is not empty nor None.

        # We return the lookup.
        return lookup.Dns(dns_server=dns_server, lifetime=lifetime).request(
            subject, complete=complete
        )

    # We return None, there is nothing to work with.
    return None


def whois(subject, server=None, timeout=3):  # pragma: no cover
    """
    Request the WHOIS record of the given subject.

    :param str subject: The subject we are working with.
    :param str server:
        The WHOIS server to communicate with.

        .. note::
            If :code:`None` is given, we look for the best one.
    :param int timeout: The timeout to apply to the request.

    :return: None or the WHOIS record.
    :rtype: None|str
    """

    if subject:
        # The subject is not empty nor None.

        # We return the whois record.
        return lookup.Whois(subject, server=server, timeout=timeout).request()

    # We return None, there is nothing to work with.
    return None


def syntax_check(domain):  # pragma: no cover
    """
    Check the syntax of the given domain.

    :param domain: The domain to check the syntax from.
    :type domain: str|list

    :return: The syntax validity.
    :rtype: bool|dict

    .. warning::
        This method will be deprecated one day in the future.

        Please report to :func:`~PyFunceble.is_domain`.
    """

    warnings.warn(
        "`PyFunceble.syntax_check` will be deprecated in future version. "
        "Please use `PyFunceble.is_domain` instead.",
        DeprecationWarning,
    )

    return is_domain(domain)


def is_domain(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid domain.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validiry of the given subject.
        return core.API(subject).domain_syntax()

    # We return None, there is nothing to check.
    return None


def is_subdomain(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid subdomain.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We retun the validity of the given subject.
        return core.API(subject).subdomain_syntax()

    # We return None, there is nothing to check.
    return None


def ipv4_syntax_check(ip):  # pragma: no cover
    """
    Check the syntax of the given IPv4.

    :param ip: The IPv4 to check the syntax for.
    :type ip: str|list

    :return: The syntax validity.
    :rtype: bool|dict

    .. warning::
        This method will be deprecated one day in the future.

        Please report to :func:`~PyFunceble.is_ipv4`.
    """

    warnings.warn(
        "`PyFunceble.ipv4_syntax_check` will be deprecated in future version. "
        "Please use `PyFunceble.is_ipv4` instead.",
        DeprecationWarning,
    )

    return is_ipv4(ip)


def is_ip(subject):  # pragma: no cover
    """
    Checks if the given subject is a syntactivally valid IPv4 or IPv6.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validity of the given subject.
        return core.API(subject).ip_syntax()

    # We return None, there is nothing to check.
    return None


def is_ipv4(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid IPv4.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validity of the given subject.
        return core.API(subject).ipv4_syntax()

    # We return None, there is nothing to check.
    return None


def is_ipv6(subject):  # pragma: no cover
    """
    Checks if the given subject is syntactivally valid IPv6.

    :param subject: The subject to check the syntax from.
    :type subject: str, list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty not None.

        # We return the validity of the given subject.
        return core.API(subject).ipv6_syntax()

    # We return None, there is nothing to check.
    return None


def is_ip_range(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid IPv4 or IPv6 range.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The IPv4 range state.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validity of the given subject.
        return core.API(subject).ip_range_syntax()

    # We return None, there is nothing to check.
    return None


def is_ipv4_range(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid IPv4 range.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The IPv4 range state.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validity of the given subject.
        return core.API(subject).ipv4_range_syntax()

    # We return None, there is nothing to check.
    return None


def url_syntax_check(url):  # pragma: no cover
    """
    Check the syntax of the given URL.

    :param url: The URL to check the syntax for.
    :type url: str|list

    :return: The syntax validity.
    :rtype: bool|dict

    .. warning::
        This method will be deprecated one day in the future.

        Please report to :func:`~PyFunceble.is_url`.
    """

    warnings.warn(
        "`PyFunceble.url_syntax_check` will be deprecated in future version. "
        "Please use `PyFunceble.is_url` instead.",
        DeprecationWarning,
    )

    return is_url(url)


def is_url(subject):  # pragma: no cover
    """
    Check if the given subject is a syntactically valid URL.

    :param subject: The subject to check the syntax from.
    :type subject: str|list

    :return: The syntax validity.
    :rtype: bool|dict
    """

    if subject:
        # The given subject is not empty nor None.

        # We return the validity of the given subject.
        return core.API(subject).url_syntax()

    # We return None, there is nothing to check.
    return None


def load_config(generate_directory_structure=False, custom=None):  # pragma: no cover
    """
    Load the configuration.

    :param bool generate_directory_structure:
        Tell us if we generate the directory structure
        along with loading the configuration file.

    :param dict custom:
        A dict with the configuration index (from .PyFunceble.yaml) to update.

    .. note::
        If :code:`config` is given, the given :code:`dict` overwrite
        the last value of the given indexes in the configuration.

        It's actually something like following:

        ::

            pyfunceble.configuration.update(config_given_by_user)
    """

    if not LOADER:
        loader = cconfig.Loader()
        loader.set_path_to_config(CONFIG_DIRECTORY)
        loader.get_config()
        loader.set_custom_config(custom)
    elif not LOADER.was_configuration_loaded():
        LOADER.set_path_to_config(CONFIG_DIRECTORY)
        LOADER.get_config()
        LOADER.set_custom_config(custom)
    else:
        LOADER.set_custom_config(custom)

    if generate_directory_structure:
        output.Constructor()


def is_domain_malicious(subject):  # pragma: no cover
    """
    Checks if the given domain is malicious.

    :param str subject: The subject to work with.

    :rtype: bool
    """

    if subject:
        return core.API(subject).reputation("domain") == "MALICIOUS"
    return None


def is_ipv4_malicious(subject):  # pragma: no cover
    """
    Checks if the given IPv4 is malicious.

    :rtype: bool
    """

    return is_domain_malicious(subject)


def is_url_malicious(subject):  # pragma: no cover
    """
    Checks if the given URL is malicious.

    :param str subject: The subject to work with.

    :rtype: bool
    """

    if subject:
        return core.API(subject).reputation("url") == "MALICIOUS"
    return None


def get_complements(subject, include_given=False):
    """
    Provides the complements of the given subject(s).

    A complement is for example :code:`example.com` if :code:`www.example.com`
    is given and vice-versa.

    :param subject: The subject to get the complement for.
    :type subject: str, list

    :param bool include_given:
        Tell us to add the given one into the result.

    :rtype: list
    """

    complements = []

    if isinstance(subject, str):
        checker = Check(subject)

        if include_given and subject not in complements:
            complements.append(subject)

        if subject.startswith("www."):
            complements.append(subject[4:])
        elif checker.is_domain() and not checker.is_subdomain():
            complements.append(f"www.{subject}")
    elif isinstance(subject, (list, set)):
        for subj in subject:
            complements.extend(get_complements(subj, include_given=include_given))

    return complements
