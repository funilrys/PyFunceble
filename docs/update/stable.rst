Stable version
--------------

Important information for :code:`dev >= 3.2.11`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you update from dev@<=3.2.10 or master@<=3.2.2 to newer release, there
will be made a SQL conversion of the databases table layout.
This can take up a sagnificent amount of time based on the size of the
database.

The table layout converion is being made to:

1. Minimize the total size

2. Optimize the sql flow and minimizing the read/write to save disk I/O.

3. Minimize the number of SQL queries being made

It have been seen taking days to convert these tables on very large
installations.

Important information for :code:`dev >= 4.0.0`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you update to PyFunceble :code:`4.0.0`, there will be

- a SQL conversion if you use the :code:`mysql` or `mariadb` database type.
- a JSON to CSV conversion if one of those files is found in your filesystem:

   - :code:`inactive_db.json`
   - :code:`whois_db.json`

- a breaking and compatibility issue if you try to directly (automatically ?)
  read the data in the output directory. Indeed if you were looking for
  :code:`output/domains/ACTIVE/list` in PyFunceble :code:`3.x`, in :code:`4.0`,
  it is now under :code:`output/{{ input_file_name }}/domains/ACTIVE list`.

Using :code:`pip`
^^^^^^^^^^^^^^^^^

From PyPi
"""""""""

::

   $ pip3 install --user --upgrade PyFunceble

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies
   at the user level. More information about it can be found on
   `pip documentation`_.

.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble`
   into containers or CI engines.

From GitHub
"""""""""""

::

   $ pip3 install --user --upgrade git+https://github.com/funilrys/PyFunceble.git@master#egg=PyFunceble

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies
   at the user level. More information about it can be found on
   `pip documentation`_.

.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble`
   into containers or CI engines.

Using the AUR (for Arch Linux users)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With makepkg
""""""""""""

::

    $ wget https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=python-pyfunceble
    $ makepkg
    $ sudo pacman -U python-pyfunceble*.tar.xz

With your favorite AUR helper
"""""""""""""""""""""""""""""

.. warning::
   We do not recommend any AUR helper but keep in mind that some AUR helpers
   are "better" than other.
   For more information about your current (or any other) AUR helper please
   report to `the ArchWiki page`_.

::

   $ yourFavoriteAurHelper -Syu python-pyfunceble

Using docker (hub)
^^^^^^^^^^^^^^^^^^

The image description can be found at https://hub.docker.com/r/pyfunceble/pyfunceble

::

   $ docker pull pyfunceble/pyfunceble

Using :code:`conda`
^^^^^^^^^^^^^^^^^^^

Our repository is located at https://anaconda.org/pyfunceble/pyfunceble

::

   conda update -c conda-forge -c pyfunceble pyfunceble


Pure Python method
^^^^^^^^^^^^^^^^^^

Execute the following and enjoy PyFunceble!

::

   $ cd PyFunceble
   $ git checkout master && git fetch origin && git merge origin/master
   $ python3 setup.py test
   $ python3 setup.py install # Avoid this if you want to uninstall one day.
   $ pip3 install --user --upgrade -e . # Prefer this method.

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies
   at the user level. More information about it can be found on
   `pip documentation`_.


.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble`
   into containers like - for example - Travis CI.


.. _the ArchWiki page: https://wiki.archlinux.org/index.php/AUR_helpers
.. _pip documentation: https://pip.pypa.io/en/stable/reference/pip_install/?highlight=--user#cmdoption-user
