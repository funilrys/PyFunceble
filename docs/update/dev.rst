Development version
-------------------

IMPORTANT INFORMATION for :code:`dev >= 3.2.11`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

::

   When you update from dev@<=3.2.10 or master@<=3.2.2
   to newer release, there will be made a SQL
   conversion of the databases table layout.
   This can take up a sagnificent amount of time
   based on the size of the Database.

   The table layout converion is being made to:

   1. Minimize the total size

   2. Optimize the sql flow and minimizing the
      read/write to save disk I/O

   3. Minimize the number of SQL queries being made

   It have been seen taking days to convert these
   tables on very large installations.


For development
^^^^^^^^^^^^^^^

::

   $ cd PyFunceble && git checkout dev
   $ git fetch origin && git merge origin/dev

.. note::
   As you previously installed with

   ::

      $ . venv/bin/activate && pip3 install -e .

   Only code/repository update is required.

For usage
^^^^^^^^^

Using :code:`pip`
"""""""""""""""""

From PyPi
~~~~~~~~~

::

   $ pip3 install --user --upgrade PyFunceble-dev

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies at the user level. More information about it can be found on `pip documentation`_.
.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble` into containers like - for example - Travis CI.

From GitHub
~~~~~~~~~~~

::

   $ pip3 install --user --upgrade git+https://github.com/funilrys/PyFunceble.git@dev#egg=PyFunceble

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies at the user level. More information about it can be found on `pip documentation`_.
.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble` into containers like - for example - Travis CI.

Using the AUR (for Arch Linux users)
""""""""""""""""""""""""""""""""""""

With makepkg
~~~~~~~~~~~~

::

    $ wget https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=python-pyfunceble-dev
    $ makepkg
    $ sudo pacman -U python-pyfunceble-dev*.tar.xz

With your favorite AUR helper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::
    We do not recommend any AUR helper but keep in mind that some AUR helpers are "better" than other.
    For more information about your current (or any other) AUR helper please report to `the ArchWiki page`_.

::

    $ yourFavoriteAurHelper -Syu python-pyfunceble-dev

Using docker (hub)
""""""""""""""""""

The image description can be found at https://hub.docker.com/r/pyfunceble/pyfunceble-dev

::

   $ docker pull pyfunceble/pyfunceble-dev

Using :code:`conda`
"""""""""""""""""""

Our repository is located at https://anaconda.org/pyfunceble/pyfunceble-dev

::

   conda update -c conda-forge -c pyfunceble pyfunceble-dev

Pure Python method
""""""""""""""""""

Execute the following and enjoy PyFunceble!

::

   $ cd PyFunceble && git checkout dev
   $ git fetch origin && git merge origin/dev
   $ python3 setup.py test
   $ python3 setup.py install # Avoid this if you want to uninstall one day.
   $ pip3 install --user --upgrade -e .

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies at the user level. More information about it can be found on `pip documentation`_.
.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble` into containers like - for example - Travis CI.


.. _the ArchWiki page: https://wiki.archlinux.org/index.php/AUR_helpers
.. _pip documentation: https://pip.pypa.io/en/stable/reference/pip_install/?highlight=--user#cmdoption-user
