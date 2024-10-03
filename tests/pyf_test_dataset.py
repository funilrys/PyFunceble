"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides some datasets.

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

from typing import List

VALID_SECOND_LVL_DOMAINS: List[str] = [
    "example.org",
    "example.net",
    "example.co.uk",
    "example.de",
    "985.com",
]

NOT_VALID_SECOND_LVL_DOMAINS: List[str] = [
    "hello.example.org",
    "world.example.net",
    "hello.world.example.co.uk",
    "world.hello.example.de",
]

VALID_DOMAINS: List[str] = [
    "_hello_.example.co.uk.",
    "_hello_.example.co.uk",
    "_hello_world_.example.co.uk.",
    "_hello_world_.example.co.uk",
    "_hello_world_.hello.eu.com.",
    "_hello_world_.hello.eu.com",
    "_hello-beautiful-world_.wold.eu.com.",
    "_hello-beautiful-world_.wold.eu.com",
    "_hello-world.example.co.uk.",
    "_hello-world.example.co.uk",
    "_hello._world.example.co.uk.",
    "_hello._world.example.co.uk",
    "_hello.example.co.uk.",
    "_hello.example.co.uk",
    "_world_.hello.eu.com.",
    "_world_.hello.eu.com",
    "_world.hello.eu.com.",
    "_world.hello.eu.com",
    "hello_.world.eu.com.",
    "hello_.world.eu.com",
    "hello_world.example.co.uk.",
    "hello_world.example.co.uk",
    "hello_world.world.com.",
    "hello_world.world.com",
    "hello_world.world.hello.com.",
    "hello_world.world.hello.com",
    "hello---world.com.",
    "hello---world.com",
    "hello-.example.co.uk.",
    "hello-.example.co.uk",
    "hello-world.com.",
    "hello-world.com",
    "hello.onion",
    "hello.world_hello.world.com.",
    "hello.world_hello.world.com",
    "hello.world.com.",
    "hello.world.com",
    "hello.world.hello.com.",
    "hello.world.hello.com",
    "pogotowie-komputerowe-warszawa.com.pl",
    "worl.hello.onion",
    "xn--bittr-fsa6124c.com.",
    "xn--bittr-fsa6124c.com",
    "xn--bllogram-g80d.com.",
    "xn--bllogram-g80d.com",
    "xn--coinbse-30c.com.",
    "xn--coinbse-30c.com",
    "xn--cryptopi-ux0d.com.",
    "xn--cryptopi-ux0d.com",
    "xn--cyptopia-4e0d.com.",
    "xn--cyptopia-4e0d.com",
    "www.hello_world.blogspot.co.nz",
    "hello_world.blogspot.co.nz",
    "example.org",
    "bịllogram.com",
    "bittréẋ.com",
    "coinbȧse.com",
    "cryptopiạ.com",
    "cṙyptopia.com",
    "985.com",
    "hello-world.example.msn.cn",
    "hello_world.co.uk",
    "_world._hello.eu.com",
    "_world.hello_.eu.com",
]

NOT_VALID_DOMAINS: List[str] = [
    "-hello-.example.co.uk",
    "-hello-world_.example.co.uk",
    "-hello-world_all-mine_.hello.eu.com",
    "-hello.example.co.uk",
    "-hello.world",
    "-world.hello",
    "..",
    ".",
    r"bịl\llogram.com",
    "hello_world_.com",
    "hello_world.com",
    "hello-.world",
    "hello-world",
    "hello.-hello-world_.example.co.uk",
    "hello@world.com",
    "httpWd",
    "test.-hello-world_all-mine_.example.co.uk",
    "world_hello.com",
    "world-.hello",
    "world-hello",
    "world.hello:80",
    "world@hello.com",
    "example.com\\",
    "ex\\ample.com",
]

