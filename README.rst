.. image:: https://raw.githubusercontent.com/PyFunceble/logo/master/Green/HD/RM.png

The tool to check the availability or syntax of domain, IP or URL
-----------------------------------------------------------------

.. image:: https://img.shields.io/badge/code%20style-black-000000.png
    :target: https://github.com/ambv/black
.. image:: https://api.travis-ci.com/funilrys/PyFunceble.png?branch=master
    :target: https://travis-ci.com/funilrys/PyFunceble
.. image:: https://coveralls.io/repos/github/funilrys/PyFunceble/badge.png?branch=master
    :target: https://coveralls.io/github/funilrys/PyFunceble?branch=master
.. image:: https://api.codacy.com/project/badge/Grade/3f7684ffe6fc44d781ca0f26e0221928
    :target: https://www.codacy.com/app/funilrys/PyFunceble?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=funilrys/PyFunceble&amp;utm_campaign=Badge_Grade
.. image:: https://img.shields.io/github/license/funilrys/PyFunceble.png
    :target: https://github.com/funilrys/PyFunceble/blob/master/LICENSE
.. image:: https://img.shields.io/pypi/v/pyfunceble.png
    :target: https://pypi.org/project/pyfunceble
.. image:: https://img.shields.io/github/issues/funilrys/PyFunceble.png
    :target: https://github.com/funilrys/PyFunceble/issues
.. image:: https://pepy.tech/badge/pyfunceble
    :target: https://pepy.tech/project/pyfunceble
.. image:: https://pepy.tech/badge/pyfunceble/month
    :target: https://pepy.tech/project/pyfunceble
.. image:: https://pepy.tech/badge/pyfunceble/week
    :target: https://pepy.tech/project/pyfunceble

PyFunceble is the little sister of `Funceble`_ which was archived on 13th March 2018.

Its main objective is to provide the availability of domains, IPs and since recently URL by generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

PyFunceble is currently running actively and daily with the help of Travis CI under 60+ repositories. It is used to clean or test the availability of data which are present in hosts files, list of IP, list of domains, block lists or even AdBlock filter lists.

PyFunceble provides some useful features for continuous testing.

As an example, its auto-continue system coupled with its auto-save system allows it to run nice and smoothly under Travis CI without even reaching Travis CI time restriction. In the other side, its internal inactive database system let :code:`INACTIVE` and :code:`INVALID` caught domains, IPs or URLs being automatically retested over time on next run.

___________________________________________

Documentation as the place to be!
---------------------------------

Want to know more about **PyFunceble**?
We invite you to read the documentation at https://pyfunceble.readthedocs.io/en/master/!

Want a local copy? We get you covered!

Simply run the following and enjoy the documentation!

::

    $ cd docs/
    $ make html
    $ palemoon _build/html/index.html # palemoon or whatever browser you use.

___________________________________________

What can PyFunceble do?
-----------------------

- Test the availability of a domain.
- Test the availability of an IPv4.
- Test the availability of an IPv6.
- Test the availability of a URL.
- Test the availability of a domain/DNS name in a private or local network.
- Test the availability of an IPv4 in a private or local network.
- Test the availability of an IPv6 in a private or local network.
- Test the availability of a URL in a private or local network.
- Test the syntax of a domain.
- Test the syntax of an IPv4.
- Test the syntax of an IPv6.
- Test the syntax of a URL.
- Test the AlienVault's reputation of an IPv4.
- Test of domain or IP which are present into an Adblock formatted file.
- Test from a given raw link.
- Test using multiprocessing (from CLI only).
- Save test result(s) in file(s) (hosts file, plain text and/or JSON format).
- Save test result in a SQL database.
- Show test result(s) on screen.
- Show percentage of each status (:code:`ACTIVE`, :code:`INACTIVE`,
  :code:`INVALID`)
- Sort outputs hierarchically.
- "Mining" of domain or IP which are related to the tested element.
- Auto-continuation of tests in case of system crash or script stop.
- Filtering of a file content.

  - This feature will let us for example test all blogspot domain of the given
    file no matter the content of the file.

- Set the user-agent to use for the tests.
- Give some analytic depending of the HTTP status code (:code:`ACTIVE`,
  :code:`POTENTIALLY_ACTIVE`, :code:`POTENTIALLY_INACTIVE`, :code:`SUSPICIOUS`).
