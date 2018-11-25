"""
The tool to check the availability or syntax of domains, IPv4 or URL.

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
    https://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Contributors:
    http://pyfunceble.readthedocs.io/en/dev/special-thanks.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io

Project homepage:
    https://funilrys.github.io/PyFunceble/

License:
::


    MIT License

    Copyright (c) 2017-2018 Nissar Chababy

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
    extracted = to_match.findall(
        open("PyFunceble/__init__.py", encoding="utf-8").read()
    )[0]

    return ".".join(list(filter(lambda x: x.isdigit(), extracted.split("."))))


def _get_long_description():  # pragma: no cover
    """
    This function return the long description.
    """

    return open("README.rst", encoding="utf-8").read()


if __name__ == "__main__":
    setup(
        name="PyFunceble-dev",
        version=_get_version(),
        install_requires=_get_requirements(),
        description="The tool to check the availability or syntax of domains, IPv4 or URL.",
        long_description=_get_long_description(),
        author="funilrys",
        author_email="contact@funilrys.com",
        license="https://git.io/vh1mP",
        url="https://github.com/funilrys/PyFunceble",
        platforms=["any"],
        packages=["PyFunceble"],
        keywords=[
            "Python",
            "domain",
            "IP",
            "availability",
            "syntax",
            "syntax-checker",
            "PyFunceble",
            "WHOIS",
            "nslookup",
        ],
        classifiers=[
            "Environment :: Console",
            "Topic :: Internet",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ],
        test_suite="setup._test_suite",
        entry_points={
            "console_scripts": [
                "PyFunceble=PyFunceble:_command_line",
                "pyfunceble=PyFunceble:_command_line",
            ]
        },
    )
