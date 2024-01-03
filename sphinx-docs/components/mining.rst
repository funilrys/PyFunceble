Mining
------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

Sometimes you might, for example, want to get the list of domain(s) / URL(s) in
a redirecting loop. This feature reveals them.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here
    :class:`~PyFunceble.cli.processes.workers.miner.MinerWorker`!

We access the given domain/URL and get the redirection history which we then
test once we finished the normal test.


.. warning::
    This component might evolve with time.

How to use it?
^^^^^^^^^^^^^^

You can simply change

.. code-block:: yaml

    cli_testing:
        # Activates the mining of data.
        mining: False

to

.. code-block:: yaml

    cli_testing:
        # Activates the mining of data.
        mining: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--mining` argument
from the CLI to activate it.
