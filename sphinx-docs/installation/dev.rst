
Development version
-------------------

The development version of PyFunceble represents the :code:`dev` branch.
It's intended for the development of next features
but is always at a usable state.

Indeed, We should not push to the :code:`dev` branch until
we are sure that the new commit does not break or introduce
critical issue under PyFunceble.

For development
^^^^^^^^^^^^^^^

Execute the following and let's hack PyFunceble!

.. note::
   We highly recommend you to develop PyFunceble under a :code:`virtualenv`.


::

   $ git clone https://github.com/funilrys/PyFunceble.git
   $ cd PyFunceble
   $ git checkout dev
   $ virtualenv -p python3 venv
   $ source venv/bin/activate
   $ pip3 install -e .

.. note::
   After installing with:

   .. code-block:: console

      $ source venv/bin/activate
      $ pip3 install -e .

   * you only need to update the repository.
   * you don't have to rerun the :code:`pip` command.

For usage
^^^^^^^^^

Using :code:`pip`
"""""""""""""""""

Execute one of the following and enjoy PyFunceble!

From PyPi
~~~~~~~~~

::

   $ pip3 install --user PyFunceble-dev

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies
   at the user level. More information about it can be found on
   `pip documentation`_.
.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble`
   into containers or CI engines.

From GitHub
~~~~~~~~~~~

::

   $ pip3 install --user git+https://github.com/funilrys/PyFunceble.git@dev#egg=PyFunceble

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies
   at the user level. More information about it can be found on
   `pip documentation`_.
.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble`
   into containers or CI engines.

Using the AUR (for Arch Linux users)
""""""""""""""""""""""""""""""""""""

The package can be found at https://aur.archlinux.org/packages/pyfunceble-dev/.

With makepkg
~~~~~~~~~~~~

::

   $ curl https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=pyfunceble-dev -o PKGBUILD
   $ makepkg
   $ sudo pacman -U pyfunceble-dev*.tar.xz

With your favorite AUR helper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::
    We do not recommend any AUR helper but keep in mind that some AUR helpers
    are "better" than other.
    For more information about your current (or any other) AUR helper please
    report to `the ArchWiki page`_.

::

    $ yourFavoriteAurHelper -S pyfunceble-dev

Using docker (hub)
""""""""""""""""""

The image description can be found at https://hub.docker.com/r/pyfunceble/pyfunceble-dev

::

   $ docker pull pyfunceble/pyfunceble-dev

Pure Python method
""""""""""""""""""

Execute the following and enjoy PyFunceble!

::

   $ git clone https://github.com/funilrys/PyFunceble.git
   $ cd PyFunceble && git checkout dev
   $ tox # Run tests
   $ python3 setup.py install # Avoid this if you want to uninstall or update one day.
   $ pip3 install --user -e . # Prefer this method.

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies
   at the user level. More information about it can be found on
   `pip documentation`_.

.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble`
   into containers or CI engines.


.. _the ArchWiki page: https://wiki.archlinux.org/index.php/AUR_helpers
.. _pip documentation: https://pip.pypa.io/en/stable/reference/pip_install/?highlight=--user#cmdoption-user
