Databases
=========

Why do we use "databases"?
--------------------------

We use database to store data while we run the tests. When globally talking about databases, we are indirectly talking about the following subsystems.

* Autocontinue
* InactiveDB
* Mining
* WhoisDB

.. warning::
    There is a different about what we are talking here and the :code:`--database` argument which only enable/disable the InactiveDB subsystem.

How do we manage them?
----------------------

They consist of simple JSON files which are read and updated on the fly.

Databases types
===============

Since PyFunceble :code:`2.0.0` (equivalent of PyFunceble :code:`>=1.18.0`),
we offer multiple database types which are (as per configuration) :code:`json` (default), :code:`sqlite`, :code:`mariadb` and :code:`mysql`.

Why different database types?
-----------------------------

With the introduction of the multiprocessing logic, it became natural to introduce other database format as it's a nightmare to update a JSON formatted.

Indeed in order to write or use a JSON formatted database, we have to load it and overwrite it completly.
It's great while working with a single CPU/process but as soon as we get out of that scope it become unmanagable.

How to use the :code:`sqlite` format?
-------------------------------------

Simply switch the :code:`db_type` index of your configuration file to :code:`sqlite`. That's it.

How to use the :code:`mysql` or :code:`mariadb` format?
-------------------------------------------------------

1. Create a new user, password and database (optional) for PyFunceble to work with.
2. Create a :code:`.pyfunceble-env` file at the root of your configuration directory.
3. Complete it with the following content (example)

::

    PYFUNCEBLE_DB_CHARSET=utf8mb4
    PYFUNCEBLE_DB_HOST=localhost
    PYFUNCEBLE_DB_NAME=PyFunceble
    PYFUNCEBLE_DB_PASSWORD=Hello,World!
    PYFUNCEBLE_DB_PORT=3306
    PYFUNCEBLE_DB_USERNAME=pyfunceble

4. Switch the :code:`db_type` index of your configuration file to :code:`mysql` or :code:`mariadb`.
5. Play with PyFunceble!

.. note::
    If the environment variables are not found, you will be asked to prompt the information.