Percentage
----------

.. warning::
    This component is activated by default while testing files.

.. note::
    The percentage doesn't show up - by design - while testing for single domains (whilst using :code:`--domain`).


Why do we need it?
^^^^^^^^^^^^^^^^^^

We need it in order to get information about the amount of data we just tested.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here :func:`PyFunceble.output.percentage.Percentage`!

Regularly or at the very end of a test we get the number of subjects for each status along with the number of tested subjects.
We then generate and print the percentage calculation on the screen (:code:`stdout`) and into :code:`output/logs/percentage/percentage.txt`

How to use it?
^^^^^^^^^^^^^^

It is activated by default, but if not please update

::

    show_percentage: False

to

::

    show_percentage: True


into your personal :code:`.PyFunceble.yaml` or use the :code:`--percentage` argument from the CLI to reactivate it.
