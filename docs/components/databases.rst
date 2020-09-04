Databases
---------

Why do we use "databases"?
^^^^^^^^^^^^^^^^^^^^^^^^^^

We use databases to store data while we run the tests. When globally talking
about databases, we are indirectly talking about the following subsystems.

* Autocontinue
* InactiveDB
* Mining
* WhoisDB

.. warning::
    There is a difference between what we are talking here and the
    :code:`--database` argument which only enable/disable the InactiveDB
    subsystem.

How do we manage them?
^^^^^^^^^^^^^^^^^^^^^^

They consist of simple JSON files which are read and updated on the fly.

Warnings around Database (self) management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::
    If you plan to delete everything and still manage to use PyFunceble in the
    future, please use the :code:`--clean-all` argument.

    Indeed, it will delete everything which is related to what we generated,
    except things like the whois database file/table which saves (almost)
    static data which can be reused in the future.

    Deleting, for example, the whois database file/table will just make
    your test run for a much longer time if you retest subject that used to be
    indexed into the whois database file/table.

Databases types
^^^^^^^^^^^^^^^

Since PyFunceble :code:`2.0.0` (equivalent of :code:`>=1.18.0.dev`),
we offer multiple database types which are (as per configuration) :code:`json`
(default), :code:`mariadb` and :code:`mysql`.

Why different database types?
"""""""""""""""""""""""""""""

With the introduction of the multiprocessing logic, it became natural to
introduce other database format as it's a nightmare to update a JSON formatted
file.

In order to write or use a JSON formatted database, we have to load it and
overwrite it completely.
It's great while working with a single CPU/process but as soon as we get out of
that scope it become unmanageable.

How to use the :code:`mysql` or :code:`mariadb` format?
"""""""""""""""""""""""""""""""""""""""""""""""""""""""

1. Create a new user, password and database (optional) for PyFunceble to work
   with.

2. Create a :code:`.pyfunceble-env` file at the root of your configuration
   directory.

3. Complete it with the following content (example)

    ::

        PYFUNCEBLE_DB_CHARSET=utf8mb4
        PYFUNCEBLE_DB_HOST=localhost
        PYFUNCEBLE_DB_NAME=PyFunceble
        PYFUNCEBLE_DB_PASSWORD=Hello,World!
        PYFUNCEBLE_DB_PORT=3306
        PYFUNCEBLE_DB_USERNAME=pyfunceble

    .. note::
        Since version :code:`2.4.3.dev` it is possible to use the UNIX socket
        for the :code:`PYFUNCEBLE_DB_HOST` environment variable.

        The typical location for :code:`mysqld.sock` is
        :code:`/var/run/mysqld/mysqld.sock`.

        This have been done to make

        1. It easier to use the :code:`socket` in conjunction with a supported CI
        environment/platform.

        2. Leaving more space on the IP-stack on local DB installations.

        3. The :code:`UNIX:SOCKET` is usually faster than the IP connection on
        local runs.

            ::

                PYFUNCEBLE_DB_CHARSET=utf8mb4
                PYFUNCEBLE_DB_HOST=/var/run/mysqld/mysqld.sock
                PYFUNCEBLE_DB_NAME=PyFunceble
                PYFUNCEBLE_DB_PASSWORD=Hello,World!
                PYFUNCEBLE_DB_PORT=3306
                PYFUNCEBLE_DB_USERNAME=pyfunceble

4. Switch the :code:`db_type` index of your configuration file to :code:`mysql`
   or :code:`mariadb`.
5. Play with PyFunceble!

.. note::
    If the environment variables are not found, you will be asked to prompt the
    information.
