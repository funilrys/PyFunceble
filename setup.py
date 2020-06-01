"""
The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on 13th March 2018.

Its main objective is to provide the availability of domains, IPs and since recently
URL by generating an accurate result based on results from WHOIS, NSLOOKUP and
HTTP status codes.

PyFunceble is currently running actively and daily with the help of Travis CI under
60+ repositories. It is used to clean or test the availability of data which are
present in hosts files, list of IP, list of domains, block lists or even AdBlock
filter lists.

PyFunceble provides some useful features for continuous testing.

As an example, its auto-continue system coupled with its auto-save system allows
it to run nice and smoothly under Travis CI without even reaching Travis CI time
restriction. In the other side, its internal inactive database system
let :code:`INACTIVE` and :code:`INVALID` caught domains, IPs or URLs being
automatically retested over time on next run.


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

from re import compile as comp
from unittest import TestLoader

from setuptools import setup


def _test_suite():
    """
    This function will discover and run all the tests.
    """

    test_loader = TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    return test_suite


def _get_requirements():
    """
    This function extract all requirements from requirements.txt.
    """

    with open("requirements.txt") as file:
        requirements = file.read().splitlines()

    return requirements


def _get_version():
    """
    This function will extract the version from PyFunceble/__init__.py
    """

    to_match = comp(r'VERSION\s=\s"(.*)"\n')

    try:
        extracted = to_match.findall(
            open("PyFunceble/abstracts/package.py", encoding="utf-8").read()
        )[0]
    except FileNotFoundError:  # pragma: no cover
        extracted = to_match.findall(
            open("../PyFunceble/abstracts/package.py", encoding="utf-8").read()
        )[0]

    return ".".join([x for x in extracted.split(".") if x.isdigit()])


def _get_long_description():  # pragma: no cover
    """
    This function return the long description.
    """

    return open("README.rst", encoding="utf-8").read()


if __name__ == "__main__":
    setup(
        name="PyFunceble-dev",
        version=_get_version(),
        python_requires=">=3.6, <4",
        install_requires=_get_requirements(),
        description="The tool to check the availability or syntax of domains, IPv4, IPv6 or URL.",
        long_description=_get_long_description(),
        author="funilrys",
        author_email="contact@funilrys.com",
        license="Apache 2.0",
        url="https://github.com/funilrys/PyFunceble",
        platforms=["any"],
        packages=[
            "PyFunceble.abstracts",
            "PyFunceble.cli",
            "PyFunceble.config",
            "PyFunceble.converter",
            "PyFunceble.core",
            "PyFunceble.database",
            "PyFunceble.downloader",
            "PyFunceble.engine.ci",
            "PyFunceble.engine",
            "PyFunceble.extractor",
            "PyFunceble.helpers",
            "PyFunceble.lookup",
            "PyFunceble.output",
            "PyFunceble.status.availability",
            "PyFunceble.status.reputation",
            "PyFunceble.status.syntax",
            "PyFunceble.status",
            "PyFunceble",
        ],
        keywords=[
            "availability",
            "dns",
            "domain",
            "IP",
            "IPv4",
            "IPv6",
            "nslookup",
            "PyFunceble",
            "Python",
            "syntax-checker",
            "syntax",
            "WHOIS",
        ],
        classifiers=[
            "Environment :: Console",
            "Topic :: Internet",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved",
        ],
        test_suite="setup._test_suite",
        entry_points={
            "console_scripts": [
                "PyFunceble=PyFunceble.cli:tool",
                "pyfunceble=PyFunceble.cli:tool",
            ]
        },
    )
