.. image:: https://raw.githubusercontent.com/funilrys/PyFunceble/dev/.assets/logo/RM.png

The tool to check domains or IP availability
--------------------------------------------

.. image:: https://travis-ci.com/funilrys/PyFunceble.svg?branch=dev
    :target: https://travis-ci.com/funilrys/PyFunceble
.. image:: https://coveralls.io/repos/github/funilrys/PyFunceble/badge.svg?branch=dev
    :target: https://coveralls.io/github/funilrys/PyFunceble?branch=dev
.. image:: https://img.shields.io/github/license/funilrys/PyFunceble.svg
    :target: https://github.com/funilrys/PyFunceble/blob/dev/LICENSE
.. image:: https://img.shields.io/github/release/funilrys/PyFunceble/all.svg
    :target: https://github.com/funilrys/PyFunceble/releases/latest
.. image:: https://img.shields.io/github/release/funilrys/PyFunceble.svg
    :target: https://github.com/funilrys/PyFunceble/releases/latest
.. image:: https://img.shields.io/github/issues/funilrys/PyFunceble.svg
    :target: https://github.com/funilrys/PyFunceble/issues
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

PyFunceble is the little sister of `Funceble`_ which was archived on 13th March, 2018.

Its main objective is to get and the return domains and IPs availability by generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

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

* Test of the availability of a domain.
* Test of the availability of an IPv4.
* Test of the availability of a URL.
* Test of domain or IP which are present into an Adblock formatted file.
* Test from a given raw link.
* Save test result(s) on file(s) (in several format).
* Show test result(s) on screen.
* Show percentage of each status (:code:`ACTIVE`,:code:`INACTIVE`,:code:`INVALID`)
* Auto-continuation of tests in case of system crash or script stop.
* Filtering of a file content. This feature will let us for example test all Blogspot domain of the given file no matter the content of the file.
* Customisation of the different option via command-line arguments or configuration file.
* Set the user-agent to use for the tests.
* Continuous tests under Travis CI with the help of an autosaving and database system.
    * Set branch to push the result to for the autosaving system.
    * Set the minimal time before we autosave.
    * Set a command to execute at the end of the test.
    * Set the commit message for the autosaving system
* ... and a lot more!

___________________________________________

Supporting the project
----------------------

`PyFunceble`_, `Dead-Hosts`_, `Funceble`_ and all other analog projects are powered by :coffee:!

This project helps you and or you like it?

.. image:: https://img.shields.io/badge/Help%20me%20out-with%20a%20cup%20of%20%E2%98%95%20-blue.svg
    :target: https://www.paypal.me/funilrys/

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

.. _@dnmTX: https://github.com/dnmTX
.. _@mitchellkrogza: https://github.com/mitchellkrogza
.. _@Odyseus: https://github.com/Odyseus
.. _@pi-hole: https://github.com/pi-hole/pi-hole
.. _@PromoFaux: https://github.com/PromoFaux
.. _@SMed79: https://github.com/SMed79
.. _@ybreza: https://github.com/ybreza
.. _@Wally3K: https://github.com/WaLLy3K
.. _@xxcriticxx: https://github.com/xxcriticxx