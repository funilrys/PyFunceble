How do Dead-Hosts work?
=======================

`Dead-Hosts`_ is like a wrapper of PyFunceble. Indeed, we use Travis CI
containers in order to test lists with PyFunceble.

Once a list is set up inside our infrastructure, PyFunceble will
test the list regularly and the Dead-Hosts infrastructure will produce a
:code:`clean.list` file which represents the list of domains/IP/URL
which remains or became :code:`ACTIVE`.

In addition, if needed, we can set up a list of GitHub username
to @ping once a new test is finished.

.. _Funceble: https://github.com/funilrys/funceble

.. _Dead-Hosts: https://github.com/dead-hosts