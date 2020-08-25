AdBlock/Filter list decoding
----------------------------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

As some people may want to test the content of their AdBlock/Filter list, we offer a way to decode them!

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here :func:`PyFunceble.converter.adblock.AdBlock.get_converted`!

We keep it simple by trying to comply with the `Adblock Plus filters explained`_ documentation.
For us, the relevant parts are the one which defines/explains which domains are being blocked from a given rule.

.. note::
    A more aggressive extraction might be planned in the future.


How to use it?
^^^^^^^^^^^^^^

You can simply change

::

    adblock: False

to

::

    adblock: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--adblock` argument from the CLI to activate it.


.. _Adblock Plus filters explained: https://adblockplus.org/filter-cheatsheet