VALID_SUBDOMAINS: List[str] = [
    "hello_world.world.com",
    "hello_world.world.hello.com",
    "hello.world_hello.world.com",
    "hello.world.hello.com",
    "hello_.world.eu.com",
    "_world.hello.eu.com",
    "_world_.hello.eu.com",
    "_hello-beautiful-world_.wold.eu.com",
    "_hello_world_.hello.eu.com",
    "_hello.example.co.uk",
    "_hello_.example.co.uk",
    "_hello._world.example.co.uk",
    "_hello-world.example.co.uk",
    "_hello_world_.example.co.uk",
    "hello_world.example.co.uk",
    "hello-.example.co.uk",
    "hello.world.onion",
    "test.hello.blogspot.co.uk",
    "888.0769.com",
    "1661599812.hello.985.com",
    "hi.hello.example.world.s3.ap-northeast-2.amazonaws.com",
    "world_hello.hello_world.co.uk",
]

NOT_VALID_SUBDOMAINS: List[str] = [
    "-hello.world",
    "bịllogram.com",
    "bittréẋ.com",
    "coinbȧse.com",
    "cryptopiạ.com",
    "cṙyptopia.com",
    "google.com",
    "hello_world_.com",
    "hello_world.com",
    "hello-.world",
    "hello-world",
    "pogotowie-komputerowe-warszawa.com.pl",
    "hello.world.example.com\\",
    "he\\llo.world.example.com",
]

VALID_IPV4: List[str] = ["15.47.85.65", "45.66.255.240", "255.45.65.0/24"]

VALID_IPV6: List[str] = [
    "2001:db8::",
    "2001:db8::1000",
    "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    "2001:db8:85a3:0:0:8a2e:370:7334",
    "2001:db8:85a3::8a2e:370:7334",
    "::1",
    "::",
    "2001:db8:1234::/48",
    "2001:db8:1234:0000:0000:0000:0000:0000",
    "2001:db8:1234:ffff:ffff:ffff:ffff:ffff",
    "2001:db8:a::/64",
    "2001:db8:a::123/64",
    "2001:db8:85a3:8d3:1319:8a2e:370:7348",
    "::/0",
    "::/128",
    "::1/128",
    "::ffff:0:0/96",
    "::ffff:0:0:0/96",
    "64:ff9b::/96",
    "100::/64",
    "2001::/32",
    "2001:20::/28",
    "2001:db8::/32",
    "2002::/16",
    "fc00::/7",
    "fe80::/10",
    "ff00::/8",
]

NOT_VALID_IPV4: List[str] = ["google.com", "287.468.45.26", "245.85.69.17:8081"]

NOT_VALID_IPV6: List[str] = [
    "google.com",
    "287.468.45.26",
    "2001:db8::/4839",
    "2001:::",
    "2001:db8:85a3:8d3:1319:8a2e:370:7348f",
    "2001:db8:85a3:8d3:1319:8a2e:370:7348/129",
]

VALID_IPV4_RANGES: List[str] = ["255.45.65.0/24", "255.45.65.6/18"]

VALID_IPV6_RANGES: List[str] = [
    "2001:db8::/128",
    "2001:db8:1234::/48",
    "2001:db8:a::/64",
    "2001:db8:a::123/64",
]

NOT_VALID_IPV4_RANGES: List[str] = ["15.47.85.65", "45.66.255.240", "github.com"]

NOT_VALID_IPV6_RANGES: List[str] = ["2001:db8::/129", "github.com", "2001:db8:a::"]

RESERVED_IPV4: List[str] = [
    "0.45.23.59",
    "10.39.93.13",
    "100.64.35.85",
    "127.57.91.13",
    "169.254.98.65",
    "172.16.17.200",
    "192.0.0.145",
    "192.0.2.39",
    "192.168.21.99",
    "192.175.48.25",
    "192.31.196.176",
    "192.52.193.245",
    "192.88.99.30",
    "198.18.145.234",
    "198.51.100.212",
    "203.0.113.103",
    "224.134.13.24",
    "240.214.30.11",
    "255.255.255.255",
]

