The commit
==========

::

    $ # There paragraph is optional if your changes/commits are obvious.
    $ git commit -S -m "A summary of the commit" -m "A paragraph
    > or a sentence explaining what changed, why and its impact."

All your commits should be signed with **PGP**. (More information can be found on `GitHub documentation`_)

Please note the usage of :code:`-S` into the commit command which means that we sign the commit.
The usage of :code:`PyFunceble --production` update :code:`version.yaml` and :code:`directory_structure_production.json` automatically.

.. _GitHub documentation: https://github.com/blog/2144-gpg-signature-verification
