# pylint:disable=line-too-long
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
    https://pyfunceble.readthedocs.io/en/master/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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
# pylint: enable=line-too-long

VALID_DOMAINS = [
    "_hello_.abuse.co.za.",
    "_hello_.abuse.co.za",
    "_hello_world_.abuse.co.za.",
    "_hello_world_.abuse.co.za",
    "_hello_world_.hello.eu.com.",
    "_hello_world_.hello.eu.com",
    "_hello-beautiful-world_.wold.eu.com.",
    "_hello-beautiful-world_.wold.eu.com",
    "_hello-world.abuse.co.za.",
    "_hello-world.abuse.co.za",
    "_hello._world.abuse.co.za.",
    "_hello._world.abuse.co.za",
    "_hello.abuse.co.za.",
    "_hello.abuse.co.za",
    "_world_.hello.eu.com.",
    "_world_.hello.eu.com",
    "_world.hello.eu.com.",
    "_world.hello.eu.com",
    "hello_.world.eu.com.",
    "hello_.world.eu.com",
    "hello_world.abuse.co.za.",
    "hello_world.abuse.co.za",
    "hello_world.world.com.",
    "hello_world.world.com",
    "hello_world.world.hello.com.",
    "hello_world.world.hello.com",
    "hello---world.com.",
    "hello---world.com",
    "hello-.abuse.co.za.",
    "hello-.abuse.co.za",
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
]

NOT_VALID_DOMAINS = [
    "_world._hello.eu.com",
    "_world.hello_.eu.com",
    "-hello-.abuse.co.za",
    "-hello-world_.abuse.co.za",
    "-hello-world_all-mine_.hello.eu.com",
    "-hello.abuse.co.za",
    "-hello.world",
    "-world.hello",
    "..",
    ".",
    "bịllogram.com",
    "bittréẋ.com",
    "coinbȧse.com",
    "cryptopiạ.com",
    "cṙyptopia.com",
    "hello_world_.com",
    "hello_world.com",
    "hello-.world",
    "hello-world",
    "hello.-hello-world_.abuse.co.za",
    "hello@world.com",
    "httpWd",
    "test.-hello-world_all-mine_.abuse.co.za",
    "world_hello.com",
    "world-.hello",
    "world-hello",
    "world.hello:80",
    "world@hello.com",
    "hello_world.co.za",
]

VALID_SUBDOMAINS = [
    "hello_world.world.com",
    "hello_world.world.hello.com",
    "hello.world_hello.world.com",
    "hello.world.hello.com",
    "hello_.world.eu.com",
    "_world.hello.eu.com",
    "_world_.hello.eu.com",
    "_hello-beautiful-world_.wold.eu.com",
    "_hello_world_.hello.eu.com",
    "_hello.abuse.co.za",
    "_hello_.abuse.co.za",
    "_hello._world.abuse.co.za",
    "_hello-world.abuse.co.za",
    "_hello_world_.abuse.co.za",
    "hello_world.abuse.co.za",
    "hello-.abuse.co.za",
    "hello.world.onion",
]

NOT_VALID_SUBDOMAINS = [
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
]

VALID_IPV4 = ["15.47.85.65", "45.66.255.240", "255.45.65.0/24"]

VALID_IPV6 = [
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

NOT_VALID_IPV4 = ["google.com", "287.468.45.26", "245.85.69.17:8081"]

NOT_VALID_IPV6 = [
    "google.com",
    "287.468.45.26",
    "2001:db8::/4839",
    "2001:::",
    "2001:db8:85a3:8d3:1319:8a2e:370:7348f",
    "2001:db8:85a3:8d3:1319:8a2e:370:7348/129",
]

VALID_IPV4_RANGES = ["255.45.65.0/24", "255.45.65.6/18"]

VALID_IPV6_RANGES = [
    "2001:db8::/128",
    "2001:db8:1234::/48",
    "2001:db8:a::/64",
    "2001:db8:a::123/64",
]

NOT_VALID_IPV4_RANGES = ["15.47.85.65", "45.66.255.240", "github.com"]

NOT_VALID_IPV6_RANGES = ["2001:db8::/129", "github.com", "2001:db8:a::"]

RESERVED_IPV4 = [
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

RESERVED_IPV6 = [
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
    "2001:20::",
    "2001:2f:ffff:ffff:ffff:ffff:ffff:ffff",
    "2001:db8::",
    "2001:db8:ffff:ffff:ffff:ffff:ffff:ffff",
    "fc00::",
    "fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
    "fe80::",
    "febf:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
    "ff00::",
    "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
]

NOT_RESERVED_IPV4 = ["hello.world", "::1", "45.34.29.15"]

NOT_RESERVED_IPV6 = [
    "2001:db8::/128",
    "hello.world",
    "2001:db8:1234::/48",
    "2001:db8:a::/64",
    "2001:db8:a::123/64",
    "github.com",
]