- Retest overtime of :code:`INACTIVE` and :code:`INVALID` domains.
- Print the execution time on screen and file.
- Customisation of the different option via command-line arguments or
  configuration file.
- Continuous tests under Travis CI or GitLab CI/CI

  - ... with the help of an auto saving and database system.
  - Set the branch to push the result to. For the autosaving system.
  - Set the minimal time before we autosave in order to avoid CI/CD limitation.
  - Set a command to execute at the end of the test.
  - Set the commit message for the autosaving system.

- ... and a lot more!

.. image:: https://github.com/PyFunceble/gifs/raw/master/domain.gif
    :target: https://github.com/PyFunceble/gifs/raw/master/domain.gif

Please report to the `documentation for more GIF`_.

___________________________________________

Supporting the project
----------------------


`PyFunceble`_, `Dead-Hosts`_, and all other analog projects are powered by free time and a lot of coffee!

This project helps you and/or you like it?

GitHub Sponsor
""""""""""""""
`@funilrys`_ is part of the GitHub Sponsor program!

*GitHub will match all donation for the coming months!*

.. image:: https://github.com/PyFunceble/logo/raw/master/pyfunceble_github.png
    :target: https://github.com/sponsors/funilrys
    :height: 70px

`Sponsor me`_!

Ko-Fi
"""""

Don't want to use the GitHub Sponsor program ?
Single donation are welcome too!

.. image:: https://az743702.vo.msecnd.net/cdn/kofi3.png
    :target: https://ko-fi.com/V7V3EH2Y
    :height: 70px

`Buy me a coffee`_!

___________________________________________

Contributors
------------

Thanks to those awesome peoples for their awesome and crazy idea(s), contribution(s) and or issue report which made or make `PyFunceble`_ a better tool.

::

    _______ _                 _          _                              _
   |__   __| |               | |        | |                            | |
      | |  | |__   __ _ _ __ | | _____  | |_ ___    _   _  ___  _   _  | |
      | |  | '_ \ / _` | '_ \| |/ / __| | __/ _ \  | | | |/ _ \| | | | | |
      | |  | | | | (_| | | | |   <\__ \ | || (_) | | |_| | (_) | |_| | |_|
      |_|  |_| |_|\__,_|_| |_|_|\_\___/  \__\___/   \__, |\___/ \__,_| (_)
                                                     __/ |
                                                    |___/

-   Daniel - `@dnmTX`_
-   hawkeye116477 - `@hawkeye116477`_
-   Imre Kristoffer Eilertsen - `@DandelionSprout`_
-   jawz101 - `@jawz101`_
-   kowith337 - `@kowith337`_
-   Mitchell Krog - `@mitchellkrogza`_
-   NeolithEra - `@NeolithEra`_
-   Odyseus - `@Odyseus`_
-   opav - `@opav`_
-   Reza Rizqullah - `@ybreza`_
-   sjhgvr - `@sjhgvr`_
-   ScriptTiger - `@ScriptTiger`_
-   speedmann - `@speedmann`_
-   spirillen - `@spirillen`_
-   The Unknown - `@AnonymousPoster`_
-   WaLLy3K - `@WaLLy3K`_
-   xxcriticxx - `@xxcriticxx`_
-   ZeroDot1 - `@ZeroDot1`_

___________________________________________

Special Thanks
--------------

Thanks to those awesome organization(s), tool(s) and or people(s) for

*   Their awesome documentation
*   Their awesome repository
*   Their awesome tool/software/source code
*   Their breaking reports
*   Their contributions
*   Their current work/purpose
*   Their promotion of Py-Funceble
*   Their support
*   Their testings reports

which helped and/or still help me build, test and or make `PyFunceble`_ a better tool.

::

     _______ _                 _          _                              _
    |__   __| |               | |        | |                            | |
       | |  | |__   __ _ _ __ | | _____  | |_ ___    _   _  ___  _   _  | |
       | |  | '_ \ / _` | '_ \| |/ / __| | __/ _ \  | | | |/ _ \| | | | | |
       | |  | | | | (_| | | | |   <\__ \ | || (_) | | |_| | (_) | |_| | |_|
       |_|  |_| |_|\__,_|_| |_|_|\_\___/  \__\___/   \__, |\___/ \__,_| (_)
                                                      __/ |
                                                     |___/

-   Adam Warner - `@PromoFaux`_
-   Adblock Plus - `@adblockplus`_
-   asciinema - `@asciinema`_
-   Bob Halley - `@rthalley`_ (`DNSPython`_)
-   Chris Griffith - `@cdgriffith`_ (`Box`_)
-   Daniel - `@dnmTX`_
-   Jonathan Hartley - `@tartley`_ (`colorama`_)
-   `IANA`_ - `ICANN`_ (`Root Zone Database`_)
-   Kenneth Reitz - `@kennethreitz`_ (`requests`_)
-   Mitchell Krog - `@mitchellkrogza`_
-   Mohammad Fares - `@faressoft`_ (`Terminalizer`_)
-   Pi-Hole - `@pi-hole`_
-   Public Suffix List - `@publicsuffix`_
-   Reza Rizqullah - `@ybreza`_
-   Saurabh Kumar - `@theskumar`_ (`python-dotenv`_)
-   ScriptTiger - `@ScriptTiger`_
-   SMed79 - `@SMed79`_
-   spirillen - `@spirillen`_
-   The YAML Project - `@yaml`_ (`pyyaml`_)
-   `yWorks`_ - (`yEd Graph Editor`_)

___________________________________________

License
-------
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

.. _Box: https://github.com/cdgriffith/Box
.. _colorama: https://github.com/tartley/colorama
.. _Dead-Hosts: https://github.com/dead-hosts
.. _DNSPython: https://github.com/rthalley/dnspython
.. _Funceble: https://github.com/funilrys/funceble
.. _IANA: https://www.iana.org/
.. _ICANN: https://www.icann.org/
.. _PyFunceble: https://github.com/funilrys/PyFunceble
.. _python-dotenv: https://github.com/theskumar/python-dotenv
.. _pyyaml: https://github.com/yaml/pyyaml
.. _requests: https://github.com/kennethreitz/requests
.. _Root Zone Database: https://www.iana.org/domains/root/db
.. _Terminalizer: https://github.com/faressoft/terminalizer
.. _yEd Graph Editor: https://www.yworks.com/products/yed
.. _yWorks: https://www.yworks.com/company

.. _@adblockplus: https://github.com/adblockplus
.. _@AnonymousPoster: https://github.com/AnonymousPoster
.. _@asciinema: https://github.com/asciinema
.. _@cdgriffith: https://github.com/cdgriffith
.. _@DandelionSprout: https://github.com/DandelionSprout
.. _@dnmTX: https://github.com/dnmTX
.. _@faressoft: https://github.com/faressoft
.. _@funilrys: https://github.com/funilrys
.. _@hawkeye116477: https://github.com/hawkeye116477
.. _@jawz101: https://github.com/jawz101
.. _@kennethreitz: https://github.com/kennethreitz
.. _@kowith337: https://github.com/kowith337
.. _@mitchellkrogza: https://github.com/mitchellkrogza
.. _@NeolithEra: https://github.com/NeolithEra
.. _@Odyseus: https://github.com/Odyseus
.. _@opav: https://github.com/opav
.. _@pi-hole: https://github.com/pi-hole/pi-hole
.. _@PromoFaux: https://github.com/PromoFaux
.. _@publicsuffix: https://github.com/publicsuffix
.. _@rthalley: https://github.com/rthalley
.. _@ScriptTiger: https://github.com/ScriptTiger
.. _@sjhgvr: https://github.com/sjhgvr
.. _@SMed79: https://github.com/SMed79
.. _@speedmann: https://github.com/speedmann
.. _@spirillen: https://github.com/spirillen
.. _@tartley: https://github.com/tartley
.. _@theskumar: https://github.com/theskumar
.. _@Wally3K: https://github.com/WaLLy3K
.. _@xxcriticxx: https://github.com/xxcriticxx
.. _@yaml: https://github.com/yaml
.. _@ybreza: https://github.com/ybreza
.. _@ZeroDot1: https://github.com/ZeroDot1

.. _documentation for more GIF: https://pyfunceble.readthedocs.io/en/master/in-action.html
.. _Sponsor me: https://github.com/sponsors/funilrys
.. _Buy me a coffee: https://ko-fi.com/V7V3EH2Y