RESERVED_IPV6: List[str] = [
    "::",
    "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
    "::1",
    "::ffff:0.0.0.0",
    "::ffff:255.255.255.255",
    "::ffff:0:0.0.0.0",
    "::ffff:0:255.255.255.255",
    "64:ff9b::0.0.0.0",
    "64:ff9b::255.255.255.255",
    "100::",
    "100::ffff:ffff:ffff:ffff",
    "2001::",
    "2001::ffff:ffff:ffff:ffff:ffff:ffff",
    "2001:60::",
    "2001:5f:ffff:ffff:ffff:ffff:ffff:ffff",
    "2001:db8::",
    "2001:db8:ffff:ffff:ffff:ffff:ffff:ffff",
    "fc00::",
    "fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
    "fe80::",
    "febf:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
    "ff00::",
    "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
]

NOT_RESERVED_IPV4: List[str] = [
    "hello.world",
    "192.243.198.89",
    "45.34.29.15",
    "127.0.0.53/32",
]

NOT_RESERVED_IPV6: List[str] = [
    "2001:db8::/128",
    "hello.world",
    "2001:db8:1234::/48",
    "2001:db8:a::/64",
    "2001:db8:a::123/64",
    "github.com",
]

DEFAULT_CONFIG: dict = {
    "cli_decoding": {
        "adblock": False,
        "aggressive": False,
        "rpz": False,
        "wildcard": False,
    },
    "cli_testing": {
        "autocontinue": False,
        "ci": {
            "active": False,
            "branch": "master",
            "command": None,
            "commit_message": "PyFunceble - AutoSave",
            "distribution_branch": "master",
            "end_command": None,
            "end_commit_message": "PyFunceble - Results",
            "max_exec_minutes": 15,
        },
        "complements": False,
        "cooldown_time": 0.0,
        "days_between": {"db_clean": 28, "db_retest": 1},
        "db_type": "csv",
        "display_mode": {
            "all": False,
            "colour": True,
            "dots": False,
            "execution_time": False,
            "less": True,
            "percentage": True,
            "quiet": False,
            "simple": False,
            "status": "all",
        },
        "file_filter": None,
        "file_generation": {
            "analytic": True,
            "hosts": False,
            "no_file": False,
            "plain": True,
            "unified_results": False,
            "merge_output_dirs": False,
        },
        "hosts_ip": "0.0.0.0",
        "inactive_db": True,
        "local_network": False,
        "max_workers": None,
        "mining": False,
        "preload_file": False,
        "sorting_mode": {"hierarchical": False, "standard": True},
        "testing_mode": {"availability": True, "reputation": False, "syntax": False},
        "whois_db": True,
    },
    "platform": {
        "push": False,
        "preferred_data_origin": "frequent",
    },
    "debug": {"active": False, "level": "info"},
    "dns": {
        "follow_server_order": True,
        "protocol": "UDP",
        "server": None,
        "trust_server": False,
    },
    "http_codes": {
        "list": {
            "potentially_down": [400, 402, 404, 409, 410, 412, 414, 415, 416, 451],
            "potentially_up": [
                300,
                301,
                302,
                303,
                304,
                305,
                307,
                308,
                403,
                405,
                406,
                407,
                408,
                411,
                413,
                417,
                418,
                421,
                422,
                423,
                424,
                426,
                428,
                431,
                500,
                501,
                502,
                503,
                504,
                505,
                506,
                507,
                508,
                510,
                511,
            ],
            "up": [
                100,
                101,
                102,
                200,
                201,
                202,
                203,
                204,
                205,
                206,
                207,
                208,
                226,
                429,
            ],
        },
        "self_managed": False,
    },
    "links": {
        # Keep this for the sake of the tests - and future reference.
        "example": "https://example.org",
    },
    "lookup": {
        "dns": True,
        "http_status_code": True,
        "netinfo": True,
        "reputation": False,
        "special": True,
        "timeout": 5,
        "whois": True,
        "platform": False,
    },
    "proxy": {"global": {"http": None, "https": None}, "rules": []},
    "share_logs": False,
    "user_agent": {"browser": "chrome", "custom": None, "platform": "linux"},
    "verify_ssl_certificate": False,
}
