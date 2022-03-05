Development version
-------------------

For development
^^^^^^^^^^^^^^^

.. code-block:: console

   $ cd PyFunceble && git checkout dev
   $ git fetch origin && git merge origin/dev

.. note::
   As you previously installed with

   .. code-block::

      $ . venv/bin/activate && pip3 install -e .

   Only code/repository update is required.

For usage
^^^^^^^^^

Using :code:`pip`
"""""""""""""""""

From PyPi
~~~~~~~~~

.. code-block:: console

   $ pip3 install --user --upgrade PyFunceble-dev

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies
   at the user level. More information about it can be found on
   `pip documentation`_.

.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble`
   into containers or CI engines.


From GitHub
~~~~~~~~~~~

.. code-block:: console

   $ pip3 install --user --upgrade git+https://github.com/funilrys/PyFunceble.git@dev#egg=PyFunceble

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies
   at the user level. More information about it can be found on
   `pip documentation`_.

.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble`
   into containers or CI engines.

Using the AUR (for Arch Linux users)
""""""""""""""""""""""""""""""""""""

With makepkg
~~~~~~~~~~~~

.. code-block:: console

   $ curl https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=python-pyfunceble-dev -o PKGBUILD
   $ makepkg
   $ sudo pacman -U python-pyfunceble-dev*.tar.xz

With your favorite AUR helper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::
   We do not recommend any AUR helper but keep in mind that some AUR helpers
   are "better" than other.
   For more information about your current (or any other) AUR helper please
   report to `the ArchWiki page`_.

.. code-block:: console

   $ yourFavoriteAurHelper -Syu python-pyfunceble-dev

Using docker (hub)
""""""""""""""""""

The image description can be found at https://hub.docker.com/r/pyfunceble/pyfunceble-dev

.. code-block:: console

   $ docker pull pyfunceble/pyfunceble-dev


Pure Python method
""""""""""""""""""

Execute the following and enjoy PyFunceble!

.. code-block:: console

   $ cd PyFunceble && git checkout dev
   $ git fetch origin && git merge origin/dev
   $ python3 setup.py test
   $ python3 setup.py install # Avoid this if you want to uninstall one day.
   $ pip3 install --user --upgrade -e . # Prefer this method.

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies
   at the user level. More information about it can be found on
   `pip documentation`_.

.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble`
   into containers or CI engines.


.. _the ArchWiki page: https://wiki.archlinux.org/index.php/AUR_helpers
.. _pip documentation: https://pip.pypa.io/en/stable/reference/pip_install/?highlight=--user#cmdoption-user
