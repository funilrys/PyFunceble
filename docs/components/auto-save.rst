Autosave
========

Why do we need it?
------------------

This component comes along with the auto-continue one. 
Indeed, after constructing the logic to auto-continue we needed something to autosave. 

From now only Travis CI is supported but in the future another backup/saving logics
might be implemented.

How does it work?
-----------------

After a given amount of minutes, we stop the tool, generate the percentage, 
run a given command (if found), commit all the changes we made to the repository 
and finally, push to the git repository.

How to use it?
--------------

For Travis CI
^^^^^^^^^^^^^

The following (from the configuration) or their equivalent from the CLI are required.

::

    travis: False
    travis_autosave_commit: "Your awesome commit message"
    travis_autosave_final_commit: "Your awesome final commit message"
    travis_autosave_minutes: 15
    travis_branch: master
