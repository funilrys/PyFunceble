Autosave
--------

.. warning::
    This component is not activated by default.

Why do we need it?
^^^^^^^^^^^^^^^^^^

This component comes along with the auto-continue one.
Indeed, after constructing the logic to auto-continue we needed something to autosave.


How does it work?
^^^^^^^^^^^^^^^^^

.. note::
    Want to read the code ? It's here :func:`PyFunceble.engine.auto_save.AutoSave`!

After a given amount of minutes, we stop the tool, generate the percentage,
run a given command (if found), commit all the changes we made to the repository
and finally, push to the git repository.

How to use it?
^^^^^^^^^^^^^^

For Travis CI and GitLab CI/CD
""""""""""""""""""""""""""""""

The following (from the configuration) or their equivalent from the CLI are required.

::

    ci: False
    ci_autosave_commit: "Your awesome commit message"
    ci_autosave_final_commit: "Your awesome final commit message"
    ci_autosave_minutes: 15
    ci_branch: master

.. note::
    If you give the :code:`command` index something, we will run it at the end of each commits except the last one.

    The command on the last commit is executed based on the given :code:`command_before_end` index.
