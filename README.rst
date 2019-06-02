.. image:: https://raw.githubusercontent.com/PyFunceble/logo/dev/Green/HD/RM.png

The tool to check the availability or syntax of domains, IPv4 or URL
--------------------------------------------------------------------

.. image:: https://api.travis-ci.com/funilrys/PyFunceble.png?branch=dev
    :target: https://travis-ci.com/funilrys/PyFunceble
.. image:: https://coveralls.io/repos/github/funilrys/PyFunceble/badge.png?branch=dev
    :target: https://coveralls.io/github/funilrys/PyFunceble?branch=dev
.. image:: https://api.codacy.com/project/badge/Grade/3f7684ffe6fc44d781ca0f26e0221928
    :target: https://www.codacy.com/app/funilrys/PyFunceble?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=funilrys/PyFunceble&amp;utm_campaign=Badge_Grade
.. image:: https://img.shields.io/github/license/funilrys/PyFunceble.png
    :target: https://github.com/funilrys/PyFunceble/blob/dev/LICENSE
.. image:: https://img.shields.io/github/release/funilrys/PyFunceble/all.png
    :target: https://github.com/funilrys/PyFunceble/releases/latest
.. image:: https://img.shields.io/github/issues/funilrys/PyFunceble.png
    :target: https://github.com/funilrys/PyFunceble/issues
.. image:: https://img.shields.io/badge/code%20style-black-000000.png
    :target: https://github.com/ambv/black

PyFunceble is the little sister of `Funceble`_ which was archived on 13th March 2018.

Its main objective is to provide the availability of domains, IPs and since recently URL by generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

PyFunceble is currently running actively and daily with the help of Travis CI under 60+ repositories. It is used to clean or test the availability of data which are present in hosts files, list of IP, list of domains, block lists or even AdBlock filter lists.

PyFunceble provides some useful features for continuous testing.

As an example, its auto-continue system coupled with its auto-save system allows it to run nice and smoothly under Travis CI without even reaching Travis CI time restriction. In the other side, its internal inactive database system let :code:`INACTIVE` and :code:`INVALID` caught domains, IPs or URLs being automatically retested over time on next run.

___________________________________________

Documentation as the place to be!
---------------------------------

Want to know more about **PyFunceble**?
We invite you to read the documentation at https://pyfunceble.readthedocs.io/en/dev/!

Want a local copy? We get you covered!

Simply run the following and enjoy the documentation!

::

    $ cd docs/
    $ make html
    $ chromium _build/html/index.html # Chromium or whatever browser you use.

___________________________________________

What can PyFunceble do?
-----------------------

- Test of the availability of a domain.
- Test of the availability of an IPv4.
- Test of the availability of an URL.
- Test of the availability of a domain/DNS name in a private or local network.
- Test of the availability of an IPv4 in a private or local network.
- Test of the availability of an URL in a private or local network.
- Test of the syntax of a domain.
- Test of the syntax of an IPv4.
- Test of the syntax of an URL.
- Test of domain or IP which are present into an Adblock formatted file.
- Test from a given raw link.
- Save test result(s) on file(s) (hosts file, plain text and/or JSON format).
- Show test result(s) on screen.
- Show percentage of each status (:code:`ACTIVE`, :code:`INACTIVE`, :code:`INVALID`)
- Sort outputs hierarchically.
- "Mining" of domain or IP which are related to the tested element.
- Auto-continuation of tests in case of system crash or script stop.
- Filtering of a file content.

  - This feature will let us for example test all blogspot domain of the given file no matter the content of the file.

- Set the user-agent to use for the tests.
- Give some analytic depending of the HTTP status code (:code:`ACTIVE`, :code:`POTENTIALLY_ACTIVE`, :code:`POTENTIALLY_INACTIVE`, :code:`SUSPICIOUS`).
- Retest overtime of :code:`INACTIVE` and :code:`INVALID` domains.
- Print the execution time on screen and file.
- Customization of the different option via command-line arguments or configuration file.
- Continuous tests under Travis CI with the help of an auto saving and database system.

  - Set branch to push the result to for the autosaving system.
  - Set the minimal time before we autosave in order to avoid Travis CI limitation.
  - Set a command to execute at the end of the test.
  - Set the commit message for the autosaving system.

- ... and a lot more!

.. image:: https://github.com/PyFunceble/gifs/raw/dev/domain.gif
    :target: https://github.com/PyFunceble/gifs/raw/dev/domain.gif

Please report to the `documentation for more GIF`_.

___________________________________________

Supporting the project
----------------------

`PyFunceble`_, `Dead-Hosts`_, and all other analog projects are powered by free time and a lot of :coffee:!

This project helps you and/or you like it?

.. image:: https://az743702.vo.msecnd.net/cdn/kofi3.png
    :target: https://ko-fi.com/V7V3EH2Y
    :height: 36px

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
-   Mitchell Krog - `@mitchellkrogza`_
-   Odyseus - `@Odyseus`_
-   Reza Rizqullah - `@ybreza`_
-   ScriptTiger - `@ScriptTiger`_
-   speedmann - `@speedmann`_
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
-   Daniel - `@dnmTX`_
-   Bob Halley - `@rthalley`_ (`DNSPython`_)
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
-   The YAML Project - `@yaml`_ (`pyyaml`_)
-   `yWorks`_ - (`yEd Graph Editor`_)

___________________________________________

License
-------
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
.. _@asciinema: https://github.com/asciinema
.. _@DandelionSprout: https://github.com/DandelionSprout
.. _@dnmTX: https://github.com/dnmTX
.. _@faressoft: https://github.com/faressoft
.. _@hawkeye116477: https://github.com/hawkeye116477
.. _@jawz101: https://github.com/jawz101
.. _@kennethreitz: https://github.com/kennethreitz
.. _@mitchellkrogza: https://github.com/mitchellkrogza
.. _@Odyseus: https://github.com/Odyseus
.. _@pi-hole: https://github.com/pi-hole/pi-hole
.. _@PromoFaux: https://github.com/PromoFaux
.. _@publicsuffix: https://github.com/publicsuffix
.. _@rthalley: https://github.com/rthalley
.. _@ScriptTiger: https://github.com/ScriptTiger
.. _@SMed79: https://github.com/SMed79
.. _@speedmann: https://github.com/speedmann
.. _@tartley: https://github.com/tartley
.. _@theskumar: https://github.com/theskumar
.. _@Wally3K: https://github.com/WaLLy3K
.. _@xxcriticxx: https://github.com/xxcriticxx
.. _@yaml: https://github.com/yaml
.. _@ybreza: https://github.com/ybreza
.. _@ZeroDot1: https://github.com/ZeroDot1

.. _documentation for more GIF: https://pyfunceble.readthedocs.io/en/dev/in-action.html