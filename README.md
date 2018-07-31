![](https://raw.githubusercontent.com/funilrys/PyFunceble/master/.assets/logo/RM.png)

## The tool to check domains or IP availability


[![Build Status](https://travis-ci.com/funilrys/PyFunceble.svg?branch=master)](https://travis-ci.com/funilrys/PyFunceble) [![Coverage Status](https://coveralls.io/repos/github/funilrys/PyFunceble/badge.svg?branch=master)](https://coveralls.io/github/funilrys/PyFunceble?branch=master) [![license](https://img.shields.io/github/license/funilrys/PyFunceble.svg)](https://github.com/funilrys/PyFunceble/blob/master/LICENSE) [![GitHub release](https://img.shields.io/github/release/funilrys/PyFunceble.svg)](https://github.com/funilrys/PyFunceble/releases/latest) [![GitHub issues open](https://img.shields.io/github/issues/funilrys/PyFunceble.svg)](https://github.com/funilrys/PyFunceble/issues) [![Code style | Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

PyFunceble is the little sister of [Funceble](https://github.com/funilrys/funceble) which was archived on 13<sup>th</sup> March, 2018.

Its main objective is to get and the return domains and IPs availability by generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

PyFunceble is running actively and daily with the help of Travis CI under 60+ repositories. It is used to clean or test the availability of data which are present in hosts files, list of IP, list of domains, blocklists or even AdBlock filter lists. 

Indeed, it is possible because PyFunceble generates a list of all `ACTIVE` domains or IPs but in the same time, it creates by default a database of the `INACTIVE` domains or IPs so it can retest them overtime automatically at the next execution.

* * *

## Documentation as place to be!

Want to know more about **PyFunceble**? 
We invite you to read the documenation at https://pyfunceble.readthedocs.io!

### Local copy of the documentation

Want a local copy ? We get you covered!

Simply run the following and enjoy the documentation!

```shell
$ cd docs/
$ make html
$ chromium _build/html/index.html # Chromium or whatever browser you use.
```

## Main Features

-   Get the status (`ACTIVE`, `INACTIVE`, `INVALID`) of a given domain or IPv4.
-   Read an existing file and check every domain and IPv5 present into it.
-   Generate a `hosts` file according to the domains statuses.
-   Generate a list of the domain according to their discovered statuses.
-   Show results on screen
-   Save results on file(s)
-   ... and a lot more!

* * *

## Supporting the project

[PyFunceble](https://github.com/funilrys/PyFunceble), [Dead-Hosts](https://github.com/dead-hosts), [Funceble](https://github.com/funilrys/funceble) and all other analog projects are powered by :coffee:!

This project helps you and or you like it?

[![Help me with a cup of coffee](https://img.shields.io/badge/Help%20me%20out-with%20a%20cup%20of%20%E2%98%95%20-blue.svg)](https://www.paypal.me/funilrys/)

* * *

## Contributors

Thanks to those awesome peoples for their awesome and crazy idea(s) and or contribution(s) which made or make **[Funceble](https://github.com/funilrys/funceble)** and (or indirectly) **[PyFunceble](https://github.com/funilrys/PyFunceble)** better.

     _______ _                 _          _                              _
    |__   __| |               | |        | |                            | |
       | |  | |__   __ _ _ __ | | _____  | |_ ___    _   _  ___  _   _  | |
       | |  | '_ \ / _` | '_ \| |/ / __| | __/ _ \  | | | |/ _ \| | | | | |
       | |  | | | | (_| | | | |   <\__ \ | || (_) | | |_| | (_) | |_| | |_|
       |_|  |_| |_|\__,_|_| |_|_|\_\___/  \__\___/   \__, |\___/ \__,_| (_)
                                                      __/ |
                                                     |___/

-   Mitchell Krog - [@mitchellkrogza](https://github.com/mitchellkrogza)
-   Odyseus - [@Odyseus](https://github.com/Odyseus)
-   Reza Rizqullah - [@ybreza](https://github.com/ybreza)
-   WaLLy3K - [@WaLLy3K](https://github.com/WaLLy3K)
-   xxcriticxx - [@xxcriticxx](https://github.com/xxcriticxx)

* * *

## Special Thanks

Thanks to those awesome organization(s) and people(s) for

-   Their awesome repository
-   Their breaking reports
-   Their contributions
-   Their current work
-   Their promotion of Funceble and (or indirectly) PyFunceble
-   Their support
-   Their testings reports

which helped and/or still help me build and or test **[Funceble](https://github.com/funilrys/funceble)** and (or indirectly) **[PyFunceble](https://github.com/funilrys/PyFunceble)**.

     _______ _                 _          _                              _
    |__   __| |               | |        | |                            | |
       | |  | |__   __ _ _ __ | | _____  | |_ ___    _   _  ___  _   _  | |
       | |  | '_ \ / _` | '_ \| |/ / __| | __/ _ \  | | | |/ _ \| | | | | |
       | |  | | | | (_| | | | |   <\__ \ | || (_) | | |_| | (_) | |_| | |_|
       |_|  |_| |_|\__,_|_| |_|_|\_\___/  \__\___/   \__, |\___/ \__,_| (_)
                                                      __/ |
                                                     |___/

-   Adam Warner - [@PromoFaux](https://github.com/PromoFaux)
-   Mitchell Krog - [@mitchellkrogza](https://github.com/mitchellkrogza)
-   Pi-Hole - [@pi-hole](https://github.com/pi-hole/pi-hole)
-   Reza Rizqullah - [@ybreza](https://github.com/ybreza)
-   SMed79 - [@SMed79](https://github.com/SMed79)

* * *

## License

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
