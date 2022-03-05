"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Welcome to PyFunceble!

PyFunceble  is the little sister of Funceble
(https://github.com/funilrys/funceble) which was archived on 13th March
2018. In March 2018, because Funceble was starting to become a huge unmanageable
script, I - Nissar Chababy aka `@funilrys`_ - decided to make it a Python tool
for the purpose of extending my Python knowledge. It was meant for my own use case.

Back then, my problem was that I didn't want to download a huge hosts file
knowing that most of the entries do not exist anymore. That's how Py-Funceble
started.

My objective - now - through this tool is to provide a tool and a Python API
which helps the world test the availability of domains, IPs and URL through
the gathering and interpretation of information from existing tools or
protocols like WHOIS records, DNS lookup, or even HTTP status codes.

The base of this tool was my idea.
But as with many Open Source (related) projects, communities or
individuals, we evolve with the people we meet, exchange with or just discuss
with privately. PyFunceble was and is still not an exception to that.

My main idea was to check the availability of domains in hosts files.
But 3 years later, PyFunceble is now capable of a lot including:

- The testing of domains, IPs, and URLs.
- The checking of the syntax or reputation of a domain, IPs, and URLs.
- The decoding of AdBlock filters, RPZ records, or plain files before a test
  from the CLI.

PyFunceble evolved and will probably continue to evolve with the time
and the people using it.

In June 2020, The PyFunceble-dev PyPI package - which gets everything as
soon as possible compared to the PyFunceble (stable) package - reached 1 million
total downloads. I never noticed it until I was reached by someone informing me
of it. But, I was shocked.

I never thought that something I built from A to Z in my free time will ever
reach that point.
I was thankful to that nice person for informing me of it. But at the same time
concerned about PyFunceble and how it will evolve. That's why I started the
development of PyFunceble 4.0.0. My idea as I was refactoring it was to provide
a better Python API and implementation of my core ideas along with a better
incorporation and extension capability.
Indeed, in the last few years, I was so much obsessed with the CLI that I
really never wrote each component individually. They were all dependent - if
not part of - the CLI. With 4.0.0, you can now import one of the components
of PyFunceble and start straight away. No real need to play with the
configuration unless you want something very specific.
That's how I see the future of PyFunceble.

As of today, PyFunceble is running actively - if not daily - within several
servers, laptops, PCs, and Raspberry Pis. It is even used - thanks to our
auto continue dataset and component - with CI engines like GitHub Action,
Travis CI, and GitLab CI.

PyFunceble is my tool. But it is indirectly also become yours.
Therefore, I invite you to let me know how you use PyFunceble or simply open a
discussion - or join an existing one - about anything you do with PyFunceble.
But also anything that you - would - like - or dislike - in PyFunceble.

Happy testing with PyFunceble!

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2022 Nissar Chababy

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

import os
import platform
import re
from typing import List

import setuptools


def is_win_platform():
    """
    Checks if the current platform is Windows.
    """

    WIN_PLATFORMS = ["windows", "cygwin", "cygwin_nt-10.0"]

    return platform.system().lower() in WIN_PLATFORMS


def get_requirements(*, mode="standard"):
    """
    This function extract all requirements from requirements.txt.
    """

    mode2files = {
        "standard": ["requirements.txt"],
        "dev": ["requirements.dev.txt"],
        "docs": ["requirements.docs.txt"],
        "test": ["requirements.test.txt"],
    }

    if is_win_platform():
        for mode, files in mode2files.items():
            new_files = set()

            for file in files:
                win_file = file.replace(".txt", ".win.txt")

                if os.path.isfile(win_file):
                    new_files.add(win_file)
                else:
                    new_files.add(file)

            mode2files[mode] = list(new_files)

    mode2files["full"] = [y for x in mode2files.values() for y in x]

    result = set()

    for file in mode2files[mode]:
        with open(file, "r", encoding="utf-8") as file_stream:
            for line in file_stream:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "#" in line:
                    line = line[: line.find("#")].strip()

                if not line:
                    continue

                result.add(line)

    return list(result)


def get_version():
    """
    This function will extract the version from PyFunceble/__init__.py
    """

    to_match = re.compile(r'PROJECT_VERSION.*=\s+"(.*)"')

    try:
        extracted = to_match.findall(
            open("PyFunceble/storage.py", encoding="utf-8").read()
        )[0]

    except FileNotFoundError:  # pragma: no cover
        extracted = to_match.findall(
            open("../PyFunceble/storage.py", encoding="utf-8").read()
        )[0]

    return extracted[: extracted.rfind(".")]


def get_long_description():  # pragma: no cover
    """
    This function return the long description.
    """

    return open("README.rst", encoding="utf-8").read()


if __name__ == "__main__":
    setuptools.setup(
        name="PyFunceble-dev",
        version=get_version(),
        python_requires=">=3.6, <4",
        install_requires=get_requirements(mode="standard"),
        extras_require={
            "docs": get_requirements(mode="docs"),
            "dev": get_requirements(mode="dev"),
            "test": get_requirements(mode="test"),
            "full": get_requirements(mode="full"),
        },
        description="The tool to check the availability or syntax of domain, IP or URL.",
        long_description=get_long_description(),
        author="funilrys",
        author_email="contact@funilrys.com",
        license="Apache 2.0",
        url="https://github.com/funilrys/PyFunceble",
        project_urls={
            "Documentation": "https://pyfunceble.readthedocs.io/en/dev/",
            "Funding": "https://github.com/sponsors/funilrys",
            "Source": "https://github.com/funilrys/PyFunceble/tree/dev",
            "Tracker": "https://github.com/funilrys/PyFunceble/issues",
        },
        platforms=["any"],
        packages=setuptools.find_packages(
            exclude=("*.tests", "*.tests.*", "tests.*", "tests")
        ),
        include_package_data=True,
        keywords=[
            "PyFunceble",
            "syntax-checker",
            "reputation-checker",
            "availability-checker",
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
                "PyFunceble=PyFunceble.cli.entry_points.pyfunceble.cli:tool",
                "pyfunceble=PyFunceble.cli.entry_points.pyfunceble.cli:tool",
                "public-suffix-pyfunceble=PyFunceble.cli.entry_points.public_suffix:generator",
                "iana-pyfunceble=PyFunceble.cli.entry_points.iana:generator",
                "production-pyfunceble=PyFunceble.cli.entry_points.production:producer",
                "clean-pyfunceble=PyFunceble.cli.entry_points.clean:cleaner",
            ]
        },
    )
