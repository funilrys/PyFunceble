Stable version
==============

Using :code:`pip`
-----------------

Choose your repository, install and enjoy PyFunceble!

From PyPi
^^^^^^^^^

::

   $ pip3 install PyFunceble

From GitHub
^^^^^^^^^^^

::

   $ pip3 install git+https://github.com/funilrys/PyFunceble.git@master#egg=PyFunceble

Using the AUR (for Arch Linux users)
------------------------------------

The package can be found at https://aur.archlinux.org/packages/pyfunceble/.

With makepkg
^^^^^^^^^^^^

::

    $ wget https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=pyfunceble
    $ makepkg
    $ sudo pacman -U pyfunceble*.tar.xz

With your favorite AUR helper
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::
    We do not recommend any AUR helper but keep in mind that some AUR helpers are "better" than other.
    For more information about your current (or any other) AUR helper please report to `the ArchWiki page`_.

::

    $ yourFavoriteAurHelper -S pyfunceble

Pure Python method
------------------

Execute the following and enjoy PyFunceble!

::

   $ git clone https://github.com/funilrys/PyFunceble.git
   $ cd PyFunceble
   $ python3 setup.py test && python3 setup.py install

.. _the ArchWiki page: https://wiki.archlinux.org/index.php/AUR_helpers