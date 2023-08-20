AdBlock/Filter list decoding
----------------------------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

As some people may want to test the content of their AdBlock/Filter list, we
offer a way to decode them!

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here:
    :class:`~PyFunceble.converter.adblock_input_line2subject.AdblockInputLine2Subject`!

We keep it simple by trying to comply with the
`Adblock Plus filters explained`_ documentation.
For us, the relevant parts are the one which defines/explains which domains
are being blocked from a given rule.

.. note::
    A more aggressive extraction might be planned in the future.


How to use it?
^^^^^^^^^^^^^^

You can simply change

::

    cli_decoding:
        adblock: False

        # Activate this only if you want to get as much as possible.
        aggressive: False

to

::

    cli_decoding:
        adblock: True

        # Activate this only if you want to get as much as possible.
        aggressive: False


into your personal :code:`.PyFunceble.yaml` or use the :code:`--adblock`
argument from the CLI to activate it.


.. _Adblock Plus filters explained: https://adblockplus.org/filter-cheatsheet