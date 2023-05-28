Known issues
============

This is the list of issues which are not or will not be fixed (yet...).

* Under Travis CI the coloration may not be shown.
* Under GitLab CI/CD the coloration may not be shown.


Python < 3.8
^^^^^^^^^^^^

    .. versionchanged:: 4.2.0

As of version 4.2.0 we no `longer support <../installation/index.html#python-3-8-0>`_
python prior to version 3.8.

This means you actually are unable to run with any version below python 3.8
as a number of build-in features may be missing or first introduced in 3.8.

------


.. sectionauthor:: @spirillen

Ubuntu 20.04.1 LTS Focal
^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 3.2.0

In Ubuntu release 20.04 they have removed a package name
:code:`libffi.so.6` and upgraded it with version :code:`libffi.so.7`

This means PyFunceble will trow an error like:

.. code-block:: console

    ImportError: libffi.so.6: cannot open shared object file: No such file or directory

The fix for this issue is then rather simple, add a softlink between the
versions with :code:`ln -s`

The complete line in my case was:

.. code-block:: console

    sudo ln -s /usr/lib/x86_64-linux-gnu/libffi.so.7 /usr/lib/x86_64-linux-gnu/libffi.so.6

However, the right way to do this is by first locate where your
:code:`libffi.so.7` is with find

.. code-block:: console

    find /usr/lib/ -type f -iname 'libffi.so.*'

Then apply the softlink to :code:`libffi.so.7`


Combination of :code:`-f`, :code:`-uf` and :code:`--adblock`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can not combine the usage of :code:`-f`, :code:`-uf` with :code:`--adblock`
simultaneously.

------


.. sectionauthor:: @spirillen


Sql Missing default data in :code:`whois` table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 4.0.0

If you are trying to move or restore your SQL database from a dump, you
will see an error message that is looking something like this

.. code-block:: SQL

    SQL Error [1364][HY000]: (conn=12345678) Field 'created_at' doesn't have a default value
      (conn=12345678) Field 'created_at' doesn't have a default value
      (conn=12345678) Field 'created_at' doesn't have a default value
        Field 'created_at' doesn't have a default value

The issue arises from the way `SQLAlchemy`_ is creating the tables. The
fact is PyFunceble is written to set a default :code:`date` for the
:code:'created_at`.

However, it isn't set in the database.

To solve this, you will have to manually set the default for `created_at`
to for example :code:`2020-12-22 09:09:50` in the
:code:`DB_name.pyfunceble_whois_record`. You can for example use dBeaver_
to do this or manually run this SQL code insode your database.

.. code-block:: sql

    ALTER TABLE DB_name.pyfunceble_whois_record
        MODIFY COLUMN created_at datetime
        DEFAULT '2020-12-22 09:09:50'
        NOT NULL;

.. warning::

    These changes will be reset next time you are running PyFunceble.


.. External links

.. _SQLAlchemy: https://www.sqlalchemy.org/

.. _dBeaver: https://dbeaver.io/

------


.. sectionauthor:: @spirillen


Windows Powershell with Python or Cygwin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: all

There are a number of well Known limitation by running or even installing Python
on a closed source Windows computer.

Among these issues is the default settings for the installation programs,
where we all know the users tend to just click next next next without reading
the questions, and the path toward hell continues.

  1. To have Python to become installed within the system :code:`PATH:` by the
     installer, you are required to use the advanced install option.
     (spirillen_ Was told).

  2. Cygwin do not INCLUDE- and therefore not exporting current :code:`PATH` to running
     environment. Full path is always required, to be set by your scripts or
     command line.

Since any of these problems, ain't @PyFunceble related issues we have left a
Cygwin_ related issue at github.

.. _Cygwin: https://github.com/funilrys/PyFunceble/issues/127

.. _spirillen: https://mypdns.org/spirillen
