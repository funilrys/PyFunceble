.. image:: https://raw.githubusercontent.com/PyFunceble/logo/dev/Green/HD/RM.png
    :alt: PyFunceble logo

The tool to check the availability or syntax of domain, IP or URL.
==================================================================

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


Welcome to PyFunceble!

**PyFunceble** is a tool that aims to provide an accurate availability check
through the usage of multiple sources which are for example - to only list a few:

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

.. _Python API: api/index.html
.. _PyFunceble web-worker: https://github.com/pyfunceble/web-worker

.. toctree::
   :maxdepth: 3

   history
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

   installation/index

.. toctree::
   :maxdepth: 3

   update/index

.. toctree::
   :maxdepth: 5

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

   dead-hosts/index

.. toctree::
   :maxdepth: 3

   facts/they-use-d-it
   facts/faq
   facts/known_issues
   facts/contact

.. toctree::
   :maxdepth: 5

   code/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
