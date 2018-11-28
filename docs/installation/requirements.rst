Requirements
============

Here is the list of requirements:

-   Python 3.6+
-   :code:`colorama`
-   :code:`domain2idna`
-   :code:`PyYAML`
-   :code:`requests`
-   :code:`setuptools`
-   :code:`urllib3`

Python 3.6+
-----------

As we use for example ::

   print('hello', end=' ')

which does not exist in Python 2.x and as I wanted to give a priority to Python 3, Python 3 is required.

:code:`colorama`
----------------

As we use some coloration coloration, :code:`colorama` is required.

:code:`domain2idna`
-------------------

As we propose the conversion of domains to IDNA, :code:`domain2idna` is required.

.. note::
    :code:`domain2idna` is maintained and developed by `Nissar Chababy (@funilrys)`_, the main developer of PyFunceble.
    Its source code can be found `on GitHub`_.

.. _Nissar Chababy (@funilrys): https://github.com/funilrys
.. _on GitHub: https://github.com/funilrys/domain2idna

:code:`PyYAML`
--------------

As our configuration file is written in :code:`.yaml`, :code:`PyYAML` is required.

:code:`requests`
----------------

As we use :code:`requests` when calling all :code:`Lookup()` methods, :code:`requests` is required.

:code:`setuptools`
------------------

As we use :code:`install_requires=xx` inside our :code:`setup.py`, :code:`setuptools` is required.

:code:`urllib3`
---------------

You should normally already have it. But as we handle some of its errors while using :code:`requests`, :code:`urllib3` is required.
