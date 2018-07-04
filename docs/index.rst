.. image:: https://github.com/funilrys/PyFunceble/raw/master/.assets/logo/RM.png
    :alt: PyFunceble Logic representation

The tool to check domain or IP availability
===========================================

.. raw:: html
   
   <p align="center"><a href="https://travis-ci.com/funilrys/PyFunceble"><img src="https://travis-ci.com/funilrys/PyFunceble.svg?branch=master" alt="Build Status"></a> <a href="https://coveralls.io/github/funilrys/PyFunceble?branch=master"><img src="https://coveralls.io/repos/github/funilrys/PyFunceble/badge.svg?branch=master" alt="Coverage Status"></a> <a href="https://github.com/funilrys/PyFunceble/blob/master/LICENSE"><img src="https://img.shields.io/github/license/funilrys/PyFunceble.svg" alt="license"></a> <a href="https://github.com/funilrys/PyFunceble/releases/latest"><img src="https://img.shields.io/github/release/funilrys/PyFunceble.svg" alt="GitHub release"></a> <a href=""><img src="https://img.shields.io/github/issues/funilrys/PyFunceble.svg" alt="GitHub issues open"></a> <a href="https://github.com/ambv/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style | Black"></a></p>

PyFunceble is the little sister of `Funceble`_ which was archived on 13th March, 2018.

Its main objective is to get and the return domains and IPs availability by generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

PyFunceble is running actively and daily with the help of Travis CI under 60+ repositories. It is used to clean or test the availability of data which are present in hosts files, list of IP, list of domains, blocklists or even AdBlock filter lists. 

Indeed, it is possible because PyFunceble generates a list of all `ACTIVE` domains or IPs but in the same time, it creates by default a database of the `INACTIVE` domains or IPs so it can retest them overtime automatically at the next execution.

.. _Funceble: https://github.com/funilrys/funceble

Main Features
-------------

-   Get the status (`ACTIVE`, `INACTIVE`, `INVALID`) of a given domain or IPv4.
-   Read an existing file and check every domain and IPv5 present into it.
-   Generate a `hosts` file according to the domains statuses.
-   Generate a list of the domain according to their discovered statuses.
-   Show results on screen
-   Save results on file(s)
-   ... and a lot more!

.. toctree::
   :maxdepth: 2
   :caption: Contents
   
   installation
   update
   usage
   colomns
   logs-sharing
   contributing
   logic-representation
   code
   contributors
   special-thanks
   license
   code-of-conduct
   contact



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
