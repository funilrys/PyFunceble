Requirements
============

Here is the list of requirements:

-   Python 3.6.2+
-   :code:`colorama`
-   :code:`cryptography`
-   :code:`dnspython`
-   :code:`domain2idna`
-   :code:`PyMySQL`
-   :code:`python-box`
-   :code:`python-dotenv`
-   :code:`PyYAML`
-   :code:`requests`
-   :code:`setuptools`
-   :code:`urllib3`

Python 3.6.8+
-------------

The specification :code:`3.6.8+` is because we test PyFunceble (daily)
in all version from :code:`3.6.8`.
Otherwise, more semantically, PyFunceble is written for all Python 3.6+ version.

:code:`colorama`
----------------

As we use some coloration coloration, :code:`colorama` is required.

:code:`cryptography`
--------------------

As we use some cryptography algorithm for message hashing as example,
:code:`cryptography` is required.

:code:`dnspython`
-----------------

As we use it to do the DNS lookups, :code:`dnspython` is required.

:code:`domain2idna`
-------------------

As we propose the conversion of domains to IDNA, :code:`domain2idna` is required.

.. note::
    :code:`domain2idna` is maintained and developed by
    `Nissar Chababy (@funilrys)`_, the main developer of PyFunceble.
    Its source code can be found `on GitHub`_.

.. _Nissar Chababy (@funilrys): https://github.com/funilrys
.. _on GitHub: https://github.com/funilrys/domain2idna

:code:`PyMySQL`
---------------

As we propose the :code:`MariaDB` or :code:`MySQL` database types,
:code:`PyMySQL` is required.

:code:`python-box`
------------------

As we use :code:`python-box` for a better code access to the configuration, it is required.

:code:`python-dotenv`
---------------------

As we are able to load dotenv files, :code:`python-dotenv` is required.

:code:`PyYAML`
--------------

As our configuration file is written in :code:`.yaml`, :code:`PyYAML` is required.

:code:`requests`
----------------

As we use :code:`requests` multiple times to communicate with webservices, :code:`requests` is required.

:code:`setuptools`
------------------

As we use :code:`install_requires=xx` inside our :code:`setup.py`, :code:`setuptools` is required.

:code:`urllib3`
---------------

You should normally already have it. But as we handle some of its errors while using :code:`requests`, :code:`urllib3` is required.
