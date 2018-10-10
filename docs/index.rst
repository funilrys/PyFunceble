.. image:: https://github.com/funilrys/PyFunceble/raw/dev/.assets/logo/RM.png
    :alt: PyFunceble Logic representation

The tool to check the availability of domains, IPv4 or URL
==========================================================

.. image:: https://az743702.vo.msecnd.net/cdn/kofi3.png
    :target: https://ko-fi.com/V7V3EH2Y
    :height: 30px
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

Its main objective is to get and the return domains and IPs availability by generating an accurate result based on results from WHOIS, NSLOOKUP and HTTP status codes.

PyFunceble is running actively and daily with the help of Travis CI under 60+ repositories. It is used to clean or test the availability of data which are present in hosts files, list of IP, list of domains, blocklists or even AdBlock filter lists. 

Indeed, it is possible because PyFunceble generates a list of all `ACTIVE` domains or IPs but in the same time, it creates by default a database of the `INACTIVE` domains or IPs so it can retest them overtime automatically at the next execution.

.. _Funceble: https://github.com/funilrys/funceble

.. toctree::
   :maxdepth: 3
   :caption: Contents

   what-can-we-do
   installation
   update
   configuration
   usage
   colomns
   logs-sharing
   contributing
   logic-representation
   code
   contributors
   special-thanks
   supporting-the-project
   license
   code-of-conduct
   contact



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
