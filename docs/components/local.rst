Test in/for local hostnames, IPs, components
--------------------------------------------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

As we may need to test for local hostnames, IPs, components in a local network, this component allows a less aggressive way of syntax validation.

How does it work?
^^^^^^^^^^^^^^^^^

We simply use a less aggressive syntax validation so that everything you give us is being tested.

How to use it?
^^^^^^^^^^^^^^

Simply change

::

   local:                   False

to

::

   local:                   True

into your personal :code:`.PyFunceble.yaml` or use the :code:`--local` argument from the CLI to activate it.