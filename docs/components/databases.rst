Databases
---------

Why do we use "databases"?
^^^^^^^^^^^^^^^^^^^^^^^^^^

We use databases to store data while we run the tests. When globally talking
about databases, we are indirectly talking about the following subsystems.
(JSON)

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
    If you plan to delete everything and still manage to use PyFunceble
    in the future, please use the :code:`--clean-all` argument.

    Indeed, it will delete everything which is related to what we generated,
    except things like the whois database file/table which saves (almost)
    static data which can be reused in the future.

    Deleting, for example, the whois database file/table will just make
    your test run for a much longer time if you retest subject that used
    to be indexed into the whois database file/table.

Databases types
^^^^^^^^^^^^^^^

Since PyFunceble :code:`2.0.0` (equivalent of :code:`>=1.18.0.dev`),
we offer multiple database types which are (as per configuration)
:code:`json` (default), :code:`mariadb` and :code:`mysql`.

We however only offers our support time for opensource software, hence
Oracles MySql are not supported. if it works, great. However they should
be pretty good covered through SQLAlchemy <https://docs.sqlalchemy.org/>

Why different database types?
"""""""""""""""""""""""""""""

With the introduction of the multiprocessing logic, it became natural to
introduce other database format as it's a nightmare to update a JSON
formatted file.

In order to write or use a JSON formatted database, we have to load it and
overwrite it completely.
It's great while working with a single CPU/process but as soon as we get
out of that scope it become unmanageable.

How to use the :code:`mariadb` or :code:`mysql` format?
"""""""""""""""""""""""""""""""""""""""""""""""""""""""

1. Create a new user, password and database (optional) for PyFunceble to
   work with.

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
        Since version :code:`2.4.3.dev` it is possible to use the UNIX
        socket for the :code:`PYFUNCEBLE_DB_HOST` environment variable.

        The typical location for :code:`mysqld.sock` is
        :code:`/var/run/mysqld/mysqld.sock`.

        This have been done to make

        1. It easier to use the :code:`socket` in conjunction with a
           supported CI environment/platform.

        2. Leaving more space on the IP-stack on local DB installations.

        3. The :code:`UNIX:SOCKET` is usually faster than the IP
           connection on local runs.

            ::

                PYFUNCEBLE_DB_CHARSET=utf8mb4
                PYFUNCEBLE_DB_HOST=/var/run/mysqld/mysqld.sock
                PYFUNCEBLE_DB_NAME=PyFunceble
                PYFUNCEBLE_DB_PASSWORD=Hello,World!
                PYFUNCEBLE_DB_PORT=3306
                PYFUNCEBLE_DB_USERNAME=pyfunceble

4. Switch the :code:`db_type` index of your configuration file to
   :code:`mariadb` or :code:`mysql`.
5. Play with PyFunceble!

.. note::
    If the environment variables are not found, you will be asked to
    prompt the information.

SQL Layout:
^^^^^^^^^^^

The layout and data within the Sql database and how they are used should
currently be following this patterns.

alembic_version
  - version_num The Current version of Pyfunceble in number

pyfunceble_file
  - :code:`id` Primary key, auto_increment
  - :code:`created` creation date of the record
  - :code:`modified` Data the record was last tested, altered
  - :code:`path` source of the file tested. URI or File_path
  - :code:`test_completed` (bool) this data is used for picking up a
    interrupted (broken) test or in CI for auto-continue :code:`-c`

pyfunceble_mined
  - :code:`id` Primary key, auto_increment
  - :code:`created` creation date of the record
  - :code:`modified` Data the record was last tested, altered
  - :code:`subject_id` key_ref to :code:`pyfunceble_status.id`
  - :code:`file_id` key_ref to :code:`pyfunceble_file.id`
  - :code:`mined` the full fqdns results of a :code:`--mining` response

pyfunceble_status
  - :code:`id` Primary key, auto_increment
  - :code:`created` creation date of the record
  - :code:`modified` Data the record was last tested, altered
  - :code:`file_id` (one to many relation) to :code:`pyfunceble_file.id`
    This is used to extract where a record comes from.
  - :code:`tested` IS the actual record tested in full (domain/URI)
  - :code:`_status` ACTIVE/INACTIVE status from the PyFunceble test (Twice??)
  - :code:`status` ACTIVE/INACTIVE status from the PyFunceble test (Twice??)
  - :code:`_status_source` The technique to determine the status WHOIS/DNSLOOKUP (Twice??)
  - :code:`status_source` The technique to determine the status WHOIS/DNSLOOKUP (Twice??)
  - :code:`domain_syntax_validation` (*INT???) Would expect a (bool(true,false)). Here I'm in doubt: Does this mean there was performed a :code:`--syntax` test OR if it (0= failed, 1= past) syntax test?
  - :code:`expiration_date` domain expiration date from a successful WHOIS response (shouldn't it be served true the whois table???)
  - :code:`http_status_code` the HTTP code from a lookup, example: 200 =
    succes, 404 file not found (suggested to be moved to new table see <https://www.mypdns.org/T1250#19039> for reusable data) 
  - :code:`ipv4_range_syntax_validation` (*INT???) Would expect a (bool(true,false))
  - :code:`ipv4_syntax_validation` (*INT???) Would expect a (bool(true,false))
  - :code:`ipv6_range_syntax_validation` (*INT???) Would expect a (bool(true,false))
  - :code:`ipv6_syntax_validation` (*INT???) Would expect a (bool(true,false))
  - :code:`subdomain_syntax_validation` ?? but from current data set I would again expect a (bool) and not (*INT) as it is 0 OR 1
  - :code:`url_syntax_validation` (*INT???) Would expect a (bool(true,false)). Here I'm in doubt: Does this mean there was performed a :code:`--syntax` test OR if it (0= failed, 1= past) syntax test?
  - :code:`is_complement` is this record from a :code:`--complement` test. (*INT???) Would expect a (bool(true,false))
  - :code:`test_completed` (*INT???) Would expect a (bool(true,false)) Have we done testing this record since last commit for test.
  - :code:`tested_at` The date for last succeeded tested.

pyfunceble_whois_record
  - :code:`id` Primary key, auto_increment
  - :code:`created` creation date of the record
  - :code:`modified` Data the record was last tested, altered
  - :code:`subject` the domain for which this record is stored
  - :code:`expiration_date` The domain expiration data according to the WHOIS
  - :code:`epoch` The domain expiration data according to the WHOIS. **just in EPOC format**
  - :code:`state` the domain state based on `expiration_date` and/or `epoc` future/past 
  - :code:`record` [NULL]?? would expect a key_ref to :code:`pyfunceble_status.id` and as replacement for :code:`pyfunceble_whois_record.subject`
  - :code:`server` the whois server holding the WHOIS data (Should be altered to separate table/(DB) for reusable data and gaining from db.cache and minimize I/O & DB size)
