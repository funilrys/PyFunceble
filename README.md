![image](https://raw.githubusercontent.com/PyFunceble/logo/dev/Green/HD/RM.png)

# The tool to check the availability or syntax of domain, IP or URL

[![image](https://img.shields.io/badge/code%20style-black-000000.png)](https://github.com/ambv/black)
[![image](https://coveralls.io/repos/github/funilrys/PyFunceble/badge.png?branch=dev)](https://coveralls.io/github/funilrys/PyFunceble?branch=dev)
[![image](https://img.shields.io/github/license/funilrys/PyFunceble.png)](https://github.com/funilrys/PyFunceble/blob/dev/LICENSE)
[![image](https://img.shields.io/pypi/v/pyfunceble-dev.png)](https://pypi.org/project/pyfunceble-dev)
[![image](https://img.shields.io/github/issues/funilrys/PyFunceble.png)](https://github.com/funilrys/PyFunceble/issues)

[![image](https://pepy.tech/badge/pyfunceble-dev)](https://pepy.tech/project/pyfunceble-dev)
[![image](https://pepy.tech/badge/pyfunceble-dev/month)](https://pepy.tech/project/pyfunceble-dev)
[![image](https://pepy.tech/badge/pyfunceble-dev/week)](https://pepy.tech/project/pyfunceble-dev)

**PyFunceble** aims to provide an accurate availability check through
the usage of multiple sources which are for example - to only list a
few:

- the WHOIS record(s).
- the DNS record(s).
- the HTTP status code.

PyFunceble can be included in your existing project through:

- its standard built-in CLI implementation.
- its [Python
  API](https://pyfunceble.readthedocs.io/en/dev/api/index.html).
- the [PyFunceble
  web-worker](https://github.com/pyfunceble/web-worker) project that
  provides the core functionalities of PyFunceble behind a web API.

The PyFunceble CLI can test from a hosts file, a plain list of subjects,
an AdBlock filter list or even an RPZ record.

As of today, PyFunceble is running actively - if not daily - within
several servers, laptops, PCs, and Raspberry Pis. It is even used -
thanks to our auto continue mechanism - with CI engines like GitHub
Action, Travis CI, or GitLab CI.

Happy testing with PyFunceble!

[![image](https://github.com/PyFunceble/gifs/raw/dev/domain.gif)](https://github.com/PyFunceble/gifs/raw/dev/domain.gif)

# Installation

## Package
The PyFunceble project is distributed as 2 packages that reflects our 2 deployment
branches. Both packages are stable but with 2 different phylosophies.
Therefore, the choice is up to you.

The 2 packages are `pyfunceble` and `pyfunceble-dev`.

If you want a **stable** but **mature**, and **slowly** updating package, you
should install the `pyfunceble` package.
It reflects the `master` branch which only get updated once the new features and
bugfixes of `pyfunceble-dev` are tested long enough to be considered mature.

On the other hand, if you want a **stable** but **fast** updating package, you
should install the `pyfunceble-dev` package.
It reflects the `dev` branch which get updated frequently to allow the community to
provide feedbacks as soon as possible.

**Recommendation:**
For most people the `pyfunceble` package should be sufficient. But if you want to help
the community or always want to have the latest features and bugfix as soon as possible,
you should prefer the `pyfunceble-dev` package.

## PyPi - Python Package Index

For the **`pyfunceble`** package:

```shell
pip install --upgrade --pre pyfunceble
pyfunceble --version
```

For the **`pyfunceble-dev`** package:

```shell
pip install --upgrade --pre pyfunceble-dev
pyfunceble --version
```

## Docker Hub

For the **`pyfunceble`** package:

```shell
docker pull pyfunceble/pyfunceble
docker run -it pyfunceble/pyfunceble --version
```

For the **`pyfunceble-dev`** package:

```shell
docker pull pyfunceble/pyfunceble-dev
docker run -it pyfunceble/pyfunceble-dev --version
```

## ArchLinux

For the **`pyfunceble`** package:

```shell
[aur-helper] -S pyfunceble
pyfunceble --version
```

For the **`pyfunceble-dev`** package:

```shell
[aur-helper] -S pyfunceble-dev
pyfunceble --version
```

# Documentation as the place to be!

Want to know more about details **PyFunceble**? I invite you to read the
documentation at <https://pyfunceble.readthedocs.io/en/dev/>!

Want a local copy? I get you covered!

Simply run the following and enjoy the documentation!

```shell
# Install dependencies.
pip install --user -r requirements.docs.txt
# Move into the docs directory.
cd docs/
# Build Documentation
make clean html
# Open Documentation with browser
palemoon _build/html/index.html
```

**NOTE:** You are also invited to submit changes and improvement to the
documentation through a new Pull Request.

# Supporting the project

[PyFunceble](https://github.com/funilrys/PyFunceble),
[Dead-Hosts](https://github.com/dead-hosts), and all other analog
projects are powered by free time and a lot of coffee!

This project helps you you? Sponsor [@funilrys](https://github.com/funilrys) through the GitHub Sponsor
program by clicking the image bellow!

[![image](https://github.blog/de/wp-content/uploads/sites/3/2019/05/mona-heart-featured.png?w=200)](https://github.com/sponsors/funilrys)

# Contributors

Thanks to those awesome peoples for their awesome and crazy idea(s),
contribution(s) and or issue report which made or make
[PyFunceble](https://github.com/funilrys/PyFunceble) a better tool.

- avatartw - [@avatartw](https://github.com/avatartw)
- Avinash Reddy -
  [@AvinashReddy3108](https://github.com/AvinashReddy3108)
- BigDargon - [@bigdargon](https://github.com/bigdargon)
- Daniel - [@dnmTX](https://github.com/dnmTX)
- gwarser - [@gwarser](https://github.com/gwarser)
- Haris Gušić - [@veracioux](https://github.com/veracioux)
- hawkeye116477 - [@hawkeye116477](https://github.com/hawkeye116477)
- Human Being - [@T145](https://github.com/T145)
- Imre Kristoffer Eilertsen -
  [@DandelionSprout](https://github.com/DandelionSprout)
- jawz101 - [@jawz101](https://github.com/jawz101)
- Josenilson Ferreira da SIlva -
  [@Nilsonfsilva](https://github.com/Nilsonfsilva)
- keczuppp - [@keczuppp](https://github.com/keczuppp)
- kowith337 - [@kowith337](https://github.com/kowith337)
- Mitchell Krog - [@mitchellkrogza](https://github.com/mitchellkrogza)
- NeolithEra - [@NeolithEra](https://github.com/NeolithEra)
- Odyseus - [@Odyseus](https://github.com/Odyseus)
- opav - [@opav](https://github.com/opav)
- Reza Rizqullah - [@ybreza](https://github.com/ybreza)
- rusty-snake - [@rusty-snake](https://github.com/rusty-snake)
- ScriptTiger - [@ScriptTiger](https://github.com/ScriptTiger)
- sjhgvr - [@sjhgvr](https://github.com/sjhgvr)
- speedmann - [@speedmann](https://github.com/speedmann)
- spirillen - [@spirillen](https://www.mypdns.org/p/Spirillen/)
- The Unknown -
  [@AnonymousPoster](https://www.mypdns.org/p/AnonymousPoster/)
- WaLLy3K - [@WaLLy3K](https://github.com/WaLLy3K)
- xxcriticxx - [@xxcriticxx](https://github.com/xxcriticxx)
- Yuki2718 - [@Yuki2718](https://github.com/Yuki2718)
- Zachinquarantine -
  [@Zachinquarantine](https://github.com/Zachinquarantine)
- ZeroDot1 - [@ZeroDot1](https://github.com/ZeroDot1)

# Special Thanks

Thanks to those awesome organization(s), tool(s) and or people(s) for

- Their awesome documentation
- Their awesome repository
- Their awesome tool/software/source code
- Their breaking reports
- Their contributions
- Their current work/purpose
- Their promotion of Py-Funceble
- Their support
- Their testings reports

which helped and/or still help me build, test and or make
[PyFunceble](https://github.com/funilrys/PyFunceble) a better tool.

- Adam Warner - [@PromoFaux](https://github.com/PromoFaux)
- Adblock Plus - [@adblockplus](https://github.com/adblockplus)
- asciinema - [@asciinema](https://github.com/asciinema)
- Bob Halley - [@rthalley](https://github.com/rthalley)
  ([DNSPython](https://github.com/rthalley/dnspython))
- Chris Griffith - [@cdgriffith](https://github.com/cdgriffith)
  ([Box](https://github.com/cdgriffith/Box))
- Daniel - [@dnmTX](https://github.com/dnmTX)
- Jonathan Hartley - [@tartley](https://github.com/tartley)
  ([colorama](https://github.com/tartley/colorama))
- [IANA](https://www.iana.org/) - [ICANN](https://www.icann.org/)
  ([Root Zone Database](https://www.iana.org/domains/root/db))
- [Iterative](https://github.com/iterative)
  ([shtab](https://github.com/iterative/shtab))
- Kenneth Reitz - [@kennethreitz](https://github.com/kennethreitz)
  ([requests](https://github.com/kennethreitz/requests))
- Mitchell Krog - [@mitchellkrogza](https://github.com/mitchellkrogza)
- Mohammad Fares - [@faressoft](https://github.com/faressoft)
  ([Terminalizer](https://github.com/faressoft/terminalizer))
- Pi-Hole - [@pi-hole](https://github.com/pi-hole/pi-hole)
- Public Suffix List -
  [@publicsuffix](https://github.com/publicsuffix)
- Reza Rizqullah - [@ybreza](https://github.com/ybreza)
- Saurabh Kumar - [@theskumar](https://github.com/theskumar)
  ([python-dotenv](https://github.com/theskumar/python-dotenv))
- ScriptTiger - [@ScriptTiger](https://github.com/ScriptTiger)
- SMed79 - [@SMed79](https://github.com/SMed79)
- spirillen - [@spirillen](https://www.mypdns.org/p/Spirillen/)
- The YAML Project - [@yaml](https://github.com/yaml)
  ([pyyaml](https://github.com/yaml/pyyaml))
- [yWorks](https://www.yworks.com) - ([yEd Graph
  Editor](https://www.yworks.com/products/yed))

# License

    Copyright 2017, 2018, 2019, 2020, 2022, 2023 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
