Requirements
------------

Here is the list of requirements:

-   Python 3.6.11+
-   :code:`alembic`
-   :code:`colorama`
-   :code:`cryptography`
-   :code:`dnspython`
-   :code:`domain2idna`
-   :code:`inflection`
-   :code:`PyMySQL`
-   :code:`python-box`
-   :code:`python-dotenv`
-   :code:`PyYAML`
-   :code:`requests`
-   :code:`setuptools`
-   :code:`sqlalchemy`

Python 3.6.11+
^^^^^^^^^^^^^^

The specification :code:`3.6.11+` is because we test PyFunceble (daily)
in all (:code:`3.x`) versions from :code:`3.6.11`.
Otherwise, more semantically, PyFunceble is written for all Python 3.6+ version.

:code:`alembic`
^^^^^^^^^^^^^^^

As we want to automate database (MySQL/MariaDB) schema migration, we
chose :code:`alembic` for the job.

:code:`colorama`
^^^^^^^^^^^^^^^^

As we use some coloration, :code:`colorama` is required.

:code:`cryptography`
^^^^^^^^^^^^^^^^^^^^

As we use some cryptography algorithm for message hashing as example,
:code:`cryptography` is required.

:code:`dnspython`
^^^^^^^^^^^^^^^^^

As we use it to do the DNS lookups, :code:`dnspython` is required.

:code:`domain2idna`
^^^^^^^^^^^^^^^^^^^

As we propose the conversion of domains to IDNA, :code:`domain2idna` is required.

.. note::
    :code:`domain2idna` is maintained and developed by
    `Nissar Chababy (@funilrys)`_, the developer of PyFunceble.
    Its source code can be found `on GitHub`_.

.. _Nissar Chababy (@funilrys): https://github.com/funilrys
.. _on GitHub: https://github.com/PyFunceble/domain2idna

:code:`inflection`
^^^^^^^^^^^^^^^^^^

We don't necessarily want to reinvent the wheel while generating the (database)
tables name from our schama descriptions. This tool is a relief!

:code:`PyMySQL`
^^^^^^^^^^^^^^^

As we propose the :code:`MariaDB` or :code:`MySQL` database types,
:code:`PyMySQL` is required.

:code:`python-box`
^^^^^^^^^^^^^^^^^^

As we use :code:`python-box` for a better code access to the configuration, it is required.

:code:`python-dotenv`
^^^^^^^^^^^^^^^^^^^^^

As we are able to load dotenv files, :code:`python-dotenv` is required.

:code:`PyYAML`
^^^^^^^^^^^^^^

As our configuration file is written in :code:`.yaml`, :code:`PyYAML` is required.

:code:`requests`
^^^^^^^^^^^^^^^^

As we use :code:`requests` multiple times to communicate with webservices, :code:`requests` is required.

:code:`setuptools`
^^^^^^^^^^^^^^^^^^

As we use :code:`install_requires=xx` inside our :code:`setup.py`, :code:`setuptools` is required.

:code:`sqlalchemy`
^^^^^^^^^^^^^^^^^^

As we don't want to maintain several RAW SQL files, we use :code:`sqlalchemy`
for the database communication and manipulation.