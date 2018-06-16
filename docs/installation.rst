Installation
############

Requirements
============

Here is the list of requirements:

-   Python 3.x
-   :code:`colorama`
-   :code:`requests`
-   :code:`PyYAML`

Python 3.x
----------

As we use for example ::

   print('hello', end=' ')

which does not exist in Python 2.x and as I wanted to give a priority to Python 3, Python 3 is required.

colorama
--------

As I wanted to add some coloration, I choose :code:`colorama` for the job as it offers a portable solution.

requests
--------

As we use :code:`requests` when calling all :code:`Lookup()` methods, :code:`requests` is required.

PyYAML
------

As our configuration file is written in :code:`.yaml`, :code:`PyYAML` is required.

--------------------------------------------------------

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


Pure Python method
^^^^^^^^^^^^^^^^^^

Execute the following and enjoy PyFunceble!

::

   $ git clone https://github.com/funilrys/PyFunceble.git
   $ cd PyFunceble
   $ python3 setup.py test && python3 setup.py install


Developement version
--------------------

The developement version of PyFunceble represents the :code:`dev` branch.
It's intended for the developement of next features but is always at a usable state.

Indeed, We should not push to the :code:`dev` branch until we are sure that the new commit does not break or introduce critical issue under PyFunceble.

For developpement
^^^^^^^^^^^^^^^^^

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



Pure Python method
""""""""""""""""""

Execute the following and enjoy PyFunceble!

::

   $ git clone https://github.com/funilrys/PyFunceble.git
   $ cd PyFunceble && git checkout dev
   $ python3 setup.py test && python3 setup.py install

--------------------------------------------------------

First steps
===========


Make sure that you can run 

::

   $ PyFunceble --version

and enjoy PyFunceble!!

