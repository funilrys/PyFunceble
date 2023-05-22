# PyFunceble

![image](https://raw.githubusercontent.com/PyFunceble/logo/dev/Green/HD/RM.png)

<p align="center">
    <em>The tool to check the availability or syntax of domain, IP or URL.</em>
</p>

<p align="center">
    <a href="https://github.com/ambv/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.png" alt="image">
    </a>
    <a href="https://coveralls.io/github/funilrys/PyFunceble?branch=dev">
        <img src="https://coveralls.io/repos/github/funilrys/PyFunceble/badge.png?branch=dev" alt="image">
    </a>
    <a href="https://github.com/funilrys/PyFunceble/blob/dev/LICENSE">
        <img src="https://img.shields.io/github/license/funilrys/PyFunceble.png" alt="image">
    </a>
    <a href="https://pypi.org/project/pyfunceble-dev">
        <img src="https://img.shields.io/pypi/v/pyfunceble-dev.png" alt="image">
    </a>
    <a href="https://github.com/funilrys/PyFunceble/issues">
        <img src="https://img.shields.io/github/issues/funilrys/PyFunceble.png" alt="image">
    </a>
</p>
<p align="center">
    <a href="https://pepy.tech/project/pyfunceble-dev">
        <img src="https://pepy.tech/badge/pyfunceble-dev" alt="image">
    </a>
    <a href="https://pepy.tech/project/pyfunceble-dev">
        <img src="https://pepy.tech/badge/pyfunceble-dev/month" alt="image">
    </a>
    <a href="https://pepy.tech/project/pyfunceble-dev">
        <img src="https://pepy.tech/badge/pyfunceble-dev/week" alt="image">
    </a>
</p>

**PyFunceble** is a tools that aims to provide an accurate availability check through
the usage of multiple sources which are for example - to only list a few:

- the WHOIS record(s).
- the DNS record(s).
- the HTTP status code.
- a community currated list of **special** rules.

PyFunceble can be included in your existing project through:

- its standard built-in CLI implementation.
- its [Python
  API](https://pyfunceble.readthedocs.io/en/dev/api/index.html).
- the [PyFunceble
  web-worker](https://github.com/pyfunceble/web-worker) project that
  provides the core functionalities of PyFunceble behind a web API.

The PyFunceble CLI can test from a hosts file, a plain list of subjects,
an AdBlock filter list or even an RPZ record file.

As of today, PyFunceble is running actively - if not daily - behind a pool of
several servers, laptops, PCs, and Raspberry Pis. It is even used -
thanks to our auto continue mechanism - with CI engines like GitHub
Action, Travis CI, or GitLab CI.
