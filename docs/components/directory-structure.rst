Directory Structure
-------------------

Why do we need it?
^^^^^^^^^^^^^^^^^^

As we wanted the end-user to be able to work from everywhere into the filesystem,
we created a logic which will create and keep the :code:`output/` directory which
complies with our source code.

How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ?
    It's here
    :class:`PyFunceble.cli.filesystem.dir_structure.backup.DirectoryStructureBackup`
    and
    :class:`PyFunceble.cli.filesystem.dir_structure.backup.DirectoryStructureRestoration`!

After each version, the maintainer run the :code:`production-pyfunceble` CLI
which will prepare the repository for production.

That has the side effect to map the maintainer's version of the
:code:`output/__pyfunceble_origin__` directory into a file called
:code:`dir_structure_production.json` which is then bundled into the PyPI
package.

Once pushed, on the end-user side, when testing for file, that file is
copied from the Python Package into
a file called :code:`dir_structure.json` which is then used to restore/create a
a perfect copy of the output directory the maintainer had when pushing the new
version.

