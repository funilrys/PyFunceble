.. image:: https://raw.githubusercontent.com/funilrys/PyFunceble/dev/.assets/logo/RM.png

The tool to check the availability of domains, IPv4 or URL
----------------------------------------------------------

.. image:: https://travis-ci.com/funilrys/PyFunceble.svg?branch=dev
    :target: https://travis-ci.com/funilrys/PyFunceble
.. image:: https://coveralls.io/repos/github/funilrys/PyFunceble/badge.svg?branch=dev
    :target: https://coveralls.io/github/funilrys/PyFunceble?branch=dev
.. image:: https://img.shields.io/github/license/funilrys/PyFunceble.svg
    :target: https://github.com/funilrys/PyFunceble/blob/dev/LICENSE
.. image:: https://img.shields.io/github/release/funilrys/PyFunceble/all.svg
    :target: https://github.com/funilrys/PyFunceble/releases/latest
.. image:: https://img.shields.io/github/issues/funilrys/PyFunceble.svg
    :target: https://github.com/funilrys/PyFunceble/issues
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

PyFunceble is the little sister of `Funceble`_ which was archived on 13th March, 2018.

Its main objective is to get and/or return the availability of domains and IPs by generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

PyFunceble is running actively and daily with the help of Travis CI under 60+ repositories. It is used to clean or test the availability of data which are present in hosts files, list of IP, list of domains, blocklists or even AdBlock filter lists. 

Indeed, it is possible because PyFunceble generates a list of all `ACTIVE` domains or IPs but in the same time, it creates by default a database of the `INACTIVE` domains or IPs so it can retest them overtime automatically at the next execution.

___________________________________________

Documentation as place to be!
-----------------------------

Want to know more about **PyFunceble**?
We invite you to read the documenation at https://pyfunceble.readthedocs.io!

Want a local copy ? We get you covered!

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
- Test of the availability of a URL.
- Test of the availability of a local domain.
- Test of the availability of a local IPv4.
- Test of the availability of a local URL.
- Test of domain or IP which are present into an Adblock formatted file.
- Test from a given raw link.
- Save test result(s) on file(s) (in several format).
- Show test result(s) on screen.
- Show percentage of each status (:code:`ACTIVE`, :code:`INACTIVE`, :code:`INVALID`)
- Sort outputs hierarchicaly.
- "Mining" of domain or IP which are related to the tested element.
- Auto-continuation of tests in case of system crash or script stop.
- Filtering of a file content. This feature will let us for example test all blogspot domain of the given file no matter the content of the file.
- Set the user-agent to use for the tests.
- Give some analytic depending of the HTTP status code (:code:`ACTIVE`, :code:`POTENTIALLY_ACTIVE`, :code:`POTENTIALLY_INACTIVE`, :code:`SUSPICIOUS`).
- Retest overtime of :code:`INACTIVE` and :code:`INVALID` domains.
- Print the execution time on screen and file.
- Customisation of the different option via command-line arguments or configuration file.
- Continuous tests under Travis CI with the help of an autosaving and database system.
    - Set branch to push the result to for the autosaving system.
    - Set the minimal time before we autosave in order to avoid Travis CI limitation.
    - Set a command to execute at the end of the test.
    - Set the commit message for the autosaving system.
- ... and a lot more!

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

-   dnmTX - `@dnmTX`_
-   jawz101 - `@jawz101`_
-   Mitchell Krog - `@mitchellkrogza`_
-   Odyseus - `@Odyseus`_
-   Reza Rizqullah - `@ybreza`_
-   WaLLy3K - `@WaLLy3K`_
-   xxcriticxx - `@xxcriticxx`_

___________________________________________

Special Thanks
--------------

Thanks to those awesome organization(s) and people(s) for

*   Their awesome repository
*   Their awesome documentation
*   Their breaking reports
*   Their contributions
*   Their current work
*   Their promotion of Funceble and (or indirectly) PyFunceble
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
-   Mitchell Krog - `@mitchellkrogza`_
-   Pi-Hole - `@pi-hole`_
-   Reza Rizqullah - `@ybreza`_
-   SMed79 - `@SMed79`_

___________________________________________

License
-------
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

.. _Funceble: https://github.com/funilrys/funceble
.. _PyFunceble: https://github.com/funilrys/PyFunceble
.. _Dead-Hosts: https://github.com/dead-hosts

.. _@adblockplus: https://github.com/adblockplus
.. _@dnmTX: https://github.com/dnmTX
.. _@jawz101: https://github.com/jawz101
.. _@mitchellkrogza: https://github.com/mitchellkrogza
.. _@Odyseus: https://github.com/Odyseus
.. _@pi-hole: https://github.com/pi-hole/pi-hole
.. _@PromoFaux: https://github.com/PromoFaux
.. _@SMed79: https://github.com/SMed79
.. _@ybreza: https://github.com/ybreza
.. _@Wally3K: https://github.com/WaLLy3K
.. _@xxcriticxx: https://github.com/xxcriticxx