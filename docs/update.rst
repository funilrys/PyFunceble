Update
======

Stable version
--------------

Using :code:`pip`
^^^^^^^^^^^^^^^^^

Choose your repository, install and enjoy PyFunceble!

From PyPi
"""""""""

::
 
   $ pip3 install --upgrade PyFunceble

From GitHub
"""""""""""

::

   $ pip3 install --upgrade git+https://github.com/funilrys/PyFunceble.git@master#egg=PyFunceble

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
    We do not recommend any AUR helper but keep in mind that some AUR helpers are "better" than other.
    For more information about your current (or any other) AUR helper please report to `the ArchWiki page`_.

::

    $ yourFavoriteAurHelper -Syu python-pyfunceble


Pure Python method
^^^^^^^^^^^^^^^^^^

Execute the following and enjoy PyFunceble!

::

   $ cd PyFunceble
   $ git checkout master && git fetch origin && git merge origin/master
   $ python3 setup.py test && python3 setup.py install


Development version
--------------------

For development
^^^^^^^^^^^^^^^^

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

Execute one of the following and enjoy PyFunceble!

**From PyPi**

::

   $ pip3 install --upgrade PyFunceble-dev

**From GitHub**

::

   $ pip3 install --upgrade git+https://github.com/funilrys/PyFunceble.git@dev#egg=PyFunceble


Using the AUR (for Arch Linux users)
""""""""""""""""""""""""""""""""""""

**With makepkg**

::

    $ wget https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=python-pyfunceble-dev
    $ makepkg
    $ sudo pacman -U python-pyfunceble-dev*.tar.xz

**With your favorite AUR helper**

.. warning::
    We do not recommend any AUR helper but keep in mind that some AUR helpers are "better" than other.
    For more information about your current (or any other) AUR helper please report to `the ArchWiki page`_.

::

    $ yourFavoriteAurHelper -Syu python-pyfunceble-dev

Pure Python method
""""""""""""""""""

Execute the following and enjoy PyFunceble!

::

   $ cd PyFunceble && git checkout dev
   $ git fetch origin && git merge origin/dev
   $ python3 setup.py test && python3 setup.py install


.. _the ArchWiki page: https://wiki.archlinux.org/index.php/AUR_helpers