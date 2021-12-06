.. image:: https://raw.githubusercontent.com/PyFunceble/logo/dev/Green/HD/RM.png

The tool to check the availability or syntax of domain, IP or URL
-----------------------------------------------------------------

.. image:: https://img.shields.io/badge/code%20style-black-000000.png
    :target: https://github.com/ambv/black
.. image:: https://coveralls.io/repos/github/funilrys/PyFunceble/badge.png?branch=dev
    :target: https://coveralls.io/github/funilrys/PyFunceble?branch=dev
.. image:: https://img.shields.io/github/license/funilrys/PyFunceble.png
    :target: https://github.com/funilrys/PyFunceble/blob/dev/LICENSE
.. image:: https://img.shields.io/pypi/v/pyfunceble-dev.png
    :target: https://pypi.org/project/pyfunceble-dev
.. image:: https://img.shields.io/github/issues/funilrys/PyFunceble.png
    :target: https://github.com/funilrys/PyFunceble/issues
.. image:: https://pepy.tech/badge/pyfunceble-dev
    :target: https://pepy.tech/project/pyfunceble-dev
.. image:: https://pepy.tech/badge/pyfunceble-dev/month
    :target: https://pepy.tech/project/pyfunceble-dev
.. image:: https://pepy.tech/badge/pyfunceble-dev/week
    :target: https://pepy.tech/project/pyfunceble-dev

**PyFunceble** aims to provide an accurate availability check through the usage
of multiple sources which are for example - to only list them:

- the WHOIS record(s).
- the DNS record(s).
- the HTTP status code.

PyFunceble can be included in your existing project through:

- its standard built-in CLI implementation.
- its `Python API`_.
- the `PyFunceble web-worker`_ project that provides the core functionalities
  of PyFunceble behind a web API.

The PyFunceble CLI can test from a hosts file, a plain list of subjects, an
AdBlock filter list or even an RPZ record.

As of today, PyFunceble is running actively - if not daily - within several
servers, laptops, PCs, and Raspberry Pis. It is even used - thanks to our
auto continue mechanism - with CI engines like GitHub Action, Travis CI, or
GitLab CI.

Happy testing with PyFunceble!

.. image:: https://github.com/PyFunceble/gifs/raw/dev/domain.gif
    :target: https://github.com/PyFunceble/gifs/raw/dev/domain.gif

.. _Python API: https://pyfunceble.readthedocs.io/en/dev/api/index.html
.. _PyFunceble web-worker: https://github.com/pyfunceble/web-worker


___________________________________________

Installation
------------

:code:`pip`
^^^^^^^^^^^

::

    $ pip install --upgrade --pre pyfunceble-dev
    $ pyfunceble --version

:code:`docker`
^^^^^^^^^^^^^^

::

    $ docker pull pyfunceble/pyfunceble-dev
    $ docker run -it pyfunceble/pyfunceble-dev --version

___________________________________________

Documentation as the place to be!
---------------------------------

Want to know more about details **PyFunceble**?
I invite you to read the documentation at https://pyfunceble.readthedocs.io/en/dev/!

Want a local copy? I get you covered!

Simply run the following and enjoy the documentation!

::

    $ pip install --user -r requirements.docs.txt # Install dependencies.
    $ cd docs/
    $ make clean html
    $ palemoon _build/html/index.html # palemoon or whatever browser you use.

.. note::
    You are also invited to submit changes and improvement to the documentation
    through a new Pull Request.

___________________________________________

Supporting the project
----------------------


`PyFunceble`_, `Dead-Hosts`_, and all other analog projects are powered by free
time and a lot of coffee!

This project helps you and/or you like it?

GitHub Sponsor
^^^^^^^^^^^^^^

`@funilrys`_ is part of the GitHub Sponsor program!

.. image:: https://github.com/PyFunceble/logo/raw/master/pyfunceble_github.png
    :target: https://github.com/sponsors/funilrys
    :height: 70px

`Sponsor me`_!

Ko-Fi
^^^^^

Don't want to use the GitHub Sponsor program ?
Single donations are welcome too!

.. image:: https://az743702.vo.msecnd.net/cdn/kofi3.png
    :target: https://ko-fi.com/V7V3EH2Y
    :height: 70px

`Buy me a coffee`_!

___________________________________________

Contributors
------------

Thanks to those awesome peoples for their awesome and crazy idea(s),
contribution(s) and or issue report which made or make `PyFunceble`_ a better tool.

