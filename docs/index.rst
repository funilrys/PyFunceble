.. image:: https://raw.githubusercontent.com/PyFunceble/logo/master/Green/HD/RM.png
    :alt: PyFunceble logo

The tool to check the availability or syntax of domain, IP or URL.
==================================================================

.. image:: https://img.shields.io/badge/code%20style-black-000000.png
    :target: https://github.com/ambv/black
.. image:: https://coveralls.io/repos/github/funilrys/PyFunceble/badge.png?branch=3.x
    :target: https://coveralls.io/github/funilrys/PyFunceble?branch=3.x
.. image:: https://img.shields.io/github/license/funilrys/PyFunceble.png
    :target: https://github.com/funilrys/PyFunceble/blob/3.x/LICENSE
.. image:: https://img.shields.io/pypi/v/pyfunceble.png
    :target: https://pypi.org/project/pyfunceble
.. image:: https://img.shields.io/github/issues/funilrys/PyFunceble.png
    :target: https://github.com/funilrys/PyFunceble/issues
.. image:: https://pepy.tech/badge/pyfunceble
    :target: https://pepy.tech/project/pyfunceble
.. image:: https://pepy.tech/badge/pyfunceble/month
    :target: https://pepy.tech/project/pyfunceble
.. image:: https://pepy.tech/badge/pyfunceble/week
    :target: https://pepy.tech/project/pyfunceble

PyFunceble is the little sister of `Funceble`_ which was archived on 13th
March 2018.

**EOL of PyFunceble 3.x**. Please do read more about this in the
`EOL <installation/index.html#eol-of-any-version-3-x>`_ chapter.

Its main objective is to provide the availability of domains, IPs and since
recently URL by generating an accurate result based on results from WHOIS,
NSLOOKUP and HTTP status codes.

PyFunceble provides some useful features for continuous testing.

As an example, its auto-continue system coupled with its auto-save system
allows it to run nice and smoothly under Travis CI without even reaching
Travis CI time restriction. In the other side, its internal inactive database
system let :code:`INACTIVE` and :code:`INVALID` caught domains, IPs or URLs
being automatically retested over time on next run.

.. _Funceble: https://github.com/funilrys/funceble

.. toctree::
   :maxdepth: 3

   what-can-we-do
   contributors
   special-thanks
   supporting-the-project

.. toctree::
   :maxdepth: 3

   respect/license
   respect/code-of-conduct

.. toctree::
   :maxdepth: 3

   facts/they-use-d-it
   facts/faq
   facts/known_issues
   facts/contact

.. toctree::
   :maxdepth: 3

   dead-hosts/index

.. toctree::
   :maxdepth: 3

   installation/index

.. toctree::
   :maxdepth: 3

   update/index

.. toctree::
   :maxdepth: 3

   configuration/index

.. toctree::
   :maxdepth: 3

   usage/index

.. toctree::
   :maxdepth: 3

   responses/index

.. toctree::
   :maxdepth: 3

   api/index

.. toctree::
   :maxdepth: 3

   components/index

.. toctree::
   :maxdepth: 3

   contributing/index

.. toctree::
   :maxdepth: 3

   code/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
