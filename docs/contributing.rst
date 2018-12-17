Contributing
============

I'm really glad you're reading this because we need contributions to make this tool one of the best tool on the Internet!


Submitting changes
------------------

Before anything, please keep in mind the following. If one or more of those conditions are not filled. Your Pull Request to PyFunceble may not be merged.

The :code:`master` branch is used only for releasing a new or stable version of the code. That's why we require that all contributions/modifications must be done under the :code:`dev` or a new branch.

In order to gain some time and also understand what you are working on, your pull requests submission as long as your commit descriptions should be clear and complete as much as possible. We do an exception to commit with minor changed but big changes should have a complete description. Please ensure to use the following method when committing a big change.

Steps before commit
^^^^^^^^^^^^^^^^^^^

.. note::

    The following do not apply if you do not touch the :code:`PyFunceble` nor the :code:`tests` directory.

::

    $ # We format our code.
    $ black PyFunceble && black tests/*.py
    $ # We lint our code. Please make sure to fix all reported issues.
    $ pylint PyFunceble && pylint tests/*.py
    $ # We check the tests coverage. Please ensure that at lease 95% of the code is covered.
    $ coverage run setup.py test && coverage report -m
    $ # Prepare our files, :code:`version.yaml` and code for pushing.
    $ PyFunceble --production

The commit
^^^^^^^^^^

::

    $ # There paragraph is optional if your changes/commits are obvious.
    $ git commit -S -m "A summary of the commit" -m "A paragraph
    > or a sentence explaining what changed, why and its impact."

All your commits should be signed with **PGP**. (More information can be found on `GitHub documentation`_)

Please note the usage of :code:`-S` into the commit command which means that we sign the commit.
The usage of :code:`PyFunceble --production` update :code:`version.yaml` and :code:`directory_structure_production.json` automatically.

Coding conventions
------------------

- We make sure that a method, a function, and a class **have doctrings**.
- One line should not exceed 79 characters for docstring and 100 characters for long declaration/assignment.
  - Exception granted for regular expressions or long string assignment.
- We use `Black`_, *The uncompromising Python code formatter*, to format our code.
- Our code should pass :code:`pylint PyFunceble && pylint tests/*.py` with at least a score of 10.00/10.00
- We do not forget to follow the steps before any commits.

.. _GitHub documentation: https://github.com/blog/2144-gpg-signature-verification
.. _Black: https://github.com/ambv/black