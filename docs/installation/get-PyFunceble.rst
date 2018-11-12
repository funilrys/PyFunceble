Get PyFunceble
==============

Stable version
--------------

Using :code:`pip`
^^^^^^^^^^^^^^^^^

Choose your repository, install and enjoy PyFunceble!

From PyPi
"""""""""

::
 
   $ pip3 install PyFunceble

From GitHub
"""""""""""

::

   $ pip3 install git+https://github.com/funilrys/PyFunceble.git@master#egg=PyFunceble

Using the AUR (for Arch Linux users)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The package can be found at https://aur.archlinux.org/packages/python-pyfunceble/.

With makepkg
""""""""""""

::

    $ wget https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=python-pyfunceble
    $ makepkg
    $ sudo pacman -U python-pyfunceble*.tar.xz

With your favorite AUR helper
"""""""""""""""""""""""""""""

.. warning::
    We do not recommend any AUR helper but keep in mind that some AUR helper are "better" than other.
    For more information about your current (or any other) AUR helper please report to `the ArchWiki page`_.

::

    $ yourFavoriteAurHelper -S python-pyfunceble

Pure Python method
^^^^^^^^^^^^^^^^^^

Execute the following and enjoy PyFunceble!

::

   $ git clone https://github.com/funilrys/PyFunceble.git
   $ cd PyFunceble
   $ python3 setup.py test && python3 setup.py install


Development version
--------------------

The development version of PyFunceble represents the :code:`dev` branch.
It's intended for the development of next features but is always at a usable state.

Indeed, We should not push to the :code:`dev` branch until we are sure that the new commit does not break or introduce critical issue under PyFunceble.

For development
^^^^^^^^^^^^^^^^

Execute the following and let's hack PyFunceble!

Please note that we recommend that you develop PyFunceble under a virtualenv this way we ensure that it should work correctly.

::

   $ git clone https://github.com/funilrys/PyFunceble.git
   $ cd PyFunceble && git checkout dev && virtualenv venv
   $ source venv/bin/activate && pip3 install -e .

For usage
^^^^^^^^^

Using :code:`pip`
"""""""""""""""""

Execute one of the following and enjoy PyFunceble!

**From PyPi**

::

   $ pip3 install PyFunceble-dev

**From GitHub**

::

   $ pip3 install git+https://github.com/funilrys/PyFunceble.git@dev#egg=PyFunceble

Using the AUR (for Arch Linux users)
""""""""""""""""""""""""""""""""""""

The package can be found at https://aur.archlinux.org/packages/python-pyfunceble-dev/.

**With makepkg**

::

    $ wget https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=python-pyfunceble-dev
    $ makepkg
    $ sudo pacman -U python-pyfunceble-dev*.tar.xz

**With your favorite AUR helper**

.. warning::
    We do not recommend any AUR helper but keep in mind that some AUR helper are "better" than other.
    For more information about your current (or any other) AUR helper please report to `the ArchWiki page`_.

::

    $ yourFavoriteAurHelper -S python-pyfunceble-dev

Pure Python method
""""""""""""""""""

Execute the following and enjoy PyFunceble!

::

   $ git clone https://github.com/funilrys/PyFunceble.git
   $ cd PyFunceble && git checkout dev
   $ python3 setup.py test && python3 setup.py install
