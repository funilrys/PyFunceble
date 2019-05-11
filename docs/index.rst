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
   :caption: Preface

   what-can-we-do
   in-action
   contributors
   special-thanks
   supporting-the-project

.. toctree::
   :maxdepth: 3
   :caption: Respect

   respect/license
   respect/code-of-conduct

.. toctree::
   :maxdepth: 3
   :caption: Facts

   facts/they-use-it
   facts/faq
   facts/known_issues
   facts/contact

.. toctree::
   :maxdepth: 3
   :caption: Use Dead-Hosts if you can't!

   dead-hosts/why
   dead-hosts/how
   dead-hosts/history

.. toctree::
   :maxdepth: 3
   :caption: Installation

   installation/requirements
   installation/stable
   installation/dev
   installation/first-steps

.. toctree::
   :maxdepth: 3
   :caption: Update

   update/stable
   update/dev

.. toctree::
   :maxdepth: 3
   :caption: Configuration

   configuration/location
   configuration/auto
   configuration/indexes

.. toctree::
   :maxdepth: 3
   :caption: Usage

   usage/from-a-terminal
   usage/from-travis-ci
   usage/with-our-python-api

.. toctree::
   :maxdepth: 3
   :caption: Our (CLI) columns

   columns/subject
   columns/status
   columns/expiration_date
   columns/source
   columns/http_code

.. toctree::
   :maxdepth: 3
   :caption: API documentation

   api

.. toctree::
   :maxdepth: 3
   :caption: Components

   components/logs-sharing

.. toctree::
   :maxdepth: 3
   :caption: Contributing

   contributing/submit
   contributing/before_commit
   contributing/the_commit
   contributing/coding_conventions

.. toctree::
   :maxdepth: 3
   :caption: Code documentation

   code/logic-representation
   code/helpers
   code/adblock
   code/api_core
   code/auto_continue
   code/auto_save
   code/check
   code/clean
   code/cli_core
   code/config
   code/directory_structure
   code/dispatcher
   code/dns_lookup
   code/execution_time
   code/expiration_date
   code/file_core
   code/generate
   code/http_code
   code/iana
   code/inactive_db
   code/logs
   code/mining
   code/percentage
   code/preset
   code/prints
   code/production
   code/publicsuffix
   code/referer
   code/simple_core
   code/sort
   code/status
   code/whois_db
   code/whois


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
