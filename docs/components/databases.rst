Databases
---------

Why do we use "databases"?
^^^^^^^^^^^^^^^^^^^^^^^^^^

We use databases to store data while we run the tests. When globally talking
about databases, we are indirectly talking about the following subsystems.

* Autocontinue
* InactiveDB
* WhoisDB

How do we manage them?
^^^^^^^^^^^^^^^^^^^^^^

They consist of simple CSV files which are read and updated on the fly.

Warnings around Database (self) management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::
    If you plan to delete everything and still manage to use PyFunceble in the
    future, please use the :code:`clean-pyfunceble` CLI.

    Indeed, it will delete everything that we generated,
    except the things like the WHOIS database file/table which saves (almost)
    static data which should be reused in the future.

    Deleting, for example, the WHOIS database file/table will just make
    your test run for a much longer time if you retest subject that used to be
    indexed into the whois database file/table.

Databases types
^^^^^^^^^^^^^^^

Since PyFunceble :code:`2.0.0` (equivalent of :code:`>=1.18.0.dev`),
we offer multiple database types which are (as per configuration) :code:`csv`
(default since :code:`4.0.0`), :code:`mariadb` and :code:`mysql`.

Why different database types?
"""""""""""""""""""""""""""""

With the introduction of the multiprocessing logic, it became natural to
introduce other database formats.

How to use the :code:`mysql` or :code:`mariadb` format?
"""""""""""""""""""""""""""""""""""""""""""""""""""""""

1. Create a new user, password and database (optional) for PyFunceble to work
   with.

2. Create a :code:`.pyfunceble-env` file at the root of your configuration
   directory.

3. Complete it with the following content (example)

    .. code-block:: console

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

            .. code-block:: console

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
