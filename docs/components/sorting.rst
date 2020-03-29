
Sorting
-------

.. note::
    While using the multiprocessing option, the data are tested as given.

Why do we need it?
^^^^^^^^^^^^^^^^^^

Because sorted is better, we sort by default!

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here: :func:`~PyFunceble.engine.sort.Sort`!

Alphabetically
""""""""""""""

This is the default one. The default python :code:`sorted()` function is used for that purpose.

Hierarchically
""""""""""""""

The objective of this is to provide sorting by service/domains.

.. note::
    This is a simplified version of what we do.

1. Let's say we have :code:`aaa.bbb.ccc.tdl`.
    .. note::
        The TDL part is determined. Indeed we first look at the IANA Root Zone database, then at the Public Suffix List.

2. Let's split the points. We then get a list :code:`[aaa, bbb, ccc, tdl]`
3. Put the TDL first. It will gives us :code:`[tdl, aaa, bbb, ccc]`
4. Reverse everything after the TDL. It will gives us :code:`[tdl, ccc, bbb, aaa]`.
5. Get the string to use for sorting. It will gives us :code:`tdl.ccc.bbb.aaa`.


How to activate the hierarchical sorting?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simply change

::

    hierarchical_sorting: False

to

::

    hierarchical_sorting: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--hierarchical` argument from the CLI to activate it.
