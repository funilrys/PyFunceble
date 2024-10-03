"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Tests of the Platform query tool.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://docs.pyfunceble.com

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022, 2023, 2024 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# pylint: disable=too-many-lines

import json
import os
import secrets
import unittest
import unittest.mock
from datetime import datetime, timezone

import requests
import requests.models

from PyFunceble.checker.availability.status import AvailabilityCheckerStatus
from PyFunceble.config.loader import ConfigLoader
from PyFunceble.query.platform import PlatformQueryTool


class TestPlatformQueryTool(unittest.TestCase):
    """
    Tests the Platform query tool.
    """

    def setUp(self) -> None:
        """
        Sets everything needed by the tests.
        """

        self.query_tool = PlatformQueryTool()

        self.response_dataset = {
            "subject": "example.net",
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "status": {
                "syntax": {
                    "latest": {
                        "status": "VALID",
                        "status_source": "SYNTAX",
                        "tested_at": "2021-09-28T19:32:07.167Z",
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    },
                    "frequent": "VALID",
                },
                "availability": {
                    "latest": {
                        "status": "ACTIVE",
                        "status_source": "WHOIS",
                        "tested_at": "2021-09-28T19:32:07.167Z",
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    },
                    "frequent": "ACTIVE",
                },
                "reputation": {
                    "latest": {
                        "status": "SANE",
                        "status_source": "REPUTATION",
                        "tested_at": "2021-09-28T19:32:07.167Z",
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    },
                    "frequent": "SANE",
                },
                "whois": {
                    "expiration_date": "2021-09-28T19:32:07.167Z",
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "subject_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                },
            },
        }

        self.status_dataset = {
            "status": "ACTIVE",
            "status_source": "WHOIS",
            "tested_at": "2021-09-28T20:55:41.730Z",
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "subject_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        }

        self.availability_status_dataset = {
            "checker_type": "AVAILABILITY",
            "dns_lookup": {"NS": ["a.iana-servers.net.", "b.iana-servers.net."]},
            "dns_lookup_record": {
                "dns_name": "example.com.",
                "follow_nameserver_order": True,
                "nameserver": "9.9.9.9",
                "port": 53,
                "preferred_protocol": "UDP",
                "query_record_type": "NS",
                "query_timeout": 5.0,
                "response": ["a.iana-servers.net.", "b.iana-servers.net."],
                "subject": "example.com",
                "used_protocol": "UDP",
            },
            "domain_syntax": True,
            "expiration_date": None,
            "http_status_code": None,
            "idna_subject": "example.com",
            "ip_syntax": False,
            "ipv4_range_syntax": False,
            "ipv4_syntax": False,
            "ipv6_range_syntax": False,
            "ipv6_syntax": False,
            "netinfo": None,
            "params": {
                "do_syntax_check_first": False,
                "use_dns_lookup": True,
                "use_extra_rules": True,
                "use_http_code_lookup": True,
                "use_netinfo_lookup": True,
                "use_reputation_lookup": False,
                "use_whois_db": True,
                "use_whois_lookup": False,
            },
            "second_level_domain_syntax": True,
            "status": "ACTIVE",
            "status_after_extra_rules": None,
            "status_before_extra_rules": None,
            "status_source": "DNSLOOKUP",
            "status_source_after_extra_rules": None,
            "status_source_before_extra_rules": None,
            "subdomain_syntax": False,
            "subject": "example.com",
            "tested_at": datetime.fromisoformat(
                "2021-03-09T17:42:15.771647"
            ).astimezone(timezone.utc),
            "url_syntax": False,
            "whois_lookup_record": {
                "expiration_date": None,
                "port": 43,
                "query_timeout": 5.0,
                "record": None,
                "server": None,
                "subject": "example.com",
            },
            "whois_record": None,
        }
        return super().setUp()

    def tearDown(self) -> None:
        """
        Destroys everything needed by the tests.
        """

        del self.query_tool
        del self.response_dataset
        del self.availability_status_dataset

    def test_set_token_return(self) -> None:
        """
        Tests the response from the method which let us set the token to work
        with.
        """

        given = secrets.token_urlsafe(6)

        actual = self.query_tool.set_token(given)

        self.assertIsInstance(actual, PlatformQueryTool)

    def test_set_token_method(self) -> None:
        """
        Tests the method which let us set the token to work with.
        """

        given = secrets.token_urlsafe(6)
        expected = given

        self.query_tool.set_token(given)
        actual = self.query_tool.token

        self.assertEqual(expected, actual)

    def test_set_token_attribute(self) -> None:
        """
        Tests the overwritting of the token attribute.
        """

        given = secrets.token_urlsafe(6)
        expected = given

        self.query_tool.token = given
        actual = self.query_tool.token

        self.assertEqual(expected, actual)

    def test_set_token_through_init(self) -> None:
        """
        Tests the overwritting of the token to work through the class
        constructor.
        """

        given = secrets.token_urlsafe(6)
        expected = given

        query_tool = PlatformQueryTool(token=given)
        actual = query_tool.token

        self.assertEqual(expected, actual)

    def test_set_token_through_init_environment_variable_not_given(self) -> None:
        """
        Tests the overwritting of the token to work through the class
        constructor.

        In this test we test the case that nothing is given or declared.
        """

        if "PYFUNCEBLE_COLLECTION_API_TOKEN" in os.environ:  # pragma: no cover
            del os.environ["PYFUNCEBLE_COLLECTION_API_TOKEN"]

        if "PYFUNCEBLE_PLATFORM_API_TOKEN" in os.environ:  # pragma: no cover
            del os.environ["PYFUNCEBLE_PLATFORM_API_TOKEN"]

        expected = ""

        query_tool = PlatformQueryTool(token=None)
        actual = query_tool.token

        self.assertEqual(expected, actual)

    def test_set_token_through_init_environment_variable_given(self) -> None:
        """
        Tests the overwritting of the token to work through the class
        constructor.

        In this test we test the case that the environment variable is given.
        """

        given = secrets.token_urlsafe(6)
        expected = given

        if "PYFUNCEBLE_COLLECTION_API_TOKEN" in os.environ:
            del os.environ["PYFUNCEBLE_COLLECTION_API_TOKEN"]

        os.environ["PYFUNCEBLE_PLATFORM_API_TOKEN"] = given

        query_tool = PlatformQueryTool(token=None)
        actual = query_tool.token

        self.assertEqual(expected, actual)

    def test_set_token_not_str(self) -> None:
        """
        Tests the method which let us set the token to work with for the case
        that the given token is not a :py:class:`str`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.query_tool.set_token(given))

    def test_set_url_base_not_str(self) -> None:
        """
        Tests the method which let us set the URL to work from for the case
        that the given URL is not a :py:class:`str`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(TypeError, lambda: self.query_tool.set_url_base(given))

    def test_set_url_base_not_url(self) -> None:
        """
        Tests the method which let us set the URL to work from for the case
        that the given URL is not a supported URL.
        """

        given = "example.org"

        self.assertRaises(ValueError, lambda: self.query_tool.set_url_base(given))

    def test_set_url_base_ends_with_slash(self) -> None:
        """
        Tests the method which let us set the URL to work from for the case
        that the given URL is not a supported URL.
        """

        given = "http://example.org/"
        expected = "http://example.org"

        self.query_tool.url_base = given
        actual = self.query_tool.url_base

        self.assertEqual(expected, actual)

    def test_set_preferred_status_origin_return(self) -> None:
        """
        Tests the response from the method which let us set the preferred status
        origin.
        """

        given = "latest"

        actual = self.query_tool.set_preferred_status_origin(given)

        self.assertIsInstance(actual, PlatformQueryTool)

    def test_set_preferred_status_origin_method(self) -> None:
        """
        Tests the method which let us set the preferred status origin.
        """

        given = "frequent"
        expected = given

        self.query_tool.set_preferred_status_origin(given)
        actual = self.query_tool.preferred_status_origin

        self.assertEqual(expected, actual)

    def test_set_preferred_status_origin_attribute(self) -> None:
        """
        Tests the overwritting of the the preferred status origin.
        """

        given = "latest"
        expected = given

        self.query_tool.preferred_status_origin = given
        actual = self.query_tool.preferred_status_origin

        self.assertEqual(expected, actual)

    def test_setpreferred_status_origin_through_init(self) -> None:
        """
        Tests the overwritting of the preferred status origin through the class
        constructor.
        """

        given = "frequent"
        expected = given

        query_tool = PlatformQueryTool(preferred_status_origin=given)
        actual = query_tool.preferred_status_origin

        self.assertEqual(expected, actual)

    def test_set_preferred_status_origin_through_init_none_given(self) -> None:
        """
        Tests the overwritting of the preferred status origin through the class
        constructor.

        In this test, we test the case that nothing is given.
        """

        given = None
        expected = "frequent"

        query_tool = PlatformQueryTool(preferred_status_origin=given)
        actual = query_tool.preferred_status_origin

        self.assertEqual(expected, actual)

    def test_set_preferred_status_origin_not_str(self) -> None:
        """
        Tests the method which let us set the preferred status origin for the case
        that the given value is not a :py:class:`str`.
        """

        given = ["Hello", "World!"]

        self.assertRaises(
            TypeError, lambda: self.query_tool.set_preferred_status_origin(given)
        )

    def test_set_preferred_status_origin_not_supported(self) -> None:
        """
        Tests the method which let us set the URL to work from for the case
        that the given URL is not a supported URL.
        """

        given = "hello"

        self.assertRaises(
            ValueError, lambda: self.query_tool.set_preferred_status_origin(given)
        )

    def test_guess_and_set_preferred_status_origin(self) -> None:
        """
        Tests the method which let us guess and set the preferred status origin.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config(
            {"platform": {"preferred_status_origin": "latest"}}
        ).start()

        self.query_tool.guess_and_set_preferred_status_origin()

        expected = "latest"
        actual = self.query_tool.preferred_status_origin

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_preferred_status_origin_not_str(self) -> None:
        """
        Tests the method which let us guess and set the preferred status origin.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config(
            {"platform": {"preferred_status_origin": None}}
        ).start()

        self.query_tool.guess_and_set_preferred_status_origin()

        expected = "frequent"
        actual = self.query_tool.preferred_status_origin

        self.assertEqual(expected, actual)

        del config_loader

    def test_set_checker_priority_return(self) -> None:
        """
        Tests the response from the method which let us set the checker priority
        to use.
        """

        given = ["reputation", "syntax", "availability"]

        actual = self.query_tool.set_checker_priority(given)

        self.assertIsInstance(actual, PlatformQueryTool)

    def test_set_checker_priority_method(self) -> None:
        """
        Tests the method which let us set the checker priority to use.
        """

        given = ["availability", "syntax", "reputation"]
        expected = given

        self.query_tool.set_checker_priority(given)
        actual = self.query_tool.checker_priority

        self.assertEqual(expected, actual)

    def test_set_checker_priority_attribute(self) -> None:
        """
        Tests the overwritting of the the checker priority.
        """

        given = ["syntax", "availability", "reputation"]
        expected = given

        self.query_tool.checker_priority = given
        actual = self.query_tool.checker_priority

        self.assertEqual(expected, actual)

    def test_checker_priority_through_init(self) -> None:
        """
        Tests the overwritting of the checker priority through the class
        constructor.
        """

        given = ["reputation", "syntax", "availability"]
        expected = given

        query_tool = PlatformQueryTool(checker_priority=given)
        actual = query_tool.checker_priority

        self.assertEqual(expected, actual)

    def test_set_checker_priority_init_none_given(self) -> None:
        """
        Tests the overwritting of the checker through the class
        constructor.

        In this test, we test the case that nothing is given.
        """

        given = None
        expected = ["none"]

        query_tool = PlatformQueryTool(checker_priority=given)
        actual = query_tool.checker_priority

        self.assertEqual(expected, actual)

    def test_set_checker_priority_not_str(self) -> None:
        """
        Tests the method which let us set the checker priority for the case
        that a given value is not a :py:class:`str`.
        """

        given = ["reputation", "syntax", 123]

        self.assertRaises(
            TypeError, lambda: self.query_tool.set_checker_priority(given)
        )

    def test_set_checker_priority_not_supported(self) -> None:
        """
        Tests the method which let us set the checker priority to work from
        for the case that the given checker is not supported.
        """

        given = ["reputation", "syntax", "hello"]

        self.assertRaises(
            ValueError, lambda: self.query_tool.set_checker_priority(given)
        )

    def test_guess_and_set_checker_priority(self) -> None:
        """
        Tests the method which let us guess and set the checker type.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config(
            {"platform": {"checker_priority": ["reputation", "syntax", "availability"]}}
        ).start()

        self.query_tool.guess_and_set_checker_priority()

        expected = ["reputation", "syntax", "availability"]
        actual = self.query_tool.checker_priority

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_checker_priority_not_str(self) -> None:
        """
        Tests the method which let us guess and set the checker priority.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config(
            {"platform": {"checker_priority": None}}
        ).start()

        self.query_tool.guess_and_set_checker_priority()

        expected = ["none"]
        actual = self.query_tool.checker_priority

        self.assertEqual(expected, actual)

        del config_loader

    def test_set_checker_exclude_return(self) -> None:
        """
        Tests the response from the method which let us set the checker to
        exclude.
        """

        given = ["reputation", "syntax", "availability"]

        actual = self.query_tool.set_checker_exclude(given)

        self.assertIsInstance(actual, PlatformQueryTool)

    def test_set_checker_exclude_method(self) -> None:
        """
        Tests the method which let us set the checker to exclude.
        """

        given = ["availability", "syntax", "reputation"]
        expected = given

        self.query_tool.set_checker_exclude(given)
        actual = self.query_tool.checker_exclude

        self.assertEqual(expected, actual)

    def test_set_checker_exclude_attribute(self) -> None:
        """
        Tests the overwritting of the checker exclude to use.
        """

        given = ["syntax", "availability", "reputation"]
        expected = given

        self.query_tool.checker_exclude = given
        actual = self.query_tool.checker_exclude

        self.assertEqual(expected, actual)

    def test_checker_exclude_through_init(self) -> None:
        """
        Tests the overwritting of the checker to exclude through the class
        constructor.
        """

        given = ["reputation", "syntax", "availability"]
        expected = given

        query_tool = PlatformQueryTool(checker_exclude=given)
        actual = query_tool.checker_exclude

        self.assertEqual(expected, actual)

    def test_set_checker_exclude_init_none_given(self) -> None:
        """
        Tests the overwritting of the checker through the class
        constructor.

        In this test, we test the case that nothing is given.
        """

        given = None
        expected = ["none"]

        query_tool = PlatformQueryTool(checker_exclude=given)
        actual = query_tool.checker_exclude

        self.assertEqual(expected, actual)

    def test_set_checker_exclude_not_str(self) -> None:
        """
        Tests the method which let us set the checker exclude for the case
        that a given value is not a :py:class:`str`.
        """

        given = ["reputation", "syntax", 123]

        self.assertRaises(TypeError, lambda: self.query_tool.set_checker_exclude(given))

    def test_set_checker_exclude_not_supported(self) -> None:
        """
        Tests the method which let us set the checker exclude to work with
        for the case that the given checker is not supported.
        """

        given = ["syntax", "reputation", "hello"]

        self.assertRaises(
            ValueError, lambda: self.query_tool.set_checker_exclude(given)
        )

    def test_guess_and_set_checker_exclude(self) -> None:
        """
        Tests the method which let us guess and set the checker type to exclude.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config(
            {"platform": {"checker_exclude": ["syntax", "reputation", "availability"]}}
        ).start()

        self.query_tool.guess_and_set_checker_exclude()

        expected = ["syntax", "reputation", "availability"]
        actual = self.query_tool.checker_exclude

        self.assertEqual(expected, actual)

        del config_loader

    def test_guess_and_set_checker_exclude_not_str(self) -> None:
        """
        Tests the method which let us guess and set the checker to exclude.
        """

        config_loader = ConfigLoader()
        config_loader.set_custom_config({"platform": {"checker_exclude": None}}).start()

        self.query_tool.guess_and_set_checker_exclude()

        expected = ["none"]
        actual = self.query_tool.checker_exclude

        self.assertEqual(expected, actual)

        del config_loader

    @unittest.mock.patch.object(requests.Session, "post")
    def test_platform_contain(self, request_mock) -> None:
        """
        Tests the method which let us pull the subject from the platform.
        """

        response_dict = self.response_dataset
        response_dict["subject"] = "example.com"

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = json.dumps(response_dict)

            response = requests.models.Response()
            response.url = "https://example.org/v1/search"
            response.status_code = 200

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.url_base = "https://example.org"
        request_mock.side_effect = mocking

        expected = True
        actual = "example.com" in self.query_tool

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(requests.Session, "post")
    def test_platform_not_contain(self, request_mock) -> None:
        """
        Tests the method which let us pull the subject from the platform.
        """

        response_dict = {"detail": "Invalid subject."}

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = json.dumps(response_dict)

            response = requests.models.Response()
            response.url = "https://example.org/v1/search"
            response.status_code = 404

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.url_base = "https://example.org"
        request_mock.side_effect = mocking

        expected = False
        actual = "example.com" in self.query_tool

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(requests.Session, "post")
    def test_getitem(self, request_mock) -> None:
        """
        Tests the method which let us pull the subject from the platform.
        """

        response_dict = self.response_dataset
        response_dict["subject"] = "example.org"

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = json.dumps(response_dict)

            response = requests.models.Response()
            response.url = "https://example.org/v1/search"
            response.status_code = 200

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.url_base = "https://example.org"
        request_mock.side_effect = mocking

        expected = response_dict
        actual = self.query_tool["example.org"]

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(requests.Session, "post")
    def test_getitem_not_found(self, request_mock) -> None:
        """
        Tests the method which let us pull the subject from the platform.
        """

        response_dict = {"detail": "Invalid subject."}

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = json.dumps(response_dict)

            response = requests.models.Response()
            response.url = "https://example.org/v1/search"
            response.status_code = 404

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.url_base = "https://example.org"
        request_mock.side_effect = mocking

        expected = None
        actual = self.query_tool["example.de"]

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(requests.Session, "post")
    def test_pull(self, request_mock) -> None:
        """
        Tests the method which let us pull the subject from the platform.
        """

        response_dict = self.response_dataset
        response_dict["subject"] = "example.net"

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = json.dumps(response_dict)

            response = requests.models.Response()
            response.url = "https://example.org/v1/search"
            response.status_code = 200

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.url_base = "https://example.org"
        request_mock.side_effect = mocking

        expected = response_dict
        actual = self.query_tool.pull("example.net")

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(requests.Session, "post")
    def test_pull_subject_not_found(self, request_mock) -> None:
        """
        Tests the method which let us pull the subject from the platform.

        In this test case we check what happens when a subject is not found.
        """

        response_dict = {"detail": "Invalid subject."}

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = json.dumps(response_dict)

            response = requests.models.Response()
            response.url = "https://example.org/v1/search"
            response.status_code = 404

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.url_base = "https://example.org"
        request_mock.side_effect = mocking

        expected = None
        actual = self.query_tool.pull("example.net")

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(requests.Session, "post")
    def test_pull_subject_no_json_response(self, request_mock) -> None:
        """
        Tests the method which let us pull the subject from the platform.

        In this test case we check what happens when no JSON response is given.
        """

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = "I'm a teapot."

            response = requests.models.Response()
            response.url = "https://example.org/v1/search"
            response.status_code = 418

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.url_base = "https://example.org"
        request_mock.side_effect = mocking

        expected = None
        actual = self.query_tool.pull("example.net")

        self.assertEqual(expected, actual)

    def test_pull_subject_not_str(self) -> None:
        """
        Tests the method which let us pull the subject from the platform.

        In this test we test the case that the given subject is not a
        :py:class:`str`.
        """

        self.query_tool.url_base = "https://example.org"

        self.assertRaises(TypeError, lambda: self.query_tool.pull(284))

    @unittest.mock.patch.object(requests.Session, "post")
    def test_push(self, request_mock) -> None:
        """
        Tests the method which let us push some dataset into the platform.
        """

        response_dict = self.response_dataset
        response_dict["subject"] = "example.net"

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = json.dumps(response_dict)

            response = requests.models.Response()
            response.url = "https://example.org/v1/status/availability"
            response.status_code = 200

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.url_base = "https://example.org"
        self.query_tool.token = secrets.token_urlsafe(6)

        request_mock.side_effect = mocking

        expected = response_dict
        actual = self.query_tool.push(
            AvailabilityCheckerStatus(**self.availability_status_dataset)
        )

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(requests.Session, "post")
    def test_push_no_json_response(self, request_mock) -> None:
        """
        Tests the method which let us push some dataset into the platform.

        In this test case, we test the case that the response is not JSON
        encoded.
        """

        response_dict = self.response_dataset
        response_dict["subject"] = "example.net"

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = "I'm a teapot."

            response = requests.models.Response()
            response.url = "https://example.org/v1/status/availability"
            response.status_code = 418

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.url_base = "https://example.org"
        request_mock.side_effect = mocking

        expected = None
        actual = self.query_tool.push(
            AvailabilityCheckerStatus(**self.availability_status_dataset)
        )

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(requests.Session, "post")
    def test_push_with_whois(self, request_mock) -> None:
        """
        Tests the method which let us push some dataset into the platform.
        """

        response_dict = self.response_dataset
        response_dict["subject"] = "example.net"
        self.availability_status_dataset["expiration_date"] = "23-nov-2090"

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = json.dumps(response_dict)

            response = requests.models.Response()
            response.url = "https://example.org/v1/status/availability"
            response.status_code = 200

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.url_base = "https://example.org"
        self.query_tool.token = secrets.token_urlsafe(6)
        request_mock.side_effect = mocking

        expected = response_dict
        actual = self.query_tool.push(
            AvailabilityCheckerStatus(**self.availability_status_dataset)
        )

        self.assertEqual(expected, actual)

    @unittest.mock.patch.object(requests.Session, "post")
    def test_push_with_whois_no_json_response(self, request_mock) -> None:
        """
        Tests the method which let us push some dataset into the platform.
        """

        response_dict = self.response_dataset
        response_dict["subject"] = "example.net"
        self.availability_status_dataset["expiration_date"] = "23-nov-2090"

        def mocking(*args, **kwargs):  # pylint: disable=unused-argument
            response_content = "I'm a teapot."

            response = requests.models.Response()
            response.url = "https://example.org/v1/status/availability"
            response.status_code = 418

            # pylint: disable=protected-access
            response._content = str.encode(response_content)

            response.history = [response]

            return response

        self.query_tool.url_base = "https://example.org"
        self.query_tool.token = secrets.token_urlsafe(6)
        request_mock.side_effect = mocking

        expected = None
        actual = self.query_tool.push(
            AvailabilityCheckerStatus(**self.availability_status_dataset)
        )

        self.assertEqual(expected, actual)

    def test_push_with_whois_token_not_given(self) -> None:
        """
        Tests the method which let us push some dataset into the platform.

        In this test, we test the case that no token is given.
        """

        response_dict = self.response_dataset
        response_dict["subject"] = "example.net"
        self.availability_status_dataset["expiration_date"] = "23-nov-2090"

        if "PYFUNCEBLE_COLLECTION_API_TOKEN" in os.environ:  # pragma: no cover
            del os.environ["PYFUNCEBLE_COLLECTION_API_TOKEN"]

        if "PYFUNCEBLE_PLATFORM_API_TOKEN" in os.environ:  # pragma: no cover
            del os.environ["PYFUNCEBLE_PLATFORM_API_TOKEN"]

        self.query_tool.token = ""

        expected = None
        actual = self.query_tool.push(
            AvailabilityCheckerStatus(**self.availability_status_dataset)
        )

        self.assertEqual(expected, actual)

    def test_push_subject_not_str(self) -> None:
        """
        Tests the method which let us push some dataset into the platform.

        In this test, we test the case that the given subject is not a string.
        """

        self.availability_status_dataset["subject"] = 293

        self.assertRaises(
            TypeError,
            lambda: self.query_tool.push(
                AvailabilityCheckerStatus(**self.availability_status_dataset)
            ),
        )

    def test_push_checker_status_not_correct(self) -> None:
        """
        Tests the method which let us push some dataset into the platform.

        In this test, we test the case that the given checker status is not
        correct.
        """

        self.availability_status_dataset["subject"] = "foo.example.org"

        self.assertRaises(
            TypeError,
            lambda: self.query_tool.push(self.availability_status_dataset),
        )

    def test_push_subject_empty_str(self) -> None:
        """
        Tests the method which let us push some dataset into the platform.

        In this test, we test the case that the given subject is an empty string.
        """

        self.availability_status_dataset["subject"] = ""

        self.assertRaises(
            ValueError,
            lambda: self.query_tool.push(
                AvailabilityCheckerStatus(**self.availability_status_dataset)
            ),
        )

    def test_push_checker_type_not_str(self) -> None:
        """
        Tests the method which let us push some dataset into the platform.

        In this test, we test the case that the given subject is not a string.
        """

        self.availability_status_dataset["checker_type"] = 987

        self.assertRaises(
            TypeError,
            lambda: self.query_tool.push(
                AvailabilityCheckerStatus(**self.availability_status_dataset)
            ),
        )

    def test_push_checker_type_not_supported(self) -> None:
        """
        Tests the method which let us push some dataset into the platform.

        In this test, we test the case that the given subject is not a string.
        """

        self.availability_status_dataset["checker_type"] = "GIT"
        self.query_tool.token = secrets.token_urlsafe(6)

        self.assertRaises(
            ValueError,
            lambda: self.query_tool.push(
                AvailabilityCheckerStatus(**self.availability_status_dataset)
            ),
        )

    def test_push_token_not_given(self) -> None:
        """
        Tests the method which let us push some dataset into the platform.

        In this test, we test the case that no token is given.
        """

        if "PYFUNCEBLE_COLLECTION_API_TOKEN" in os.environ:  # pragma: no cover
            del os.environ["PYFUNCEBLE_COLLECTION_API_TOKEN"]

        if "PYFUNCEBLE_PLATFORM_API_TOKEN" in os.environ:  # pragma: no cover
            del os.environ["PYFUNCEBLE_PLATFORM_API_TOKEN"]

        self.query_tool.token = ""

        expected = None
        actual = self.query_tool.push(
            AvailabilityCheckerStatus(**self.availability_status_dataset)
        )

        self.assertEqual(expected, actual)
