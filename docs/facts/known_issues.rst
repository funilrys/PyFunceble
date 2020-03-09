Known issues
============

This is the list of issues which are not or will not be fixed (yet...).

* Under Travis CI the coloration may not be shown.
* Under GitLab CI/CD the coloration may not be shown.

* When using either Oracle's MySQL or MariaDB-Server you will have to be 
  either SUPER-PRIVILIDGED user (root) or be able to do 
  :code:`set global log_bin_trust_function_creators=1;` Read more about this 
  in the `components/databases`_

.. _components/databases:
