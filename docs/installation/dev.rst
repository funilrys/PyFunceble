
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
   $ virtualenv venv
   $ source venv/bin/activate
   $ pip3 install -e .

.. note::
   After installing with:

   ::

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
   We recommend the :code:`--user` flag which installs the required dependencies at the user level. More information about it can be found on `pip documentation`_.
.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble` into containers like - for example - Travis CI.

From GitHub
~~~~~~~~~~~

::

   $ pip3 install --user git+https://github.com/funilrys/PyFunceble.git@dev#egg=PyFunceble

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies at the user level. More information about it can be found on `pip documentation`_.
.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble` into containers like - for example - Travis CI.

Using the AUR (for Arch Linux users)
""""""""""""""""""""""""""""""""""""

The package can be found at https://aur.archlinux.org/packages/pyfunceble-dev/.

With makepkg
~~~~~~~~~~~~

::

   $ wget https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=pyfunceble-dev
   $ makepkg
   $ sudo pacman -U pyfunceble-dev*.tar.xz

With your favorite AUR helper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::
    We do not recommend any AUR helper but keep in mind that some AUR helpers are "better" than other.
    For more information about your current (or any other) AUR helper please report to `the ArchWiki page`_.

::

    $ yourFavoriteAurHelper -S pyfunceble-dev

Using docker (hub)
""""""""""""""""""

The image description can be found at https://hub.docker.com/r/pyfunceble/pyfunceble-dev

::

   $ docker pull pyfunceble/pyfunceble-dev

Using :code:`conda`
"""""""""""""""""""

Our repository is located at https://anaconda.org/pyfunceble/pyfunceble-dev

::

   conda install -c conda-forge -c pyfunceble pyfunceble-dev=3

Pure Python method
""""""""""""""""""

Execute the following and enjoy PyFunceble!

::

   $ git clone https://github.com/funilrys/PyFunceble.git
   $ cd PyFunceble && git checkout dev
   $ python3 setup.py test
   $ python3 setup.py install # Avoid this if you want to uninstall one day.
   $ pip3 install --user -e .

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies at the user level. More information about it can be found on `pip documentation`_.
.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble` into containers like - for example - Travis CI.


.. _the ArchWiki page: https://wiki.archlinux.org/index.php/AUR_helpers
.. _pip documentation: https://pip.pypa.io/en/stable/reference/pip_install/?highlight=--user#cmdoption-user
