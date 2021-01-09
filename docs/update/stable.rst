Stable version
--------------


Using :code:`pip`
^^^^^^^^^^^^^^^^^

From PyPi
"""""""""

.. code-block:: bash

   pip3 install --user --upgrade PyFunceble

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies
   at the user level. More information about it can be found on
   `pip documentation`_.

.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble`
   into containers or CI engines.

From GitHub
"""""""""""

.. code-block:: bash

   pip3 install --user --upgrade git+https://github.com/funilrys/PyFunceble.git@master#egg=PyFunceble

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

.. code-block:: bash

   wget https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=python-pyfunceble
   makepkg
   sudo pacman -U python-pyfunceble*.tar.xz

With your favorite AUR helper
"""""""""""""""""""""""""""""

.. warning::
   We do not recommend any AUR helper but keep in mind that some AUR helpers
   are "better" than other.
   For more information about your current (or any other) AUR helper please
   report to `the ArchWiki page`_.

.. code-block:: bash

   yourFavoriteAurHelper -Syu python-pyfunceble

Using docker (hub)
^^^^^^^^^^^^^^^^^^

The image description can be found at https://hub.docker.com/r/pyfunceble/pyfunceble

.. code-block:: bash

   docker pull pyfunceble/pyfunceble

Using :code:`conda`
^^^^^^^^^^^^^^^^^^^

Our repository is located at https://anaconda.org/pyfunceble/pyfunceble

.. code-block:: bash

   conda update -c conda-forge -c pyfunceble pyfunceble


Pure Python method
^^^^^^^^^^^^^^^^^^

Execute the following and enjoy PyFunceble!

.. code-block:: bash

   cd PyFunceble
   git checkout master && git fetch origin && git merge origin/master
   python3 setup.py test
   python3 setup.py install # Avoid this if you want to uninstall one day.
   pip3 install --user --upgrade -e . # Prefer this method.

.. note::
   We recommend the :code:`--user` flag which installs the required dependencies
   at the user level. More information about it can be found on
   `pip documentation`_.


.. warning::
   We do not recommend the :code:`--user` flag when using :code:`PyFunceble`
   into containers like - for example - Travis CI.


.. _the ArchWiki page: https://wiki.archlinux.org/index.php/AUR_helpers
.. _pip documentation: https://pip.pypa.io/en/stable/reference/pip_install/?highlight=--user#cmdoption-user
