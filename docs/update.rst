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


Pure Python method
^^^^^^^^^^^^^^^^^^

Execute the following and enjoy PyFunceble!

::

   $ cd PyFunceble
   $ git checkout master && git fetch origin && git merge origin/master
   $ python3 setup.py test && python3 setup.py install


Developement version
--------------------

For developpement
^^^^^^^^^^^^^^^^^

::

   $ cd PyFunceble && git checkout dev
   $ git fetch origin && git merge origin/dev
   $ . venv/bin/activate && pip3 install -e .

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



Pure Python method
""""""""""""""""""

Execute the following and enjoy PyFunceble!

::

   $ cd PyFunceble && git checkout dev
   $ git fetch origin && git merge origin/dev
   $ python3 setup.py test && python3 setup.py install