::

    _______ _                 _          _                              _
   |__   __| |               | |        | |                            | |
      | |  | |__   __ _ _ __ | | _____  | |_ ___    _   _  ___  _   _  | |
      | |  | '_ \ / _` | '_ \| |/ / __| | __/ _ \  | | | |/ _ \| | | | | |
      | |  | | | | (_| | | | |   <\__ \ | || (_) | | |_| | (_) | |_| | |_|
      |_|  |_| |_|\__,_|_| |_|_|\_\___/  \__\___/   \__, |\___/ \__,_| (_)
                                                     __/ |
                                                    |___/

-   Avinash Reddy - `@AvinashReddy3108`_
-   Daniel - `@dnmTX`_
-   hawkeye116477 - `@hawkeye116477`_
-   Human Being - `@T145`_
-   Imre Kristoffer Eilertsen - `@DandelionSprout`_
-   jawz101 - `@jawz101`_
-   keczuppp - `@keczuppp`_
-   kowith337 - `@kowith337`_
-   Mitchell Krog - `@mitchellkrogza`_
-   NeolithEra - `@NeolithEra`_
-   Odyseus - `@Odyseus`_
-   opav - `@opav`_
-   Reza Rizqullah - `@ybreza`_
-   rusty-snake - `@rusty-snake`_
-   ScriptTiger - `@ScriptTiger`_
-   sjhgvr - `@sjhgvr`_
-   speedmann - `@speedmann`_
-   spirillen - `@spirillen`_
-   The Unknown - `@AnonymousPoster`_
-   WaLLy3K - `@WaLLy3K`_
-   xxcriticxx - `@xxcriticxx`_
-   Yuki2718 - `@Yuki2718`_
-   Zachinquarantine - `@Zachinquarantine`_
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
-   `Iterative`_ (`shtab`_)
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

.. _Box: https://github.com/cdgriffith/Box
.. _colorama: https://github.com/tartley/colorama
.. _Dead-Hosts: https://github.com/dead-hosts
.. _DNSPython: https://github.com/rthalley/dnspython
.. _Funceble: https://github.com/funilrys/funceble
.. _IANA: https://www.iana.org/
.. _ICANN: https://www.icann.org/
.. _Iterative: https://github.com/iterative
.. _PyFunceble: https://github.com/funilrys/PyFunceble
.. _python-dotenv: https://github.com/theskumar/python-dotenv
.. _pyyaml: https://github.com/yaml/pyyaml
.. _requests: https://github.com/kennethreitz/requests
.. _Root Zone Database: https://www.iana.org/domains/root/db
.. _shtab: https://github.com/iterative/shtab
.. _Terminalizer: https://github.com/faressoft/terminalizer
.. _yEd Graph Editor: https://www.yworks.com/products/yed
.. _yWorks: https://www.yworks.com/company

.. _@adblockplus: https://github.com/adblockplus
.. _@AnonymousPoster: https://www.mypdns.org/p/AnonymousPoster/
.. _@asciinema: https://github.com/asciinema
.. _@AvinashReddy3108: https://github.com/AvinashReddy3108
.. _@cdgriffith: https://github.com/cdgriffith
.. _@DandelionSprout: https://github.com/DandelionSprout
.. _@dnmTX: https://github.com/dnmTX
.. _@faressoft: https://github.com/faressoft
.. _@funilrys: https://github.com/funilrys
.. _@hawkeye116477: https://github.com/hawkeye116477
.. _@jawz101: https://github.com/jawz101
.. _@keczuppp: https://github.com/keczuppp
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
.. _@rusty-snake: https://github.com/rusty-snake
.. _@ScriptTiger: https://github.com/ScriptTiger
.. _@sjhgvr: https://github.com/sjhgvr
.. _@SMed79: https://github.com/SMed79
.. _@speedmann: https://github.com/speedmann
.. _@spirillen: https://www.mypdns.org/p/Spirillen/
.. _@T145: https://github.com/T145
.. _@tartley: https://github.com/tartley
.. _@theskumar: https://github.com/theskumar
.. _@Wally3K: https://github.com/WaLLy3K
.. _@xxcriticxx: https://github.com/xxcriticxx
.. _@yaml: https://github.com/yaml
.. _@ybreza: https://github.com/ybreza
.. _@Yuki2718: https://github.com/Yuki2718
.. _@Zachinquarantine: https://github.com/Zachinquarantine
.. _@ZeroDot1: https://github.com/ZeroDot1

.. _documentation for more GIF: https://pyfunceble.readthedocs.io/en/dev/in-action.html
.. _Sponsor me: https://github.com/sponsors/funilrys
.. _Buy me a coffee: https://ko-fi.com/V7V3EH2Y
