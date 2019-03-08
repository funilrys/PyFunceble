.. image:: https://raw.githubusercontent.com/PyFunceble/logo/dev/Green/HD/RM.png
    :alt: PyFunceble logo

The tool to check the availability or syntax of domains, IPv4 or URL.
=====================================================================

.. image:: https://az743702.vo.msecnd.net/cdn/kofi3.png
    :target: https://ko-fi.com/V7V3EH2Y
    :height: 30px
.. image:: https://api.travis-ci.com/funilrys/PyFunceble.png?branch=dev
    :target: https://travis-ci.com/funilrys/PyFunceble
.. image:: https://coveralls.io/repos/github/funilrys/PyFunceble/badge.png?branch=dev
    :target: https://coveralls.io/github/funilrys/PyFunceble?branch=dev
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

.. _Funceble: https://github.com/funilrys/funceble

.. toctree::
   :maxdepth: 3
   :caption: Contents

   what-can-we-do
   in-action
   dead-hosts
   installation
   update
   configuration
   usage
   columns
   logs-sharing
   logic-representation
   api
   code
   issues
   faq
   contributing
   contributors
   special-thanks
   supporting-the-project
   they-use-it
   license
   code-of-conduct
   contact



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
