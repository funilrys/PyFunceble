Directory Structure
-------------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

As we wanted the end-user to be able to work from everywhere into the filesystem,
we created a logic which will create and keep the :code:`output/` directory which complies
with our code.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here :func:`PyFunceble.output.constructor.Constructor`!

After each version, the maintainer does a :code:`--production` which will prepare the repository
for production.
That has the side effect to map the maintainer version of the :code:`output/`
directory into a file called :code:`dir_structure_production.json`.

Once pushed, on the end-user side, when testing for file, that file is downloaded into
a file called :code:`dir_structure.json` which is then used to restore/create a
a perfect copy of the output directory the maintainer had when pushing the new
version.

.. note::
    If you find yourself in a case that a directory is not found, please try first to
    delete the :code:`dir_structure*.json` files to force a resynchronization.


How to generate it manually?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can't. But using the :code:`--dir-structure` argument will do the job on purpose.