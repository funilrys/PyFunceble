Dead-Hosts as place to use PyFunceble!
======================================

Why Dead-Hosts?
----------------

We are conscient that PyFunceble may run for days, that's why we
offer you to request your list to be `tested at Dead-Hosts`_.

How do Dead-Hosts work?
---------------------------

`Dead-Hosts`_ is like a wrapper of PyFunceble. Indeed, we use Travis CI
containers in order to test lists with PyFunceble.

Once a list is set up inside our infrastructure, PyFunceble will
test the list regularly and the Dead-Hosts infrastructure will produce a
:code:`clean.list` file which represents the list of domains/IP/URL
which remains or became :code:`ACTIVE`.

In addition, if needed, we can set up a list of GitHub username
to @ping once a new test is finished.

History of  Dead-Hosts
-----------------------

The project started on 3rd March 2017 at `funilrys/dead-hosts`_.

The original idea was to test `Funceble`_ against hosts file in order
to find bugs inside `Funceble`_ but also letting me have a fewer long hosts file.

On 23rd January 2018, I (funilrys) decided to shut `funilrys/dead-hosts`_ down.
Indeed, as it became impossible to test all members of the project without having
to wait weeks, I decided that it was time to move to another level.

That was the beginning of `Dead-Hosts`_.

Today `Dead-Hosts`_'s objective is to provide to project/list maintainers or individuals 
- with the help of PyFunceble - more information about their favorite project/list or domains, IP or URL.


.. _tested at Dead-Hosts: https://github.com/dead-hosts/dev-center/issues/new?template=inclusion-request.md
.. _funilrys/dead-hosts: https://github.com/funilrys/dead-hosts
.. _Funceble: https://github.com/funilrys/funceble
.. _Dead-Hosts: https://github.com/dead-hosts