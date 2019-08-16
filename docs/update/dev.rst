Development version
===================

For development
---------------

::

   $ cd PyFunceble && git checkout dev
   $ git fetch origin && git merge origin/dev

.. note::
   As you previously installed with

   ::

      $ . venv/bin/activate && pip3 install -e .

   Only code/repository update is required.

For usage
---------

Using :code:`pip`
^^^^^^^^^^^^^^^^^

From PyPi
"""""""""

::

   $ pip3 install --user --upgrade PyFunceble-dev

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies at the user level. More information about it can be found on `pip documentation`_.
.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble` into containers like - for example - Travis CI.

From GitHub
"""""""""""

::

   $ pip3 install --user --upgrade git+https://github.com/funilrys/PyFunceble.git@dev#egg=PyFunceble

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies at the user level. More information about it can be found on `pip documentation`_.
.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble` into containers like - for example - Travis CI.

Using the AUR (for Arch Linux users)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With makepkg
""""""""""""

::

    $ wget https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=python-pyfunceble-dev
    $ makepkg
    $ sudo pacman -U python-pyfunceble-dev*.tar.xz

With your favorite AUR helper
"""""""""""""""""""""""""""""

.. warning::
    We do not recommend any AUR helper but keep in mind that some AUR helpers are "better" than other.
    For more information about your current (or any other) AUR helper please report to `the ArchWiki page`_.

::

    $ yourFavoriteAurHelper -Syu python-pyfunceble-dev

Pure Python method
^^^^^^^^^^^^^^^^^^

Execute the following and enjoy PyFunceble!

::

   $ cd PyFunceble && git checkout dev
   $ git fetch origin && git merge origin/dev
   $ python3 setup.py test
   $ python3 setup.py install # Avoid this if you want to uninstall one day.
   $ pip install --user --upgrade -e .

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies at the user level. More information about it can be found on `pip documentation`_.
.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble` into containers like - for example - Travis CI.


.. _the ArchWiki page: https://wiki.archlinux.org/index.php/AUR_helpers
.. _pip documentation: https://pip.pypa.io/en/stable/reference/pip_install/?highlight=--user#cmdoption-user